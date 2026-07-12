# Migrating from TigerKit 16.x to 18.0.0

TigerKit 16.x is the Claude Code plugin generation. TigerKit 18.x is the Agent Skills generation for Claude Code, Codex, and Hermes Agent. The change is a hard cut-over with no compatibility aliases or automatic state migration.

## 1. Remove the legacy Claude Code plugin

Inspect the installed plugin first, then remove the TigerKit plugin from the scope where it was installed:

```bash
claude plugin list
claude plugin uninstall tk@tiger-kit --scope user
```

Use the matching project/local scope if that is where the legacy plugin is installed.

## 2. Install Agent Skills

```bash
npx skills add MTGVim/tiger-kit \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill '*'
```

## 3. Invocation mapping

| Legacy | TigerKit 18 |
| --- | --- |
| `/tk:grill` | `/tk-grill-me` |
| `/tk:to-prd` | `/tk-to-spec` |
| `/tk:to-issues` | `/tk-to-tickets` |
| `/tk:prototype` | `/tk-prototype` |
| `/tk:reflect` | `/tk-reflect` |
| `/tk:learn` | `/tk-learn` |
| `/tk:grooming` | `/tk-grooming` |
| `/tk:handoff` | `/tk-handoff` |
| `/tk:browser-verify` | `/tk-browser-verify` |
| no execution command | `/tk-implement` |

Codex uses `$tk-*` or its skill picker instead of slash invocation.

## 4. Legacy state is not migrated

TigerKit 18 does not discover, import, merge, or copy legacy global TigerKit state, repo-key mappings, ledgers, current pointers, browser profiles, or UI-diff profiles. Existing files remain untouched.

If useful information exists there, inspect individual files manually and copy only current, non-sensitive facts into the relevant repository convention or repo-local `.tigerkit/` scratch path.

Do not blindly copy credentials, stale URLs, historical screenshots, raw logs, or old browser login material. Recreate sensitive configuration through the current host or environment instead.

## 5. New work state

Current scratch state lives under the active repository or worktree's `.tigerkit/`. It is not durable documentation and TigerKit does not modify `.gitignore` automatically. Move official specs or decisions into the repository's existing documentation/tracker convention when needed.
