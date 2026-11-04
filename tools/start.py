#!/usr/bin/env python3
"""Install task skills and open the provided Codex with the short task-start request."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
from bootstrap import prepare


def launch(target, codex=None):
    executable = codex or shutil.which('codex')
    if not executable:
        raise ValueError('provided codex executable not found; use the platform terminal and report the issue')
    handoff = prepare(target)
    prompt = ('$solve-task ' + json.dumps(handoff['entry_path'], ensure_ascii=False)
              + ' 파일을 읽고 기본 업무 시작 흐름을 실행해줘. '
              + '담당자 답변 반영 뒤 구현 전 상세 브리핑을 제시하고 사용자가 계획을 확인할 때까지 구현을 기다려줘. '
              + '현재 업무 일정에 맞춰 첫 인계·보완 종료·변경 없는 이해 구간을 합의해줘. '
              + ('스킬은 공개 원본을 직접 참조하는 모드이며 앱 뼈대 복사는 --templates-only를 사용해줘. '
                 if handoff['mode'] == 'reference' else ''))
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
