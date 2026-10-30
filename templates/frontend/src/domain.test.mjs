import { test } from 'node:test';
import assert from 'node:assert/strict';
import { summarize, bars, errorMessage } from './domain.mjs';

test('summary uses visible records, including zero and negative values', () => {
  assert.deepEqual(
    summarize([
      { value: 2, status: 'done' },
      { value: -3, status: 'new' },
    ]),
    { total: 2, completed: 1, value: -1 },
  );
  assert.deepEqual(summarize([]), { total: 0, completed: 0, value: 0 });
});
test('chart widths are bounded and retain signed means', () => {
  assert.deepEqual(
    bars([{ mean: -4 }, { mean: 2 }, { mean: null }]).map((x) => [x.mean, x.width]),
    [
      [-4, 100],
      [2, 50],
      [null, 0],
    ],
  );
});
test('API validation errors identify fields', () => {
  assert.equal(
    errorMessage({ detail: [{ loc: ['body', 'title'], msg: 'required' }] }),
    'title: required',
  );
  assert.equal(errorMessage({ detail: 'unavailable' }), 'unavailable');
  assert.equal(errorMessage(null, 'failed'), 'failed');
});
