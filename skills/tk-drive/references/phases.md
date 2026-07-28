# Phase invariants

These are orchestration gates. Semantic phase behavior belongs to
`tk-grill-me`, `tk-to-spec`, `tk-to-tickets`, and `tk-implement`; drive
consumes their receipts and never recreates a failed or unavailable phase
inline.

## Preflight and source

- Resolve branch, initial `HEAD`, pre-existing dirty paths, and ownership
  before mutation.
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

## Phase handoff envelope

Every handoff records phase, task identity, source/artifact paths, stable R/AC
or ticket IDs, branch, initial/current `HEAD`, ownership, and the success state
needed to continue. Each owner keeps its native receipt; drive maps only the
minimal continuation state and does not create a shared runtime contract.

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

When spec or ticket work discovers a new user-owned decision, the phase owner
returns `User decision: required` in its native non-success receipt to drive.
Drive invokes `tk-grill-me`; after confirmation it re-runs `tk-to-spec` to
`Ready` before rederiving or resuming tickets. If the same or equivalent
decision blocker recurs after that confirmation, stop `Blocked` instead of
automatically routing it again. Phase owners never invoke one another.

## Spec owner

Apply `tk-to-spec` with the confirmed source and decisions. It alone owns the
source map, stable R/AC IDs, Ready gate, spec write/print behavior, and UI
writing inventory. Drive records its receipt and does not repair a non-Ready
spec inline. A decision-related non-Ready receipt returns to drive's decision
owner; all other non-Ready states stop at the spec phase.

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

For visible UI or browser behavior, `tk-implement` owns the required
`tk-browser-verify` gate. Drive aggregates returned literal/rendered evidence
without selecting browser tools itself.

## Aggregate verification and review

After all units are committed:

- verify every R/AC ID is covered by a unit receipt and commit;
- verify commit ancestry and current `HEAD` match the ordered unit receipts;
- inspect cross-ticket interfaces, cumulative side effects, and uncovered
  scope without repeating each ticket's line-level code review;
- run the broadest executable relevant tests, build, integration, and browser
  verification once;
- classify failure as `change-related`, `pre-existing`, `environment`, or
  `unverifiable`.

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

## Final receipt

Report source identity, phase receipts, ticket states, ordered
ticket/unit-to-commit mapping, broad verification, integration review, actual
branch and `HEAD`, remaining risks, and reusable-candidate existence. Do not
repeat child evidence or automatically invoke reflection, handoff, release, or
publish actions. User-facing prose follows the user's language; canonical
fields and status tokens remain unchanged.
