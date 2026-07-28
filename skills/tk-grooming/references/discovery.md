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

## Ownership evidence

Resolve each candidate path and every relevant symlink before proposing an
edit. Classify ownership from observed evidence:

- package-manager installation roots or manifests;
- updater-controlled markers, version files, or update metadata;
- a version/current file or directory symlink that resolves into an external
  installation root;
- available author history showing or failing to show user authorship.

No single weak signal is conclusive, and absence of user history alone does
not prove vendor ownership. Combine the available path, link, installer,
updater, and history evidence. Artifact names and naming conventions are not
ownership evidence.

Confirmed vendor ownership makes the candidate report-only as `keep (vendor)`.
Unknown ownership requires one user decision before any edit proposal. Honor
explicit exclusions already present in the active conversation or a durable
governing source; do not persist them in hidden global state or `.tigerkit/`.

User-facing progress and receipt prose follows the user's language.
