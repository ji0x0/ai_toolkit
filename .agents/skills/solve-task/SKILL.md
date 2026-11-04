---
name: solve-task
description: Guide a practical task through problem framing, stakeholder answers, a detailed implementation briefing and user confirmation, then implementation and verification with devlog/probe updates and local snapshots. Use for a new task or 업무 시작해줘; not for a general toolkit question.
---

# 문제 분석부터 인계까지

`$solve-task` 또는 “업무 시작해줘”로 시작한다. 기존 README·AGENTS·코드·제공 자료와 실제 업무 루트를 먼저 확인한다. 키트 자체를 업무 대상으로 삼지 않는다.

## 시작과 합의

1. [자동 세션](references/automatic-session.md)으로 기록/로컬 사본을 준비한다. 실행 성공을 실제 상태로 확인한다.
2. [담당자 대화](references/discovery-dialogue.md)에 따라 사용자 역할·목표·페인포인트·원인 근거·완료 기준을 정리한다. 답이 없는 핵심 규칙만 질문하고, 이미 답변/승인이 있는 단계는 반복하지 않는다.
3. 답변을 반영해 [구현 전 브리핑](references/implementation-brief.md)을 채팅에 자세히 제시한다. 결과물·사용 흐름·기능/예외·설계·기술/대안·검증·시간을 설명하고 **이 계획에 대한 사용자 확인** 뒤 구현한다. 대기 중에는 독립적인 자료 확인만 계속한다.
4. [시간 합의](references/time-budget.md)에서 첫 인계·보완 종료·변경 없는 이해 구간을 정한다. 현재 사용자 지시나 업무 지침의 일정을 사용하며 특정 기간을 가정하지 않는다.

## 필요한 작업만 실행

- 기존 스택을 우선하고 [업무 유형](references/task-profiles.md)에 맞는 최소 범위를 정한다. 앱 뼈대는 승인된 계획에 필요한 모듈만 적용한다.
- 구현은 `build-service`, 데이터는 `analyze-data`, 검증은 `verify-result`, 이해/인계는 `explain-work`를 해당 단계에만 읽는다. 미설치라면 같은 역할을 직접 수행한다. 시작할 때 모든 참고 문서와 예시 앱을 읽지 않는다.
- 테스트 전 목적·입력/기대값을 알리고, 실행 후 실제 결과·판정·한계·케이스 위치를 쉬운 한국어로 설명한다. 실제 코드/출력을 근거로 하며 미실행을 통과로 쓰지 않는다.
- 핵심 함수에 한국어 설명 주석과 대표 입력의 읽는 순서를 준비한다. 구조·규칙·예외·검증·기술 선택을 본인이 추적할 수 있게 한다.
- `record-work`에 따라 의미 있는 결정/변경/검사 뒤 해당 문서 구획만 갱신한다. 변동 없는 설명 턴마다 세 문서를 다시 쓰지 않는다. 업무 README는 보존한다.
- 같은 승인 범위의 통상 구현·검사·수정은 계속한다. 사용자에게 보이는 결과·업무 정책·저장/API 계약·구조·일정이 크게 달라질 때만 변경 부분을 브리핑하고 확인받는다.
- 범위/오류/실행 시간으로 추정이 달라지면 현재 상태·남은 시간·인계 영향을 알린다. 설명이나 확인 질문마다 새 견적을 붙이지 않는다.
- 변경 중단 시점부터 코드/설정/테스트·장시간 문서 확장을 멈추고 입력 예측→코드 추적→기존 결과 대조→본인 설명을 지원한다. 발견한 문제는 수정 후보로 남긴다.

외부 연결이 실제로 부족할 때만 [도구 연결](references/tool-connections.md)을 읽는다. 자료·자격 증명·외부 전송은 현재 업무의 허용 범위 안에서 다룬다. 인계 시 [마무리 기준](references/handoff-guidance.md)으로 필수 산출물·실행/검증·저장 상태와 남은 한계를 확인한다.
