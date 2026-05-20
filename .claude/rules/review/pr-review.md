---
paths:
  - "**/*"
---

# PR Review Rules

## REVIEW-001: Review comments must be directly actionable

- Include severity in the first line.
- Quote basis evidence and current target evidence.
- Explain why the mismatch matters.
- Provide a suggested change when the fix is clear.
- Do not post speculative findings as confirmed defects.

## REVIEW-002: Review mode emits PR-ready comments

- In review mode, output comments that can be pasted into a PR.
- Avoid long analysis tables in review mode unless the user explicitly asks for both analysis and review.
