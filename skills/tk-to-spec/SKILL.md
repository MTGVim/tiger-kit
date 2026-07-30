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
artifact path, and R/AC IDs. The handoff also supplies `Success state` and
`Outstanding transition`. On `Ready`, include `Return to: tk-drive` and echo
the parent-supplied `Outstanding transition` verbatim without choosing or
executing it. A missing or mismatched `Success state` or transition cannot
produce a successful active-drive receipt; return `Blocked`. If status is not
`Ready`, do not create a substitute spec or weaken the verdict so drive can
continue.

## Workflow

1. `collect source`: report paths, claims, and access state from precedence-
   ordered source plus any existing spec.
2. `source map`: map each claim to source location and
   `verified | unverified`.
3. `separate and identify`: separate facts, decisions, assumptions, and
   unresolved conflicts; assign stable requirement and acceptance IDs.
4. `vertical slicing candidate areas`: group related R/AC by user-visible
   behavior and coupling evidence without deciding independence, ticket shape,
   IDs, or whether a ledger is justified.
5. `Ready gate`: return `Ready | Draft | Blocked | Unverifiable` with missing
   evidence.
6. `write/print and verify`: write the selected output or print-only result,
   then revalidate required elements, source map, and IDs.
7. `receipt`: connect phase, path, status, source map, unverified items,
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
verifiability with no unresolved conflict. It also includes a compact
`Vertical slicing candidate areas` table with area label, user-visible
behavior, R/AC coverage, and coupling evidence. Areas are non-authoritative
inputs, not slices or tickets: drive alone decides whether a ledger is
justified, and `tk-to-tickets` alone owns decomposition, ticket IDs, coverage,
and dependencies. Otherwise use `Draft`, `Blocked`, or `Unverifiable`.

Lead with the `Ready | Draft | Blocked | Unverifiable` decision. Summarize the
core scope, requirements, and exceptions in two to five short bullets; one
result may use one to three short lines. For eight or more underlying items,
show the top five to seven and cite the spec artifact path that owns the full
inventory. The spec artifact owns phase, path, status, R/AC IDs, source map,
candidate areas, unverified items, conflicts, and verification. Do not restate
that provenance in a bottom metadata block. For active drive, return the
required phase/status/path/R/AC and transition fields only in the internal
handoff envelope. These are budgets, not quotas.

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

### 🔴 HARD GATE · actionable user output

Treat the skill's canonical output contract as the schema and this gate as its presentation layer. Never remove or reorder required headings, tables, IDs, status tokens, result budgets, approval or safety boundaries, host-required progress notices, or response-language rules. Apply the response-language rules to every free-form clause and prose result value; retain another language only for canonical tokens, code identifiers, commands, paths, or exact quoted or source literals. Ordinary workflow jargon is prose, not a code identifier: translate it unless changing the token would make it incorrect.

In the first available free-form prose slot, lead with the answer, outcome, or action instead of a preamble. For multi-step user work, use the fewest bounded numbered steps. For continuing work, restate current state and the next transition without duplicating a plan or result. Make completed behavior visible. State errors as the observed failure, an evidence-backed cause when known, and a concrete recovery; never manufacture a cause.

Suppress tangents, ceremonial openers, repeated recaps, and closing pleasantries. When a required field repeats a result already stated, make its value referential or minimal instead of recapping the result. When work remains, end with exactly one concrete next action owned by the user or workflow; when work is complete, stop without inventing one. Use a concrete time estimate only when evidence supports it and it helps the person executing the step.

When this gate conflicts with the canonical output contract or the host harness, preserve the higher-priority contract and apply the same shape inside its first prose value or slot. Do not label the user, mention this gate, expose a persistent mode, or require a runtime reference outside this skill.

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
