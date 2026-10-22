import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import {
  checkProvider,
  classifyCommentAuthorship,
  classifyPullRequest,
  computeReplyEvidence,
  computeReReviewEvidence,
  computeSummaryCommentEvidence,
  computeReviewDecision,
  formatLocalTimestamp,
  flattenPages,
  isActionableText,
  isBotAccount,
  latestAuthorResponseAfter,
  latestExternalMessagesByScope,
  latestSummaryPrerequisite,
  loadCommentMarkers,
  loadOrBootstrapConfig,
  loadToolAuthoredCommentMarkers,
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

test('comment authorship prefers a configured body marker over a human account', () => {
  const markers = ['<!-- review-tool:'];
  const marked = classifyCommentAuthorship({
    user: { login: 'collaborator', type: 'User' },
    body: 'Please fix this.\n<!-- review-tool:rules/no-null -->',
  }, markers);
  assert.deepEqual(marked, {
    kind: 'tool-authored',
    basis: 'configured-marker',
    marker: '<!-- review-tool:',
  });

  const unmarked = classifyCommentAuthorship({
    user: { login: 'collaborator', type: 'User' },
    body: 'Please fix this.',
  }, markers);
  assert.deepEqual(unmarked, {
    kind: 'human-authored',
    basis: 'human-account-fallback',
    marker: null,
  });
});

test('comment authorship falls back conservatively when marker config is absent', () => {
  assert.deepEqual(classifyCommentAuthorship({
    user: { login: 'collaborator', type: 'User' },
    body: 'Please fix this.',
  }), {
    kind: 'human-authored',
    basis: 'no-marker-config',
    marker: null,
  });
  assert.equal(isBotAccount({ login: 'automation[bot]', type: 'User' }), true);
  assert.equal(classifyCommentAuthorship({
    user: { login: 'automation[bot]', type: 'User' },
    body: 'Please fix this.',
  }).kind, 'tool-authored');
});

test('reply evidence records marker-based authorship without changing account review state', () => {
  const body = 'Please add a regression test.\n<!-- review-tool:rules/testing -->';
  const rows = collectRows([], [{
    user: { login: 'collaborator', type: 'User' },
    created_at: '2026-01-01T00:00:00Z',
    body,
    id: 1,
  }], []);
  const reply = computeReplyEvidence(rows, 'author', null, ['<!-- review-tool:']);
  assert.equal(reply.outstanding[0].authorship, 'tool-authored');
  assert.equal(reply.outstanding[0].authorshipBasis, 'configured-marker');

  const review = computeReviewDecision([{
    user: { login: 'collaborator', type: 'User' },
    state: 'CHANGES_REQUESTED',
    submitted_at: '2026-01-01T00:00:00Z',
    body,
  }], 'author');
  assert.deepEqual(review.changeReviewers, [{
    login: 'collaborator',
    timestamp: '2026-01-01T00:00:00Z',
  }]);
  assert.deepEqual(computeReReviewEvidence({ requested_reviewers: [] }, review, []).missingReviewers, ['collaborator']);
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
  const headSha = 'a'.repeat(40);
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
  const headSha = 'a'.repeat(40);
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
  const headSha = 'a'.repeat(40);
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
  const headSha = 'a'.repeat(40);
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

test('rejects duplicate markers and summaries posted before the latest reply', () => {
  const headSha = 'a'.repeat(40);
  const marker = summaryCommentMarker(headSha);
  const afterReply = latestSummaryPrerequisite({responded:[{responseAt:'2026-01-03T00:00:00Z'}]});
  const early = computeSummaryCommentEvidence([{
    user:{login:'author'}, created_at:'2026-01-02T00:00:00Z', body:marker,
  }], 'author', headSha, true, afterReply);
  assert.equal(early.stale, true);
  assert.equal(early.verified, false);
  const duplicate = computeSummaryCommentEvidence([{
    user:{login:'author'}, created_at:'2026-01-04T00:00:00Z', body:`${marker}\n${marker}`,
  }], 'author', headSha, true, afterReply);
  assert.equal(duplicate.duplicate, true);
  assert.equal(duplicate.verified, false);
  const current = computeSummaryCommentEvidence([{
    user:{login:'author'}, created_at:'2026-01-04T00:00:00Z', body:marker,
  }], 'author', headSha, true, afterReply);
  assert.equal(current.verified, true);
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

test('skips a summary when no actionable reply or re-review was published', () => {
  assert.equal(summaryCommentRequired(false, [], { outstanding: [], responded: [] }), false);
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
    assert.deepEqual(loaded, {
      repositories: ['MTGVim/tiger-kit'],
      toolAuthoredCommentMarkers: [],
      informationalCommentMarkers: [],
      bootstrapped: true,
      source: 'config',
    });
    assert.deepEqual(JSON.parse(readFileSync(path, 'utf8')), { repositories: ['MTGVim/tiger-kit'] });
    assert.deepEqual(loadOrBootstrapConfig(path), {
      repositories: ['MTGVim/tiger-kit'],
      toolAuthoredCommentMarkers: [],
      informationalCommentMarkers: [],
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
      toolAuthoredCommentMarkers: [],
      informationalCommentMarkers: [],
      bootstrapped: false,
      source: 'origin',
    });
    assert.equal(existsSync(path), false);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('triage config accepts optional tool-authorship marker prefixes', async () => {
  const root = await mkdtemp(join(tmpdir(), 'tk-pr-sweep-triage-markers-'));
  try {
    const path = triageConfigPath({ XDG_CONFIG_HOME: root });
    loadOrBootstrapConfig(path, ['MTGVim/tiger-kit']);
    const config = JSON.parse(readFileSync(path, 'utf8'));
    config.toolAuthoredCommentMarkers = ['<!-- review-tool:', '<!-- review-tool:'];
    writeFileSync(path, `${JSON.stringify(config, null, 2)}\n`);
    assert.deepEqual(loadOrBootstrapConfig(path).toolAuthoredCommentMarkers, ['<!-- review-tool:']);
    assert.deepEqual(loadToolAuthoredCommentMarkers(path), ['<!-- review-tool:']);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('issue comments from different accounts remain independently visible', () => {
  const request = {
    user: { login: 'review-bot[bot]', type: 'Bot' },
    created_at: '2026-01-01T00:00:00Z',
    body: 'Review skipped. Please re-run with the command.',
    id: 1,
  };
  const status = {
    user: { login: 'ci-bot[bot]', type: 'Bot' },
    created_at: '2026-01-01T00:01:00Z',
    body: 'Deployment preview ready.',
    id: 2,
  };
  const reply = computeReplyEvidence(collectRows([], [], [request, status]), 'author');
  assert.deepEqual(reply.outstanding.map((item) => item.id), [1]);
  assert.equal(reply.outstanding[0].scope, 'issue');

  const retracted = { ...request, created_at: '2026-01-01T00:02:00Z', body: 'LGTM, no action.', id: 3 };
  assert.equal(computeReplyEvidence(collectRows([], [], [request, retracted]), 'author').outstanding.length, 0);

  const answer = { user: { login: 'author' }, created_at: '2026-01-01T00:03:00Z', body: 'Re-ran the review.', id: 4 };
  const answered = computeReplyEvidence(collectRows([], [], [request, status, answer]), 'author');
  assert.equal(answered.outstanding.length, 0);
  assert.deepEqual(answered.responded.map((item) => item.id), [1]);
});

test('informational markers exclude only matching comments from reply triage', () => {
  const report = {
    user: { login: 'ci-bot[bot]', type: 'Bot' },
    created_at: '2026-01-02T00:00:00Z',
    body: '<!-- status-report:coverage -->\nTest suite run success',
    id: 2,
  };
  const request = {
    user: { login: 'review-bot[bot]', type: 'Bot' },
    created_at: '2026-01-01T00:00:00Z',
    body: 'Please re-run this review.',
    id: 1,
  };
  const rows = collectRows([], [], [request, report]);
  assert.deepEqual(computeReplyEvidence(rows, 'author').outstanding.map((item) => item.id), [1, 2]);
  assert.deepEqual(computeReplyEvidence(rows, 'author', null, [], ['<!-- status-report:']).outstanding.map((item) => item.id), [1]);
  assert.equal(computeReplyEvidence(collectRows([], [], [report]), 'author', null, [], ['<!-- status-report:']).outstanding.length, 0);
  assert.equal(computeReplyEvidence(collectRows([], [], [report]), 'author').outstanding.length, 1);
});

test('informational comment markers use the same strict config validation', async () => {
  const root = await mkdtemp(join(tmpdir(), 'tk-pr-sweep-informational-markers-'));
  try {
    const path = triageConfigPath({ XDG_CONFIG_HOME: root });
    mkdirSync(join(root, 'tigerkit'), { recursive: true });
    writeFileSync(path, JSON.stringify({
      repositories: ['MTGVim/tiger-kit'],
      informationalCommentMarkers: ['<!-- status-report:', '<!-- status-report:'],
    }));
    assert.deepEqual(loadCommentMarkers(path, 'informationalCommentMarkers'), ['<!-- status-report:']);
    assert.deepEqual(loadOrBootstrapConfig(path).informationalCommentMarkers, ['<!-- status-report:']);
    writeFileSync(path, JSON.stringify({
      repositories: ['MTGVim/tiger-kit'],
      informationalCommentMarkers: ['status-report:'],
    }));
    assert.throws(() => loadOrBootstrapConfig(path), /HTML-comment prefix strings/);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('a current-head summary remains verified when it is also the only reply', () => {
  const headSha = 'a'.repeat(40);
  const summary = {
    user: { login: 'author' },
    created_at: '2026-01-02T00:00:00Z',
    body: `${summaryCommentMarker(headSha)}\nSummary`,
    id: 2,
  };
  const request = {
    user: { login: 'review-bot[bot]', type: 'Bot' },
    created_at: '2026-01-01T00:00:00Z',
    body: 'Please fix this.',
    id: 1,
  };
  const reply = computeReplyEvidence(collectRows([], [], [request, summary]), 'author');
  assert.equal(reply.responded.length, 1);
  assert.equal(summaryCommentRequired(false, [], reply), true);
  const evidence = computeSummaryCommentEvidence([summary], 'author', headSha, true);
  assert.equal(evidence.verified, true);
  assert.equal(evidence.count, 1);
});

test('an explicit repository can still load marker config without bootstrapping it', async () => {
  const root = await mkdtemp(join(tmpdir(), 'tk-pr-sweep-triage-explicit-repo-'));
  try {
    const path = triageConfigPath({ XDG_CONFIG_HOME: root });
    assert.deepEqual(loadToolAuthoredCommentMarkers(path), []);
    assert.equal(existsSync(path), false);

    loadOrBootstrapConfig(path, ['different/repository']);
    writeFileSync(path, JSON.stringify({
      repositories: ['different/repository'],
      toolAuthoredCommentMarkers: ['<!-- review-tool:'],
    }));
    assert.deepEqual(loadToolAuthoredCommentMarkers(path), ['<!-- review-tool:']);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test('triage config rejects broad non-comment authorship markers', async () => {
  const root = await mkdtemp(join(tmpdir(), 'tk-pr-sweep-triage-invalid-marker-'));
  try {
    const path = triageConfigPath({ XDG_CONFIG_HOME: root });
    loadOrBootstrapConfig(path, ['MTGVim/tiger-kit']);
    writeFileSync(path, JSON.stringify({
      repositories: ['MTGVim/tiger-kit'],
      toolAuthoredCommentMarkers: ['review-tool:'],
    }));
    assert.throws(() => loadOrBootstrapConfig(path), /HTML-comment prefix strings/);
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

test('a summary that is itself the only response is not stale against itself', () => {
  const headSha = 'a'.repeat(40);
  const marker = summaryCommentMarker(headSha);
  const summary = {
    user: { login: 'author' }, created_at: '2026-01-02T00:00:00Z', body: `${marker}\nSummary`, id: 2,
  };
  const botComment = {
    user: { login: 'review-bot[bot]', type: 'Bot' }, created_at: '2026-01-01T00:00:00Z', body: 'Please fix this.', id: 1,
  };
  const selfResponse = computeReplyEvidence(collectRows([], [], [botComment, summary]), 'author');
  assert.equal(selfResponse.responded.length, 1);
  assert.equal(selfResponse.responded[0].responseIsSummary, true);
  const verified = computeSummaryCommentEvidence(
    [summary], 'author', headSha, true, latestSummaryPrerequisite(selfResponse),
  );
  assert.equal(verified.stale, false);
  assert.equal(verified.verified, true);

  const laterReply = {
    user: { login: 'author' }, created_at: '2026-01-03T00:00:00Z', body: 'Done.', id: 3,
  };
  const laterBot = { ...botComment, created_at: '2026-01-02T12:00:00Z', id: 4 };
  const stale = computeSummaryCommentEvidence(
    [summary],
    'author',
    headSha,
    true,
    latestSummaryPrerequisite(computeReplyEvidence(collectRows([], [], [botComment, summary, laterBot, laterReply]), 'author')),
  );
  assert.equal(stale.stale, true);
  assert.equal(stale.verified, false);
});


test('an active unresolved thread needs a reply without request-language patterns', () => {
  const body = '테스트를 추가하거나 설명을 보강하면 두 지적이 함께 해소됩니다.';
  assert.equal(isActionableText(body), false);
  const comments = [{ id: 11, user: { login: 'reviewer' }, created_at: '2026-01-01T00:00:00Z', body }];
  const threads = [{ isResolved: false, isOutdated: false, comments: { nodes: [{ databaseId: 11 }] } }];
  const evidence = (items, states = threads, markers = []) => computeReplyEvidence(
    collectRows([], items, []), 'author', '2026-01-02T00:00:00Z', [], markers, states,
  );
  assert.deepEqual(evidence(comments).outstanding.map((item) => item.id), [11]);
  const answer = { id: 12, in_reply_to_id: 11, user: { login: 'author' }, created_at: '2026-01-03T00:00:00Z', body: '반영했습니다.' };
  const answered = evidence([...comments, answer]);
  assert.equal(answered.outstanding.length, 0);
  assert.deepEqual(answered.responded.map((item) => item.id), [11]);
  const unrelated = { ...answer, in_reply_to_id: 99 };
  assert.equal(evidence([...comments, unrelated]).outstanding.length, 1);
  const followup = { id: 13, in_reply_to_id: 11, user: { login: 'reviewer' }, created_at: '2026-01-04T00:00:00Z', body };
  assert.deepEqual(evidence([...comments, answer, followup]).outstanding.map((item) => item.id), [13]);
  for (const state of [{ isResolved: true }, { isOutdated: true }]) {
    assert.equal(evidence(comments, [{ ...threads[0], ...state }]).outstanding.length, 0);
    assert.equal(evidence([{ ...comments[0], body: 'Please fix this.', created_at: '2026-01-03T00:00:00Z' }], [{ ...threads[0], ...state }]).outstanding.length, 0);
  }
  assert.equal(evidence([{ ...comments[0], body: 'LGTM, no action.' }]).outstanding.length, 0);
  assert.equal(evidence([{ ...comments[0], body: '<!-- status-report:ok -->' + body }], threads, ['<!-- status-report:']).outstanding.length, 0);
  assert.equal(evidence([{ ...comments[0], body: '<!-- hidden -->' }]).outstanding.length, 0);
  assert.equal(evidence(comments, []).outstanding.length, 0);
});

test('closed answered threads retain summary prerequisites without reopening replies', () => {
  const rows = collectRows([], [
    { id: 11, user: { login: 'reviewer' }, created_at: '2026-01-01T00:00:00Z', body: '설명을 보강하면 해소됩니다.' },
    { id: 12, in_reply_to_id: 11, user: { login: 'author' }, created_at: '2026-01-02T00:00:00Z', body: 'Done.' },
  ], []);
  const threads = [{ isResolved: true, isOutdated: false, comments: { nodes: [{ databaseId: 11 }] } }];
  const reply = computeReplyEvidence(rows, 'author', null, [], [], threads);
  assert.equal(reply.outstanding.length, 0);
  assert.equal(summaryCommentRequired(false, [], reply), true);
});

test('malformed re-review markers fail independently of shell-built expected strings', () => {
  const head = 'a'.repeat(40);
  const check = (suffix, required = true) => computeSummaryCommentEvidence([{
    user: { login: 'author' }, body: summaryCommentMarker(head) + '\n' + suffix,
  }], 'author', head, required);
  for (const broken of [
    '<!-- tigerkit:pr-rereview:.eviewer -->',
    '<!-- tigerkit:pr-rereview:abc123:reviewer -->',
    '<!-- tigerkit:pr-rereview:' + 'g'.repeat(40) + ':reviewer -->',
    '<!-- tigerkit:pr-rereview:' + head + ': -->',
    '<!-- tigerkit:pr-rereview:' + head + ':reviewer',
  ]) {
    for (const required of [true, false]) {
      const result = check(broken, required);
      assert.equal(result.malformed, true, broken);
      assert.equal(result.verified, false, broken);
      assert.deepEqual(result.reviewers, []);
    }
  }
  const valid = check(reReviewReviewerMarker(head, 'reviewer'));
  assert.equal(valid.malformed, false);
  assert.equal(valid.verified, true);
  assert.deepEqual(valid.reviewers, ['reviewer']);
  assert.equal(check('', false).verified, true);
  assert.equal(check(reReviewReviewerMarker(head, 'reviewer') + '\n<!-- tigerkit:pr-rereview:.other -->').verified, false);
});


test('CLI joins fresh GraphQL thread state to REST comments and surfaces malformed summaries', async () => {
  const root = await mkdtemp(join(tmpdir(), 'tk-pr-sweep-thread-state-'));
  try {
    writeFileSync(join(root, 'gh'), `#!/usr/bin/env node
const path = process.argv[3];
const head = 'a'.repeat(40);
const pull = { number: 1, user: { login: 'author' }, head: { sha: head }, mergeable: true, mergeable_state: 'clean' };
let result;
if (path === 'user') result = { login: 'author' };
else if (path.startsWith('user/teams')) result = [];
else if (path === 'graphql') {
  if (!process.argv.some((arg) => arg.includes('databaseId'))) process.exit(2);
  result = { data: { repository: { pullRequest: { reviewThreads: { nodes: [{
    id: 'thread1', isResolved: process.env.CLOSED === '1', isOutdated: false,
    comments: { nodes: [{ id: 'comment-node-11', databaseId: 11 }] }
  }], pageInfo: { hasNextPage: false, endCursor: null } } } } } };
}
else if (path.includes('/pulls?')) result = [pull];
else if (path.endsWith('/pulls/1')) result = pull;
else if (path.includes('/pulls/1/comments')) result = [{
  id: 11, user: { login: 'reviewer' }, created_at: '2026-01-01T00:00:00Z',
  body: '테스트를 추가하거나 설명을 보강하면 두 지적이 함께 해소됩니다.',
}];
else if (path.includes('/issues/1/comments')) result = [{
  id: 21, user: { login: 'author' }, created_at: '2026-01-02T00:00:00Z',
  body: '<!-- tigerkit:pr-summary:' + head + ' -->\\n<!-- tigerkit:pr-rereview:.eviewer -->',
}];
else if (path.includes('/check-runs')) result = { check_runs: [] };
else if (path.endsWith('/status')) result = { state: 'success' };
else if (path.includes('/reviews')) result = [];
else process.exit(3);
console.log(JSON.stringify(result));
`, { mode: 0o755 });
    const run = (closed) => JSON.parse(execFileSync(process.execPath, [
      new URL('./triage.mjs', import.meta.url).pathname, '--repo', 'example/repo', '--no-bootstrap',
    ], { encoding: 'utf8', env: { ...process.env, PATH: root + ':' + process.env.PATH, XDG_CONFIG_HOME: root, CLOSED: closed ? '1' : '0' } }));
    const open = run(false);
    assert.deepEqual(open.failures, []);
    assert.equal(open.items[0].evidence.replyEvidence.outstanding[0].id, 11);
    const closed = run(true);
    assert.deepEqual(closed.failures, []);
    assert.equal(closed.items[0].category, 'missing_summary_comment');
    assert.equal(closed.items[0].evidence.summaryComment.malformed, true);
    assert.equal(closed.items[0].evidence.summaryComment.verified, false);
    assert.equal(closed.items[0].evidence.replyEvidence.outstanding.length, 0);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});
