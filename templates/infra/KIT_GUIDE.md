# 앱 실행과 수정

이 파일은 전체 앱 뼈대와 함께 과제 폴더에 설치된다. 기존 과제 README와 AGENTS.md의 요구를 먼저 확인한다.

## 실행

Python 3.11+ / Node 22.12+ 또는 24+를 사용한다. 기본 조합은 Python 3.11 / Node 24다.

```sh
make setup
make api    # 터미널 1, 8000
make ui     # 터미널 2, 5173
```

제공 Browser에서 5173을 연다. 직접 명령은 다음과 같다.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
npm --prefix frontend ci --no-audit --no-fund
.venv/bin/python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
# 다른 터미널
npm --prefix frontend run dev
```

단일 포트 실행: `make build` 후 `make serve`, 8000에서 화면과 API를 함께 제공한다. Docker가 허용되고 실행 중이면 `docker compose up --build`로 실행할 수 있다. 직접 실행의 저장은 `.local/app/app.sqlite3`, Docker는 named volume이다. 개발 포트를 변경하면 `frontend/vite.config.ts`의 프록시도 맞춘다. API 문서는 `/docs`다.

## 검증

```sh
make test
make ml-deps
make test-ml
docker compose config --quiet
```

Docker 구성 검사와 이미지 빌드·실행은 서로 다른 검사다. CI는 API·검색·CSV·ML·프런트 테스트와 프런트 빌드를 수행한다. UI의 실제 클릭·좁은 화면·오류 복구는 제공 Browser에서 직접 확인한다. 브라우저 자동 조작은 사용하지 않는다.

## 코드 경로

| 사용자 동작 | 화면 | 서버·계산 |
| --- | --- | --- |
| 기록 추가·진행 변경·삭제 | frontend/src/App.tsx | backend/app/main.py → database.py |
| CSV 파일·그룹별 평균 | App.tsx → api.ts | data/analysis.py |
| 문서 등록·질문·출처 | App.tsx → api.ts | database.py → ai/rag.py |
| 분류·회귀·예측 CSV | CLI | data/train.py → predict.py |
| 시계열 기준선 | CLI | data/forecast.py |

RAG 기본은 BM25 검색과 원문 발췌다. `ai/generation.py`는 이미 허용된 모델 호출 함수를 주입하는 어댑터다. 기본 앱에 외부 모델·개인 키 연결은 없다. ML은 Dummy 기준선과 같은 분할로 비교하며, 시간/그룹/무작위 분할 중 실제 사용과 맞는 것을 고른다. 시계열은 한 개체·오름차순·일정 간격 데이터를 전제로 한다.

## 과제에 맞게 바꾸기

현재 앱은 단일 사용자용 뼈대다. 실제 용어·필수 계산·단위·데이터·제출 계약으로 교체한다. 인증·조직 권한·백업·대규모 작업 큐는 요구가 있을 때 구현한다. 예시 기능은 필수 기능과 연결되지 않으면 제거한다.

- React/TypeScript: 화면 상태·타입 확인을 빠르게 구성. 단순 정적 화면이면 HTML/JS, SSR이 필수면 서버 렌더링 대안을 비교.
- FastAPI/SQLite: 계약·API 문서·저장을 서버 하나로 제공. 다중 사용자·동시 쓰기 요구면 PostgreSQL 등 비교.
- BM25: 키·모델 다운로드 없는 근거 검색. 의미 검색이 중요하면 허용된 임베딩/하이브리드 검색을 평가.
- LogisticRegression/Ridge: 빠르고 읽기 쉬운 표 데이터 기준선. 비선형 관계면 트리/부스팅을 같은 검증 분할에서 비교.
- Docker: 한 컨테이너 전달·영속 볼륨. 제공 환경에서 직접 실행이면 Docker 없이 진행.

devlog.md에는 실제 변경·실행·실패·수정을 기록한다. probe.md에는 **적용한 기능별** 코드 위치, 도구/라이브러리, 대안과 장단점, 현재 선택 이유, 검증 결과와 한계를 기록한다. 기본 표를 업무 판단의 근거로 대신하지 않는다.

원격 저장이 허용되는지 먼저 확인한다. `.local/`, `.venv/`, `.env`, `node_modules/`, 빌드 결과는 기존 `.gitignore`에 병합하고 비밀·원본 데이터·모델 파일을 무심코 추가하지 않는다. solve-task는 별도 설정 없이 기록 준비와 3분 간격 로컬 자동저장을 시작하고, 단계별로 devlog/probe를 갱신한다. 상태 확인과 종료는 solve-task/scripts/session.py의 status/stop을 사용한다. 제출 확정 전에 최종 사본과 종료를 확인한다. 실제 과제 코드를 공개 키트로 전송하지 않는다.
