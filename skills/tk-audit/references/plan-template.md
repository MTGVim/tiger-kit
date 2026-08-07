# Handoff plan adaptation

Adapted from `shadcn/improve` at source snapshot
`03369ee6d7cafbfcecc4346539b05b3dc0a603bb`. The upstream template's quality
bar is applied to each `AUD-*` finding rather than copied as a second plan
lifecycle.

A cheaper executor must receive self-contained context, exact paths and
symbols, current-state excerpts or evidence, repository conventions, commands
with expected results, hard in/out boundaries, assumptions, and explicit
STOP/report-back conditions. Stamp the finding with the audited HEAD and say
how to handle drift. Keep dependencies and maintenance notes grounded.

`tk-audit` never writes `plans/`, implementation code, units, or remote issues.
`tk-drive` owns downstream R/AC, execution units, and decisions.
