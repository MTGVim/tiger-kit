# Code-Change Execution

Read this reference after selecting a code-changing route and before requesting approval. Use it read-only to plan
workspace and Seed handling; perform no mutation until the plan has current approval. Reply-only work does not load it.

## Workspace isolation

Inspect branch/HEAD, linked-worktree state, unrelated work, and submodule status. Treat `GIT_DIR != GIT_COMMON` as a
linked-worktree signal only after excluding submodules with `git rev-parse --show-superproject-working-tree`; it does not
prove that the checkout belongs to this PR.

For eligible text-only work, the approved index-only route below also proves isolation, including under Sweep.
For other work, a small direct fix may reuse the current checkout only when it is the exact PR branch, clean, safe, and free of unrelated
work. Otherwise detect existing task isolation, prefer an available agent-callable native mechanism such as
`EnterWorktree`, `WorktreeCreate`, `/worktree`, or `--worktree`, and fresh-read the resulting path, branch or detached
state, and HEAD. Current approval for the exact plan and isolation also authorizes that mechanism without another question.

Use manual `git worktree` only when no safe native mechanism exists. Start from the exact approved PR head, avoid
collisions and unrelated work, and verify the result. Use the owning SKILL.md Artifact Paths setup only for missing `.tigerkit/` coverage;
do not make unrelated ignore edits or create a setup commit for isolation.
If isolation cannot be proven, return `Blocked` before mutation. Preserve host-managed workspace lifecycle; do not remove,
prune, relocate, or clean it on completion.

### Index-only commit

Use this direct route only for ordinary comments, documentation, or other provably behavior-preserving text excluding
string literals, when no local build/test or runtime verification is needed. Executable documentation, agent instructions,
compiler/linter directives, configuration, behavior changes, uncertain impact, multiple response commits, and rebase use
the workspace route. State index-only isolation in the resolution plan and require approval covering that exact route;
matching current standalone or parent approval already satisfies it. Never describe a worktree plan and silently switch.

1. Pin the approved PR head as `RESPONSE_BASE`; fresh-read repository/PR/branch/identity and require the remote head to
   match before construction. Record the parent's HEAD/branch, real index bytes, and tracked/untracked work state without
   refreshing its index. Existing unrelated changes remain untouched and are never input to this commit.
2. Require existing effective `.tigerkit/` exclusion and pass Artifact Paths safety/ownership checks before any write.
   If exclusion is absent, use the workspace route or return `Blocked`; never run parent ignore setup for index-only.
   Use a unique run-owned `.tigerkit/tmp/tk-pr-respond/<run-id>/` for candidate bytes and an initially absent, absolute
   `GIT_INDEX_FILE`. Scope that variable to each index command or a subshell and restore the
   caller environment afterward. Populate it with `git read-tree "$RESPONSE_BASE"` without `-u`. Read source bytes and
   file modes from that exact Git tree, not the parent's checkout; never checkout, stage, reset, stash, switch branches,
   or update the parent's HEAD, real index, or local branch refs.
3. Since `commit-tree` bypasses commit hooks (including Husky/commitlint), verify repository commit-message and signing
   requirements explicitly. Run the repository formatter on candidate stdin with `--stdin-filepath <original-path>` or
   its supported equivalent, using configuration/dependencies verified against `RESPONSE_BASE`; compare the formatted
   bytes and keep only mapped changes. If required formatting, signing, or other hook obligations cannot be satisfied
   without a checkout, use the workspace route. Run no build/test against the unrelated parent's files.
4. Store only approved candidate bytes with `git hash-object -w`: use `--no-filters` for edits made in canonical stored
   blob form; for working-form bytes, use `--path=<original-path>` only with attributes/filters verified against
   `RESPONSE_BASE`. Never apply the dirty parent's attributes or clean an already canonical blob twice. Replace entries with `git update-index --cacheinfo <original-mode>,<blob>,<path>` using the temporary index.
   Create the tree with `git write-tree`. Inspect its exact name-status, diffstat, full diff and finding map, and apply the
   existing independent review protocol. Recheck head drift before `git commit-tree <tree> -p "$RESPONSE_BASE"` creates
   one commit; record its SHA as `COMMIT`. Compare `RESPONSE_BASE..COMMIT` and verify parent state is unchanged before push
   and after publication, excluding only owned ignored run files and the allowed object-store writes.
5. Use `COMMIT`, not the unrelated parent's `HEAD`, for review ranges, ancestry, publication and current-head evidence.
   Recheck all existing publication guards and require the remote head still equals `RESPONSE_BASE`. Push only a normal
   fast-forward with `git push <remote> "${COMMIT}:refs/heads/<approved-branch>"`; braces prevent zsh's `$C:r` modifier
   from corrupting a refspec. Never force, rebase, or overwrite drift. Preserve the candidate and stop for a changed plan
   on drift/rejection instead of retrying against a new head without approval.
6. After push, fresh-read the exact remote head and its CI build/test results. Pending checks mean `Pending`; failed
   checks mean `Fail`, and absent/unverifiable required coverage means `Unverifiable`. Claim `Pass` only after current-head
   build/test success and every existing reply/thread/summary/re-review obligation. This route grants no extra publication
   or cleanup authority. Preserve unpublished candidate recovery data; remove only owned temporary files after success.

## Seed selection

Use no Seed for a small, obvious direct fix when conversation and fresh PR evidence are sufficient. Use a Ready Seed for
fresh-child execution, durable context, complex verification, or SDD with multiple material Units. Never create
`pr-respond.md`.

Before approval, preserve an existing Seed byte-for-byte and create no `Status: Pending` file. After approval, write a
needed Ready Seed atomically, reread it, and require `<!-- tigerkit:seed -->` plus deterministic PR/head/task identity.
Replace only a proven TigerKit-owned Seed; preserve an unmarked, legacy, or identity-ambiguous file and return `Blocked`.

The Seed uses Korean user-facing prose and includes the exact repository/PR/head, feedback and requested outcome,
each finding's approved disposition and evidence, objective, scope and exclusions, decisions, implementation evidence,
material Reuse/Simplicity/Tests/Security/Experience gaps or exceptions, per-AC verification, browser plan, publication
boundary, a semantic Review Plan, and guidance for a lower-capability executor. The Review Plan records intent, expected
scenario/outcome, `must-not-change` surfaces, change-owned risk edges, required evidence, and known uncertainty without
reviewer count or provider/worker routing. Do not add readiness rows merely to state that an axis is ready or
irrelevant. Never rewrite an exact active Seed. Material feedback or state drift requires approval of the changed portion
before atomic replacement. A direct/no-Seed route preserves the same semantic Review Plan in the approved current
interaction without creating Seed ceremony; it remains bound to approved reviewer intent, tests, and publication.

## Response delta discipline

Before mutation, record `RESPONSE_BASE` as the exact approved PR head. Every production or test hunk in
`RESPONSE_BASE..HEAD` (or `RESPONSE_BASE..COMMIT` for index-only) must map to one approved `fixed` finding or the minimum
acceptance-criterion and regression protection needed for that fix. Supporting changes are allowed only when required to build, test, or verify that mapped
response. Do not include opportunistic refactoring, cleanup, formatting, dependency updates, or neighboring fixes.

Before commit and again before push, inspect the name-status, diffstat, and full response diff against the finding map:
`RESPONSE_BASE..HEAD` for a workspace, the candidate tree before index-only commit and `RESPONSE_BASE..COMMIT` afterward. Remove run-owned unmapped changes safely. If an unmapped change cannot be separated without altering approved
scope or unrelated work, stop for a changed plan instead of publishing it.

## Execution

- Index-only remains direct: use the guards above with testing `N/A` for provably non-executable text, exact-tree/range
  independent review, and post-push current-head CI. The checkout/TDD/local-commit steps below apply to workspace routes.
- `direct+TDD`: one coherent change and review surface; use the testing reference and the proven safe checkout.
- `SDD+TDD`: multiple material Units; read [private SDD](sdd.md) and follow its grammar, recovery, role gates, model and
  effort contract, fix loop, and final review.

Direct execution follows [behavior-first testing](testing.md): changed behavior requires RED → verified failure →
minimal GREEN; behavior-preserving refactoring requires pre-edit GREEN → refactor → matching GREEN. Run required checks.
SDD Unit reports retain the applicable RED/GREEN or pre/post GREEN evidence. If fan-out is unavailable, preserve the same role and range gates sequentially; do not
downgrade to unreviewed direct work or persist provider routing.

After implementation, construct the untrusted implementation retro required by
[independent review protocol](review-protocol.md). Apply that protocol to direct exact-change and SDD Unit/whole-change
reviews: use its risk-based direct seat count; SDD whole-change final still uses two context-isolated discovery seats,
while each SDD Unit uses one fresh seat. Every seat judges both `Spec/AC` and `Quality/Standards` and completes both walks; withhold the retro until its
blind pass, aggregate candidate unions, and separately verify every reportable candidate. Finish with AC review, required gap correction,
verified local commits, and `tk-browser-verify` for browser-visible changes. Provide the verifier with exact
command/cwd/URL/auth/readiness; it owns server lifecycle. Do not repeat SDD's whole-change review with another generic review.

Apply [finding quality](finding-quality.md) to every code review. Read [TypeScript](typescript.md),
[React](react.md), and [security](security.md) only when the reviewed scope meets those references' conditions. These
lenses do not change finding disposition, response-delta, re-review targets, or publication order.

Handle direct review remediation for at most five rounds, using the original open findings, exact fix diff, and only
unchanged caller/callee or producer/consumer contracts that the remediation can directly affect rather than rerunning
broad discovery after each edit. Add a new `Critical`/`Important` finding only when it is causally attributable to the
remediation, including when its evidence is in that directly affected unchanged boundary. Stop as `Fail` or
`Unverifiable` after round five; SDD uses the same maximum.
Material Goal/Scope/Decision/AC/security/required Verification drift returns to the preparation owner. Reversible
engineering ambiguity receives an explicit `Ruling:`. Neither route expands publication authority.
