import { fileURLToPath } from 'node:url';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  // 바인딩 주소와 브라우저가 보내는 Host는 서로 다릅니다.
  // 제공된 미리보기 URL의 호스트만 쉼표로 지정합니다. 클라이언트에 공개되는 VITE_ 변수는 쓰지 않습니다.
  const env = loadEnv(mode, fileURLToPath(new URL('.', import.meta.url)), 'KIT_');
  const allowedHosts = [
    ...new Set(
      (env.KIT_PREVIEW_HOSTS ?? '')
        .split(',')
        .map((h) => h.trim().toLowerCase())
        .filter(Boolean),
    ),
  ];
  const hostname =
    /^(?=.{1,253}$)[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)*$/;
  if (allowedHosts.some((host) => !hostname.test(host) || host === 'true' || host === 'false')) {
    throw new Error(
      'KIT_PREVIEW_HOSTS에는 URL·포트·와일드카드 대신 실제 호스트 이름만 지정하세요.',
    );
  }
  const proxy = {
    '/api': 'http://127.0.0.1:8000',
    '/health': 'http://127.0.0.1:8000',
    '/docs': 'http://127.0.0.1:8000',
    '/redoc': 'http://127.0.0.1:8000',
    '/openapi.json': 'http://127.0.0.1:8000',
  };
  return {
    // 미지정이면 Vite의 localhost/IP 허용과 외부 호스트 차단을 유지합니다.
    // 포트 충돌을 조용히 다른 포트로 바꾸지 않아 IDE 연결 오류를 바로 알 수 있습니다.
    server: { host: '0.0.0.0', port: 5173, strictPort: true, allowedHosts, proxy },
    preview: { host: '0.0.0.0', port: 4173, strictPort: true, allowedHosts, proxy },
  };
});
