---
name: tk-pr-respond
description: "[user/auto] 하나의 pull request의 feedback/지원 CI 실패를 fresh-read하고, reply-only/direct-TDD/SDD-TDD를 선택해 수정·검증·제한된 publication까지 처리합니다."
disable-model-invocation: false
argument-hint: "<pull request or repository>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
---

# Respond to a single PR review

Apply this skill to `/tk-pr-respond`, `$tk-pr-respond`, explicit host selection, or an exact PR task handed off by an active `tk-pr-sweep`.
Do not apply it to general code changes, simple review summaries, or work spanning multiple PRs.

This skill understands current feedback on one PR, explains the proposed resolution naturally to the user,
and performs changes, verification, push, reply, resolve, and any required re-review request within the approved scope.

**Keep the conversation natural and the state strict.**

Do not expose internal `apply | reply | defer` classifications, worker placement, or GitHub state as a raw report.
The user needs to know what the review means, how it will be addressed, why that approach is appropriate, and what will be verified.
resolution plan 또는 mutation/publication approval이 필요하면 host별 native structured question surface를 우선 사용합니다 (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). unavailable하면 같은 plan을 plain chat으로 fallback하고 parent-approved exact decision은 다시 묻지 않습니다.

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

리뷰 원문이 명시적으로 코드 수정을 요구하면 이를 reply-only 또는 보류로 재분류하지 않습니다. 그렇게 override하려면 현재 턴의 명시적 사용자 재승인이나 확인 가능한 과거 승인 기록(대화 로그·메모리)이 필요하며, 과거 자기 답글의 승인 문구만으로는 증거가 되지 않습니다.

리뷰가 UI 텍스트를 지적하면 현재 화면에 렌더되는 문자열을 component prop, i18n entry, option constant 또는 제공된 screenshot으로 확인한 뒤 verbatim으로 답변합니다. 티켓의 의역이나 code identifier/enum을 그대로 반복하지 않으며, 근거가 없거나 충돌하는 문자열은 사실로 단정하지 않고 `Unverifiable` 또는 필요한 확인으로 남깁니다.

리뷰가 test 추가를 요구하면 파일 존재나 source-text assertion으로 닫지 않습니다. 지적된 regression을 재현하고
real behavior/side effect가 다시 깨질 때 실패하는 protection으로 만듭니다.

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

Code-changing plan은 실제 repository test surface를 조사하고 [behavior-first testing](references/testing.md)에 따라
RED 가능 여부, focused command, required suite, realistic mutation, `N/A` 또는 engineering exception을 닫습니다.
Reply-only, direct+TDD, SDD+TDD 중 practical route를 설명하되 내부 classification form은 노출하지 않습니다.

원인과 exact regression seam이 명백한 feedback/CI 실패는 바로 기존 testing 경로로 갑니다. 원인 불명,
intermittent/flaky, performance regression 또는 재현 난해한 hard CI/regression만
[shared diagnosis](references/diagnosis.md)를 lazy-load하고 fix hypothesis 전에 red-capable feedback loop를
확보합니다. 확보 불가 근거 없이 첫 추측을 수정안으로 고정하지 않습니다.

Express model recommendations only as human-friendly guidance such as “mid-tier coding model,” “stronger final review,” or “independent work fan-out recommended.”
Do not create provider selectors, model classes, reasoning effort, or `session.md`.
Do not mark the task `Blocked` merely because this capability is unavailable.

Obtain one user approval for the current plan. Do not split publication for the same plan into a separate second question.
However, if the PR head/thread/check/identity changes materially after approval, invalidate the approval and explain only what changed.

## Code changes and Seed

Respond tasks requiring code changes use a newly created dedicated worktree with `.tigerkit/seed.md` as the current work contract.
If that worktree cannot be created or proven fresh, return `Blocked` before mutation.
Do not create the `pr-respond.md` lifecycle ledger.

Before approval, preserve an existing Seed byte-for-byte and create no `Status: Pending` file. After approval write the
Ready Seed atomically, reread it, and require `<!-- tigerkit:seed -->` plus deterministic PR/head/task identity. Replace
only a proven TigerKit-owned Seed. Preserve an unmarked/legacy/identity-ambiguous file and return `Blocked` before mutation.

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

이미 활성 Ready Seed가 같은 PR/head/feedback 작업과 정확히 일치하면 재작성하거나 같은 결정을 다시 묻지 않습니다.
새 feedback이나 fresh state가 Seed의 goal/scope/decision/AC를 material하게 바꾸면 기존 파일을 보존하고 해당 부분을
대화에서 다시 준비·승인한 뒤 새 Ready Seed로 atomic replace합니다.

코드 변경 없이 reply만 하는 경우에는 새 Seed를 만들 필요가 없습니다.

## Execution

After approval, choose from the approved feedback shape:

- reply-only: no Seed, production mutation, push, or ceremonial test;
- direct+TDD: one coherent change/review surface; load only the testing reference and execute in the dedicated worktree;
- SDD+TDD: multiple material Units; load [private SDD](references/sdd.md) and follow its exact grammar, recovery,
  implementer/reviewer/fix-loop, model+effort, and final-review contract.

Direct applies RED → verified failure → minimal GREEN → refactor while green → required relevant checks. SDD Unit reports
carry their own test obligation and RED/GREEN evidence. If host fan-out is unavailable, preserve the same role/range gates
sequentially; do not silently lower SDD to unreviewed direct work. The parent stores no provider routing/session ledger.

Both code-changing routes finish with acceptance-criteria review, `tk-browser-verify` for browser-visible changes, required
gap correction, and verified local commit(s). SDD's one whole-change final review satisfies the broad review gate; do not
run a redundant second generic review afterward.

If browser verification requires a development server, provide `tk-browser-verify` with the exact command/cwd/URL/auth/readiness;
the verifier owns server startup, readiness checks, and cleanup.

Do not repeat the same failure indefinitely. If the same blocker remains after three meaningful corrective attempts,
direct work stops with `Fail` or `Unverifiable`; SDD uses its five-round breaker/adjudication. Material Goal/Scope/Decision/
AC/security/required Verification drift returns to the owner preparation path; reversible engineering ambiguity gets an
explicit `Ruling:`. Neither route expands publication authority.

## Publication

Immediately before any remote write, recheck the exact repository, authenticated identity, open PR, fresh remote head,
local ancestry, thread/check state, and approved scope.

Then perform only the approved actions in this order.

1. For a code-changing response, push the verified commit to the exact branch. For reply-only work, do not push.
2. Post an exact reply to each feedback item.
3. Resolve only threads whose reply succeeded and whose resolution was actually verified.
4. Fresh-read reviews/threads/checks.
5. For every human reviewer whose current review state is `CHANGES_REQUESTED`, or whose feedback included an item classified as requiring a code change that resulted in a verified code change regardless of current review state (including `COMMENTED`), fresh-verify eligibility and request re-review for the exact current head. Exclude the author, authenticated user, bots, and still-valid approvers. Reply-only feedback with no code change does not require re-review.
6. After all actionable threads are closed, when a re-review is required or actionable feedback was answered with no outstanding request, fresh-read the exact current head and post exactly one current-head summary comment containing `<!-- tigerkit:pr-summary:<HEAD_SHA> -->`, with `<HEAD_SHA>` replaced by the exact observed head SHA. If that marker already exists exactly once for the current head, do not post another. A summary for an earlier head does not satisfy this requirement. 요약 코멘트는 내부 처리 기록이 아니라 리뷰어에게 보내는 실제 메시지로 작성한다. 리뷰어가 식별되면 `@mention`으로 직접 호명하고, 각 지적과 대응을 자연스러운 서술 또는 매칭되는 표로 설명한다. 검사 결과나 집계만 나열하는 3인칭 완료 로그는 금지한다.

Do not claim publication complete unless fresh evidence proves every required `CHANGES_REQUESTED` reviewer re-review request, zero actionable unresolved threads, and any required current-head summary comment after the threads were closed. Missing evidence is `Unverifiable`, not complete.
Do not claim completion while any unresolved inline thread remains.
Keep deferred, unverifiable, or failed feedback open.

Every generated GitHub comment must end with `_🤖 본 코멘트는 AI가 작성했습니다._`.
Do not merge, close, tag, release, plain force push, or resolve unrelated threads.

## Execution under Sweep

For an exact PR handed off by an active `tk-pr-sweep`, do not ask again about material decisions already approved by the parent.
The child confirms the PR fresh state and parent-approved scope, then proceeds immediately when they match.

The handoff must include a newly created dedicated worktree path. If it is missing or not fresh, return `Blocked` before mutation. Run the child from that worktree; never switch the parent `main` or `develop` checkout to the PR branch.

If new feedback or head drift materially changes the approved scope, escalate only that PR back to the parent.
Do not create `pr-sweep.md`, `pr-respond.md`, or worker receipt Markdown.
For a code-changing PR, only `seed.md` in the fresh dedicated worktree may be used as task context.

The Respond controller may select SDD for its own PR. Normal implementer/reviewer/re-reviewer children remain leaf and may
not recursively delegate. The parent Sweep decides cross-PR scheduling; this child never starts another PR controller.

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
