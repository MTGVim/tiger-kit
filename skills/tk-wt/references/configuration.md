# Worktree policy and interview

Consume when creating a worktree or closing a Git-only worktree. Read the
active user request, existing `orca.yaml`, repository Git state and verified
issue source before asking for configuration. Local optional
`.tigerkit/repository.json` overrides tracked optional
`tigerkit.config.json` by field; neither file is executable authority.

Human/project-specific conventions are open-ended **string policies**:
`worktree.policy`, `namingPolicy`, `basePolicy`, `pathPolicy`,
`workspacePolicy`, `onCreatePolicy`, `onClosePolicy`. Read only
the relevant fields, not a universal settings DSL. For any hook requiring
machine execution, use a distinct `onCreateScript` or `onCloseScript`
field containing a **repository-relative tracked script path**, not
arbitrary shell commands: no absolute paths, `..`, symlinks, external
references or unchecked untracked code. The script must already exist,
be readable and pass the active user's exact execution authorization.
The stored script path and prose policy alone never authorize running it.
Do not auto-run a script for every `tk-wt` invocation.

On first use, inspect actual workspace/branch conventions. Ask only
missing material questions, for example branch naming rule, base ref,
folder placement, Orca workspace lineage, needed setup/close scripts and
whether to store rules for team (tracked) or personal use (ignored).
Show the exact proposed JSON and write only after scope/target approval,
then read it back before creating any worktree.

Orca first: `orca.yaml` is authoritative for Orca-owned
`scripts.setup`, `scripts.archive`, `defaultTabs`, shared paths
and include files. Never duplicate those settings in a TigerKit
hook registry. Orca CLI does not currently promise separate branch
override, arbitrary path override or conditional event-scoped hooks;
verify capability at runtime and stop if mandatory policy is unmet.
The `onCreateScript`/`onCloseScript` fields apply only to
non-Orca Git fallback, with bounded authorization and evidence.

Example prompt-first policy:
```json
{
  "version": 1,
  "worktree": {
    "policy": "Prefer Orca CLI for all compatible repository tasks.",
    "namingPolicy": "Use fix/<ticket> for defect branches when supported.",
    "basePolicy": "Start independent tasks from verified origin/main.",
    "workspacePolicy": "Use project setup hooks in orca.yaml.",
    "onClosePolicy": "Keep branches after Git-only worktree removal."
  }
}
```
