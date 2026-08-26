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
When a resolution plan or mutation/publication approval is needed, prefer the host's native structured question surface (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). If unavailable, present the same plan in plain chat; do not ask again for an exact decision approved by the parent.

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

If the review text already specifies the required outcome, do not ask the same question again.
Investigate repository evidence independently, then explain the recommendation and rationale for decisions about reuse, simplification, testing, security, and user experience.

When review text explicitly requires a code change, do not reclassify it as reply-only or deferred. Overriding that requirement needs explicit user reapproval in the current turn or a verifiable prior approval record (conversation log or memory); approval wording in the agent's own earlier reply is not evidence.

When review feedback concerns UI text, verify the currently rendered string through a component prop, i18n entry, option constant, or supplied screenshot, then reply verbatim. Do not repeat a ticket paraphrase or code identifier/enum as visible text. Leave an unsupported or conflicting string `Unverifiable` or request the needed confirmation.

When feedback uses project-specific terminology, lazy-load [domain context](references/domain-context.md) and preserve
canonical vocabulary without overriding verified user-visible UI literals.

When feedback directly concerns architecture, compatibility, or a boundary decision, combine the current diff with
only relevant ADR rationale. Do not make ADR review a generic checklist and never scan an unrelated ADR or context tree.

When feedback requests a test, do not close it with file-existence or source-text assertions. Reproduce the reported
regression and add protection that fails when the real behavior or side effect breaks again.

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
- practical execution shape: reply-only, direct, or SDD

For a code-changing plan, inspect the actual repository test surface and use [behavior-first testing](references/testing.md)
to resolve RED feasibility, the focused command, required suite, realistic mutation, and any `N/A` or engineering exception.
Explain the practical route among reply-only, direct+TDD, and SDD+TDD without exposing an internal classification form.

Send feedback/CI failures with an obvious cause and exact regression seam directly through the existing testing path.
Lazy-load [shared diagnosis](references/diagnosis.md) only for unknown-cause, intermittent/flaky, performance, or
difficult-to-reproduce hard CI/regression cases, and establish a red-capable feedback loop before a fix hypothesis.
Do not lock the first guess into a change without evidence that such a loop cannot be established.

TigerKit decides only `reply-only | direct | SDD`; host/user model selection remains outside durable artifacts.
Do not mark the task `Blocked` merely because model-control capability is unavailable.

Obtain one user approval for the current plan. Do not split publication for the same plan into a separate second question.
However, if the PR head/thread/check/identity changes materially after approval, invalidate the approval and explain only what changed.

## Workspace isolation

Reply-only work needs no workspace solely for isolation. For a code-changing route, first inspect the current Git
checkout, including branch/HEAD, linked-worktree state, unrelated work, and whether
`git rev-parse --show-superproject-working-tree` identifies a submodule. `GIT_DIR != GIT_COMMON` is only a linked-worktree
signal after that submodule guard; it does not by itself prove the checkout belongs to this PR.

A small direct fix may reuse the current checkout only when it is the exact PR branch, clean, safe, and contains no
unrelated work. When dedicated isolation is required, detect existing task isolation before creating anything. Inspect
the current tool surface for concrete native entry points such as `EnterWorktree`, `WorktreeCreate`, `/worktree`, or
`--worktree`; these are capability examples, not durable provider routing. Prefer an available agent-callable native
worktree/workspace mechanism and fresh-read the resulting path, branch or detached state, and HEAD. An approval that
already authorizes the exact code-changing plan and isolated workspace setup also authorizes using that host-native
mechanism; do not ask a duplicate workspace-consent question.

Use manual `git worktree` only when no safe native mechanism is available. The fallback must start from the exact
approved PR head, avoid path/branch collisions and unrelated work, and be fresh-read after creation. Do not edit
`.gitignore` or create a setup commit merely to make manual isolation possible. If required isolation cannot be created
and proven safe, return `Blocked` before mutation rather than falling back to an unsafe parent/default checkout.

A host-managed workspace keeps its host-owned lifecycle. Do not remove, prune, relocate, or otherwise clean it as part of
Respond completion. "Dedicated worktree" in this skill is a semantic isolation requirement, not a requirement to bypass
a host-native workspace with raw `git worktree add`.

## Code changes and Seed

Use no Seed for reply-only or a small, obvious code fix when conversation plus fresh repository/PR evidence is sufficient.
Use a dedicated isolated workspace when the current checkout does not satisfy the preceding safety contract. Use a Ready
Seed for fresh-child execution, durable context, or complex verification, and Ready Seed + SDD for multiple material Units.
If a required isolated workspace cannot be created or proven fresh, return `Blocked` before mutation.
Do not create the `pr-respond.md` lifecycle ledger.

Before approval, preserve an existing Seed byte-for-byte and create no `Status: Pending` file. When the selected route
needs a Seed, after approval write the
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

If an active Ready Seed exactly matches the same PR/head/feedback work, do not rewrite it or ask the same decision again.
If new feedback or fresh state materially changes the Seed's goal/scope/decision/AC, preserve the existing file,
prepare and approve the changed portion in conversation, then atomically replace it with a new Ready Seed.

A no-Seed route still binds reviewer intent, test obligation, and publication scope to the approved conversation and
fresh repository/PR evidence.

## Execution

After approval, choose from the approved feedback shape:

- reply-only: no Seed, production mutation, push, or ceremonial test;
- direct+TDD: one coherent change/review surface; load only the testing reference and execute in the proven safe checkout;
- SDD+TDD: multiple material Units; load [private SDD](references/sdd.md) and follow its exact grammar, recovery,
  implementer/reviewer/fix-loop, model+effort, and final-review contract.

Direct applies RED → verified failure → minimal GREEN → refactor while green → required relevant checks. SDD Unit reports
carry their own test obligation and RED/GREEN evidence. If host fan-out is unavailable, preserve the same role/range gates
sequentially; do not silently lower SDD to unreviewed direct work. The parent stores no provider routing/session ledger.

Every direct exact-change review and every SDD `Unit`/whole-change review records independent `Spec/AC` and `Quality/Standards`
verdicts; a clean result on one axis never offsets failure on the other. One reviewer or one serial review may judge both axes;
do not add a mandatory second reviewer or parallel reviewer fan-out.

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
6. After all actionable threads are closed, when a re-review is required or actionable feedback was answered with no outstanding request, fresh-read the exact current head and post exactly one current-head summary comment containing `<!-- tigerkit:pr-summary:<HEAD_SHA> -->`, with `<HEAD_SHA>` replaced by the exact observed head SHA. If that marker already exists exactly once for the current head, do not post another. A summary for an earlier head does not satisfy this requirement. Write the summary as a real message to the reviewer, not an internal processing record. When the reviewer is identifiable, address them with `@mention` and explain each finding and response in natural prose or a matching table. Do not publish a third-person completion log that only lists checks or totals.

Do not claim publication complete unless fresh evidence proves every required `CHANGES_REQUESTED` reviewer re-review request, zero actionable unresolved threads, and any required current-head summary comment after the threads were closed. Missing evidence is `Unverifiable`, not complete.
Do not claim completion while any unresolved inline thread remains.
Keep deferred, unverifiable, or failed feedback open.

Every generated GitHub comment must end with `_🤖 본 코멘트는 AI가 작성했습니다._`.
Do not merge, close, tag, release, plain force push, or resolve unrelated threads.

## Execution under Sweep

For an exact PR handed off by an active `tk-pr-sweep`, do not ask again about material decisions already approved by the parent.
The child confirms the PR fresh state and parent-approved scope, then proceeds immediately when they match.

Reply-only handoffs need no workspace solely for isolation. A code-changing handoff must include a newly established
dedicated workspace path, exact PR head, and enough provenance to prove it belongs to that row. "Newly established" may
mean a host-native workspace or a safe manual Git fallback; it never requires a nested manual worktree inside an already
proven host-managed workspace. If the path/HEAD/provenance is missing or not fresh, return `Blocked` before mutation. Run
the code-changing child from that workspace; never switch the parent `main` or `develop` checkout to the PR branch.

If new feedback or head drift materially changes the approved scope, escalate only that PR back to the parent.
Do not create `pr-sweep.md`, `pr-respond.md`, or worker receipt Markdown.
For a code-changing PR that needs durable context, only `seed.md` in the proven dedicated workspace may be used as task context.

The Respond controller may select SDD for its own PR. Normal implementer/reviewer/re-reviewer children remain leaf and may
not recursively delegate. The parent Sweep decides cross-PR scheduling; this child never starts another PR controller.

## Completion response

Do not output a normal protocol receipt.

Only when an issue remains, explain the blocker and next action in detail.
Use exactly one final state matching the actual result: `Status: Pass | Pending | Blocked | Unverifiable | Fail`.
