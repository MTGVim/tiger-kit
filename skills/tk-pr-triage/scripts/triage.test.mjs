import assert from 'node:assert/strict';
import test from 'node:test';
import {
  classifyPullRequest,
  computeReplyEvidence,
  computeReviewDecision,
  flattenPages,
  isActionableText,
  latestAuthorResponseAfter,
  latestExternalMessagesByScope,
  parseRepoFromRemote,
  requestedTeamForUser,
  stripNoise,
  teamKeysForUser,
} from './triage.mjs';

test('parseRepoFromRemote supports SSH and HTTPS remotes', () => {
  assert.equal(parseRepoFromRemote('git@github.com:MTGVim/tiger-kit.git'), 'MTGVim/tiger-kit');
  assert.equal(parseRepoFromRemote('https://github.com/MTGVim/tiger-kit'), 'MTGVim/tiger-kit');
});

test('team review requests are matched against the authenticated user teams', () => {
  const keys = teamKeysForUser([{ organization: { login: 'MTGVim' }, slug: 'maintainers' }]);
  const requested = requestedTeamForUser({ requested_teams: [{ organization: { login: 'MTGVim' }, slug: 'maintainers' }] }, keys);
  assert.equal(requested.length, 1);
  assert.equal(requested[0].slug, 'maintainers');
});

test('flattenPages supports arrays and object pages', () => {
  assert.deepEqual(flattenPages([[{ id: 1 }], [{ id: 2 }]]), [{ id: 1 }, { id: 2 }]);
  assert.deepEqual(flattenPages([{ check_runs: [{ id: 3 }] }], 'check_runs'), [{ id: 3 }]);
});

test('stripNoise removes hidden and details content', () => {
  assert.equal(stripNoise('visible <!-- hidden --> <details>secret</details>'), 'visible');
});

test('actionable text does not revive an old request after an LGTM-like message', () => {
  assert.equal(isActionableText('Please add a test.'), true);
  assert.equal(isActionableText('LGTM, no action.'), false);
});

test('review decision keeps a later COMMENTED review from clearing changes requested', () => {
  assert.deepEqual(computeReviewDecision([
    { user: { login: 'reviewer' }, state: 'CHANGES_REQUESTED', submitted_at: '2026-01-01T00:00:00Z' },
    { user: { login: 'reviewer' }, state: 'COMMENTED', submitted_at: '2026-01-02T00:00:00Z' },
  ], 'author').decision, 'CHANGES_REQUESTED');
});

test('latest external message is scoped per thread', () => {
  const rows = [
    { scope: 'inline:1', login: 'reviewer', timestamp: '2026-01-01T00:00:00Z', body: 'Please rename this.' },
    { scope: 'inline:1', login: 'reviewer', timestamp: '2026-01-02T00:00:00Z', body: 'LGTM' },
    { scope: 'inline:2', login: 'reviewer', timestamp: '2026-01-03T00:00:00Z', body: 'Please add a test.' },
  ];
  assert.deepEqual(latestExternalMessagesByScope(rows, 'author').map((row) => row.scope), ['inline:1', 'inline:2']);
});

test('author response must be in the same thread scope', () => {
  const rows = [
    { scope: 'issue', login: 'reviewer', timestamp: '2026-01-01T00:00:00Z', body: 'Please fix this.' },
    { scope: 'other', login: 'author', timestamp: '2026-01-02T00:00:00Z', body: 'Unrelated note.' },
    { scope: 'issue', login: 'author', timestamp: '2026-01-03T00:00:00Z', body: 'Fixed.' },
  ];
  assert.equal(latestAuthorResponseAfter(rows, 'author', '2026-01-01T00:00:00Z', 'issue').timestamp, '2026-01-03T00:00:00Z');
  assert.equal(latestAuthorResponseAfter(rows, 'author', '2026-01-01T00:00:00Z', 'missing'), null);
  assert.equal(computeReplyEvidence(rows, 'author').responded.length, 1);
});

test('review response evidence is not inferred from an unrelated author comment', () => {
  const rows = [
    { scope: 'issue', login: 'reviewer', timestamp: '2026-01-01T00:00:00Z', body: 'Please fix this.' },
    { scope: 'other', login: 'author', timestamp: '2026-01-02T00:00:00Z', body: 'Unrelated note.' },
  ];
  const reply = computeReplyEvidence(rows, 'author');
  assert.equal(reply.outstanding.length, 1);
  assert.equal(reply.responded.length, 0);
});

test('unavailable check evidence is never classified as approval', () => {
  assert.equal(classifyPullRequest({
    draft: false,
    conflict: false,
    checksFailed: false,
    checksUnverifiable: true,
    decision: 'APPROVED',
    authorRespondedToChangeRequest: false,
    latestExternalActionable: false,
    authorRespondedToLatestExternal: false,
  }), 'checks_unverifiable');
});

test('classification priority is checks, conflict, changes requested, draft, reply', () => {
  const base = {
    draft: true,
    conflict: false,
    checksFailed: false,
    checksUnverifiable: false,
    decision: 'CHANGES_REQUESTED',
    authorRespondedToChangeRequest: false,
    latestExternalActionable: true,
    authorRespondedToLatestExternal: false,
  };
  assert.equal(classifyPullRequest({ ...base, checksUnverifiable: true }), 'checks_unverifiable');
  assert.equal(classifyPullRequest({ ...base, checksUnverifiable: false, conflict: true }), 'merge_conflict');
  assert.equal(classifyPullRequest({ ...base, conflict: false }), 'changes_requested');
  assert.equal(classifyPullRequest({ ...base, conflict: false, draft: false, decision: 'APPROVED' }), 'needs_reply');
  assert.equal(classifyPullRequest({ ...base, conflict: false, draft: false, decision: 'APPROVED', latestExternalActionable: false }), 'approved');
});
