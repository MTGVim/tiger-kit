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
or out-of-scope product work.

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

1. Resolve the authenticated identity and configured repository set through a
   fresh full `tk-pr-triage` run. Do not execute a supplied PR list, cached output,
   or previous conversation snapshot. Freeze the initial supported queue in
   triage priority/repository/PR order and record report-only items.
2. Before each queued PR, re-read repository identity, PR author/open state,
   base/head refs and SHAs, category/provider evidence, and current reviews,
   comments, threads, and checks. Skip stale queue entries into the fresh router;
   stop mutation on author/login, fork destination, or ownership ambiguity.
3. Reuse a clean worktree only when its remote repository, PR, head ref, and head
   SHA match exactly. Otherwise prefer `orca worktree list --json` and
   `orca worktree create --json` using the current machine schema. Use direct
   `git worktree` only when Orca is unavailable or the repository is unregistered,
   and record which fallback and exact path were used.
4. Invoke exactly one owner from the closed router. A child `Pass` is an internal
   signal: re-triage that exact PR/head without a terminal response, then follow a
   new supported category only while its bound remains. A child non-success is
   recorded and does not authorize a sibling call for that same failed state.
5. Keep prompt-local route evidence only: one rebase per exact
   `(base_sha, head_sha)`, at most three GitHub Actions corrective cycles, and one
   feedback response per fresh head SHA. Repeated unchanged failure or an
   exhausted bound stops that PR without another mutation. Do not create a
   durable cursor, scheduler, retry queue, or shared state framework.
6. Continue after PR-local `Fail`, `Blocked`, or `Unverifiable`. Freeze all
   remaining mutation only for a shared safety failure such as unresolved
   authenticated identity, corrupt configured-repository evidence, or inability
   to prove repository/worktree ownership.
7. Track one summary budget per PR. Accept `summary budget: unused` from rebase;
   let a later response publish the combined rebase/CI summary, otherwise publish
   one rebase-only summary after the final fresh PR read. Never publish a second
   PR-level summary. Every generated GitHub reply or comment ends exactly with
   `_🤖 본 코멘트는 AI가 작성했습니다._`.
8. Remove only a sweep-created, clean worktree for a PR whose complete route
   passed. Prefer the matching Orca removal command for Orca-created worktrees;
   otherwise use direct Git. Retain and report dirty, failed, blocked,
   unverifiable, ambiguous, or reused worktrees.
9. After every initial target is accounted for, run a new full `tk-pr-triage`.
   Do not grow a new unbounded queue from that snapshot. Any newly observed
   supported `Act now` item remains unprocessed, is recorded as `Blocked`, and
   prevents batch `Pass`.
   Write `.tigerkit/pr-sweep.md` with initial/final evidence times, exact PR/head
   routes, child native states, consumed bounds, summary budget, worktree owner and
   disposition, report-only items, systemic stop if any, and every remaining
   final-triage item. Do not store credentials or a resume cursor.

## Aggregate result

`Pass` requires every supported target encountered by the initial, per-PR, or
final router to pass; a final-only supported item is `Blocked`. Otherwise
aggregate supported results as
`Fail > Blocked > Unverifiable > Pass`; a shared systemic status freezes later
mutation and is preserved. External CI, `checks_unverifiable`, and unsupported
final items remain conspicuous but do not become supported successes or by
themselves change an otherwise empty/successful batch from `Pass`.

Lead with `## PR sweep`. Show processed PR results, report-only external CI and
`checks_unverifiable`, retained worktrees, and all remaining final-triage items.
For eight or more rows, show the top five to seven and cite
`.tigerkit/pr-sweep.md`. Keep exact child provenance in owned artifacts, not in
the terminal response.

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
