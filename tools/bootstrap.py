#!/usr/bin/env python3
"""Install skills and return a handoff for the already-running coding agent."""
import argparse
import json
from pathlib import Path
import re
import sys
from install import SOURCE, install


def catalog():
    result = []
    for path in sorted(SOURCE.glob('*/SKILL.md')):
        match = re.match(r'\A---\n(.*?)\n---\n', path.read_text(encoding='utf-8'), re.S)
        fields = dict(re.findall(r'^(name|description):\s*(.+)$', match[1], re.M)) if match else {}
        name, description = fields.get('name'), fields.get('description')
        if name != path.parent.name or not description:
            raise ValueError('invalid skill metadata: ' + str(path))
        result.append({'name': name, 'description': description})
    if not result or not any(skill['name'] == 'solve-task' for skill in result):
        raise ValueError('solve-task entry skill is missing')
    return result


def prepare(target):
    target = Path(target).resolve()
    skills = catalog()
    # Read task instructions before allowing extra record files or starting a watcher.
    plan = install(target, [skill['name'] for skill in skills], apply=True, create_records=False)
    actions = dict(plan)
    for skill in skills:
        skill['path'] = str(target / '.agents/skills' / skill['name'] / 'SKILL.md')
        skill['action'] = actions[skill['name']]
    entry = target / '.agents/skills/solve-task/SKILL.md'
    return {
        'status': 'ready',
        'target': str(target),
        'toolkit': str(SOURCE.parents[1]),
        'continue_in_current_session': True,
        'skills': skills,
        'entry_skill': 'solve-task',
        'entry_path': str(entry),
        'task_instruction_paths': [str(target / name) for name in ['AGENTS.md', 'README.md'] if (target / name).is_file()],
        'next_instruction': (
            '현재 Codex 대화를 유지한다. '
            '새 Codex를 실행하지 말고 entry_path의 SKILL.md를 실제로 읽어 참조 문서와 기본 흐름을 적용한다. '
            '사용자가 현재 대화에 제공한 문제 상황·해결 과제를 우선하고 과제 README와 기존 지침을 확인한다. '
            '정보가 없으면 문제 설명을 간단히 요청한다. '
            '과제 제약을 확인한 뒤 기록·자동저장을 준비하고, 먼저 담당자 질문을 제안해 확인한 답변을 기다린다.'
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, help='actual task root; keep it separate from the toolkit clone')
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.target), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
