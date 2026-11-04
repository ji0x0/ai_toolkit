#!/usr/bin/env python3
"""Create devlog.md and probe.md without overwriting existing documents."""
import argparse
from pathlib import Path
import sys

DEVLOG = """# devlog.md — 실제 업무 이력

양식 생성은 구현·검증·이해 완료의 근거가 아니다. 실제 사건이 있을 때만 추가한다.

## 현재 상태

- 업무/필수 결과·실제 시작/마감: 확인 전
- 현재 단계·열린 질문/사용자 판단: 확인 전
- 구현 계획/확인 범위: 상세 브리핑 전, 사용자 확인 없음
- 첫 인계·보완 종료·변경 없는 이해 구간: 현재 사용자/업무 지침으로 합의 전
- 현재 구현/검증·남은 한계·다음 행동: 아직 없음

## 사건 이력

시각/시간대 또는 확인한 경과, 목적/결정, 실제 변경 파일:함수·이유,
검사 목적/케이스·명령·입력·기대값/근거·실제 결과·판정·환경/변경 상태,
사용자 직접 확인 범위·남은 한계/다음 행동을 남긴다.

AI 협업은 실제 증상/전달→원인 가설/수정안→채택/수정 요청/기각과 근거→재확인으로 연결한다.
담당자 답변과 설계 승인을 구분하고 AI 실행을 사용자 수행으로 기록하지 않는다.
실패 이력을 덮어쓰지 않으며 사후 정리는 그 사실과 근거를 표시한다.
같은 긴 설명은 복제하지 않고 probe/SERVICE의 실제 위치로 연결한다. 변동 없는 설명 턴에는 새 사건을 만들지 않는다.
"""

PROBE = """# probe.md — 문제·선택·핵심 근거

확인한 자료·현재 코드·실행 근거를 연결한다. 미확인/미구현/미실행을 완료로 쓰지 않는다.

## 현재 업무와 합의

- 문제 상황·업무 목표/필수 결과·범위/제약·근거: 확인 전
- 실제 시작/마감·첫 인계·보완 종료·변경 없는 이해 구간: 합의 전
- 현재 단계·열린 질문·다음 행동: 확인 전
- SERVICE.md의 구조/계약/검사 상세·devlog 사건 위치: 아직 없음

## 사용자·문제·해결 연결

| 실제 역할/목표·업무 맥락 | 페인포인트/영향 | 원인·근거/가설 | 해결 원리·기능/성공 기준 |
| --- | --- | --- | --- |

제공 자료·답변/관측으로 확인한 역할과 원인만 적는다. 근거 없는 인물 설정·개선율을 만들지 않는다.

## 질문·답변과 사용자 판단

| 질문/쟁점·이유/우선순위 | 실제 답변/출처 또는 대기 | 선택지/장단점·사용자 결정 | 구현/검증/일정 영향 |
| --- | --- | --- | --- |

## 구현 전 브리핑과 확인

- 계획/버전·제안 결과물·사용 흐름·기능/입출력/예외·수용 사례: 작성 전
- 구조/데이터·추천 기술/대안/장단점·변경 예정 위치: 작성 전
- 검증/주석/읽는 지도·예상 시간·인계/이해 영향: 작성 전
- 실제 설명 시점·사용자 응답·확인 범위/상태: 아직 없음
- 계획 대비 현재 구현 차이·중요한 변경/재확인: 아직 없음

담당자 답변·내부 계획·침묵을 설계 승인으로 쓰지 않는다. 같은 승인 범위는 재확인하지 않는다.

## 기능과 선택 근거

| 기능/연결 문제·입력→출력 | 현재 파일:함수·상태 | 채택 기술/방식·현실적 대안·각 장단점 | 선택 이유/포기한 점·검증/상세 위치 |
| --- | --- | --- | --- |

공통 선택은 한 번 기록하고 참조한다. 최적화 기준/강제 조건·독립 검사·배경 작업 수명·조건 변화는 해당 기능일 때만 보완한다.
현재 사용 기술/버전은 실제 확인 근거를 적는다. 설계상 예상과 실제 비교 실행을 구분한다.

## 테스트 설명과 현재 결과

- 코드/입력/설정·환경·시각 기준과 실행/통과/실패/생략 집계: 아직 미실행

| 무엇을 왜 검사하나·케이스 위치 | 입력/조건 | 기대값/근거 | 실제 결과·판정 | 범위/한계·다음 조치·상세 위치 |
| --- | --- | --- | --- | --- |

실제 준비 입력·호출·비교(assert)와 출력을 읽어 쉽게 설명한다. 미실행/생략/수동 대기와 검사 자체의 실패를 구분한다.
SERVICE에 검사 상세가 있으면 여기에는 핵심과 위치만 연결하고, 명령/실패/수정 이력은 devlog를 가리킨다.

## AI 협업 판단·사용자 이해·한계

실제 제안/가설→사용자 직접 확인→채택/수정 요청/기각의 이유→재확인을 관련 기능/devlog 사건에 연결한다.
없는 기각 사례나 사용자 행동을 만들지 않는다. 별도 필수 협업 문서가 있으면 그 의무 형식을 유지한다.

이해는 입력 예측→코드/주석 추적→기존 검사 대조→본인 설명에서 실제 확인한 범위만 적는다. 현재 상태는 확인 대기다.

| 미구현/미검증·업무 효과 미측정 | 사용자 영향 | 우선순위/이유 | 다음 확인 입력·지표/방법 |
| --- | --- | --- | --- |
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
