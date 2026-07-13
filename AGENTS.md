# TigerKit Repository Guidance

## Product boundary

TigerKit 18 is an Agent Skills repository, not a workflow framework or Claude Code plugin.

- Keep the 18 canonical skills under `skills/tk-*/`.
- Each skill's `SKILL.md` is its behavior source of truth.
- Keep each skill self-contained; skill-specific detail and code stay in its own `references/` and `scripts/`.
- Prefer thin instructions. Add detail only for repeated failures, costly ordering mistakes, mutation safety, objective verification, specialist procedures, or bounded delegation/review.
- Do not restore `.claude-plugin/`, `commands/`, shared runtime contracts, or host-specific copies of skill bodies.

## Behavior boundaries

- User-invoked skills never invoke another user-invoked skill automatically.
- Small work stays owned by the current agent. Non-agent tools, MCPs, sandboxes, browsers, and context-management utilities remain available whenever useful. Delegate implementation ownership to another autonomous agent only for real isolation or parallel benefit; never nest agent delegation.
- Review is optional and bounded to one review, one fix, and one regression check for high-risk work.
- TigerKit never commits, pushes, opens PRs, merges, or publishes unless the user explicitly asks. Explicit invocation of `tk-implement` authorizes a verified commit to the current branch under that skill's documented contract, but does not authorize push, PR creation, merge, tag, release, or publish.

## State and distribution

- Runtime scratch is repo/worktree-local `.tigerkit/`; never use global TigerKit state.
- Do not create archives, current pointers, repo/scope/worktree keys, or automatic legacy migration.
- Do not modify a consumer repository's `.gitignore`; warn when scratch is not ignored.
- Distribution is through `npx skills` for Claude Code, Codex, and Hermes Agent. Git tags and GitHub Releases are the version source of truth.

## Change discipline

- Preserve canonical names, invocation kinds, and upstream attribution.
- Reuse existing skill-local files before adding new surfaces; prefer deletion and the Python standard library.
- Run `python3 scripts/validate_skills.py`, `python3 scripts/validate_skills.py --links-only`, and `npx --yes skills add . --list` for relevant changes.
- For packaging changes, smoke-install all three supported targets in a temporary home.
