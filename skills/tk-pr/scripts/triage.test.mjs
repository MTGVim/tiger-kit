import assert from 'node:assert/strict';
import test from 'node:test';
import {
  classifyPullRequest,
  computeReplyEvidence,
  computeReviewDecision,
  flattenPages,
  hasAuthorResponseAfter,
  isActionableText,
  latestExternalMessagesByScope,
  parseRepoFromRemote,
  stripNoise,
} from './triage.mjs';

test('parseRepoFromRemote supports SSH and HTTPS remotes', () => {
  assert.equal(parseRepoFromRemote('git@github.com:openai/openai.git'), 'openai/openai');
  assert.equal(parseRepoFromRemote('https://github.com/openai/openai.git'), 'openai/openai');
  assert.equal(parseRepoFromRemote('ssh://git@github.com/openai/openai.git'), 'openai/openai');
  assert.equal(parseRepoFromRemote('not-a-remote'), null);
});

test('flattenPages supports arrays and check-runs object pages', () => {
  assert.deepEqual(flattenPages([[{ id: 1 }], [{ id: 2 }]]), [{ id: 1 }, { id: 2 }]);
  assert.deepEqual(
    flattenPages([{ total_count: 2, check_runs: [{ id: 1 }] }, { check_runs: [{ id: 2 }] }], 'check_runs'),
    [{ id: 1 }, { id: 2 }],
  );
});

test('stripNoise removes hidden and details content', () => {
  assert.equal(stripNoise('hello <!-- hidden --> <details>noise</details> world'), 'hello   world');
});

test('actionable text does not revive old requests after LGTM-like messages', () => {
  assert.equal(isActionableText('Could you rename this?'), true);
  assert.equal(isActionableText('LGTM, nothing to change.'), false);
  assert.equal(isActionableText('핵심 액션 아이템: 이상 발견 없음'), false);
  assert.equal(isActionableText('Rename this variable.'), true);
  assert.equal(isActionableText('This should use the shared helper.'), true);
  assert.equal(isActionableText('이 검증을 추가해야 합니다.'), true);
});

test('computeReviewDecision keeps only each reviewer latest state', () => {
  const decision = computeReviewDecision([
    { user: { login: 'reviewer' }, state: 'CHANGES_REQUESTED', submitted_at: '2026-01-01T00:00:00Z' },
    { user: { login: 'reviewer' }, state: 'APPROVED', submitted_at: '2026-01-02T00:00:00Z' },
    { user: { login: 'author' }, state: 'CHANGES_REQUESTED', submitted_at: '2026-01-03T00:00:00Z' },
  ], 'author');
  assert.deepEqual(decision, { decision: 'APPROVED', decisiveAt: '2026-01-02T00:00:00Z' });
});

test('a later COMMENTED review does not clear changes requested', () => {
  const decision = computeReviewDecision([
    { user: { login: 'reviewer' }, state: 'CHANGES_REQUESTED', submitted_at: '2026-01-01T00:00:00Z' },
    { user: { login: 'reviewer' }, state: 'COMMENTED', submitted_at: '2026-01-02T00:00:00Z' },
  ], 'author');
  assert.deepEqual(decision, { decision: 'CHANGES_REQUESTED', decisiveAt: '2026-01-01T00:00:00Z' });
});

test('latest external message supersedes older requests only in the same scope', () => {
  const rows = [
    { scope: 'inline:1', login: 'reviewer-a', timestamp: '2026-01-01T00:00:00Z', body: 'Could you rename this?' },
    { scope: 'inline:1', login: 'reviewer-a', timestamp: '2026-01-02T00:00:00Z', body: 'LGTM' },
    { scope: 'inline:2', login: 'reviewer-b', timestamp: '2026-01-03T00:00:00Z', body: 'Please add a test.' },
  ];
  const latest = latestExternalMessagesByScope(rows, 'author');
  assert.deepEqual(latest.map((row) => row.body), ['LGTM', 'Please add a test.']);
  assert.deepEqual(computeReplyEvidence(rows, 'author').outstanding.map((row) => row.scope), ['inline:2']);
});

test('reply evidence requires an author response in the same thread scope', () => {
  const rows = [
    { scope: 'inline:1', login: 'reviewer', timestamp: '2026-01-01T00:00:00Z', body: 'Could you rename this?' },
    { scope: 'inline:2', login: 'author', timestamp: '2026-01-02T00:00:00Z', body: 'Done elsewhere.' },
    { scope: 'inline:1', login: 'author', timestamp: '2026-01-03T00:00:00Z', body: 'Renamed.' },
  ];
  const reply = computeReplyEvidence(rows, 'author');
  assert.equal(reply.outstanding.length, 0);
  assert.deepEqual(reply.responded.map((row) => row.scope), ['inline:1']);
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

test('classification priority is conflict, checks, changes requested, draft, reply', () => {
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
  assert.equal(classifyPullRequest({ ...base, draft: true, decision: 'CHANGES_REQUESTED' }), 'changes_requested');
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
