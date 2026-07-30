---
name: tk-reflect
description: "[user/auto] Classify reusable rule or skill candidates from conversation, diff, and outcome evidence. Implicit mode is report-only; only a valid active-drive tail may apply an eligible repo rule automatically."
argument-hint: "<conversation, change, diff, outcome, or source>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Reflect

Apply on explicit invocation, a clear request to extract reusable candidates
from evidence, or one valid active-drive tail handoff. Do not auto-apply to an
ordinary summary or implementation completion. Implicit mode is report-only.
Do not invoke another skill except for the single bounded diagnosis handoff
below.

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

## Drive-tail mode

Only a handoff containing `Mode: drive-optimistic`, `Success state: Pass`, and
`Outstanding transition: final receipt` grants the bounded authority in
[drive-optimistic reflection](references/drive-optimistic.md). It may apply
only an eligible existing `repo rule`, writes `.tigerkit/reflect.md`, never
promotes a skill, and returns `Return to: tk-drive` plus the outstanding
transition verbatim. Missing or mismatched authority falls back to no mutation
and cannot return a drive-tail success receipt.

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

This table governs standalone and ordinary implicit reflection; drive-tail
transitions use the eligibility, restoration, and receipt table in its
reference.

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
- `Preferred prevention owner`: exactly one of
  `repo rule | repo skill | user rule | user skill | persistent memory`,
  chosen from the narrowest durable owner that can prevent recurrence.
- `Host dependency`: `host-independent | current-host-native | inaccessible`,
  with the exact native path or unavailable evidence when host behavior is
  required.
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
approval naming target and scope, except for an eligible existing repository
rule in the valid drive-tail mode. Silence, continuation, past analogous
answers, or standalone reflect invocation is not approval.

Only `tk-learn` creates a new skill or semantically updates/merges one. This
skill reports skill evidence, current-host native exact target, working draft,
and `pending` only; it never invokes tk-learn or writes a skill path.

Run terminal status is `Pass | Pending | Fail | Blocked | Unverifiable |
aborted`. Use `Pending` while actionable candidates await apply disposition,
`Pass` after a completed no-op/report or revalidated mutation, `Fail` for a
violated deterministic claim or apply gate, `aborted` for user stop, and
`Blocked` for conflict/unclear apply scope. Never mix per-candidate
`reported | pending | applied` with run terminal status.

By default, mutate no file and create no ledger. An explicit report-artifact
request may write the bounded `.tigerkit/reflect.md` ledger below without
authorizing target application; valid drive-tail mode writes the same ledger
under its own bounded authority. Do not inspect legacy global state or
generalize a one-off workaround. `RF-##` is run-local, not durable identity.
Never promote raw credentials, logs, or screenshots verbatim even after
approval.

Unreadable required source is `unverified` with path/error and cannot support
interpretation. Retry once only after exact access/path/command appears;
otherwise fix `Unverifiable`. Apply/revalidation failures follow the transition
table.

## CHECKPOINT / STOP

Outside valid drive-tail mode, require separate explicit apply approval after
target, evidence, confidence, and action. Before it, stop at
`pending | reported`. Drive-tail mode follows its eligibility and rollback
checkpoint instead of asking a question.

## Output contract

Assign `RF-01`, `RF-02`, ... once in discovery order. In chat, emit only
`## Disposition`; insert the decision question after it only when apply
approval is required. Disposition shows at most five
decision-relevant rows:

| ID | Candidate | Action | Target | Why |
| --- | --- | --- | --- | --- |
| RF-01 | `<short name>` | `<action/status>` | `<target>` | `<evidence refs>` |

Keep chat compact by citing evidence paths instead of copying long bodies.
Every `Action` and `Why` cell must explain the human-readable next action and
reason; an `RF-##` ID or status token alone is not a result. Keep at most five
rows and cite `.tigerkit/reflect.md` when it owns additional candidates. A
no-op stays minimal.
Within `## Disposition`, add a bounded `Draft` block only when an actionable
rule/skill candidate requires working wording.

Only on an explicit report-artifact request outside drive-tail mode, or on a
valid drive-tail handoff, write or replace `.tigerkit/reflect.md`. The
standalone ledger has one compact row per
candidate with ID, target, evidence references, interpretation, confidence,
preferred prevention owner, host dependency, action, status, and optional
draft path; drive-tail fields follow its reference. It contains
no raw logs, transcripts, diff excerpts, repeated rationale, or copied output
fields.
Create its parent lazily, write atomically, and warn if scratch is not ignored;
never modify `.gitignore`.
The ledger records terminal status, candidate counts, its own path, and IDs
requiring a decision; the chat summary never substitutes for the Disposition
table or appends that metadata. With no candidate, emit one
`— | None | no-op | — | no verified reusable evidence` row.

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

- Do not present interpretation as fact or inflate confidence.
- Do not duplicate an existing skill or mutate without apply approval.
- Do not omit discoverable persistent memory from prior-art checks or invent an
  undiscovered host memory path.
- Do not diagnose inline, repeat a diagnosis handoff, or create a
  reflect/diagnose cycle.
- Do not promote raw credentials/logs/screenshots or one-off workarounds.
- Do not omit, reuse, or renumber candidate IDs, or omit Summary.
