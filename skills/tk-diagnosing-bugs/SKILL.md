---
name: tk-diagnosing-bugs
description: "Diagnose difficult bugs by reproducing, minimizing, testing hypotheses, and verifying a regression fix."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: mattpocock/skills
    upstream-skill: diagnosing-bugs
    relationship: adapted
---

# Diagnosing Bugs

Use for difficult or unclear failures. Follow [the investigation loop](references/investigation.md).

Do not patch before reproducing the reported symptom. Distinguish multiple falsifiable hypotheses, use observations to eliminate them, and separate root cause from symptoms. Fix the shared cause, add a regression check at the correct seam when valuable, then rerun the original reproduction.

Report reproduction, root cause, fix, and regression evidence.
