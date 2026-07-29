---
name: tk-grill-me
description: "[user/auto] Validate an idea, plan, design, ticket, or RFC through evidence-first, one-question-at-a-time decision closure. Use on explicit invocation, an explicit decision handoff from active tk-drive, or the answer to this skill's pending question; do not auto-start from ordinary ambiguity."
argument-hint: "<idea, plan, design, ticket, RFC, source, or active-drive handoff>"
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: grill-me
    relationship: adapted
---

# Grill Me

Use for explicit invocation, an explicit decision handoff from active
`tk-drive`, or the user's answer to this skill's pending question in the same
conversation. Do not auto-activate from an ordinary ambiguous request,
artifact presence, generic continuation, or merely because drive is active.

Standalone and drive handoff use the same closure contract. A drive handoff
includes task identity, current source and evidence, confirmed decisions, and
unresolved user-owned decisions plus the parent-supplied `Success state` and
`Outstanding transition`. This skill owns only decision closure. It never
writes source, spec, tickets, ADRs, or commits and never invokes downstream
phase owners.

## Contract

Do not confirm or apply a user decision without an explicit answer or
verifiable evidence. Silence, moving to another question, and a similar past
answer are not consent. Factual evidence does not approve a choice for the
user.

If the user stops, return `pending` while awaiting an answer, `aborted` for an
explicit stop, `Blocked` for a decision conflict, or `Unverifiable` when
required evidence cannot be obtained. Continue only after the answer directly
corresponds to this skill's pending question.

## 🔴 CHECKPOINT · 🛑 STOP · user decision boundary

After presenting one recommended question, do not ask another question,
incorporate the decision, or mutate artifacts before the user's answer. Return
`pending` without an answer and `Blocked` when the answer conflicts with
confirmed evidence.

## Workflow

1. `read input`: establish task identity, review scope, caller, current source,
   and evidence.
2. `investigate facts`: produce source-located
   `verified | inferred | unavailable` facts and identify inference that needs
   confirmation.
3. `identify gaps`: compare facts and confirmed decisions against the
   Scope, Constraints, Outputs, and Verification ledger.
4. `ask`: select the highest-impact unresolved user-owned decision and present
   exactly one `Question`, `Recommendation`, and `Evidence`, in that order.
   Make Question explain the evidence-derived context and decision impact in
   readable user-facing language; keep raw paths, logs, and traceability in
   Evidence below it.
5. `incorporate answer`: preserve the answer as the corresponding Decision,
   Constraint, Out of scope, Output, or Verification entry.
6. `repeat or close`: do not repeat answered questions; ask the next one or
   present the one-sentence closure statement when all four axes are settled.
7. `return receipt`: without mutation, return
   `confirmed | pending | aborted | Blocked | Unverifiable`, a non-duplicated
   Decisions reference when one exists, assumptions, remaining risks, and the
   caller to resume.

## Ambiguity ledger

Keep this ledger only in the conversation. Do not automatically record it in
`.tigerkit/`, a spec, tickets, or another document.

- `Scope`: included and excluded behavior
- `Constraints`: technical, operational, and business constraints, or
  explicitly none
- `Outputs`: required behavior, artifacts, and results
- `Verification`: acceptance criteria and completion evidence

Separate unresolved items, confirmed user decisions, and unverified
assumptions on every axis. Choose only the highest-impact unresolved item for
the next question while continuing to evaluate all four axes. Rank items by
safe-progress blocker, scope or irreversible-effect change, verification
blocker, then downstream rework; break any remaining tie in ledger order.

The ledger is not a per-turn dump template. On a question turn, report only
new or changed evidence, the selected unresolved item, one Question,
Recommendation, and Evidence in that order, and `pending`. Repeat unchanged
axes only when needed to explain a conflict or evaluate closure.
Question must remain understandable without reading the raw Evidence field.

## Facts and user judgment

- Auto-confirm only a single current fact supported by exact code, manifest,
  configuration, or equivalent evidence, and cite its path.
- Present facts inferred from code patterns and ask the user to confirm the
  inference.
- Investigate code first when a question mixes current facts with judgment
  about new behavior, but treat the choice as a user decision.
- Always ask about goals, scope, priorities, business rules, success criteria,
  and new behavior.
- Ask rather than guess when fact and judgment cannot be separated.

When required source cannot be read, record its path and failure as
`unavailable`. Do not infer the fact or ask the user to guess repository state.
Continue with one independent user decision only when its impact can be stated
without that fact; otherwise return `Unverifiable`. When confirmed sources
conflict, preserve both sources and ask one decision question rather than
silently selecting either.

## Answer preservation and closure

Preserve the meaning of free-form answers in `Decision`, `Constraints`,
`Out of scope`, `Outputs`, or `Verification`. Leave anything the user did not
say as an `Assumption`. Do not force a confirmation question after every
answer, but ask one when a summary changes meaning, conflicts with an existing
decision, or makes intent ambiguous.

Saying `done` or model confidence does not close the ledger:

1. Check all four axes.
2. Ask the highest-impact remaining question while any axis is unresolved.
3. When all axes are confirmed or explicitly none, restate the agreed goal in
   one sentence.
4. Return `confirmed` only after the user explicitly approves that sentence.
5. Incorporate wording corrections as new decisions and repeat the closure
   gate.

The one-sentence statement is a temporary approval prompt. After approval, do
not copy it into the final response. Record confirmed content once under
`## Decisions` as `Scope`, `Constraints`, `Outputs`, and `Verification`.

Ask about domain terminology only when different meanings affect a decision.
Confirmed terms may later enter a spec, but this skill does not create or edit
`CONTEXT.md`, glossaries, domain documents, or ADRs.

Use only non-empty final sections: `## Decisions`, `## Assumptions`,
`## Remaining risks`, and `## Receipt`. `## Decisions` alone owns decision
content. Keep a question turn atomic at one unresolved decision. For confirmed
results, use one to three short lines for one decision, two to seven readable
rows or bullets for a compound decision set, and the top five to seven plus the
owning source/spec path for eight or more. These are budgets, not quotas. Do
not add a second combined-goal summary. In `## Receipt`, record
`Outcome: <one user-facing sentence>`, `Phase: decision`, `Status`, source or
user-answer evidence, whether decisions were applied, the `## Decisions`
reference when it exists, and `Return to`. Do not duplicate decisions in the
receipt. On a question turn with no decision, omit the Decisions reference and
return the unresolved ledger item with `pending`.

Native `Status` uses `confirmed | pending | aborted | Blocked | Unverifiable`.
For an orchestrator terminal result, map these respectively to
`Pass | Pending | Blocked | Blocked | Unverifiable`.

For a standalone call, `Return to` is the user and the final response may
suggest explicit `tk-to-spec` use without invoking it. For an active-drive
handoff, `Return to` is `tk-drive`; only `confirmed` permits drive to resume at
the spec gate. A `confirmed` active-drive receipt must include
`Return to: tk-drive` and echo the parent-supplied `Outstanding transition`
verbatim. A missing or mismatched `Success state` or transition cannot produce
a successful active-drive receipt; return `Blocked` without choosing or
executing the transition.

### 🔴 HARD GATE · actionable user output

Treat the skill's canonical output contract as the schema and this gate as its presentation layer. Never remove or reorder required headings, tables, receipt keys, IDs, status tokens, result budgets, approval or safety boundaries, host-required progress notices, or response-language rules. Apply the response-language rules to every free-form clause and prose receipt value; retain another language only for canonical tokens, code identifiers, commands, paths, or exact quoted or source literals. Ordinary workflow jargon is prose, not a code identifier: translate it unless changing the token would make it incorrect.

In the first available free-form prose slot, lead with the answer, outcome, or action instead of a preamble. For multi-step user work, use the fewest bounded numbered steps. For continuing work, restate current state and the next transition without duplicating a plan or receipt. Make completed behavior visible. State errors as the observed failure, an evidence-backed cause when known, and a concrete recovery; never manufacture a cause.

Suppress tangents, ceremonial openers, repeated recaps, and closing pleasantries. When a required schema field repeats a result already stated, keep the field but make its value referential or minimal instead of recapping the result. When work remains, end with exactly one concrete next action owned by the user or workflow; when work is complete, stop without inventing one. Use a concrete time estimate only when evidence supports it and it helps the person executing the step.

When this gate conflicts with the canonical output contract or the host harness, preserve the higher-priority contract and apply the same shape inside its first prose value or slot. Do not label the user, mention this gate, expose a persistent mode, or require a runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, summary, or receipt, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose receipt value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, receipt keys, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

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

- Do not decide for the user or bundle multiple independent decisions into one
  question.
- Do not interpret investigation, silence, or forward motion as approval.
- Do not mutate artifacts or call `tk-to-spec`, `tk-to-tickets`,
  `tk-implement`, or another sibling phase owner.
- Do not auto-start from ordinary ambiguity or an active drive without an
  explicit decision handoff.
