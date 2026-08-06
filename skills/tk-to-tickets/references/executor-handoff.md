# Cheaper-model handoff

Write each ticket so a cheaper executor can run it without the parent
conversation, audit session, or another ticket in memory.

- **Context closure**: inline the unit goal, exact paths/symbols, current-state
  evidence, repository convention, and relevant exemplar.
- **Boundaries**: state included and excluded scope, predecessor output needed,
  and concrete STOP/report-back conditions.
- **Verification**: name independently observable checks and expected results;
  include source HEAD and drift handling.
- **Decisions**: preserve source R/AC IDs, assumptions, constraints, and
  predecessor contracts rather than relying on hidden context.
- **Secrets**: record only a path and credential type; never copy values,
  cookies, tokens, or private identity into the artifact.

This is a handoff quality contract, not permission to implement, publish
remotely, or merge ticket lifecycle with Ready-spec ownership.
