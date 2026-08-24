# Apply handoff planning

Adapted from `shadcn/improve` at source snapshot
`03369ee6d7cafbfcecc4346539b05b3dc0a603bb`. Apply the quality criteria from the
`upstream template` to each `AUD-*` `finding` instead of copying a second plan
lifecycle.

A lower-cost executor or `tk-prep` must receive `self-contained context`, exact paths
and `symbol`s, current-state evidence, repository rules, commands with expected
results, strict in/out boundaries, assumptions, and explicit `STOP/report-back`
conditions. Record the `audited HEAD` in the `finding` and state how to handle `drift`.

`tk-audit` does not write `plans/`, implementation code, execution units, or remote
issues. When an executable task contract, `AC`, and verification plan are needed,
`tk-prep` re-reads current evidence and prepares them in `.tigerkit/seed.md`.
