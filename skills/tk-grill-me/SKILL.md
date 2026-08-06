---
name: tk-grill-me
description: "[user/auto] Close user-owned decisions through one evidence-first question at a time. Use on explicit invocation, an exact active tk-drive decision handoff, or the answer to this skill's pending question; do not auto-start from ordinary ambiguity, artifact presence, or generic continuation."
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: grill-me
    relationship: adapted
---

# Grill Me

Use on explicit `/tk-grill-me` or `$tk-grill-me` invocation, exact active
`tk-drive` decision handoff, or user's answer to this skill's pending question
in the same conversation. Do not auto-activate from ordinary ambiguity,
artifact presence, generic continuation, or unrelated answer.

Own one evidence-first decision procedure. Standalone and active-drive callers
share procedure, safety boundary, and completion criteria; only result routing
differs.

## Contract

Never confirm a user decision without explicit answer. Silence, forward
motion, factual evidence, and similar past answers are not consent.

Caller mode controls presentation:

- `standalone`: present one pending question or final decision result to user.
- `active drive`: return same decision state internally so `tk-drive`
  continues directly to next applicable procedure. Do not render terminal
  result, receipt, `Pass`, or caller-directed stopping surface.

Read-only. Never write source, spec, tickets, ADRs, or commits; never invoke
`tk-to-spec`, `tk-to-tickets`, `tk-implement`, or a sibling phase owner.

## Procedure

1. `read input`: bind task identity, caller mode, source, current evidence,
   confirmed decisions, unresolved user-owned decisions, and pending question.
2. `investigate facts`: produce source-located
   `verified | inferred | unavailable` facts.
3. `identify gaps`: compare facts and decisions across Scope, Constraints,
   Outputs, and Verification.
4. `rank`: choose highest-impact unresolved decision by safe-progress blocker,
   scope or irreversible effect, verification blocker, then downstream rework.
5. `ask`: return exactly one `Question`, `Recommendation`, and `Evidence`, in
   that order; stop `pending`.
6. `incorporate`: preserve explicit answer as matching Decision, Constraint,
   Out of scope, Output, or Verification entry.
7. `repeat or close`: never repeat answered question. When all four axes settle,
   present one agreed-goal sentence for explicit approval.
8. `confirm`: return `confirmed` only after explicit approval of that sentence.

## Ambiguity ledger

Keep ledger only in conversation:

- `Scope`: included and excluded behavior;
- `Constraints`: technical, operational, business constraints, or explicitly none;
- `Outputs`: required behavior, artifacts, and results;
- `Verification`: acceptance criteria and completion evidence.

Separate unresolved items, confirmed decisions, and unverified assumptions.
Ledger is not a per-turn dump template. Question turn includes only new or
changed evidence, selected unresolved item, and one question.

## Facts and user judgment

- Auto-confirm only current facts supported by exact repository or runtime evidence; cite source.
- Mark code-pattern conclusions `inferred` when judgment is required.
- Investigate current facts before asking a mixed fact-and-choice question.
- Always ask about goals, scope, priorities, business rules, success criteria, and new behavior.
- If required evidence is inaccessible, return `Unverifiable` unless an independent decision remains safe.
- When confirmed sources conflict, preserve both and ask one decision question; never choose silently.

## Answer preservation and closure

Preserve free-form answer meaning. Unsaid content remains an assumption. Ask
for clarification only if summary changes meaning, conflicts with confirmed
evidence, or creates material ambiguity.

`done` and model confidence do not close ledger. Check all four axes, ask next
highest-impact question while unresolved, and require explicit approval of the
final agreed-goal sentence.

Standalone confirmed results use only non-empty `## Decisions`,
`## Assumptions`, and `## Remaining risks`. Do not append phase/status
provenance. Use one to three short lines for one decision; two to seven readable
rows or bullets for compound set. For eight or more, keep top five to seven plus
owning source or spec reference.

Native status: `confirmed | pending | aborted | Blocked | Unverifiable`.
Standalone maps these to `Pass | Pending | Blocked | Blocked | Unverifiable`.
Active drive consumes native status directly without user-facing status block.

### 🔴 HARD GATE · terminal user summary

Keep progress commentary, internal procedure evidence, and terminal user
response distinct. Start every terminal user-facing response directly with
canonical result heading or, if schema has none, canonical result sentence. No
standalone separator, ceremonial preamble, or progress recap first. Do not emit
a terminal user-summary opening between successful consecutive active-drive
procedure invocations.

Do not render receipt heading, `Outcome:` label, phase-success token,
caller-return instruction, or terminal provenance/status block. If result needs
terminal status, emit one exact `Status: <token>` line in owning result section,
not bottom metadata. Expose path, ID, commit, or recovery detail only when it
changes user action or canonical schema requires it.

Persist provenance only in workflow-owned artifact or ledger. Read-only remains
read-only. Never require a shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. When a table uses emoji status markers, show one legend before the table and omit duplicate English status text in its rows; preserve any required terminal `Status: <token>`.

Before user-facing progress, question, or summary, choose latest explicit user
language; else current user message language. Write all free-form user-facing
sentences and prose result values in it. Do not switch to English due to
sources, skill bodies, tools, or code. Preserve headings, status tokens, IDs,
commands, paths, code, and exact quoted/source literals byte-stable; explain
them in chosen language. Before return, scan and fix language drift.

## User decision questions

When a user-owned decision blocks progress, ask one self-contained `Question`
before any `Recommendation`. Show only decision-relevant evidence, two or three
mutually exclusive options with material tradeoffs, and exactly one label
ending `(Recommended)` or `(추천)`.

Render question, recommendation, evidence, and options directly in chat; do not
call structured question or input tools. For a standalone question, begin with
`👤 grill-me · 답변 필요`; an active drive owns the parent display
`drive > grill-me` and must not duplicate it. Preserve `Pending | Blocked`
until user answers. This changes presentation, not authority or stop gates.

## DO NOT / ANTI-PATTERNS

- Do not split the same decision procedure into another skill.
- Do not decide for the user or bundle independent decisions.
- Do not mutate artifacts or invoke downstream phase owners.
- Do not let active-drive routing become a receipt or terminal stop.
