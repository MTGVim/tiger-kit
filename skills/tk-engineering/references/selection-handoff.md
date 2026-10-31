# Selected prototype handoff

Read this only when a prototype comparison informs the current implementation decision.
The producer returns a compact selection record in its existing result; the preparation
owner carries it in the current plan, or in the Ready Seed's decisions/evidence when a
Seed is already required. Do not create a separate selection file or use `CONTEXT.md` as
a task ledger. A recommendation is not a user selection; retain `unresolved` until the
active user or an already-authorized decision owner selects an option.

Preserve the task/repository identity, explicitly selected variant ID and original absolute
run path, selection reason and material rejected alternative, the relevant screen/state,
and the exact evidence/run-command locations with their verification status. Label paths
as machine-local/best-effort and record whether each needed artifact remains accessible.
Keep conclusions separate from fake integration and official product acceptance. Carry only
decision-relevant details and citations, not the whole prototype, screenshot or transcript.

Before implementation or child handoff, resolve the selected ID to its original run, inspect
the relevant available evidence and verify access from the actual implementation checkout
or child environment. A relative `.tigerkit/` path in another worktree does not identify the
original run. Pass the same selection and minimum constraints to the executor; do not choose
the newest file, another variant or a similarly named run. Preserve artifacts needed for the
active handoff and do not commit prototypes or copy them into production to make them portable.

If evidence is inaccessible, report which path/state is missing and retain the selected ID
and confirmed decision in the plan. Continue only when approved requirements and the retained
constraints fully determine implementation without the missing artifact; otherwise mark the
affected decision `Blocked | Unverifiable` and request only the missing evidence or decision.
Never reconstruct a missing visual claim as verified or substitute another variant. Material
conflict between the selection and approved requirements returns to the existing preparation
boundary; missing optional reference media alone does not invalidate sufficient requirements.

Selection does not approve implementation, publication, promotion or dependency changes.
Reuse current explicit authorization; when implementation is not authorized, return the
selection record and next decision without starting production work.
