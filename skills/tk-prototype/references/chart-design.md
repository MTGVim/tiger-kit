# Chart design and interaction

Read only when the artifact needs a numeric chart or an inspectable relationship graph.
Use [chart examples](../assets/chart-examples.html) as working, offline recipes: bar, line,
area, scatter and a small directed relationship graph. The example data is synthetic.
Reuse a relevant figure, scoped CSS and progressive enhancement, not the full gallery or its
sample conclusions. This is a design reference, not a general chart framework or extraction tool.

## Select and prepare

Name the question, unit, population/time window, source and comparability limits first.
Keep unknown values unknown; never convert missing data to zero, interpolate it silently,
or remove incomplete records without disclosure. Preserve source precision in the value table
and tooltip; rounding for axis ticks must not change the plotted position.

| Reader's question | Form | Contract |
| --- | --- | --- |
| Which category is larger? | Bar / horizontal bar | Include zero; use horizontal bars for long labels. |
| How does a value change over time? | Line | Scale actual elapsed time; show gaps for missing samples. |
| How does a nonnegative volume evolve? | Area | Fill to zero only when magnitude matters; no decorative fill. |
| How do two numeric variables relate? | Scatter | Label both units; correlation does not prove causation. |
| How did two endpoints change? | Dumbbell / slope | Shared unit and scale; label both endpoints. |
| Which cells differ across two categories? | Heatmap | Stable color scale, numeric cells/table, missing-value key. |
| How do signed contributions produce a total? | Waterfall | Reconcile start + contributions = end; preserve signs. |
| How is a whole composed? | Stacked bar / donut | Same denominator; disclose exclusions; prefer bars for close values. |
| Which entities are related, and why? | Directed graph | Verified edges, relationship labels and source/evidence details. |

Only the first four numeric forms and a small graph have bundled runnable recipes. Other forms
require custom implementation and their own validation; do not imply the gallery implements them.
Use prose for a single fact and a table for dense exact comparisons. Never discard records simply
to fit a preset; split views or use a table.

Choose form before color: one number uses a stat tile; observed-versus-baseline uses one emphasis
color and gray baseline; more than seven categories uses a table. Use a fixed categorical order
without cycling colors, one hue for sequential values, and two hues with a gray midpoint for
diverging values. Status colors identify status only. Use one axis; split different units into
small multiples. Use text tokens for labels, not series colors. Two or more series need a legend;
up to four also need direct labels. Every chart includes a value-table alternative, a hover tooltip
(at least SVG `<title>`) and non-color cues. Add one sentence explaining how to read each chart,
including units and the comparison's meaning. Check contrast and color-vision-deficiency distinction;
use an appropriately licensed tool or independently authored check, never copy a proprietary bundle.
Do not invent charts, measurements or a passing palette check when the content/evidence lacks them.

## Compose a polished figure

Use one clear title, a short reading sentence and a source/limitation line outside the plot.
Allocate room for the longest labels before drawing marks. Keep a coherent title/body/axis
type hierarchy, spacious plot margins, subtle gridlines and few ticks. Use the document's
semantic theme tokens and a stable series order. Put emphasis on the comparison that matters;
do not give every mark a different color. Modest rounded bar ends and low-opacity gradients
are optional polish; they must not move endpoints or obscure a zero/negative value.

Keep labels in text colors, not low-contrast series tints. Distinguish multiple series with
solid/dashed strokes or marker shapes as well as color, with a visible legend and direct labels.
Use system fonts. Do not import the upstream's brand palette, required fonts, maximum node
counts, no-shadow rule or mandatory style onboarding. A restrained tooltip shadow is appropriate.

Calculate every coordinate from the data and a shared finite scale. Include zero for bars
and area; signed bars extend from the same zero line. Provide a finite fallback domain for
all-zero/constant data. Do not smooth sampled lines into invented extrema or force irregular
dates to equal spacing. Split unlike units rather than adding a deceptive second value axis.
Changing series visibility must not silently rescale the axes or change denominators.

## Make interaction useful

Author complete static SVG/HTML, captions and a semantic value table first. Embed scoped CSS
and JavaScript into the delivered file; never leave empty plots or inert controls without JS.
The gallery is standalone and deliberately contains its own small theme shell. In an existing
document, use its theme control instead of adding a second global control. Prefix all figure,
gradient, tooltip, description and table IDs when reusing a recipe more than once.

Enhance only after listeners attach. A tooltip must show the item/series, exact value and unit
on pointer hover, keyboard focus and touch activation. Keep it within the viewport, dismiss
it with Escape, outside activation and scroll/resize, and never make it the sole source of
essential data. Insert data as textContent or escaped text/attributes, never raw HTML.
Give marks native titles and accessible names; keep the complete table available without JS.

Use native buttons with visible focus and aria-pressed for legend toggles; remove hidden series
from focus order and restore them when shown. Show an explicit empty-selection state when
all series are hidden. Do not add decorative filters, fake zoom/export buttons or animation.
Add zoom/reset only when the actual data density needs it and verify range/state restoration.
Honor reduced motion and retain a meaningful static state throughout any transition.

For a relationship graph, keep node identities and edge directions stable. Let selection reveal
adjacent relationships and their evidence in a persistent detail area; include a clear reset.
Distinguish observed, inferred and unknown edges in wording and line style. Do not manufacture
connections, confidence scores or clusters. Large graphs need a justified search/filter path
and an accessible relationship list; the small static recipe is not a large-graph layout engine.

## Verify the adapted result

Check the real browser at desktop and narrow mobile widths in light and dark themes, with
JavaScript both enabled and disabled. Inspect actual screenshots, not DOM existence alone.
At narrow widths reflow long labels or keep a labeled, keyboard-accessible local plot scroller;
do not shrink a fixed viewBox until labels become unreadable or overflow the whole document.

Reconcile every mark and tooltip with the same source row. Check minimum/maximum, zero,
negative/constant values where supported, missing samples, long labels and duplicate figure IDs.
Test hover, Tab/Enter/Space/Escape, touch activation, legend off/on, all-hidden state, reset,
tooltip boundaries, and absence of external requests. Verify glyph/line contrast and non-color
cues; do not claim full accessibility compliance from this limited inspection.
The screenshot supplied by a user may guide visual treatment without supplying measurements:
do not invent its unreadable values or claim pixel-exact fidelity unless actually compared.

## Sources and adaptation

Reviewed 2026-10-13:

- `cathrynlavery/diagram-design@0a8ea20ae69b33a5edce6018eedd3a9d26e90c1c`, MIT:
  `skills/diagram-design/SKILL.md`, `references/type-bar.md`, `type-line.md`,
  `type-scatter.md` and their example assets. Adapt question-led type selection, shared scales,
  explicit endpoints, layout hierarchy and honest missing-data treatment. Keep the existing
  Cathryn Lavery MIT notice in the package. Omit branded skins, fixed pixel/node quotas,
  external fonts and mandatory style setup. The bundled gallery is independently authored.
- `Graphify-Labs/graphify@a9860f70dc3cc2e9c2d8cb923484cfa0592b9067`, Apache-2.0:
  `graphify/skill.md` and `graphify/exporters/html.py`. Reference only: inspected the product's
  node selection, neighbor detail and evidence distinctions. No upstream code, prose, palettes,
  dependencies or assets are distributed. Implement the generic interaction independently;
  omit extraction, persistent graphs, watchers, GraphRAG, service/provider setup and CDN runtime.

These source inspections establish design provenance, not upstream runtime certification.
