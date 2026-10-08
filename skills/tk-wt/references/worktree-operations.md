# Orca and Git worktree operations

Orca documentation reviewed 2026-10-08:
- https://github.com/stablyai/orca/blob/main/docs/site/content/docs/cli/reference.mdx
- https://github.com/stablyai/orca/blob/main/docs/site/content/docs/model/orca-yaml.mdx
- https://github.com/stablyai/orca/blob/main/docs/site/content/docs/model/worktrees.mdx

## Orca examples

```sh
orca repo list --json
orca worktree current --json
orca worktree show --worktree active --json
orca worktree create --name task-name --no-parent --setup inherit --json
orca worktree create --name task-name --agent codex --prompt "exact task" --json
orca worktree list --repo id:REPO_ID --json
```

Orca CLI may launch terminal agents only when requested, and the create
result's complete worktree id binds `repoId::worktreePath`. `--no-parent`
changes UI lineage, not Git start ref. If an issue/PR-linked worktree is
requested, only pass flags shown by the *actual installed* CLI. `orca.yaml`
supports `scripts.setup` and `scripts.archive`, with archive hook
requiring an Orca hook-enabled removal. Do not invent event-specific
callbacks. Do not call Orca `rm` in tk-wt; users close Orca-owned workspaces
through Orca. `--force` is never part of tk-wt's cleanup path.

## Safe Git-only operations

```sh
git rev-parse --show-toplevel
git rev-parse --show-superproject-working-tree
git worktree list --porcelain
git status --porcelain=v1 --untracked-files=all
git merge-base --is-ancestor BASE HEAD
git worktree add --no-track -b BRANCH PATH BASE
git -C PATH rev-parse HEAD
git -C PATH status --porcelain=v1 --untracked-files=all
git worktree remove PATH
git worktree list --porcelain
```

Do not interpret a clean command exit as proof of right repository,
worktree ownership or branch identity; re-read on both sides. A Git
worktree may be in use by another process; verify externally before
removing. A shared branch is not safe to delete without separate
explicit authorization and merger evidence. Retain the branch even
when a successful ordinary removal leaves it unmerged.
