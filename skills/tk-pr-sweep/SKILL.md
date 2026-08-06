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

Start only via `/tk-pr-sweep`, `$tk-pr-sweep`, or host skill picker. A same-
conversation re-invocation after preview, child route, or system wait resumes
only after fresh triage revalidates the approved repository/PR/head/category/
route. Never activate for generic PR cleanup, triage, response, rebase, CI,
release, continuation, or multi-repository requests.

Explicit multi-PR maintenance orchestrator only. `tk-drive` owns product-change
lifecycle. `tk-pr-triage` stays read-only; one-PR owners `tk-pr-rebase` and
`tk-pr-respond` never invoke each other. Sweep owns the preflight preview,
one batch approval, `.tigerkit/pr-sweep.md`, worktree coordination, route
bounds, one shared PR-summary budget, aggregate verification, and sole
terminal response.

Re-invocation grants no new approval and trusts no cursor, child receipt, or
stale artifact: run fresh full `tk-pr-triage`, match the exact approval/head,
and continue only for unchanged rows. Drift or no match emits
`❓ sweep > preflight · 승인 필요` and stops before mutation; an unfinished CI
wait gets a bounded fresh recheck, not a blind child restart.

## Authority

One explicit start authorizes fresh configured-repository triage and a
read-only preview. A second current-turn approval authorizes only the rows
shown as low-risk and `auto` in that preview: bounded local
implementation/commits; exact branch push; replies; verified thread
resolution; conditional human re-review; and at most one PR summary. It never
silently broadens to a new PR, head, category, or high-risk action. External CI
or unverifiable-check repair, PR creation, merge, close, tag, release, general
publication, history rewrite outside exact rebase lease,
draft-to-`Ready for review` transition, and out-of-scope product work remain
unauthorized. An exact high-risk PR/route needs a new explicit selection and
preview.

## Preflight preview

Before any worktree creation, local commit, push, reply, or thread resolution,
run fresh full `tk-pr-triage` and render `## PR sweep preview` with a table for
every initial item: repository, PR number, title, link, observed head SHA,
fresh category, planned action, risk, and decisive evidence. Include report-only
and held items. State `No remote changes yet`. If there are `auto` rows, emit
`❓ sweep > preflight · 승인 필요` and stop with `Status: Pending` until the
user explicitly approves them. If there are no
`auto` rows, complete the report-only run without an approval. Never replace
this gate with a timer or automatic continuation; do not ask for approval once
per PR.

### Risk gate

Mark a row `auto` only when the requested change is test-only: test files or
test cases may change, but production source, configuration, dependencies,
lockfiles, security/data/performance behavior, or weakened assertions may not.
This means paths in the repository's existing test layout (`test/`, `tests/`,
`spec/`, `*.test.*`, `*.spec.*`, or documented test fixtures) only; mixed,
unknown, or helper/config paths are not `auto`. The child must stop before
commit if its planned or staged paths leave that scope. A test-only change still
needs repository tests to pass.

Mark bug fixes, behavior changes, merge-conflict resolution, CI corrective
changes, security/data/performance work, ambiguous scope or requests, and
ownership or provider uncertainty `hold` or `report-only` by default. A user
may explicitly select one or more named held rows in a later preview; generic
batch approval never selects them. That later preview must name every exact PR,
observed head, and route; a current-turn approval of that exact high-risk set
may then authorize the existing closed router for those rows only. It is a
separate approval, not a broadening of the low-risk batch.

## Closed router

| Fresh category | Evidence | Route |
| --- | --- | --- |
| `merge_conflict` | exact base/head pair | `tk-pr-rebase --ci` |
| `checks_failed` | every selected failure is GitHub Actions | `tk-pr-respond --ci` |
| `checks_failed` | any selected failure is external or provider `unknown` | report-only |
| `changes_requested` | fresh actionable findings | `tk-pr-respond --ci` |
| `needs_reply` | fresh actionable findings | `tk-pr-respond --ci` |
| external-only `checks_failed` | provider evidence | report-only |
| `checks_unverifiable` | failed/incomplete evidence | report-only |
| any other category | fresh triage item | final report only |

Never infer provider, category, thread state, or transition from child receipt.
Reclassify from GitHub evidence.

## Workflow

1. Run fresh full `tk-pr-triage`: resolve authenticated identity and configured
   repositories. Reject supplied/cached queues; build the preview in triage
   priority/repository/PR order and record report-only and held items.
2. Stop at the preflight checkpoint until the user approves the displayed
   low-risk rows. Freeze only those approved rows. A later exact high-risk
   selection creates a new preview; never infer it from a generic continuation.
3. Before each approved PR, re-read repository identity, author/open/draft
   state, base and head refs and SHAs, category/provider evidence, reviews,
   comments, threads, and checks. If the head or evidence drifted from the
   preview, reclassify before mutation; external drift invalidates that row and
   holds it. A sweep-owned new head may continue only within its declared bound.
   Stop mutation on author/login, fork destination, or ownership ambiguity.
   Preserve draft; never mark `Ready for review`.
4. Before creating a worktree, compare fresh GitHub evidence with the approved
   finding. If the finding is resolved and any requested code/test change is
   proven present on the observed head by current diff, commit, or test
   evidence, or if fresh triage explicitly marks it reply-only with no
   code/test obligation and its exact reply/thread is current and complete,
   record `Skipped: already applied` and do not invoke a child or create a
   worktree. Never use a complete reply to skip a code/test finding. If
   evidence is ambiguous, hold; do not guess from a local report or ledger.
5. Fetch exact remote PR head into sweep-owned deterministic local ref; prove
   SHA. Reuse only clean worktree matching remote repository, PR, head ref, and
   `HEAD`. Otherwise prefer current-schema `orca worktree list --json` and
   `orca worktree create --json`, rooted at fetched head—not coincidental local
   branch. Use direct Git only when Orca unavailable or repository unregistered.
   Before mutation, verify worktree `HEAD` and exact push refspec target observed
   head repository/ref; ambiguity stops PR. Record fetched ref/SHA, worktree
   owner/path, push refspec, fallback.
6. Per new worktree, run repository-owned lockfile-enforcing setup once. If none
   documented, use lockfile package manager frozen/immutable mode. Share package
   cache only; never symlink `node_modules` or another checkout's dependency tree.
7. Invoke exactly one closed-router owner. Pass only exact PR/head, route,
   bounded finding scope, and artifact paths; do not repeat the full triage
   table or child receipt. For an `auto` row, pass the `test-only` scope and
   stop before commit if the child would leave it. Child `Pass` is internal:
   render sweep checkpoint; re-triage exact PR/head without
   terminal response or pause; follow a new supported category only within
   bound. Record child non-success; no sibling call for the same failed state.
8. Keep prompt-local bounds: one rebase per exact `(base_sha, head_sha)`, maximum
   three GitHub Actions corrective cycles, one feedback response per fresh head
   SHA. Allow at most two additional feedback cycles when sweep-owned pushes
   create heads. Repeated unchanged feedback or third additional head becomes
   `follow-up-queued` without mutation. Never create durable cursor, scheduler,
   retry queue, or shared state framework.
9. For post-push `IN_PROGRESS`, perform at most three fresh rechecks. If still
   incomplete: record `waiting`, retain worktree, continue frozen queue without
   mutation. Repeated unchanged failure or exhausted mutation bound stops PR.
10. After PR-local `Pass`, `Skipped: already applied`, `follow-up-queued`,
    `waiting`, `Fail`, `Blocked`, or `Unverifiable`, record result and remaining
    count; immediately advance to the next frozen entry without child receipt,
    terminal response, pause, or confirmation. Freeze later mutation only on
    shared safety failure: unresolved identity, corrupt repository evidence, or
    unprovable repository/worktree ownership.
11. One summary budget per PR. Accept rebase `summary budget: unused`; let later
    response combine outcomes, else publish one rebase-only summary after final
    fresh PR read. Never publish a second PR summary. Every generated
    reply/comment ends exactly `_🤖 본 코멘트는 AI가 작성했습니다._`.
12. Remove only sweep-created clean worktree whose complete route is freshly
    `Pass`; prefer matching Orca removal. Retain and report `follow-up-queued`,
    `waiting`, dirty, failed, blocked, unverifiable, ambiguous, or reused
    worktrees.
13. After accounting for all initial targets, run new full triage without growing
    an unbounded queue. A processed PR whose sweep-owned new head exhausted
    feedback cycles is `follow-up-queued`; any other final-only supported
    `Act now` item is `Blocked`; either prevents batch `Pass`. Write
    `.tigerkit/pr-sweep.md` with evidence times, exact routes, child states,
    consumed bounds, summary budget, worktree owner/disposition, setup command
    class, report-only items, systemic stop, and all final items. Store no
    credentials or resume cursor.

## Progress

After preview approval, at meaningful route/result, wait, and final-triage
boundaries, emit one line such as `▶️ sweep > respond PR #42 1/3`,
`❓ sweep > preflight · 승인 필요`, `⏳ sweep > respond PR #42 · CI`, or
`✅ sweep > respond PR #42`. Omit `tk-`; `▶️` auto-continues, `❓` needs user
input, `🟢` is standalone manual `Ready`, and `⏳` is machine wait. Keep only
the one decisive token (PR/route/count or wait reason); the marker and route
encode result/next action. Suppress child receipts, reasoning, logs, timers, and
nonterminal `Status:` lines; actual skill names/contracts keep `tk-`.

Use `✅ Pass`, `⏳ Waiting`, `⚠️ Advisory`, `❌ Fail`, `⛔ Blocked`, and
`❓ Unverifiable` for matching outcomes. Render `follow-up-queued` and `waiting`
as `⏳ Waiting`; render user approval, exact held-route selection, and preview
reconfirmation as `❓`, not `⏳`. Preserve terminal `Status: <token>` exactly.

## Aggregate result

`Skipped: already applied` is a PR-local `Pass` with no mutation and counts as
a supported target pass in the batch aggregate. `Pass` requires every
supported target from initial, per-PR, or final router pass.
`follow-up-queued` and `waiting` aggregate to `Pending`, never `Blocked` or
`Fail`. Otherwise aggregate supported results:
`Fail > Blocked > Unverifiable > Pending > Pass`; preserve shared systemic
status that froze later mutation. Keep external CI, `checks_unverifiable`, and
unsupported final items conspicuous; they are not supported successes and alone
do not change otherwise empty/successful batch from `Pass`. When no `auto` row
exists, the report-only/held inventory is scope-complete and does not need
approval or change that otherwise empty batch from `Pass`. After an approved
`auto` batch, a held row awaiting the user's exact high-risk selection or a
re-preview after external head drift is `Pending`; a supported `Act now` item
still present only at final triage is `Blocked`.

Lead `## PR sweep`. Show a Markdown table for every processed PR with
repository, PR number, title, link, initial category, approved/planned action,
actual result, and skip/hold reason when applicable. Also show report-only
external CI and `checks_unverifiable`, retained worktrees, and all remaining
final-triage items. For eight+ final-only rows, show the top five to seven with
links and cite `.tigerkit/pr-sweep.md`. Keep exact child provenance in
artifacts, not terminal response. Lead aggregate result with mapped visible
marker, including `✅ Pass` for full pass, without replacing exact final status
line.

### 🔴 HARD GATE · terminal user summary

Begin only terminal response with `## PR sweep`. No child receipts,
phase-success output, `Outcome:`, caller-return instructions, or bottom metadata
block. End aggregate result section exactly `Status: <token>`.

### 🔴 HARD GATE · response language

Use latest explicit user language for free-form user-facing prose. Keep
headings, statuses, IDs, paths, commands, refs, categories, and exact source
literals stable.

## User decision questions

The preflight preview owns one routine batch approval. Do not ask per-PR
selection or publication questions after that approval. If a new material
identity, ownership, high-risk scope, or out-of-scope authority decision is
required, ask one self-contained `Question` before any `Recommendation`; stop
`Pending | Blocked`. Never infer or broaden the sweep.
