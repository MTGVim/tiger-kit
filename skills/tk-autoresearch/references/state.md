# Durable Autoresearch

A new requested autoresearch run normally owns one resumable state file at `.tigerkit/autoresearch/state.md` after the research identity is clear. An explicit conversation-only/no-save request skips it. Before any write, apply Artifact Paths. If experiments create evidence that must survive, keep only those artifacts under `.tigerkit/autoresearch/experiments/<EXP-ID>/`; do not create a directory for every run.

The canonical state retains stable `researchId`, research-home worktree/branch, active persistence config path, trackedRoot, last checkpoint ID, last checkpoint commit, and the last terminal-transaction state fingerprint/HEAD when available, plus:

- repository/worktree identity and research identity;
- research goal, downstream decision, constraints and excluded scope;
- direction portfolio, known facts and settled decisions;
- open items, fog, dependencies and current frontier;
- last frontier regeneration result: candidates and ranks, candidates set aside with reasons, and the evidence/premises against which it remains valid; record any explicit research-home designation;
- findings with `KEEP`/`REJECT`/`INCONCLUSIVE`/`BLOCKED` and provenance;
- experiment index with artifact paths;
- evaluation contract and its identity when metric/mechanical evaluation applies, with protected/editable surfaces, dev/acceptance evidence roles and any replication or contamination limits;
- convergence state and one next action.

Preserve rejected directions and failed experiments with their reason. Keep budget/priority/resource deferrals separate from observed negative evidence, preserving rank, reactivation conditions and any partial observations without inventing a failure verdict. Link raw evidence instead of copying transcripts.

## Optional lineage and reusable lessons

Use one optional `parent` or `derivedFrom` link on a concrete item when its origin matters: reference the existing direction, finding or observation by stable ID and retain its evidence provenance. Siblings derived from the same observation can share that source link. Add source IDs only when needed for durable traceability; do not require both fields, convert every item into a tree node, or create a separate tree runtime.

After resolving a linked item, preserve any reusable lesson in its parent direction's findings/provenance with the originating item/experiment and evidence IDs. Keep the lesson's scope and uncertainty: a child result updates parent confidence only when evidence tests a shared premise, and a parent's failure does not automatically reject its children. A budget cut yields no failure lesson. Consult relevant positive and negative lessons before sibling/new candidate generation; revisit a known failure only with a changed premise or explicit evidence-backed counter. Keep useful children only when they have realistic information value, and do not reopen a converged branch to maintain tree shape.

On resume, restore relevant origin links and parent lessons through the existing state/findings index. Preserve the canonical single research home and missing-state boundary; consult history by ID when needed rather than replaying every branch.

## Resume

`--resume` resolves the canonical state from the current worktree or linked Git research homes for this same repository; match by stable researchId and research identity. When exactly one valid research home matches, continue there automatically. If several distinct valid research programs exist, ask the user to choose among those concrete programs. Verify repository/worktree identity, research identity, current goal and constraints, then refresh only material evidence that can have changed. Preserve unaffected findings and continue from the stored frontier; apply required frontier regeneration when its prior result is absent or no longer valid, without restarting the setup interview, replacing settled findings, or asking the user to restate the operating protocol.

If no valid state exists in the current or linked worktrees, or a found state belongs to another repository/program, do not guess from memory, chat history, GitHub issues or arbitrary nearby files. Report the exact mismatch and ask one material question: start a new program here or choose one of the actual state-owning worktrees.

`--resume` under a concrete user resume request or user-configured external loop carries the same standard local research authority in the owning worktree without replaying old approvals. Model selection alone is not that request. The saved state identifies the research program and prior evidence; it does not expand authority beyond the standard local boundary. Protected/operational data, secrets, paid or state-changing external services, remote Git publication and destructive/irreversible actions still require explicit authority when needed.

At batch start capture the canonical state fingerprint and research-home HEAD. Before allocating final IDs or writing a terminal material outcome, reread both and apply the persistence concurrent-run guard. Write state atomically and reread it. Use monotonically increasing `CHK-<NNN>` and `EXP-<NNN>` identifiers from the current research program; never reuse an ID after a rejected or reverted attempt. Checkpoint knowledge persistence is defined by [autoresearch persistence](persistence.md). When no frontier action has realistic information gain, apply the SKILL.md convergence and blocker rules before choosing an outcome. An unchanged resume returns `NO-DELTA` without fabricating a checkpoint or repeating a final handoff.

Do not maintain a database, scheduler, execution cursor, worker queue, per-run transcript or global cross-repository research memory. Do not use GitHub issues or PRs as the raw research ledger. Promote a converged engineering action separately through its owning TigerKit workflow.
