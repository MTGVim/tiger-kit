---
name: tk-to-tickets
description: "[user] Split a request or specification into independently verifiable vertical tickets. Use only when explicitly invoked by the user."
disable-model-invocation: true
argument-hint: "<spec, plan, or request> [--output <path>]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: to-tickets
    relationship: adapted
---

# To Tickets

Use only when the user explicitly invokes this skill. Do not activate it automatically.

Source priority: user-designated source, current conversation, `.tigerkit/spec.md`, request, relevant code. Create outcome-oriented vertical behavior slices with independent acceptance criteria and verification. Keep a behavior's tests in its ticket; do not create horizontal type/API/UI/test-only tickets.

Write to the user path or `.tigerkit/tickets.md` as `# <Feature> Tickets`, then tickets with Goal, Scope, Dependencies, Acceptance criteria, Verification, and optional Notes. For `.tigerkit/` output, create parents lazily, use temporary-file-plus-rename when possible, never create timestamp archives or edit `.gitignore`, and warn if the scratch path is not ignored. Do not implement or publish to a remote tracker.

Report path, ticket count, dependencies, and unresolved decomposition issues.
