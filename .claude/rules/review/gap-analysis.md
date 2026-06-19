# Gap Analysis Rules

## GAP-001: Treat SoT as comparison material, not absolute truth

- Use `SoT` for Product/Design/Design System/Engineering/QA/Analytics requirements used in the current comparison.
- Do not call any source absolute truth.
- If sources conflict, record ambiguity or source conflict instead of silently merging them.
- If evidence is insufficient, mark the observation as `ambiguous`, `missing evidence`, or `unverifiable` instead of accepting a finding.
- If external evidence is inaccessible, keep it as pending evidence and do not invent a requirement.

## GAP-002: Separate evidence from interpretation

- Label direct observations as Evidence.
- Label inferred conclusions as Interpretation.
- Label user-confirmed or source-confirmed items as Decision.
- Label proposed next steps as Suggestion.
- Keep raw source text and derived comparison text separate.

## GAP-003: Use TigerKit Slim `/tk:gap` shape

- `/tk:gap` is one-shot SoT ↔ Current Implementation analysis.
- `/tk:gap` must not produce sealed workflows, workflow hashes, launch receipts, runner plans, advisor dispatch, or autopilot policies.
- Classify gaps as `missing`, `mismatch`, `overbuilt`, or `ambiguous`.
- Findings must include SoT, Current, Evidence, Impact, Priority, and Suggested fix.
- Accepted finding priority should be `P0`, `P1`, or `P2`.
- `P3`, duplicate, unverifiable, source conflict, not-user-visible, not-actionable, low-confidence, missing-evidence, and missing-producer-evidence observations are not confirmed Findings.
- Visible UI copy differences are actionable when confirmed contracts require exact copy. Meaning similarity is not enough unless the contract explicitly allows variation.

## GAP-004: Match output to user-facing contract

Default `/tk:gap` output uses this shape:

```md
## Gap Summary

| Area | SoT | Current | Gap | Impact | Priority |
|---|---|---|---|---|---|

## Findings

### 1. <finding title>
- SoT:
- Current:
- Evidence:
- Impact:
- Priority:
- Suggested fix:

## Ambiguities / Missing Evidence

| Ref | Question | Evidence checked | Impact | Recommendation |
|---|---|---|---|---|

## Recommended Next Steps

1. <next step>
```

Do not print or write launch-era surfaces as active gap output:

- `GAP_READY`
- `GAP_AUTO_LAUNCHED`
- sealed workflow
- `tigerkit-launch-workflow`
- workflow hash
- `/tk:launch` next action

## GAP-005: Explore ambiguity, then use consent gate

Do not decide silently when any of these apply:

- Requirements document and code conflict.
- Product Spec, Design Spec, API contract, QA expectation, or source priority can be read more than one way.
- Similar implementations exist with different patterns.
- Spec reference or source basis is inaccessible.
- UI/UX intent cannot be confirmed by copy or screenshot alone.
- API response, DTO, permission, persistence, or state transition is unclear.
- Change scope can affect common modules.
- Decision belongs to user, PM, Design, BE owner, QA, or another department.

Required handling:

- First explore code, docs, similar implementations, repo rules, and reuse surfaces enough to avoid avoidable questions.
- If still unclear, do not accept a finding from the likely interpretation.
- Record an ambiguity or clarification request with evidence, impact, recommendation, and status.
- For UI decisions, include TUI/ASCII prototypes when useful.

## GAP-006: Require producer evidence for producer-absence claims

- A producer-absence claim says a backend, API, serializer, DTO, data layer, or other producer does not provide, persist, transform, expose, or cover a required value or behavior.
- Do not infer producer absence from consumer-side UI shape, fallback/default branch, empty state, mock, fixture, mapper, or missing consumer usage alone.
- Producer-absence claims need direct producer-side evidence such as API contract, schema, serializer, endpoint response, data model, persistence logic, backend test fixture, or owner-confirmed behavior.
- If only consumer-side evidence exists, keep the observation as ambiguous, missing producer evidence, missing evidence, or unverifiable.

## GAP-007: Separate design source trust axes

- Treat structural or metadata evidence as `source_type=structural_context`.
- Treat screenshots, screen recordings, raster exports, and scaled visual captures as `source_type=visual_capture`.
- Use `visual_capture` for layout, composition, visible state, hierarchy, and presence checks.
- Do not confirm color, spacing, dimensions, typography scale, or other numeric design values from `visual_capture` alone.
- Numeric design values require structural/context evidence, design tokens, or explicit user/source confirmation.
