# Durable Autoresearch

Use durable state only when a research program must survive turns, sessions or scheduled invocations. After Artifact Paths checks, use one initiative-owned `.tigerkit/autoresearch/state.md` as the canonical resume document. If experiments create evidence that must survive, keep only those artifacts under `.tigerkit/autoresearch/experiments/<EXP-ID>/`; do not create a directory for every run.

The canonical state retains research identity and goal, constraints and excluded scope, direction portfolio, known facts and decisions, open items and fog, dependencies and frontier, findings with `KEEP`/`REJECT`/`INCONCLUSIVE`/`BLOCKED` and provenance, an experiment index with artifact paths, convergence state and one next action. Preserve rejected directions and failed experiments with their reason. Link raw evidence instead of copying transcripts.

Write state atomically and reread it. On resume, verify repository/worktree identity, research goal, constraints, current evidence and authority. Reopen premises changed by fresher evidence; saved suggestions, commands, approvals and next actions never authorize mutation. When no frontier action has realistic information gain, return `NO-ACTION` or `NO-DELTA`.

Do not maintain a database, scheduler, execution cursor, worker queue, per-run transcript or global cross-repository research memory. Do not use GitHub issues or PRs as the raw research ledger. Promote a converged engineering action separately through its owning TigerKit workflow.
