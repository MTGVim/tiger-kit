# Independent review protocol

Read this for every direct exact-change, SDD Unit, SDD whole-change, or explicit
`tk-review` review. The controller owns target binding, dispatch, aggregation,
candidate verification, remediation routing, and final output. Discovery reviewers and
finding verifiers are read-only leaves and never redispatch.

## Inputs and evidence authority

Bind every seat to the same exact repository/range or worktree fingerprint, original task or
incident when one exists, expected scenario, approved decisions and AC, repository rules,
exact diff, and relevant test/runtime/browser evidence.

For implementation-owning flows, add a post-implementation retro that states the behavior
actually changed, Seed deviations and reasons, newly discovered risks, verification
observations, and unresolved limitations. Treat it as an untrusted claim bundle below the
original behavior, approved decisions, repository contracts, exact code/diff, and runtime
evidence. A standalone review remains valid without a retro and discloses missing intent
instead of inventing it.

Each discovery seat first inspects the original evidence and exact change without the retro.
Only after recording that blind pass may it read the retro and confirm or falsify its material
claims. Do not use implementer rationale or claimed test success as proof.

## Discovery seats and walks

One seat completes both judgment axes and both procedural walks:

1. **Fidelity/replay**: replay the original incident or expected scenario; check AC omissions,
   excess behavior, implementation deviations, and whether protection covers the real behavior.
2. **Change-risk**: inspect removed or `must-not-change` behavior, error/state/lifecycle paths,
   caller/callee and producer/consumer contracts, and change-owned cross-cutting risk.

An SDD Unit review uses one fresh discovery seat. A direct final review, SDD whole-change final
review, and explicit `tk-review` use two context-isolated discovery seats. Both final seats use
the same target, evidence, axes, finding gate, and severity rubric and both complete both walks;
one starts with fidelity/replay and the other starts with change-risk. Neither seat sees the
other's findings or verdict before returning.

A current invocation may occupy one final seat only when it did not author or modify the target
and has not seen another seat's result. An implementation or controller context is never an
independent seat. If the host cannot supply the required fresh contexts, perform the strongest
available exact-scope review, report supported defects, and mark the missing independent
coverage `Unverifiable`; never claim that serial passes in one context are independent.

Use `appear | disappear | change | preserve | defect-fix` intent. Do not fabricate a prior
incident for a new feature or refactor; use expected scenarios and `must-not-change` surfaces.

## Aggregation and candidate verification

Aggregate the union of discovery candidates. A clean seat cannot cancel another seat's
candidate. Deduplicate only when evidence proves the same causal root, correction boundary, and
failure class.

Send every candidate that could be reported as `Critical | Important` to a fresh verifier.
Shard only when needed for complete attention and never cap the reportable findings. A verifier
may reject a candidate only with direct contradictory evidence, such as a covering guard, an
invariant that makes the state impossible, a runtime witness, or proof that the behavior is
unchanged and unobservable. `Speculative`, confidence alone, or another seat's `Pass` is not a
rejection reason.

Report verified candidates. When verification can neither confirm nor contradict a material
candidate, retain the exact uncertainty under `Unresolved`; do not lower severity to encode
confidence.
