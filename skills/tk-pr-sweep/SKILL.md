---
name: tk-pr-sweep
description: "[user] 설정된 repository들의 open pull request를 deterministic fresh triage로 읽고, 지금 처리할 일과 기다릴 일을 자연스럽게 브리핑한 뒤 한 번 승인된 범위에서 bounded multi-PR maintenance를 수행합니다."
disable-model-invocation: true
argument-hint: "[--report] [--recover-publication] [--repo <owner/name>]"
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
Instead, brief the user in plain language: what can be handled now, what must wait, why, and how the work will proceed.

## Target repositories

Use the following user-level configuration as the default repository scope:

```text
$XDG_CONFIG_HOME/tigerkit/pr-triage.json
```

This configuration owns only the long-lived repository list.
Do not store model mappings, selectors, effort levels, worker routing, fan-out preferences, or task state there.

If the configuration does not exist, bootstrap it only when the current checkout’s origin can be identified safely.
An explicit `--repo owner/name` limits the scope of that run.

## Deterministic triage

Use `skills/tk-pr-sweep/scripts/triage.mjs` as the canonical fresh inventory.

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

Example:

```text
지금 처리할 PR은 3개예요.
#121 — 리뷰 대응 필요
#124 — GitHub Actions 수정 필요
#128 — rebase 필요

#130, #132는 사람 리뷰 대기이고 #135는 외부 CI 대기라 지금 손댈 필요 없습니다.
```

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

Example:

```text
PR 8개를 봤는데 지금 손댈 건 4개예요.
#121은 리뷰 수정, #124는 repository-caused Actions 실패, #128은 rebase,
#130은 코드 변경 없이 답변만 하면 됩니다.

#121/#124는 서로 독립적이라 격리된 subagent 병렬 처리가 가능하고,
#128은 별도 rebase로 두는 걸 추천해요. 끝나면 전체 상태를 다시 확인하겠습니다.
```

The execution model may recommend only broad capability classes such as “중간급 coding model” or “충돌은 더 강한 reasoning model”.
Do not create a specific provider selector, tier, reasoning effort, or `session.md`.
Do not mark the entire Sweep as `Blocked` merely because these controls are unavailable.

Once the user approves the batch plan, that approval grants authority only for the exact PRs, heads, work types, and publication scope in the plan.
Do not request the same approval again for each child.

## Execution isolation

Prove checkout isolation before changing multiple PRs concurrently.
Use isolated worktrees or subagents when the host provides them.
If safe parallel isolation is unavailable, process the PRs sequentially.

If one PR cannot be bound safely to the current checkout, hold only that PR and continue with other independent PRs.
The absence of worker or model controls is not itself a blocker.

## Per-PR handling

Immediately before handling each PR, reread fresh triage and the exact PR state.

Representative routes:

- review feedback or repository-caused GitHub Actions failure → follow the `tk-pr-respond` procedure
- merge conflict or base drift → follow the `tk-pr-rebase` procedure
- external CI, queued/flaky/infrastructure failures, or pending human review → wait
- unsupported state → report-only

If the parent-approved exact PR/head and resolution direction remain unchanged, the child must not ask for the same decision again.
Return that PR to the user only when there is a material change, such as new feedback, head drift, or scope drift.

## Per-PR Seed

Do not create one giant Seed for the entire Sweep.

Each PR requiring code changes may use `.tigerkit/seed.md` in its own isolated checkout or worktree.
The Seed must be self-contained and include that PR’s feedback, objective, decisions, approach, AC, verification, and publication boundary.

Do not force a Seed onto reply-only work or a pure rebase that does not require separate implementation context.

Do not create `pr-sweep.md`, `pr-respond.md`, or worker receipt Markdown.

## Publication

Before every child remote write, fresh-read and verify the exact repository, PR, head, identity, refspec, thread, and check.
Permit only push, reply, resolve, and re-review actions within the parent-approved scope.

After all actionable review threads are closed, the publication contract additionally requires:

- For every reviewer whose current review decision is `CHANGES_REQUESTED`, fresh verification that a re-review request was sent to that exact reviewer for the current head.
- Exactly one current-head summary comment containing the marker `<!-- tigerkit:pr-summary:<HEAD_SHA> -->`, where `<HEAD_SHA>` is the exact current head SHA.
- Fresh verification that the marked summary comment exists on the exact PR and current head, and that no duplicate current-head summary comment with the same marker exists.
- The summary comment must be published only after actionable threads are closed.

Do not report a PR as complete when evidence is missing for any required `CHANGES_REQUESTED` reviewer re-review request, actionable-thread closure, or the single current-head summary comment.

If publication is partially blocked by permissions, preserve and report the already verified local commit and exact remote state.
A retry in the same run is allowed only after re-verifying the exact target and refspec.
A later-session `--recover-publication` is allowed only when the local commit, remote head, approved target, required re-review requests, actionable-thread state, and current-head summary-comment state can all be reconstructed from fresh evidence.
Otherwise stop as `Unverifiable`.
Never use plain force or a guessed refspec.

## Queue progress

A local failure in one PR does not automatically stop other independent PRs.
Stop the entire Sweep only for a systemic failure, such as identity or permission contamination, ambiguous repository scope, or untrustworthy triage.

After each PR succeeds or fails, triage that PR again to confirm that its actual state changed.
After every planned row finishes, run final fresh triage across all configured repositories.

A PR is not complete unless final fresh triage confirms the required checks, publication state, all required `CHANGES_REQUESTED` reviewer re-review requests, closed actionable threads, and exactly one current-head summary comment marked `<!-- tigerkit:pr-summary:<HEAD_SHA> -->`.

## Completion response

Do not dump internal categories or receipts.

Example:

```text
이번 Sweep에서는 4개 중 3개를 처리했습니다.
#121과 #124는 수정·검증·push 완료, #130은 답변 완료입니다.
#128은 새 conflict가 확인돼 보류했고, 나머지는 사람/외부 CI 대기 상태입니다.
```

Keep successfully handled items brief and explain only problematic PRs in the necessary detail.
Never describe an item as complete when required publication evidence is missing.
Use exactly one final status based on the actual result: `Status: Pass | Pending | Blocked | Unverifiable | Fail`.
