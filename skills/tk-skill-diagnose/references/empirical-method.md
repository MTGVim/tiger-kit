# 경험적 진단 방법

입력 단계에서 정확히 하나의 target과 incident를 확인한 뒤에만 이 reference를 읽는다.
넓은 최적화가 아니라 causal diagnosis에 맞춘 경험적 prompt tuning이다.

## 1. 정적 일관성

fresh execution 전에 frontmatter description과 body를 비교한다:

- positive 및 negative triggers;
- capability 및 output promises;
- approval, mutation, failure 및 recovery owners.

Description에만 있는 promise, body에만 있는 behavior 및 모순되는 owner는 가설이다.
정적 일관성만으로는 runtime cause를 증명할 수 없다.

## 2. 가장 작게 결정하는 set 고정

experiment 전에 다음을 고정한다:

```text
Incident: observed prompt와 expected/observed result
Control: suspected cause를 구별하는 nearest adjacent behavior
Must preserve: critical behavior, safety, routing, authority 및 host boundary
Metric: actual anchor, labeled proxy 또는 unavailable
```

첫 incident/control pair로 failure planes를 구분할 수 없을 때만 scenario를 추가한다.
generic holdout은 optional이며 default ceremony가 아니다.

## 3. 새 실행(Fresh execution)

clean matched context에서 incident를 한 번 실행한다. 결과가 불안정하거나 metric
threshold에 가깝거나 control과 비교해 모호할 때만 반복한다. diagnosis 또는 candidate를
이미 본 executor는 fresh하지 않다.

normal deliverable을 우선한다. adapter가 diagnostic suffix를 지원할 때만 다음을 수집한다:

```json
{
  "trace": {
    "understanding": "ok | stuck | skipped",
    "planning": "ok | stuck | skipped",
    "execution": "ok | stuck | skipped",
    "formatting": "ok | stuck | skipped"
  },
  "unclear_points": [
    {
      "issue": "observed event",
      "cause": "candidate cause",
      "general_fix_rule": "class-level prevention rule"
    }
  ],
  "discretionary_fill_ins": [],
  "retries": 0
}
```

executor에게 expected answers, judge criteria 또는 baseline/candidate verdicts를
공개하지 않는다. 잘못된 diagnostics는 evaluation-plane evidence이며, 검증된
deliverable을 자동으로 무효화하지 않는다.

## 4. 양면 evidence

다음을 결합한다:

- deterministic assertions와 Git/path/runtime evidence;
- selection/loading 및 host/adapter events;
- phase-local trace 및 discretionary fill-ins;
- 사용 가능한 경우 actual token, duration, tool, nested-call 또는 retry metrics.

Self-report는 하나의 observation일 뿐, 원인을 입증하기에 충분하지 않다. 모든 causal
claim에는 instruction, routing, runtime, repository 또는 eval anchor가 필요하다.

## 5. 최소 experiment

incident/control evidence만으로 cause를 직접 증명할 수 없을 때만 run-owned isolated
checkout을 사용한다. 먼저 suspected cause와 이를 구분할 expected result를 명시한다.
하나의 root-cause theme만 바꾸고 affected scenario를 가장 작게 실행한다.

experiment는 causality를 confirm 또는 reject하며 canonical patch가 아니다. 두 번째
experiment에는 첫 결과에서 나온 새 specific cause가 필요하다. 같은 failure가 반복된
뒤 wording changes를 쌓지 않는다.

## 6. 처분(Disposition)

- 검증된 skill objective → 간결한 `learn-ready` handoff;
- 독립적으로 유용한 새 skill → `learn-candidate`;
- grader/harness/fixture defect → `eval-owner`;
- loader/adapter/host defect → `host-owner`;
- consumer override/configuration → `local-only`;
- not reproduced 또는 target correct → `no-change`;
- decisive evidence missing → `unverifiable`.

실제 telemetry 또는 다섯 개가 넘는 evidence row가 필요할 때만 temporary diagnostic
artifact를 작성한다. 지속적인 optimization ledger는 만들지 않는다.
