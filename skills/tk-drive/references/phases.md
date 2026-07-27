# Phase invariants

These are orchestration gates. Semantic phase behavior belongs to
`tk-to-spec`, `tk-to-tickets`, and `tk-implement`; drive consumes their
receipts and never recreates a failed or unavailable phase inline.

## Preflight and source

- Resolve branch, initial `HEAD`, pre-existing dirty paths, and ownership
  before mutation.
- Source precedence is: latest explicit drive input, confirmed
  same-conversation decisions, relevant current spec, relevant current
  tickets, repository instructions, code/tests.
- Adopt existing artifacts only when task identity and current evidence match.
  Revalidate completed phases and skip them only when their owner skill's
  current contract still passes.
- When a new decision invalidates downstream tickets, replace or remove the
  stale artifact without archives. Ask only when task identity or decision
  reversal cannot be established.
- Treat `/tk-drive`, `$tk-drive`, and picker-equivalent direct selection as
  host-native explicit starts. Do not bind explicit start to one host syntax.

## Phase handoff envelope

Every handoff records phase, task identity, source/artifact paths, stable R/AC
or ticket IDs, branch, initial/current `HEAD`, ownership, and the success state
needed to continue. Each owner keeps its native receipt; drive maps only the
minimal continuation state and does not create a shared runtime contract.

- Spec continues only from `tk-to-spec` `Ready`.
- Tickets continue only from a successfully written and revalidated
  `tk-to-tickets` ledger.
- Implementation continues only from a `tk-implement` `Pass` receipt with the
  expected unit/ticket ID and commit SHA.
- `Draft`, `Pending`, `Blocked`, `Fail`, `Unverifiable`, unavailable skills,
  stale evidence, or mismatched IDs stop drive at that phase.

The user's answer to the directly corresponding pending decision updates the
source and resumes that phase. No other response inherits drive authority.

## Spec owner

Apply `tk-to-spec` with the confirmed source and decisions. It alone owns the
source map, stable R/AC IDs, Ready gate, spec write/print behavior, and UI
writing inventory. Drive records its receipt and does not repair a non-Ready
spec inline.

## Ticket decision and owner

Drive decides whether tickets are justified: use them only for at least two
independently verifiable vertical slices or when a long-running/resumable task
materially benefits from a ledger. Otherwise pass the Ready spec to
implementation as one unit.

When tickets are justified, apply `tk-to-tickets`. It alone owns vertical
decomposition, ticket IDs, source coverage, dependencies, corrective-ticket
shape, and ledger writes. Keep at most one ticket `in_progress`. Status text is
not evidence; only a matching implementation receipt can make a ticket
`verified`.

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
