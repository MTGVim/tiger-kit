## `PR template`

Before creating any `PR body`, check supported template locations on the default branch.

- Root
- `docs/`
- `.github/`
- `PULL_REQUEST_TEMPLATE/` under each location

If exactly one template applies, preserve its heading order, checklists, HTML comments, and required sections.
If multiple templates exist and there is no basis for choosing one, explain the candidates with one recommendation and ask the user to choose before publication approval.
If the template cannot be read, do not invent a body.

Choose title guidance in this order: explicit repository instruction, normative current PR template or maintainer
documentation, verified recent merged-PR convention, then the existing fallback. History can establish a convention only
when no higher-authority current guidance applies. Surface a conflict instead of silently overriding the stronger source.

Describe the change by reviewable concern (behavior, module or contract), derived from `base...HEAD`,
not by commit order. Do not list commit SHAs or one bullet per commit unless the template or repository
instruction asks for it; the PR's commit list already carries that history. Recent merged-PR bodies
inform tone and section use, not commit-by-commit structure. When updating an existing PR after new
commits, re-derive the affected sections from the current `base...HEAD` instead of appending per-commit lines.

Before finalizing a body whose architecture, flow, state transition, dependency or migration
relationship is materially easier to review visually, read [GitHub-native PR visuals](../../tk-pr-guidance/references/github-visuals.md).
Use Mermaid selectively and evidence-first; prefer a table for exact numeric comparisons and keep
material meaning available in prose.

Before finalizing the body, assess material reversibility and blast radius from the verified publication input: affected callers, users, surfaces, data and contracts; the concrete rollback or recovery path; and any destructive migration, irreversible external side effect or compatibility break. Reverting code does not restore deleted data or undo external actions. Preserve unknown recovery evidence instead of describing the change as cheaply reversible. Put useful facts in the template's existing risk, rollback, migration or deployment section; preserve its headings, order, comments and checklists, without adding a duplicate section. If no template or stronger format applies, the fallback body may include a compact risk/recovery section when it adds information. Low-risk changes need no empty risk prose or decorative one-way/two-way labels. This assessment grants no implementation or new investigation authority.

Apply UI Evidence to PR bodies and QA steps. Before publication, reconcile each required UI literal and navigation claim against the supplied evidence. Include a compact UI evidence gap report in the preparation output: item, source/status (observed, render-bound source, user-provided, or `Unverifiable`), limitation, and requested input. State explicitly when no required gaps remain; use N/A only when there are no UI claims. Keep user-provided text distinct from independent observation and retain unresolved items in the PR/QA limitations. Ask for the missing exact label, contextual capture, or connection evidence item by item; incorporate supplied answers only for the claims they support. Do not start a new investigation from this publication-only phase.

Use an entry path only when every step is verified; breadcrumb-only evidence permits a hierarchy description, not click instructions. If a required QA step or publication evidence depends on an unresolved item, stop publication as `Blocked | Unverifiable` and return the concrete input request. Optional gaps may remain only as explicit limitations, without invented labels or executable path guidance.

When a title or body summarizes or interprets repository behavior, requirements, ownership, impact, or domain meaning,
lazy-load [domain context](../../tk-repository-guidance/references/domain-context.md) when repository-owned context exists. Read only the relevant
mapped context, preserve canonical vocabulary, and never replace verified UI literals with glossary terms.

For a stack, apply the same title/template rules to every layer. Each layer body must explain only that layer's review surface and, when useful, its dependency on the preceding layer rather than duplicating the full feature summary into every PR.

Source: the reversibility/blast-radius safeguard adapts `mattpocock/skills@d81f3a183412e71a5b1e84ca21bc1a35eea03a60`, `skills/engineering/pr/SKILL.md`. Keep TigerKit's template, evidence and publication contracts; omit the mandatory upstream body and labels. Original MIT notice: [LICENSE.txt](../LICENSE.txt).

For a user-owned QA inventory, recommend explicit `/tk-qa-sheet` outside this publication-only phase and consume only its returned Markdown section; never auto-invoke the user-only skill or start its investigation here.

