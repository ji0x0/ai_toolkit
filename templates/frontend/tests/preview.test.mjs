import { test } from 'node:test';
import assert from 'node:assert/strict';
import http from 'node:http';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createServer, preview } from 'vite';

const root = fileURLToPath(new URL('../', import.meta.url));
const configFile = join(root, 'vite.config.ts');

// 외부 DNS/공유 서버를 쓰지 않습니다. 로컬 연결의 Host 헤더만 바꿔 실제 Vite 응답을 검사합니다.
function request(server, host, path = '/') {
  return new Promise((resolve, reject) => {
    const req = http.get(
      { hostname: '127.0.0.1', port: server.address().port, path, headers: { Host: host } },
      (response) => {
        let body = '';
        response.on('data', (chunk) => {
          body += chunk;
        });
        response.on('end', () => resolve({ status: response.statusCode, body }));
      },
    );
    req.setTimeout(5000, () => req.destroy(new Error('local HTTP test timeout')));
    req.on('error', reject);
  });
}

async function withEnvironment(hosts, action) {
  const keys = ['KIT_PREVIEW_HOSTS', '__VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS'];
  const original = keys.map((key) => process.env[key]);
  process.env.KIT_PREVIEW_HOSTS = hosts;
  delete process.env.__VITE_ADDITIONAL_SERVER_ALLOWED_HOSTS;
  try {
    return await action();
  } finally {
    keys.forEach((key, i) =>
      original[i] === undefined ? delete process.env[key] : (process.env[key] = original[i]),
    );
  }
}

async function withDev(hosts, action, port = 0) {
  return withEnvironment(hosts, async () => {
    const server = await createServer({
      root,
      configFile,
      logLevel: 'silent',
      server: { host: '127.0.0.1', port },
    });
    try {
      await server.listen();
      return await action(server);
    } finally {
      await server.close();
    }
  });
}

test('개발 서버는 기본 로컬 요청을 허용하고 미지정 외부 호스트를 거절한다', async () => {
  await withDev('', async (server) => {
    assert.equal((await request(server.httpServer, 'localhost')).status, 200);
    const rejected = await request(server.httpServer, 'unknown.workspace.test');
    assert.equal(rejected.status, 403);
    assert.match(rejected.body, /Blocked request/);
  });
});

test('명시한 복수 미리보기 호스트만 허용하고 유사 도메인은 거절한다', async () => {
  await withDev(' Preview.Workspace.Test, second.workspace.test ', async (server) => {
    for (const host of ['preview.workspace.test', 'second.workspace.test']) {
      assert.equal((await request(server.httpServer, host)).status, 200);
    }
    assert.equal(
      (await request(server.httpServer, 'preview.workspace.test.other.test')).status,
      403,
    );
  });
});

test('정적 미리보기도 호스트 정책과 API 프록시를 적용한다', async () => {
  const outDir = await mkdtemp(join(tmpdir(), 'toolkit-preview-'));
  const upstream = http.createServer((req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ path: req.url, status: 'mock-ok' }));
  });
  try {
    await writeFile(join(outDir, 'index.html'), '<!doctype html><title>preview-test</title>');
    await new Promise((resolve, reject) => {
      upstream.once('error', reject);
      upstream.listen(0, '127.0.0.1', resolve);
    });
    await withEnvironment('preview.workspace.test', async () => {
      const server = await preview({
        root,
        configFile,
        logLevel: 'silent',
        build: { outDir },
        preview: {
          host: '127.0.0.1',
          port: 0,
          proxy: { '/api': `http://127.0.0.1:${upstream.address().port}` },
        },
      });
      try {
        assert.equal((await request(server.httpServer, 'preview.workspace.test')).status, 200);
        assert.equal((await request(server.httpServer, 'unknown.workspace.test')).status, 403);
        assert.equal(
          (await request(server.httpServer, 'unknown.workspace.test', '/api/sample')).status,
          403,
        );
        // 접속 허용 후 /api 요청이 실제 upstream으로 전달되는지를 봅니다. 실제 업무 API 검사는 아닙니다.
        const api = await request(server.httpServer, 'preview.workspace.test', '/api/sample');
        assert.equal(api.status, 200);
        assert.deepEqual(JSON.parse(api.body), { path: '/api/sample', status: 'mock-ok' });
      } finally {
        await server.close();
      }
    });
  } finally {
    if (upstream.listening) await new Promise((resolve) => upstream.close(resolve));
    await rm(outDir, { recursive: true, force: true });
  }
});

test('와일드카드·전체 URL·포트가 든 호스트 설정은 시작 전에 거절한다', async () => {
  for (const invalid of [
    '*',
    'true',
    '.example.test',
    'https://example.test',
    'example.test:5173',
  ]) {
    await assert.rejects(() => withDev(invalid, async () => {}), /KIT_PREVIEW_HOSTS/);
  }
});

test('포트가 이미 사용 중이면 다른 포트로 옮기지 않고 실패한다', async () => {
  const blocker = http.createServer();
  await new Promise((resolve, reject) => {
    blocker.once('error', reject);
    blocker.listen(0, '127.0.0.1', resolve);
  });
  try {
    await assert.rejects(
      () => withDev('', async () => {}, blocker.address().port),
      /already in use/,
    );
  } finally {
    await new Promise((resolve) => blocker.close(resolve));
  }
});
