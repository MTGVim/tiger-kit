---
name: tk-tdd
description: "Use test-driven development at a valuable behavior seam when red-green-refactor improves confidence."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: mattpocock/skills
    upstream-skill: tdd
    relationship: adapted
---

# TDD discipline

Use only when a meaningful test seam exists.

1. Choose the highest useful public behavior seam.
2. Write one vertical-slice test and run it red.
3. Implement the minimum behavior and run it green.
4. Refactor without changing behavior.

Test behavior, not internals; avoid test-only production distortion. Do not force TDD when no valuable seam exists. Report the red command/result, green command/result, and implemented behavior.
