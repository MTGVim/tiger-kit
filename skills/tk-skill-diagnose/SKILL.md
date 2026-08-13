---
name: tk-skill-diagnose
description: "[user/auto] 하나의 observed 또는 measured Agent Skill anomaly를 fresh context에서 재현·격리한 뒤, 검증된 skill objective를 tk-learn으로 라우팅한다. selection, instruction, output, host, eval, stability 또는 resource incident에 사용한다. ordinary code bug, static audit, new skill creation 또는 symptom-free optimization에는 사용하지 않는다."
disable-model-invocation: false
argument-hint: "<skill name/path> <incident prompt, expected, observed, host, metric, or trace>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
---

# Agent Skill Diagnosis

Use only for exactly one Agent Skill target and one observed or measured anomaly.
Direct selection is allowed. Automatic selection requires a target and incident evidence;
generic terms such as `skill`, `debug`, or `performance` are insufficient.

This skill performs diagnosis only. It does not write the canonical skill, optimize the
catalog, or own the final patch. Route a verified skill objective through `tk-learn` as
the sole `create | improve | merge` writer. Do not semantically modify the canonical
source skill.

## Input Gate

Record:

- exact target package/path, installed ref, origin, host, and invocation;
- incident prompt, expected behavior or metric anchor, and observed result;
- available transcript/event, file, Git, eval, or resource evidence;
- known consumer override or host configuration.

Mark missing values as `unverified`. A missing incident or metric anchor does not mean
`NotApplicable`. If fresh execution is unavailable or required evidence is inaccessible,
the result is `Unverifiable | Blocked`, not permission to infer a cause.

Accept a `learn-ready` handoff only once when it specifies the incident, exact target,
host/invocation, prompt, expected and observed result, and evidence. Do not invoke
`tk-learn` during diagnosis, and do not repeat the same target + incident + blocker cycle.

## Evidence Order

Decide in this order:

1. target provenance, description/body consistency, deterministic assertions,
   repository state, and adapter/host evidence;
2. reproduce the smallest fresh incident;
3. check one adjacent control that distinguishes the suspected failure plane;
4. run a run-owned minimum experiment only when needed to establish causality.

Classify reproduction as `Reproduced | Not reproduced | Inconclusive`. Self-report may
suggest a hypothesis but does not prove root cause. Repeat a fresh run only when the first
result is unstable or the boundary with the control is unclear. Do not require a fixed
trial count, generic holdout suite, or rubric scoring when narrow evidence can determine
the cause.

Read the following references only when applicable:

- [failure planes and evidence](references/failure-planes.md)
- [empirical diagnostic method](references/empirical-method.md)
- [upstream issue anonymization](references/upstream-issue-anonymization.md)

## Efficiency Gate

A resource claim requires a matched baseline, historical run, repository threshold, or
explicit budget. Otherwise, record the observed value only as a profile and leave the
direction `Unverifiable`. Lower token, time, call, retry, or fan-out usage does not offset
a correctness or safety regression.

## Workflow

1. **Freeze**: Fix the exact incident, target ref, must-preserve behavior, affected host,
   and reliable evidence/metric.
2. **Reproduce**: Reproduce once in a clean context and classify the result as
   `Reproduced | Not reproduced | Inconclusive`.
3. **Control**: Compare the nearest alternative. Distinguish loader from body, parent
   from child, candidate from grader, one host from another, and correctness from
   resource cost.
4. **Isolate**: Select one verified failure plane from:
   `selection | loading | instruction | planning | execution | formatting |
   evaluation | compatibility | efficiency | local override`.
5. **Experiment only when needed**: Run only in one run-owned isolated checkout.
   Change one root-cause theme and confirm or reject the cause. Do not treat the
   experiment as the canonical fix.
6. **Route**: Choose one owner based on verified evidence.

Stop at a conclusive cause or disposition. Allow a second experiment only if the first
reveals a new concrete cause. Clean up only run-owned isolation; do not rewrite or patch
the canonical target.

## 🔴 CHECKPOINT / STOP · Next-Step Gate

Do not begin the next step, experiment, or handoff until each checkpoint passes.

- **Input checkpoint**: An exact target, eligible Agent Skill incident, and incident
  evidence exist. If there is no eligible Agent Skill incident, such as an ordinary
  code bug, stop with `NotApplicable`. If a required incident or metric anchor is
  missing or unverified, stop with `Blocked | Unverifiable`, not `NotApplicable`.
- **Reproduction checkpoint**: Record the fresh result as
  `Reproduced | Not reproduced | Inconclusive`. If `Inconclusive`, do not finalize
  the cause or route; stop with `Unverifiable`.
- **Isolation checkpoint**: Evidence confirms one failure plane and an adjacent control
  that distinguishes it. Otherwise, make no root-cause claim and stop with
  `Unverifiable`.
- **Routing checkpoint**: One concrete, testable objective and must-preserve boundary
  are verified. Otherwise, do not emit a `learn-ready` handoff.
- **🛑 STOP**: After emitting `learn-ready`, this skill still does not invoke `tk-learn`
  or mutate the canonical skill/catalog. Wait for a separate explicit invocation.

## Routing

### Verified Skill Objective: `learn-ready`

Use only when one existing package and one concrete, testable objective have been
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

이는 이후 명시적으로 실행하는 `tk-learn`의 input이다. 여기서 호출하지 않는다.

### Other Dispositions

- `learn-candidate`: A new independently useful skill is needed.
- `eval-owner`: The grader, fixture, harness, or assertion is the verified cause.
- `host-owner`: The loader, metadata, adapter, or host runtime is the verified cause.
- `local-only`: A consumer override/configuration causes the incident.
- `no-change`: Target behavior is correct or the incident is not reproduced.
- `unverifiable`: Evidence cannot safely determine the result.

In an external consumer repository, verify the upstream origin/ref and current upstream
behavior before proposing an anonymized issue. Classify only a redacted proposal that
has passed duplicate checking as `upstream-draft-ready`; do not automatically create,
comment, label, or publish it.

## Results

`## Diagnosis`로 시작하고 이어서 `## Action`을 출력한다. 필요할 때만
`## Remaining uncertainty`를 추가한다.

하나의 incident에는 짧은 설명을 사용한다. 여러 symptom이 하나의 cause를 공유하면
`ID | Incident | Root cause` 형식으로 cause마다 안정적인 `SD-##` row 하나를 유지한다.
reproduction verdict, verified failure plane, evidence, route 및 정확한 next handoff를
보고한다. raw log, transcript, screenshot, secret 또는 반복된 run narration을
복사하지 않는다.

experiment evidence가 다섯 row를 넘거나 이후 resume에 정확한 reference가 필요하면
`.tigerkit/skill-diagnosis.md` 를 bounded incident IDs, candidate/control/holdout
evidence refs, measurements 및 route와 함께 atomically replace한다. 채팅에는
`## Diagnosis`, `## Action` 및 필요한 uncertainty만 남긴다. archive, lifecycle state
또는 중복된 raw output은 만들지 않는다.

다음 terminal status 중 하나를 사용한다:

- `Pass`: diagnosis와 routing이 완료되었다.
- `Fail`: deterministic diagnosis/experiment claim이 gate를 위반했다.
- `Blocked`: 필요한 permission, decision 또는 environment를 사용할 수 없다.
- `Unverifiable`: provenance, reproduction, cause 또는 metric을 검증할 수 없다.
- `NotApplicable`: 적격한 Agent Skill incident가 없다.

## Precautions

- Do not assume the skill body is the cause.
- Do not patch an unreproduced incident based only on wording intuition.
- Do not change correctness, safety, or holdout behavior to reduce resource usage.
- Do not use fixed repeated runs or judge majority to manufacture confidence.
- Do not expose expected answers, secrets, or private evidence in prompts.
- Do not mutate the canonical skill or automatically invoke a downstream skill.
