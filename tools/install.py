#!/usr/bin/env python3
"""Preview or install selected repository-scoped skills, preserving existing content."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

SOURCE = Path(__file__).resolve().parents[1] / '.agents' / 'skills'


def identical(a, b):
    def files(root):
        return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*')
                if p.is_file() and '__pycache__' not in p.relative_to(root).parts
                and p.suffix != '.pyc' and p.name != '.DS_Store'}
    aa, bb = files(a), files(b)
    return aa == bb


def run_records(target, check_only=False):
    command = [sys.executable, str(SOURCE / 'record-work/scripts/init_records.py'), '--root', str(target)]
    if check_only:
        command.append('--check')
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        raise ValueError(result.stderr.strip() or 'could not initialize task records')


def install(target, names, apply=False, create_records=True):
    target = Path(target).resolve()
    if not target.is_dir():
        raise ValueError('target directory must already exist')
    package_root = SOURCE.parents[1]
    if target == package_root or package_root in target.parents:
        raise ValueError('install into the actual task workspace, outside the toolkit distribution')
    dest = target / '.agents' / 'skills'
    for p in (target / '.agents', dest):
        if p.is_symlink():
            raise ValueError('installation directory must not be a symlink')
    plan = []
    for name in names:
        if Path(name).name != name or name in {'.', '..'} or not (SOURCE / name / 'SKILL.md').is_file():
            raise ValueError('unknown skill: ' + name)
        d = dest / name
        if d.is_symlink() or (d.exists() and (not d.is_dir() or not identical(SOURCE / name, d))):
            raise ValueError('existing different skill preserved; nothing installed: ' + str(d))
        plan.append((name, 'unchanged' if d.exists() else 'install'))
    wants_records = create_records and bool({'solve-task', 'record-work'} & set(names))
    if wants_records:
        run_records(target, check_only=True)
    if apply:
        dest.mkdir(parents=True, exist_ok=True)
        for name, action in plan:
            if action == 'install':
                shutil.copytree(SOURCE / name, dest / name,
                                ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
        if wants_records:
            run_records(target)
    return plan


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--target', default='.')
    p.add_argument('--skills', nargs='+')
    p.add_argument('--apply', action='store_true')
    p.add_argument('--skip-records', action='store_true', help='install skills without creating task records')
    a = p.parse_args()
    names = a.skills or sorted(p.name for p in SOURCE.iterdir() if (p / 'SKILL.md').exists())
    try:
        for name, action in install(a.target, names, a.apply, not a.skip_records):
            print(('APPLIED' if a.apply else 'PREVIEW') + ' ' + action + ' ' + name)
        if not a.skip_records and {'solve-task', 'record-work'} & set(names):
            print(('APPLIED' if a.apply else 'PREVIEW') + ' task records: devlog.md, probe.md')
    except (OSError, ValueError) as e:
        print('ERROR: ' + str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
