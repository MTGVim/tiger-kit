---
name: tk-to-spec
description: "[user/auto] Turn confirmed decisions and evidence into a Ready implementation spec. Apply to an explicit standalone spec-artifact request or an explicit spec handoff from active tk-drive; do not apply to ticket decomposition, interviews, remote issues, or implementation requests."
argument-hint: "<conversation, source, or request> [--output <path>|--print-only]"
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: to-spec
    relationship: adapted
---

# Write a spec

Use for explicit invocation, a clear natural-language request for an
implementation spec artifact, or an explicit spec handoff in which active
`tk-drive` provides current source and decisions. Do not auto-activate from
ticket decomposition, an interview, remote issue creation, an implementation
request, artifact presence, or merely because drive is active.

Source precedence is: user-designated source, current decisions,
tickets/documents, relevant code, existing `.tigerkit/spec.md`. Do not start an
interview, create tickets, publish, or implement.

When an active-drive handoff still needs a user decision, return the native
`Draft | Blocked | Unverifiable` receipt to drive. Do not invoke
`tk-grill-me`; drive alone decides whether to route that evidence through its
decision phase and retry the spec gate. Include
`User decision: required | none`; `required` cites the new decision and source
evidence.

Standalone and drive handoff use the same Ready contract. In a drive handoff,
preserve task identity and source traceability; return `Phase: spec`, status,
artifact path, and R/AC IDs. If status is not `Ready`, do not create a substitute
spec or weaken the verdict so drive can continue.

## Workflow

1. `collect source`: report paths, claims, and access state from precedence-
   ordered source plus any existing spec.
2. `source map`: map each claim to source location and
   `verified | unverified`.
3. `separate and identify`: separate facts, decisions, assumptions, and
   unresolved conflicts; assign stable requirement and acceptance IDs.
4. `Ready gate`: return `Ready | Draft | Blocked | Unverifiable` with missing
   evidence.
5. `write/print and verify`: write the selected output or print-only result,
   then revalidate required elements, source map, and IDs.
6. `receipt`: connect phase, path, status, source map, unverified items,
   conflicts, and verification in a standalone or drive-consumable receipt.

Write to the user-designated path, print only when requested, otherwise write
`.tigerkit/spec.md`. When an existing spec covers the same task, retain valid
decisions; otherwise replace it without an archive. Under `.tigerkit/`, create
the parent only when needed, prefer a same-directory temporary file plus
rename, never modify `.gitignore`, and warn briefly if scratch is not ignored.

For `--print-only`, create no parent, temporary, or output file. Emit the spec
once, then a compact receipt with `Path: print-only`; reference its R/AC,
source-map, and verification sections instead of repeating their content.

## Failure paths

Preserve the existing target state before output.

| Trigger | Gate/status | Recovery |
|---|---|---|
| Required element missing or assumption unresolved | `Draft` | Separate confirmed content and omissions; do not write as `Ready` |
| Confirmed sources conflict or need a user decision | `Blocked` | Record source locations and one required decision; do not write |
| Required source is inaccessible or an exact UI literal cannot be compared | `Unverifiable` | Record path, error, and affected R/AC; do not write |
| Write/rename fails | `Fail` | Preserve the intact target and precisely restore/revalidate only this run's changes |
| Post-write gate, source map, or R/AC IDs mismatch | Use the one supported state: `Fail` for a known invalid output, `Unverifiable` when evidence cannot establish validity | Do not report `Ready`; stop further writes and record actual state |

After write/rename, reread the file and confirm its gate verdict, source map,
and R/AC IDs match the candidate.

## Contract

Build a `source map` that connects claims to source and separates facts,
decisions, assumptions, and unresolved conflicts. Assign document-unique
requirement IDs such as `R1`, `R2` and acceptance IDs such as `AC1`, `AC2`.
When updating the same task, do not renumber semantically unchanged IDs.
Preserve user-source IDs and never reuse a deleted ID for another meaning.

For bug source, separate `symptom`, `current behavior`, `expected behavior`,
`reproduction`, observed evidence, environment, and regression-seam
availability. Do not turn an unreproduced cause or solution into a decision;
keep it an `unverified` hypothesis. If no reproduction command, fixture, or
seam exists, state that gap in verification planning.

Use `Ready` only when the spec includes problem, goal, included/excluded scope,
requirements, acceptance criteria, verification, source traceability, and
verifiability with no unresolved conflict. Otherwise use `Draft`, `Blocked`,
or `Unverifiable`. The receipt records phase, path, status, and R/AC IDs, then
references the source-map, unverified, conflict, and verification sections
instead of restating their content.

### 🔴 HARD GATE · source UI writing

For every string literal rendered in UI, freeze a separate source-map
inventory. Labels, copy, numbers, units, currency, suffixes, and separators are
examples, not an upper bound. Each row maps source location, non-empty source
literal, current rendered/source-path literal, target literal, and destination
R/AC.

Missing source/current evidence is `Unverifiable`. Any source↔current mismatch
makes every row a conflict candidate and prevents `Ready` without a user
decision. A typo requires rechecking all same-kind tokens; never generalize
source unreliability to adopt current code silently.

Unless the user explicitly decides to change wording, preserve spelling, case,
spacing, punctuation, symbols, numbers, and meaningful line breaks. Do not
translate, paraphrase, shorten, correct, fix typos, or normalize.

After write/print, compare all three literal columns exactly. A code
before/after table cannot replace the source column. Any unauthorized drift or
missing comparison evidence prevents `Ready` and downstream use. Mark only
explicitly approved wording as `authorized change`.

## 🔴 CHECKPOINT · 🛑 STOP · Ready boundary

Before writing, check required elements, unresolved conflicts, and UI-writing
inventory. Missing or unresolved assumptions remain `Draft`; source conflict
requiring a user decision is `Blocked`; inaccessible required source or
uncheckable UI literals are `Unverifiable`. Never save them as `Ready`.

Write user-facing progress and receipt prose in the user's language. Preserve
canonical status tokens, IDs, and receipt keys.

## DO NOT / ANTI-PATTERNS

- Do not mix facts, decisions, and assumptions without a source map or choose
  an unresolved conflict silently.
- Do not alter source UI writing without approval or mark a spec `Ready`
  without exact comparison.
- Do not renumber stable R/AC IDs or reuse deleted IDs.
- Do not mark a document with missing required elements `Ready` or describe
  implementation as complete.
- Do not repair `Draft | Blocked | Unverifiable | Fail` inline merely because
  active drive called this skill.
- Do not mix interviews, ticket creation, implementation, or remote publishing
  into this output. If a combined spec/ticket request produces a non-Ready
  spec, do not proceed to tickets.
