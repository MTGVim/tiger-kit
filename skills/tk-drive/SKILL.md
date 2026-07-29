---
name: tk-drive
description: "[user] Orchestrate an explicitly started source through conditional decision closure and the canonical spec, ticket, and implementation phase owners to verified ticket-level commits. Use only when selected explicitly; an active invocation may continue after its child phase returns."
disable-model-invocation: true
argument-hint: "<source, request, issue, spec, or tickets>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Drive

Start only when the user selects `/tk-drive`, `$tk-drive`, or the host skill
picker. Within that conversation, keep ownership across the directly
corresponding child answer and continuation receipt; a success receipt advances
to the next required phase in the same turn.

An ordinary request, generic `continue`, artifact presence, unrelated answer,
new session, or broken conversation is not a start or resume. A new session
requires a fresh explicit start and reconstruction from repository evidence.

## Contract

An explicit start authorizes planning, ticket-level implementation,
verification, review, and verified current-branch unit commits within the
current source scope. It does not authorize push, PR, merge, tag, release,
publish, automatic reflection, history rewriting, or out-of-scope mutation.

Prefer the latest explicit source and revalidate artifacts as defined by the
phase invariants. Do not create drive-only or global state.

Follow [phase invariants](references/phases.md). Drive owns orchestration;
`tk-grill-me`, `tk-to-spec`, `tk-to-tickets`, and `tk-implement` respectively
own decision closure, spec, ticket decomposition, and one implementation unit.
`tk-to-spec` is mandatory on every active drive run before the ticket decision
or implementation. There is no small-task exception; task size and
proportionality affect only whether a ticket ledger is justified.

Invoke only owners allowed by the phase invariants. Propagate an unavailable or
unsuccessful phase and never recreate it inline. Before each handoff, record
`Success state` and one `Outstanding transition`; success must echo
`Return to: tk-drive` and that transition verbatim. A missing or mismatched echo
is receipt drift and `Blocked`; a valid success triggers its same-turn
transition.

### 🔴 HARD GATE · source UI writing

For every string literal rendered in UI, freeze an inventory before spec
mutation; labels, copy, numbers, units, currency, suffixes, and separators are
examples, not an upper bound. Map source location, non-empty source literal,
current rendered/source-path literal, target literal, spec R/AC, optional
ticket, and implementation destination.

Missing source/current evidence is `Unverifiable`. Any source↔current mismatch
makes every row a conflict candidate and prevents `Ready`, `Pass`, or commit without
a user decision. A typo requires rechecking all same-kind tokens; never generalize
source unreliability to adopt current code silently.

Approval covers only the asked axis; option premises remain unconfirmed. Only exact
separately approved wording is an `authorized change`; prohibit all other drift.

Compare the inventory exactly through spec, tickets, implementation,
candidate/staged diff, and rendered UI; drift or evidence gaps block commit.

## Workflow

1. `preflight`: resolve the complete source per phase invariants, relevant
   artifacts/instructions, Git and dirty ownership, task identity, completed
   phases, and unresolved decisions.
2. `decision phase`: when any unresolved user-owned decision prevents a Ready
   spec, explicitly hand current source, evidence, confirmed decisions, and
   open decisions to `tk-grill-me`. Skip this phase when the source is already
   sufficient. Continue only from its `confirmed` receipt.
3. `spec phase`: explicitly hand current source, confirmed decisions, and
   traceability to `tk-to-spec`; accept only a `Ready` receipt, then make the
   ticket decision in the same active turn. Run this phase for every task,
   including trivial and single-slice work.
4. `ticket decision`: use `tk-to-tickets` only for at least two independent
   vertical slices or material ledger value. Otherwise create no ticket/ledger
   and carry task identity plus Ready R/AC as one no-ticket unit.
5. `prototype branch`: only when unresolved web visual ambiguity affects
   behavior or structure and 2–3 disposable alternatives materially narrow
   one decision.
6. `implementation commits`: keep at most one ticket `in_progress`; hand one
   ticket and its R/AC, or the one no-ticket unit, to `tk-implement`. Mark it
   `verified` only from the matching verified commit receipt, then hand off the
   next unit or enter aggregate verification.
7. `aggregate verification`: reconcile all unit receipts, commit ancestry,
   R/AC coverage, and cross-ticket interaction; run the broadest executable
   relevant verification once. Do not repeat each ticket's line-level
   Standards/Spec review.
8. `corrective cycle/report`: for one isolated final change-related regression,
   create at most one corrective ticket through `tk-to-tickets`, run
   `tk-implement` once, and rerun broad verification once. Otherwise stop
   mutating and produce the final receipt.

At any downstream phase, only a native receipt with
`User decision: required` and a newly identified user-owned decision returns
control to drive. Hand it to `tk-grill-me`; after `confirmed`, re-run
`tk-to-spec` to `Ready` before tickets. A repeated or equivalent blocker after
that confirmation is `Blocked`, not another automatic loop.

## 🔴 CHECKPOINT · 🛑 STOP · decision handoff

Drive does not reproduce grill questions. A non-confirmed grill receipt stops;
`confirmed` merges only cited Decisions and resumes at the spec gate. An
unrelated answer gains no commit authority and requires a new explicit start.

## Failure and completion

Missing source/authority, receipt drift, or a decision that cannot be routed is
`Blocked`. A child verification or commit failure is `Fail`; inaccessible
evidence is `Unverifiable`. Preserve valid diffs and verified commits, stop the
next handoff, and never rewrite history. Only an isolated final
change-related regression permits the one corrective cycle defined in the
phase invariants.

Lead the final response with a compact receipt starting `Outcome: <one user-facing sentence>`. `Status` and `Source` are required.
Include `Phases`, `Tickets`,
`Verification`, `Integration review`, `Commits`, `Remaining risks`, and
`Reusable candidate` only when they contain decision-relevant or non-default
information. Omit skipped phases, no-ticket placeholders, empty risks, and an
absent reusable candidate. Use `Status: Pass` only after every completion gate.

For multiple tickets, place a compact `Ticket | Outcome | Commit` table before the receipt. Use a sentence when only one user-relevant row exists; rows are vertical slices, never phases/files/commands, and Receipt's Outcome summarizes them without repeating rows.

Return control only with that final receipt or an explicit phase-stop receipt;
first assert that every consumed success receipt has its next transition.
Reference child receipts instead of copying their evidence, and never expose a
child handoff envelope or invoke `tk-reflect`.

Write user-facing progress updates and the final receipt in the user's language,
while preserving canonical status and receipt field names.

## User decision questions

When a user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`. This changes presentation, not authority or stop gates.
