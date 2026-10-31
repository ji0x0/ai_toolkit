# AI Toolkit

실무 과제의 요구 파악부터 서비스·AI·데이터 구현, 검증과 코드 이해까지 지원하는 **Codex 스킬 + 실행형 앱 뼈대**입니다.

## Codex에서 한 문장으로 시작

과제 폴더에서 실행 중인 Codex에 다음처럼 입력합니다.

```text
https://github.com/ji0x0/ai_toolkit 를 설치해서 스킬을 파악하고 시작해줘
```

**이 요청을 받은 Codex는 [BOOTSTRAP.md](BOOTSTRAP.md)를 읽고 실행합니다.** 실제 과제 폴더를 보존한 채 키트를 `/tmp/ai_toolkit`에 받아 `tools/bootstrap.py --target <실제 과제 루트>`로 준비합니다. 스킬 설치가 허용되면 설치하고, .agents 쓰기가 제한되면 공개 원본을 직접 읽는 reference 모드로 반환합니다. 스킬 목록·설명을 파악하고 반환된 `entry_path`의 solve-task/SKILL.md를 읽어 **현재 대화에서** 이어갑니다. Codex를 다시 실행하지 않습니다.

문제 상황·해결 과제가 대화나 과제 README에 있으면 그 내용을 사용하고, 없으면 간단히 입력하도록 요청합니다. 이후 기록·자동저장 준비, 담당자 질문 제안과 답변 대기, 확인한 내용에 따른 구현·검증으로 진행합니다. 이 안내는 요청을 해석한 Codex가 실행하는 절차이며 전역 자연어 명령을 등록하는 기능은 아닙니다.

reference 모드는 “스킬 설치 완료”가 아닙니다. 반환된 원본 스킬·스크립트 경로를 직접 사용하며 필요한 단계에서 해당 스킬을 읽습니다. 일곱 스킬이 준비됐다는 사실과 모두 실행했다는 주장은 구분합니다. 관리 폴더의 권한·마운트·전역 설정은 바꾸지 않습니다. 이미 읽기 전용임을 확인했다면 `bootstrap.py --target <과제 루트> --mode reference`로 시작할 수 있습니다.

| 영역 | 포함 코드 |
| --- | --- |
| frontend | React·TypeScript·Vite, 기록 CRUD·CSV 분석 화면·차트·문서 질문/인용·반응형 UI |
| backend | FastAPI·Pydantic·SQLite, 입력 검증·영속 저장·페이지 조회·OpenAPI·정적 화면 제공 |
| ai | BM25 문서 검색·한국어 토큰·근거 인용·근거 부족 처리·생성기 어댑터·검색 평가 |
| data | CSV 품질·그룹 집계, 분류·회귀·Dummy 비교, 시간/그룹 분할, 모델 저장/추론·시계열 기준선 |
| infra | Docker 다단계 빌드·Compose·영속 볼륨·healthcheck·Makefile·CI |

뼈대의 기록·분석·문서 탐색은 서로 연결되어 실행됩니다. 과제의 필수 기능으로 바꾸고 해당 업무의 데이터·수용 기준으로 검증합니다. [모듈별 구현·선택 근거·실행 안내](docs/APP_STARTERS.md)를 참고합니다.

서버/API가 있는 웹서비스를 구현할 때는 상태 URL·API 안내·실제 접속 정보도 함께 준비합니다. FastAPI 뼈대의 기본 경로는 `/health`, `/api`, `/docs`, `/redoc`, `/openapi.json`이며 기존 `/api/health`도 유지합니다. API 목록은 현재 라우트 계약에서 생성합니다. `ENABLE_API_DOCS=false`로 목록·문서 UI·스키마를 함께 끌 수 있고 업무 API의 인증·권한은 별도로 다룹니다. 실제 과제의 SERVICE.md 또는 기존 실행 문서에 포트·경로·확인 결과를 유지합니다. [상태·API 안내 적용 기준](.agents/skills/build-service/references/service-access.md)을 참고합니다.

MCP·플러그인은 현재 도구로 접근할 수 없는 자료나 기능이 필요할 때 선택합니다. 앱 구현·CSV 분석·API 문서 생성에 필수는 아닙니다. [연결 선택 기준](.agents/skills/solve-task/references/tool-connections.md)에 따라 필요한 도구만 확인하며 일괄 설치하지 않습니다.

## 실제 과제 작업환경에 설치

아래 명령은 **실제 과제의 작업 폴더**에서 실행합니다. 키트는 별도 경로에 받습니다.

```sh
git clone --depth 1 https://github.com/ji0x0/ai_toolkit.git /tmp/ai_toolkit
python3 /tmp/ai_toolkit/tools/start.py --target .
```

시작 도구는 일곱 스킬을 설치하고 **제공된 Codex**에 짧은 시작 요청을 전달합니다. Codex는 과제 README·기존 지침·제출 제한을 읽은 뒤 기록 파일과 3분 간격 로컬 자동저장을 준비하고 **문제 입력→담당자 질문 제안→확인한 답변 반영→구현→검증→코드 이해 인계**로 진행합니다. 첫 질의 단계에서는 답변을 기다립니다. 모델·인증·Codex 버전·플랫폼 설정은 변경하지 않습니다. 설치 충돌은 덮어쓰지 않고 알립니다.

이미 Codex를 실행 중이면 위의 한 문장 설치 요청을 사용합니다. 수동으로 설치했다면 입력란에 `$solve-task`만 입력할 수도 있습니다. 스킬 인식이 안 되면 `.agents/skills/solve-task/SKILL.md를 읽고 실행해줘`라고 요청합니다. 실행 중인 Codex 안에서 start.py를 사용하지 않습니다.

설치를 먼저 검토하려면 다음 명령을 사용합니다.

```sh
python3 /tmp/ai_toolkit/tools/install.py --target .
python3 /tmp/ai_toolkit/tools/install.py --target . --apply
codex '$solve-task'
```

첫 설치 명령은 미리보기입니다. `--apply`하면 스킬을 작업 폴더의 `.agents/skills/`에 설치하고 **그 작업 폴더에 devlog.md와 probe.md를 생성**합니다. 기존 README·AGENTS·소스·기록 파일은 덮어쓰지 않습니다. 배포용 키트 폴더는 설치·기록 생성 대상으로 사용할 수 없습니다.

같은 이름의 다른 스킬이 있으면 자동 교체하지 않고 충돌을 알립니다. 선택 설치는 `--skills solve-task verify-result git-checkpoint`처럼 지정합니다. solve-task는 기록·저장에 필요한 record-work와 git-checkpoint를 함께 설치합니다. 과제가 추가 기록 파일을 금지하면 `--skip-records`로 설치하고 자동 세션에는 `--no-records`를 적용해 허용된 문서의 구획으로 관리합니다. start.py는 이 판단을 위해 과제 확인 전 기록 파일을 만들지 않습니다.

## 실행형 앱까지 설치

새 앱이 필요한 경우 실제 과제 폴더에서 프로필을 지정합니다. 기존 소스가 있다면 먼저 스킬만 설치하고 필요한 모듈을 선택합니다.

```sh
python3 /tmp/ai_toolkit/tools/install.py --target . --profile fullstack
python3 /tmp/ai_toolkit/tools/install.py --target . --profile fullstack --apply
make setup
make api    # 터미널 1: 8000
make ui     # 터미널 2: 5173
```

앱은 Python 3.11+ / Node 22.12+ 또는 24+가 필요합니다. 제공 Browser에서 5173을 엽니다. `make build` 후 `make serve`는 화면과 API를 8000 한 포트로 제공합니다. Docker는 선택입니다. `--profile api`, `--profile frontend`, `--profile data`, `--profile rag` 또는 `--modules frontend data`도 가능합니다. backend는 ai/data를 자동 포함합니다.

기존 파일이 다른 내용이면 덮어쓰기 전에 충돌을 알립니다. 의존성 설치·서버 실행·과제별 변경은 실제 작업환경에서 수행합니다. 기본 RAG는 **검색+원문 발췌**이며 실제 모델 생성은 허용된 호출 함수를 연결해야 합니다. 인증·조직별 권한·운영 백업은 과제 요구에 맞게 추가합니다.

스킬을 원본에서 직접 참조하는 환경에서는 `.agents`를 건드리지 않고 필요한 앱 코드만 복사합니다.

```sh
python3 /tmp/ai_toolkit/tools/install.py --target . --profile api --templates-only --apply
```

## 스킬

| 호출 | 역할 |
| --- | --- |
| `$solve-task` | 목표·요구·가정·담당자 질문·수용 기준·실행 계획 |
| `$build-service` | 기존 스택 또는 선택한 앱 뼈대의 UI·API·데이터 연결과 오류 처리 |
| `$analyze-data` | 데이터 의미·품질·누수·평가·수치 해석 |
| `$verify-result` | 요구별 검증·실패 조사·CSV 제출 계약 검사 |
| `$explain-work` | 코드 추적·직접 실행·선택 이유와 한계 설명 |
| `$git-checkpoint` | Git 컨벤션·로컬 스냅샷·복구 |
| `$record-work` | 과제 작업환경의 devlog.md·probe.md 생성과 갱신 |

새로 설치한 스킬의 발견 여부는 제공 환경에서 확인합니다. 자동 발견이 안 되면 설치된 SKILL.md를 명시적으로 읽고 같은 대화에서 적용합니다. 이 설치·인계 흐름은 Codex 재실행이나 버전 업데이트를 요구하지 않습니다.

## 과제 시작 요청

```text
$solve-task
문제 상황: 과제에서 받은 설명
해결 과제: 요구된 목표와 결과물
```

문제 설명이 README나 기존 대화에 있으면 `$solve-task`만 입력해도 됩니다. 이 한 번의 호출에 아래 대화 흐름과 기록·자동저장, 기본 60분 인계/지연 시 80분 목표를 포함합니다. 사용자 지침이나 실제 과제 제약이 다르면 그 조건을 우선합니다.

1. **문제 정의·질문 제안:** 페르소나·페인포인트·원인 가설을 정리하고, 사용자가 업무 담당자에게 보낼 질문과 확인 이유·우선순위·구현 영향을 제안합니다. 첫 응답에서는 업무 기능 코드나 앱 뼈대를 작성·설치하지 않습니다.
2. **답변 전달·반영:** 사용자가 담당자에게 질문한 뒤 실제 답변을 같은 Codex 대화에 입력합니다. Codex는 답변·근거·충돌·열린 질문과 요구/수용 기준을 갱신합니다. 기존 대화에서 확인된 것을 다시 묻지 않습니다.
3. **코드 작성·검증:** 필요한 정보가 확보되면 계획을 짧게 알리고 기존 코드를 보존하며 필요한 뼈대·기능을 구현합니다. 일반적인 개발 시작 승인을 다시 요구하지 않습니다.
4. **중간 판단:** 사용자 우선순위·업무 정책·범위·중요한 시간/품질 절충은 선택지·추천 이유·영향과 함께 묻고 해당 부분의 답을 기다립니다. 함수명 등 통상적인 구현 선택을 매번 묻지 않습니다.

확인한 답변은 다음처럼 짧게 전달할 수 있습니다.

```text
담당자에게 확인한 답변이야.
Q1: 실제 받은 답변
Q2: 실제 받은 답변
추가 조건: 실제 확인한 내용
```

담당자 질문·답변 대기도 과제 경과시간에 포함합니다. 답을 받았다는 이유로 인계 타이머를 다시 시작하지 않습니다.

## 과제 작업 기록

- `devlog.md`: 실제 질의응답·사용자 판단·변경·실행·실패·수정·검증·다음 행동의 시간순 기록.
- `probe.md`: 페르소나·업무 맥락·페인포인트·원인/근거·해결 원리를 기능과 연결하고, 코드 위치·사용 기술·대안/장단점·선택 이유·검증·업무 효과·이해 확인까지 설명하는 현행 문서.

이 파일들은 배포 저장소에 미리 채워두지 않습니다. 설치 시 **과제 작업 폴더**에 기본 구조를 만들고, 작업을 수행하며 실제 코드와 실행 결과로 갱신합니다. 기존 내용은 보존하며, 생성 자체를 구현·검증·이해 완료로 취급하지 않습니다.

solve-task가 시작되면 별도 record-work 호출 없이 문제 분석·담당자 답변·사용자 판단·구현/선택 변경·검증·인계와 작업 턴 종료 전에 Codex가 해당 내용을 갱신합니다. 페르소나는 확인한 업무 역할로 작성하고 원인 가설·담당자 설명·관측을 구분합니다. 기술 테스트 통과를 측정하지 않은 업무 개선 효과로 바꾸지 않습니다. 자동 감시 도구는 devlog에 관측한 파일명·해시 변화만 기록합니다. 의미 있는 설명은 Codex가 실제 근거로 작성하며, 감시 프로그램이 AI를 따로 호출하지 않습니다.

수동 생성도 실제 과제 폴더에서 실행합니다.

```sh
python3 .agents/skills/record-work/scripts/init_records.py --root .
```

[구현·이해·검증 시간표](docs/UNDERSTAND_AND_VERIFY.md)를 참고합니다. 과제의 필수 문서·파일명·금지 조건이 우선입니다.

## 실행 도구

- `analyze-data/scripts/profile_csv.py`: CSV 구조·결측·중복·숫자 범위 요약.
- `verify-result/scripts/run_checks.py`: 명시한 검증 명령 실행과 결과 JSON 기록.
- `verify-result/scripts/check_submission.py`: 명시한 CSV 열·행·ID·필수 값 계약 검사.
- `record-work/scripts/init_records.py`: 작업 기록 파일 생성·기존 파일 보존.
- `git-checkpoint/scripts/checkpoint.py`: 선택 파일의 로컬 스냅샷과 별도 폴더 복구.

CSV 검사에서는 예시 행 수나 첫 열을 계약으로 추정하지 않습니다. 실제 과제에 맞는 옵션만 사용하며 정답·예측 품질은 별도로 검증합니다.

## 로컬 저장

solve-task는 별도 설정 없이 자동 세션을 시작합니다. 기본 3분 간격·최대 3시간·최근 20개이며 새 소스 폴더도 자동 발견합니다. Git 유무와 관계없이 **과제 폴더의 `.local/ai-toolkit/snapshots/`**에 보관하고 `.git`은 수정하지 않습니다. Git을 임의로 초기화하지 않습니다. 중복 시작은 기존 세션을 재사용합니다.

“자동저장 상태 확인해줘” 또는 “자동저장 꺼줘”로 제어할 수 있습니다. 제출물 확정 전에는 최종 스냅샷과 종료를 확인합니다. 직접 점검할 때는 다음 명령을 사용합니다.

```sh
python3 .agents/skills/solve-task/scripts/session.py status --root .
python3 .agents/skills/solve-task/scripts/session.py stop --root .
```

reference 모드에서는 위 경로 대신 bootstrap이 반환한 `session_script`를 사용합니다. 일반 작업 폴더에도 쓰기가 금지되면 자동저장 실패를 알리고 임의 권한 변경이나 우회를 하지 않습니다.

기본 자동 선택은 CSV·의존성·생성물·숨김 도구 폴더·비밀 파일명·바이너리·크기 초과 파일을 제외합니다. Linux/macOS에서 동작하며 제공 IDE에서 실제 시작 상태를 확인해야 합니다. 선택 경로를 직접 지정하는 수동 도구도 유지합니다.

```sh
python3 .agents/skills/git-checkpoint/scripts/checkpoint.py --root . --include src tests docs README.md devlog.md probe.md --once
python3 .agents/skills/git-checkpoint/scripts/checkpoint.py --root . --include src tests docs README.md devlog.md probe.md --watch --interval 180 --duration 10800
```

앱 뼈대를 사용하면 `--include frontend/src backend ai data Makefile Dockerfile compose.yaml devlog.md probe.md`처럼 실제 소스를 지정합니다. 경로는 실제 과제에 맞춥니다. 저장소 내부의 로컬 ZIP 사본이며 자동 커밋·원격 전송을 하지 않습니다. 미저장 에디터 버퍼는 보존하지 않습니다. [저장·복구 설명](docs/GIT_AND_SAVE.md)을 참고합니다.

## 소스 관리·CI/CD·보안 범위

| 영역 | 포함 | 현재 포함하지 않는 것 |
| --- | --- | --- |
| 소스 작성·관리 | 앱 뼈대, 요구별 구현/검증, Git 컨벤션, 로컬 스냅샷·복구 | 자동 stage/commit/push, 원격 저장 보장 |
| CI | GitHub Actions의 Python·프런트 테스트, 타입/빌드 검사, 설치된 앱의 컨테이너 빌드 정의 | 시험 중 Git Push를 통한 외부 CI 실행 |
| CD | Docker/Compose 실행·영속 볼륨·healthcheck, 단일 포트 전달 경로 | 클라우드 자동 배포·운영 자격증명·배포 승인·롤백 파이프라인 |
| 보안 | 입력 검증·매개변수 SQL·클라이언트 키 분리 지침·비루트 컨테이너·RAG 비신뢰 문서 구분 | 인증/권한 완성본, SAST/DAST·의존성 취약점·전체 비밀정보 자동 검사 |
| 컴플라이언스 | 시험 제한·외부 전송 금지·실제 포함 원본의 라이선스 고지 | 법률 준수 판정·감사·인증 자동화 |
| AI 개발 흐름 | 분석·담당자 질의응답→구현→검증→기록→직접 이해, 사용자 판단 요청, 시간 배분 | 모든 문제의 정답·점수·사용자 이해 보장 |

표의 CI/CD는 구성과 실행 경로다. 검사·배포가 실제 성공했는지는 해당 환경의 실행 근거로 확인한다. 필요한 보안·권한과 개인정보 취급 조건은 실제 과제의 요구에 따라 추가 구현·검증한다.

## 검증

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -v
```

[검증 범위](docs/VALIDATION.md)를 확인합니다. 최신 운영 안내·과제 규정을 우선하고, 금지된 외부 전송·개인 모델 연결·자동 UI 조작·관리 설정 변경을 수행하지 않습니다. AI 금지 후속 문항에서는 AI 사용을 중단합니다.

배포에 포함된 외부 원본과 라이선스는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), 고정 버전은 [sources.json](sources.json)에 있습니다.
