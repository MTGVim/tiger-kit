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

The latest explicit source outranks scratch artifacts. Ignore unrelated
artifacts and revalidate stale spec or ticket artifacts against current
evidence. Ask only when task identity or decision reversal cannot be resolved.
Do not create drive-only state, current pointers, archives, global state, or
automatic migration.

Follow [phase invariants](references/phases.md). Drive owns orchestration;
`tk-grill-me`, `tk-to-spec`, `tk-to-tickets`, and `tk-implement` respectively
own decision closure, spec, ticket decomposition, and one implementation unit.

The phase-owner allowlist is
`tk-grill-me | tk-to-spec | tk-to-tickets | tk-implement`. The conditional
support allowlist is
`tk-prototype | tk-browser-verify | tk-merge-conflict`. Do not invoke other
planning, learning, reflection, or handoff skills, and do not create a shared
runtime contract.

If a phase skill is unavailable or does not return its required success
receipt, propagate that state and stop at the phase. Never recreate its
semantics inline. Do not intercept a standalone phase request, and do not let a
phase owner take over drive-wide orchestration, aggregate verification, or the
final receipt.

### 🔴 HARD GATE · source UI writing

If user-provided source contains a label, button, heading, guide/help copy,
table or column name, placeholder, validation/error, or status text, freeze an
inventory before spec mutation. Map source location, exact literal, spec R/AC,
optional ticket, and implementation destination.

Unless the user explicitly approves a wording change, prohibit translation,
paraphrase, shortening, correction, typo fixes, and normalization. Mark only
approved changes as `authorized change`. An unreadable literal is
`Unverifiable`; conflicting literals that require a user choice are `Blocked`.

Compare the same inventory exactly in the spec, tickets, implementation,
candidate/staged diff, and rendered UI. Do not commit when any unauthorized
drift or exact-comparison evidence gap remains.

## Workflow

1. `preflight`: resolve source, relevant spec/tickets, repository instructions,
   branch, initial `HEAD`, dirty ownership, drift, task identity, completed
   phases, and unresolved decisions.
2. `decision phase`: when any unresolved user-owned decision prevents a Ready
   spec, explicitly hand current source, evidence, confirmed decisions, and
   open decisions to `tk-grill-me`. Skip this phase when the source is already
   sufficient. Continue only from its `confirmed` receipt.
3. `spec phase`: explicitly hand current source, confirmed decisions, and
   traceability to `tk-to-spec`; accept only a `Ready` receipt.
4. `ticket decision`: hand the Ready spec to `tk-to-tickets` only when there
   are at least two independently verifiable vertical slices or a ledger adds
   material long-resume value. Otherwise use one no-ticket implementation unit.
5. `prototype branch`: only when unresolved web visual ambiguity affects
   behavior or structure and 2–3 disposable alternatives materially narrow
   one decision.
6. `implementation commits`: keep at most one ticket `in_progress`; hand one
   ticket and its R/AC, or the one no-ticket unit, to `tk-implement`. Mark it
   `verified` only from the matching verified commit receipt, then continue.
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

Write user-facing progress updates and the final receipt in the user's language,
while preserving canonical status and receipt field names.

## DO NOT / ANTI-PATTERNS

- Do not start from an ordinary request, artifact, or generic continuation.
- Do not extend commit authority from an unrelated answer, force tickets for a
  small slice, or trust stale ticket status.
- Do not duplicate or bypass phase-owner semantics.
- Do not ask grill questions inline, let spec or tickets invoke grill, or resume
  downstream artifacts without revalidating the Ready spec.
- Do not stage/commit source, repeat ticket-level review, rewrite verified
  commits, run a second corrective cycle, or invoke skills outside allowlists.
