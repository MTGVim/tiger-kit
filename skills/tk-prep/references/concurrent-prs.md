# Concurrent PR preflight

Read this only after planned paths, symbols, or owning contracts are known and the change affects code, API/schema/config, a shared component, route/export, data/state/lifecycle, a reusable pattern, or a normative skill/eval/public command/config contract. A suitable GitHub remote and read access must be available.

Skip this branch for non-normative prose/comments, isolated assets, missing or non-GitHub remotes, or offline/unavailable read access. State the reason and continue ordinary preparation unless collision evidence is essential to a safe plan.

Exclude exactly one current PR only when repository, PR number, base, and head identity are established. If repository/head maps to multiple PRs, exclude none and disclose the ambiguity. Start with the 30 most recently updated remaining open or draft PRs, breaking ties by PR number, using completely paginated metadata and changed paths. Treat 30 as an initial cost budget, not proof that older open work is irrelevant. If known paths, symbols, contracts, dependencies, or changed-pattern consumers leave a plausible collision frontier beyond that window, expand metadata in another bounded batch and state why. Stop when the candidate frontier closes. If retrieval is truncated or fails, mark the uncovered portion `Unverifiable`.

Shortlist details with exact path overlap, an explicit branch dependency, a verified producer-consumer edge, or a bounded weak signal such as matching title/body, shared directory, or similar theme. Weak signals may earn detail inspection but never establish a collision.

Start with details for up to five shortlisted PRs and full diffs for up to three. Expand only when an inspected candidate exposes another exact dependency or the plausible frontier cannot otherwise be closed; record the reason and added count. Material collision evidence is one of:

- overlapping symbols or hunks;
- an incompatible contract change;
- duplicate implementation of the same behavior;
- a concurrent consumer that still adopts the old pattern;
- a verified sequencing dependency.

Immediately before approval, re-read the inspected metadata frontier and every detailed PR's state, head, and changed-path fingerprint. Reclassify new or drifted candidates within a newly justified bounded expansion; otherwise mark their coverage `Unverifiable`. For a material collision, recommend `coordinate | sequence | replan` and cite the exact PR and evidence. Otherwise say only that no material collision was found within the inspected coverage. Disclose any uninspected remainder; never claim the repository is clear when a plausible frontier remains open.

Report observed `metadata/detail/full-diff` counts, the initial `30/5/3` budget, every expansion reason, and failed or truncated retrievals. Counts are cost evidence, not permission to claim unobserved coverage.

This preflight is read-only. Do not comment, close, merge, retarget, or create persistent artifacts.
