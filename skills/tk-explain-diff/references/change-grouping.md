# Change grouping

After pinning the caller's comparison endpoints and recording the changed inventory, group
by behavior, contract and preserved condition rather than file order. Include text hunks,
rename, binary, mode and submodule changes; mark a partial inventory and its limitation.
One behavior can span files and one file can participate in distinct groups. Reuse a unit
when the same change supports multiple groups. Every primary unit needs a group; secondary
or unavailable units need a concrete reason. Generated, test, type-only or AI-authored
status alone is not a reason to omit a change.

Order groups for a reader; `depends_on` means explanation prerequisites, not program calls.
Use unchanged neighbors as evidence, never as changed inventory. A single group and no graph
are valid. Do not fabricate source for additions, deletions or non-text changes: use verified
metadata or describe the precise limitation. Source statements, inference and unknowns stay
separate. Validate the resulting model and supplied source bundle as described in
[change model](change-model.md); then independently review the final explanation and source.
