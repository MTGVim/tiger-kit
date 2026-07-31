# Empirical diagnostic method

Read this reference only after intake identifies one exact target and incident.
It adapts empirical prompt tuning for causal diagnosis, not broad optimization.

## 1. Static consistency

Before fresh execution, compare the frontmatter description with the body:

- positive and negative triggers;
- capability and output promises;
- approval, mutation, failure, and recovery owners.

Description-only promises, body-only behavior, and contradictory owners are
hypotheses. Static consistency never proves runtime cause.

## 2. Freeze the smallest deciding set

Freeze before experimentation:

```text
Incident: the observed prompt and expected/observed result
Control: the nearest adjacent behavior that distinguishes the suspected cause
Must preserve: critical behavior, safety, routing, authority, and host boundary
Metric: actual anchor, labeled proxy, or unavailable
```

Add another scenario only when the first incident/control pair cannot separate
the failure planes. A generic holdout is optional, not a default ceremony.

## 3. Fresh execution

Run the incident once in a clean matched context. Repeat only when the result is
unstable, close to a metric threshold, or ambiguous against the control. An
executor that saw the diagnosis or candidate is not fresh.

Keep the normal deliverable primary. When the adapter supports a diagnostic
suffix, collect only:

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

Do not reveal expected answers, judge criteria, or baseline/candidate verdicts
to the executor. Malformed diagnostics are evaluation-plane evidence; they do
not automatically invalidate an otherwise verified deliverable.

## 4. Two-sided evidence

Combine:

- deterministic assertions and Git/path/runtime evidence;
- selection/loading and host/adapter events;
- phase-local trace and discretionary fill-ins;
- actual token, duration, tool, nested-call, or retry metrics when available.

Self-report is one observation, never sufficient cause. Every causal claim
needs an instruction, routing, runtime, repository, or eval anchor.

## 5. Minimum experiment

Use a run-owned isolated checkout only when incident/control evidence cannot
prove the cause directly. State the suspected cause and expected distinguishing
result first. Change one root-cause theme and run the smallest affected scenario.

The experiment confirms or rejects causality; it is not the canonical patch.
A second experiment requires a new specific cause from the first result. Do not
stack wording changes after the same failure repeats.

## 6. Disposition

- verified existing-package objective → compact `evolve-ready` handoff;
- new independently useful skill → `learn-candidate`;
- grader/harness/fixture defect → `eval-owner`;
- loader/adapter/host defect → `host-owner`;
- consumer override/configuration → `local-only`;
- not reproduced or target correct → `no-change`;
- missing decisive evidence → `unverifiable`.

Write a temporary diagnostic artifact only when actual telemetry or more than
five evidence rows require it. Never create a durable optimization ledger.
