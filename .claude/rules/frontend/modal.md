---
paths:
  - "src/**/*.{ts,tsx,js,jsx}"
---

# Modal Rules

## MODAL-001: Use repository modal wrapper

- Use the repository modal wrapper for modal/dialog UI.
- Do not directly import modal components from external UI libraries for new modal implementation.
- Prefer existing modal wrapper used in nearby code.
