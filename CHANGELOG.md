# Changelog

## 18.0.4 — Implementation and Browser Contracts

- Added explicit `direct`/`delegated` and TDD strategy approval before `tk-implement` modifies files.
- Restored incremental verification, bounded review, and verified current-branch commit behavior while keeping push and release actions separately authorized.
- Defined single-level implementation delegation and kept MCPs, sandboxes, browsers, and context-management tools available in either execution mode.
- Documented ownership and cleanup rules for browser sessions launched or attached by `tk-browser-verify`.
- Extended static behavior fixtures and repository validation for these contracts.

## 18.0.3 — Korean Skill Documentation

- Localized skill instructions and the README for Korean users while preserving canonical skill names and invocation labels.

## 18.0.2 — Invocation Labels

- Prefixed skill descriptions with `[user]`, `[auto]`, or `[user/auto]` so picker entries communicate their intended invocation.
- Mirrored `[user]` in Codex interface descriptions for explicitly invoked skills.
- Enforced invocation labels in repository validation without renaming skills or changing invocation kinds.

## 18.0.1 — README Invocation Guide

- Distinguished user-invoked, model-invoked, and hybrid skills throughout the README catalog.
- Restored the cute TigerKit cover image and displayed it at the top of the README.
- Updated the immutable installation example to `v18.0.1`.

## 18.0.0 — Agent Skills Reboot

TigerKit 18 is a breaking distribution and runtime reboot.

### Breaking changes

- Ended new support for the Claude Code plugin runtime and removed plugin manifests, command wrappers, central state helpers, legacy schema/evidence machinery, and common emoji output contracts from `main`.
- Switched distribution to 18 self-contained `skills/tk-*/` Agent Skills installed with `npx skills`.
- Added initial host support for Claude Code, Codex, and Hermes Agent.
- Replaced legacy `/tk:*` namespace calls with `tk-*` skill names; see `MIGRATION.md` for the mapping.
- Stopped all automatic discovery or migration of legacy global TigerKit state.
- Moved optional work state to repo/worktree-local `.tigerkit/` scratch with no repo/worktree keys, ledgers, archives, or current pointers.

### Skill catalog

User-invoked: `tk-grill-me`, `tk-grill-with-docs`, `tk-to-spec`, `tk-to-tickets`, `tk-implement`, `tk-prototype`, `tk-reflect`, `tk-learn`, `tk-grooming`, `tk-handoff`.

Hybrid: `tk-browser-verify`.

Model-invoked: `tk-grilling`, `tk-domain-modeling`, `tk-tdd`, `tk-diagnosing-bugs`, `tk-code-review`, `tk-merge-conflict`, `tk-codebase-design`.

### Installation

```bash
npx skills add "MTGVim/tiger-kit#v18.0.0" \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill '*'
```

### Attribution

Ten skills are adapted from `mattpocock/skills` and retain their upstream names with the `tk-` prefix. See `NOTICE.md`.

### Release status

This entry is the prepared GitHub Release body. Creating tag `v18.0.0`, publishing the GitHub Release, and any remote push remain separate explicit release actions.
