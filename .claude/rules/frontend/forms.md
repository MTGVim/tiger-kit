---
paths:
  - "src/**/*.{ts,tsx,js,jsx}"
---

# Form Rules

## FORM-001: Prefer repository Formik wrapper / HoC pattern

- Prefer the repository’s Formik wrapper or HoC pattern over direct Formik hooks.
- Use direct Formik hooks only when the surrounding module already follows that pattern or the user explicitly requests it.
