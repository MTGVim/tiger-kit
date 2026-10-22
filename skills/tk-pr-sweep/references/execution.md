# Approved Sweep Execution

Read this reference only after batch approval and only when at least one row mutates code/Git or dispatches child work.
Report-only and pre-approval paths do not need it.

## Isolation

The child owner's explicitly approved index-only route in `tk-pr-respond` code-change execution also counts as isolation;
pass exact PR/head/row identity and run ownership, and let that owner prove its guards without requiring a workspace path.
Other code-changing and Git-mutating children require a newly established dedicated workspace. Reply-only children do not
create one solely for isolation. Preserve the parent `main` or `develop` work files, real index, HEAD and local branch
refs; index-only permits only its owner's ignored run files and object-store writes.

Before creating a workspace, inspect the row's Git state. Treat `GIT_DIR != GIT_COMMON` as a linked-worktree signal only
after excluding submodules with `git rev-parse --show-superproject-working-tree`; it does not prove row ownership. Reuse a
host-created workspace only when path, exact PR head, row identity, and dedicated provenance are fresh and unambiguous.

Before creating workspaces or dispatching children, select setup and execution width under **Resource bounds** below.
When Orca is installed, read [repository workspace setup](workspace-setup.md) before choosing the creation route; honor
its effective setup/archive hooks instead of adding a duplicate dependency install or bypassing its lifecycle.

Prefer an available agent-callable native mechanism such as `EnterWorktree`, `WorktreeCreate`, `/worktree`, or
`--worktree`, then fresh-read its path, branch or detached state, and HEAD. Use manual `git worktree` only when no safe
native mechanism exists. Start from the approved head, avoid collisions and unrelated work, and verify the result. Do not
make unrelated ignore edits or create a setup commit for isolation. Use the owning SKILL.md
Artifact Paths setup only when an authorized `.tigerkit/` workspace needs ignore coverage.

A workspace child is isolated only when it receives and uses the proven workspace. Never reuse another row's workspace. If
isolation cannot be proven, hold only that PR as `Held` or `Blocked`; do not mutate in the parent checkout. Preserve
host-managed workspace lifecycle and limit cleanup to the explicitly approved run-owned scope.

## Child scope and Seed

Sweep is a PR queue controller, not a task-level SDD controller. The PR owner handles Units and reviewers inside one
workspace. Run rows whose owner selects SDD sequentially by default to avoid multiplying nested controllers. Apply the
resource bounds below to every other row; pass setup ownership, completion evidence and execution width to each child.

Never create a Sweep-wide Seed. A child uses a marked, exact-PR/head Ready `.tigerkit/seed.md` only when its owner selects
durable context or SDD. Reply-only work uses neither a Seed nor workspace solely for isolation; pure rebase follows its
owner's isolation contract. A Seed includes feedback, objective, decisions, approach, AC, verification, and publication
boundary. For visible UI text, pass the exact rendered string or verified entry path and its evidence, never a paraphrase,
identifier, enum inference, or unverified grouped claim.

Do not create `pr-sweep.md`, `pr-respond.md`, or worker receipts. Do not reuse another PR identity's Seed or `sdd.md`.

## Resource bounds

Across all repositories in this Sweep, default code/Git-mutating rows to batches of one: finish the current child's
setup, work, verification and owned process cleanup before creating or dispatching the next workspace. Do not prewarm
all worktrees or start installs in the background. Missing or unverified setup hooks keep this default; installing a
package manager or finding a script is not proof of safe concurrency.

Allow concurrent code/Git rows only when every participating row has a verified lightweight setup hook and their actual
install, build, test and server workloads fit the execution host's available resources without shared writable state.
A hook that runs `npm install`, equivalent dependency initialization or an unbounded workload remains sequential.
Never install into or mutate shared dependencies concurrently. Independent read-only/reply-only rows may overlap when safe.
Reassess before a child adds heavyweight work; let active work finish and admit no further resource-heavy row until safe.
Do not create a scheduler, global lock, capacity configuration or ledger; use the existing queue and child handoff.

## Queue progress

A row-local failure does not stop later independent rows. Stop the Sweep only for a systemic failure such as identity or
permission contamination, ambiguous repository scope, or untrustworthy triage. Triage each PR after its child returns.
After verifying a row's required publication, perform its approved run-owned workspace cleanup under
**Authorized cleanup** below, even while re-review is pending. Retain only that row on failed guards or cleanup.
After all rows finish, run fresh triage across every configured repository and report actual cleanup or retained paths.

## Authorized cleanup

Remove only workspaces this run created and whose cleanup the batch plan explicitly authorized. Reusing an existing
workspace does not make it run-created. Immediately before removal, verify exact path/repository/row creation provenance,
no remaining tracked changes (including staged changes), and local HEAD equal to the fresh remote PR head. Inspect untracked
and ignored contents too; preserve unexpected user work or recovery material. If any guard fails or cannot be proven,
preserve that row's workspace and local branch and report why. Pending re-review alone need not retain a safely published
workspace: it can be recreated from the remote head.

Run cleanup from outside the target, with its literal verified path and no force. Use the owning host's lifecycle and
archive hook; for Orca follow [repository workspace setup](workspace-setup.md). Snapshot `git worktree list --porcelain`
and, when host-managed, the host's workspace inventory before removal; reread the same inventories immediately afterward. Verify the exact target is gone
and all non-target entries remain. An unexpected disappearance is a discrepancy to report and investigate, not proof of
who removed it; pause further cleanup while ownership or scope is uncertain. Never sweep other runs' workspaces or branches.
Delete a run-created local branch only through approved host cleanup or a separately proven exact branch with no other
workspace attached and no unpublished commits; do not expand to remote branch deletion.

A PR is complete only when final triage proves required checks and publication state, closed actionable threads, a
current re-review request or post-summary review for every required reviewer (active `CHANGES_REQUESTED` reviewers and
those named by current-head `<!-- tigerkit:pr-rereview:<HEAD_SHA>:<LOGIN> -->` markers), and any required current-head
summary marker `<!-- tigerkit:pr-summary:<HEAD_SHA> -->`, with its body verified under the owning SKILL.md Publication contract.
