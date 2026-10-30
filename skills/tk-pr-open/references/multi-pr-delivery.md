# Multi-PR delivery safety

Read only when the task is planned or handed off as several PRs. A single PR needs no
grouping or extra artifact. Use the existing conversation or Ready Seed, not a new ledger.

Before implementation, bind each whole Unit to exactly one PR group and name the groups
it waits on. For SDD, keep the existing contiguous Unit headings and put the group mapping
in Global constraints; do not nest, duplicate or renumber Units. For direct work, use the
same ownership and dependency facts without inventing SDD. Cite repository branching and
migration conventions instead of copying them.

Check the proposed groups against these conditions:

- Each shared schema, type, migration or config key has one creating Unit/PR; consumers
  belong to that group or depend on it. Do not create competing definitions.
- After every dependency-ordered merge, identify the reachable capability, its callers,
  and the permission, limit or other guard that makes that state safe. A guard delivered
  later or deferred out of scope cannot protect an earlier capability. Restrict access
  to callers the absent guard would not limit, or keep the capability unreachable.
- Groups without a dependency must merge safely in either order, both semantically and
  without conflicting shared changes. Check each valid dependency prefix and either
  order of independent groups, not just the completed feature.

For each group, record the resulting exposure, its smallest deciding check and one of
`Safe`, `Needs gating`, or `Must merge together`. `Needs gating` is unresolved until its
concrete minimal gate is part of that group and its intermediate state is verified.
`Must merge together` requires regrouping before implementation, not a plan to merge
unsafe PRs quickly. Missing evidence or an unresolved unsafe state blocks that split.
Material product/security changes return to the existing approval owner.

Carry the approved group-to-Unit mapping, dependencies, sole creators, gates and
intermediate-state checks through implementation and the `tk-pr-open` handoff. At
publication preflight, compare actual commits/paths and layer order with that plan.
Keep one planned group per layer; do not silently collapse groups into one PR, split
Units or reassign owners. A non-linear plan cannot be represented as the existing
linear stack without revising the plan and obtaining the required exact approval.
Publication does not authorize new gates or product edits. Recheck each reconstructed
layer and preserve the existing exact final-tree, source-branch and remote-approval guards.

Sources: `obra/superpowers@2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`
(`writing-plans`, SDD preflight) and
`EveryInc/compound-engineering-plugin@33e76fa8a5ac02c3bdc5d2ede2e3924a345ffdbe`
(`ce-plan` structure/final review, `lfg` shipping; PRs #1948/#1950), MIT.
Adapt the safety and handoff conditions, retain TigerKit's Unit grammar and publication
owner, omit upstream runtime/workspace/branch automation. No upstream benchmark result
establishes TigerKit behavior; local cases own that evidence.
