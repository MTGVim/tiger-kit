#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { mkdirSync, readFileSync, realpathSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';

const SUCCESS_CONCLUSIONS = new Set(['success', 'neutral', 'skipped']);
const NO_ACTION_PATTERN = /(?:no action|nothing to change|looks good|lgtm|이상 발견 없음|조치 없음)/i;
const REQUEST_PATTERN = /(?:\?|please\b|could you\b|would you\b|\b(?:should|must|need(?:s|ed)? to)\b|(?:^|[\n.!?]\s*)(?:please\s+)?(?:change|rename|remove|add|use|replace|update|fix|move|extract|avoid|prefer|document|test|handle|return|make|consider)\b|부탁|요청|해\s*주(?:세요|시겠|길)?|(?:수정|변경|추가|삭제|제거|교체|적용|처리|분리|이동|확인)(?:해|하세요|해주세요|해야|할 필요))/i;

export function stripNoise(body = '') {
  return body.replace(/<!--[\s\S]*?-->/g, '').replace(/<details>[\s\S]*?<\/details>/gi, '').trim();
}

export function isActionableText(body = '') {
  const text = stripNoise(body);
  const normalized = text.replace(/(^|\n)\s*(?:[-*#>]+\s*)+/g, '$1');
  return Boolean(text) && !NO_ACTION_PATTERN.test(text) && REQUEST_PATTERN.test(normalized);
}

export function parseRepoFromRemote(remote) {
  const value = String(remote || '').trim().replace(/\.git$/, '');
  let match = value.match(/^[^@\s]+@[^:\s]+:([^/\s]+\/[^/\s]+)$/);
  if (match) return match[1];
  match = value.match(/^(?:https?|ssh):\/\/[^/]+\/(?:[^/]+@)?([^/\s]+\/[^/\s]+)$/);
  return match ? match[1] : null;
}

export function teamKeysForUser(teams) {
  return new Set(teams
    .map((team) => {
      const organization = team.organization?.login || team.organization?.name;
      return organization && team.slug ? `${organization}/${team.slug}` : null;
    })
    .filter(Boolean));
}

export function requestedTeamForUser(pull, teamKeys) {
  return (pull.requested_teams || []).filter((team) => {
    const organization = team.organization?.login || team.organization?.name;
    return organization && team.slug && teamKeys.has(`${organization}/${team.slug}`);
  });
}

export function computeReviewDecision(reviews, authorLogin) {
  const latestByReviewer = new Map();
  const ordered = [...reviews].sort((a, b) =>
    (a.submitted_at || a.created_at || '').localeCompare(b.submitted_at || b.created_at || ''));
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
    return { decision: 'CHANGES_REQUESTED', decisiveAt: changes.map((entry) => entry.timestamp).sort().at(-1) || null };
  }
  const approvals = entries.filter((entry) => entry.state === 'APPROVED');
  if (approvals.length) {
    return { decision: 'APPROVED', decisiveAt: approvals.map((entry) => entry.timestamp).sort().at(-1) || null };
  }
  return { decision: 'REVIEW_REQUIRED', decisiveAt: null };
}

export function flattenPages(pages, arrayField = null) {
  return pages.flatMap((page) => {
    if (Array.isArray(page)) return page;
    if (arrayField && Array.isArray(page?.[arrayField])) return page[arrayField];
    return [];
  });
}

export function latestExternalMessagesByScope(rows, authorLogin) {
  const latest = new Map();
  for (const row of [...rows].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))) {
    if (row.replyEligible !== false && row.scope && row.login && row.login !== authorLogin && stripNoise(row.body)) {
      latest.set(row.scope, row);
    }
  }
  return [...latest.values()];
}

export function latestAuthorResponseAfter(rows, authorLogin, timestamp, scope = null) {
  if (!timestamp) return null;
  return [...rows]
    .filter((row) => row.replyEligible !== false && row.login === authorLogin)
    .filter((row) => !scope || row.scope === scope)
    .filter((row) => new Date(row.timestamp) > new Date(timestamp))
    .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))[0] || null;
}

export function computeReplyEvidence(rows, authorLogin, afterTimestamp = null) {
  const actionable = latestExternalMessagesByScope(rows, authorLogin)
    .filter((row) => isActionableText(row.body))
    .filter((row) => !afterTimestamp || new Date(row.timestamp) > new Date(afterTimestamp));
  const outstanding = [];
  const responded = [];
  for (const row of actionable) {
    const response = latestAuthorResponseAfter(rows, authorLogin, row.timestamp, row.scope);
    const target = response ? responded : outstanding;
    target.push({
      scope: row.scope,
      login: row.login,
      timestamp: row.timestamp,
      id: row.id || null,
      responseAt: response?.timestamp || null,
    });
  }
  return { outstanding, responded };
}

export function triageConfigPath(env = process.env) {
  return join(env.XDG_CONFIG_HOME || join(env.HOME || homedir(), '.config'), 'tigerkit', 'pr-triage.json');
}

function configuredRepositories(value, path) {
  if (!Array.isArray(value?.repositories)
      || !value.repositories.length
      || value.repositories.some((repo) => typeof repo !== 'string' || !/^[^/\s]+\/[^/\s]+$/.test(repo))) {
    throw new Error(`Invalid triage config ${path}: repositories must be a non-empty owner/name array`);
  }
  return [...new Set(value.repositories)];
}

export function loadOrBootstrapConfig(path, fallbackRepositories = []) {
  try {
    return { repositories: configuredRepositories(JSON.parse(readFileSync(path, 'utf8')), path), bootstrapped: false };
  } catch (error) {
    if (error.code !== 'ENOENT') {
      if (error instanceof SyntaxError) throw new Error(`Invalid JSON in triage config ${path}: ${error.message}`);
      throw error;
    }
  }
  if (!fallbackRepositories.length) {
    throw new Error(`Cannot bootstrap triage config ${path}: supply --repo owner/name or run from a checkout with origin`);
  }
  const repositories = configuredRepositories({ repositories: fallbackRepositories }, path);
  mkdirSync(dirname(path), { recursive: true });
  try {
    writeFileSync(path, `${JSON.stringify({ repositories }, null, 2)}\n`, { encoding: 'utf8', flag: 'wx' });
  } catch (error) {
    if (error.code === 'EEXIST') return loadOrBootstrapConfig(path, fallbackRepositories);
    throw error;
  }
  return { repositories, bootstrapped: true };
}

export function classifyPullRequest({
  draft,
  conflict,
  checksFailed,
  checksUnverifiable,
  decision,
  authorRespondedToChangeRequest,
  latestExternalActionable,
  authorRespondedToLatestExternal,
}) {
  if (checksUnverifiable) return 'checks_unverifiable';
  if (conflict) return 'merge_conflict';
  if (checksFailed) return 'checks_failed';
  if (latestExternalActionable && !authorRespondedToLatestExternal) return 'needs_reply';
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
    return { ok: true, stdout: execFileSync(command, args, { encoding: 'utf8', maxBuffer: 32 * 1024 * 1024, stdio: ['ignore', 'pipe', 'pipe'] }).trim() };
  } catch (error) {
    const detail = String(error.stderr || error.message || '').trim();
    if (allowFailure) return { ok: false, error: detail };
    throw new Error(detail);
  }
}

function ghObject(path) {
  const result = run('gh', ['api', path], { allowFailure: true });
  if (!result.ok) return result;
  try { return { ok: true, data: JSON.parse(result.stdout) }; } catch (error) {
    return { ok: false, error: `Invalid JSON from ${path}: ${error.message}` };
  }
}

function ghList(path, arrayField = null) {
  const result = run('gh', ['api', path, '--paginate', '--slurp'], { allowFailure: true });
  if (!result.ok) return result;
  try { return { ok: true, data: flattenPages(JSON.parse(result.stdout || '[]'), arrayField) }; } catch (error) {
    return { ok: false, error: `Invalid paginated JSON from ${path}: ${error.message}` };
  }
}

export function checkProvider(check = {}) {
  const slug = String(check.app?.slug || '').toLowerCase();
  const name = String(check.app?.name || '').toLowerCase();
  if (!slug && !name) return 'unknown';
  return slug === 'github-actions' || /github\s*actions/.test(name) ? 'github-actions' : 'external';
}

function currentRepository() {
  const remote = run('git', ['remote', 'get-url', 'origin'], { allowFailure: true });
  return remote.ok ? parseRepoFromRemote(remote.stdout) : null;
}

function collectRows(reviews, inlineComments, issueComments) {
  return [
    ...reviews.map((review) => ({ login: review.user?.login, timestamp: review.submitted_at || review.created_at, body: review.body || '', kind: 'review', state: review.state, replyEligible: false })),
    ...inlineComments.map((comment) => ({ login: comment.user?.login, timestamp: comment.created_at, body: comment.body || '', kind: 'inline_comment', id: comment.id, scope: `inline:${comment.in_reply_to_id || comment.id}` })),
    ...issueComments.map((comment) => ({ login: comment.user?.login, timestamp: comment.created_at, body: comment.body || '', kind: 'issue_comment', id: comment.id, scope: 'issue' })),
  ].filter((row) => row.timestamp);
}

function checkState(repo, sha) {
  const checkRuns = ghList(`repos/${repo}/commits/${sha}/check-runs?per_page=100`, 'check_runs');
  const combined = ghObject(`repos/${repo}/commits/${sha}/status`);
  const failures = [];
  if (checkRuns.ok) {
    for (const check of checkRuns.data) {
      if (check.status === 'completed' && !SUCCESS_CONCLUSIONS.has(check.conclusion)) {
        failures.push({
          kind: 'check_run',
          name: check.name,
          state: check.conclusion,
          provider: checkProvider(check),
          app: check.app?.slug || check.app?.name || null,
        });
      }
    }
  }
  if (combined.ok && ['failure', 'error'].includes(combined.data.state)) {
    for (const status of combined.data.statuses || []) {
      if (['failure', 'error'].includes(status.state)) {
        failures.push({ kind: 'status', name: status.context, state: status.state, provider: 'unknown' });
      }
    }
  }
  return {
    failures,
    errors: [checkRuns, combined].filter((result) => !result.ok).map((result) => result.error),
  };
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

async function triageRepository(repo, login, teamKeys) {
  const openPulls = ghList(`repos/${repo}/pulls?state=open&per_page=100`);
  if (!openPulls.ok) return { repository: repo, items: [], failures: [openPulls.error] };
  const items = [];
  const failures = [];
  for (const pull of openPulls.data) {
    const requested = (pull.requested_reviewers || []).some((reviewer) => reviewer.login === login);
    const requestedTeams = requestedTeamForUser(pull, teamKeys);
    if (pull.user?.login !== login) {
      if (requested || requestedTeams.length) {
        items.push(pullItem(repo, pull, 'review_requested', {
          requestedReviewer: requested ? login : null,
          requestedTeams: requestedTeams.map((team) => `${team.organization?.login || team.organization?.name}/${team.slug}`),
        }));
      }
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
      failures.push(`#${pull.number}: ${required.filter((result) => !result.ok).map((result) => result.error).join('; ')}`);
      continue;
    }
    if (detail.data.mergeable === null || detail.data.mergeable_state === 'unknown') {
      failures.push(`#${pull.number}: mergeability remained unknown after retry`);
      continue;
    }
    const rows = collectRows(reviews.data, inlineComments.data, issueComments.data);
    const review = computeReviewDecision(reviews.data, login);
    const reply = computeReplyEvidence(
      rows,
      login,
      review.decision === 'APPROVED' ? review.decisiveAt : null,
    );
    const check = checkState(repo, pull.head.sha);
    const changeResponse = review.decisiveAt
      && reply.responded.some((item) => item.responseAt && new Date(item.responseAt) > new Date(review.decisiveAt));
    const category = classifyPullRequest({
      draft: pull.draft,
      conflict: detail.data.mergeable_state === 'dirty',
      checksFailed: check.failures.length > 0,
      checksUnverifiable: check.errors.length > 0,
      decision: review.decision,
      authorRespondedToChangeRequest: Boolean(changeResponse),
      latestExternalActionable: reply.outstanding.length > 0 || reply.responded.length > 0,
      authorRespondedToLatestExternal: reply.outstanding.length === 0 && reply.responded.length > 0,
    });
    failures.push(...check.errors.map((error) => `#${pull.number}: ${error}`));
    if (!['approved', 'pending_review'].includes(category)) {
      items.push(pullItem(repo, pull, category, {
        reviewDecision: review.decision,
        decisiveAt: review.decisiveAt,
        replyEvidence: reply,
        failedChecks: check.failures,
        checkErrors: check.errors,
        mergeableState: detail.data.mergeable_state,
      }));
    }
  }
  return { repository: repo, items, failures };
}

function parseArgs(argv) {
  const repos = [];
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === '--repo') {
      if (!argv[index + 1]) throw new Error('--repo requires owner/name');
      repos.push(argv[index + 1]);
      index += 1;
    } else if (argv[index] === '--help' || argv[index] === '-h') return { help: true, repos: [] };
    else throw new Error(`Unknown argument: ${argv[index]}`);
  }
  return { help: false, repos };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { console.log('Usage: node triage.mjs [--repo owner/name]...'); return; }
  const user = ghObject('user');
  if (!user.ok) throw new Error(`Unable to resolve GitHub identity: ${user.error}`);
  const userTeams = ghList('user/teams?per_page=100');
  const teamKeys = userTeams.ok ? teamKeysForUser(userTeams.data) : new Set();
  const configPath = args.repos.length ? null : triageConfigPath();
  const target = args.repos.length
    ? { repositories: configuredRepositories({ repositories: args.repos }, 'arguments'), bootstrapped: false }
    : loadOrBootstrapConfig(configPath, [currentRepository()].filter(Boolean));
  const repos = target.repositories;
  const results = [];
  for (const repo of [...new Set(repos)]) results.push(await triageRepository(repo, user.data.login, teamKeys));
  const items = results.flatMap((result) => result.items);
  const failures = results.flatMap((result) => result.failures.map((error) => ({ repository: result.repository, error })));
  if (!userTeams.ok) failures.unshift({ repository: null, error: `Unable to resolve team review membership: ${userTeams.error}` });
  const counts = items.reduce((accumulator, item) => { accumulator[item.category] = (accumulator[item.category] || 0) + 1; return accumulator; }, {});
  console.log(JSON.stringify({
    generatedAt: new Date().toISOString(),
    login: user.data.login,
    config: { path: configPath, source: configPath ? 'config' : 'arguments', bootstrapped: target.bootstrapped },
    repositories: repos,
    counts,
    items,
    failures,
  }, null, 2));
}

function isDirectRun() {
  try { return realpathSync(process.argv[1]) === realpathSync(fileURLToPath(import.meta.url)); } catch { return false; }
}

if (isDirectRun()) main().catch((error) => { console.error(error.message); process.exitCode = 1; });
