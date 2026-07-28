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
unmodified upstream source. Consumer-only drift is `local-only`. A verified
upstream cause may produce an anonymized issue draft by following
[upstream-issue-anonymization.md](references/upstream-issue-anonymization.md).
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
share a root-cause theme. Emit these canonical sections:

- `## Target and provenance`
- `## Incident`
- `## Reproduction`
- `## Failure plane`
- `## Empirical diagnostics`
- `## Candidate experiment`
- `## Regression and efficiency`
- `## Upstream disposition`
- `## Handoff`
- `## Receipt`

`Upstream disposition` is exactly `not-applicable | local-only |
upstream-candidate | upstream-draft-ready | upstream-unverifiable`. Receipt
contains terminal status and section references only. Keep incident state
separate from terminal status:

- `Pass`: the diagnosis workflow and evidence completed; it does not mean the
  target skill is issue-free.
- `Fail`: a candidate or diagnosis claim violated a deterministic gate.
- `Blocked`: a required decision, permission, or environment is unavailable.
- `Unverifiable`: provenance, reproduction, metrics, or fresh execution could
  not be verified.
- `NotApplicable`: no qualifying skill incident exists.

Write user-facing progress and receipt prose in the user's language. Preserve
canonical headings, IDs, enums, and status tokens.

## DO NOT / ANTI-PATTERNS

- Do not assume every incident is a SKILL.md wording defect.
- Do not leak expected outputs, assertion answers, secrets, raw private logs,
  screenshots, or identifiers into diagnostic prompts or drafts.
- Do not trade correctness for lower resource use.
- Do not reuse a learned executor, repeat an equivalent blocker, or replace a
  fresh executor with self-review.
- Do not mutate canonical skills or automatically invoke `tk-learn` or
  `tk-reflect`.
