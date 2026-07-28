# Discovery candidates

Repository rules may include root or nested `AGENTS.md`, `CLAUDE.md`,
`CLAUDE.local.md`, `.claude/rules/**/*.md`, `SOUL.md`, and actual host-native
repository instructions. Repository skills may exist under `.agents/skills/`,
`.claude/skills/`, or `.hermes/skills/`. User skills may exist under the
host's `.agents`, `.claude`, `.codex`, or `.hermes` skill directories.

Identify the current host through actual paths or host-discovery evidence and
interpret only its native targets. If the host is unknown, do not invent a
target; leave it `Unverifiable`. Never force one host's location onto another
or fan out/synchronize across hosts. Consider a shared repository rule only
when the user named it or discovery found a tracked shared instruction file.
Never use `.tigerkit/` as a persistent registry.

User-facing progress and receipt prose follows the user's language.
