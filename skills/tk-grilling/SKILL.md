---
name: tk-grilling
description: "Ask one consequential design question at a time with a recommendation and evidence."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: mattpocock/skills
    upstream-skill: grilling
    relationship: adapted
---

# Grilling discipline

Use when a design or plan needs decisions before implementation.

- Inspect code for discoverable facts instead of asking the user.
- Ask only questions that require user judgment, one at a time.
- Include a recommendation and brief reason with every question.
- Do not repeat answered questions or implement before agreement.

Output: question, recommendation, reason. Complete when no consequential user decision remains or the user stops.
