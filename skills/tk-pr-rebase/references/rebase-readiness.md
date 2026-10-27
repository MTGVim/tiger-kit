# PR Base and Rebase Readiness

Use this reference before recommending or executing a base update for one exact pull request. It assesses purpose and base readiness; it does not authorize a rebase, push, reply, closure, or resolution.

## Fresh evidence

Read the current open pull request from GitHub by exact repository and number. Capture the base repository/ref/SHA, head repository/ref/SHA, and fresh `mergeable` and `mergeable_state` values. If mergeability is `null` or `unknown`, reread that same pull request once after a short wait. Do not substitute a cached state or a local branch name for the remote PR head.

When the mergeability state does not settle the base status, read the current base ref SHA and compare that exact SHA with the exact PR head SHA in the base repository. Use the comparison only if GitHub returns evidence for both commits; a cross-fork or unavailable comparison is not evidence that the branch is current.

## Purpose before refresh

First summarize the PR's goal from its diff and linked intent. Compare the fresh base's
changes since the merge-base with the PR's touched paths, including deleted or renamed
ancestor directories of newly added files. Age and commits behind alone do not justify
a full history investigation. If the paths and behavior are unaffected, keep this check
brief. If overlap, removed architecture, changed ownership/API, a possible replacement,
or an explicit reassessment request exists, inspect the relevant base commits and search
open/merged replacement PRs by purpose and paths. An open alternative alone does not
prove the goal is already fulfilled. If comparison or intent evidence is unavailable,
mark the purpose assessment `Unverifiable` and stop the update rather than infer validity.

Bind the decision to the exact base/head SHAs before any rebase or refresh:

- `Update`: the goal remains needed and the approach fits the current structure;
  continue to the base assessment and existing approval/lease gates.
- `Rework`: the goal remains needed, but a mechanical update would restore removed
  structure or preserve an obsolete approach. Explain the smallest current-structure
  change and stop the ordinary update route for a scope decision.
- `Close`: verified replacement or deliberate removal has made the goal unnecessary.
  Cite that evidence and recommend closure; this verdict never closes the PR itself.

Only `Update` proceeds through ordinary refresh. A conflict-free rebase is not evidence
of purpose validity. Reassess when base/head changes or conflict resolution reveals new
intent; compare the final diff/commit series before publication for restored removals,
duplicated fixes or an empty result. Preserve the caller's freshness and authority rules.

## Base assessment

- `dirty` means GitHub reports a merge conflict. The branch needs an integration/update before it can merge. Use the `tk-pr-rebase` route when that route is approved, but do not claim that rebase is the only possible resolution unless repository policy requires rebase specifically.
- `behind`, or a verified comparison with `behind_by > 0`, means the base contains commits absent from the PR head. Recommend updating the branch. Call that update mandatory only when verified branch protection or repository policy requires an up-to-date base. Rebase is the canonical TigerKit route when the user approves that operation; do not silently expand a review response into a history rewrite.
- A fresh `clean` state with the exact base/head evidence means no rebase is indicated for base freshness.
- `unstable`, `blocked`, `draft`, failing checks, unresolved feedback, or missing reviews do not by themselves prove that rebase is needed. Check the exact base status separately when it affects the decision.
- If the state remains unknown and exact comparison is unavailable, report the rebase assessment as unverifiable. Never translate missing evidence into “no rebase needed.”

Explain the practical outcome in natural language: conflict, base is ahead, no rebase indicated, or status could not be verified. Keep the evidence tied to the exact PR and current SHAs.
