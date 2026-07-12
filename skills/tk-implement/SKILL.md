---
name: tk-implement
description: "Implement and verify a requested code change. Use only when explicitly invoked by the user."
disable-model-invocation: true
argument-hint: "<request, ticket, or spec>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: implement
    relationship: adapted
---

# Implement

Use only when the user explicitly invokes this skill. Do not activate it automatically.

Follow `understand → inspect → implement → verify → report`. Source priority is the current request, confirmed conversation decisions, relevant `.tigerkit/tickets.md`, relevant `.tigerkit/spec.md`, repo guidance, then code/tests. Existing files are not automatically relevant.

Default to direct implementation. Delegate only for clean isolation or real independent parallelism; never nest delegation or let a subagent invoke user-invoked TigerKit skills. Apply installed disciplines when useful, but do not block if absent. See [delegation](references/delegation.md) and [review boundary](references/review-boundary.md).

Choose change-related verification. Classify failures as change-related, pre-existing, environment, or unverifiable. Do not automatically run another user-invoked skill, commit, push, open a PR, or merge.

Report `## Changed`, `## Verification`, and non-empty `## Remaining risks`, describing behavior rather than only files.
