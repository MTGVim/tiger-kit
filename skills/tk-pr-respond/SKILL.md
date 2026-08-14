---
name: tk-pr-respond
description: "[user/auto] 하나의 pull request의 review feedback 또는 지원 가능한 GitHub Actions 실패를 fresh state로 읽고, 자연스러운 해결 계획을 합의한 뒤 필요 시 `seed.md`를 사용해 수정·검증·제한된 publication까지 처리합니다."
disable-model-invocation: false
argument-hint: "<pull request or repository>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Respond to a single PR review

Apply this skill to `/tk-pr-respond`, `$tk-pr-respond`, explicit host selection, or an exact PR task handed off by an active `tk-pr-sweep`.
Do not apply it to general code changes, simple review summaries, or work spanning multiple PRs.

This skill understands current feedback on one PR, explains the proposed resolution naturally to the user,
and performs changes, verification, push, reply, resolve, and any required re-review request within the approved scope.

**Keep the conversation natural and the state strict.**

Do not expose internal `apply | reply | defer` classifications, worker placement, or GitHub state as a raw report.
The user needs to know what the review means, how it will be addressed, why that approach is appropriate, and what will be verified.

## Fresh state

At the start, fresh-read exactly one open PR.

- repository and authenticated identity
- PR author, base/head ref, and SHA
- checks and evidence from failed GitHub Actions
- reviews, inline threads, and conversation comments
- unresolved threads
- requested reviewers
- exact push target

Complete all required pagination. Do not treat cached lists or previous Markdown ledgers as current truth.
If identity, the exact PR/head, or remote authority is ambiguous, stop as `Blocked` before mutation.

## Understand feedback

Internally, current feedback may be classified by meaning as follows.

- feedback requiring a code change
- feedback appropriately handled with an evidence-based reply and no code change
- feedback outside the current PR scope or requiring an additional decision

Explain the meaning to the user instead of exposing classification tokens.

Example:

```text
리뷰 3건 확인했어요. 첫 번째는 실제 모바일 깨짐이라 수정이 필요합니다.
두 번째는 현재 구현이 이미 요구사항을 만족해서 코드 변경 없이 근거를 설명하는 게 맞아 보여요.
마지막 건은 제품 동작 자체를 바꾸는 의견이라 이것만 확인이 필요합니다.
```

If the review text already specifies the required outcome, do not ask the same question again.
Investigate repository evidence independently, then explain the recommendation and rationale for decisions about reuse, simplification, testing, security, and user experience.

Ask the user directly only about:

- user-owned decisions that materially change product behavior or scope
- risky or hard-to-reverse decisions involving security, permissions, data, or compatibility
- exceptional approval when the work has been sufficiently improved but verification readiness cannot be raised further

## 🔴 CHECKPOINT · 🛑 STOP · Plan and mutation boundary

Before mutation, require fresh state plus one current approval for standalone work, or the exact parent `tk-pr-sweep` approval for a handed-off PR; invalidate it on material drift and stop before mutation.

## Resolution plan and approval

Before mutation, explain the resolution plan for the current feedback in natural language.

At minimum, cover:

- which feedback will be fixed and which will receive replies only
- implementation approach and existing code to reuse
- how unnecessary complexity will be avoided
- regression and new-test plan
- any special security or user-experience concerns
- the `tk-browser-verify` plan for browser-visible changes
- bounded publication scope for push/reply/resolve/re-review
- recommendation for execution mode and model level

Express model recommendations only as human-friendly guidance such as “mid-tier coding model,” “stronger final review,” or “independent work fan-out recommended.”
Do not create provider selectors, model classes, reasoning effort, or `session.md`.
Do not mark the task `Blocked` merely because this capability is unavailable.

Obtain one user approval for the current plan. Do not split publication for the same plan into a separate second question.
However, if the PR head/thread/check/identity changes materially after approval, invalidate the approval and explain only what changed.

## Code changes and Seed

Respond tasks requiring code changes use `.tigerkit/seed.md` in the relevant checkout/worktree as the current work contract.
Do not create the `pr-respond.md` lifecycle ledger.

The Seed must contain at least the following PR context. Keep user-facing Seed and ledger prose in Korean.

- exact repository/PR/head
- feedback being handled and the outcome requested by the reviewer
- confirmed decisions for code changes, replies, and deferrals
- work background and objective
- scope and forbidden changes
- user decisions
- implementation approach and repository evidence
- Reuse / Simplicity / Tests / Security / Experience decisions
- acceptance criteria and a verification path for each
- browser verification plan
- publication boundary
- implementation guidance needed by a lower-capability executor

이미 활성 Ready Seed가 같은 PR 작업과 정확히 일치하면 재작성하거나 같은 결정을 다시 묻지 않습니다.
새 feedback이나 fresh state가 Seed의 goal/scope/decision/AC를 material하게 바꾸면 `Pending`으로 다시 열고 해당 부분만 재승인합니다.

코드 변경 없이 reply만 하는 경우에는 새 Seed를 만들 필요가 없습니다.

## Execution

After approval, execute through the safe mechanisms available in the current host.

- Use subagent fan-out when work is independent and safely isolated.
- Execute sequentially when isolation is unavailable.
- Use the host default when a specific model cannot be selected.
- The parent must not persist execution details as Markdown routing state.

Each implementer reads the Ready Seed and its assigned scope. The parent does not copy the full conversation or detailed plan again.

Required order:

```text
implementation
→ focused tests/checks
→ acceptance-criteria review
→ tk-browser-verify for browser-visible changes
→ required gap correction
→ verified commit
```

If browser verification requires a development server, provide `tk-browser-verify` with the exact command/cwd/URL/auth/readiness;
the verifier owns server startup, readiness checks, and cleanup.

Do not repeat the same failure indefinitely. If the same blocker remains after three meaningful corrective attempts,
stop with `Fail` or `Unverifiable` and include the remaining evidence.

## Publication

Immediately before any remote write, recheck the exact repository, authenticated identity, open PR, fresh remote head,
local ancestry, thread/check state, and approved scope.

Then perform only the approved actions in this order.

1. Push the verified commit to the exact branch.
2. Post an exact reply to each feedback item.
3. Resolve only threads whose reply succeeded and whose resolution was actually verified.
4. Fresh-read reviews/threads/checks.
5. For every reviewer whose current review state is `CHANGES_REQUESTED`, fresh-verify that the reviewer remains eligible and that a re-review request is required for the exact current head. Request re-review from each such human reviewer, excluding the author, authenticated user, bots, and still-valid approvers.
6. After all actionable threads are closed, fresh-read the exact current head and post exactly one current-head summary comment containing `<!-- tigerkit:pr-summary:<HEAD_SHA> -->`, with `<HEAD_SHA>` replaced by the exact observed head SHA. If that marker already exists exactly once for the current head, do not post another. A summary for an earlier head does not satisfy this requirement.

Do not claim publication complete unless fresh evidence proves every required `CHANGES_REQUESTED` reviewer re-review request, zero actionable unresolved threads, and exactly one current-head summary comment after the threads were closed. Missing evidence is `Unverifiable`, not complete.
Do not claim completion while any unresolved inline thread remains.
Keep deferred, unverifiable, or failed feedback open.

Every generated GitHub comment must end with `_🤖 본 코멘트는 AI가 작성했습니다._`.
Do not merge, close, tag, release, plain force push, or resolve unrelated threads.

## Execution under Sweep

For an exact PR handed off by an active `tk-pr-sweep`, do not ask again about material decisions already approved by the parent.
The child confirms the PR fresh state and parent-approved scope, then proceeds immediately when they match.

If new feedback or head drift materially changes the approved scope, escalate only that PR back to the parent.
Do not create `pr-sweep.md`, `pr-respond.md`, or worker receipt Markdown.
For a code-changing PR, only `seed.md` in the relevant isolated worktree may be used as task context.

## Completion response

Do not output a normal protocol receipt.

Example:

```text
리뷰 3건 처리했습니다. 2건은 코드 수정 후 검증했고 1건은 근거를 설명해 답변했습니다.
모바일 변경은 browser verification까지 통과했고 관련 thread는 모두 resolve됐어요.
현재 head의 검증 결과를 요약해 게시하고 reviewer에게 재검토를 요청했습니다.
이제 reviewer 재확인만 기다리면 됩니다.
```

Only when an issue remains, explain the blocker and next action in detail.
Use exactly one final state matching the actual result: `Status: Pass | Pending | Blocked | Unverifiable | Fail`.
