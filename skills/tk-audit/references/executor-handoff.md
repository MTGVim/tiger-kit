# Finding handoff

Write each `AUD-*` finding so the next executor or `tk-prep` can understand the work
without this conversation or the audit session.

- **Self-contained context**: Include exact paths/symbols, current evidence,
  repository rules, and relevant exemplars.
- **Boundaries**: Include in/out scope, assumptions, dependencies, and concrete
  `STOP/report-back` conditions.
- **Verification**: Include commands, expected results, the audited HEAD, any pinned
  documentation comparison commit, and drift handling. Recheck upstream-only findings
  against the executor's actual target; they do not establish a local HEAD defect.
- **Safety**: Include only secret locations and credential types. Do not copy values,
  cookies, tokens, or private identity data.

These quality criteria adapt `shadcn/improve` at source snapshot
`03369ee6d7cafbfcecc4346539b05b3dc0a603bb`; they do not create a second plan lifecycle.
`tk-audit` does not write `plans/`, implementation code, execution units, or remote
issues. When an executable task contract, AC, and verification plan are needed,
`tk-prep` re-reads current evidence and prepares the Seed in `.tigerkit/seed.md`. A finding only prepares
reusable evidence; it grants no implementation, execution-unit, or remote publication
authority.
