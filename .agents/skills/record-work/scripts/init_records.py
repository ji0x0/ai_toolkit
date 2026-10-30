#!/usr/bin/env python3
"""Create devlog.md and probe.md without overwriting existing documents."""
import argparse
from pathlib import Path
import sys

DEVLOG = """# devlog.md — 실제 개발·검증 이력

기록 시각은 시간대를 표시한다. 현재 단계·요구·판단·변경·검증·한계를 실제 근거로 기록한다.
이 양식 생성 자체는 구현·검증·사용자 이해 완료의 근거가 아니다.

## 현재 상태

- 과제·관련 요구: 미확인
- 구현 인계 목표: 기본 T+60분, 지연 시 T+80분 목표. 실제 과제 제약에 맞춰 확인한다.
- 이해·검증 구간: 기본 T+60~170분, 지연 시 T+80~170분. 제출 10분은 별도다.
- 현재 기능·검증·사용자 확인: 아직 기록 없음
- 다음 행동: 실제 README·제공 파일과 기존 지침 확인

## 사건 이력

실제 사건이 생기면 시각/경과시간, 목적, 변경 파일·함수, 선택 이유,
검증 명령·입력·기대값·실제 결과·상태·근거 위치, 사용자 확인 범위,
남은 한계와 다음 행동을 덧붙인다. 과거 재구성은 ‘사후 정리’로 표시한다.
"""

PROBE = """# probe.md — 현재 기능·기술 선택·이해와 검증

이 문서는 현재 코드를 근거로 갱신한다. 아직 구현·실행·사용자 확인하지 않은 내용을 완료로 쓰지 않는다.

## 요구·기능 목록

| ID | 기능·관련 요구 | 구현 위치·상태 | 선택 결정 | 검증 근거 | 사용자 이해 확인 |
| --- | --- | --- | --- | --- | --- |

현재 기능 목록: 아직 코드 확인 전.

## 공통 환경과 직접 의존성

실제 확인한 실행 환경·버전·의존성·제약과 근거를 기록한다. 확인하지 않은 버전은 미확인으로 둔다.

## 기능별 설명

각 기능마다 요구·입출력·구현 위치·상태, 선택한 도구/라이브러리,
동일 기능의 현실적 대안, 선택안/대안의 장점·단점·적용 조건,
최종 선택 이유·감수한 한계·전환 조건을 기록한다.
실제 검증 명령·사례·기대값·결과와 읽을 코드 순서도 연결한다.

## 사용자 이해·직접 검증

입력 결과 예측 → 코드 추적 → 직접 실행·대조 → 본인 설명으로 확인한다.
사용자 확인 상태: 확인 대기. 실제 답변과 실행 확인 뒤에만 범위를 갱신한다.

## 미구현·미검증·남은 한계

아직 확인한 내용 없음. 실제 구현/검증 뒤에 근거와 함께 작성한다.
"""


def validate_target(root):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError('task root must be an existing directory')
    if any((p / '.toolkit-package').is_file() for p in (root, *root.parents)):
        raise ValueError('choose the actual task workspace, outside the toolkit distribution')
    # Validate both paths before creating either file.
    for name in ('devlog.md', 'probe.md'):
        p = root / name
        if p.is_symlink() or (p.exists() and not p.is_file()):
            raise ValueError('document path is not a regular file: ' + name)
    return root


def initialize(root):
    root = validate_target(root)
    documents = [('devlog.md', DEVLOG), ('probe.md', PROBE)]
    result = []
    for name, body in documents:
        p = root / name
        try:
            with p.open('x', encoding='utf-8') as f:
                f.write(body)
            action = 'created'
        except FileExistsError:
            action = 'preserved'
        result.append((name, action))
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', default='.')
    p.add_argument('--check', action='store_true', help='validate target without creating files')
    a = p.parse_args()
    try:
        if a.check:
            validate_target(a.root)
            print('task workspace ready')
            return 0
        for name, action in initialize(a.root):
            print(action + ' ' + name)
    except (OSError, ValueError) as e:
        print('ERROR: ' + str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
