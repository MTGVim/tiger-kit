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
content. Do not add a second combined-goal summary. In `## Receipt`, record
`Phase: decision`, `Status`, source or user-answer evidence, whether decisions
were applied, the `## Decisions` reference when it exists, and `Return to`.
Do not duplicate decisions in the receipt. On a question turn with no decision,
omit the Decisions reference and return the unresolved ledger item with
`pending`.

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

Write user-facing questions and receipts in the user's language while
preserving canonical fields and status tokens.

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

- Do not decide for the user or bundle multiple independent decisions into one
  question.
- Do not interpret investigation, silence, or forward motion as approval.
- Do not mutate artifacts or call `tk-to-spec`, `tk-to-tickets`,
  `tk-implement`, or another sibling phase owner.
- Do not auto-start from ordinary ambiguity or an active drive without an
  explicit decision handoff.
