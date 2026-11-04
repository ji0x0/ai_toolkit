# AI Toolkit

담당자와 업무 문제를 확인하고 구현·검증·코드 이해·인계까지 이어가는 Codex 스킬과 선택형 앱 뼈대입니다.

## 시작

실제 업무 폴더에서 제공된 Codex를 열고 입력합니다.

```text
https://github.com/ji0x0/ai_toolkit 를 설치해서 스킬을 파악하고 시작해줘.
```

[BOOTSTRAP.md](BOOTSTRAP.md)에 따라 키트를 `/tmp/ai_toolkit`에 받고 실제 업무 루트를 유지합니다. 스킬 폴더 쓰기가 제한되면 공개 원본을 직접 읽는 참조 모드를 사용합니다. 반환된 solve-task/SKILL.md를 현재 대화에서 읽고 이어가며 Codex를 다시 실행하지 않습니다. 이 요청은 에이전트가 해석하는 절차입니다.

일반 터미널에서 시작하는 대안:

```sh
git clone --depth 1 https://github.com/ji0x0/ai_toolkit.git /tmp/ai_toolkit
python3 /tmp/ai_toolkit/tools/start.py --target .
```

기존 `.agents`·README·AGENTS·소스·기록이 다른 내용이면 덮어쓰지 않고 충돌을 알립니다. 네트워크/권한/디스크 오류와 참조 모드를 구분합니다. 모델·인증·제공 도구의 버전/전역 설정은 바꾸지 않습니다.

## 진행 방식

1. 사용자/업무 문제·제공 자료·현재 코드·필수 결과와 미확인 규칙을 확인합니다. 필요한 담당자 질문만 제안하고 실제 답변을 반영합니다.
2. 예상 화면/결과물·사용 흐름·기능/예외·설계·기술 대안·테스트·시간을 상세 브리핑합니다. 새 계획에 대한 사용자 확인 후 구현합니다.
3. 승인된 범위의 구현·검증·수정은 계속합니다. 중요한 결과/정책/계약/구조/일정 변경에만 다시 확인받습니다.
4. 업무별 첫 인계·보완 종료·변경 없는 코드 이해 구간을 합의합니다. 인계가 늦어져도 이해 시간을 임의로 개발에 쓰지 않습니다.
5. 대표 입력을 예측하고 실제 코드·주석·테스트 결과를 추적해 본인 설명으로 이해를 확인합니다.

시작 시 모든 참고 문서나 예시 앱을 읽지 않습니다. 해당 단계의 스킬과 기능에 필요한 자료만 읽고, 문서는 의미 있는 변경이 생긴 구획만 갱신합니다. [시간/이해 운영](docs/UNDERSTAND_AND_VERIFY.md)을 참고합니다.

## 스킬

| 호출 | 역할 |
| --- | --- |
| `$solve-task` | 문제/질문·답변·브리핑·계획 확인·필요 단계 연결 |
| `$build-service` | 최소 기능 경로·UI/API/저장·서비스 문서 |
| `$analyze-data` | 데이터 의미/품질·분할·분석/모델 근거 |
| `$verify-result` | 독립 검증·반례/민감도·실패 조사·결과 설명 |
| `$explain-work` | 입력 예측·코드/주석/검사 추적·선택 이유와 한계 |
| `$record-work` | 현재 설명과 실제 사건을 필요한 구획에 기록 |
| `$git-checkpoint` | Git 컨벤션·로컬 사본·복구 |

자동 발견이 안 되면 실제 설치/참조 경로의 solve-task/SKILL.md를 읽고 실행하도록 요청합니다. 목록이 준비됐다는 것과 모든 스킬이 실행됐다는 것은 구분합니다.

## 업무 기록과 테스트

| 문서 | 정본으로 관리할 내용 |
| --- | --- |
| devlog.md | 실제 질의응답·결정·변경·실패/수정·실행의 시간순 사건 |
| probe.md | 사용자/문제·원인 근거·기능 선택/대안·핵심 검증·한계 |
| SERVICE.md | 서비스 구조·유스케이스·라우팅/모듈 계약·API/운영·검사 상세·읽는 지도 |

설치/자동 세션은 devlog와 probe 양식을 준비하고, SERVICE는 실제 서비스 작업 때 작성합니다. 업무 README는 보존합니다. 같은 긴 내용을 세 번 복제하지 않으며 변동 없는 설명 턴에는 다시 쓰지 않습니다. 기존 문서와 추가 파일 제한을 따릅니다.

핵심 함수·분기/계산·비동기 상태에 상세한 한국어 주석을 남깁니다. 입력/단위·반환값·이유·부작용/예외와 처음 보는 문법을 설명합니다. [코드 이해 기준](.agents/skills/build-service/references/code-understanding.md)을 사용합니다.

테스트 전 무엇을 왜 검사하고 어떤 결과를 기대하는지 알립니다. 실행 뒤 **목적·입력·기대값/근거·실제값·판정·범위/한계**를 설명하고 케이스/명령에 연결합니다. 독립 검사기에 잘못된 합성 결과를 넣어 규칙 위반을 잡는지도 확인합니다. 미실행·생략·수동 확인 대기를 통과로 쓰지 않습니다. [테스트 설명 기준](.agents/skills/verify-result/references/test-explanation.md)을 참고합니다.

## 앱 뼈대는 필요한 경우에만

기존 앱을 우선합니다. 소수 파일로 충분하면 작은 구현을 직접 만들고, 뼈대가 더 빠를 때만 필요한 프로필/모듈을 선택합니다. 전체 예시 앱을 기본 설치하지 않습니다.

| 프로필 | 실제 포함한 예시 |
| --- | --- |
| frontend | React·TypeScript·Vite, 기록/CSV·문서 탐색 UI |
| api | FastAPI·SQLite와 분석/RAG API 모듈 |
| data | CSV 품질·ML 분류/회귀·예측·시계열 기준선 |
| rag | BM25 검색·근거 인용·발췌·선택형 생성기 연결 |
| fullstack | 위 앱과 Docker·Compose·Makefile·CI |

API 프로필도 분석/RAG 예시를 포함합니다. 이 기능들이 불필요하면 전체 프로필 대신 작은 서버를 구현합니다. 채택한 코드만 결과물에 남기고, 미사용 예시까지 설명 대상으로 늘리지 않습니다. 외부 AI 연결·인증/조직 권한·대규모 작업 큐·운영 복구는 요구에 따라 구현합니다.

설치 검토/적용 예:

```sh
python3 /tmp/ai_toolkit/tools/install.py --target . --profile api
python3 /tmp/ai_toolkit/tools/install.py --target . --profile api --apply
```

스킬 설치가 제한된 참조 모드에서는 `--templates-only`로 앱 코드만 복사합니다. [모듈/실행 안내](docs/APP_STARTERS.md)와 [선택 기준](.agents/skills/build-service/references/starter-selection.md)을 확인합니다.

Vite 외부 미리보기는 제공된 URL의 **호스트 이름만** 지정합니다. 아래 예시 호스트를 실제 값으로 바꿉니다.

```sh
KIT_PREVIEW_HOSTS=preview.example.test make ui
```

미지정 외부 호스트는 차단합니다. `0.0.0.0`은 바인딩 주소이며 Host 허용 설정과 다릅니다. 실제 포트·호스트·프록시는 [접속 진단](.agents/skills/build-service/references/service-access.md)으로 확인합니다.

## 로컬 사본과 검증

solve-task의 자동 세션은 실제 실행 상태를 확인한 뒤 업무의 `.local/ai-toolkit/snapshots/`에 사본을 남깁니다. Git 초기화·자동 stage/commit/push는 하지 않습니다. 기본 제외 파일과 미저장 버퍼 등 범위는 [저장 안내](docs/GIT_AND_SAVE.md)를 확인합니다. 파일 감시는 판단 근거/기술 선택을 대신하지 않으며 모델을 추가 호출하지 않습니다.

```sh
python3 -m unittest discover -s tests -q
python3 tools/validate.py
```

[검증 범위](docs/VALIDATION.md)에 실제 실행/미실행과 한계를 기록합니다. 현재 업무의 자료·도구·접근·외부 전송 정책을 따릅니다. MCP/플러그인은 기존 도구로 부족한 기능이 있을 때만 [연결 기준](.agents/skills/solve-task/references/tool-connections.md)으로 선택합니다.

포함한 외부 원본과 라이선스/버전은 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)와 [sources.json](sources.json)을 참고합니다.
