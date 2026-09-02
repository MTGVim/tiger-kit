# Concurrent PR preflight

Read this only after planned paths, symbols, or owning contracts are known and the change affects code, API/schema/config, a shared component, route/export, data/state/lifecycle, a reusable pattern, or a normative skill/eval/public command/config contract. A suitable GitHub remote and read access must be available.

Skip this branch for non-normative prose/comments, isolated assets, missing or non-GitHub remotes, or offline/unavailable read access. State the reason and continue ordinary preparation unless collision evidence is essential to a safe plan.

Exclude exactly one current PR only when repository, PR number, base, and head identity are established. If repository/head maps to multiple PRs, exclude none and disclose the ambiguity. Inspect the 30 most recently updated remaining open or draft PRs, breaking ties by PR number, using completely paginated metadata and changed paths. If retrieval is truncated or fails, mark the uncovered portion `Unverifiable`.

Shortlist details with exact path overlap, an explicit branch dependency, a verified producer-consumer edge, or a bounded weak signal such as matching title/body, shared directory, or similar theme. Weak signals may earn detail inspection but never establish a collision.

Read details for at most five shortlisted PRs and full diffs for at most three. Material collision evidence is one of:

- overlapping symbols or hunks;
- an incompatible contract change;
- duplicate implementation of the same behavior;
- a concurrent consumer that still adopts the old pattern;
- a verified sequencing dependency.

Immediately before approval, re-read the current top-30 metadata and every inspected PR's state, head, and changed-path fingerprint. Reclassify new or drifted candidates within the same detail/diff budget; otherwise mark their coverage `Unverifiable`. For a material collision, recommend `coordinate | sequence | replan` and cite the exact PR and evidence. Otherwise say only that no material collision was found within the inspected coverage. If more than 30 PRs are open, disclose the uninspected remainder; never claim the repository is clear.

Report observed `metadata/detail/full-diff` counts against `30/5/3`, including failed or truncated retrievals. These counts are evidence, not permission to claim unobserved coverage.

This preflight is read-only. Do not comment, close, merge, retarget, or create persistent artifacts.
