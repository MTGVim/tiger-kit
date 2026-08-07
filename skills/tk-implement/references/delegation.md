# Delegation

## Definitions

`direct` means the current agent owns implementation. Non-agent tools such as
context-mode, MCP, search, static analysis, browser tooling inside the required
browser contract, sandboxes, subprocesses, test runners, formatters, linters,
and type checkers are compatible with direct work and are not delegation.

`delegated` means transferring implementation ownership to one autonomous
implementor agent. A tool or subprocess does not make work delegated.

## Decision

Prefer direct when any are true: the change is small or mechanical,
concentrated in one or a few files, touches shared or tightly coupled code,
requires tight implementation-verification loops, has unresolved cause/design/
scope, depends on the controller's current context, costs more to brief than to
implement, or has no compatible implementor path.

Consider delegated only when all are true: the goal and completion criteria are
Ready; included/excluded scope transfers independently; entry points,
decisions, and verification are clear; shared-file conflict risk is low; the
task is implementation rather than design exploration; full controller context
is unnecessary; isolation or controller-context preservation has material
value; and a compatible implementor path is available. Size alone is not
sufficient.

Risk is classified separately. `direct + low-risk`, `direct + high-risk`,
`delegated + low-risk`, and `delegated + high-risk` are all valid.

## Implementor contract

Give one implementor:

- goal, included scope, and excluded scope;
- relevant files or entry points;
- confirmed decisions and TDD mode;
- verification commands or expectations;
- a self-review requirement against the same unit scope and R/AC;
- prohibited actions;
- required diff, self-review evidence, verification results, and remaining-risk
  return.

The implementor does not create another agent, re-delegate, invoke a
user-invoked TigerKit skill, expand scope, mix unrelated refactors, commit,
push, create a PR, merge, tag, release, or publish.

## Implementor resolution

After `delegated` and its tier are fixed, resolve the implementor before
dispatch; the tier is not a provider, model alias, or agent by itself.

1. Query the selected host's candidate roster and collect each stable
   implementor identifier, writable tools, model/profile, effort backing, and
   read-only flag.
2. Reject candidates that cannot edit the unit, lack required tools, or are
   read-only investigation/planning personas such as `Explore` or `Plan`.
3. Prefer the v2 managed `agent` mapping when it is a writable candidate that
   satisfies the unit. Otherwise choose the first tier-compatible writable
   candidate in the host's stable roster order; do not invent a provider alias.
4. Pass the selected identifier and tier to dispatch and record the
   `resolved implementor`, dispatch values, and selection reason in the unit
   result, handoff/evidence, and implementation ledger.

If no suitable candidate exists, an inferred optimization falls back to
`direct` plus the current model and reports the transition and reason in the
unit result and implementation ledger. A required override that cannot be
satisfied is `Blocked`; never substitute a read-only or unrelated candidate
silently.

The current agent inspects the actual diff, request compliance, and
verification evidence, adjudicates findings, and owns the bounded fix loop in
[review-boundary.md](review-boundary.md). Rounds 1–3 resume the original
implementor when possible; a fresh implementor may receive the same brief and
open findings when resumption is impossible. Never accept delegated output
without controller Built-in review. Final verification and commit remain with
the current agent.
