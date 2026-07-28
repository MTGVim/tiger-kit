# Failure planes and evidence

Do not begin with a wording-defect assumption. Classify every observed symptom
against one or more evidence-backed planes.

| Plane | Meaning | Representative evidence |
|---|---|---|
| `selection` | Skill was selected when it should not be, or missed when required | trigger train/validation result, selected skill |
| `loading` | Selection occurred but the body was not loaded | adapter `skill_loaded`, loaded-skill list |
| `understanding` | Scope, terms, or input contract were misunderstood | fresh trace, output evidence |
| `planning` | Owner, branch, sequence, or decision loop was wrong | trace, retries, discretionary fill-in |
| `execution` | Tool, command, verification, or mutation failed | command, file, Git, runtime evidence |
| `formatting` | Output or receipt ownership was violated | output assertion, structured comparison |
| `evaluation` | Correct output was misclassified by grader/assertion | deliverable versus criterion/mechanical evidence |
| `compatibility` | Host invocation, loading, tool, or metadata behavior differs | Claude Code/Codex/Hermes matrix |
| `efficiency` | Correct output consumes avoidable resources | matched baseline/candidate metrics |

Record stability across all planes rather than as one causal plane:

```text
reproduction rate
selected-skill variance
terminal-state variance
assertion-pass variance
retry variance
token/duration variance
tool/nested-call/fan-out variance
```

## Isolation rules

- If output is correct and only grading fails, inspect `evaluation` before
  enlarging the skill body.
- If selection is correct but `skill_loaded` differs, inspect `loading` or
  `compatibility`.
- If the same decision repeats, locate the earliest weak phase and blocker
  fingerprint before blaming execution.
- If resource use grows, identify the phase, retry, reference descent, tool
  loop, nested call, or fan-out that grew.
- Require deterministic evidence beside every self-reported cause.

## Efficiency comparison

At least one anchor must be verified:

- previous stable ref;
- no-skill baseline;
- prior verified run of the same prompt;
- explicit token/time/tool threshold;
- a candidate under comparison.

Match prompt, host, model/config, tools, repository state, and at least two
trials. Missing metrics remain `null`/`Unverifiable`; never estimate them.

Resource savings cannot offset:

- critical or mechanical assertion regression;
- safety, routing, or mutation regression;
- repeated new `stuck | skipped`;
- retry regression from a zero baseline;
- control or holdout regression.

Without a matched anchor, report current measurements as `Profile only`.

## Diagnostic verdict

- `Fail`: deterministic/critical regression, repeated new weak phase, repeated
  retry regression, or correctness traded for savings.
- `Concern`: one-off unclear point/fill-in or unmatched resource increase.
- `Pass`: normal checks pass with no repeated new phase/retry/holdout
  regression; a claimed efficiency improvement is matched and verified.
- `Unverifiable`: fresh execution, parse, provenance, or required matched metric
  is unavailable after the bounded attempts.

A diagnostic verdict is evidence inside the diagnosis receipt; it is not the
same as the skill's terminal status.
