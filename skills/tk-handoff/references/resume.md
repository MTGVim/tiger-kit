# Handoff resume

Read only for explicit `--resume`; this does not authorize product, Git or remote mutation.

`--resume` requests resuming work by comparing the `handoff snapshot` against the current Git and files.

First, fresh-read:

- the exact `handoff` and its task-bound Seed when referenced; otherwise its self-contained no-Seed contract
- `branch`/`HEAD`/`worktree`
- changed files
- relevant verification evidence
- exact current remote state only when the next approved action depends on that PR; do not discover other open PRs

Then classify drift.

| Classification | Action |
| --- | --- |
| None | Continue from `Next step` without additional questions |
| Nonessential `drift` | Record it and continue |
| Significant progress `drift` | Update the `Handoff` from current evidence and confirm only the necessary decisions |
| `Seed` contract `drift` | Do not resolve it in the `Handoff`; report that re-entering `tk-prep` is required |
| Conflict | Show the incompatible evidence and mark `Blocked` |
| unverified | If the required state cannot be confirmed, mark `Unverifiable` |

`--resume` may authorize continuing the work, but it does not replace approval to change the `Seed`’s `goal/scope/decision/AC` or permission to publish remotely.
