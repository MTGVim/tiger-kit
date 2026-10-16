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

## Reader-author dialogue as a visual grammar

Dialogue is a presentation grammar, not a substitute for evidence. Use it only when a realistic
reader question makes background, intuition, a boundary or a likely misconception easier to
follow. The reader must not ask artificial questions merely to restate the next paragraph, and the
author must answer directly from verified claims while preserving uncertainty.

Keep precise artifacts outside the dialogue when they are clearer there: code, file maps, numeric
comparisons, tables, diagrams, verification outcomes and citations remain structured evidence.
A dialogue view may point to those artifacts but must not paraphrase away a material condition.
For easy-dialogue mode, reduce prerequisites and sentence complexity while retaining the actual
mechanism, technical terms needed for correctness, and the point where an analogy stops matching.

## Plan an evidence-backed visual storyboard

For a nontrivial document, plan visuals only after establishing the prose claims and their evidence.
For each candidate figure, write a compact internal storyboard: the reader's specific question,
the one claim the figure should make easier to understand, the verified entities and links,
the chosen static visual grammar, and the source location or assumption behind each material
label, edge, value and transition. This is a planning check, not a required user-facing
worksheet, file, JSON schema, new approval gate, or separate agent. Omit it for obvious
single-fact presentations and straightforward semantic tables.

Choose the view by the cognitive task: compare alternatives side by side, orient a hierarchy
with a stable spatial map, trace causal order with directed connections, show temporal change
with shared identities and scales, or explore a stateful mechanism with controlled steps.
Use one central takeaway per figure and a caption that states what the marks demonstrate,
including important scope limits. If multiple claims compete for attention, divide the view
into an overview and one focused detail rather than shrinking everything or producing
ornamental cards. Do not translate unsupported prose into apparently factual graphics.

Before rendering a stepper or interactive sequence, specify each frame's same entity IDs,
actual state, guard/event, and outgoing transition. Render each frame from those facts, not
from independently improvised captions or decorative motion. Only introduce progression if
intermediate states expose a cause that before/after alone hides; start paused, allow backward
steps and reset, and retain the meaningful static baseline. Follow the calling skill's
interactive-examples contract when one exists.

After rendering, audit the storyboard against the actual figure: every arrow, number, label,
highlight and step must be supported by the cited source or marked illustrative/inferred.
Inspect whether the reader can answer the original question from the visual plus caption
without guessing a hidden legend. A visually attractive but ambiguous or unsupported figure
fails this check. Reuse existing browser/HTML verification rather than creating another
runtime, image service or verification harness.

## Decision evolution versus dated event timeline

A dated event timeline answers what happened and when. A decision-evolution view answers
which *documented* finding changed an assessment and why. Choose the latter only with
actual prior and revised judgments on record; final conclusions, file order and publication
dates alone do not prove an intervening decision. Without that history, use an evidence-to-
recommendation map or comparison table instead.

For each supported change, retain the previous assessment, newly discovered evidence,
revised assessment, affected candidate/condition and source link. Label the order as
recorded decision sequence when calendar times are unavailable; never invent timestamps
or imply that mere succession establishes causality. Do not show rejected candidates as
failed experiments when they were never tried. Clearly distinguish facts, inference,
recommendations and still-open limits. Give each change one concise takeaway and keep
long source detail available without hiding material caveats.

In offline HTML, use semantic ordered steps or compact cards before custom SVG. Where
the relationship cannot be understood without interacting, progressive enhancement
may reveal source details or toggle verified views, but full conclusions and essential
evidence remain visible without JS. Prefer a static figure if interaction adds no insight.
Verify keyboard navigation, narrow-screen reading, source anchors and matching captions
under the existing HTML contract. Apply `clear-writing.md` to labels and sentences;
emojis are optional semantic signposts, never the only status cue or a compulsory decoration.

## Card flow for grouped processing

Use a vertical card flow when the question is how one input set passes through a central
process, produces several distinct results, and feeds a verified reuse stage. Keep stage
order visible and label result groups as simultaneous outputs or alternative choices;
an alternative needs its condition and must not imply every choice executes. The results
share a parent stage, not a sequence between neighboring cards. Draw only supported
input/process/result/reuse relationships; omit an unknown downstream connection rather
than implying every output feeds it. Name a subset explicitly when only some outputs are reused.

Prefer semantic HTML cards for short prose and grouped outcomes; use a flowchart when
branch guards, cross-links or edge tracing need explicit geometry. Keep a simple statement
as prose and dense exact comparisons as a table. Do not force this pattern into every
document or replace prototype/checklist interfaces. [HTML output](html-output.md) owns
the opt-in markup, shared styles and responsive checks.

## Bound complexity without shrinking meaning

For criteria or diagnostic findings, prefer a compact icon-led list in one container when
aligned labels and supporting evidence improve scanning. A list is not a flow: do not imply
sequence or causal edges. Keep ordinary prose/list/table when it conveys the same information
more clearly. Icons supplement visible wording; never use them as the only criterion or status.
Use a callout only for a material note, limitation or recommendation, not decoration.

For a diagnostic overview, pair optional KPI label/value groups with populated finding areas.
Derive counts from actual inspected records and define units and overlap: analyzed PRs,
deduplicated candidates and currently solved candidates are different measures. Identify the
time window and observed, illustrative or partially collected data. A finding connects its
area, evidence-backed status, judgment, short basis and next action to the existing citation
contract. Unknown is not solved. Zero findings or missing access needs plain coverage/No change
text, not fabricated metrics or empty cards. Do not mandate three KPIs, six areas, an icon per
paragraph, severity colors or a particular skill's report format.

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

When a source-supported duration, TTL, distance, or validity window measures one fixed span,
label that value on or directly beside the measured span and make its endpoints clear. A
remote legend alone should not require readers to infer which span the value measures.
Distinguish illustrative values from observed or required values; never invent a measurement.
Use a table or chart instead when direct labels would obscure precise comparison or crowd
the drawing. Verify the span and label together at narrow viewports without clipping,
overlap, or horizontal overflow.

For structure changes, keep the same component identities and spatial correspondence in
Before and After wherever practical. Pair the views with a Changes ledger identifying
added, removed, changed, moved and rewired elements as applicable. Preserve unchanged context;
an attribute-only change usually needs a table rather than a topology diagram.

Inspect the actual figures at the required HTML viewports/themes, including the complete
static form of an interactive figure. A clean page-width measurement does not prove all
diagram content is reachable: check clipping and any local scroller. Correct geometry
failures before claiming visual acceptance; report unavailable checks honestly.

## Distillation provenance

Reviewed 2026-10-13 at `nicobailon/visual-explainer@1829e4f61ee804dff3651eb9ffdec4dfb779dbfc`
(MIT): keep only source-supported dimension labels on meaningful spans; adapt to TigerKit's
existing HTML and viewport checks. Omit every-number-as-picture, figure-first prose,
numbered callout infrastructure and renderer-specific markup. Upstream runtime and model
behavior were not rerun in TigerKit.

Reviewed 2026-10-07 at `cathrynlavery/diagram-design@d1376371965f513d99cc9ec388835d255c5c88d5`:
`skills/diagram-design/SKILL.md` and relevant sections of `references/layout-budget.md`,
`references/semantic-patterns.md`, `references/primitives-core.md` and
`references/output-spec.md` under that package. Implementation and
inline rationale were inspected; separate upstream behavior evals and runtime efficacy are
unverified. Keep question-led representation and traceable geometry; adapt semantic selection,
overview/detail and architecture deltas to TigerKit's existing HTML contract. Omit upstream
branding, fonts/palette, onboarding, reference catalog, import/export workflow and renderer.
Original MIT notice is included in each consuming package's `LICENSE.txt`.
