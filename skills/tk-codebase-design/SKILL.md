---
name: tk-codebase-design
description: "Identify evidence-backed structural pain and propose the smallest effective codebase design improvement."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: tigerkit
    relationship: native
---

# Codebase Design discipline

Use when changes repeatedly scatter across files, ownership is unclear, test seams are absent, similar bugs/conflicts recur, or feature cost keeps rising.

Inspect boundary leaks, ownership confusion, coupling hotspots, repeated pain, and incremental migration shape. Cite concrete evidence and propose the smallest effective structural improvement. Do not recommend vague rewrites or implement automatically.

Complete with evidence-backed hotspots, impact, and smallest safe direction.
