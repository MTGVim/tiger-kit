---
name: tk-to-spec
description: "[user] Synthesize current decisions and evidence into an implementation specification. Use only when explicitly invoked by the user."
disable-model-invocation: true
argument-hint: "<conversation, source, or request> [--output <path>|--print-only]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: to-spec
    relationship: adapted
---

# To Spec

Use only when the user explicitly invokes this skill. Do not activate it automatically.

Source priority: user-designated source, current decisions, ticket/document, relevant code, then existing `.tigerkit/spec.md`. Do not start an interview, create tickets, publish, or implement.

Write to the user path, print-only output, or `.tigerkit/spec.md`. If an existing spec is for the same work, retain valid decisions; otherwise replace it without an archive. For `.tigerkit/` output, create parents lazily, write through a same-directory temporary file and rename when possible, never edit `.gitignore`, and warn briefly if the scratch path is not ignored. Separate facts, decisions, assumptions, and unresolved conflicts.

Required sections: Problem, Goal, Scope (in/out), Requirements, Acceptance criteria, Verification. Add Status, Existing behavior, Expected behavior, Constraints, Decisions, Assumptions, Unresolved when useful.

Report path, Draft/Ready status, and unresolved items.
