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

Use on explicit `/tk-grill-me` or `$tk-grill-me` invocation, an exact active
`tk-drive` decision handoff, or the user's answer to this skill's pending
question in the same conversation. Do not auto-activate from ordinary
ambiguity, artifact presence, generic continuation, or an unrelated answer.

This skill owns one evidence-first decision procedure. The procedure,
safety boundary, and completion criteria are identical for standalone and
active-drive callers; only result routing differs.

## Contract

Never confirm a user decision without an explicit answer. Silence, forward
motion, factual evidence, and a similar past answer are not consent.

Caller mode controls presentation:

- `standalone`: present the one pending question or final decision result to
  the user.
- `active drive`: return the same decision state internally so `tk-drive`
  continues directly to the next applicable procedure. Do not render a
  terminal result, receipt, `Pass`, or `Return to: tk-drive` stopping surface.

This skill is read-only. It never writes source, spec, tickets, ADRs, or
commits and never invokes `tk-to-spec`, `tk-to-tickets`, `tk-implement`, or a
sibling phase owner.

## Procedure

1. `read input`: bind task identity, caller mode, source, current evidence,
   confirmed decisions, unresolved user-owned decisions, and any pending
   question.
2. `investigate facts`: produce source-located
   `verified | inferred | unavailable` facts.
3. `identify gaps`: compare facts and decisions across Scope, Constraints,
   Outputs, and Verification.
4. `rank`: select the highest-impact unresolved decision by safe-progress
   blocker, scope or irreversible effect, verification blocker, then
   downstream rework.
5. `ask`: return exactly one `Question`, `Recommendation`, and `Evidence`, in
   that order, then stop `pending`.
6. `incorporate`: preserve the explicit answer as the matching Decision,
   Constraint, Out of scope, Output, or Verification entry.
7. `repeat or close`: never repeat an answered question. When all four axes
   are settled, present one agreed-goal sentence for explicit approval.
8. `confirm`: return `confirmed` only after explicit approval of that sentence.

## Ambiguity ledger

Keep the ledger only in the conversation:

- `Scope`: included and excluded behavior;
- `Constraints`: technical, operational, and business constraints, or
  explicitly none;
- `Outputs`: required behavior, artifacts, and results;
- `Verification`: acceptance criteria and completion evidence.

Separate unresolved items, confirmed decisions, and unverified assumptions.
The ledger is not a per-turn dump template. A question turn includes only new
or changed evidence, the selected unresolved item, and one question.

## Facts and user judgment

- Auto-confirm only a current fact supported by exact repository or runtime
  evidence and cite its source.
- Mark code-pattern conclusions as `inferred` when they require judgment.
- Investigate current facts before asking a mixed fact-and-choice question.
- Always ask about goals, scope, priorities, business rules, success criteria,
  and new behavior.
- When required evidence is inaccessible, return `Unverifiable` unless an
  independent decision can still be stated safely.
- When confirmed sources conflict, preserve both and ask one decision question
  instead of selecting silently.

## Answer preservation and closure

Preserve the meaning of free-form answers. Leave unsaid content as an
assumption. Ask for clarification only when a summary changes meaning,
conflicts with confirmed evidence, or creates material ambiguity.

`done` and model confidence do not close the ledger. Check all four axes,
return the next highest-impact question while one remains unresolved, and
require explicit approval of the final agreed-goal sentence.

For standalone confirmed results, use only non-empty `## Decisions`,
`## Assumptions`, and `## Remaining risks`. Do not append phase/status
provenance. Use one to three short lines for one decision and two to seven
readable rows or bullets for a compound set. For eight or more, retain the top
five to seven plus the owning source or spec reference.

Native status is
`confirmed | pending | aborted | Blocked | Unverifiable`. A standalone result
maps these to `Pass | Pending | Blocked | Blocked | Unverifiable`. Active drive
consumes native status directly without a user-facing status block.

### 🔴 HARD GATE · terminal user summary

Treat progress commentary, internal handoff envelopes, and the terminal user response as distinct surfaces. Begin every terminal user-facing response directly with the skill's canonical result heading or, when its result schema owns no heading, its canonical result sentence. Do not emit a standalone separator, ceremonial preamble, or progress recap before that opening. Do not emit a terminal user-summary opening between a successful phase receipt and the next active-drive phase invocation.

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

- Do not split the same decision procedure into another skill.
- Do not decide for the user or bundle independent decisions.
- Do not mutate artifacts or invoke downstream phase owners.
- Do not let active-drive routing become a receipt or terminal stop.
