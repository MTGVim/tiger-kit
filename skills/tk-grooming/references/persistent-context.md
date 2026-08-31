# Persistent context audit

Use this branch only for repository/user rules, imported instructions, auto memory, or
user-corrected behavior plausibly influenced by them.

## Evidence chain

1. Identify the behavior and the user's correction without converting either into a
   general rule.
2. Resolve the active host, exact loaded paths, imports, directory scope, symlinks, and
   ownership. A familiar filename or remembered host convention is not evidence.
3. Identify the current behavior owner, such as an installed current skill, from package,
   version, source, or installation evidence.
4. Compare exact applicable statements. Classify an entry as `stale override` only when
   its required behavior contradicts the established current owner and can plausibly
   account for the observed behavior.
5. Record `behavior -> persistent statement -> current owner statement -> conflict`.
   File presence, age, load order, and model speculation cannot replace this chain.

Use `duplicate` when statements have the same meaning, `conflict` when both remain
current but disagree, `stale override` when an obsolete statement conflicts with the
current owner, and `keep` when no outcome-changing conflict is proven.

## Mutation boundary

Default to report-only. Show the exact entry, path, ownership, conflicting current source,
and proposed replacement or deletion. Require item-level current-turn approval before
deleting or semantically rewriting any rule or auto-memory entry, even with initial
`--apply`. Preserve unrelated entries and file structure. Never rewrite generated,
vendor-managed, or unknown-ownership context.

After an approved edit, reread effective context and forward-test the original corrected
scenario. A text deletion alone does not prove that the stale behavior is gone. If the
same behavior remains, report `Fail` without broadening cleanup.

When no persistent statement is attributable, keep the context and propose
`tk-skill-diagnose`. When the current skill is the defective owner, preserve persistent
context and propose `tk-learn`. Do not invoke either automatically.
