import assert from 'node:assert/strict';
import test from 'node:test';
import {
  classifyPullRequest,
  computeReviewDecision,
  hasAuthorResponseAfter,
  isActionableText,
  latestExternalMessage,
  parseRepoFromRemote,
  stripNoise,
} from './triage.mjs';

test('parseRepoFromRemote supports SSH and HTTPS remotes', () => {
  assert.equal(parseRepoFromRemote('git@github.com:openai/openai.git'), 'openai/openai');
  assert.equal(parseRepoFromRemote('https://github.com/openai/openai.git'), 'openai/openai');
  assert.equal(parseRepoFromRemote('ssh://git@github.com/openai/openai.git'), 'openai/openai');
  assert.equal(parseRepoFromRemote('not-a-remote'), null);
});

test('stripNoise removes hidden and details content', () => {
  assert.equal(stripNoise('hello <!-- hidden --> <details>noise</details> world'), 'hello   world');
});

test('actionable text does not revive old requests after LGTM-like messages', () => {
  assert.equal(isActionableText('Could you rename this?'), true);
  assert.equal(isActionableText('LGTM, nothing to change.'), false);
  assert.equal(isActionableText('핵심 액션 아이템: 이상 발견 없음'), false);
});

test('computeReviewDecision keeps only each reviewer latest state', () => {
  const decision = computeReviewDecision([
    { user: { login: 'reviewer' }, state: 'CHANGES_REQUESTED', submitted_at: '2026-01-01T00:00:00Z' },
    { user: { login: 'reviewer' }, state: 'APPROVED', submitted_at: '2026-01-02T00:00:00Z' },
    { user: { login: 'author' }, state: 'CHANGES_REQUESTED', submitted_at: '2026-01-03T00:00:00Z' },
  ], 'author');
  assert.deepEqual(decision, { decision: 'APPROVED', decisiveAt: '2026-01-02T00:00:00Z' });
});

test('latestExternalMessage uses the latest external message, not an older request', () => {
  const rows = [
    { login: 'reviewer', timestamp: '2026-01-01T00:00:00Z', body: 'Could you rename this?' },
    { login: 'reviewer', timestamp: '2026-01-02T00:00:00Z', body: 'LGTM' },
  ];
  assert.equal(latestExternalMessage(rows, 'author').body, 'LGTM');
  assert.equal(isActionableText(latestExternalMessage(rows, 'author').body), false);
});

test('hasAuthorResponseAfter is scoped to the decisive timestamp', () => {
  const rows = [
    { login: 'author', timestamp: '2026-01-01T00:00:00Z' },
    { login: 'reviewer', timestamp: '2026-01-02T00:00:00Z' },
    { login: 'author', timestamp: '2026-01-03T00:00:00Z' },
  ];
  assert.equal(hasAuthorResponseAfter(rows, 'author', '2026-01-02T00:00:00Z'), true);
  assert.equal(hasAuthorResponseAfter(rows, 'author', '2026-01-04T00:00:00Z'), false);
});

test('classification priority is conflict, checks, draft, review state, reply', () => {
  const base = {
    draft: false,
    conflict: false,
    checksFailed: false,
    decision: 'REVIEW_REQUIRED',
    authorRespondedToChangeRequest: false,
    latestExternalActionable: false,
    authorRespondedToLatestExternal: false,
  };
  assert.equal(classifyPullRequest({ ...base, conflict: true, checksFailed: true }), 'merge_conflict');
  assert.equal(classifyPullRequest({ ...base, checksFailed: true, draft: true }), 'checks_failed');
  assert.equal(classifyPullRequest({ ...base, draft: true }), 'draft');
  assert.equal(classifyPullRequest({ ...base, decision: 'CHANGES_REQUESTED' }), 'changes_requested');
  assert.equal(classifyPullRequest({
    ...base,
    decision: 'CHANGES_REQUESTED',
    authorRespondedToChangeRequest: true,
  }), 'awaiting_re_review');
  assert.equal(classifyPullRequest({ ...base, latestExternalActionable: true }), 'needs_reply');
  assert.equal(classifyPullRequest({
    ...base,
    latestExternalActionable: true,
    authorRespondedToLatestExternal: true,
  }), 'awaiting_re_review');
  assert.equal(classifyPullRequest({ ...base, decision: 'APPROVED' }), 'approved');
  assert.equal(classifyPullRequest(base), 'pending_review');
});
