# Discovery Source Dispositions

## Revision-bound repository findings

Reviewed 2026-10-01: `Data-System-School/agent-skills` at
`a117418ab3596c59d641cab4cb89bdbe560fb277`, `investigate-codebase/SKILL.md`,
`references/orient-large-codebase.md`, `references/analyze-pr-impact.md` and the
`examples/investigate-codebase/README.md` example index. Read the DuckDB IMPACT and
vLLM TRACE reports, including the rule-toggle attribution limitation, a no-GPU
runtime boundary and harness failures. These are upstream-authored observations,
not TigerKit-reproduced benchmark results.

- `keep`: read-only discovery and unresolved dynamic/runtime claims.
- `adapt`: revision/snapshot identity and the minimum sufficient vertical slice in
  existing findings; reconcile intent documents against code/tests/configuration.
- `omit`: mode orchestration, component/file counts, evidence ledger, manifests,
  navigation DAG, traceability indexes and automatic subagent execution.

Compared `DiUS/agent-toolkit` at `6dc62cc0beadc92e7617ee8e8a916da369bfa65c`,
`skills/codebase-discovery/SKILL.md`: freshness and intent reconciliation support
the choice, but its registers and onboarding document workflow are omitted.
Its dedicated runtime eval evidence was not reproduced and remains unverified.
The existing single discovery resume artifact and research/roadmap/prep owners remain intact.

Reviewed 2026-09-30:

- `mattpocock/skills` at `d81f3a183412e71a5b1e84ca21bc1a35eea03a60`:
  `skills/engineering/wayfinder/SKILL.md`, `docs/engineering/wayfinder.md` and
  `skills/productivity/grilling/SKILL.md`. Implementation and embedded design rationale were read.
  Dedicated upstream behavior evals for wayfinder were not found; runtime efficacy is unverified.
- `EveryInc/compound-engineering-plugin` at `7b867109526165def0cc2a31b7c348b7308ae2c8`:
  relevant research/evidence and handoff sections of `skills/ce-plan/references/research.md`,
  `universal-planning.md` and `plan-handoff.md`, plus `tests/skill-eval-cell/packs/ce-plan-sizing.md`.
  These supply evidence-grounding, authority continuity and planning-boundary criteria, not a
  reproduced benchmark. Remaining provider/runtime procedures were intentionally not adopted.
- Existing TigerKit `tk-roadmap/references/sources.md` already adapts outcome planning and
  unspecified-versus-excluded scope from wayfinder. That stays owned by roadmap.

| Disposition | Element | Reason |
| --- | --- | --- |
| keep | Destination, precise items versus fog, dependencies and newly exposed questions | A discovery result can change the investigation itself. |
| adapt | Decision tickets and frontier | Conversation or one local resume artifact, without issue-tracker ownership or a DAG engine. |
| adapt | Research, repository, user and prototype modes | Read-only evidence gathering; experiments need a separate execution authority. |
| adapt | Evidence-to-plan handoff and validation criteria | Findings determine roadmap/prep/no-go/unavailable exits; no mandatory skill chain. |
| omit | Tracker labels, assignment, one-ticket sessions, workers and scheduler | TigerKit packages stay independent and self-contained. |
| omit | Mandatory deepening, review personas, provider routing and global state | These do not resolve the distinct discovery intent. |

## Owner comparison

`tk-research` investigation starts with a bounded downstream decision, compares alternatives
and ends with a sourced recommendation. Its evidence standards are extracted into its local
`evidence.md` and synchronized to discovery, without adding a continuing map to research.
`tk-roadmap` can begin with unclear direction and plan an investigation milestone, but stops
at the planning result. Adding repeated evidence resolution, fog graduation, dependency repair
and milestone invalidation would expand that boundary. Discovery owns precisely those changes;
it does not replace either owner or become a prerequisite.

Routing cases distinguish an explicitly selected continuing investigation from one external
comparison and an agreed-direction roadmap. Behavior cases independently cover new questions,
retirement, changed prerequisites, stopping, unavailable evidence and mutation boundaries.
Original MIT notices are in [upstream licenses](../UPSTREAM-LICENSES.txt).
