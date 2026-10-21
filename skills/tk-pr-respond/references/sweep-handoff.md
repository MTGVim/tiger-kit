## Execution under Sweep

For an exact PR handed off by an active `tk-pr-sweep`, do not ask again about material decisions already approved by the parent.
The child confirms the PR fresh state and parent-approved scope, then proceeds immediately when they match.
Include the applicable execution/authority contract text, source revision, exact PR/head, approved
actions, workspace provenance and pending evidence in the handoff. A fresh child must receive
the actual applicable rules, not an "already read" claim. A fork may reuse rules actually inherited
and still present at the same revision; otherwise read the missing owning sections. A leaf with
a complete task-local contract need not reload the whole controller SKILL.md merely for context;
this never waives required conditional references, fresh-state checks or leaf/authority boundaries.
If the parent did not approve the rebase route and its bounded history-rewrite publication, return the newly discovered conflict or base-drift decision to the parent instead of adding it to the approved work.

Reply-only handoffs need no workspace solely for isolation. An explicitly approved index-only handoff uses the exact
PR/head/row identity and run ownership under [code-change execution](code-change.md), without a workspace path.
Other code-changing handoffs must include a newly established
dedicated workspace path, exact PR head, and enough provenance to prove it belongs to that row. "Newly established" may
mean a host-native workspace or a safe manual Git fallback; it never requires a nested manual worktree inside an already
proven host-managed workspace. If the path/HEAD/provenance is missing or not fresh, return `Blocked` before mutation. Run
the code-changing child from that workspace; never switch the parent `main` or `develop` checkout to the PR branch.

If new feedback or head drift materially changes the approved scope, escalate only that PR back to the parent.
Do not create `pr-sweep.md`, `pr-respond.md`, or worker receipt Markdown.
For a code-changing PR that needs durable context, only `seed.md` in the proven dedicated workspace may be used as task context.

The Respond controller may select SDD for its own PR. Normal implementer/reviewer/re-reviewer children remain leaf and may
not recursively delegate. The parent Sweep decides cross-PR scheduling; this child never starts another PR controller.

