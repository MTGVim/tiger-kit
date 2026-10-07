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
Inspect saved HTML for self-containment, anchor targets, escaping and answer separation. When a
local renderer is available, inspect the rendered result and keyboard interactions without
starting a server or launching the user's browser; disclose any unperformed rendering or checks.

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
read core facts. Verify desktop/mobile layout, hash deep links, keyboard navigation, no-JS readability
and reduced-motion behavior when a renderer is available; disclose missing checks.

Experimental prototype UIs are not document viewers: do not force this navigation shell onto them.
Their offline/accessibility principles still apply. Document portions of QA sheets can use these
navigation rules without changing the behavior of their test/checklist interface.
