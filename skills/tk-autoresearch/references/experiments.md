# Experiment Integrity

Read this only for metric/mechanically evaluated research or consequential noisy results.
Ordinary qualitative research uses its observable evidence and falsifier without extra metric setup.

## Protected evaluation contract

Before comparing candidates, reuse an existing evaluation contract or establish the smallest feasible one:

- metric and direction (`maximize`, `minimize` or equivalence), baseline and baseline revision;
- authoritative evaluation command/evaluator and its version or fingerprint;
- protected evaluation surface: evaluator, metric computation, fixed inputs/data and split semantics;
- candidate-editable surface and acceptance criteria;
- dev/search versus independent acceptance evidence roles, when available.

Keep this identity in canonical research state and the applicable experiment record, not new config keys.
Check protected surfaces before execution and again before accepting the result, including indirect changes
through imports, configuration, data selection or command overrides. A better score obtained by changing the
evaluation contract is invalid improvement evidence and cannot support `KEEP`. Preserve the drift and its
effect; use `INCONCLUSIVE` or `BLOCKED` when the original contract cannot be evaluated safely, rather than
claiming the hypothesis was falsified. Restore only run-owned changes when safe.

A legitimate evaluator correction is a separate contract revision with a fresh baseline and comparable
candidate evaluation. Do not silently compare scores across contract versions or credit the correction as
candidate improvement. Resolve a new user-owned material criterion through the existing question boundary;
routine research setup inside current authority needs no additional approval.

## Search and acceptance evidence

When an independent held-out/acceptance signal already exists or can reasonably be created within current
authority, iterate on dev evidence and fix the candidate before checking independent acceptance for a
direction adoption or consequential conclusion. Apply the recorded acceptance criterion; a dev gain that
fails it cannot establish `KEEP`. Investigate noise, overfitting or split mismatch without tuning to the
held-out cases or moving the threshold to admit that candidate.

Do not repeatedly inspect test/held-out results to steer search. Record any exposure or adaptive reuse
that compromises independence; restore an unexposed acceptance signal when feasible, otherwise state the
limitation and lower the conclusion's strength. Do not relabel a used search signal as held-out evidence.
If separate acceptance evidence is unavailable or unreasonable to create, continue research and report
that limitation in the finding/final synthesis. Do not require a fixed number of splits or a benchmark
scaffold for all research, and do not invent validation evidence.

## Decision-critical noise and replication

When meaningful stochasticity/noise could change an important `KEEP`, direction adoption/rejection,
program conclusion or downstream implementation decision, assess independent repetition before relying
on one result. Choose repetitions by variability, cost and decision importance; use fresh runs/seeds or
independent samples when appropriate. Preserve all comparable outcomes and uncertainty rather than
selecting the luckiest run. Re-reading the same output is not replication.

Deterministic results and repetitions with negligible information value need no ceremonial rerun.
If consequential uncertainty remains and useful repetition is unaffordable or unavailable, retain a
qualified/inconclusive finding or blocker with the replication limit; do not promote an unstable best
score into a confident accepted direction. Replication never widens authority or installs a fixed seed quota.
