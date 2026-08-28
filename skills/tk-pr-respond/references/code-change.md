# Code-Change Execution

Read this reference after selecting a code-changing route and before requesting approval. Use it read-only to plan
workspace and Seed handling; perform no mutation until the plan has current approval. Reply-only work does not load it.

## Workspace isolation

Inspect branch/HEAD, linked-worktree state, unrelated work, and submodule status. Treat `GIT_DIR != GIT_COMMON` as a
linked-worktree signal only after excluding submodules with `git rev-parse --show-superproject-working-tree`; it does not
prove that the checkout belongs to this PR.

A small direct fix may reuse the current checkout only when it is the exact PR branch, clean, safe, and free of unrelated
work. Otherwise detect existing task isolation, prefer an available agent-callable native mechanism such as
`EnterWorktree`, `WorktreeCreate`, `/worktree`, or `--worktree`, and fresh-read the resulting path, branch or detached
state, and HEAD. Current approval for the exact plan and isolation also authorizes that mechanism without another question.

Use manual `git worktree` only when no safe native mechanism exists. Start from the exact approved PR head, avoid
collisions and unrelated work, and verify the result. Do not edit `.gitignore` or create a setup commit for isolation.
If isolation cannot be proven, return `Blocked` before mutation. Preserve host-managed workspace lifecycle; do not remove,
prune, relocate, or clean it on completion.

## Seed selection

Use no Seed for a small, obvious direct fix when conversation and fresh PR evidence are sufficient. Use a Ready Seed for
fresh-child execution, durable context, complex verification, or SDD with multiple material Units. Never create
`pr-respond.md`.

Before approval, preserve an existing Seed byte-for-byte and create no `Status: Pending` file. After approval, write a
needed Ready Seed atomically, reread it, and require `<!-- tigerkit:seed -->` plus deterministic PR/head/task identity.
Replace only a proven TigerKit-owned Seed; preserve an unmarked, legacy, or identity-ambiguous file and return `Blocked`.

The Seed uses Korean user-facing prose and includes the exact repository/PR/head, feedback and requested outcome,
confirmed fixes/replies/deferrals, objective, scope and exclusions, decisions, implementation evidence, Reuse/Simplicity/
Tests/Security/Experience judgments, per-AC verification, browser plan, publication boundary, and guidance for a
lower-capability executor. Never rewrite an exact active Seed. Material feedback or state drift requires approval of the
changed portion before atomic replacement. A no-Seed route remains bound to approved reviewer intent, tests, and publication.

## Execution

- `direct+TDD`: one coherent change and review surface; use the testing reference and the proven safe checkout.
- `SDD+TDD`: multiple material Units; read [private SDD](sdd.md) and follow its grammar, recovery, role gates, model and
  effort contract, fix loop, and final review.

Direct execution applies RED → verified failure → minimal GREEN → refactor while green → required checks. SDD Unit
reports retain RED/GREEN evidence. If fan-out is unavailable, preserve the same role and range gates sequentially; do not
downgrade to unreviewed direct work or persist provider routing.

Record independent `Spec/AC` and `Quality/Standards` verdicts for direct exact-change and SDD Unit/whole-change reviews.
One reviewer may judge both axes; do not require a second reviewer. Finish with AC review, required gap correction,
verified local commits, and `tk-browser-verify` for browser-visible changes. Provide the verifier with exact
command/cwd/URL/auth/readiness; it owns server lifecycle. Do not repeat SDD's whole-change review with another generic review.

After three meaningful direct corrective attempts, stop as `Fail` or `Unverifiable`; SDD uses its five-round breaker.
Material Goal/Scope/Decision/AC/security/required Verification drift returns to the preparation owner. Reversible
engineering ambiguity receives an explicit `Ruling:`. Neither route expands publication authority.
