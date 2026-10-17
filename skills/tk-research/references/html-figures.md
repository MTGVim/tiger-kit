# Figure Authoring

Read only for a chart, SVG, card flow, diagnostic summary or related visual component. Plain prose
and semantic tables do not require this reference. The shared shell remains owned by the existing
template and theme assets; these rules apply to content figures.

## Data visualization

When numeric data or an evidence-backed relationship graph benefits from a visual, read
[chart design](chart-design.md) and inspect the matching section of the standalone
[chart examples](../assets/chart-examples.html). Adapt one relevant example and its scoped
styles/interaction, not the whole gallery. Keep the final HTML self-contained; do not require
the installed package, a CDN, or a chart runtime to remain available to its reader.

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

## Render-safe authoring

Apply these rules before the first render check so common layout defects are prevented instead of
discovered one by one.

For compact criteria/finding groups, use a semantic list with `role="list"` and the opt-in
`.ht-info-list` styles inside one `.ht-card` container. Each `.ht-info-row` contains a
decorative `.ht-info-icon` (`aria-hidden="true"`, inline SVG or text) and one shrinkable
content block. Keep the item number/label, status meaning, judgment, basis and action as
visible text in DOM reading order. Use ordered lists or explicit ASCII numbering only when
order matters. Icons and CSS removal must not remove meaning. Use a short heading and body
in `.ht-callout` for an actual note/limitation; a static callout is not a live `alert`.

For a diagnostic summary, use `.ht-kpis` on a `<dl>`, with one `<div><dt>Label and unit</dt>
<dd>Verified value</dd></div>` per supported metric. Auto-wrap on narrow screens. Define the
source window/data nature visibly and calculate each value from the same records that feed
the finding list; never fill absent data with zero. Keep status text `.ht-status` optional,
with an explicit meaning and evidence. Reuse normal numbered citations beside the relevant
judgment. Separate rows with spacing/dividers rather than mandatory independent cards or
large badges; do not alter checklist/prototype interaction UI.

Verify four criteria, mixed-language multiline labels, long links and status text at desktop
and mobile in all themes. Check heading/list/definition-list semantics and accessible text,
keyboard links, reduced motion, no-JS and icon/CSS removal. For report fixtures, mark example
data explicitly; compare KPI totals/statuses against source records, and exercise empty and
partial data plus a prose/table negative case. A DOM accessibility check is not a claim that
every screen reader was executed.

For a card flow selected under the document skill's visual grammar, use a labeled
`<figure>` with an ordered `.ht-flow` list. Each list item is one stage; group its
outputs in an unordered `.ht-flow-results` list of `.ht-card` elements. Keep DOM
order equal to reading order; use real headings and explicit relationship text in
`.ht-flow-link`. A decorative arrow is `aria-hidden`; it does not supply a missing
relationship. `.ht-flow-focus` can emphasize the central process with the accent
token. All classes are opt-in and reuse the common theme, without a renderer or JS.

Adapt this minimal structure, naming every input, result and supported relationship:

```html
<figure aria-labelledby="flow-title">
  <figcaption id="flow-title">Input, processing and simultaneous results</figcaption>
  <ol class="ht-flow">
    <li><div class="ht-card"><h3>Input set</h3><p>Verified input scope.</p></div>
      <p class="ht-flow-link"><span aria-hidden="true">↓</span> Inputs enter processing.</p></li>
    <li><div class="ht-card ht-flow-focus"><h3>Central process</h3><p>What changes.</p></div>
      <p class="ht-flow-link"><span aria-hidden="true">↓</span> Produces both results.</p></li>
    <li><h3>Simultaneous results</h3><ul class="ht-flow-results">
      <li class="ht-card"><h4>Result A</h4><p>Its distinct purpose.</p></li>
      <li class="ht-card"><h4>Result B</h4><p>Its distinct purpose.</p></li>
    </ul><p class="ht-flow-link"><span aria-hidden="true">↓</span> Both results support reuse.</p></li>
    <li class="ht-card"><h3>Reuse</h3><p>The supported downstream use.</p></li>
  </ol>
</figure>
```

Use two output columns on desktop and one below 600px; one output spans the group
without an empty slot. Let cards grow with their text, use shrinkable tracks and
wrap long Korean/English labels. Do not use fixed card heights, positional arrows
between columns or color alone to distinguish stages/choices. Verify 1, 2 and 4
results, long labels, simultaneous/alternative wording, DOM order, no-JS reading,
keyboard targets and light/dark/system/reduced-motion at the required viewports.
Check card text and relationship labels for overlap/clipping as well as page width.

- Grid or flex tracks that can contain `pre`, tables, long code, or unbounded prose use
  `minmax(0, 1fr)` and the child uses `min-width: 0`; do not use page-level clipping or
  `overflow-x: hidden` to hide an overflow defect.
- Size inline SVG for the narrowest required viewport. The smallest readable label must remain at
  least 11 CSS px after scaling (`font-size * rendered-width / viewBox-width`). If a before/after
  or multi-panel figure cannot meet that threshold, use one SVG per panel and stack panels on narrow
  screens instead of shrinking the text.
- Short identifiers in table cells, such as commit SHAs, IDs, and status tokens, stay on one line.
  Use `.ht-token` or an equivalent local rule for them. Long paths and URLs may wrap or use their
  own bounded horizontal scroller.
- Text using `white-space: nowrap` in a header or toolbar must have a proven bounded width or
  switch back to wrapping at the mobile breakpoint. A shared utility class must not accidentally
  force a longer environment label or title to stay on one line.
- Programmatic scrolling performed only to position a verification capture uses instant behavior.
  Smooth scrolling must not leave the intended target outside the captured viewport.

