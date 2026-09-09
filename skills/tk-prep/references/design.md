# Conditional design comparison

Read this document only for `material architecture uncertainty` that
`Repository precedent` and `current evidence` do not resolve. Unless all four conditions hold,
recommend repository precedent or the simplest reversible choice and continue
preparation without extra procedure.

1. The choice is difficult to reverse, such as an `interface/seam/schema/architecture/migration`.
2. At least two genuinely viable designs exist.
3. A wrong choice has meaningful rework, compatibility, data, or testing cost.
4. Current repository evidence does not sufficiently determine one option.

## Comparison

The controller creates at least two brief `materially different design`s. Renamed
variants do not count. Compare each option using:

- existing reuse and repository fit;
- simplicity and the complexity it hides;
- observable testing `seam`s;
- `blast radius` and dependency impact;
- migration, rollback, and compatibility cost;
- `cost-if-wrong`.

Recommend the option with the strongest evidence and explain why instead of listing a
menu. A hybrid that combines advantages from different options is allowed when it is
actually simpler. If repository precedent is found, stop the comparison and recommend
that precedent.

## Runtime system lens

When the material choice changes live traffic/data flow, asynchronous processing,
distributed components, external dependencies, or failure containment, compare the
candidate designs against the runtime requirements that can actually change topology
or limits. Establish only relevant constraints and do not invent precision:

- steady/peak/burst load, data volume, and bounded resource use;
- latency or freshness expectations and acceptable degradation;
- availability, durability, ordering, duplication, or loss guarantees when applicable;
- security/privacy boundaries and sensitive-data retention;
- observability, incident-debugging path, operational complexity, and cost.

For each candidate, trace relevant failure modes instead of evaluating only the happy
path. Consider component crash/restart, dependency latency/outage, overload and
backpressure, retry amplification, queue lag, partial failure, duplicate/lost/out-of-order
delivery, stale state, observability/notification failure, and abuse only when the design
can realistically encounter them. For each material mode, establish:

1. `effect`: what user/system behavior degrades or fails;
2. `containment`: what prevents propagation or unbounded resource growth;
3. `detection`: what runtime evidence lets an operator recognize it promptly;
4. `recovery`: automatic recovery, fallback, rollback, replay, or explicit manual action;
5. `validation`: a test, load experiment, fault injection, replay, or measurable production check.

Prefer keeping telemetry, monitoring, notification, and other control-plane paths off the
request critical path unless requirements demand otherwise. Reuse existing trustworthy
telemetry/queues before creating a duplicate observation path. If incident response depends
on delayed durable logs, identify what bounded, redacted evidence is available immediately
and how it correlates with later durable records.

Do not turn this lens into a mandatory distributed-systems checklist. Skip irrelevant
constraints and failure modes, and surface only findings that change the recommendation,
AC, validation plan, rollback, or accepted risk.

## Optional exploration and review protection

Choose subagent `fan-out` only for a complex case where at least two independent
explorations materially improve confidence. If the current host lacks `fan-out`, the
controller performs the same comparison; this is not `Blocked`. Do not persist agent
count, provider, model, or reasoning values in this reference or the `Seed`.

This heuristic is a proposal and exploration aid. Reviewers do not use design terms as
independent failure criteria unless they were actually promoted into repository
standards, approved `Seed` decisions, or ACs. Do not create a TigerKit-owned design
ledger or new public workflow.
