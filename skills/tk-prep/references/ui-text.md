# UI Text Evidence

Read this when a task names or changes a user-visible label or navigation path. Apply the entrypoint UI Evidence guard.

Distinguish the current verified string from proposed replacement copy. Record the source and target environment,
locale, and role when they affect visibility. Trace source literals through the actual render path and transformations;
a translation entry or API response alone does not prove the final displayed value or menu hierarchy.

When no visible label exists, use a verified structural description or verified path ending in an exact title.
A destination title alone never verifies the preceding steps. Leave unknown segments unverified and obtain the
missing source, redacted response, or scoped browser evidence before treating the route as executable QA guidance.
Ticket/spec text establishes requested behavior, not proof of existing UI. Preserve conflicting provenance and resolve
material conflicts in preparation instead of silently choosing a source.

## Distillation basis

Reviewed `microsoft/playwright` at `18205280b6112a4a08238195942c4fa30c199a62`:
[locator guidance](https://github.com/microsoft/playwright/blob/18205280b6112a4a08238195942c4fa30c199a62/docs/src/locators.md),
[implementation](https://github.com/microsoft/playwright/blob/18205280b6112a4a08238195942c4fa30c199a62/packages/playwright-core/src/client/locator.ts), and
[text selector tests](https://github.com/microsoft/playwright/blob/18205280b6112a4a08238195942c4fa30c199a62/tests/page/selectors-text.spec.ts).
Keep current DOM evidence and element-scoped lookup. Adapt the distinction between locator matching and actual text:
exact text locators still normalize whitespace, so a match alone cannot establish a verbatim quote. Omit framework
installation and runtime ownership changes. The TigerKit-specific correction is per-segment navigation evidence,
explicit external boundaries, and concrete evidence requests when source cannot establish the rendered UI.
