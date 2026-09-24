# Independent review protocol

Read this for every direct exact-change, SDD Unit, SDD whole-change, or explicit
`tk-review` review. The controller owns target binding, dispatch, aggregation,
candidate verification, remediation routing, and final output. Discovery reviewers and
finding verifiers are read-only leaves and never redispatch.

## Delegation permissions

Before dispatching any implementer, reviewer, verifier, diagnostic leaf, or delegated controller,
verify from current host/tool evidence that its effective tool and data access is the same as or
narrower than the parent/controller's for the same target environment. Preserve `deny | ask | allow`,
read/path restrictions, approval scope, and publication/destructive-action authority. A read-only
role, prompt instruction, provider name, or static allowlist alone does not prove enforcement.

Bind that evidence to the actual workspace/worktree, repository root, sandbox/container, filesystem
restrictions, remote target, and account/connector context as applicable. Recheck when the environment,
policy, or requested access changes, including on resume. Prior approval, cached decisions, and
review results do not transfer automatically across environments or authorize wider subsequent access.
Do not turn parent `deny` or `ask` into child `allow`; preserve the existing supported approval route
or stop the affected action, without adding automatic elevation or a new approval lifecycle.

Read restrictions cover indirect shell/Git reads and material embedded in prompts, diffs, or tool
results as well as direct file tools. Reuse existing bounded review transport with only authorized
material; filtering a brief does not make broader child tool access safe. Include the applicable
boundary and current evidence in the child brief; leaves stop and return a mismatch to the controller.

If safe inheritance/narrowing cannot be established and broader access is possible, do not dispatch.
Use an already-authorized controller path only when it preserves the restrictions and role obligations;
otherwise return `Blocked | Unverifiable` for the affected work. Controller self-review cannot satisfy
required independent coverage. With verified same-or-narrower access, proceed without extra approval,
a permission registry, durable environment ledger, or re-dispatch ceremony.

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

Each discovery seat first receives and inspects the original evidence and exact change without the
retro. After the seat records its blind observations, the controller resumes that same read-only
leaf with the retro so it can confirm or falsify the material claims. Do not place the retro in the
initial discovery payload or use implementer rationale or claimed test success as proof.

## Discovery seats and walks

One seat completes both judgment axes and both procedural walks:

1. **Fidelity/replay**: replay the original incident or expected scenario; check AC omissions,
   excess behavior, implementation deviations, and whether protection covers the real behavior.
2. **Change-risk**: inspect removed or `must-not-change` behavior, error/state/lifecycle paths,
   caller/callee and producer/consumer contracts, and change-owned cross-cutting risk.

An SDD Unit review uses one fresh discovery seat. A direct final review uses one fresh discovery
seat only when the exact diff and evidence establish a bounded, reversible change with understood
callers, focused behavior protection (or justified testing `N/A`), and no material unresolved risk.
Use two context-isolated discovery seats for direct changes involving security/permissions,
persisted data or migrations, public-contract compatibility, cross-boundary state/lifecycle,
or complex interactions. Unknown impact or a required testing exception also requires two;
small file count, a `direct` label, or unavailable reviewer capacity never proves low risk.
Honor a stricter approved or repository review requirement. Reassess the exact candidate after
material changes and increase coverage when the one-seat conditions no longer hold.

SDD whole-change final review and explicit `tk-review` continue to use two context-isolated
discovery seats. Every seat uses the same target, evidence, axes, finding gate, and severity
rubric and completes both walks. With two seats, one starts with fidelity/replay and the other
with change-risk; neither sees the other's findings or verdict before returning. One seat still
requires the blind pass, retro check, and separate verification of reportable candidates below.

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

## Evidence-only response to a reported finding

During bounded remediation, the controller may send concrete direct counter-evidence for one existing finding
back through the fresh-verifier boundary above. First verify that `HEAD` still equals the reviewed revision
and that the reviewed working-tree/index content has not changed; an uncommitted fix is still a code change.
Bind the original finding, reviewed target, and cited current guard, invariant, source contract, runtime witness,
or focused test output. Preference or an unsupported denial does not qualify.

Keep the finding open while the fresh verifier independently checks only that finding and its new evidence,
including reachable callers or contracts needed to decide it. The implementer and controller cannot self-dismiss.
If accepted, close only the disproved finding as `DISPROVED`, with the verifier's contradictory evidence; keep
unrelated findings unchanged. Rejected or unverifiable rebuttals return to normal remediation with the exact
reason or uncertainty. Missing independent verification leaves the finding open, never implicitly accepted.

This branch needs no empty fix commit, empty `FIX_BASE..HEAD` package, or protection-test rerun solely for
ceremony. A focused check may resolve a concrete remaining doubt. Any actual code change, including an
uncommitted one, follows normal protection tests and scoped fix review. Do not restart broad discovery.
Use this branch at most once per finding at that reviewed revision, count it within the existing five-round
remediation cap, and retain the existing stop after the cap. Keep pending identity/verdict in transient controller
state. Only if optional recovery is already active and interruption requires persistence, retain the minimum
finding reference, reviewed revision, pending verifier identity and consumed attempt in that existing state;
reconcile before redispatch. Add no new finding-ID scheme, ledger, artifact, or reviewer lifecycle.
