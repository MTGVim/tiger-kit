---
name: tk-pr-sweep
description: "[user] Process supported PR-maintenance items across configured repositories with fresh triage, bounded one-PR handlers, and aggregate verification."
argument-hint: "[configured repositories]"
disable-model-invocation: true
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Sweep pull requests

Start only when the user selects `/tk-pr-sweep`, `$tk-pr-sweep`, or the host
skill picker. Do not activate from generic PR cleanup, triage, response, rebase,
CI, release, continuation, or multi-repository requests.

This is the explicit orchestrator for multi-PR maintenance only. `tk-drive`
remains the product-change lifecycle orchestrator. `tk-pr-triage` remains
read-only; `tk-pr-rebase` and `tk-pr-respond` remain one-PR owners and never
invoke each other. The sweep owns `.tigerkit/pr-sweep.md`, worktree coordination,
route bounds, one shared PR-summary budget, aggregate verification, and the only
terminal response.

## Authority

One explicit start authorizes fresh configured-repository triage and, for each
fresh supported target, bounded local implementation/commits, exact branch push,
verified force-with-lease, replies, verified thread resolution, conditional
human re-review, and at most one PR-level summary comment. It does not authorize
external CI repair, unverifiable-check repair, PR creation, merge, close, tag,
release, general publication, history rewriting outside the exact rebase lease,
draft-to-`Ready for review` transitions, or out-of-scope product work.

## Closed router

| Fresh category | Evidence | Route |
| --- | --- | --- |
| `merge_conflict` | exact base/head pair | `tk-pr-rebase --ci` |
| `checks_failed` | every selected failure is GitHub Actions | `tk-pr-respond --ci` |
| `changes_requested` | fresh actionable findings | `tk-pr-respond --ci` |
| `needs_reply` | fresh actionable findings | `tk-pr-respond --ci` |
| external-only `checks_failed` | provider evidence | report-only |
| `checks_unverifiable` | failed/incomplete evidence | report-only |
| any other category | fresh triage item | final report only |

Never infer a provider, category, thread state, or transition from a child
receipt. Reclassify from GitHub evidence.

## Workflow

1. Resolve authenticated identity and configured repositories through a fresh full `tk-pr-triage`. Never execute a supplied/cached queue; freeze supported items in triage priority/repository/PR order and record report-only items.
2. Before each queued PR, re-read repository identity, author/open/draft state, base/head refs and SHAs, category/provider evidence, reviews, comments, threads, and checks. Route stale entries afresh; stop mutation on author/login, fork destination, or ownership ambiguity. A draft stays report-only; never mark it `Ready for review`.
3. Fetch the exact remote PR head into a sweep-owned deterministic local ref and prove its SHA. Reuse only a clean worktree whose remote repository, PR, head ref, and `HEAD` match. Otherwise prefer current-schema `orca worktree list --json` and `orca worktree create --json`, rooted at the fetched head rather than a coincidental local branch; use direct Git only when Orca is unavailable or the repository is unregistered. Before mutation, verify worktree `HEAD` and the exact push refspec target the observed head repository/ref; ambiguity stops that PR. Record fetched ref/SHA, worktree owner/path, push refspec, and fallback.
4. In each new worktree, run once the repository-owned setup that enforces its lockfile; if none is documented, use the lockfile package manager in frozen/immutable mode. Share only the package cache; never symlink `node_modules` or another checkout's dependency tree.
5. Invoke exactly one closed-router owner. A child `Pass` is internal: render the sweep checkpoint, re-triage that exact PR/head without a terminal response or pause, then follow a new supported category only within its bound. Record child non-success without a sibling call for the same failed state.
6. Keep prompt-local bounds: one rebase per exact `(base_sha, head_sha)`, at most three GitHub Actions corrective cycles, and one feedback response per fresh head SHA. Process at most two additional feedback cycles when sweep-owned pushes create new heads; repeated unchanged feedback or a third additional head becomes `follow-up-queued` without mutation. Never create a durable cursor, scheduler, retry queue, or shared state framework.
7. For post-push `IN_PROGRESS`, perform at most three fresh rechecks. If still incomplete, record `waiting`, retain the worktree, and continue the frozen queue without mutation. Repeated unchanged failure or another exhausted mutation bound stops that PR.
8. After PR-local `Pass`, `follow-up-queued`, `waiting`, `Fail`, `Blocked`, or `Unverifiable`, record result and remaining count, then immediately advance to the next frozen entry without child receipt, terminal response, pause, or confirmation. Freeze all later mutation only for shared safety failure such as unresolved identity, corrupt repository evidence, or unprovable repository/worktree ownership.
9. Keep one summary budget per PR. Accept rebase `summary budget: unused`; let a later response combine outcomes, otherwise publish one rebase-only summary after the final fresh PR read. Never publish a second PR summary. Every generated reply/comment ends exactly `_🤖 본 코멘트는 AI가 작성했습니다._`.
10. Remove only a sweep-created clean worktree whose complete route is freshly `Pass`, preferring its matching Orca removal; retain and report `follow-up-queued`, `waiting`, dirty, failed, blocked, unverifiable, ambiguous, or reused worktrees.
11. After every initial target is accounted for, run new full triage without growing an unbounded queue. A processed PR whose sweep-owned new head exhausted feedback cycles is `follow-up-queued`; any other final-only supported `Act now` item is `Blocked`; both prevent batch `Pass`. Write `.tigerkit/pr-sweep.md` with evidence times, exact routes, child states, consumed bounds, summary budget, worktree owner/disposition, setup command class, report-only items, systemic stop, and all final items. Store no credentials or resume cursor.

## Progress commentary

The sweep owns the unified progress surface. At meaningful boundaries, render one compact checkpoint beginning `▶️ Progress` with `Decision`, `Evidence`, and `Result/Next` semantics: after freezing the initial queue; before each PR route; after every child mutation or bounded check cycle; when closing a PR with its remaining count; and before and after final triage. Use only the decisive fresh GitHub/repository evidence and active route bound. Mention a rejected route only when evidence made it materially competitive.

These checkpoints are nonterminal commentary and never consume the one terminal response. A child invoked by the sweep returns its decision, evidence, result, and next action internally; it does not render duplicate progress, a receipt, or a status. Within existing sweep authority, render the checkpoint and continue immediately. Before a long blocking check or verification, state what is starting and the next decision condition, then report its result immediately afterward. Do not promise timer heartbeats or expose raw chain-of-thought or command-by-command logs.

Make outcomes scannable without replacing canonical status tokens: use
`✅ Pass`, `⏳ Waiting`, `⚠️ Advisory`, `❌ Fail`, `⛔ Blocked`, and
`❓ Unverifiable` for the corresponding PR-local, checkpoint, or aggregate
outcome. Always pair the emoji with that exact text; never emit an emoji-only
state. Render `follow-up-queued` and `waiting` with `⏳ Waiting`. Preserve the
required terminal `Status: <token>` line unchanged.

## Aggregate result

`Pass` requires every supported target encountered by the initial, per-PR, or
final router to pass. `follow-up-queued` and `waiting` aggregate to `Pending`,
not `Blocked` or `Fail`. Otherwise aggregate supported results as
`Fail > Blocked > Unverifiable > Pending > Pass`; a shared systemic status
freezes later mutation and is preserved. External CI, `checks_unverifiable`, and
unsupported final items remain conspicuous but do not become supported successes
or by themselves change an otherwise empty/successful batch from `Pass`.

Lead with `## PR sweep`. Show processed PR results, report-only external CI and
`checks_unverifiable`, retained worktrees, and all remaining final-triage items.
For eight or more rows, show the top five to seven and cite
`.tigerkit/pr-sweep.md`. Keep exact child provenance in owned artifacts, not in
the terminal response. Lead the aggregate result itself with its mapped visible
marker, including `✅ Pass` for a full pass, without replacing the exact final
status line.

### 🔴 HARD GATE · terminal user summary

Begin the only terminal response with `## PR sweep`. Do not emit child receipts,
phase-success output, `Outcome:`, caller-return instructions, or a bottom metadata
block. End the aggregate result section with exactly `Status: <token>`.

### 🔴 HARD GATE · response language

Use the latest explicit user language for all free-form user-facing prose. Keep
headings, statuses, IDs, paths, commands, refs, categories, and exact source
literals stable.

## User decision questions

This workflow asks no routine selection or publication questions. If a new
material identity, ownership, or out-of-scope authority decision is required,
ask one self-contained `Question` before any `Recommendation` and stop
`Pending | Blocked`; do not infer or broaden the sweep.
