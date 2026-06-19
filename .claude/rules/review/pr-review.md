---
paths:
  - "**/*"
---

# PR Review Rules

## REVIEW-001: Review comments must be directly actionable

- Include severity in the first line.
- Quote source evidence and current target evidence.
- Explain why the mismatch matters.
- Provide a required change when the fix is clear.
- Do not post speculative findings as confirmed defects.
- If ambiguity remains after checking code/docs/similar implementations, include the question category, recommendation, and evidence.

## REVIEW-002: TigerKit Slim gap findings are evidence-first

- PR-ready comments derived from `/tk:gap` must use confirmed Findings from the Slim output, not raw notes or ambiguous observations.
- Use priority `P0`, `P1`, or `P2` for confirmed findings.
- Do not post `P3`, duplicate, unverifiable, source conflict, not-user-visible, not-actionable, low-confidence, missing-evidence, or missing-producer-evidence observations as confirmed defects.
- Source conflicts and unverifiable items may be written as asks, not confirmed defects.

## REVIEW-003: Use `/tk:grill` for reviewer pressure tests

- `/tk:grill` is an optional active TigerKit Slim command for proposal, plan, change, and reviewer-judgment pressure tests.
- Grill output is a question/risk list, not a confirmed defect list.
- Before turning a Grill item into a PR comment, confirm direct source evidence, current target evidence, impact, and a concrete required change.
- If merge readiness needs delegation, use `/tk:afk --patron reviewer` for the scoped decision.

## REVIEW-004: Preserve evidence and actionability

- Every accepted comment must cite the confirmed SoT evidence and current target evidence.
- Every accepted comment must include at least one concrete required change.
- Visible UI copy remains exact-match when a confirmed contract specifies exact copy.
