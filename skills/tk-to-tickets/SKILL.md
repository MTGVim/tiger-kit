---
name: tk-to-tickets
description: "[user/auto] Decompose a request or Ready spec into independently verifiable vertical tickets. Apply to a clear standalone decomposition request or an explicit ticket handoff from active tk-drive; do not apply to spec writing, remote issue creation, or implementation."
argument-hint: "<spec, plan, or request> [--output <path>]"
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: to-tickets
    relationship: adapted
---

# Write tickets

Use for explicit invocation, a clear natural-language request for vertical
ticket decomposition, or an explicit handoff in which active `tk-drive`
provides a Ready spec and ticket-decision evidence. Do not auto-activate from
spec writing, remote issue creation, implementation, artifact presence, or
merely because drive is active.

Source precedence is: user-designated source, current conversation,
`.tigerkit/spec.md`, request, relevant code.

Standalone and drive handoff use the same vertical-slice contract. Drive
decides whether tickets are needed; this skill does not re-own that decision or
proceed to implementation. Return `Phase: tickets`, path, terminal state,
ticket IDs, and source R/AC coverage.

## Workflow

1. `extract source requirements`: capture requirement/acceptance IDs, source
   locations, and `confirmed | unverified | conflict`.
2. `vertical slices`: create candidates with initial `Status: pending`, one
   independent goal, scope, behavior, and tests.
3. `acceptance and verification`: define observable acceptance criteria and
   executable verification commands or evidence.
4. `traceability and dependencies`: map every source ID to ticket coverage,
   predecessor tickets, and unresolved split problems.
5. `checkpoint`: return write permission or
   `Unresolved split report | Blocked | Unverifiable`.
6. `write/verify/receipt`: write only after the checkpoint, then revalidate
   source-ID coverage and dependencies and return the phase receipt.

Write to the user-designated path or `.tigerkit/tickets.md` using
`# <Feature> Tickets`. Under `.tigerkit/`, create the parent only when needed,
prefer a same-directory temporary file plus rename, never create timestamped
archives or modify `.gitignore`, and warn if scratch is not ignored. Do not
implement or publish to a remote tracker.

## Failure paths

| Trigger | Terminal state | Recovery |
|---|---|---|
| No evidence for independent decomposition | `Unresolved split report` | Do not invent tickets; report requirements or dependencies preventing the split |
| Confirmed sources conflict or a user decision is missing | `Blocked` | Identify conflicting IDs and one needed decision; do not write |
| Required source access prevents traceability | `Unverifiable` | Record inaccessible path, error, and affected IDs; do not write |
| Source ID/status or target changes after checkpoint | `Blocked` | Preserve the target and rerun checkpoint with new evidence |
| Write/rename fails | `Fail` | Preserve the intact target and precisely restore/revalidate only this run's changes |
| Post-write coverage, UI literal, or dependency mismatches | Use the one supported state: `Fail` for a known invalid output, `Unverifiable` when evidence cannot establish validity | Do not report completion; stop further writes and record actual state |

After write/rename, reread the file and confirm every source ID maps to the
coverage table and actual tickets and that dependencies match the candidate.
Do not substitute terminal states for one another.

## Contract

### Ticket shape and traceability

Preserve source traceability per requirement. Each ticket begins
`Status: pending` and is a vertical behavior unit with an independent goal,
scope, acceptance criteria, and verification. Standalone execution does not
infer implementation progress. Preserve source R/AC IDs in each ticket and in
the coverage table. Without source IDs, cite source location and do not invent
IDs.

### Vertical-slice boundaries

Keep behavior and its tests in the same ticket; do not create horizontal
type/API/UI/test-only tickets. If evidence cannot support independent slices,
return `Unresolved split report`. Classify unsupported requirements or
unresolved conflicts as `Blocked` or `Unverifiable`. The receipt includes path,
status, ticket count, source-ID traceability, dependencies, evidence,
unverified items, and unresolved split problems.

Keep one bug as one vertical slice from reproduction through root-cause fix,
regression seam, original reproduction, and cleanup. Do not split it into
UI/API/test or diagnose/fix/verify layers. From a Ready spec, cover every R/AC.
Do not write from `Draft | Blocked | Unverifiable`.

### 🔴 HARD GATE · source UI writing

When user-provided source or the Ready spec contains UI writing, freeze a
separate inventory before decomposition. Map every label, button, heading,
guide/help copy, table or column name, placeholder, validation/error, and
status text from source location and existing R/AC to its owning ticket,
preserving the exact literal.

Unless the user explicitly decides to change wording, preserve spelling, case,
spacing, punctuation, symbols, numbers, and meaningful line breaks. Do not
translate, paraphrase, shorten, correct, fix typos, or normalize during ticket
writing. If an image literal is unreadable or sources conflict, do not guess;
stop as `Blocked` or `Unverifiable`.

After write, compare every literal against coverage and actual ticket
acceptance/verification. Unauthorized drift or missing comparison evidence
prevents completion and implementation handoff. Mark only approved wording as
`authorized change`.

## CHECKPOINT / STOP

Before writing, check decomposition evidence, source traceability, unresolved
conflicts, and UI-writing inventory. When evidence is insufficient or an exact
UI literal cannot be compared, do not create or overwrite tickets; return
`Unresolved split report`, `Blocked`, or `Unverifiable`.

Write user-facing progress and receipt prose in the user's language. Preserve
canonical status tokens, IDs, and receipt keys.

## DO NOT / ANTI-PATTERNS

- Do not create horizontal type/API/UI/test-only tickets or unsupported
  performance numbers.
- Do not alter source UI writing without approval or call tickets
  implementation-ready without exact comparison.
- Do not freeze unresolved requirements/conflicts as facts or force
  non-independent work into separate tickets.
- Do not bypass `Unresolved split report | Blocked | Unverifiable | Fail`
  inline merely because active drive called this skill.
- Do not write the spec, implement, publish remotely, or create traceability
  from unconfirmed source.
