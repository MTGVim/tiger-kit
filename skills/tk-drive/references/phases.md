# Phase invariants

These are minimal orchestration gates. They do not invoke sibling phase skills.

## Preflight and source

- Resolve branch, initial `HEAD`, pre-existing dirty paths and ownership before mutation.
- Source precedence is: latest explicit drive input, confirmed same-conversation decisions, relevant current spec, relevant current tickets, repository instructions, code/tests.
- Adopt existing artifacts only when task identity and current evidence match. Revalidate completed phases and skip them when valid.
- When a new decision invalidates downstream tickets, replace or remove the stale artifact without archives. Ask only when task identity or a decision reversal cannot be established.

## Spec

A Ready spec has problem, goal, included/excluded scope, confirmed decisions, stable R/AC IDs, verification, source traceability and no unresolved conflict. Missing information is `Draft`; a required decision is `Blocked`; inaccessible essential evidence is `Unverifiable`. Do not proceed to tickets or implementation until Ready.

## Tickets

Create tickets only for at least two independently verifiable vertical slices or when a long-running/resumable task materially benefits from a ledger. Otherwise implement directly from the Ready spec.

Every adopted ticket has one of `pending | in_progress | verified | blocked`, source R/AC coverage and current evidence references. Keep at most one `in_progress`. Revalidate status from current diff and tests on resume; status text alone is not evidence.

## Prototype

Use a disposable web branch only when unresolved visual choices affect behavior or structure and side-by-side evidence will reduce the pending decision. Keep the same content/data/state across 2–3 meaningful alternatives. Do not make a third option without distinct decision value or prototype a choice repository evidence already resolves.

## Implementation and diagnosis

Implement the smallest vertical slice and run focused verification. For unknown-cause bugs, first establish a red-capable loop, minimize, rank falsifiable hypotheses, isolate one variable, patch the evidenced cause, verify a public regression seam when available, rerun the original reproduction and remove instrumentation.

For visible UI, layout, responsive behavior, interaction, navigation, forms, or browser final state, activate `tk-browser-verify` before the first browser tool or verification server. When a design reference defines intent, run its preflight before source mutation; after implementation require runtime interaction and screenshot evidence. A forbidden or unavailable browser contract makes the phase `Unverifiable` and prevents commit.

## Built-in review parity

Before commit, pin the initial fixed point and candidate/staged diff inventory. `small` means no more than 15 files and no more than 800 additions plus deletions; otherwise use bounded large/unknown inspection without putting a raw full diff in current context.

The current agent always reviews Standards and Spec. Standards covers repository rules, correctness, ownership, scope, interfaces, testability and side effects. Spec maps every source R/AC ID to implementation and verification evidence. High-risk or large work may use one independent reviewer total, without editing, fan-out, re-delegation or automatic re-review. Findings require severity, file/line evidence, basis and impact. Allow one fix and one regression verification, then stop. Important findings, drift or uncovered scope prevent commit.

## Commit

Immediately before commit, recheck branch, `HEAD`, ownership, staged inventory and all R/AC evidence. Stage only owned changes. Create exactly one current-branch commit after the whole drive is verified. Never push or publish. On partial failure, keep valid work uncommitted and clean only owned temporary artifacts.
