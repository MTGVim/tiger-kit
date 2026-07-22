# Built-in implementation review

Every standalone implementation and drive implementation phase runs this current-agent gate after final verification and before commit. Review is separate from direct/delegated implementation; an implementor never counts as an independent reviewer.

## Fixed point and inventory

At preflight, resolve and record the initial `HEAD`, branch, and pre-existing dirty paths. Before reading diff content, snapshot candidate and staged inventories against that fixed point with `git diff --stat`, `git diff --numstat`, `git diff --cached --stat`, `git diff --cached --numstat`, and the changed-file list. Exclude pre-existing user changes from ownership and staging.

A candidate is `small` only when it has at most 15 changed files and at most 800 additions plus deletions. More than either threshold is `large`; binary/rename ambiguity or incomplete inventory is `size_unknown`. For `large | size_unknown`, do not print a raw full diff into the current context. Use context-indexed summarization, redirected and paged file/hunk inspection, or one bounded independent reviewer while tracking coverage of every changed file and hunk. Missing coverage makes the verdict `Unverifiable`.

Pin the review-head SHA and candidate/staged snapshot before findings. Recheck `HEAD`, branch and staged inventory immediately before verdict and commit. Do not combine stale line evidence with a changed review head; rerun affected inspection or stop `Blocked | Unverifiable`.

## Review axes

Run both axes in the current agent even for small, low-risk work. Keep verdicts separate.

- **Standards:** repository instructions, correctness, duplication, scope creep, ownership, unnecessary pass-throughs, public/private boundary leaks, testability, side-effect/error boundaries, speculative abstraction and shotgun changes. Stay within the current diff.
- **Spec:** missing, partial, extra or incorrect behavior; acceptance and verification gaps; scope violations. When the source has R/AC IDs, mark each `implemented | missing | partial | unverified | not-applicable` with file/line and verification evidence. If there is no spec source, record `spec 없음`; do not call that axis passed.

Load the high-risk lanes below only when the inventory shows an applicable signal. Record the selected lane and evidence, not an all-N/A checklist.

| Diff signal | Focused evidence |
| --- | --- |
| 인증·권한 | protected entry points, deny-by-default, tenant/object ownership, privilege boundary |
| 개인정보·결제 | collection/exposure, log leakage, consent/retention, external side effects and idempotency |
| Dependency | source/lockfile change, execution path, permission/network expansion, compatibility evidence |
| Migration·data loss | forward/backward compatibility, rollback, partial failure, old/new reader-writer coexistence |
| Concurrency | atomicity, ordering, retry/idempotency, race and cancellation boundaries |
| Public API | compatibility, validation/error contract, consumer migration and version boundary |

Each finding needs severity, fixed-diff `file:line` evidence, applicable repository/spec basis, and concrete impact. An independent reviewer is allowed only for `large` or high-risk work, at most one total; it may not edit, re-delegate, fan out or automatically re-review.

The bounded flow is `review once → fix once → regression verification once → stop`. If an important finding, drift, or unverified coverage remains, do not commit.
