---
name: tk-grill-with-docs
description: "[user] Pressure-test decisions and record settled domain terms or consequential ADRs. Use only when explicitly invoked by the user."
disable-model-invocation: true
argument-hint: "<idea, plan, design, ticket, RFC, or path>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: grill-with-docs
    relationship: adapted
---

# Grill With Docs

Use only when the user explicitly invokes this skill. Do not activate it automatically.

Run the one-question-at-a-time grilling behavior while maintaining domain documentation. Search in order: `CONTEXT-MAP.md`, area `CONTEXT.md`, root `CONTEXT.md`, `docs/adr/`, then the repo's existing ADR convention. Create a file only when a term or qualifying ADR must be recorded.

- Write settled domain meaning using [context format](references/context-format.md).
- Write an ADR only when all criteria in [ADR format](references/adr-format.md) hold.
- Do not create a spec/ticket, implement code, or turn minor choices into ADRs.

Complete when important decisions converge and only qualifying terms/decisions are recorded.
