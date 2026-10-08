# Visual grammar

Read when a figure may clarify a relationship in an explanation, change walkthrough,
course or research report. This reference owns representation choice and diagram geometry;
[HTML output](html-output.md) owns offline rendering, accessibility, navigation, themes and
render verification. Reuse those contracts without adding a renderer or calling another skill.

## Choose a representation

Identify the reader's question and the verified relationship before choosing a visual type.
Keep prose for a simple fact, condition or conclusion. Prefer a semantic table for dense
attributes or exact comparisons, with expandable evidence when needed. Use a chart for
numeric magnitude, trend or distribution; follow HTML output's data-visualization rules.
Use a diagram when structure, branching or order becomes easier to understand visually.
Use an interactive figure only when changing an input, state or event teaches a mechanism;
its complete static explanation must remain available.

Do not add a figure just for variety or decoration, duplicate prose without reducing
reasoning effort, or turn an exact numeric comparison into a less precise diagram.

| Relationship the reader needs | Useful grammar |
| --- | --- |
| Components and connections in one system | Architecture |
| Conditions and alternative outcomes | Flowchart |
| Time-ordered messages between actors | Sequence |
| States, triggers and guarded transitions | State machine |
| Data transformations or processing stages | Data flow |
| Dated events | Timeline |
| Ownership and handoffs across participants | Swimlane |
| Parent/child hierarchy | Tree |
| Prerequisites or dependencies | Dependency graph |
| Added, removed or rewired system relationships | Architecture delta |

Use one primary grammar for one question. When two grammars need substantial treatment,
split an overview and detail rather than mixing their conventions. Preserve source identities,
edge direction, timing, guards, outcomes and unknown connections; never invent an edge to
complete the layout. Name the visual's scope so a focused view does not imply full coverage.

## Bound complexity without shrinking meaning

Include only relationships needed for the question. Combine elements only when the distinction
is irrelevant to that question, with the grouping named. If labels, spacing or traceability
suffer, split overview/detail and keep an explicit mapping between them. Do not solve crowding
by shrinking text or silently deleting an important relationship. No universal node quota or
upstream pixel ceiling substitutes for the actual reader and viewport checks.

## Verify geometry and correspondence

Trace every connector from its source to its destination in the rendered figure. Repair
overlapping/shared strokes, ambiguous crossings, labels hiding a connection, routes passing
through unrelated nodes, clipped endpoints and indistinguishable attachment points. Use
clear routes and enough separation; an orthogonal path is useful when it improves tracing,
not a mandatory brand style. Label the relationship when direction alone cannot explain it.
Keep readable labels and use text or shape as well as color for status distinctions.

For structure changes, keep the same component identities and spatial correspondence in
Before and After wherever practical. Pair the views with a Changes ledger identifying
added, removed, changed, moved and rewired elements as applicable. Preserve unchanged context;
an attribute-only change usually needs a table rather than a topology diagram.

Inspect the actual figures at the required HTML viewports/themes, including the complete
static form of an interactive figure. A clean page-width measurement does not prove all
diagram content is reachable: check clipping and any local scroller. Correct geometry
failures before claiming visual acceptance; report unavailable checks honestly.

## Distillation provenance

Reviewed 2026-10-07 at `cathrynlavery/diagram-design@d1376371965f513d99cc9ec388835d255c5c88d5`:
`skills/diagram-design/SKILL.md` and relevant sections of `references/layout-budget.md`,
`references/semantic-patterns.md`, `references/primitives-core.md` and
`references/output-spec.md` under that package. Implementation and
inline rationale were inspected; separate upstream behavior evals and runtime efficacy are
unverified. Keep question-led representation and traceable geometry; adapt semantic selection,
overview/detail and architecture deltas to TigerKit's existing HTML contract. Omit upstream
branding, fonts/palette, onboarding, reference catalog, import/export workflow and renderer.
Original MIT notice is included in each consuming package's `LICENSE.txt`.
