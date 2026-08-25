---
name: tk-pr-sweep
description: "[user] 설정된 repository들의 open pull request를 deterministic fresh triage로 읽고, 지금 처리할 일과 기다릴 일을 자연스럽게 브리핑한 뒤 한 번 승인된 범위에서 bounded multi-PR maintenance를 수행합니다."
disable-model-invocation: true
argument-hint: "[--report] [--repo <owner/name>]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Multi-PR cleanup

Start only through an explicit `/tk-pr-sweep`, `$tk-pr-sweep`, or host skill selection.
Do not invoke automatically for a generic request to clean up open PRs, respond to one PR review, or fix ordinary CI failures.

Sweep is a controller that reads and organizes the **fresh state of multiple PRs**.
Do not duplicate long-lived task state in a Markdown ledger. The current GitHub and Git state is the source of truth.

**Keep the conversation natural and the state handling strict.**

Do not expose `actionable`, `held`, backend details, routing state, or worker receipts by default.
Brief the user in plain language about what can proceed, what must wait, why, and how. For batch plan approval, prefer the host's native structured question surface (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). If unavailable, fall back to plain chat and do not repeat approval for every child.

## Target repositories

Use the following user-level configuration as the default repository scope:

```text
$XDG_CONFIG_HOME/tigerkit/pr-triage.json
```

This configuration owns only the long-lived repository list.
Do not store model mappings, selectors, effort levels, worker routing, fan-out preferences, or task state there.

If the configuration does not exist, bootstrap it only in execution mode when the current checkout’s origin can be identified safely. `--report` must use the helper's no-bootstrap path and keep the origin-derived repository list in memory; an explicit `--repo owner/name` limits the scope of that run.

## Deterministic triage

Use `skills/tk-pr-sweep/scripts/triage.mjs` as the canonical fresh inventory. Report-only runs use `--no-bootstrap`.

At minimum, inspect:

- open PRs
- author and requested reviews
- exact base/head and SHA
- mergeability and conflicts
- GitHub Actions versus external checks
- review decision
- unresolved review threads
- latest actionable feedback and author response
- current re-review request for every active `CHANGES_REQUESTED` reviewer
- exactly one current-head summary marker after actionable threads close

Do not treat a cached user-supplied list or a previous `.tigerkit/pr-sweep.md` as current truth.

## `--report`

`--report` is strictly read-only.

When the user-level config is missing, read the current checkout's origin for this run only. Do not create the config directory/file; use an explicit `--repo owner/name` when no safe origin exists.

Keep the default output to a short briefing. Do not create lifecycle Markdown, a Seed, worktree, commit, push, reply, or resolution.
If a repository cannot be read, separate that failure from successful repository results and explain which state could not be retrieved.

## Execution plan

In execution mode, plan only PRs that are currently actionable according to fresh triage.

Explain each PR at the level the user needs to understand:

- why it is actionable now
- what kind of work it requires
- whether code changes are required
- what verification is required
- whether it is risky or requires a user decision
- whether it is independent of the other work
- whether the PR owner is likely to use direct execution or its shared SDD protocol

TigerKit decides only the execution shape. Model selection remains the host/user's responsibility and is never persisted.
Do not mark the entire Sweep as `Blocked` merely because model controls are unavailable.

## 🔴 CHECKPOINT · 🛑 STOP · Batch approval

Do not create child worktrees, write Seeds, or perform any remote or product mutation until the user explicitly
approves the exact PRs, heads, work types, and publication scope in the batch plan. If approval is missing or fresh
state changes that scope, remain pending and ask again only for the affected decision.

Once the user approves the batch plan, that approval grants authority only for the exact PRs, heads, work types, and publication scope in the plan.
Do not request the same approval again for each child.

## Execution isolation

`--report` and pre-approval fresh triage are read-only and do not create worktrees.
After batch approval, code-changing children and any child that performs Git mutation require a newly created dedicated
worktree before handling begins. Reply-only children do not create a worktree solely for isolation. The parent `main` or
`develop` checkout is never used for child Git mutation and never branch-switched with `git switch` or `git checkout`.
A subagent counts as isolation only when it receives and uses that fresh worktree. Do not reuse another PR's or a previous child's worktree.
If a fresh worktree cannot be created or passed to the child, hold only that PR as `Held` or `Blocked`; do not fall back to sequential handling in the parent `main`/`develop` checkout. The absence of worker or model controls is not itself a blocker; inability to establish the worktree boundary is a PR-local blocker.

Sweep remains a PR queue controller, not a task-level SDD controller. It never parses SDD Units, dispatches their
implementers/reviewers, or writes `sdd.md`; the PR owner such as `tk-pr-respond` owns those semantics inside one worktree.
PR-level fan-out is not SDD task decomposition.

Rows whose PR owner selects shared SDD run **sequentially by default within this Sweep** so nested controllers do not
multiply concurrently. Reply-only, wait/report, pure rebase, and non-SDD rows may retain existing safe PR-level
concurrency. Do not create a global scheduler/capacity ledger. One PR-local SDD failure does not stop later independent
rows; record that PR's result and continue.

## Per-PR handling

Immediately before handling each PR, reread fresh triage and the exact PR state.
Before a child route that needs Git mutation, verify the fresh dedicated worktree path for that PR and pass it to the
child. If it is absent, hold or block before mutation.

Representative routes:

- review feedback or repository-caused GitHub Actions failure → follow the `tk-pr-respond` procedure
- merge conflict or base drift → follow the `tk-pr-rebase` procedure
- external CI, queued/flaky/infrastructure failures, or pending human review → wait
- unsupported state → report-only

If the parent-approved exact PR/head and resolution direction remain unchanged, the child must not ask for the same decision again.
Return that PR to the user only when there is a material change, such as new feedback, head drift, or scope drift.

## Per-PR Seed

Do not create one giant Seed for the entire Sweep.

Each code-changing or Git-mutating PR child uses its own newly created dedicated worktree. A code-changing child uses a
marked, current-PR/head Ready `.tigerkit/seed.md` only when its owner selects durable context or SDD; reply-only work uses
neither a Seed nor a worktree solely for isolation, and pure rebase follows `tk-pr-rebase` isolation.
The Seed must be self-contained and include that PR’s feedback, objective, decisions, approach, AC, verification, and publication boundary. If a child scope names a user-visible UI element, carry the verbatim constraint into that handoff: quote the exact rendered string or verified entry path, cite its repository or supplied-screenshot basis, and do not pass along paraphrases, code identifiers, enum-derived labels, or unverified grouped claims.

Do not force a Seed onto reply-only work or a pure rebase that does not require separate implementation context.

Do not create `pr-sweep.md`, `pr-respond.md`, or worker receipt Markdown.
Do not reuse or resume a different PR/Seed identity's `sdd.md`.

## Publication

Child owners own their detailed publication order, reviewer semantics, replies, thread closure, summary format, refspec,
and retry rules. Sweep passes only the parent-approved scope and never broadens it.

After each child returns, fresh-read GitHub state and verify the required outcome: exact head, checks, actionable thread
closure, required re-review request, and any owner-required current-head summary. Do not trust a child receipt or repeat
the child procedure in Sweep. Missing or irreconstructible evidence is `Unverifiable`; one PR's partial publication does
not broaden authority or stop independent rows.

## Queue progress

A local failure in one PR does not automatically stop other independent PRs.
Stop the entire Sweep only for a systemic failure, such as identity or permission contamination, ambiguous repository scope, or untrustworthy triage.

After each PR succeeds or fails, triage that PR again to confirm that its actual state changed.
After every planned row finishes, run final fresh triage across all configured repositories.

A PR is not complete unless final fresh triage confirms the required checks, publication state, all required `CHANGES_REQUESTED` reviewer re-review requests, closed actionable threads, and any required current-head summary comment marked `<!-- tigerkit:pr-summary:<HEAD_SHA> -->`.

## Completion response

Do not dump internal categories or receipts.

Keep successfully handled items brief and explain only problematic PRs in the necessary detail.
Never describe an item as complete when required publication evidence is missing.
Use exactly one final status based on the actual result: `Status: Pass | Pending | Blocked | Unverifiable | Fail`.
