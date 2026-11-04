# 서버 접속·상태/API 안내

서버가 있는 업무에만 적용한다. 프런트 전용 결과물에 안내용 서버를 추가하지 않는다. 기존 인증·접근·문서 공개 정책을 유지한다.

## 실제 접속 경로

프로세스→로그/실행 유지→포트/바인딩→Host→프록시→업무 경로 순서로 진단한다. 웹 IDE는 내부 주소와 제공된 외부 미리보기 URL을 구분한다. `0.0.0.0`은 서버 바인딩이며 브라우저 접속 주소가 아니다.

Vite에서 `Blocked request`와 403이 보이면 제공된 URL의 신뢰할 수 있는 호스트를 확인한다. 키트는 `KIT_PREVIEW_HOSTS`를 개발/정적 미리보기에 동일 적용한다. `https://`, 포트, 경로 없이 실제 호스트만 지정하고 서버를 다시 실행한다. `.env.local`은 frontend 폴더에 두거나 명령의 환경 변수로 전달한다.

```sh
KIT_PREVIEW_HOSTS=preview.example.test make ui
curl -i -H 'Host: preview.example.test' http://127.0.0.1:5173/
```

예시를 실제 호스트로 바꾼다. 여러 호스트는 쉼표로 구분한다. 임의 요청의 Host를 자동 신뢰하거나 `allowedHosts: true`/전체 도메인 와일드카드로 풀지 않는다. 포트 충돌은 실패로 알리며 합의한 포트를 바꾸면 IDE 연결과 API 프록시도 함께 맞춘다. HMR/WebSocket·TLS·경로 접두사 등 플랫폼별 연결은 따로 확인한다.

[Vite 서버 Host 설정](https://v8.vite.dev/config/server-options#server-allowedhosts)과 [정적 미리보기 설정](https://vite.dev/config/preview-options#preview-allowedhosts)을 참고한다.

## 상태와 API 계약

- 기존 상태 경로를 재사용한다. 신규 기본 `/health`의 최소 응답은 `{"status":"ok"}`이며 프로세스 응답만 뜻한다. 준비 상태·업무 정확성과 구분하고 상세 내부 정보는 넣지 않는다.
- 실제 라우트의 메서드·목적·입력/응답·오류·권한을 SERVICE에 적는다. FastAPI 뼈대는 `/api` 목록, `/docs`·`/redoc`, `/openapi.json`과 호환용 `/api/health`를 제공한다.
- `ENABLE_API_DOCS=false`로 목록/문서/스키마를 끌 수 있다. 문서 공개 설정과 업무 API 인증은 별개다. 문서 UI의 쓰기 요청은 실제 데이터를 바꿀 수 있다.
- 현재 환경의 UI 제약이 있으면 [호환 기준](ui-compatibility.md)을 적용한다. 개발 문서 안내를 이유로 제품 화면에 새 탭/이동 버튼을 추가하지 않는다.

실제 포트/경로·실행 유지 방법·상태 범위·문서 공개·대표 HTTP 기대/실제 결과를 SERVICE의 해당 구획에 유지한다. 실행하지 않은 UI/연결은 미확인으로 남기고 원시 로그를 세 문서에 복제하지 않는다.
