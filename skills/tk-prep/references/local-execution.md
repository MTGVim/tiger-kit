# Local Execution

Read this reference only when the approved outcome may include local implementation. Handoff-only preparation does not
need workspace setup or completion mechanics.

## Workspace safety

Before final approval, establish the repository root, current branch/HEAD, default branch, linked-worktree state,
submodule status, staged/unstaged/untracked paths, unrelated user work, and required test/browser/server readiness.
Never absorb, stage, commit, clean, stash, review, or overwrite unrelated work.

Reuse a non-default task checkout only when its task identity and HEAD are proven. Treat `GIT_DIR != GIT_COMMON` as a
linked-worktree signal only after excluding submodules with `git rev-parse --show-superproject-working-tree` or equivalent
evidence. If execution would start from the default branch, final approval must cover creating or using a fresh isolated
task checkout.

When isolation is required, detect existing isolation first. Prefer an available agent-callable native mechanism such as
`EnterWorktree`, `WorktreeCreate`, `/worktree`, or `--worktree`, then fresh-read its path, branch or detached state, and
HEAD. Approval for the exact plan and isolated checkout also authorizes that native mechanism; do not ask again solely
because the tool has its own name.

Use manual `git worktree` only when no safe native mechanism exists. Start from the approved source HEAD, avoid unrelated
work and path/branch collisions, and verify the result. When creating a task branch from any ref other than current HEAD,
prevent inherited upstream tracking (for example, `git worktree add ... -b <branch> --no-track <base-ref>`). Before product
mutation, verify the task branch does not track a shared integration branch such as `origin/main`, `origin/dev`, or
`origin/production`; unset that upstream or return `Blocked` if safe isolation cannot be proven. Do not edit `.gitignore`
or create a setup commit for isolation. If isolation cannot be proven, return `Blocked` before product mutation. Preserve
the lifecycle of host-managed workspaces; do not remove, prune, relocate, or clean them on completion.

## Direct execution and completion

Direct changes follow RED → verified failure → minimal GREEN → refactor while green → self-simplify → exact-change
read-only review → scoped remediation/re-review → binding verification → commit. Remove unnecessary indirection,
speculative flexibility, dead branches, custom replacements for repository-native helpers, and production APIs added
only for tests.

Record independent `Spec/AC` and `Quality/Standards` verdicts. One fresh reviewer may judge both axes; do not require a
second reviewer. Prefer a host-native fresh reviewer. Otherwise perform a distinct serial exact-scope review and disclose
that it was not independent.

For direct and SDD execution, preserve scope and UI literals, use the exact review range, run acceptance review, retain
automated regression protection, and create only approved local commits. Invoke `tk-browser-verify` for every
browser-visible AC; its runtime evidence does not replace automated protection. SDD's whole-change final review already
satisfies the broad review gate.

Material Goal/Scope/approved Decision/AC/security/required Verification drift returns to preparation for revision and
reapproval. A reversible engineering ambiguity may receive a visible `Ruling:` with its reason and cost if wrong.
Repeated blockers end as `Fail | Unverifiable | Blocked`, not an infinite loop.
