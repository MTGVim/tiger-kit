## Baseline continuation and final-response gate

Before invoking a pre-edit baseline, retain the approved execution shape, remaining implementation/verification/commit
obligations, and next implementation action in current task context; direct/no-Seed needs no new artifact.
When that baseline succeeds, bind its run/replay evidence to this task and execute the next approved implementation action
in the same active turn. A progress update may precede that action; a final answer or a promise to resume cannot replace it.
Then obtain the matching after comparison before final review, binding verification, or commit.

This applies both when the host loads the planned verifier (`tk-browser-verify` or `tk-app-verify`) through a Skill tool in the same agent and when a separate child
returns. In the first case, resume the retained owner procedure yourself; do not wait for a nonexistent parent process.
In the second, consume the child's terminal response as phase-local evidence. `Status: Pass`, `## Verdict`, or
`resume_parent: required` in a child report never means the approved parent task is complete or triggers host scheduling.

Before sending a final user-facing result, check the retained approved obligations. If any approved implementation,
verification, review, or commit obligation remains actionable, continue execution without another approval. Pause only for material drift, an unapproved
limitation, a required user-owned decision, a safety boundary, or an explicit user stop/change of scope; name the actual
reason and remaining work. Never end the parent turn merely to report baseline success.

When any uncovered row remains unexecuted because of missing authority, irreversibility, unavailable
data, verifier limits, or another manual reason, state the count and stable criterion IDs in
`human_action`, with each row's reason and unblock step, and recommend that the user start `/tk-qa-sheet` for
follow-up. Exclude `covered-by` rows from that count because their equivalence evidence is recorded.
Never auto-invoke the user-only skill.
When the user asks for a manual QA checklist or HTML sheet, recommend explicit `/tk-qa-sheet`; it does
not replace required implementation verification.

For local execution, follow the already loaded local-execution reference. SDD additionally follows the private SDD
protocol. Only after the final-response gate permits completion or a justified pause, return a compact result with the execution shape, Seed path or `none`, commits or handoff status, focused and
required verification, runtime evidence, exceptions, review independence, and any blocker. Claim remote publication only after the separately authorized publication owner verifies it.

