# Distillation provenance

Reviewed 2026-10-07 at `ayghri/i-have-adhd@723af7d9afaf43eb871dbcce6129e2bf80de90d5`:
`skills/i-have-adhd/SKILL.md`, `README.md`, `evals/rubric.md` and `LICENSE`.
The implementation, rationale and blind quality rubric were inspected. Upstream judge/runtime
execution and comparative efficacy are unverified; they are not TigerKit improvement evidence.

- `keep`: easily found action/answer, numbered user steps, calm errors and visible verified results.
- `adapt`: bounded visible groups retain complete reasoning, alternatives, caveats and sources;
  explicit detail/format and agent-owned execution take priority over presentation preferences.
- `omit`: medical inference, guessed times/progress, persistent mode, mandatory status restatement,
  fixed list cap and a fabricated next user task when the agent can finish or no action remains.

This supersedes the former orientation-only interpretation. `tk-handoff` now owns the unchanged
conversation-only orientation procedure and its migrated regression cases. `tk-adhd` owns only
current-response presentation and grants no execution, artifact or publication authority.
The original MIT notice remains in this package and the orientation consumer's `LICENSE.txt`.
