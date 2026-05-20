---
paths:
  - "src/**/*.{ts,tsx,js,jsx}"
---

# Frontend Library Rules

## LIB-001: Avoid new direct antd usage

- Do not introduce new direct `antd` imports for feature implementation unless explicitly approved.
- Prefer existing internal components and repository wrappers.
- Existing legacy `antd` usage does not imply approval for new usage.
