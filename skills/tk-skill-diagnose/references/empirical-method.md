# Empirical diagnostic method

Use this reference after intake passes. The method adapts mizchi's
`empirical-prompt-tuning` for incident diagnosis rather than broad prompt
optimization.

## Static iteration 0

Before dispatch:

1. List the positive and negative trigger promises in the description.
2. List each capability promise.
3. Locate its body owner in workflow, failure, approval, mutation, or output
   contracts.
4. Record description-only promises, body-only behavior, and contradictory
   owners as hypotheses.

Static consistency can narrow reproduction but cannot prove cause.

## Freeze scenarios and requirements

Use this bounded set:

```text
A. incident/median: the observed prompt
B. nearby control/edge: adjacent behavior that should remain valid
C. holdout: an existing case not used to choose the candidate
```

Prefer existing trigger and behavior evals in TigerKit. In an external
repository, normalize the actual incident without persisting private data.
Freeze three to seven requirements per scenario, including at least one
`[critical]` requirement. Do not change requirements or critical tags after
seeing a candidate.

## Fresh execution

Run the target twice in clean, matched contexts. Use fresh executors for every
candidate re-evaluation; an executor that saw the previous diagnosis is not
fresh. If fresh dispatch is unavailable, stop empirical claims as
`Unverifiable`.

The normal deliverable remains primary. A separate diagnostic suffix asks only
for:

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
      "cause": "instruction-level cause",
      "general_fix_rule": "class-level prevention rule"
    }
  ],
  "discretionary_fill_ins": [],
  "retries": 0
}
```

Empty issue/fill-in arrays are valid. Do not ask the executor to restate an
expected output, judge criterion, mechanical expectation, or baseline/candidate
verdict. Malformed diagnostics are an evaluation-plane record, not proof that
the normal deliverable failed.

## Two-sided evidence

Capture:

- normal assertions and deterministic Git/path/runtime evidence;
- phase-local trace;
- `Issue / Cause / General Fix Rule`;
- discretionary fill-ins and retries;
- available token, duration, tool, nested-call, and fan-out metrics.

Qualitative ambiguity is primary; resource metrics are supporting evidence.
Connect each causal claim to at least one instruction, runtime, routing, or eval
artifact. Do not accept self-report alone.

## Minimum candidate

Before creating a temporary candidate, state:

```text
Frozen requirement/assertion served
General Fix Rule applied
Expected correctness effect
Expected resource effect
```

Change one root-cause theme per candidate. Related micro-edits may remain one
theme; unrelated fixes wait. If the same failure class persists after two
themes, report a structural problem rather than stacking patches.

## Convergence and holdout

A final candidate needs two consecutive fresh checks with:

- no new unclear point;
- no repeated `stuck | skipped`;
- no critical/control regression;
- no retry regression;
- matched resource improvement when efficiency is claimed.

Run one unused holdout last. Any correctness, safety, routing, mutation, or
holdout regression rejects the candidate regardless of token/time savings.

Maintain a run-local failure ledger keyed by normalized General Fix Rule.
Repeated patterns explain convergence or structural divergence; the ledger is
never global TigerKit state.

## Cost boundary

Default to one target, one incident, one nearby control, one holdout, two trials
per scenario, two concurrent fresh executors, and two candidate themes. Stop on
repeated equivalent blockers, rate limits, or executor failure rather than
retrying indefinitely.
