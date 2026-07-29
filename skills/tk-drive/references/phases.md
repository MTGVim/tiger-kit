# Phase invariants

These are orchestration gates. Semantic phase behavior belongs to
`tk-grill-me`, `tk-to-spec`, `tk-to-tickets`, and `tk-implement`; drive
consumes their receipts and never recreates a failed or unavailable phase
inline.

The phase-owner allowlist is
`tk-grill-me | tk-to-spec | tk-to-tickets | tk-implement`. The conditional
support allowlist is
`tk-prototype | tk-browser-verify | tk-merge-conflict | tk-reflect
(drive-optimistic tail only)`. Do not invoke other planning, learning,
reflection, or handoff skills.
Do not intercept standalone phase requests or let a phase owner take over
drive-wide orchestration, aggregate verification, or the final receipt.

## Preflight and source

- Resolve branch, initial `HEAD`, pre-existing dirty paths, and ownership
  before mutation.
- For a remote source, retrieve the complete body, all comments and thread
  updates, and every referenced attachment before freezing scope. An
  inaccessible required item is `Unverifiable`; a later scope amendment is
  source, not optional context.
- Source precedence is: latest explicit drive input, confirmed
  same-conversation decisions, relevant current spec, relevant current
  tickets, repository instructions, code/tests.
- Adopt existing artifacts only when task identity and current evidence match.
  Revalidate completed phases and skip them only when their owner skill's
  current contract still passes.
- When a new decision invalidates a Ready spec or downstream tickets,
  revalidate the spec through `tk-to-spec`, then replace or remove stale
  tickets without archives. Ask only when task identity or decision reversal
  cannot be established.
- Treat `/tk-drive`, `$tk-drive`, and picker-equivalent direct selection as
  host-native explicit starts. Do not bind explicit start to one host syntax.
- Do not create current pointers, archives, automatic migration, or other
  drive-only or global state.

### Risk-based verification profile

After source and ownership are resolved, classify only material signals with
an exact source/repository location. A category name, task label, intuition, or
unsupported possibility is not evidence.

| Signal | Material evidence | Derived obligations |
| --- | --- | --- |
| `security-data` | user/sensitive data, authentication, authorization, privacy, payment, or another trust boundary changes | `regression-seam`, `side-effect-recovery`, `independent-review` |
| `state-compatibility` | schema, migration, persisted state, backward compatibility, dependency, or old/new reader-writer behavior changes | `regression-seam`, `compatibility`, `side-effect-recovery`, `independent-review` |
| `public-blast-radius` | a public API, distributed contract, or behavior used by multiple evidenced consumers changes | `regression-seam`, `compatibility`, `independent-review` |
| `browser-network` | persistent visible UI, browser runtime, network transition, or cross-browser behavior changes | `regression-seam`, `browser-verdict` |
| `concurrency-side-effect` | concurrency, retry, idempotency, destructive operation, or external side effect changes | `regression-seam`, `side-effect-recovery`, `independent-review` |
| `evidence-recovery` | required source/reproduction/testability evidence is missing or unstable, or rollback cost/failure-detection delay is material | `evidence-closure` |

Emit selected signals in table order. De-duplicate derived obligations and emit
them in this order: `evidence-closure`, `regression-seam`, `compatibility`,
`browser-verdict`, `side-effect-recovery`, `independent-review`. The compact
material profile contains only `Signals`, source-located `Evidence`,
`Obligations`, and `Unverified`.

With no selected signal, preserve the baseline path without an artifact,
profile section, additional handoff payload, reviewer, browser run,
compatibility command, or user output. Never create a dedicated risk document
or convert the mapping into a score.

Before the spec handoff, freeze any material profile. Required inaccessible
non-user-owned evidence is `Unverifiable`; missing user-owned authority or
intent may route through the existing decision owner. Do not infer a safe
default, continue with an incomplete profile, or silently remove an obligation.

## Phase handoff envelope

Every handoff records phase, task identity, source/artifact paths, stable R/AC
or ticket IDs, branch, initial/current `HEAD`, ownership, and the success state
needed to continue. Before invoking the owner, drive records the native
`Success state` and exactly one drive-owned `Outstanding transition`. The
transition names the next drive action after success, such as `spec gate`,
`ticket decision`, `implementation unit <ID>`, or `aggregate verification`.
When a material verification profile exists, the envelope also carries its
frozen four fields unchanged; a baseline run carries no placeholder profile.
Each owner keeps its native receipt; drive maps only the minimal continuation
state and does not create a shared runtime contract.

On native success, an active-drive owner echoes `Return to: tk-drive` and the
parent-supplied `Outstanding transition` verbatim without choosing or executing
that transition. Drive compares the echo with the recorded handoff before
consuming the receipt. A missing or mismatched success-state or transition echo
is receipt drift and stops drive `Blocked`; progress text or an otherwise valid
child receipt cannot substitute for the echo.

Decision-capable non-success receipts include
`User decision: required | none`. `required` must cite a new user-owned
decision and its evidence; `none` never routes to grill. Drive maps grill native
status to workflow terminal status as `confirmed → Pass`, `pending → Pending`,
`aborted | Blocked → Blocked`, and `Unverifiable → Unverifiable`.

- Decision closure continues only from `tk-grill-me` `confirmed`.
- Spec continues only from `tk-to-spec` `Ready`.
- Tickets continue only from a successfully written and revalidated
  `tk-to-tickets` ledger.
- Implementation continues only from a `tk-implement` `Pass` receipt with the
  expected unit/ticket ID and commit SHA.
- `Draft`, `Pending`, `Blocked`, `Fail`, `Unverifiable`, unavailable skills,
  stale evidence, or mismatched IDs stop drive at that phase.

The user's answer to the directly corresponding pending grill question stays
owned by `tk-grill-me`. Its `confirmed` receipt updates source traceability and
returns control to drive at the spec gate. No other response inherits drive
authority.

## Receipt liveness

Consuming a native receipt creates a transition obligation; it is not itself
completion. In the same active turn, drive must map the receipt to exactly one
of:

1. the next eligible phase handoff;
2. the bounded corrective cycle;
3. `tk-grill-me` for a newly evidenced user-owned decision; or
4. an explicit drive terminal receipt with the supported
   `Pass | Pending | Blocked | Fail | Unverifiable` status and reason.

Spec `Ready` transitions to the ticket decision. A valid ticket ledger
transitions to its first or next pending unit. A matching implementation
`Pass` transitions to the next unit or aggregate verification. Aggregate
success transitions to the reflection tail. Reflection `Pass` with a matching
echo transitions to the final `Pass` receipt. A reflection `Fail` with verified
restoration also transitions to the final receipt while preserving product
`Pass`; unrestored or indeterminate reflection state stops
`Blocked | Unverifiable`. Progress commentary and child receipt summaries do
not discharge this obligation.

Before returning control, verify that every consumed receipt has one recorded
outgoing transition. A receipt with no transition is an orchestration failure:
do not silently return or ask the user to invoke drive again; emit the
evidence-supported non-success terminal receipt if no valid transition exists.
For an active-drive success receipt, first verify its verbatim
`Outstanding transition` echo, then execute that transition in the same turn.

## Decision owner

Skip decision closure when confirmed source and evidence already support a
Ready spec without a user-owned choice. Otherwise apply `tk-grill-me` with task
identity, current source and evidence, confirmed decisions, and unresolved
user-owned decisions.

`tk-grill-me` alone owns investigation, the four-axis ambiguity ledger,
one-question-at-a-time interaction, closure approval, and its decision receipt.
Drive does not ask the question inline. A
`pending | aborted | Blocked | Unverifiable` receipt stops downstream
handoffs. A `confirmed` receipt returns cited decisions to drive without
writing an artifact or invoking another phase.

Approval is granular to the exact axis asked. A premise embedded in an option
explanation is not confirmed by selecting that option; label it unconfirmed or
route it as a separate decision.

When spec or ticket work discovers a new user-owned decision, the phase owner
returns `User decision: required` in its native non-success receipt to drive.
Drive invokes `tk-grill-me`; after confirmation it re-runs `tk-to-spec` to
`Ready` before rederiving or resuming tickets. If the same or equivalent
decision blocker recurs after that confirmation, stop `Blocked` instead of
automatically routing it again. Phase owners never invoke one another.

## Spec owner

Apply `tk-to-spec` on every active drive run with the confirmed source and
decisions before any ticket decision or implementation.
There is no small-task exception; size, proportionality, and a single-slice
shape affect only the ticket decision after `Ready`. The spec owner alone owns
the source map, stable R/AC IDs, Ready gate, spec write/print behavior, and UI
writing inventory.
Drive records its receipt and does not repair a non-Ready spec inline. A
decision-related non-Ready receipt returns to drive's decision owner; all other
non-Ready states stop at the spec phase.

For a material profile, give the spec owner its evidence and obligations as
verification input. The spec owner decides how they map to R/AC and
verifiability inside its existing contract; drive does not write those
requirements or accept a Ready spec that silently omits a material obligation.

## Ticket decision and owner

Drive decides whether tickets are justified: use them only for at least two
independently verifiable vertical slices or when a long-running/resumable task
materially benefits from a ledger. Otherwise pass the Ready spec to
implementation as one unit.

When tickets are justified, apply `tk-to-tickets`. It alone owns vertical
decomposition, ticket IDs, source coverage, dependencies, corrective-ticket
shape, and ledger writes. Keep at most one ticket `in_progress`. Status text is
not evidence; only a matching implementation receipt can make a ticket
`verified`. A decision-related non-success receipt returns to drive, which must
restore a Ready spec before asking tickets to derive again.

Signal count, obligation count, or a risk label never justifies a ticket
ledger. The existing independent-slice/material-ledger rule remains the only
ticket decision.

## Prototype

Use a disposable web branch only when unresolved visual choices affect behavior
or structure and side-by-side evidence will reduce the pending decision. Keep
the same content, data, and state across 2–3 meaningful alternatives. Do not
add an option without distinct decision value or prototype a choice that
repository evidence already resolves.

## Implementation owner

Apply `tk-implement` once per selected ticket, or once for a no-ticket
single-slice spec. It alone owns direct/delegated strategy, TDD/no-TDD,
production-behavior tests, existing coverage gates, testless exceptions,
focused and affected verification, ticket-level Standards/Spec review,
staging, and one current-branch commit.

Before the next handoff, confirm the receipt's unit/ticket ID, commit SHA,
branch, ancestry, R/AC evidence, and unchanged ownership boundary. Never ask
`tk-implement` to batch tickets, and never create a separate drive commit.

Pass the frozen material profile to each affected unit. `tk-implement` owns the
exact supported regression seam, compatibility scope, side-effect/recovery
evidence, browser handoff, and bounded independent-review method. It must
return its native non-success state rather than recompute signals, drop an
obligation, or perform work owned by a sibling phase.

For visible UI or browser behavior, `tk-implement` owns the required
`tk-browser-verify` gate. Drive aggregates returned literal/rendered evidence
without selecting browser tools itself.

## Aggregate verification and review

After all units are committed:

- verify every R/AC ID is covered by a unit receipt and commit;
- verify commit ancestry and current `HEAD` match the ordered unit receipts;
- reconcile every frozen material obligation with unit and broad verification
  evidence; a missing or unverifiable obligation prevents aggregate `Pass`;
- inspect cross-ticket interfaces, cumulative side effects, and uncovered
  scope without repeating each ticket's line-level code review;
- run the broadest executable relevant tests, build, integration, and browser
  verification once;
- classify failure as `change-related`, `pre-existing`, `environment`, or
  `unverifiable`.

Freeze the successful product verification HEAD before reflection. A later
tracked reflection commit changes final HEAD but never the product verification
evidence; ignored/local reflection leaves both HEAD values equal.

High-risk cumulative effects may require broader verification before an
individual unit commit through `tk-implement`; the final aggregate gate still
runs once.

## Corrective cycle

On a final change-related failure, isolate the affected R/AC and root cause. If
it forms one independently verifiable unit, apply `tk-to-tickets` to append one
corrective ticket, then apply `tk-implement` once and rerun aggregate
verification once.

Do not create a corrective ticket for pre-existing, environment, or
unverifiable failures. Do not amend, squash, force-push, or silently rewrite
verified commits. A repeated failure, unisolated cause, or second requested
cycle ends in the one concrete terminal state supported by current evidence.

## Reflection tail

After aggregate product verification (including one successful corrective
cycle when used) is `Pass`, hand off exactly once to `tk-reflect`:

```text
Mode: drive-optimistic
Success state: Pass
Outstanding transition: final receipt
Return to: tk-drive
```

The handoff cites task identity, product verification HEAD, implementation
ledger, spec/tickets, ordered commits, aggregate evidence, branch, initial
HEAD, and pre-existing dirty ownership. `tk-reflect` alone owns prevention
classification, eligibility, rule mutation/rollback, skill promotion packets,
and `.tigerkit/reflect.md`.

Accept success only with `Status: Pass`, `Return to: tk-drive`, and the
verbatim `Outstanding transition: final receipt` echo, then emit the final
receipt in the same turn. A no-op is successful and omitted from user output.
A verified-restored reflection failure is reported but preserves product
`Pass`; target drift, failed restoration, out-of-scope mutation, or an
indeterminate workspace ends `Blocked | Unverifiable`.

Never enter this tail for `Fail | Blocked | Unverifiable` product verification,
call it twice, invoke `tk-learn`, auto-promote a skill, or let reflection touch
product/source paths.

## Final receipt

Report source identity, phase receipts, ticket states, ordered
ticket/unit-to-commit mapping, broad verification, integration review, actual
branch and `HEAD`, remaining risks, and reusable-candidate existence. Do not
repeat child evidence or automatically invoke another reflection, handoff,
release, or publish action. User-facing prose follows the user's language;
canonical fields and status tokens remain unchanged.

Mention the verification profile only when it materially changed executed
verification or leaves meaningful residual risk. Omit baseline/no-op profile
details and never print an all-default signal checklist.
