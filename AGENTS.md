# TigerKit Repository Guidance

## Product boundary

TigerKit 20 is an Agent Skills repository, not a workflow framework or Claude Code plugin.

- Keep exactly 12 canonical skills under `skills/tk-*/`: 2 user-invoked and 10 hybrid. Do not add model-only skills.
- Each skill's `SKILL.md` is its behavior source of truth.
- Keep each skill self-contained; skill-specific detail and code stay in its own `references/` and `scripts/`.
- Prefer thin instructions. Add detail only for repeated failures, costly ordering mistakes, mutation safety, objective verification, specialist procedures, or bounded delegation/review.
- Do not restore `.claude-plugin/`, `commands/`, shared runtime contracts, or host-specific copies of skill bodies.

## Skill existence discipline

Before adding a skill or splitting behavior from an existing skill, check:

1. Does a user have a reason to invoke it independently?
2. Does it have a unique and clear automatic trigger?
3. Is its procedure materially different from normal model behavior?
4. Does it have objective completion criteria?
5. Does it own an independent artifact, mutation, approval, or safety boundary?
6. Does it have at least two real consumers?
7. If it has one consumer, is it too large or risky to inline?
8. Does it justify loading a separate description into context?
9. Would removing it lower real task quality?
10. Would ordinary conversation be more natural?

If the answers are weak, choose `inline`, `merge`, `convert to reference`, `make user-invoked`, or `delete`. Prefer self-contained skills with independent value and completion boundaries over micro-skills used only by another micro-skill.

## Behavior boundaries

- User-invoked skills never invoke another user-invoked skill automatically.
- Small work and ordinary follow-up feedback stay owned by the current agent without requiring a new skill.
- Non-agent tools, MCPs, sandboxes, browsers, and context-management utilities remain available whenever useful.
- Delegate implementation ownership only for real isolation or parallel benefit; never nest agent delegation.
- Every `tk-implement` and `tk-drive` implementation phase runs current-agent Standards/Spec review. Large or high-risk work permits at most one independent reviewer, without fan-out, editing, re-delegation, or automatic re-review.
- TigerKit never commits, pushes, opens PRs, merges, tags, releases, or publishes unless explicitly authorized by a skill contract or user request.
- Explicit `tk-implement` invocation and explicit `$tk-drive` start authorize a verified current-branch commit under their contracts. Neither authorizes push or later release actions; implicit drive resume inherits only the active same-conversation scope.

## Repository documentation

- Do not accumulate `CONTEXT.md`, domain documents, glossaries, or ADRs automatically during feature work.
- Keep branch-local decisions in the conversation, `.tigerkit/spec.md`, `.tigerkit/tickets.md`, commit messages, PR descriptions, code, and tests.
- Write an ADR only when the decision constrains the repository long-term and the user explicitly requests it.
- Do not reference removed skills in current runtime contracts. Historical mentions belong only in `MIGRATION.md`, `CHANGELOG.md`, or `NOTICE.md`.

## State and distribution

- Runtime scratch is repo/worktree-local `.tigerkit/`; never use global TigerKit state.
- Do not create archives, current pointers, repo/scope/worktree keys, or automatic legacy migration.
- Do not modify a consumer repository's `.gitignore`; warn when scratch is not ignored.
- Distribution is through `npx skills` for Claude Code, Codex, and Hermes Agent. Root `CLAUDE.md` and `AGENTS.md` are maintainer guidance and are not installed as skill content.
- Git tags and GitHub Releases are the version source of truth.

## Change discipline

- Preserve canonical names, invocation kinds, and upstream attribution.
- Reuse existing skill-local files before adding new surfaces; prefer deletion and the Python standard library.
- Keep validation local-only. Do not add GitHub Actions workflows for validators, evals, packaging smoke tests, or CLI canaries.
- Run `python3 scripts/validate_skills.py`, `python3 scripts/validate_skills.py --links-only`, and `npx --yes skills add . --list` for relevant changes.
- For packaging changes, smoke-install Claude Code, Codex, and Hermes Agent in temporary homes.
