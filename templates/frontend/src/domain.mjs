export function summarize(items) {
  return {
    total: items.length,
    completed: items.filter((item) => item.status === 'done').length,
    value: items.reduce((sum, item) => sum + item.value, 0),
  };
}

export function bars(groups) {
  const max = Math.max(1, ...groups.map((group) => Math.abs(group.mean ?? 0)));
  return groups.map((group) => ({ ...group, width: (Math.abs(group.mean ?? 0) / max) * 100 }));
}

export function errorMessage(payload, fallback = '요청을 처리하지 못했습니다.') {
  if (typeof payload?.detail === 'string') return payload.detail;
  if (Array.isArray(payload?.detail))
    return payload.detail
      .map((item) => `${item.loc?.slice(1).join('.') || '입력'}: ${item.msg}`)
      .join(' / ');
  return fallback;
}
