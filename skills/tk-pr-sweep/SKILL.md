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

Start only via `/tk-pr-sweep`, `$tk-pr-sweep`, or host skill picker. Never
activate for generic PR cleanup, triage, response, rebase, CI, release,
continuation, or multi-repository requests.

Explicit multi-PR maintenance orchestrator only. `tk-drive` owns product-change
lifecycle. `tk-pr-triage` stays read-only; one-PR owners `tk-pr-rebase` and
`tk-pr-respond` never invoke each other. Sweep owns `.tigerkit/pr-sweep.md`,
worktree coordination, route bounds, one shared PR-summary budget, aggregate
verification, and sole terminal response.

## Authority

One explicit start authorizes fresh configured-repository triage and, per fresh
supported target: bounded local implementation/commits; exact branch push;
verified force-with-lease; replies; verified thread resolution; conditional
human re-review; maximum one PR summary. Never authorizes external CI or
unverifiable-check repair, PR creation, merge, close, tag, release, general
publication, history rewrite outside exact rebase lease,
draft-to-`Ready for review` transition, or out-of-scope product work.

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

Never infer provider, category, thread state, or transition from child receipt.
Reclassify from GitHub evidence.

## Workflow

1. Fresh full `tk-pr-triage`: resolve authenticated identity and configured
   repositories. Reject supplied/cached queues. Freeze supported items in triage
   priority/repository/PR order; record report-only items.
2. Before each queued PR, re-read repository identity, author/open/draft state,
   base and head refs and SHAs, category/provider evidence, reviews, comments, threads,
   and checks. Reroute stale entries. Stop mutation on author/login, fork
   destination, or ownership ambiguity. Preserve draft; never mark
   `Ready for review`.
3. Fetch exact remote PR head into sweep-owned deterministic local ref; prove
   SHA. Reuse only clean worktree matching remote repository, PR, head ref, and
   `HEAD`. Otherwise prefer current-schema `orca worktree list --json` and
   `orca worktree create --json`, rooted at fetched head—not coincidental local
   branch. Use direct Git only when Orca unavailable or repository unregistered.
   Before mutation, verify worktree `HEAD` and exact push refspec target observed
   head repository/ref; ambiguity stops PR. Record fetched ref/SHA, worktree
   owner/path, push refspec, fallback.
4. Per new worktree, run repository-owned lockfile-enforcing setup once. If none
   documented, use lockfile package manager frozen/immutable mode. Share package
   cache only; never symlink `node_modules` or another checkout's dependency tree.
5. Invoke exactly one closed-router owner. Child `Pass` is internal: render sweep
   checkpoint; re-triage exact PR/head without terminal response or pause; follow
   new supported category only within bound. Record child non-success; no sibling
   call for same failed state.
6. Keep prompt-local bounds: one rebase per exact `(base_sha, head_sha)`, maximum
   three GitHub Actions corrective cycles, one feedback response per fresh head
   SHA. Allow at most two additional feedback cycles when sweep-owned pushes
   create heads. Repeated unchanged feedback or third additional head becomes
   `follow-up-queued` without mutation. Never create durable cursor, scheduler,
   retry queue, or shared state framework.
7. For post-push `IN_PROGRESS`, perform at most three fresh rechecks. If still
   incomplete: record `waiting`, retain worktree, continue frozen queue without
   mutation. Repeated unchanged failure or exhausted mutation bound stops PR.
8. After PR-local `Pass`, `follow-up-queued`, `waiting`, `Fail`, `Blocked`, or
   `Unverifiable`, record result and remaining count; immediately advance to next
   frozen entry without child receipt, terminal response, pause, or confirmation.
   Freeze later mutation only on shared safety failure: unresolved identity,
   corrupt repository evidence, or unprovable repository/worktree ownership.
9. One summary budget per PR. Accept rebase `summary budget: unused`; let later
   response combine outcomes, else publish one rebase-only summary after final
   fresh PR read. Never publish second PR summary. Every generated
   reply/comment ends exactly `_🤖 본 코멘트는 AI가 작성했습니다._`.
10. Remove only sweep-created clean worktree whose complete route is freshly
    `Pass`; prefer matching Orca removal. Retain and report `follow-up-queued`, `waiting`,
    dirty, failed, blocked, unverifiable, ambiguous, or reused worktrees.
11. After accounting for all initial targets, run new full triage without growing
    unbounded queue. Processed PR whose sweep-owned new head exhausted
    feedback cycles is `follow-up-queued`; any other final-only supported
    `Act now` item is `Blocked`; either prevents batch `Pass`. Write
    `.tigerkit/pr-sweep.md` with evidence times, exact routes, child states,
    consumed bounds, summary budget, worktree owner/disposition, setup command
    class, report-only items, systemic stop, and all final items. Store no
    credentials or resume cursor.

## Progress

After queue freeze, before and after each PR route/check, and around final triage,
emit compact `▶️ Progress`: decision, decisive evidence, result/next action,
remaining count. Continue within sweep authority. Children return evidence
internally. Never expose child receipts, raw reasoning, command logs, timer
promises, approval requests, or nonterminal `Status:` lines.

Use `✅ Pass`, `⏳ Waiting`, `⚠️ Advisory`, `❌ Fail`, `⛔ Blocked`, and
`❓ Unverifiable` for matching outcomes. Render `follow-up-queued` and `waiting`
as `⏳ Waiting`; preserve terminal `Status: <token>` exactly.

## Aggregate result

`Pass` requires every supported target from initial, per-PR, or final router pass.
`follow-up-queued` and `waiting` aggregate to `Pending`, never `Blocked` or
`Fail`. Otherwise aggregate supported results:
`Fail > Blocked > Unverifiable > Pending > Pass`; preserve shared systemic
status that froze later mutation. Keep external CI, `checks_unverifiable`, and
unsupported final items conspicuous; they are not supported successes and alone
do not change otherwise empty/successful batch from `Pass`.

Lead `## PR sweep`. Show processed results, report-only external CI and
`checks_unverifiable`, retained worktrees, all remaining final-triage items. For
eight+ rows, show top five to seven and cite `.tigerkit/pr-sweep.md`. Keep exact
child provenance in artifacts, not terminal response. Lead aggregate result with
mapped visible marker, including `✅ Pass` for full pass, without replacing exact
final status line.

### 🔴 HARD GATE · terminal user summary

Begin only terminal response with `## PR sweep`. No child receipts,
phase-success output, `Outcome:`, caller-return instructions, or bottom metadata
block. End aggregate result section exactly `Status: <token>`.

### 🔴 HARD GATE · response language

Use latest explicit user language for free-form user-facing prose. Keep
headings, statuses, IDs, paths, commands, refs, categories, and exact source
literals stable.

## User decision questions

No routine selection or publication questions. If new material identity, ownership,
or out-of-scope authority decision is required, ask one self-contained `Question`
before any `Recommendation`; stop `Pending | Blocked`. Never infer or broaden
sweep.
