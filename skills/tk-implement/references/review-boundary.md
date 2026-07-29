# Built-in implementation review

Every standalone unit and every unit handed off by active drive runs this
current-agent gate after unit verification and before commit. Review is scoped
to that unit/ticket and its R/AC; drive separately owns aggregate traceability
and cross-ticket verification. Review is separate from direct/delegated
implementation, and an implementor never counts as an independent reviewer.

## Pre-review quality gates

These gates run before final unit verification and review. The current agent
owns them in direct and delegated modes; an implementor may return evidence but
does not make the ownership decision.

### Design fit

Before source mutation:

1. inspect the one to three closest existing implementations and their tests;
2. inventory reusable components, hooks, utilities, types, state owners,
   query-key factories, and test helpers;
3. identify the existing module that owns each changed responsibility;
4. classify every major responsibility as `reuse existing`,
   `extend existing`, `local implementation`, or `new shared abstraction`.

Use `new shared abstraction` only when code evidence shows an actual second
consumer, an independent variation axis in the current diff, or a clearly
insufficient existing public seam. Without that evidence, keep the
responsibility local or extend its existing owner. Record inspected
paths/symbols and the classification. Do not invoke `tk-ask-repo` or create a
parallel abstraction for convenience.

### Behavior-preserving simplify

After initial GREEN and before final unit verification, run exactly one pass
over the current unit diff and directly connected call sites:

- **Repository reuse:** replace parallel helpers, components, hooks, or types
  with the existing owner where behavior stays unchanged.
- **Simplicity:** remove unnecessary wrappers, pass-throughs, state, effects,
  branches, and indirection.
- **Efficiency:** remove duplicate lookup, transformation, traversal, render
  work, and unsupported memoization.
- **Abstraction fit:** place responsibility with the correct owner, keep
  single-use code local, share only for evidenced consumers, and narrow public
  surfaces to actual need.

Do not change R/AC, behavior, or UI writing, and do not expand into unrelated
cleanup or a repository-wide refactor. Apply at most one bounded change set
and rerun focused verification. With no finding, record `no-op`. Do not add a
reviewer, repeat the full Standards/Spec review, or create a review loop.

### Implementation ledger

Atomically write `.tigerkit/implementation.md` with a same-directory temporary
file plus rename. Update the current unit section for the same task identity;
replace a different task without an archive. Never modify `.gitignore`, and
warn once for the task when `.tigerkit/` is not ignored.

Each unit section records task and unit/ticket identity, R/AC references,
design-fit evidence as `reuse | extend | local | new abstraction`, inspected
paths/symbols, simplify finding and `changed | no-op | deferred`, rerun focused
verification, Standards and Spec dispositions, unit commit SHA, and remaining
risk. Keep it bounded: no raw transcript, full diff, repeated command output,
secret, or unrelated history. After commit, update the SHA without staging the
ignored scratch file.

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

The earlier simplify gate is a proactive, behavior-preserving mutation pass
over repository reuse, simplicity, efficiency, and abstraction fit. It is not
a review axis and does not own correctness or R/AC verdicts. Standards review
may still identify a structural defect that simplify missed, but it does not
repeat the simplify checklist or start another full review cycle.

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

## Post-commit hook drift

Freeze the reviewed candidate/staged diff before invoking commit. Immediately
after a successful commit command, compare the actual committed diff with that
snapshot. For moves, separate expected import/path rewrites before classifying
the remaining delta.

Classify hook-created delta as:

- `none`: committed diff matches the reviewed snapshot;
- `format-only`: only layout such as line wrapping, parentheses, or trailing
  commas changed; record the exact files/lines in Verification;
- `reverted-semantic`: an autofix changed meaning, such as a dependency array.
  Restore the reviewed intent in the working tree, add the narrowest supported
  suppression with a reason, and rerun affected verification.

Never call an unclassified or semantic-drift commit verified. Do not amend,
reset, or hide actual history, and do not create a second unit commit in the
same invocation. Report the actual commit SHA and restored working state as
`Fail` or `Blocked`; a later explicit unit must commit the correction.

Hook bypass is allowed only when byte preservation is itself the spec for a
vendor/generated tree, or a demonstrated hook configuration defect prevents
the target file from being committed. Run every safe applicable check, limit
the bypass to that commit, preserve the required bytes, and include the exact
reason in the commit body. Convenience, speed, or ordinary hook failure is not
an exception.
