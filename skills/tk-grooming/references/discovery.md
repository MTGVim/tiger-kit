# Skill discovery candidates

Repository skills may live under `.agents/skills/`, `.claude/skills/`, or
`.hermes/skills/`. User skills may live under the host's `.agents`, `.claude`, `.codex`,
or `.hermes` skill directory. Repository and user rules, imported instruction files, and
auto-memory directories are candidates only when their exact host-native path is verified.

Identify the current host from actual paths or host-discovery evidence and interpret
only that host's native targets. Resolve imports and directory-scoped rule inheritance
before comparing instructions. If the host is unknown, do not invent a target; leave it
`Unverifiable`. Do not impose one host's location on another or fan out/synchronize
across multiple hosts. Do not use `.tigerkit/` as a persistent registry.

## Ownership evidence

Resolve every candidate path and related symlink before proposing an edit. Classify
ownership from observed evidence:

- a package-manager installation root or manifest;
- updater-managed markers, version files, or update metadata;
- version/current file or directory symlinks that resolve into an external installation
  root;
- verifiable author history that does or does not show user authorship.

Do not conclude from one weak signal, and do not treat absence of user history as proof
of vendor ownership. Combine path, link, installer, updater, and history evidence.
Handle a candidate with confirmed vendor ownership as report-only `keep (vendor)`.
Unknown ownership requires one user decision before an edit proposal. Respect an
explicit exclusion already present in the active conversation or a durable governing
source; do not store it in hidden global state or `.tigerkit/`.

User-facing progress and receipt prose follow the user's language.
