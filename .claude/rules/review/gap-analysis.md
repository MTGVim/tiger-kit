---
paths:
  - "**/*"
---

# Gap Analysis Rules

## GAP-001: Treat basis as comparison material, not absolute truth

- Use `basis` for the material used in the current comparison.
- Do not call basis absolute truth.
- If basis sources conflict, report `conflicting_sources`.
- If evidence is insufficient, report `cannot_verify`.
- Do not synthesize a new requirement by silently merging conflicting sources.

## GAP-002: Separate evidence from interpretation

- Label direct observations as Evidence.
- Label inferred conclusions as Interpretation.
- Label user-confirmed or basis-confirmed items as Decision.
- Label proposed next steps as Suggestion.
