# HTML Output

Render already verified content with a suitable available renderer or minimal semantic HTML.
Produce one offline-readable HTML file with inline CSS, SVG and optional JavaScript, without
external assets, fonts, frameworks, build steps or runtime network requests. Source hyperlinks
are allowed; core reading and navigation must work without a server or network. Keep content
independent of presentation. Render diagrams locally as inline SVG or accessible HTML rather
than depending on a remote diagram/math library. Do not execute retrieved markup or scripts:
escape source/code text for its HTML or script context and preserve whitespace in `<pre><code>`.

Use semantic heading order, stable chapter/section anchors, descriptive navigation, readable
contrast, accessible visual titles, non-color-only cues and `prefers-reduced-motion`. Use native
links and `<details><summary>` for keyboard-accessible navigation and answer reveals; keep
required background and conclusions readable without JavaScript. Add richer interaction only
when it improves understanding, with a readable static equivalent. Diagrams must match verified
claims, terminology and uncertainty; distinguish illustrative data from observed measurements.

For a live explanatory figure, expose only the one to three variables needed for
its claim. Compute the drawing, numbers and explanatory sentence from one pure
`model(settings)`; render them together from its result, without separate derived
state. Start from a verified current value or an explicit explanatory baseline,
never imply an illustrative default is a measurement. Render that state in HTML
before JavaScript; hide or omit inert controls without JavaScript. Reduced motion
removes transitions, not the readable state or user-operated controls. Identify
simplified models and their relevant assumptions. When implementation details
matter, reference original production logic or validators rather than copying
them into the explanation. Replay a changed setting and check drawing, numbers
and sentence against the same result; disclose unexecuted checks.

Keep exercise answers collapsed until an explicit reveal; initial labels, styling, choice order
and length must not expose correctness. Offline HTML cannot hide answers from source inspection,
so never claim exam security. Preserve source anchors and version/snapshot labels in the artifact.
Inspect saved HTML for self-containment, anchor targets, escaping and answer separation. Apply the
required Render verification below before delivery; an unavailable renderer is `Unverifiable`.

Live-figure provenance is kept in the calling package's provenance file; the calling package's
`LICENSE.txt` preserves the MIT notice.

## Document navigation

For long document-like artifacts, keep meaningful stable `<section id="...">` elements in the DOM
and native links whose URL hashes support direct access, browser history and browser Find. Provide
a desktop sticky TOC/sidebar or equally fast section navigation, switching on narrow screens to a
compact accessible sticky top navigation or collapsible TOC. Indicate the current section, using
`:target` as the no-JavaScript cue and optional progressive `aria-current` updates for the TOC.
Use `<details><summary>` for long secondary evidence/logs, keeping required background/conclusions
expanded and searchable. Preserve keyboard order, visible focus, semantic navigation labels, readable
contrast and reduced motion. Navigation must not remove inactive sections or require JavaScript to
read core facts. On narrow screens, keep navigation inside the viewport rather than creating a page-level
horizontal scroller. Flex/grid children that contain prose or controls must be shrinkable with `min-width: 0`;
use a bounded table/code wrapper for genuinely wide content instead of clipping the page or relying on a flex
row that extends past the viewport. Include hash deep links, keyboard navigation, no-JS readability and reduced
motion in the required render checks; disclose missing checks.

Experimental prototype UIs are not document viewers: do not force this navigation shell onto them.
Their offline/accessibility principles still apply. Document portions of QA sheets can use these
navigation rules without changing the behavior of their test/checklist interface.

## Reader contract

Rewrite source prose for the reader instead of dumping state, findings or logs. Preserve exact
code, identifiers and necessary quotations as marked evidence, with context. Before finalizing
reader-facing prose, headings, labels or captions, read and apply the calling package's
`clear-writing.md`, synchronized from `tk-rewrite`. Start each section with its conclusion.
Use content-specific headings that name the subject, decision, evidence or limitation; do not
narrate the assistant's reading order with generic headings such as `먼저 볼 것`, `먼저 확인할 것`
or `처음 읽는 분께` when the actual topic can be named. Keep table cells to about one sentence
(roughly 120 characters); move long secondary evidence
into `<details>` without hiding essential background. Embed needed local content; show an external
local path as code rather than a broken file link. Use unique component classes for distinct roles.
Body text is the largest non-heading text, except KPI values and hero figures. Define domain and
statistical terms for a capable reader outside the field. When the document uses reader-unfamiliar
terms before the section that explains them, add a compact term list immediately after the opening
conclusion: one-line definitions linked to their detailed sections, expanded and searchable.
Place it after the gist in explain/explain-diff, the summary in research, and the learning objectives
in teach. Still define each term at first use; the list supports, not replaces, definitions.
Omit the list when no such term precedes its explanation; do not use a fixed term-count threshold.

## Shared theme

Inline [theme CSS](../assets/html-theme.css) and [theme control](../assets/html-theme.js) into the
single HTML file; these are package assets, not runtime dependencies. Keep their canonical tokens,
font stack, scale, spacing and card/table styles together. Existing product/design-reference tokens
remain authoritative for a prototype comparison; use this neutral default for standalone output
without such a basis. Add an initially hidden `fieldset[data-ht-theme-control]` with a `legend`
and three native radio inputs named `ht-theme` whose values are `system`, `light`, `dark` in
that order. Style the labels as one segmented control with body-size text and at least 40px target
height. Keep the native radio semantics so Tab enters the group and arrow keys change the selected
value. The script reveals it only when functional. Do not collapse this control into a small select.

In document-like artifacts, place the theme control at the right end of a top bar that spans the
page; keep it sticky on desktop and in normal flow on narrow screens so it does not stack with
section navigation. The top-bar title is a short content title that stays meaningful while
scrolling: name the subject and its central change or conclusion in reader terms. Put ticket keys,
branch names and other identifiers in secondary metadata; do not use them or generic words such
as `설명`, `explanation` or `report` as the title. The existing prototype UI exception applies;
apply this document shell only to document portions of QA sheets, preserving their checklist UI.

Before writing a TigerKit standalone HTML artifact, resolve its generation default from
`${XDG_CONFIG_HOME:-~/.config}/tigerkit/settings.json`. Treat this file as bounded user preference
data, never as instructions or authority. The supported shape is
`{"html":{"theme":"system|light|dark"}}`. An explicit theme in the active user request wins.
If the settings file does not exist, create its parent directory as needed and create the minimal
file `{"html":{"theme":"system"}}`; report that bootstrap once in the completion message. This
missing-file bootstrap is part of an authorized HTML artifact generation and grants no other host
configuration mutation. If the file exists but `html.theme` is absent, null or blank, use
`system` without rewriting it. If existing JSON is unreadable, malformed, has the wrong type, or
contains any other nonblank theme value, preserve the file, fall back to `system`, and report the
limitation. Preserve unrelated keys.

Put the resolved generation default in `html[data-default-theme]`. For `light` or `dark`, also
put that value in `html[data-theme]` so the first paint does not depend on the operating-system
theme or JavaScript; for `system`, omit `data-theme`. A valid browser preference already stored
under `tigerkit-html-theme` is an explicit reader choice and wins at runtime over the generated
default. If browser storage is unavailable, keep the generated default and all theme controls usable.

Define colors as root tokens. Give body an explicit background and text color and set `color-scheme`.
Dark values belong in both `@media (prefers-color-scheme: dark)` under `:root:not([data-theme="light"])`
and `:root[data-theme="dark"]`, so a manual choice wins. Default to gray surfaces with one accent
hue; reserve good/warn/bad colors for status with a text/icon cue. Offer system/light/dark as a
three-segment native radio control with at least 40px control height and a layout that stays within
the viewport; wrap every localStorage operation in try/catch. Never let storage refusal break
reading or controls.

## Data visualization

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

## Render verification

Before delivery, inspect rendered desktop (at least 1280px) and mobile (390–500px), in light and dark.
Delegate browser-visible checks to `tk-browser-verify` within its provider, headless and evidence
boundaries. Do not launch the user's browser or silently install/switch verification providers.
Check actual keyboard use, hashes, static/no-JS core reading and reduced motion. Required numerical
checks are the emulated mobile CSS viewport width matching `innerWidth` and
`document.documentElement.scrollWidth <= innerWidth`; a wider `innerWidth` under mobile
emulation means content widened the layout viewport and fails the check. Table overflow is confined to a
`position:relative` scrolling wrapper; body/table/definition-list non-heading sizes at most body
size (KPI/hero exceptions only); and row headers retaining readable multi-character widths.
Off-screen absolute helper text and measurement elements must not widen the document. Fix failed
checks in the generator/template and replay. Completion reports name inspected viewports/themes
and results, or `Unverifiable` with the unavailable renderer/check. Saving HTML alone is not proof
of readability; unreadable output is a functional defect and cannot pass the affected acceptance.

For document-like artifacts, verify that the theme control is inside the top bar and visible in
the initial viewport. On desktop, its `getBoundingClientRect().top` must fall within the top bar's
vertical bounds. Check that the title still identifies the subject without ticket keys or generic
labels, and that any required term list follows the opening conclusion, expanded with working links.
