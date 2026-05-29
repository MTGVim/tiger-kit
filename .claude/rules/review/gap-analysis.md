# Gap Analysis Rules

## GAP-001: Treat basis as comparison material, not absolute truth

- Use `basis` for the material used in the current comparison.
- Do not call basis absolute truth.
- If basis sources conflict, report Status `conflicting_sources`.
- If evidence is insufficient, report Type `unverifiable` and Status `cannot_verify`.
- If external evidence is inaccessible, report Type `unverifiable` and Status `blocked_external`.
- Do not synthesize a new requirement by silently merging conflicting sources.

## GAP-002: Separate evidence from interpretation

- Label direct observations as Evidence.
- Label inferred conclusions as Interpretation.
- Label user-confirmed or basis-confirmed items as Decision.
- Label proposed next steps as Suggestion.

## GAP-003: Use the current `/tk:gap` output taxonomy

- Type must be one of `missing`, `mismatch`, `convention`, `unverifiable`, `out_of_scope`.
- Severity must be one of `critical`, `major`, `minor`.
- Status must be one of `needs_fix`, `cannot_verify`, `conflicting_sources`, `blocked_external`, `out_of_scope`.
- Do not use Judgment as an output axis.
- Visible UI copy differences are Type `mismatch`; exact match is required unless basis explicitly allows variation.

## GAP-004: Use stable finding IDs and meaningful scopes

- Stable finding IDs use `gap-<scope-slug>-<finding-slug>`.
- Do not use sequential finding IDs like `GAP-001` for findings.
- Rule IDs in this file, such as `GAP-001` and `GAP-002`, are repo rule IDs. They are not `/tk:gap` finding IDs.
- Scope labels must include a human-readable title, menu, page, component, row, or equivalent name.
- Do not use section numbers alone as Scope labels.

## GAP-005: Match output to the selected mode

- `mode=analysis` emits only compact `## Summary Table`, `## Findings`, and `## Bottom Recap`. Summary Table must be a table with result counts and key next action; Bottom Recap repeats the key counts and next action after long Findings.
- `mode=review` emits PR-ready basis-target gap comments only; it is not general code review.
- `mode=both` emits analysis first, then basis-target gap comments, using the same stable IDs for the same findings.

## GAP-006: Explore ambiguity before asking or deciding

Do not decide silently when any of these apply:

- Requirements document and code conflict.
- 2+ similar implementations exist with different patterns.
- Spec reference or source basis is inaccessible.
- reuse-map lacks an entry and repo-wide exploration is not sufficient yet.
- UI/UX intent cannot be confirmed by copy or screenshot alone.
- API response, DTO, permission, or state transition is unclear.
- Change scope can affect common modules.

Required handling:

- First explore code, docs, similar implementations, repo rules, and reuse-map more.
- If still unclear, create questions instead of guessing.
- Each question must include recommendation and evidence.
- Split questions into `implementation-blocking` and `reference-only`.
- In `mode=analysis`, keep questions inside the single Findings table.
- In `mode=review`, write ambiguity as an `Ask:` with the question category, recommendation, and evidence, not as a confirmed defect.
