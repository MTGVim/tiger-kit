---
name: tk-code-review
description: "[auto] Review a fixed diff for specification compliance and code quality without editing it."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: mattpocock/skills
    upstream-skill: code-review
    relationship: adapted
---

# Code Review discipline

Pin the diff range and inspect only that range. Separate requested/spec compliance from code quality. Do not edit code or start an automatic re-review.

Every finding includes `Critical | Important | Minor`, a title, and `file:line` evidence. If there are no findings, say so.

Output `## Findings` and `## Verdict` with `Pass | Changes requested`.
