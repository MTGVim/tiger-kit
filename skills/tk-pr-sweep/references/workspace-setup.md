# Repository workspace setup

Read only when Orca is installed and an approved Sweep row needs a workspace. Discover the installed CLI/runtime's
supported read-only repository/settings surface, match the repository origin/path and execution host, and inspect its
effective setup/archive scripts and run/source policy. Inspect referenced script bodies before executing them. Do not
install or open Orca, change settings, or infer hooks from a similarly named file merely to enable this route.
Include automatic startup/tab commands when assessing resource use.

## Effective configuration

For local Git worktrees, inspect `orca.yaml` and repository-local Orca settings together. `scripts.setup` and
`scripts.archive` are hooks; local overrides and command-source policy can replace or combine them. The new worktree's
revision supplies YAML setup; the registered primary checkout supplies archive and shared-path rules. The primary
checkout's setup alone does not prove the approved PR head's setup. Use current installed behavior for other targets.
`worktree.sharedDirectories` and configured shared paths may avoid repeated installs, but verify dependency/lockfile
compatibility and shared-write implications rather than creating new links or assuming reuse is safe.

## Run once and verify

Prefer the approved host-native creation route that applies the effective setup and required environment. Preserve
Orca's hook trust and run policy; the presence of a script grants no additional authority. Let automatic setup run once,
observe its actual completion and verify required dependency/readiness postconditions before dispatching dependent work.
Creation success or an agent terminal appearing is not setup success: setup and agent startup may be asynchronous.
Pass the exact prepared workspace, setup owner/status and omitted redundant install to the child. Neither parent nor
child reruns the hook or adds `npm install` after successful setup. If supported setup is absent, use the repository's
proven initialization under the one-row resource bound in [approved execution](execution.md).

A setup script is a replacement for the initialization it actually performs, not evidence of a cheaper workload.
Inspect its effective commands and retain sequential execution for heavy or unknown setup. On failure or an uncertain
outcome, reconcile owned setup state before retrying; hold only the affected row if readiness or required trust cannot
be established. Do not silently bypass a required hook with a generic install or repeat a still-running setup.

## Authorized cleanup

When workspace archive/removal is already authorized, use the owning host's lifecycle and effective archive hook once.
Inspect its scope; a hook may remove more than dependencies. A failed archive hook blocks that cleanup, not later safe
rows. Preserve the workspace and report residue; do not force removal, invoke a teardown script separately, or delete
shared dependencies. Apply the run-created provenance, clean-state, remote-head and inventory checks in
[approved execution](execution.md#authorized-cleanup). Batch approval authorizes cleanup only when explicitly included
for that row; Sweep completion does not authorize removal of preexisting or out-of-scope workspaces or user-owned resources.
