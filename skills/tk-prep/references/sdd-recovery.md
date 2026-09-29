# SDD Recovery

Read before starting optional durable recovery, on interruption, or on an empty/malformed/unbound terminal return.


The Ready Seed, current controller context, and local commits are the normal recovery
sources. Do not create a progress ledger merely because execution shape is SDD.

If a terminal leaf return is empty, malformed, or cannot be bound to the expected Unit and
dispatch/review identity, treat the mutation outcome and progress as unknown, not success or failure.
Reconcile only against the exact Seed identifier/hash, Unit, BASE (FIX_BASE for remediation), and
workspace already owned by the controller, using fresh run-owned Git/recovery evidence. Never infer
identity from `cwd`, recent activity, another ledger, or nearby task state. If identity is unavailable
or that evidence cannot prove the outcome, terminate as `Blocked | Unverifiable`.

Until reconciliation, do not blindly re-run the Unit, enter remediation/diagnosis on an assumed failure,
or advance to the next Unit or phase. A recovered commit proves neither verification nor a clean review;
resume only the remaining obligations supported by bound evidence. Reuse existing controller context
and optional recovery/transport artifacts; add no result ledger, retry subsystem, or mandatory durable
child report. A nonterminal launch acknowledgement or pending child is not an empty terminal result;
continue the existing bounded wait.

Create at most one ignored `.tigerkit/sdd.md` only when execution is likely to outlive
the current controller context, the host cannot reliably retain Unit/review state, or an
interrupted run actually needs durable recovery. When a ledger is needed, keep only:

- Ready `Seed` identifier and content hash;
- preflight conflicts or rulings that are not already preserved in the Seed;
- current `Unit` and completed commit SHAs;
- active dispatch: full `BASE` SHA, exact workspace identity, and dispatch identity/phase bound to that Unit;
- open review findings and remediation round when active;
- temporary artifact identifiers and paths that are required for recovery.

When this optional ledger is active, persist the active dispatch immediately before delegation;
if that write fails, stop before dispatch. Keep its identity and BASE until the Unit outcome is
reconciled, including remaining verification/review. For remediation, also persist `FIX_BASE` and
the round before delegation; preserve the original Unit BASE for the complete Unit review.

After interruption, validate the exact Seed identifier/hash, Unit, workspace, and dispatch identity
before inspecting fresh run-owned Git evidence for the recorded `BASE..HEAD` (or `FIX_BASE..HEAD`).
Verify that the recorded base exists and is an ancestor of the current HEAD; a missing base or
ambiguous attribution is `Blocked | Unverifiable`, not permission to reconstruct it from recency.
When applicable Unit work is proven, do not replay it; resume only the outstanding obligations.
For an interaction-blocked partial implementation, prefer resuming the same child. If it cannot
resume, a replacement may continue only the remaining approved implementation after bound evidence
proves the prior mutations, exact remaining scope, and that the old child cannot still mutate the
workspace. Preserve the original Unit BASE for the complete review, and bind the replacement dispatch
to that same Unit/workspace; persist it before launch only when optional recovery state is active.
Completed implementation resumes verification/review/remediation, never implementation replay.
An empty commit range alone does not prove no work:
check run-owned uncommitted changes and the prior child lifecycle as well. Re-dispatch the whole implementation only when
bound evidence proves the prior dispatch produced no applicable work and cannot still mutate the
workspace. A pending child uses the existing bounded wait; an unknown outcome remains
`Blocked | Unverifiable`. Clear or advance active-dispatch state only after reconciliation, never
merely on a child return or interruption. Do not create a ledger for ordinary same-context dispatch.

Do not copy stable Seed content or completed reports into the ledger. Do not resume a
ledger with a different Seed identifier/hash or one from completed work. If it does not
match the current Seed exactly, return `Blocked` before new dispatch and return to the
preparation owner. Before deleting a run-owned ledger, inspect any material deferred or accepted `Ruling:` that
it uniquely preserves. Delete the ledger only when binding acceptance is clean and every such ruling already
exists in another durable owner; otherwise retain the existing ledger as the recovery record. Do not retain it
solely for style/minor findings, completed reports, or rulings already preserved elsewhere, and do not create a
follow-up artifact just to make cleanup possible.

