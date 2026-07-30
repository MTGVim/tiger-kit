---
name: tk-skill-diagnose
description: "[user/auto] Reproduce and isolate an observed or measured Agent Skill anomaly in a clean context, including missing or excessive selection, ignored instruction or output contracts, host differences, eval misclassification, unstable or repeated behavior, and abnormal token, time, tool, retry, nested-call, or fan-out use. Do not use for ordinary application bugs, static skill audits, skill creation, typo-only edits, or symptom-free catalog-wide optimization."
argument-hint: "<skill name/path> <incident prompt, expected, observed, host, metric, or trace>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
---

# Agent Skill Diagnosis

Use this skill only for a specific Agent Skill target plus an observed or
measured anomaly. Direct selection is allowed. Automatic selection requires
both target and incident evidence; words such as "skill", "debug", or
"performance" alone are insufficient.

Diagnose correctness, stability, compatibility, evaluation validity, and
resource efficiency. Do not replace ordinary code debugging, `tk-grooming`
static audits, `tk-learn` semantic writing, `tk-reflect` candidate
classification, or Darwin-style broad optimization.

## Intake gate

Record the exact target path, host-native location, origin, installed
version/ref, invocation, prompt, expected behavior or resource anchor, observed
behavior or metrics, and evidence paths/commands. Mark every unknown value
`unverified`; never infer it from a name.

If there is no incident or measured anomaly, return `NotApplicable` with the
correct owner boundary. If a fresh executor cannot be used, do not substitute
self-rereading; return `Unverifiable` or `Blocked`.

An active `tk-reflect` handoff is valid only when its payload supplies:

```text
Incident ID
Target skill / exact path
Host and invocation
Observed prompt
Expected behavior or resource anchor
Observed behavior or metrics
Available evidence paths/commands
Candidate/baseline refs if present
Caller: tk-reflect
```

Accept at most one such handoff. Never call `tk-reflect`, and never re-enter an
equivalent `Incident ID + target + blocker`.

## Workflow

1. `target/provenance`: distinguish TigerKit canonical/adapted source,
   consumer-local fork/override, and local configuration.
2. `iteration 0`: compare description trigger/capability promises with body
   workflow, failures, approval boundary, and output owners. Treat static gaps
   as reproduction hypotheses only.
3. `freeze`: define incident/median, nearby control/edge, and an unused holdout;
   freeze critical requirements before changing any candidate.
4. `reproduce`: run the current target twice in fresh clean contexts under
   matched conditions and classify `Reproduced | Not reproduced |
   Inconclusive`.
5. `diagnose`: run the separate empirical pass in
   [empirical-method.md](references/empirical-method.md), keeping deliverable
   and diagnostic report distinct.
6. `isolate`: combine self-report with deterministic evidence and map the cause
   through [failure-planes.md](references/failure-planes.md). Self-report alone
   never proves root cause.
7. `experiment`: create a one-theme minimum candidate only in a run-owned
   isolated checkout/path. State the frozen requirement/assertion served,
   General Fix Rule, and predicted correctness/resource effect first.
8. `re-evaluate`: use fresh executors for incident, control, regression cases,
   and holdout. Require two clean final checks with no new critical regression.
9. `dispose`: report the exact owner candidate. A semantic skill change becomes
   a `tk-learn` handoff proposal; an eval/grader/adapter defect names that owner
   instead.

Do not patch a non-reproduced incident from wording intuition. Default to at
most two candidate themes, two concurrent fresh executors, two trials per
scenario, and one reflect handoff. Do not nest delegation or sweep the catalog.

## Efficiency gate

Require at least one verified stable/no-skill/historical/threshold/candidate
anchor. Compare the same prompt, host, model/config, tools, repository state,
and at least two trials. Without an anchor, report `Profile only` and leave
improvement/regression `Unverifiable`.

Correctness, safety, routing, mutation, control, or holdout regression always
outweighs resource savings. Never invent unavailable token, duration, tool,
retry, nested-call, or fan-out metrics.

## External consumer repositories

When the repository is not TigerKit and the target is `tk-*`, verify TigerKit
origin/ref, consumer overrides, and—when possible—the incident against
unmodified upstream source. Consumer-only drift is `local-only`. Before any
upstream proposal, complete the provenance, reproduction, control/holdout,
issue-search, and ancestry gates in
[upstream-issue-anonymization.md](references/upstream-issue-anonymization.md).
A matching issue is cited and reconciled instead of redrafted. Only
`upstream-draft-ready` may include an upstream issue title or body; every
other disposition reports evidence gaps without proposal content.
Never create, comment on, label, or publish an issue automatically.

## Mutation boundary

Never semantically mutate the canonical source skill. Keep experiments in an
isolated temporary path, and do not silently change consumer production/code
files. Do not push, publish, release, rewrite history, or start another skill.

If fresh evidence is missing or a candidate regresses a frozen scenario,
discard the candidate, preserve the attempted evidence, and clean only
run-owned isolation. A deterministic regression is `Fail`; unavailable
required capability is `Blocked`; unverifiable evidence, ownership, or cleanup
state is `Unverifiable`. Never recover by editing the canonical target.

A validated semantic candidate reports this handoff only:

```text
Target exact path
Incident and frozen scenarios
Verified root cause
General Fix Rule
Minimal diff candidate
Normal/diagnostic/holdout evidence
Compatibility/resource evidence
Remaining uncertainty
Requested tk-learn action
```

## Output contract

Assign `SD-01`, `SD-02`, ... in discovery order. Keep one ID for symptoms that
share a root-cause theme. In chat, emit `## Diagnosis`, `## Action`, optional
`## Remaining uncertainty`. Diagnosis leads with the
verified root cause or reproduction verdict; Action names only the next owner
or validated candidate.

When more than one ID is affected, render `Diagnosis` as a compact
`ID | Incident | Root cause` table and `Action` as an `ID | Next action` table.
Use a sentence when only one user-relevant row exists. Rows represent
root-cause themes, not experiments, hosts, logs, or evidence fragments.
Summarize two to seven reproduced/root-cause/candidate results as bounded rows
or bullets. For eight or more, show the top five to seven and cite
`.tigerkit/skill-diagnosis.md` for the remainder. These are budgets, not quotas.

When the run uses more than one experiment or host, or has more than five
evidence rows, write or replace `.tigerkit/skill-diagnosis.md`. Its compact
rows contain ID, target/provenance, incident, evidence references,
reproduction, failure plane, root cause, candidate verdict, resource result,
upstream disposition, and handoff. Never copy raw logs, transcripts, repeated
rationale, or output metadata. Create the parent lazily, write atomically, and
warn if scratch is not ignored; never modify `.gitignore`.

Upstream disposition is exactly `not-applicable | local-only |
upstream-candidate | upstream-draft-ready | upstream-unverifiable`. Receipt
provenance belongs in the existing diagnosis ledger when it is written.
Otherwise expose terminal status, affected IDs, or references only when they
change the user's next action, without appending metadata. Keep incident state
separate from terminal status:

- `Pass`: the diagnosis workflow and evidence completed; it does not mean the
  target skill is issue-free.
- `Fail`: a candidate or diagnosis claim violated a deterministic gate.
- `Blocked`: a required decision, permission, or environment is unavailable.
- `Unverifiable`: provenance, reproduction, metrics, or fresh execution could
  not be verified.
- `NotApplicable`: no qualifying skill incident exists.

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

- Do not assume every incident is a SKILL.md wording defect.
- Do not leak expected outputs, assertion answers, secrets, raw private logs,
  screenshots, or identifiers into diagnostic prompts or drafts.
- Do not trade correctness for lower resource use.
- Do not reuse a learned executor, repeat an equivalent blocker, or replace a
  fresh executor with self-review.
- Do not mutate canonical skills or automatically invoke `tk-learn` or
  `tk-reflect`.
