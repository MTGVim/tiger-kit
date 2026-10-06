# Grooming source dispositions

## Model-fit audit

Reviewed `anthropics/skills` at `683bc88e56f3e09ba94f7055977f3d3aa499f202`:
`skills/claude-api/shared/prompt-audit.md`, its embedded rationale and verification procedure,
and the target-model sections in `skills/claude-api/shared/model-migration.md`.
The source is Apache-2.0; it is comparison material, not vendored text or runtime code.
Separate upstream behavioral eval results for prompt-audit are `unverified`.

- `keep`: target-relative evidence, preservation of author context and fragile contracts,
  confidence-qualified observations, and a valid clean/no-change outcome.
- `adapt`: pressure, output limits, version-relative prose, runtime history, stale facts,
  conflicting instructions, exact-phrase modes, and stale eval expectations become existing
  GR findings. Explicit user formats remain binding; model-specific claims need current primary
  evidence. Existing ownership and mechanical-versus-semantic authority determine the action.
- `adapt`: provenance is a conditional maintenance record; behavioral comparison stays with the
  existing instruction-economy reference. Conflicts stay pending regardless of Git recency.
- `omit`: application/API migration, request builders, tool-description audits, model routing,
  automatic broad inventory, mandatory report/diff artifacts, and upstream implementation or fixtures.

The concrete TigerKit gaps were discretionary output caps and divergent package-local contracts.
This branch adds target-model classification without changing invocation kind, description, vendor
ownership, or the existing apply boundary. Local cases compare prior and candidate behavior;
they do not establish efficacy on every target model.
