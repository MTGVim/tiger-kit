# Acceptance scope

Nested execution uses the target, scenario, authentication, and evidence plan already
defined by its parent. For standalone calls with no explicit criteria or only a scope
phrase, resolve the full criterion set before starting any server or browser: inspect the
same-task inventory in `.tigerkit/qa/` (including embedded `qa-data`) and the current
`tk-prep` impact inventory or Seed. Use every row from the matching inventory, including
`verification-gap` rows; only explicit user scope may narrow it. If more than one unrelated
inventory matches and task identity cannot resolve it, ask before runtime startup. Never
substitute a self-selected subset or a previous run's private plan.

Read the QA sheet's top-level `head` and the Prep Seed's checkout/PR head to establish
lineage. If both current-task sources exist, union their rows by exact stable criterion ID;
keep IDs unchanged and do not merge merely similar wording. A conflicting duplicate ID or
unprovable task/head lineage is a pre-runtime blocker to resolve or report, not permission to
drop one source. A missing inventory head is stale/unknown and must be reconciled against the
current diff before execution.

If the inventory is bound to an older head or its labels/rows no longer match the current
diff, disclose that once and reconcile the complete row map to the current head before
runtime startup: update affected labels, add newly affected rows, and remove rows only with
a diff-based reason. Preserve stable row IDs. Do not regenerate or overwrite the user-owned
QA sheet; return the reconciled ID-to-criterion map so `/tk-qa-sheet` can consume it. Reuse
current evidence only for the exact reconciled row and head; attempt every remaining in-scope
row. An explicit narrower scope records all excluded inventory rows as `out-of-scope`.

