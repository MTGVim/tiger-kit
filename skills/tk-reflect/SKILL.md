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
completion, and do not invoke another skill. Implicit mode is report-only.

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

Use `aborted` for user stop and `Blocked` for conflict/unclear apply scope.
Never mix per-candidate `reported | pending | applied` with run terminal status.

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

## DO NOT / ANTI-PATTERNS

- Do not present interpretation as fact or inflate confidence.
- Do not duplicate an existing skill or mutate without apply approval.
- Do not omit discoverable persistent memory from prior-art checks or invent an
  undiscovered host memory path.
- Do not promote raw credentials/logs/screenshots or one-off workarounds.
- Do not omit, reuse, or renumber candidate IDs, or omit Summary.
