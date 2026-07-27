# Built-in implementation review

Every standalone unit and every unit handed off by active drive runs this
current-agent gate after unit verification and before commit. Review is scoped
to that unit/ticket and its R/AC; drive separately owns aggregate traceability
and cross-ticket verification. Review is separate from direct/delegated
implementation, and an implementor never counts as an independent reviewer.

## Fixed point and inventory

At preflight, record initial `HEAD`, branch, and pre-existing dirty paths.
Before reading diff content, snapshot candidate and staged inventories against
that fixed point with `git diff --stat`, `git diff --numstat`,
`git diff --cached --stat`, `git diff --cached --numstat`, and the changed-file
list. Exclude pre-existing user changes from ownership and staging.

A candidate is `small` only with at most 15 changed files and at most 800 total
additions plus deletions. More than either threshold is `large`;
binary/rename ambiguity or incomplete inventory is `size_unknown`. For
`large | size_unknown`, do not print a raw full diff into current context. Use
context-indexed summarization, paged file/hunk inspection, or one bounded
independent reviewer while tracking every changed file and hunk. Missing
coverage makes the verdict `Unverifiable`.

Pin review-head SHA and candidate/staged snapshot before findings. Recheck
`HEAD`, branch, and staged inventory immediately before verdict and commit.
Never combine stale line evidence with a changed review head. Changed review
state is `Blocked`; inaccessible evidence after a stable snapshot is
`Unverifiable`.

## Review axes

The current agent runs both axes even for small, low-risk work and keeps the
verdicts separate.

- **Standards:** repository instructions, correctness, duplication, scope
  creep, ownership, unnecessary pass-throughs, public/private boundary leaks,
  testability, side-effect/error boundaries, speculative abstraction, and
  shotgun changes. Stay within the current diff.
- **Spec:** missing, partial, extra, or incorrect behavior; acceptance and
  verification gaps; scope violations. With R/AC IDs, mark each
  `implemented | missing | partial | unverified | not-applicable` with
  file/line and verification evidence. Without a spec source, record
  `no spec`; do not call this axis passed.

Load a high-risk lane only when inventory shows its signal. Record selected
lane and evidence rather than an all-N/A checklist.

| Diff signal | Focused evidence |
|---|---|
| Authentication/authorization | protected entry points, deny-by-default, tenant/object ownership, privilege boundary |
| Privacy/payment | collection/exposure, log leakage, consent/retention, external side effects, idempotency |
| Dependency | source/lockfile change, execution path, permission/network expansion, compatibility evidence |
| Migration/data loss | forward/backward compatibility, rollback, partial failure, old/new reader-writer coexistence |
| Concurrency | atomicity, ordering, retry/idempotency, race and cancellation boundaries |
| Public API | compatibility, validation/error contract, consumer migration, version boundary |

Each finding needs severity, fixed-diff `file:line` evidence, applicable
repository/spec basis, and concrete impact. One independent reviewer is
allowed only for `large` or high-risk work. It may not edit, re-delegate, fan
out, or automatically re-review.

The bounded flow is
`review once → fix once → regression verification once → stop`. Do not commit
while an important finding, drift, or unverified coverage remains.
