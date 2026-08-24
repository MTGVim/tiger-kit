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

## Optional exploration and review protection

Choose subagent `fan-out` only for a complex case where at least two independent
explorations materially improve confidence. If the current host lacks `fan-out`, the
controller performs the same comparison; this is not `Blocked`. Do not persist agent
count, provider, model, or reasoning values in this reference or the `Seed`.

This heuristic is a proposal and exploration aid. Reviewers do not use design terms as
independent failure criteria unless they were actually promoted into repository
standards, approved `Seed` decisions, or ACs. Do not create a TigerKit-owned design
ledger or new public workflow.
