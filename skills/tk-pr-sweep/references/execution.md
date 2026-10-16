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

Prefer an available agent-callable native mechanism such as `EnterWorktree`, `WorktreeCreate`, `/worktree`, or
`--worktree`, then fresh-read its path, branch or detached state, and HEAD. Use manual `git worktree` only when no safe
native mechanism exists. Start from the approved head, avoid collisions and unrelated work, and verify the result. Do not
make unrelated ignore edits or create a setup commit for isolation. Use the owning SKILL.md
Artifact Paths setup only when an authorized `.tigerkit/` workspace needs ignore coverage.

A workspace child is isolated only when it receives and uses the proven workspace. Never reuse another row's workspace. If
isolation cannot be proven, hold only that PR as `Held` or `Blocked`; do not mutate in the parent checkout. Preserve
host-managed workspace lifecycle and do not add general cleanup authority.

## Child scope and Seed

Sweep is a PR queue controller, not a task-level SDD controller. The PR owner handles Units and reviewers inside one
workspace. Run rows whose owner selects SDD sequentially by default to avoid multiplying nested controllers. Other safe
rows may retain PR-level concurrency. Do not create a scheduler or capacity ledger.

Never create a Sweep-wide Seed. A child uses a marked, exact-PR/head Ready `.tigerkit/seed.md` only when its owner selects
durable context or SDD. Reply-only work uses neither a Seed nor workspace solely for isolation; pure rebase follows its
owner's isolation contract. A Seed includes feedback, objective, decisions, approach, AC, verification, and publication
boundary. For visible UI text, pass the exact rendered string or verified entry path and its evidence, never a paraphrase,
identifier, enum inference, or unverified grouped claim.

Do not create `pr-sweep.md`, `pr-respond.md`, or worker receipts. Do not reuse another PR identity's Seed or `sdd.md`.

## Queue progress

A row-local failure does not stop later independent rows. Stop the Sweep only for a systemic failure such as identity or
permission contamination, ambiguous repository scope, or untrustworthy triage. Triage each PR after its child returns.
After all rows finish, run fresh triage across every configured repository.

A PR is complete only when final triage proves required checks and publication state, closed actionable threads, a
current re-review request or post-summary review for every required reviewer (active `CHANGES_REQUESTED` reviewers and
those named by current-head `<!-- tigerkit:pr-rereview:<HEAD_SHA>:<LOGIN> -->` markers), and any required current-head
summary marker `<!-- tigerkit:pr-summary:<HEAD_SHA> -->`.
