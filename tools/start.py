#!/usr/bin/env python3
"""Install task skills and open the provided Codex with the short task-start request."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
from install import SOURCE, install


def launch(target, codex=None):
    executable = codex or shutil.which('codex')
    if not executable:
        raise ValueError('provided codex executable not found; use the platform terminal and report the issue')
    names = sorted(path.name for path in SOURCE.iterdir() if (path / 'SKILL.md').is_file())
    # The skill reads task instructions before deciding whether extra record files are allowed.
    install(target, names, apply=True, create_records=False)
    prompt = '$solve-task .agents/skills/solve-task/SKILL.md를 읽고 기본 과제 시작 흐름을 실행해줘.'
    return subprocess.call([executable, prompt], cwd=Path(target).resolve())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', default='.')
    args = parser.parse_args()
    try:
        return launch(args.target)
    except (OSError, ValueError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
