---
name: tk-grooming
description: "Audit and optionally repair existing repo and user rules or skills. Use only when explicitly invoked by the user."
disable-model-invocation: true
argument-hint: "[scope] [--apply]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Grooming

Use only when the user explicitly invokes this skill. Do not activate it automatically.

Inspect the four existing surfaces: repo rules, repo skills, user rules, user skills. Use host-native paths that actually exist; [discovery](references/discovery.md) lists candidates. Do not create missing files or inspect/migrate legacy global TigerKit state.

Classify duplicate, contradiction, obsolete, broken reference, no-op, overlong, wrong scope/kind, trigger collision, dead skill, stale example, or missing attribution. Propose `keep | tighten | merge | split | move | convert | deprecate | delete | fix`.

Default report-only. Apply only on explicit request: reread originals, search references before deletion, preserve managed/generated ownership, and avoid silently mixing broad repo/user changes. Recheck links, duplicates, and frontmatter after edits. Do not invent knowledge or substitute for reflection/learning.

Output Findings, Proposed operations, Applied, and Verification, omitting empty sections.
