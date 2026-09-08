# Concurrent PR preflight

Read this only after planned paths, symbols, or owning contracts are known and the change affects code, API/schema/config, a shared component, route/export, data/state/lifecycle, a reusable pattern, or a normative skill/eval/public command/config contract. A suitable GitHub remote and read access must be available.

Skip this branch for non-normative prose/comments, isolated assets, missing or non-GitHub remotes, or offline/unavailable read access. Continue ordinary preparation unless collision evidence is essential to a safe plan; disclose unavailable coverage when it matters to the decision.

## Targeted discovery

Build the search surface from exact planned paths/symbols and verified direct producer-consumer or branch dependencies.
Inspect already known dependent PRs first, regardless of update age. Exclude exactly one current PR only when repository,
PR number, base, and head identity are established. If multiple PRs match, exclude none and disclose the ambiguity.

Use a fresh, coverage-known changed-path index when available. Otherwise use supported targeted searches and lightweight,
paginated open/draft PR metadata to identify candidates, then fetch their changed paths. Paths/symbols mentioned in titles
or bodies are leads, not a complete changed-file index: a keyword miss or an unrelated title cannot prove non-overlap.
If those leads cannot cover a material dependency, inspect further changed-path lists in bounded batches or disclose that
coverage as `Unverifiable`. Do not claim the whole repository is clear from a partial search.

Fetch details and only the necessary diff for candidates with exact path overlap, a verified dependency, or a bounded weak
signal such as a related title, directory, or theme. Weak signals earn inspection but never establish a collision. Expand
only when an inspected candidate exposes another relevant dependency or leaves a material collision question unresolved.
There is no mandatory recent-PR quota, fixed `30/5/3` report, or requirement to read unrelated diffs. Stop when the relevant
collision questions are resolved or required evidence is genuinely inaccessible; ordinary uninspected unrelated work does
not block preparation.

## Evidence and freshness

Material collision evidence is one of:

- overlapping symbols or hunks;
- an incompatible contract change;
- duplicate implementation of the same behavior;
- a concurrent consumer that still adopts the old pattern;
- a verified sequencing dependency.

Before approval, refresh the targeted discovery surface for newly relevant PRs and the state/head of PRs material to the
plan. Reuse unchanged-head path/diff evidence; fetch it again only when the head changes or other material state changes
invalidate it. Reclassify new or drifted candidates before relying on their earlier result. Bound failed or truncated
retrievals explicitly, and stop for missing evidence only when it is essential to the safe plan.

For a material collision, recommend `coordinate | sequence | replan` with the exact PR and evidence. Otherwise report
only that no material collision was found in the relevant inspected coverage. Surface a material coverage limitation
with its practical consequence. Keep routine retrieval counts and batch budgets out of the user-facing report unless
requested or needed to explain a specific cost/coverage limitation. Do not create a persistent scan report.

This preflight is read-only. Do not comment, close, merge, retarget, or create persistent artifacts.
