# PR Base and Rebase Readiness

Use this reference when deciding whether one exact pull request conflicts with or trails its base branch. It classifies readiness only; it does not authorize a rebase, push, reply, or resolution.

## Fresh evidence

Read the current open pull request from GitHub by exact repository and number. Capture the base repository/ref/SHA, head repository/ref/SHA, and fresh `mergeable` and `mergeable_state` values. If mergeability is `null` or `unknown`, reread that same pull request once after a short wait. Do not substitute a cached state or a local branch name for the remote PR head.

When the mergeability state does not settle the base status, read the current base ref SHA and compare that exact SHA with the exact PR head SHA in the base repository. Use the comparison only if GitHub returns evidence for both commits; a cross-fork or unavailable comparison is not evidence that the branch is current.

## Assessment

- `dirty` means GitHub reports a merge conflict. The branch needs an integration/update before it can merge. Use the `tk-pr-rebase` route when that route is approved, but do not claim that rebase is the only possible resolution unless repository policy requires rebase specifically.
- `behind`, or a verified comparison with `behind_by > 0`, means the base contains commits absent from the PR head. Recommend updating the branch. Call that update mandatory only when verified branch protection or repository policy requires an up-to-date base. Rebase is the canonical TigerKit route when the user approves that operation; do not silently expand a review response into a history rewrite.
- A fresh `clean` state with the exact base/head evidence means no rebase is indicated for base freshness.
- `unstable`, `blocked`, `draft`, failing checks, unresolved feedback, or missing reviews do not by themselves prove that rebase is needed. Check the exact base status separately when it affects the decision.
- If the state remains unknown and exact comparison is unavailable, report the rebase assessment as unverifiable. Never translate missing evidence into “no rebase needed.”

Explain the practical outcome in natural language: conflict, base is ahead, no rebase indicated, or status could not be verified. Keep the evidence tied to the exact PR and current SHAs.
