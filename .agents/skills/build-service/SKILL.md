---
name: build-service
description: Implement or repair a usable service from confirmed acceptance criteria using the existing stack. Covers a working UI/API/data path and meaningful error handling; use only when the requested artifact is a service or application.
---

# 승인한 범위의 서비스 구현

새 업무의 상세 브리핑과 사용자 계획 확인이 끝났는지 확인한다. 직접 호출됐더라도 결과물·사용 흐름·기능/예외·구조·기술 대안·검증·시간을 설명한 뒤 확인받는다. 같은 범위의 통상 구현/오류 수정은 반복 승인받지 않는다.

## 최소 경로부터

1. 실제 실행 명령·의존성·데이터 계약과 기존 코드를 확인한다. 예시 앱 전체를 먼저 읽거나 복사하지 않는다. 새 뼈대가 필요할 때만 [선택 기준](references/starter-selection.md)을 읽는다.
2. 사용자 입력→서버/계산→출력/저장 하나를 먼저 연결한다. 정상·빈 결과·잘못된 입력·실패 상태, 실제 재조회/저장과 필요한 접근 제어를 구현한다.
3. [코드 이해 기준](references/code-understanding.md)에 따라 핵심 파일/함수·분기·수식·상태에 상세한 한국어 주석을 남긴다. 입력/단위·반환값·이유·부작용·예외와 필요한 문법을 설명한다.
4. 중요한 정상/경계/실패를 기존 도구로 검사한다. 검사 전 목적/성공 조건, 검사 후 입력·기대/실제값·판정·범위를 알린다. 새 핵심 테스트에도 준비→실행→비교의 이유를 설명한다.

## 조건부 참고 자료

| 현재 기능/상황 | 읽을 기준 |
| --- | --- |
| 서버 접속·상태/API 안내·외부 미리보기 | [실행 환경](references/service-access.md) |
| 결과 선택·최적화·추천/점수 | [강제 조건·목표·대안·민감도](references/decision-criteria.md) |
| 오래 걸리는 작업·배경 계산 | [중복·실패·재시작·결과 게시](references/background-work.md) |
| 페이지 이동/외부 창 등이 제한된 UI | [환경 호환성](references/ui-compatibility.md) |
| 서비스 설명서 작성/구조 변경 | [SERVICE.md 기준](references/service-document.md) |

실제 업무 폴더에 SERVICE.md를 작성하며 업무 README는 보존한다. 유스케이스·구성도·화면/API 라우팅·모듈 계약·규칙·실행/검증·효과/한계·읽는 순서를 현재 코드에 연결한다. 관련 없는 구획과 미사용 기술은 채우지 않는다. probe에는 선택 이유/핵심 결과, devlog에는 실제 사건만 연결한다.

사용자와 합의한 변경 중단 시점까지 구현·검증·설명 자료를 준비한다. 이후에는 읽기/설명만 진행하며 수정 요청이 있으면 이해 시간 영향을 알리고 요청 범위만 다룬다.
