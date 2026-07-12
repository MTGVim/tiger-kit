# Changelog

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
