#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { realpathSync } from 'node:fs';

const SUCCESS_CONCLUSIONS = new Set(['success', 'neutral', 'skipped']);
const NO_ACTION_PATTERN = /(?:no action|nothing to change|looks good|lgtm|이상 발견 없음|조치 없음)/i;
const REQUEST_PATTERN = /(?:\?|please\b|could you\b|would you\b|\b(?:should|must|need(?:s|ed)? to)\b|(?:^|[\n.!?]\s*)(?:please\s+)?(?:change|rename|remove|add|use|replace|update|fix|move|extract|avoid|prefer|document|test|handle|return|make|consider)\b|부탁|요청|해\s*주(?:세요|시겠|길)?|(?:수정|변경|추가|삭제|제거|교체|적용|처리|분리|이동|확인)(?:해|하세요|해주세요|해야|할 필요))/i;

export function stripNoise(body = '') {
  return body
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<details>[\s\S]*?<\/details>/gi, '')
    .trim();
}

export function isActionableText(body = '') {
  const text = stripNoise(body);
  if (!text || NO_ACTION_PATTERN.test(text)) return false;
  return REQUEST_PATTERN.test(text);
}

export function parseRepoFromRemote(remote) {
  const value = String(remote || '').trim().replace(/\.git$/, '');
  let match = value.match(/^[^@\s]+@[^:\s]+:([^/\s]+\/[^/\s]+)$/);
  if (match) return match[1];
  match = value.match(/^(?:https?|ssh):\/\/[^/]+\/(?:[^/]+@)?([^/\s]+\/[^/\s]+)$/);
  if (match) return match[1];
  return null;
}

export function computeReviewDecision(reviews, authorLogin) {
  const latestByReviewer = new Map();
  const ordered = [...reviews].sort((a, b) => {
    const left = a.submitted_at || a.created_at || '';
    const right = b.submitted_at || b.created_at || '';
    return left.localeCompare(right);
  });
  for (const review of ordered) {
    const login = review.user?.login;
    const state = review.state;
    if (!login || login === authorLogin || state === 'PENDING') continue;
    const timestamp = review.submitted_at || review.created_at || '';
    const previous = latestByReviewer.get(login);
    if (state === 'APPROVED' || state === 'CHANGES_REQUESTED') {
      latestByReviewer.set(login, { state, timestamp });
    } else if (state === 'DISMISSED') {
      latestByReviewer.delete(login);
    } else if (!previous) {
      latestByReviewer.set(login, { state, timestamp });
    }
  }
  const entries = [...latestByReviewer.values()];
  const changes = entries.filter((entry) => entry.state === 'CHANGES_REQUESTED');
  if (changes.length) {
    return {
      decision: 'CHANGES_REQUESTED',
      decisiveAt: changes.map((entry) => entry.timestamp).sort().at(-1) || null,
    };
  }
  const approvals = entries.filter((entry) => entry.state === 'APPROVED');
  if (approvals.length) {
    return {
      decision: 'APPROVED',
      decisiveAt: approvals.map((entry) => entry.timestamp).sort().at(-1) || null,
    };
  }
  return { decision: 'REVIEW_REQUIRED', decisiveAt: null };
}

export function latestExternalMessagesByScope(rows, authorLogin) {
  const latest = new Map();
  const ordered = [...rows].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  for (const row of ordered) {
    if (
      row.replyEligible !== false
      && row.scope
      && row.login
      && row.login !== authorLogin
      && stripNoise(row.body)
    ) {
      latest.set(row.scope, row);
    }
  }
  return [...latest.values()];
}

export function hasAuthorResponseAfter(rows, authorLogin, timestamp, scope = null) {
  if (!timestamp) return false;
  return rows.some(
    (row) => row.login === authorLogin
      && (!scope || row.scope === scope)
      && new Date(row.timestamp) > new Date(timestamp),
  );
}

export function computeReplyEvidence(rows, authorLogin) {
  const actionable = latestExternalMessagesByScope(rows, authorLogin)
    .filter((row) => isActionableText(row.body));
  const outstanding = [];
  const responded = [];
  for (const row of actionable) {
    const target = hasAuthorResponseAfter(rows, authorLogin, row.timestamp, row.scope)
      ? responded
      : outstanding;
    target.push({ scope: row.scope, login: row.login, timestamp: row.timestamp, id: row.id || null });
  }
  return { outstanding, responded };
}

export function classifyPullRequest({
  draft,
  conflict,
  checksFailed,
  decision,
  authorRespondedToChangeRequest,
  latestExternalActionable,
  authorRespondedToLatestExternal,
}) {
  if (conflict) return 'merge_conflict';
  if (checksFailed) return 'checks_failed';
  if (decision === 'CHANGES_REQUESTED') {
    return authorRespondedToChangeRequest ? 'awaiting_re_review' : 'changes_requested';
  }
  if (draft) return 'draft';
  if (latestExternalActionable) {
    return authorRespondedToLatestExternal ? 'awaiting_re_review' : 'needs_reply';
  }
  if (decision === 'APPROVED') return 'approved';
  return 'pending_review';
}

function run(command, args, { allowFailure = false } = {}) {
  try {
    return {
      ok: true,
      stdout: execFileSync(command, args, {
        encoding: 'utf8',
        maxBuffer: 32 * 1024 * 1024,
        stdio: ['ignore', 'pipe', 'pipe'],
      }).trim(),
    };
  } catch (error) {
    const stderr = String(error.stderr || error.message || '').trim();
    if (allowFailure) return { ok: false, error: stderr };
    throw new Error(stderr);
  }
}

function ghObject(path) {
  const result = run('gh', ['api', path], { allowFailure: true });
  if (!result.ok) return result;
  try {
    return { ok: true, data: JSON.parse(result.stdout) };
  } catch (error) {
    return { ok: false, error: `Invalid JSON from ${path}: ${error.message}` };
  }
}

export function flattenPages(pages, arrayField = null) {
  return pages.flatMap((page) => {
    if (Array.isArray(page)) return page;
    if (arrayField && Array.isArray(page?.[arrayField])) return page[arrayField];
    return [];
  });
}

function ghList(path, arrayField = null) {
  const result = run('gh', ['api', path, '--paginate', '--slurp'], { allowFailure: true });
  if (!result.ok) return result;
  try {
    const pages = JSON.parse(result.stdout || '[]');
    return { ok: true, data: flattenPages(pages, arrayField) };
  } catch (error) {
    return { ok: false, error: `Invalid paginated JSON from ${path}: ${error.message}` };
  }
}

function currentRepository() {
  const remote = run('git', ['remote', 'get-url', 'origin'], { allowFailure: true });
  if (!remote.ok) return null;
  return parseRepoFromRemote(remote.stdout);
}

function collectRows(reviews, inlineComments, issueComments) {
  return [
    ...reviews.map((review) => ({
      login: review.user?.login,
      timestamp: review.submitted_at || review.created_at,
      body: review.body || '',
      kind: 'review',
      state: review.state,
      replyEligible: false,
    })),
    ...inlineComments.map((comment) => ({
      login: comment.user?.login,
      timestamp: comment.created_at,
      body: comment.body || '',
      kind: 'inline_comment',
      id: comment.id,
      scope: `inline:${comment.in_reply_to_id || comment.id}`,
    })),
    ...issueComments.map((comment) => ({
      login: comment.user?.login,
      timestamp: comment.created_at,
      body: comment.body || '',
      kind: 'issue_comment',
      id: comment.id,
      scope: 'issue',
    })),
  ].filter((row) => row.timestamp);
}

function checkState(repo, sha) {
  const checkRuns = ghList(`repos/${repo}/commits/${sha}/check-runs?per_page=100`, 'check_runs');
  const combined = ghObject(`repos/${repo}/commits/${sha}/status`);
  const failures = [];
  if (checkRuns.ok) {
    for (const check of checkRuns.data) {
      if (check.status === 'completed' && !SUCCESS_CONCLUSIONS.has(check.conclusion)) {
        failures.push({ kind: 'check_run', name: check.name, state: check.conclusion });
      }
    }
  }
  if (combined.ok && ['failure', 'error'].includes(combined.data.state)) {
    for (const status of combined.data.statuses || []) {
      if (['failure', 'error'].includes(status.state)) {
        failures.push({ kind: 'status', name: status.context, state: status.state });
      }
    }
  }
  const errors = [];
  if (!checkRuns.ok) errors.push(checkRuns.error);
  if (!combined.ok) errors.push(combined.error);
  return { failures, errors };
}

function pullItem(repo, pull, category, evidence = {}) {
  return {
    repository: repo,
    number: pull.number,
    title: pull.title,
    url: pull.html_url,
    author: pull.user?.login,
    head: pull.head?.ref,
    headSha: pull.head?.sha,
    base: pull.base?.ref,
    draft: Boolean(pull.draft),
    category,
    evidence,
  };
}

async function triageRepository(repo, login) {
  const openPulls = ghList(`repos/${repo}/pulls?state=open&per_page=100`);
  if (!openPulls.ok) return { repository: repo, items: [], failures: [openPulls.error] };

  const items = [];
  const failures = [];
  for (const pull of openPulls.data) {
    const requested = (pull.requested_reviewers || []).some((reviewer) => reviewer.login === login);
    if (pull.user?.login !== login) {
      if (requested) items.push(pullItem(repo, pull, 'review_requested'));
      continue;
    }

    let detail = ghObject(`repos/${repo}/pulls/${pull.number}`);
    if (detail.ok && (detail.data.mergeable === null || detail.data.mergeable_state === 'unknown')) {
      await new Promise((resolve) => setTimeout(resolve, 750));
      detail = ghObject(`repos/${repo}/pulls/${pull.number}`);
    }
    const reviews = ghList(`repos/${repo}/pulls/${pull.number}/reviews?per_page=100`);
    const inlineComments = ghList(`repos/${repo}/pulls/${pull.number}/comments?per_page=100`);
    const issueComments = ghList(`repos/${repo}/issues/${pull.number}/comments?per_page=100`);
    const required = [detail, reviews, inlineComments, issueComments];
    if (required.some((result) => !result.ok)) {
      failures.push(
        `#${pull.number}: ${required.filter((result) => !result.ok).map((result) => result.error).join('; ')}`,
      );
      continue;
    }
    if (detail.data.mergeable === null || detail.data.mergeable_state === 'unknown') {
      failures.push(`#${pull.number}: mergeability remained unknown after retry`);
      continue;
    }

    const rows = collectRows(reviews.data, inlineComments.data, issueComments.data);
    const review = computeReviewDecision(reviews.data, login);
    const reply = computeReplyEvidence(rows, login);
    const check = checkState(repo, pull.head.sha);
    failures.push(...check.errors.map((error) => `#${pull.number}: ${error}`));

    const category = classifyPullRequest({
      draft: pull.draft,
      conflict: detail.data.mergeable_state === 'dirty',
      checksFailed: check.failures.length > 0,
      decision: review.decision,
      authorRespondedToChangeRequest: hasAuthorResponseAfter(rows, login, review.decisiveAt),
      latestExternalActionable: reply.outstanding.length > 0 || reply.responded.length > 0,
      authorRespondedToLatestExternal: reply.outstanding.length === 0 && reply.responded.length > 0,
    });

    if (!['approved', 'pending_review'].includes(category)) {
      items.push(
        pullItem(repo, pull, category, {
          reviewDecision: review.decision,
          decisiveAt: review.decisiveAt,
          replyEvidence: reply,
          failedChecks: check.failures,
          mergeableState: detail.data.mergeable_state,
        }),
      );
    }
  }
  return { repository: repo, items, failures };
}

function parseArgs(argv) {
  const repos = [];
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === '--repo') {
      const repo = argv[index + 1];
      if (!repo) throw new Error('--repo requires owner/name');
      repos.push(repo);
      index += 1;
    } else if (value === '--help' || value === '-h') {
      return { help: true, repos: [] };
    } else {
      throw new Error(`Unknown argument: ${value}`);
    }
  }
  return { help: false, repos };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log('Usage: node triage.mjs [--repo owner/name]...');
    return;
  }

  const user = ghObject('user');
  if (!user.ok) throw new Error(`Unable to resolve GitHub identity: ${user.error}`);
  const repos = args.repos.length ? args.repos : [currentRepository()].filter(Boolean);
  if (!repos.length) throw new Error('No repository supplied and origin could not be resolved');

  const results = [];
  for (const repo of [...new Set(repos)]) results.push(await triageRepository(repo, user.data.login));
  const items = results.flatMap((result) => result.items);
  const failures = results.flatMap((result) => result.failures.map((error) => ({ repository: result.repository, error })));
  const counts = items.reduce((accumulator, item) => {
    accumulator[item.category] = (accumulator[item.category] || 0) + 1;
    return accumulator;
  }, {});

  console.log(JSON.stringify({
    generatedAt: new Date().toISOString(),
    login: user.data.login,
    repositories: [...new Set(repos)],
    counts,
    items,
    failures,
  }, null, 2));
}

function isDirectRun() {
  try {
    return realpathSync(process.argv[1]) === realpathSync(fileURLToPath(import.meta.url));
  } catch {
    return false;
  }
}

if (isDirectRun()) {
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
