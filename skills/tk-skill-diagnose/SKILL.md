---
name: tk-skill-diagnose
description: "[user/auto] Reproduce and isolate one observed or measured Agent Skill anomaly in a fresh context, then route a verified skill objective to tk-learn. Use for selection, instruction, output, host, eval, stability, or resource incidents. Do not use for ordinary code bugs, static audits, new skill creation, or symptom-free optimization."
argument-hint: "<skill name/path> <incident prompt, expected, observed, host, metric, or trace>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
---

# Agent Skill Diagnosis

Use only for one exact Agent Skill target and one observed or measured anomaly.
Direct selection allowed. Automatic selection requires target and incident
evidence; generic words such as "skill", "debug", or "performance" are
insufficient.

This skill diagnoses. It does not write canonical skills, optimize catalog, or
own final patch. Verified skill objectives route to `tk-learn` as sole
`create | improve | merge` writer. Never semantically mutate canonical source
skill.

## Intake gate

Record:

- exact target package/path, installed ref, origin, host, and invocation;
- incident prompt, expected behavior or metric anchor, and observed result;
- available transcript/event, file, Git, eval, or resource evidence;
- known consumer override or host configuration.

Mark missing values `unverified`. No incident or metric anchor is
`NotApplicable`. Missing fresh execution or inaccessible required evidence is
`Unverifiable | Blocked`, not permission to infer cause.

Accept one `learn-ready` handoff once only when it names incident, exact target,
host/invocation, prompt, expected and observed result, and evidence. Never invoke
`tk-learn` from diagnostic phase or repeat same target + incident + blocker cycle.

## Evidence order

Decide in order:

1. target provenance, description/body consistency, deterministic assertions,
   repository state, and adapter/host evidence;
2. smallest fresh incident reproduction;
3. one nearby control distinguishing suspected failure plane;
4. run-owned minimum experiment only when needed to prove causality.

Reproduction is `Reproduced | Not reproduced | Inconclusive`. Self-report
suggests hypothesis; it does not prove root cause. Repeat fresh run only when
first result is unstable or boundary remains ambiguous. Do not require fixed
trial counts, generic holdout suite, or rubric scoring when narrower evidence
decides incident.

Read references only when applicable:

- [failure planes](references/failure-planes.md)
- [empirical method](references/empirical-method.md)
- [upstream issue anonymization](references/upstream-issue-anonymization.md)

## Efficiency gate

Resource claim needs matched baseline, historical run, repository threshold, or
explicit budget. Otherwise report observed value as profile-only and direction as
`Unverifiable`. Never offset correctness or safety regression with lower tokens,
time, calls, retries, or fan-out.

## Workflow

1. **Freeze** exact incident, target ref, must-preserve behavior, affected host,
   and reliable evidence/metric.
2. **Reproduce** once in clean context. Classify
   `Reproduced | Not reproduced | Inconclusive`.
3. **Control** nearest alternative: loader vs body, parent vs child, candidate vs
   grader, one host vs another, correctness vs resource cost.
4. **Isolate** verified failure plane:
   `selection | loading | instruction | planning | execution | formatting |
   evaluation | compatibility | efficiency | local override`.
5. **Experiment when needed** in one run-owned isolated checkout. Change one
   root-cause theme only; confirm or reject cause. Never treat experiment as
   canonical fix.
6. **Route** next owner from verified evidence.

Stop after conclusive cause or disposition. Second experiment allowed only when
first exposes new specific cause. Clean only run-owned isolation; never rewrite
or patch canonical target.

## Routes

### Verified skill objective: `learn-ready`

Use only when one existing package and one concrete testable objective are
verified. Emit:

```text
Target package: skills/<name>/
Objective: <one observable correction or cost reduction>
Evidence: <incident, control, code, event, or metric references>
Must preserve: <behavior, safety, routing, authority, and host boundaries>
Affected execution: <smallest fresh scenario that decides the objective>
Metric: <actual measurement, labeled proxy, or unavailable>
Incident: <stable ID or source reference>
```

This is input to later explicit `tk-learn`; do not invoke it.

### Other dispositions

- `learn-candidate`: new independently useful skill required.
- `eval-owner`: grader, fixture, harness, or assertion is verified cause.
- `host-owner`: loader, metadata, adapter, or host runtime is verified cause.
- `local-only`: consumer override/configuration causes incident.
- `no-change`: target behavior correct or incident not reproduced.
- `unverifiable`: evidence cannot decide safely.

For external consumer repository, verify upstream origin/ref and current upstream
behavior before proposing anonymized issue. Only duplicate-checked, redacted
proposal with verified provenance is `upstream-draft-ready`; never create,
comment, label, or publish automatically.

## Result

Lead with `## Diagnosis`, then `## Action`; add `## Remaining uncertainty` only
when needed.

For one incident, use short prose. For multiple symptoms sharing one cause, keep
one stable `SD-##` row per cause in `ID | Incident | Root cause`. Report
reproduction verdict, verified failure plane, evidence, route, and exact next
handoff. Do not copy raw logs, transcripts, screenshots, secrets, or repeated run
narration.

When experiment evidence exceeds five rows or later resume needs exact references,
atomically replace `.tigerkit/skill-diagnosis.md` with bounded incident IDs,
candidate/control/holdout evidence refs, measurements, and route. Keep chat to
`## Diagnosis`, `## Action`, and necessary uncertainty; do not create archive,
lifecycle state, or duplicate raw output.

Use one terminal status:

- `Pass`: diagnosis and routing completed;
- `Fail`: deterministic diagnosis/experiment claim violated a gate;
- `Blocked`: required permission, decision, or environment unavailable;
- `Unverifiable`: provenance, reproduction, cause, or metric unverifiable;
- `NotApplicable`: no qualifying Agent Skill incident exists.

### 🔴 HARD GATE · terminal user summary

Separate progress from terminal response. Begin with `## Diagnosis`; no preamble,
`Outcome:`, receipt heading, duplicate status, or raw internal handoff. Expose
only evidence and paths changing next action.

### 🔴 HARD GATE · response language

Use latest explicit user language, else current message's language. Preserve
canonical headings, statuses, IDs, commands, paths, schemas, code, and quoted
literals exactly.

## User decision questions

Only when material user-owned decision blocks diagnosis: put one self-contained
`Question` before `Recommendation`; offer two or three exclusive options with
tradeoffs; mark exactly one `(Recommended)` or `(추천)`. Render directly in chat,
never via structured question/input tool. Preserve `Pending | Blocked` until
answer.

## Pitfalls

- Do not assume skill body is cause.
- Do not patch non-reproduced incident from wording intuition.
- Do not trade correctness, safety, or holdout behavior for lower resource use.
- Do not use fixed repeated runs or judge majorities to manufacture confidence.
- Do not leak expected answers, secrets, or private evidence into prompts.
- Do not mutate canonical skills or invoke downstream skills automatically.
