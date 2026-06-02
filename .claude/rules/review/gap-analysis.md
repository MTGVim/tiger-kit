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

## GAP-004: Use `G<number>` IDs and meaningful scopes

- Findings use a single user-facing ID such as `G1`, `G2`.
- `G<number>` is the canonical handle users refer to in conversation.
- The same finding must use the same `G<number>` across `mode=analysis`, `mode=review`, and `mode=both` within one generated gap result.
- Do not emit separate slug-style stable IDs such as `gap-<scope-slug>-<finding-slug>`.
- Do not emit a `Stable` column or `Stable:` line.
- Rule IDs in this file, such as `GAP-001` and `GAP-002`, are repo rule IDs. They are not `/tk:gap` finding IDs.
- Scope labels must include a human-readable title, menu, page, component, row, or equivalent name.
- Do not use section numbers alone as Scope labels.

## GAP-005: Match output to the selected mode

- `mode=analysis` emits only compact `## Summary Table`, `## Findings`, and `## Bottom Recap`. Summary Table must use `Target`, `Counts`, `Next`; Findings must use `ID / Scope`, `Class`, `Evidence`, `Finding`, `Ask`; Bottom Recap repeats the key counts and next action after long Findings.
- `mode=review` emits PR-ready basis-target gap comments only; it is not general code review and must not include `Stable:` lines.
- `mode=both` emits analysis first, then basis-target gap comments, using the same `G<number>` IDs for the same findings.

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

## Target freshness: Check current implementation freshness before comparing

When the target means `current implementation`, current working tree, current branch, or local checkout:

- Identify the integration branch tip first. Prefer the repository default remote branch; use `origin/main` when that is the repository convention.
- Refresh or verify remote metadata when possible. If freshness cannot be verified, report base freshness as `cannot_verify` evidence.
- If local `HEAD` is behind the integration branch, check whether files in the requested scope or target evidence changed between `HEAD` and the integration tip.
- If behind changes affect the target area, compare against the integration branch tip shape instead of stale local `HEAD`, and report the base state in the Summary Table or first finding.
- If behind changes do not affect the target area, the local target may still be used, but report the freshness check briefly.
- If the user explicitly names a commit, branch, PR diff, or working tree state as the target, do not switch targets silently; report stale status as evidence instead.
