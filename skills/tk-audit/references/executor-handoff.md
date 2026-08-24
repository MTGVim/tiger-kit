# Lower-cost model handoff

Write each `AUD-*` `finding` so the next model or `tk-prep` can understand the work
without this conversation or the `audit session`.

- **Self-contained context**: Include exact paths/`symbol`s, current evidence,
  repository rules, and relevant `exemplar`s.
- **Boundaries**: Include the `in/out` scope, assumptions, dependencies, and concrete
  `STOP/report-back` conditions.
- **Verification**: Include commands, expected results, the `audited HEAD`, and how to
  handle `drift`.
- **Safety**: Include only `secret` locations and credential types. Do not copy `values`,
  `cookies`, `tokens`, or `private identity` data.

This contract only prepares evidence that `tk-prep` can reuse when creating an
executable `Seed`. It does not grant implementation, execution-unit, or remote
publication authority.
