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

Use only for an explicit vertical-ticket decomposition request or an exact active
`tk-drive` handoff containing a Ready source and the decision that tickets are
needed. Do not write the spec, publish remote issues, or implement.

Source precedence is user-designated source, current confirmed decisions,
`.tigerkit/spec.md`, the request, then relevant code.

## Workflow

1. **Extract** — collect source R/AC IDs or source locations and classify them
   `confirmed | unverified | conflict`.
2. **Slice** — derive user-visible vertical behaviors. Treat spec candidate areas
   as evidence, not preapproved slices or ticket IDs.
3. **Prove independence** — each ticket must have an independently observable
   goal, scope, acceptance criteria, verification, and supported entry points.
4. **Map** — cover every source ID, record predecessors, coupling, and unresolved
   split problems.
5. **Gate** — return writable tickets or
   `Unresolved split report | Blocked | Unverifiable`.
6. **Write and verify** — atomically write the ledger, reread it, and verify
   coverage, dependencies, and ticket contents.

## Ticket contract

Each ticket begins `Status: pending` and is executable from the artifact and its
cited sources without hidden conversation context. Preserve R/AC IDs; when none
exist, cite source locations rather than inventing IDs.

A ticket is a vertical behavior unit: keep behavior, tests, and verification
together. Do not split into type/API/UI/test layers or diagnose/fix/verify
stages. Keep one bug as one slice from reproduction through root-cause fix,
regression seam, original reproduction, and cleanup.

This skill alone assigns ticket IDs and owns ticket shape, coverage,
dependencies, mutable status, commit receipts, and resume state. It does not
re-own whether a ledger is needed.

| State | Meaning |
| --- | --- |
| `Unresolved split report` | Evidence cannot support independent boundaries |
| `Blocked` | Confirmed conflict, missing decision, or post-checkpoint drift |
| `Unverifiable` | Required source access or traceability evidence is unavailable |
| `Fail` | Writing or post-write validation produced a known invalid result |

Do not write from `Draft | Blocked | Unverifiable`. On active-drive non-success,
pass native state, exact evidence, and `User decision: required | none` directly
to the graph; do not invoke `tk-grill-me` or edit the Ready spec.

## Failed-attempt ownership

Preserve completed receipts and unrelated pending tickets. When an exact ledger
and current incomplete ticket exist, `tk-drive non-success finalization` is the
sole downstream writer for bounded `Last attempt`, `Evidence`, and `Recovery`
fields. It never invokes this skill again. `Dependency blocked`, `Not attempted`,
and `Unverified` are terminal presentation classifications, not durable ticket
statuses.

## Source UI writing

When source or the Ready spec defines rendered text, freeze source location,
source literal, current rendered/source-path literal, target literal, R/AC, and
owning ticket before decomposition. Preserve exact spelling, case, spacing,
punctuation, symbols, numbers, units, and meaningful line breaks unless wording
change is explicitly authorized.

Missing source/current evidence is `Unverifiable`; source↔current mismatch is a
conflict and prevents handoff. Mark only approved wording as `authorized change`.
Do not translate, paraphrase, normalize, or silently fix typos.

## Output

Write to `--output` or atomically replace `.tigerkit/tickets.md`. Create parents
lazily, do not archive, do not modify `.gitignore`, and never publish remotely.

User-facing output uses the ticket table when multiple or one result sentence
when singular; the artifact owns ticket bodies, status, coverage, dependencies,
evidence, and unresolved split detail. For multiple tickets, use
`Ticket | User-visible slice`. Use a sentence when only one user-relevant row
exists. Show two to seven tickets; for more, show the top five to seven, include
a compact coverage/blocker summary, and cite the ledger. Active prep receives
only the internal path, ticket IDs, coverage, and state handoff.

### 🔴 HARD GATE · terminal user summary

Keep progress and internal procedure evidence out of the terminal user response.
Begin with the canonical result heading or sentence. Emit no ceremonial
preamble, receipt heading, `Outcome:` label, duplicate status, or active-drive
child summary. Put detailed provenance only in the owned tickets artifact.

### 🔴 HARD GATE · response language

Use the latest explicit user language, otherwise the current message's language.
Preserve canonical headings, status tokens, IDs, commands, paths, code, and
quoted source literals exactly. Rewrite free-form language drift before return.

## User decision questions

Ask one self-contained `Question` only for a material user-owned decision, then
show a `Recommendation`, two or three mutually exclusive options, and exactly
one `(Recommended)` or `(추천)` label. Use native `AskUserQuestion`, Codex
`request_user_input`, or Hermes Agent `clarify`; plain text is allowed only when
none is exposed. A failed or rejected call is not absence; preserve
`Pending | Blocked`.

## Pitfalls

- Do not force non-independent work into separate tickets.
- Do not invent exact paths, code, IDs, or unsupported performance numbers.
- Do not alter source UI writing or hide essential context.
- Do not implement, publish, or repair a non-success state inline.
