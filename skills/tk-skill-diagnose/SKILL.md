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

# Agent Skill 진단

정확히 하나의 Agent Skill target과 하나의 observed 또는 measured anomaly에만 사용한다.
직접 선택은 허용한다. 자동 선택에는 target과 incident evidence가 필요하며,
`skill`, `debug`, `performance` 같은 일반 단어만으로는 부족하다.

이 skill은 진단만 수행한다. canonical skill을 작성하거나 catalog를 최적화하거나
최종 patch를 소유하지 않는다. 검증된 skill objective는 `tk-learn` 을 유일한
`create | improve | merge` writer로 거쳐 라우팅한다. canonical source skill을
의미적으로 변경하지 않는다.

## 입력 게이트

다음을 기록한다:

- exact target package/path, installed ref, origin, host 및 invocation;
- incident prompt, expected behavior 또는 metric anchor 및 observed result;
- 사용 가능한 transcript/event, file, Git, eval 또는 resource evidence;
- 알려진 consumer override 또는 host configuration.

누락값은 `unverified` 로 표시한다. incident나 metric anchor가 없다는 것은
`NotApplicable` 이 아니다. fresh execution이 없거나 필요한 evidence에 접근할 수
없으면 원인을 추론할 권한이 아니라 `Unverifiable | Blocked`다.

incident, exact target, host/invocation, prompt, expected 및 observed result, evidence를
명시한 `learn-ready` handoff는 한 번만 수락한다. 진단 단계에서는 `tk-learn` 을
호출하지 않으며, 동일한 target + incident + blocker cycle을 반복하지 않는다.

## 증거 순서

다음 순서로 결정한다:

1. target provenance, description/body 일관성, deterministic assertions,
   repository state 및 adapter/host evidence;
2. 가장 작은 fresh incident 재현;
3. 의심되는 failure plane을 구분하는 하나의 인접 control;
4. 인과관계를 입증하는 데 필요할 때만 run-owned minimum experiment.

재현 결과는 `Reproduced | Not reproduced | Inconclusive` 중 하나다. Self-report는
가설을 제안할 뿐 root cause를 증명하지 않는다. 첫 결과가 불안정하거나
control과의 경계가 모호할 때만 fresh run을 반복한다. 좁은 evidence로 원인을 결정할
수 있는데도 fixed trial counts, generic holdout suite 또는 rubric scoring을 요구하지
않는다.

해당할 때만 다음 references를 읽는다:

- [failure plane와 evidence](references/failure-planes.md)
- [경험적 진단 방법](references/empirical-method.md)
- [upstream issue 익명화](references/upstream-issue-anonymization.md)

## 효율성 게이트

Resource claim에는 matched baseline, historical run, repository threshold 또는
명시적 budget이 필요하다. 그렇지 않으면 observed value는 profile만 기록하고
방향은 `Unverifiable` 로 둔다. tokens, time, calls, retries 또는 fan-out이 적다는
이유로 correctness 또는 safety regression을 상쇄하지 않는다.

## 작업 흐름

1. **동결(Freeze)**: exact incident, target ref, must-preserve behavior, affected host 및
   신뢰할 수 있는 evidence/metric을 고정한다.
2. **재현(Reproduce)**: clean context에서 한 번 재현한다. 결과를
   `Reproduced | Not reproduced | Inconclusive` 로 분류한다.
3. **대조(Control)**: nearest alternative를 비교한다. loader와 body, parent와 child,
   candidate와 grader, 한 host와 다른 host, correctness와 resource cost를
   구분한다.
4. **격리(Isolate)**: 검증된 failure plane을 다음 중에서 선택한다:
   `selection | loading | instruction | planning | execution | formatting |
   evaluation | compatibility | efficiency | local override`.
5. **필요할 때만 실험(Experiment)**: 하나의 run-owned isolated checkout에서만 수행한다.
   하나의 root-cause theme만 바꾸고 원인을 confirm 또는 reject한다. experiment를
   canonical fix로 취급하지 않는다.
6. **라우팅(Route)**: 검증된 evidence에 따라 다음 owner를 정한다.

결론적인 cause 또는 disposition에서 멈춘다. 첫 experiment가 새로운 구체적 cause를
드러낸 경우에만 두 번째 experiment를 허용한다. run-owned isolation만 정리하며
canonical target을 다시 쓰거나 patch하지 않는다.

## 🔴 CHECKPOINT / STOP · 다음 단계 진행 게이트

각 checkpoint를 통과하기 전에는 다음 단계, experiment 또는 handoff를 시작하지 않는다.

- **입력 checkpoint**: exact target, eligible Agent Skill incident 및 incident evidence가
  있다. ordinary code bug처럼 적격 Agent Skill incident 자체가 아니면 `NotApplicable` 로
  멈춘다. incident 또는 metric anchor가 필요한데 누락·미검증이면 `NotApplicable` 이
  아니며 `Blocked | Unverifiable` 로 멈춘다.
- **재현 checkpoint**: fresh result를 `Reproduced | Not reproduced | Inconclusive` 중
  하나로 기록한다. `Inconclusive` 이면 cause나 route를 확정하지 않고 `Unverifiable` 로
  멈춘다.
- **격리 checkpoint**: 하나의 failure plane과 이를 구분하는 adjacent control이
  evidence로 확인되었다. 아니면 root-cause claim을 하지 않고 `Unverifiable` 로 멈춘다.
- **라우팅 checkpoint**: 하나의 구체적이고 testable한 objective와 must-preserve
  boundary가 검증되었다. 아니면 `learn-ready` handoff를 emit하지 않는다.
- **🛑 STOP**: `learn-ready` 를 emit한 뒤에도 이 skill은 `tk-learn` 을 호출하거나
  canonical skill/catalog를 mutate하지 않는다. 별도의 명시적 invocation을 기다린다.

## 라우팅

### 검증된 skill objective: `learn-ready`

하나의 기존 package와 하나의 구체적이며 testable한 objective가 검증된 경우에만
사용한다. 다음을 emit한다:

```text
Target package: skills/<name>/
Objective: <one observable correction or cost reduction>
Evidence: <incident, control, code, event, or metric references>
Must preserve: <behavior, safety, routing, authority, and host boundaries>
Affected execution: <smallest fresh scenario that decides the objective>
Metric: <actual measurement, labeled proxy, or unavailable>
Incident: <stable ID or source reference>
```

이는 이후 명시적으로 실행하는 `tk-learn` 의 input이다. 여기서 호출하지 않는다.

### 기타 처분

- `learn-candidate`: 독립적으로 유용한 새 skill이 필요하다.
- `eval-owner`: grader, fixture, harness 또는 assertion이 검증된 원인이다.
- `host-owner`: loader, metadata, adapter 또는 host runtime이 검증된 원인이다.
- `local-only`: consumer override/configuration이 incident를 일으킨다.
- `no-change`: target behavior가 올바르거나 incident가 재현되지 않는다.
- `unverifiable`: evidence로 안전하게 결정할 수 없다.

external consumer repository에서는 익명화된 issue를 제안하기 전에 upstream
origin/ref와 현재 upstream behavior를 검증한다. duplicate check를 마친 redacted
proposal만 `upstream-draft-ready` 로 분류하며, 자동으로 create, comment, label 또는
publish하지 않는다.

## 결과

`## Diagnosis` 로 시작하고 이어서 `## Action` 을 출력한다. 필요할 때만
`## Remaining uncertainty` 를 추가한다.

하나의 incident에는 짧은 설명을 사용한다. 여러 symptom이 하나의 cause를 공유하면
`ID | Incident | Root cause` 형식으로 cause마다 안정적인 `SD-##` row 하나를 유지한다.
reproduction verdict, verified failure plane, evidence, route 및 정확한 next handoff를
보고한다. raw logs, transcripts, screenshots, secrets 또는 반복된 run narration을
복사하지 않는다.

experiment evidence가 다섯 row를 넘거나 이후 resume에 정확한 references가 필요하면
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

## 주의사항

- skill body가 원인이라고 가정하지 않는다.
- 재현되지 않은 incident를 wording intuition만으로 patch하지 않는다.
- 낮은 resource 사용을 위해 correctness, safety 또는 holdout behavior를 바꾸지 않는다.
- confidence를 만들기 위해 fixed repeated runs 또는 judge majorities를 사용하지 않는다.
- expected answers, secrets 또는 private evidence를 prompts에 유출하지 않는다.
- canonical skills를 mutate하거나 downstream skills를 자동으로 invoke하지 않는다.
