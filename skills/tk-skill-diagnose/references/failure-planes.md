# Failure planes and evidence

Do not begin by assuming a wording defect. Classify every observed symptom against one
or more evidence-backed planes.

| Plane | Meaning | Representative evidence |
|---|---|---|
| `selection` | Skill selected when unnecessary, or not selected when required | trigger train/validation result, selected skill |
| `loading` | Selection occurred but the body did not load | adapter `skill_loaded`, loaded-skill list |
| `understanding` | Scope, terms, or input contract misunderstood | fresh trace, output evidence |
| `planning` | Wrong owner, branch, sequence, or decision loop | trace, retries, discretionary fill-in |
| `execution` | Tool, command, verification, or mutation failed | command, file, Git, runtime evidence |
| `formatting` | Output or receipt ownership violated | output assertion, structured comparison |
| `evaluation` | Grader/assertion misclassified correct output | deliverable versus criterion/mechanical evidence |
| `compatibility` | Host invocation, loading, tool, or metadata behavior differs | Claude Code/Codex/Hermes matrix |
| `efficiency` | Correct output consumed avoidable resources | matched baseline/candidate metrics |

Record stability for every plane, but do not record it as a separate causal plane:

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

- When output is correct and only grading fails, inspect `evaluation` before expanding
  the skill body.
- When selection is correct but `skill_loaded` differs, inspect `loading` or
  `compatibility`.
- When the same decision repeats, find the earliest weak phase and blocker fingerprint
  before blaming execution.
- When resource use grows, identify the increased phase, retry, reference descent, tool
  loop, nested call, or fan-out.
- Require deterministic evidence beside every self-reported cause.

## Efficiency comparison

Verify at least one anchor:

- previous stable ref;
- no-skill baseline;
- a prior verified run of the same prompt;
- explicit token/time/tool threshold;
- the candidate under comparison.

Match the prompt, host, model/config, tools, repository state, and at least two trials.
The eval adapter reports `execution_identity` from actual host metadata, never a
requested model or an agent's self-report. The common runner pairs exact host,
case, trial and prompt hashes before comparative claims. Missing/different model
identity or mismatched observable config makes comparison `Unverifiable`; keep
individual measurements and candidate-only safety failures. Config omitted on
both sides proves no config equivalence; report only the observed model match.
Do not select, pin, reroute or retry a model to force comparability.
If a metric is unavailable, leave it `null`/`Unverifiable`; never estimate it.

Maintenance provenance: compared `ayghri/i-have-adhd` at
`839872f9d1cd634fed642b4589ce7226199cc15f`, `scripts/run_evals.py`, and the
`e9fee1addbb11073131d4663fe673a4df38d3938` implementation/test diff.
`keep` missing/invalid metric honesty; `adapt` observed identity and exact pairing
to TigerKit's runner, refusing two unknown models; `omit` upstream scoring,
provider routing and harness. Upstream runtime tests were not rerun here.

Resource savings cannot offset:

- a critical or mechanical assertion regression;
- a safety, routing, or mutation regression;
- recurring new `stuck | skipped` states;
- a retry regression from a zero baseline;
- a control or holdout regression.

Without a matched anchor, report the current measurement as `Profile only`.

## Diagnostic verdict

- `Fail`: deterministic/critical regression, recurring new weak phase, recurring retry
  regression, or trading correctness for savings.
- `Concern`: one unclear point/fill-in or unmatched resource increase.
- `Pass`: normal checks pass, no new phase/retry/holdout regression recurs, and any
  claimed efficiency improvement is matched and verified.
- `Unverifiable`: fresh execution, parsing, provenance, or a required matched metric is
  unavailable after bounded attempts.

The diagnostic verdict is evidence inside the diagnosis receipt; it is not the skill's
terminal status.
