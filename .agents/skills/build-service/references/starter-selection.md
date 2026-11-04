# 실행형 뼈대 선택

기존 프로젝트를 우선한다. 소수 파일로 충분하면 작은 구현을 직접 작성하고, 뼈대의 기능/의존성이 실제 시간을 줄일 때만 필요한 모듈을 채택한다. 전체 앱은 기본값이 아니다. 아래 경로는 키트 원본의 `templates/` 기준이다.

| 선택 | 모듈 | 적용 상황 |
| --- | --- | --- |
| api | backend/ai/data | API 중심·기존 프런트 연결 |
| frontend | frontend | 기존 API가 있는 React UI |
| data | data | 분석·ML·예측 파일 |
| rag | ai | 검색·근거 인용·생성기 연결·검색 평가 |
| fullstack | frontend/backend/ai/data/infra | 이 기능들이 모두 필요한 경우에만 선택 |

API 프로필에도 분석/RAG 예시가 포함된다. 단순 API에는 이를 무조건 복사하지 말고 작은 서버와 비교한다. 브리핑에 채택할 모듈·실제 수정/읽을 파일·의존성·제외할 키트 예시를 적는다. 키트에서 새로 복사한 미사용 예시만 제거하며 기존 업무 소스는 보존한다. 미사용 모듈까지 설명/검증 범위에 넣지 않는다.

키트 원본을 받은 경로에서 `tools/install.py --target <실제 업무 폴더> --profile <선택>`으로 미리 확인한 뒤 `--apply`한다. 원본 경로를 모르면 현재 환경에서 먼저 찾고 허용 범위 안에서 확보한다. 스킬 설치 폴더 자체에 앱 원본이 있다고 가정하지 않는다. 파일 충돌은 기존 코드를 덮어쓰는 방법으로 해결하지 않는다.

전체 앱의 `KIT_GUIDE.md`에 실행·검증 명령이 있다. Python 3.11+와 Node 22.12+ 또는 24+를 확인한다. `make setup` → 별도 터미널의 `make api`/`make ui`, 또는 `make build`/`make serve`로 시작한다. 기본 API 포트는 8000, Vite는 5173, 저장은 SQLite다. Docker는 선택이다.

## 업무별 변경 지점

- 화면: frontend/src/App.tsx, 요청: frontend/src/api.ts, 계산/차트 보조: domain.mjs.
- 입력·라우트: backend/app/main.py, 영속 저장: backend/app/database.py.
- 표/CSV 계산: data/analysis.py, ML 분할·전처리·평가: data/train.py.
- 문서 분할·검색·인용: ai/rag.py, 허용된 모델 함수 주입: ai/generation.py.
- 실행·전달: Makefile, Dockerfile, compose.yaml. 운영 시스템 설정을 임의로 바꾸지 않는다.

RAG 기본은 검색된 원문 발췌이며 외부 모델 연결이 아니다. 의미 검색·실제 생성이 필수면 허용된 모델·데이터 처리 경계를 확인하고 구현한다. 생성 시 문서를 비신뢰 자료로 구분하고 유효한 인용뿐 아니라 답변 내용의 지지도 검사한다. 근거 부족·오답·무관 질문을 포함한 검색/답변 평가를 분리한다.

기본 UI에는 단일 사용자 기록·CSV·문서 탐색이 있다. 요구와 관계없는 기능을 유지하지 말고 실제 핵심 흐름으로 바꾼다. 인증·멀티테넌시·대규모 작업 처리를 이미 구현했다고 가정하지 않는다. 사용한 모듈과 바꾼 코드만 probe.md와 devlog.md의 실제 내용으로 기록한다.
