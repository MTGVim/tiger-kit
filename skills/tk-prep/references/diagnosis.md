<!-- tigerkit:`shared-execution-protocol`; `canonical`=skills/tk-prep/references/diagnosis.md -->

# Difficult bug diagnosis

Read this document only for bugs with an unknown cause, `intermittent/flaky` behavior,
a `performance regression`, environment/time/network/state dependence, or multiple
`plausible cause`s. When repository evidence makes the cause clear and an
`exact regression` RED can be written immediately at the current `observable seam`, skip this
procedure and go directly to [Behavior-first testing](testing.md).

The goal is not diagnosis ceremony. Before committing to the first unsupported
`fix hypothesis`, establish a **`red-capable feedback loop` that judges the symptom itself**.
Code, test, and `runtime` exploration to find a reproduction surface is allowed.

## Judgment loop

Choose the smallest applicable loop:

- a focused test or existing regression command;
- CLI/`curl`, a browser probe, or saved-trace replay;
- a one-off probe or `fuzz/property input`;
- `git bisect` or a `known-good differential comparison`;
- a performance baseline, profiler, or query plan.

The loop must judge the `exact symptom`, be `deterministic` or have a fixed high
reproduction rate, run quickly, and be `agent-runnable`. Preserve the command actually
run and de-identified result as evidence. If it is slow or `flaky`, pin the
`seed/input/environment` and reduce it to a minimal reproduction.

For intermittent behavior, a negative probe reports only the observed sample and rate,
such as `0 failures in 40 trials`; without a known rate and adequate sample, classify it
as not yet reproduced rather than refuted. When a rare failure occurs, preserve its run-owned
logs, screenshots, dumps, and other artifacts before any rerun that could overwrite or delete
them; without that evidence, keep the cause unproven.

If no adequate loop can be built, record the attempted `seam`s, failure evidence, and
remaining risk. A `Testability/architecture gap` may become a finding candidate, but do
not replace it with an arbitrary abstraction or speculative fix.

## Hypotheses and probes

Only after the loop is `red-capable`, rank a small set of evidence-backed
`falsifiable hypothesis` candidates. Each probe distinguishes one prediction and changes one variable
at a time. Discard hypotheses contradicted by results and keep reducing the reproduction.

Prefer `Targeted debugger/inspection`; add temporary logging only at required
boundaries. Give every temporary log a unique searchable `prefix`. For a performance
regression, prefer `baseline/profiler/bisect` over indiscriminate logging.

When this procedure runs as an SDD diagnostic leaf, stop after establishing the evidence-backed cause or
remaining uncertainty, ownership boundary, and red-capable seam. Return that bounded diagnosis to the
controller before any product remediation; the controller owns routing back to the current `Unit` or
preparation/reapproval.

## TDD convergence and cleanup

After finding the correct `regression seam`, join RED → GREEN → REFACTOR in
[Behavior-first testing](testing.md), apply the minimal fix, and verify the related
suite. Before completion, search for the unique `prefix`, one-off probes, saved traces,
and diagnostic artifacts; remove only those owned by this run.

Do not place passwords, tokens, OTPs, cookies, sessions, credentials, or sensitive
inputs in commands, logs, traces, or reports. De-identify required evidence. Do not
create a new public skill, persistent diagnosis ledger, or global state.
