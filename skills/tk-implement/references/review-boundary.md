# Implementation review boundary

Every standalone unit and every unit handed off by active drive runs this
current-agent gate after unit verification and before commit. Review is scoped
to that unit/ticket and its R/AC; drive separately owns aggregate traceability
and cross-ticket verification. Review is separate from direct/delegated
implementation. A delegated implementor's self-review never replaces controller
Built-in review or a required Additional review.

## Active-drive verification obligations

Preserve a material profile's `Signals`, source-located `Evidence`,
`Obligations`, and `Unverified` fields unchanged. Do not recompute signals or
add/drop obligations from a task label.

| Obligation | Existing owner in `tk-implement` |
| --- | --- |
| `evidence-closure` | inspection/test-seam checkpoint before mutation |
| `regression-seam` | public-behavior test and coverage contract |
| `compatibility` | affected supported consumer, old/new contract, or host verification |
| `browser-verdict` | `tk-browser-verify` hard gate and receipt |
| `side-effect-recovery` | error, partial-failure, retry/idempotency, and rollback evidence |
| `independent-review` | one bounded non-editing independent reviewer |

Choose the exact supported test, command, browser route, recovery proof, and
review focus inside the corresponding owner. If evidence cannot establish an
obligation, return `Unverifiable`; if required authority or a user decision is
missing, return `Blocked`. Never report `Pass` or commit after silently
weakening the profile. A baseline handoff has no profile and adds no work.

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
verification, implementation strategy, Built-in review status, whether
Additional review was required, its capability label, candidate snapshot
identifier, findings and dispositions, fix-round history, review-driven
changes, Standards and Spec dispositions, unit commit SHA, and remaining or
deferred risk. A no-commit terminal attempt instead records native status,
actual branch and HEAD, changed or uncommitted paths, executed verification,
unverified scope, `commit: none`, the failure or blocker, and one recovery
condition. It never
reuses stale candidate, review, or verification evidence to classify the unit
as completed. Keep the ledger bounded: no raw transcript, full diff, repeated
command output, secret, or unrelated history. After commit, update the SHA
without staging the ignored scratch file.

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

Pin review-head SHA, candidate diff, changed-file inventory, staged/working-tree
ownership, and a diff fingerprint before findings. Built-in and Additional
review inspect this same snapshot. Recheck
`HEAD`, branch, and staged inventory immediately before verdict and commit.
Never combine stale line evidence with a changed review head. Changed review
state is `Blocked`; inaccessible evidence after a stable snapshot is
`Unverifiable`.

If an Additional reviewer mutates files, invalidate its result, report the
mutation, and restore or safely isolate the frozen snapshot. Return
`Unverifiable` when restoration or isolation cannot be proven.

## Additional review policy

Built-in Standards/Spec review is mandatory for every unit. Additional review
is required when any are true: a high-risk signal exists; diff size is
`size_unknown`; a `large` diff changes executable behavior; the user explicitly
requires separate/independent review; or a sealed drive obligation requires it.
Pure documentation, comments, and non-behavioral generated artifacts are not
forced into Additional review by size alone.

Select exactly one compatible read-only capability in this order: one named by
the user, one required by repository/user instructions, then one available in
the current host. The path must be distinct from implementation. Loading a
checklist or another `SKILL.md` in the same agent is not independent review.
Do not auto-install, request new authentication solely for review, transmit code
to an unauthorized provider, fan out, permit reviewer mutation or nested
delegation, or run unrelated commands. When Additional review is required but
unavailable, return `Unverifiable` and do not commit; stop before implementation
when unavailability is known in preflight.

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

Each finding needs severity, candidate-snapshot `file:line` evidence, applicable
repository/spec basis, concrete impact or failure path, and reproduction detail
when practical. Generic suggestions without concrete evidence are non-blocking.

Aggregate Built-in and Additional findings as `accepted | rejected | contested
| deferred-minor`. Merge only the same defect and fix path, preserve distinct
failure modes, reject unsupported findings, recalibrate inflated severity, and
exclude clearly pre-existing defects from the blocking set. A real plan/spec
conflict requiring user judgment is `Blocked`.

Blocking findings are failed spec compliance, Critical or Important findings,
a controller-confirmed `cannot verify` gap, or a reproducible correctness/
regression failure. Run at most five fix rounds. One round is exactly: fix open
blocking findings, run covering verification, run scoped re-review over the fix
diff, then update open-finding state. Scoped re-review checks whether accepted
findings are fixed and whether the fix introduced new Critical/Important
breakage; untouched-code observations, unrelated refactors, style preferences,
and new Minor findings cannot extend the loop. The controller always performs
Built-in scoped review, and every round also uses a compatible independent
scoped review path when Additional review was initially required.

Rounds 1–3 use the current implementation owner. For delegated work, resume the
original implementor or give a fresh implementor the same brief, report, and
open findings when resumption is impossible. For rounds 4–5, switch to a fresh
implementation context when available; otherwise trip the breaker after round
3 instead of repeating the ineffective route. At the cap or early breaker,
adjudicate every open finding: unsupported as `rejected`, real Minor as
`deferred-minor`, real blocking as `Unverifiable`, plan/spec conflict as
`Blocked`, and covering verification failure as `Fail`. Never commit while an
accepted blocking finding, drift, or unverified coverage remains.

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
