---
name: tk-to-tickets
description: "[user/auto] Decompose a request or Ready spec into independently verifiable vertical tickets. Apply to a clear standalone decomposition request or an explicit ticket handoff from active tk-drive Preparing; do not apply to spec writing, remote issue creation, or implementation."
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
merely because prep is active.

Source precedence is: user-designated source, current conversation,
`.tigerkit/spec.md`, request, relevant code.

Standalone and prep handoff use the same vertical-slice contract. Prep
decides whether tickets are needed; this skill does not re-own that decision or
proceed to implementation. Return `Phase: tickets`, path, `Status: Pass` after
successful write/revalidation, ticket IDs, and source R/AC coverage. An active
prep handoff also supplies `Success state` and `Outstanding transition`. On
`Pass`, include `Return to: tk-drive` and echo the parent-supplied
`Outstanding transition` verbatim without choosing or executing it. A missing
or mismatched `Success state` or transition cannot produce a successful
active-drive-preparing receipt; return `Blocked`.

When an active-drive-preparing handoff exposes a missing user decision, return the native
non-success receipt to prep. Do not invoke `tk-grill-me` or edit the Ready
spec; prep alone routes decision closure and requires a revalidated Ready spec
before retrying tickets. Include `User decision: required | none`; `required`
cites the new decision and source evidence.

## Workflow

1. `extract source requirements`: capture requirement/acceptance IDs, source
   locations, and `confirmed | unverified | conflict`.
2. `vertical slices`: derive independent behavior slices. Treat Ready-spec
   candidate areas only as source evidence, never as preapproved slices or
   ticket IDs.
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

When a Ready spec has vertical-slicing candidate areas, use their R/AC and
coupling evidence but independently prove slice boundaries. This skill alone
assigns ticket IDs and owns coverage, dependencies, and ticket shape. Mutable
status, commit receipts, and resume state also belong only in tickets.

Each ticket must be executable from the artifact and its cited sources without
hidden conversation context. Name only evidence-supported entry points, and
include runnable verification with expected evidence; never invent exact paths
or code.

### Vertical-slice boundaries

Keep behavior and its tests in the same ticket; do not create horizontal
type/API/UI/test-only tickets. If evidence cannot support independent slices,
return `Status: Blocked` with an `Unresolved split report`. Classify unsupported
requirements or unresolved conflicts as `Blocked` or `Unverifiable`.

User-facing output uses the ticket table when multiple or one result sentence
when singular; the artifact owns ticket bodies, phase, path, status, ticket
IDs/count, coverage, dependencies, evidence, unverified items, and unresolved
split sections. Do not restate that provenance in a bottom metadata block. For
active prep, return required control fields only in the internal handoff.

When more than one ticket is created, place a compact
`Ticket | User-visible slice` table in the terminal summary. Use a sentence
when only one user-relevant row exists. The artifact may index IDs/count but
does not substitute for or repeat the slice rows.
Show two to seven tickets as rows. For eight or more, show the top five to
seven, add a compact coverage or blocker summary, and cite the tickets artifact
path for the complete ledger. These are budgets, not quotas.

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

### 🔴 HARD GATE · terminal user summary

Treat progress commentary, internal handoff envelopes, and the terminal user response as distinct surfaces. Before the first line of every terminal user-facing response, emit exactly one standalone `---` line, then begin immediately with the skill's canonical result heading or result sentence. Do not emit this separator in progress commentary or between a successful phase receipt and the next active-drive phase invocation.

Do not render a receipt heading, `Outcome:` label, or terminal provenance/status block in the user summary. When the host or skill requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. Expose a path, ID, commit, or recovery detail only when it changes user action or the skill's canonical result schema requires it. Keep phase receipts as internal handoff envelopes: when an active parent requires phase, status, IDs, `Return to`, `Success state`, or `Outstanding transition`, return them only to that parent workflow and never echo them in the terminal user summary.

Persist provenance only in an artifact or ledger the skill already owns. A skill without such an owner must not create one solely to store a receipt, and a read-only skill remains read-only. Never require a shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, or summary, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose result value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

When a user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Use native structured input when exposed: Claude Code `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`. Plain text is allowed only
when none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`. This changes presentation, not authority or stop gates.

## DO NOT / ANTI-PATTERNS

- Do not create horizontal type/API/UI/test-only tickets or unsupported
  performance numbers.
- Do not alter source UI writing without approval or call tickets
  implementation-ready without exact comparison.
- Do not freeze unresolved requirements/conflicts as facts or force
  non-independent work into separate tickets.
- Do not bypass `Unresolved split report | Blocked | Unverifiable | Fail`
  inline merely because active prep called this skill.
- Do not write the spec, implement, publish remotely, or create traceability
  from unconfirmed source.
