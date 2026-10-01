# Durable Autoresearch

A new explicit autoresearch run normally owns one resumable state file at `.tigerkit/autoresearch/state.md` after the research identity is clear. An explicit conversation-only/no-save request skips it. Before any write, apply Artifact Paths. If experiments create evidence that must survive, keep only those artifacts under `.tigerkit/autoresearch/experiments/<EXP-ID>/`; do not create a directory for every run.

The canonical state retains:

- repository/worktree identity and research identity;
- research goal, downstream decision, constraints and excluded scope;
- direction portfolio, known facts and settled decisions;
- open items, fog, dependencies and current frontier;
- findings with `KEEP`/`REJECT`/`INCONCLUSIVE`/`BLOCKED` and provenance;
- experiment index with artifact paths;
- convergence state and one next action.

Preserve rejected directions and failed experiments with their reason. Link raw evidence instead of copying transcripts.

## Resume

`--resume` means the canonical state in the current worktree. Read it before planning new work. Verify repository/worktree identity, research identity, current goal and constraints, then refresh only material evidence that can have changed. Preserve unaffected findings and continue from the stored frontier; do not restart the setup interview, regenerate the initial direction map, or ask the user to restate the operating protocol.

If the state is absent, belongs to another repository/worktree, or identifies a different research program, do not guess from memory, chat history, GitHub issues or nearby files. Report the exact mismatch and ask one material question: start a new program in this worktree or switch to the state-owning worktree.

Stored authorization is not active mutation authority. A resumed run may continue read-only investigation without ceremony, but protected data/service access or research-code mutation still needs current conversational authorization when that action becomes necessary. Do not ask for it before then.

Write state atomically and reread it. When no frontier action has realistic information gain, persist the unchanged/converged state only if needed and return `NO-ACTION` or `NO-DELTA`.

Do not maintain a database, scheduler, execution cursor, worker queue, per-run transcript or global cross-repository research memory. Do not use GitHub issues or PRs as the raw research ledger. Promote a converged engineering action separately through its owning TigerKit workflow.
