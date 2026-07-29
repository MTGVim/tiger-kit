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
proceed to implementation. Return `Phase: tickets`, path, `Status: Pass` after
successful write/revalidation, ticket IDs, and source R/AC coverage. An active
drive handoff also supplies `Success state` and `Outstanding transition`. On
`Pass`, include `Return to: tk-drive` and echo the parent-supplied
`Outstanding transition` verbatim without choosing or executing it. A missing
or mismatched `Success state` or transition cannot produce a successful
active-drive receipt; return `Blocked`.

When an active-drive handoff exposes a missing user decision, return the native
non-success receipt to drive. Do not invoke `tk-grill-me` or edit the Ready
spec; drive alone routes decision closure and requires a revalidated Ready spec
before retrying tickets. Include `User decision: required | none`; `required`
cites the new decision and source evidence.

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

Each ticket must be executable from the artifact and its cited sources without
hidden conversation context. Name only evidence-supported entry points, and
include runnable verification with expected evidence; never invent exact paths
or code.

### Vertical-slice boundaries

Keep behavior and its tests in the same ticket; do not create horizontal
type/API/UI/test-only tickets. If evidence cannot support independent slices,
return `Unresolved split report`. Classify unsupported requirements or
unresolved conflicts as `Blocked` or `Unverifiable`. The receipt records phase,
path, status, ticket IDs/count, then references coverage, dependencies,
evidence, unverified items, and unresolved split sections without restating
their content.

Keep one bug as one vertical slice from reproduction through root-cause fix,
regression seam, original reproduction, and cleanup. Do not split it into
UI/API/test or diagnose/fix/verify layers. From a Ready spec, cover every R/AC.
Do not write from `Draft | Blocked | Unverifiable`.

### 🔴 HARD GATE · source UI writing

For every string literal rendered in UI by user source or the Ready spec,
freeze a separate inventory before decomposition. Labels, copy, numbers,
units, currency, suffixes, and separators are examples, not an upper bound.
Each row maps source location, non-empty source literal, current
rendered/source-path literal, target literal, existing R/AC, and owning ticket.

Missing source/current evidence is `Unverifiable`. Any source↔current mismatch
makes every row a conflict candidate and prevents handoff without a user
decision. A typo requires rechecking all same-kind tokens; never generalize
source unreliability to adopt current code silently.

Unless the user explicitly decides to change wording, preserve spelling, case,
spacing, punctuation, symbols, numbers, and meaningful line breaks. Do not
translate, paraphrase, shorten, correct, fix typos, or normalize.

After write, compare all three literal columns against coverage and actual
ticket acceptance/verification. Unauthorized drift or missing comparison
evidence prevents completion and implementation handoff. Mark only approved
wording as `authorized change`.

## CHECKPOINT / STOP

Before writing, cold-start each ticket against only the artifact and its cited
sources, then check decomposition evidence, source traceability, unresolved
conflicts, and UI-writing inventory. When essential context is hidden or
evidence is insufficient, or an exact UI literal cannot be compared, do not
create or overwrite tickets; return `Unresolved split report`, `Blocked`, or
`Unverifiable`.

Write user-facing progress and receipt prose in the user's language. Preserve
canonical status tokens, IDs, and receipt keys.

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
