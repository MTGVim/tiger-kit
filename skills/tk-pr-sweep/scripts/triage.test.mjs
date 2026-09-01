import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import {
  checkProvider,
  classifyPullRequest,
  computeReplyEvidence,
  computeReReviewEvidence,
  computeSummaryCommentEvidence,
  computeReviewDecision,
  formatLocalTimestamp,
  flattenPages,
  isActionableText,
  latestAuthorResponseAfter,
  latestExternalMessagesByScope,
  loadOrBootstrapConfig,
  collectRows,
  normalizeGitHubText,
  parseRepoFromRemote,
  reReviewReviewerMarker,
  requestedTeamForUser,
  stripNoise,
  summaryCommentMarker,
  summaryCommentRequired,
  teamKeysForUser,
  triageConfigPath,
} from './triage.mjs';

test('formatLocalTimestamp renders a labeled host-local time', () => {
  const value = formatLocalTimestamp('2026-01-01T00:00:00Z');
  assert.match(value, /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \S+$/);
  assert.ok(value.endsWith(` ${Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC'}`));
});

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

test('check provider evidence distinguishes GitHub Actions, external, and unknown', () => {
  assert.equal(checkProvider({ app: { slug: 'github-actions' } }), 'github-actions');
  assert.equal(checkProvider({ app: { name: 'GitLab CI' } }), 'external');
  assert.equal(checkProvider({}), 'unknown');
});

test('stripNoise removes hidden and details content', () => {
  assert.equal(stripNoise('visible <!-- hidden --> <details>secret</details>'), 'visible');
});

test('normalizeGitHubText turns HTML breaks into TUI newlines', () => {
  assert.equal(normalizeGitHubText('first<br>second<br />third<BR/>fourth'), 'first\nsecond\nthird\nfourth');
});

test('collected review rows preserve clickable thread URLs and normalized bodies', () => {
  const rows = collectRows([], [{
    user: { login: 'reviewer' },
    created_at: '2026-01-01T00:00:00Z',
    body: 'Please add<br>test.',
    html_url: 'https://github.com/example/repo/pull/1#discussion_r1',
    id: 1,
  }], []);
  assert.equal(rows[0].body, 'Please add\ntest.');
  assert.equal(rows[0].url, 'https://github.com/example/repo/pull/1#discussion_r1');
  assert.equal(computeReplyEvidence(rows, 'author').outstanding[0].url, rows[0].url);
});

test('actionable text does not revive an old request after an LGTM-like message', () => {
  assert.equal(isActionableText('Please add a test.'), true);
  assert.equal(isActionableText('- **Fix:** Replace the stale ref before push.'), true);
  assert.equal(isActionableText('LGTM, no action.'), false);
});

test('review decision keeps a later COMMENTED review from clearing changes requested', () => {
  const review = computeReviewDecision([
    { user: { login: 'reviewer' }, state: 'CHANGES_REQUESTED', submitted_at: '2026-01-01T00:00:00Z' },
    { user: { login: 'reviewer' }, state: 'COMMENTED', submitted_at: '2026-01-02T00:00:00Z' },
  ], 'author');
  assert.equal(review.decision, 'CHANGES_REQUESTED');
  assert.deepEqual(review.latestReviews, [{
    login: 'reviewer',
    state: 'COMMENTED',
    timestamp: '2026-01-02T00:00:00Z',
    bot: false,
  }]);
  assert.deepEqual(review.approvedReviewers, []);
});

test('detects a missing re-review request after all actionable threads close', () => {
  const review = computeReviewDecision([
    { user: { login: 'reviewer' }, state: 'CHANGES_REQUESTED', submitted_at: '2026-01-01T00:00:00Z' },
  ], 'author');
  const evidence = computeReReviewEvidence(
    { requested_reviewers: [] },
    review,
    [],
  );
  assert.deepEqual(evidence.missingReviewers, ['reviewer']);
  assert.equal(evidence.verified, false);
  assert.equal(classifyPullRequest({
    draft: false,
    conflict: false,
    checksFailed: false,
    checksUnverifiable: false,
    decision: review.decision,
    authorRespondedToChangeRequest: true,
    latestExternalActionable: false,
    authorRespondedToLatestExternal: true,
    missingReReview: true,
  }), 'missing_re_review');
});

test('does not require re-review requests for bot change reviews', () => {
  const review = computeReviewDecision([
    { user: { login: 'dependabot[bot]', type: 'Bot' }, state: 'CHANGES_REQUESTED', submitted_at: '2026-01-01T00:00:00Z' },
  ], 'author');
  const evidence = computeReReviewEvidence({ requested_reviewers: [] }, review, []);
  assert.equal(evidence.required, false);
  assert.deepEqual(evidence.expectedReviewers, []);
});

test('detects a missing re-review request for a COMMENTED code-change reviewer', () => {
  const headSha = 'abc123';
  const review = computeReviewDecision([
    { id: 1, user: { login: 'reviewer' }, state: 'COMMENTED', submitted_at: '2026-01-01T00:00:00Z' },
  ], 'author');
  const summary = computeSummaryCommentEvidence([{
    user: { login: 'author' },
    created_at: '2026-01-02T00:00:00Z',
    body: `${summaryCommentMarker(headSha)}\n${reReviewReviewerMarker(headSha, 'reviewer')}`,
  }], 'author', headSha, true);
  const evidence = computeReReviewEvidence({ user: { login: 'author' }, requested_reviewers: [] }, review, [], summary);
  assert.deepEqual(evidence.expectedReviewers, ['reviewer']);
  assert.deepEqual(evidence.missingReviewers, ['reviewer']);
  assert.equal(evidence.verified, false);
});

test('a review submitted after the current-head summary satisfies re-review evidence', () => {
  const headSha = 'abc123';
  const review = computeReviewDecision([
    { id: 1, user: { login: 'reviewer' }, state: 'COMMENTED', submitted_at: '2026-01-03T00:00:00Z' },
  ], 'author');
  const summary = computeSummaryCommentEvidence([{
    user: { login: 'author' },
    created_at: '2026-01-02T00:00:00Z',
    body: `${summaryCommentMarker(headSha)}\n${reReviewReviewerMarker(headSha, 'reviewer')}`,
  }], 'author', headSha, true);
  const evidence = computeReReviewEvidence({ user: { login: 'author' }, requested_reviewers: [] }, review, [], summary);
  assert.deepEqual(evidence.reviewedAfterSummary, ['reviewer']);
  assert.deepEqual(evidence.missingReviewers, []);
  assert.equal(evidence.verified, true);
});

test('re-review evidence excludes the author, bots, and still-valid approvers', () => {
  const headSha = 'abc123';
  const review = computeReviewDecision([
    { user: { login: 'approver' }, state: 'APPROVED', submitted_at: '2026-01-01T00:00:00Z' },
  ], 'author');
  const summary = computeSummaryCommentEvidence([{
    user: { login: 'author' },
    created_at: '2026-01-02T00:00:00Z',
    body: [
      summaryCommentMarker(headSha),
      reReviewReviewerMarker(headSha, 'author'),
      reReviewReviewerMarker(headSha, 'dependabot[bot]'),
      reReviewReviewerMarker(headSha, 'approver'),
    ].join('\n'),
  }], 'author', headSha, true);
  const evidence = computeReReviewEvidence({ user: { login: 'author' }, requested_reviewers: [] }, review, [], summary);
  assert.deepEqual(evidence.expectedReviewers, []);
  assert.equal(evidence.required, false);
});

test('requires exactly one current-head Korean summary comment', () => {
  const headSha = 'abc123';
  const marker = summaryCommentMarker(headSha);
  const verified = computeSummaryCommentEvidence([
    { id: 1, user: { login: 'author' }, body: `${marker}\n리뷰 대응 요약`, html_url: 'https://example.test/1' },
  ], 'author', headSha, true);
  assert.equal(verified.verified, true);
  assert.equal(verified.count, 1);

  const stale = computeSummaryCommentEvidence([
    { id: 2, user: { login: 'author' }, body: `${summaryCommentMarker('oldsha')}\n리뷰 대응 요약` },
  ], 'author', headSha, true);
  assert.equal(stale.missing, true);
  assert.equal(stale.verified, false);
});

test('requires a summary after all actionable feedback is answered', () => {
  assert.equal(summaryCommentRequired(false, [], {
    outstanding: [],
    responded: [{ scope: 'inline:1' }],
  }), true);
  assert.equal(summaryCommentRequired(false, [{ id: 'thread-1' }], {
    outstanding: [],
    responded: [{ scope: 'inline:1' }],
  }), false);
  assert.equal(summaryCommentRequired(true, [], { outstanding: [], responded: [] }), true);
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

test('approval bounds reply evidence to comments after the approval', () => {
  const rows = [
    { scope: 'inline:1', login: 'reviewer', timestamp: '2026-01-01T00:00:00Z', body: 'Please fix this.' },
    { scope: 'inline:1', login: 'author', timestamp: '2026-01-02T00:00:00Z', body: 'Fixed.' },
    { scope: 'inline:2', login: 'reviewer', timestamp: '2026-01-04T00:00:00Z', body: 'Please add a test.' },
  ];
  const reply = computeReplyEvidence(rows, 'author', '2026-01-03T00:00:00Z');
  assert.deepEqual(reply.responded, []);
  assert.equal(reply.outstanding[0].scope, 'inline:2');
});

test('missing triage config bootstraps the current repository', async () => {
  const root = await mkdtemp(join(tmpdir(), 'tk-pr-sweep-triage-'));
  try {
    const path = triageConfigPath({ XDG_CONFIG_HOME: root });
    const loaded = loadOrBootstrapConfig(path, ['MTGVim/tiger-kit']);
    assert.deepEqual(loaded, { repositories: ['MTGVim/tiger-kit'], bootstrapped: true, source: 'config' });
    assert.deepEqual(JSON.parse(readFileSync(path, 'utf8')), { repositories: ['MTGVim/tiger-kit'] });
    assert.deepEqual(loadOrBootstrapConfig(path), {
      repositories: ['MTGVim/tiger-kit'],
      bootstrapped: false,
      source: 'config',
    });
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('report-only triage reads the origin without bootstrapping config', async () => {
  const root = await mkdtemp(join(tmpdir(), 'tk-pr-sweep-triage-report-'));
  try {
    const path = triageConfigPath({ XDG_CONFIG_HOME: root });
    const loaded = loadOrBootstrapConfig(
      path,
      ['MTGVim/tiger-kit'],
      { allowBootstrap: false },
    );
    assert.deepEqual(loaded, {
      repositories: ['MTGVim/tiger-kit'],
      bootstrapped: false,
      source: 'origin',
    });
    assert.equal(existsSync(path), false);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
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

test('classification priority is checks, conflict, outstanding reply, changes requested, draft', () => {
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
  assert.equal(classifyPullRequest({ ...base, conflict: false, unresolvedThreads: [{ id: 'thread-1' }] }), 'unresolved_threads');
  assert.equal(classifyPullRequest({ ...base, conflict: false }), 'needs_reply');
  assert.equal(classifyPullRequest({ ...base, conflict: false, latestExternalActionable: false }), 'changes_requested');
  assert.equal(classifyPullRequest({ ...base, conflict: false, authorRespondedToChangeRequest: true }), 'needs_reply');
  assert.equal(classifyPullRequest({ ...base, conflict: false, draft: false, decision: 'APPROVED' }), 'needs_reply');
  assert.equal(classifyPullRequest({ ...base, conflict: false, draft: false, decision: 'APPROVED', latestExternalActionable: false }), 'approved');
});
