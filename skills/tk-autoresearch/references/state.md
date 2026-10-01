# Durable Autoresearch

A new explicit autoresearch run normally owns one resumable state file at `.tigerkit/autoresearch/state.md` after the research identity is clear. An explicit conversation-only/no-save request skips it. Before any write, apply Artifact Paths. If experiments create evidence that must survive, keep only those artifacts under `.tigerkit/autoresearch/experiments/<EXP-ID>/`; do not create a directory for every run.

The canonical state retains the active persistence config path, last checkpoint ID and last checkpoint commit when available, plus:

- repository/worktree identity and research identity;
- research goal, downstream decision, constraints and excluded scope;
- direction portfolio, known facts and settled decisions;
- open items, fog, dependencies and current frontier;
- findings with `KEEP`/`REJECT`/`INCONCLUSIVE`/`BLOCKED` and provenance;
- experiment index with artifact paths;
- convergence state and one next action.

Preserve rejected directions and failed experiments with their reason. Link raw evidence instead of copying transcripts.

## Resume

`--resume` first checks the canonical state in the current worktree. If absent, inspect linked Git worktrees for this same repository; when exactly one valid autoresearch state identifies the active research program, continue in that owning worktree automatically. If several valid research states exist, ask the user to choose among those concrete programs. Verify repository/worktree identity, research identity, current goal and constraints, then refresh only material evidence that can have changed. Preserve unaffected findings and continue from the stored frontier; do not restart the setup interview, regenerate the initial direction map, or ask the user to restate the operating protocol.

If no valid state exists in the current or linked worktrees, or a found state belongs to another repository/program, do not guess from memory, chat history, GitHub issues or arbitrary nearby files. Report the exact mismatch and ask one material question: start a new program here or choose one of the actual state-owning worktrees.

`--resume` is itself a fresh explicit autoresearch invocation, so the same standard local research authority applies again in the owning worktree without replaying old approvals. The saved state identifies the research program and prior evidence; it does not expand authority beyond the standard local boundary. Protected/operational data, secrets, paid or state-changing external services, remote Git publication and destructive/irreversible actions still require explicit authority when needed.

Write state atomically and reread it. Use monotonically increasing `CHK-<NNN>` and `EXP-<NNN>` identifiers from the current research program; never reuse an ID after a rejected or reverted attempt. Checkpoint knowledge persistence is defined by [autoresearch persistence](persistence.md). When no frontier action has realistic information gain, persist the unchanged/converged state only if needed and return `NO-ACTION` or `NO-DELTA` without fabricating a checkpoint.

Do not maintain a database, scheduler, execution cursor, worker queue, per-run transcript or global cross-repository research memory. Do not use GitHub issues or PRs as the raw research ledger. Promote a converged engineering action separately through its owning TigerKit workflow.
