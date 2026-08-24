# Empirical diagnosis method

Read this reference only after input has identified exactly one target and incident. It
is empirical prompt tuning for causal diagnosis, not broad optimization.

## 1. Static coherence

Before fresh execution, compare the frontmatter description with the body:

- positive and negative triggers;
- capability and output promises;
- approval, mutation, failure, and recovery owners.

A description-only promise, body-only behavior, or conflicting owner is a hypothesis.
Static coherence alone does not prove the runtime cause.

## 2. Freeze the smallest deciding set

Before experimentation, freeze:

```text
Incident: observed prompt and expected/observed result
Control: nearest adjacent behavior that distinguishes the suspected cause
Must preserve: critical behavior, safety, routing, authority, and host boundaries
Metric: actual anchor, labeled proxy, or unavailable
```

Add a scenario only when the first incident/control pair cannot distinguish the failure
plane. A generic holdout is optional, not default ceremony.

## 3. Fresh execution

Run the incident once in a clean matched context. Repeat only when the result is
unstable, close to a metric threshold, or ambiguous against the control. An executor
that has already seen the diagnosis or candidate is not fresh.

Prefer the normal deliverable. Collect the following only when the adapter supports a
diagnostic suffix:

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

Do not reveal the expected answer, judge criteria, or baseline/candidate verdict to the
executor. Incorrect diagnostics are evaluation-plane evidence and do not automatically
invalidate a verified deliverable.

## 4. Two-sided evidence

Combine:

- deterministic assertions and Git/path/runtime evidence;
- selection/loading and host/adapter events;
- phase-local trace and discretionary fill-ins;
- actual token, duration, tool, nested-call, or retry metrics when available.

Self-report is one observation, not sufficient proof of cause. Every causal claim needs
an instruction, routing, runtime, repository, or evaluation anchor.

## 5. Minimal experiment

Use a run-owned isolated checkout only when incident/control evidence cannot directly
prove the cause. State the suspected cause and distinguishing expected result first.
Change one root-cause theme and run the smallest affected scenario.

An experiment confirms or rejects causality; it is not a canonical patch. A second
experiment requires a new specific cause learned from the first result. Do not stack
wording changes after the same failure repeats.

## 6. Disposition

- verified skill objective → concise `learn-ready` handoff;
- independently useful new skill → `learn-candidate`;
- grader/harness/fixture defect → `eval-owner`;
- loader/adapter/host defect → `host-owner`;
- consumer override/configuration → `local-only`;
- not reproduced or target correct → `no-change`;
- decisive evidence missing → `unverifiable`.

Write a temporary diagnostic artifact only when actual telemetry or more than five
evidence rows require one. Do not create a persistent optimization ledger.
