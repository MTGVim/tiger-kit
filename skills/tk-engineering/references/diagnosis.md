<!-- tigerkit:`shared-execution-protocol`; `canonical`=skills/tk-engineering/references/diagnosis.md -->

# Difficult bug diagnosis

Read after the first reproduction attempt misses the reported symptom, before communicating
non-reproduction, or for an unknown cause, intermittent behavior, performance regression,
environment/time/network/state dependence or multiple plausible causes. When repository evidence makes the cause clear and an
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

Derive the judgment from the reporter's symptom, not a suspected cause. For an unclickable
screen, try the blocked interaction on an unrelated control and check its event recipient
or hit target; check focus/input or scrolling when that is the reported failure. A normal
screenshot, responsive main thread or absent suspected overlay does not establish that
clicks reach their intended target. Route browser probes through `tk-browser-verify`.

For intermittent behavior, a negative probe reports only the observed sample and rate,
such as `0 failures in 40 trials`; without a known rate and adequate sample, classify it
as not yet reproduced rather than refuted. When a rare failure occurs, preserve its run-owned
logs, screenshots, dumps, and other artifacts before any rerun that could overwrite or delete
them; without that evidence, keep the cause unproven. Configure probes to exclude secrets and
sensitive inputs, then save each probe's complete safe raw output to a run-owned file before
filtering or summarizing it. Preserve exit status and analyze that saved output if a filter fails;
do not repeat a shared-test-data mutation merely to recover its lost judgment.

If no adequate loop can be built, record the attempted `seam`s, failure evidence, and
remaining risk. A `Testability/architecture gap` may become a finding candidate, but do
not replace it with an arbitrary abstraction or speculative fix.

## Timing and environment after a missed reproduction

When animation/transition, refetch, Suspense/lazy loading, debounce or retry can affect the
symptom, treat latency and event order as variables. A dev server or proxy can move a request
outside a race window; faster responses can expose a race that slower local responses hide.
Before a non-reproduction conclusion or reporter-facing draft, inspect the reporter-matching
build in an accessible deployed test environment. If unavailable or still inconclusive,
change one timing variable in an authorized isolated local probe: lower request latency,
add latency, or widen the transition window. Bypass a dev proxy only when the same test
endpoint, account and access boundaries remain intact. Record actual request/transition
timings, environment/build, the attempted interaction and its result.

These are diagnostic probes, not product fixes or permission to mutate test data. Existing
mutation/authentication rules still apply; never use production as the substitute. If neither
test-environment access nor a safe local timing probe is available, report the precise gap
and `not yet reproduced in the checked conditions`; do not fabricate a trial or refute the report.

## Hypotheses and probes

Only after the loop is `red-capable`, rank a small set of evidence-backed
`falsifiable hypothesis` candidates. Each probe distinguishes one prediction and changes one variable
at a time. Discard hypotheses contradicted by results and keep reducing the reproduction.

Server logs constrain server-side hypotheses. Fast responses or missing server errors cannot
disprove client-only rendering, focus, overlay or event-delivery symptoms; observe those in
the client and retain the distinction between unobserved and absent.

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
