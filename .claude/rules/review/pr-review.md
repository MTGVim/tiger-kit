---
paths:
  - "**/*"
---

# PR Review Rules

## REVIEW-001: Review comments must be directly actionable

- Include severity in the first line.
- Quote source contract evidence and current target evidence.
- Explain why the mismatch matters.
- Provide a required change when the fix is clear.
- Do not post speculative findings as confirmed defects.
- If ambiguity remains after checking code/docs/similar implementations, include the question category (`implementation-blocking` or `reference-only`), recommendation, and evidence.

## REVIEW-002: v7 gap review findings use JudgeMergerAgent decisions

- PR-ready comments derived from `/tk:gap` must use JudgeMergerAgent accepted findings, not raw subagent candidates.
- Use final severity `P0`, `P1`, or `P2` for accepted findings.
- Do not post `P3_nit`, `duplicate`, `unverifiable`, `source_conflict`, `not_user_visible`, `not_actionable`, `low_confidence`, `missing_evidence`, or `superseded_source` rejected candidates as confirmed PR defects.
- Source conflicts and unverifiable items may be written as asks, not confirmed defects.

## REVIEW-003: Preserve evidence and actionability

- Every accepted comment must cite the confirmed source contract and target evidence.
- Every accepted comment must include at least one concrete required change.
- Visible UI copy remains exact-match when a confirmed contract specifies exact copy.
