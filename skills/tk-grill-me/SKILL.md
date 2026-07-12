---
name: tk-grill-me
description: "Pressure-test an idea, plan, design, ticket, or RFC. Use only when explicitly invoked by the user."
disable-model-invocation: true
argument-hint: "<idea, plan, design, ticket, RFC, or path>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: grill-me
    relationship: adapted
---

# Grill Me

Use only when the user explicitly invokes this skill. Do not activate it automatically.

1. Read the request and supplied material; inspect code for answerable facts.
2. Identify unresolved decisions only the user can make.
3. Ask the highest-impact question, with a recommendation and short reason.
4. Apply the answer and repeat one question at a time until decisions converge.

Do not modify source, create specs/tickets, write documents, or repeat answered questions.

Finish with non-empty sections only: `## Decisions`, `## Assumptions`, `## Remaining risks`.
