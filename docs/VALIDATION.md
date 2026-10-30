# 검증 범위

## 로컬 확인

- 설치·저장·검사 도구: `python3 -m unittest discover -s tests -v` 53개 통과.
- FastAPI: `PYTHONPATH=templates python3 -m unittest discover -s templates/backend/tests -v` 8개 통과.
- 검색·생성기 경계: `PYTHONPATH=templates python3 -m unittest discover -s templates/ai/tests -v` 7개 통과.
- CSV·시계열: `PYTHONPATH=templates python3 -m unittest discover -s templates/data/tests -v` 6개 통과.
- 분류·회귀·저장 모델 추론: `PYTHONPATH=templates python3 -m unittest discover -s templates/data/ml_tests -v` 3개 통과.
- 프런트 계산: `cd templates/frontend && npm test` 3개 통과.
- 합계 80개, 실패·skip 없음. 앱 Python 검사는 Python 3.11의 새 가상환경에 명시한 서버·ML 의존성만 설치해 수행했다. 로컬 Node는 26.7.0이며 Docker/CI는 Node 24를 사용하도록 구성했다.
- `npm run build`: TypeScript 검사와 Vite 프로덕션 빌드 통과.
- `python3 tools/validate.py`: 일곱 스킬의 frontmatter·이름·로컬 링크·Python 구문 검사.
- Skill Creator Validator: 일곱 스킬의 형식 검사.
- 포함한 외부 원본과 라이선스 네 파일은 sources.json에 기록한 Git blob SHA와 일치.

## 주요 동작

- 설치 미리보기는 파일을 만들지 않는다.
- 기본 설치는 실제 과제 폴더에 일곱 스킬과 devlog.md·probe.md를 생성한다.
- 기존 README·AGENTS·기록 내용은 보존한다. 기록 경로 충돌은 스킬 복사 전에 알린다.
- 배포 폴더 내부에 설치하거나 작업 기록을 생성하는 것을 거부한다.
- 추가 기록이 금지된 과제는 `--skip-records`로 스킬만 설치할 수 있다.
- 기록 생성기의 독립 실행·반복 보존·심볼릭 링크/디렉터리 충돌·점검 전용 모드를 확인한다.
- 로컬 스냅샷의 Git index 보존·크기/보존 개수 제한·중복 실행 방지·별도 폴더 복구를 확인한다.
- CSV 구조 점검, 명시한 제출 계약, 검증 명령의 종료 상태·timeout·오류 처리를 합성 입력으로 확인한다.
- fullstack 미리보기·반복 설치·backend 의존성 선택·기존 코드 충돌·심볼릭 링크 보호를 확인한다.
- 별도 임시 과제 폴더에 fullstack을 설치하고 실제 uvicorn 프로세스로 HTML·JS/CSS·API 문서·기록 저장/조회·CSV 평균·문서 검색/인용을 HTTP로 확인했다. 프로세스는 검사 후 종료했다.
- SQLite 재시작 영속성, 잘못된 입력/없는 항목, 검색 근거 없음/잘못된 인용, 한국어 검색, 시간 분할 경계, 미지 범주 추론, 예측 CSV ID 보존을 확인한다.
- 설치된 프로젝트의 `docker compose config --quiet` 통과. 로컬 Docker 엔진이 꺼져 있어 이미지 빌드·컨테이너 실행은 미실행이다. 저장소 CI에는 설치한 앱의 이미지 빌드를 구성했으며 구성만으로 실행 성공을 주장하지 않는다.

## 별도로 확인할 것

실제 응시 환경의 스킬 발견·호출, 감독 연결, 실제 과제의 정답·필수 제출물·사용자 이해는 별도 확인이 필요하다. 문서 생성은 내용의 완성이나 이해 완료를 뜻하지 않으며, 자동저장은 미저장 에디터 버퍼를 보존하지 않는다. 명령의 정상 종료도 업무 정답을 자동으로 입증하지 않는다.

UI의 실제 클릭·육안·좁은 화면 확인과 실제 생성 모델 연결·답변 정답률은 미검증이다. 기본 문서 답변은 BM25 검색과 원문 발췌다. 프로토타입 테스트는 인증·멀티테넌시·대규모 부하·운영 복구 검증을 포함하지 않는다.
