---
name: tk-reflect
description: "[user/auto] Classify and report reusable rule or skill candidates from conversation, diff, and outcome evidence. Implicit mode is report-only; do not apply to ordinary summaries/completion or mutate automatically."
argument-hint: "<conversation, change, diff, outcome, or source>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Reflect

Apply on explicit invocation or a clear request to extract reusable candidates
from evidence. Do not auto-apply to an ordinary summary or implementation
completion. Implicit mode is report-only. Do not invoke another skill except
for the single bounded diagnosis handoff below.

Read current conversation, changes, diff, implementation/test/review outcomes,
relevant `.tigerkit/` artifacts, the current host's discoverable file-based
persistent memory, and user-named sources. Classify across exactly five
axes—`repo rule | repo skill | user rule | user skill | persistent memory`—and
choose `propose | update | merge | no-op | discard`.

## Workflow

1. `evidence`: produce path/command-cited `verified | unverified` facts,
   including access failures and prior-art results, classified across the five
   axes.
2. `interpretation`: derive a reuse hypothesis separate from facts.
3. `confidence`: return `high | medium | low` and basis.
4. `action`: apply the
   [placement rubric](references/repository-placement.md) to repository
   candidates; choose target and action. A separate Draft owns wording.
5. `apply/receipt`: combine candidate, separate approval, and fresh target state
   into the transition-table result and references; do not copy candidate body.

### Conditional Agent Skill diagnosis

Before promoting a root-cause-dependent `propose | update | merge`, hand off to
`tk-skill-diagnose` exactly once only when all four conditions are verified:

1. a specific Agent Skill name or exact `SKILL.md` path;
2. an observable expected/observed mismatch or measured resource anomaly;
3. root cause is not already verified;
4. the candidate action depends on that cause being true.

The request must explicitly concern a skill incident, its retrospective, or
reuse of that incident evidence. Do not hand off for historical mentions,
existing valid diagnosis receipts, `no-op | discard`, or generic reflection.
If host-native sibling handoff is unavailable, return a `Diagnosis required`
payload and `Unverifiable`; never imitate fresh empirical diagnosis inline.

Send the exact incident ID, target/path, host/invocation, observed prompt,
expected behavior or resource anchor, observed behavior/metrics, evidence
paths/commands, candidate/baseline refs, and `Caller: tk-reflect`. Mark unknowns
`unverified`.

After return, use only `Reproduced` plus verified root cause as evidence.
`Not reproduced` does not verify the original causal claim.
`Inconclusive | Blocked | Unverifiable` keeps confidence `low` and prevents a
root-cause-dependent promotion. Efficiency evidence also requires preserved
correctness. Never call diagnosis twice for one run, call it again for the same
`Incident ID + target + blocker`, or allow diagnosis to call back into reflect.
End equivalent recurrence as `Blocked`.

### Candidate transition table

| Candidate | Condition | Status | Mutation |
|---|---|---|---|
| Rule `propose | update | merge` | before separate apply approval | `pending` | none |
| Rule `no-op | discard` | nothing to apply | `reported` | none |
| Rule `propose | update | merge` | exact target applied/reverified after approval | `applied` | approved scope only |
| Rule | apply/revalidation failure | `Fail | Blocked | Unverifiable` | preserve existing target; stop mutation |
| Skill candidate | evidence, exact target, working draft shown | `pending` | no creation/semantic mutation |
| All candidates | no verified evidence | `Unverifiable` | none |

Each candidate has:

- `Evidence`: observed diff/outcomes/repetitions with path/command and
  `verified | unverified`.
- `Interpretation`: reuse scope/boundary hypothesis derived only from Evidence
  IDs; no prescriptive wording or fact-like hypothesis.
- `Confidence`: `high | medium | low`, `Basis: <Evidence IDs>`, and only when
  needed `Uncertainty`.
- `Action`: prefer `merge | no-op` for duplication. A rule is a short standing
  instruction; a skill needs trigger, repeated steps, I/O, and independent
  value.

Choose Action in order: complete ownership by an existing target is `no-op`;
missing verified boundary in the same target is `update`; consolidating
overlapping targets is `merge`; no suitable target plus rule/skill qualification
is `propose`; one-off or unresolved unverified/conflicting evidence is
`discard`. Action is not apply authority, and every skill candidate stays
`pending`.

Treat discoverable file-based persistent memory as prior art, not as an
automatic write target. When memory completely owns the same behavior and
scope, choose `no-op`. When memory and a candidate share facts but own different
behavioral axes, record the separation in Interpretation and Action, keep the
targets distinct, and propose reciprocal cross-references only when both exact
targets are known. Cross-reference or memory mutation remains `pending` until
separately approved. If the host memory path is unavailable or unreadable,
record it as `unverified`; do not claim that memory contains no prior art.

For `repo rule | repo skill`, Evidence owns normalized raw placement input,
Interpretation owns root/nested/skill boundary, and Action owns the choice.
Create no duplicate placement field. Missing/conflicting threshold evidence
keeps confidence `low` and prevents promotion.

Confidence rises only as follows: `high` requires at least two independently
verified Evidence IDs from different occurrences/source types and no unresolved
conflict/counterexample; `medium` requires at least one verified ID but lacks
one of repetition, independence, or boundary; no verified evidence or
unresolved conflict/counterexample is `low` and cannot promote
`propose | update | merge`.

## Contract

Repository targets are codebase/domain/tool/team-specific; user targets repeat
across repositories. Persistent memory is a current-host file-based target whose
native path must be demonstrated. Default is report-only. Writing a rule into
DESIGN, reuse-map, rule, or persistent-memory files requires separate explicit
approval naming target and scope. Silence, continuation, past analogous
answers, or reflect invocation is not approval.

Only `tk-learn` creates a new skill or semantically updates/merges one. This
skill reports skill evidence, current-host native exact target, working draft,
and `pending` only; it never invokes tk-learn or writes a skill path.

Run terminal status is `Pass | Fail | Blocked | Unverifiable | aborted`. `Pass`
means the evidence/classification workflow completed and every approved
mutation was revalidated; candidates may intentionally remain `pending`.
Use `Fail` for a violated deterministic claim or apply gate, `aborted` for user
stop, and `Blocked` for conflict/unclear apply scope. Never mix per-candidate
`reported | pending | applied` with run terminal status.

By default, mutate no file and create no persistent ledger/identifier. Do not
inspect legacy global state or generalize a one-off workaround. `RF-##` is
response-local, not ledger state. Never promote raw credentials, logs, or
screenshots verbatim even after approval.

Unreadable required source is `unverified` with path/error and cannot support
interpretation. Retry once only after exact access/path/command appears;
otherwise fix `Unverifiable`. Apply/revalidation failures follow the transition
table.

## CHECKPOINT / STOP

After target, evidence, confidence, and action, require separate explicit apply
approval. Before it, stop at `pending | reported`.

Each nonempty candidate reports exactly once: `Target`, IDed `Evidence`,
`Interpretation`, `Confidence`, `Action`, optional `Draft`, and `Receipt`.
Create no duplicate reason/work/learning fields; Receipt holds status and
references only.

## Output contract

Assign `RF-01`, `RF-02`, ... once in discovery order. Title each
`### RF-01 · <short name>` and reuse that ID across Target, Evidence,
Interpretation, Confidence, Action, Draft, Receipt, and final Summary. Never
renumber per section or emit an un-IDed candidate/rule.

The response's final section is always:

| No. | Rule | Summary | Target |
| --- | --- | --- | --- |
| RF-01 | `<short name> (<axis>)` | `<one sentence>` | `<concrete target or unresolved (reason)>` |

One row per candidate. Summary adds no evidence; Target is a concrete
file/skill/user/memory scope or `unresolved (<reason>)`. Keep `Summary` near 40
display characters and `Target` near 50 when an unambiguous compact path or
label is available. Do not copy evidence, draft, actions, or working text into
the table, and do not truncate a target into ambiguity. With no candidate or an
`Unverifiable` run, emit
`| — | None | No reusable rule/skill candidate | No application |`.

If the user asks to reprint a table that wrapped or broke, shorten the cells and
emit the same table with the same IDs and order. Do not rediscover, renumber, or
add evidence during a formatting-only reprint.

User-facing progress and receipt prose follows the user's language while
canonical headings, IDs, fields, and status tokens remain unchanged.

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

- Do not present interpretation as fact or inflate confidence.
- Do not duplicate an existing skill or mutate without apply approval.
- Do not omit discoverable persistent memory from prior-art checks or invent an
  undiscovered host memory path.
- Do not diagnose inline, repeat a diagnosis handoff, or create a
  reflect/diagnose cycle.
- Do not promote raw credentials/logs/screenshots or one-off workarounds.
- Do not omit, reuse, or renumber candidate IDs, or omit Summary.
