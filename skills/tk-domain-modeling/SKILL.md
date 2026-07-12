---
name: tk-domain-modeling
description: "[auto] Sharpen domain language, test concept boundaries, and record only durable terms or consequential decisions."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: mattpocock/skills
    upstream-skill: domain-modeling
    relationship: adapted
---

# Domain modeling discipline

Use when terminology or domain boundaries are ambiguous.

- Check existing glossary/context files and code for conflicting meanings.
- Test concepts with concrete edge cases and distinguish nearby terms.
- Record domain meaning only; keep implementation structure out of glossaries.
- Suggest an ADR only when a choice is hard to reverse, surprising without context, and had real alternatives.
- Do not implement the design.

See [term and ADR criteria](references/terms-and-adrs.md). Complete when the relevant vocabulary and decision boundary are unambiguous.
