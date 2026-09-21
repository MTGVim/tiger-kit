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

Keep exercise answers collapsed until an explicit reveal; initial labels, styling, choice order
and length must not expose correctness. Offline HTML cannot hide answers from source inspection,
so never claim exam security. Preserve source anchors and version/snapshot labels in the artifact.
Inspect saved HTML for self-containment, anchor targets, escaping and answer separation. When a
local renderer is available, inspect the rendered result and keyboard interactions without
starting a server or launching the user's browser; disclose any unperformed rendering or checks.
