# AI Toolkit

실무 과제의 요구 파악부터 서비스·AI·데이터 구현, 검증과 코드 이해까지 지원하는 **Codex 스킬 + 실행형 앱 뼈대**입니다.

| 영역 | 포함 코드 |
| --- | --- |
| frontend | React·TypeScript·Vite, 기록 CRUD·CSV 분석 화면·차트·문서 질문/인용·반응형 UI |
| backend | FastAPI·Pydantic·SQLite, 입력 검증·영속 저장·페이지 조회·OpenAPI·정적 화면 제공 |
| ai | BM25 문서 검색·한국어 토큰·근거 인용·근거 부족 처리·생성기 어댑터·검색 평가 |
| data | CSV 품질·그룹 집계, 분류·회귀·Dummy 비교, 시간/그룹 분할, 모델 저장/추론·시계열 기준선 |
| infra | Docker 다단계 빌드·Compose·영속 볼륨·healthcheck·Makefile·CI |

뼈대의 기록·분석·문서 탐색은 서로 연결되어 실행됩니다. 과제의 필수 기능으로 바꾸고 해당 업무의 데이터·수용 기준으로 검증합니다. [모듈별 구현·선택 근거·실행 안내](docs/APP_STARTERS.md)를 참고합니다.

## 실제 과제 작업환경에 설치

아래 명령은 **실제 과제의 작업 폴더**에서 실행합니다. 키트는 별도 경로에 받습니다.

```sh
git clone --depth 1 https://github.com/ji0x0/ai_toolkit.git /tmp/ai_toolkit
python3 /tmp/ai_toolkit/tools/install.py --target .
python3 /tmp/ai_toolkit/tools/install.py --target . --apply
codex
```

첫 설치 명령은 미리보기입니다. `--apply`하면 스킬을 작업 폴더의 `.agents/skills/`에 설치하고 **그 작업 폴더에 devlog.md와 probe.md를 생성**합니다. 기존 README·AGENTS·소스·기록 파일은 덮어쓰지 않습니다. 배포용 키트 폴더는 설치·기록 생성 대상으로 사용할 수 없습니다.

같은 이름의 다른 스킬이 있으면 자동 교체하지 않고 충돌을 알립니다. 선택 설치는 `--skills solve-task verify-result git-checkpoint`처럼 지정합니다. solve-task 또는 record-work를 선택한 경우 작업 기록도 생성합니다. 과제가 추가 기록 파일을 금지하면 `--skip-records`로 설치한 뒤 허용된 문서의 구획으로 관리합니다.

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

새로 설치한 스킬의 발견 여부는 제공 환경에서 확인합니다. Codex를 이미 실행 중이면 필요에 따라 새 세션을 시작하거나 설치된 SKILL.md를 명시적으로 읽도록 요청합니다.

## 과제 시작 요청

```text
$solve-task로 실제 과제 README·기존 지침·제공 파일을 확인해줘.
과제 작업 폴더의 devlog.md와 probe.md를 실제 작업 근거로 유지해줘.
필수 요구와 수용 기준을 정리하고 최소 구현·검증을 진행해줘.
기본 목표는 60분 구현 인계, 110분 직접 이해·검증, 10분 제출이야.
지연 시 80분 인계·90분 이해/검증을 목표로 현재 상태와 시간 영향을 알려줘.
```

## 과제 작업 기록

- `devlog.md`: 실제 결정·변경·실행·실패·수정·검증·다음 행동의 시간순 기록.
- `probe.md`: 현재 기능별 요구·코드 위치·사용 도구와 라이브러리·동일 기능의 대안·장단점·선택 이유·검증 근거·이해 확인.

이 파일들은 배포 저장소에 미리 채워두지 않습니다. 설치 시 **과제 작업 폴더**에 기본 구조를 만들고, 작업을 수행하며 실제 코드와 실행 결과로 갱신합니다. 기존 내용은 보존하며, 생성 자체를 구현·검증·이해 완료로 취급하지 않습니다.

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

```sh
python3 .agents/skills/git-checkpoint/scripts/checkpoint.py --root . --include src tests docs README.md devlog.md probe.md --once
python3 .agents/skills/git-checkpoint/scripts/checkpoint.py --root . --include src tests docs README.md devlog.md probe.md --watch --interval 180 --duration 10800
```

앱 뼈대를 사용하면 `--include frontend/src backend ai data Makefile Dockerfile compose.yaml devlog.md probe.md`처럼 실제 소스를 지정합니다. 경로는 실제 과제에 맞춥니다. 저장소 내부의 로컬 ZIP 사본이며 자동 커밋·원격 전송을 하지 않습니다. 미저장 에디터 버퍼는 보존하지 않습니다. [저장·복구 설명](docs/GIT_AND_SAVE.md)을 참고합니다.

## 검증

```sh
python3 tools/validate.py
python3 -m unittest discover -s tests -v
```

[검증 범위](docs/VALIDATION.md)를 확인합니다. 최신 운영 안내·과제 규정을 우선하고, 금지된 외부 전송·개인 모델 연결·자동 UI 조작·관리 설정 변경을 수행하지 않습니다. AI 금지 후속 문항에서는 AI 사용을 중단합니다.

배포에 포함된 외부 원본과 라이선스는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), 고정 버전은 [sources.json](sources.json)에 있습니다.
