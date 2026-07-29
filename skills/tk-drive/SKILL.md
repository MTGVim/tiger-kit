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

Start a workflow only when the user explicitly selects `tk-drive` in the
current host. `/tk-drive`, `$tk-drive`, and direct selection in a host skill
picker are equivalent explicit starts. Once started, keep ownership while a
child phase waits for and incorporates the directly corresponding answer; when
that phase returns a continuation receipt, resume without another invocation.
A continuation receipt is an internal transition, not a terminal response:
when it carries no stop state, advance to the next required phase in the same
turn instead of ending after the child receipt.

An ordinary code request, generic `continue`, an existing `.tigerkit/`
artifact, an answer outside an active child phase, a new session, or a broken
conversation is not a start or resume. Leave ordinary implementation with the
current agent. In a new session, require a new explicit `$tk-drive` start and
reconstruct phases from repository evidence.

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

Invoke only the phase and support owners allowed by the phase invariants; do
not create a shared runtime contract.

If a phase skill is unavailable or unsuccessful, propagate that state and stop
at the phase; never recreate its semantics inline.

Every consumed phase receipt must cause one same-turn transition defined in the
phase invariants. A child success receipt is never a response boundary.

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
   ticket decision in the same active turn.
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

## 🔴 CHECKPOINT · 🛑 STOP · decision handoff and resume

Drive does not ask or reproduce grill questions. A `tk-grill-me`
`pending | aborted | Blocked | Unverifiable` receipt stops downstream handoffs
and preserves the active phase evidence. When grill returns `confirmed`, merge
only its cited Decisions into source traceability and resume at the spec gate.
If the user's answer adds unrelated scope or does not correspond to the active
grill decision, do not inherit commit authority; report the drift or require a
new explicit `$tk-drive` start.

## Failure and completion

Missing source/authority, receipt drift, or a decision that cannot be routed is
`Blocked`. A child verification or commit failure is `Fail`; inaccessible
evidence is `Unverifiable`. Preserve valid diffs and verified commits, stop the
next handoff, and never rewrite history. Only an isolated final
change-related regression permits the one corrective cycle defined in the
phase invariants.

The final receipt owns `Status`, `Source`, `Phases`, `Tickets`,
`Verification`, `Integration review`, `Commits`, `Remaining risks`, and
`Reusable candidate`. Use `Status: Pass` only after every completion gate. Do
not duplicate child evidence or invoke `tk-reflect`.

Return control only with that final receipt or an explicit phase-stop receipt;
first assert that every consumed success receipt has its next transition.

Write user-facing progress updates and the final receipt in the user's language,
while preserving canonical status and receipt field names.

## User decision questions

When this skill reaches a user-owned decision, ask exactly one question at a
time. Render `Question` before `Recommendation` and the proposals. Offer
two or three mutually exclusive proposals and state the material tradeoff of
each. Make `Question` self-contained: summarize the
evidence-derived context, decision impact, and unresolved axis in user-facing
language before asking. It must not require the user to decode raw `Evidence`.
Mark exactly one best recommendation by ending its label with a localized marker such as
`(Recommended)` or `(추천)`. A host-generated custom or Other choice does not
count as an authored proposal.

When the active question tool exposes
option previews, prototype cards, or equivalent rich choice surfaces and a concrete preview can clarify the
decision, use it proactively. Do not invent unsupported fields or use this
presentation rule to bypass existing prototype or phase boundaries.

If the current execution context exposes a native structured user-input tool,
the skill must call that tool. Plain-text questions are allowed only when no
such tool is exposed. A failed or rejected tool call is not tool absence: report
the failure and preserve the pending or blocked state instead of silently
downgrading to prose. Host examples:

- Claude Code: `AskUserQuestion`
- Codex: `request_user_input`
- Hermes Agent: `clarify`

This contract changes question presentation only. It does not grant new
decision authority or weaken any existing stop, approval, or phase boundary.

## DO NOT / ANTI-PATTERNS

- Do not start from an ordinary request, artifact, or generic continuation.
- Do not extend commit authority from an unrelated answer, force tickets for a
  small slice, or trust stale ticket status.
- Do not duplicate or bypass phase-owner semantics.
- Do not ask grill questions inline, let spec or tickets invoke grill, or resume
  downstream artifacts without revalidating the Ready spec.
- Do not stage/commit source, repeat ticket-level review, rewrite verified
  commits, run a second corrective cycle, or invoke skills outside allowlists.
- Do not stop after a child success receipt; continue or emit an explicit
  terminal reason in the same turn.
