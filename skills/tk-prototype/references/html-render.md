# Document Render Checks

When browser verification is required, inspect desktop (at least 1280px) and mobile (390–500px), in light and dark.
Delegate browser-visible checks to `tk-browser-verify` within its provider, headless and evidence
boundaries. Do not launch the user's browser or silently install/switch verification providers.
Check actual keyboard use, hashes, static/no-JS core reading and reduced motion. Required numerical
checks include desktop content left/right margin differences of at most 1 CSS px and no
intersection between the footer and `.ht-doc-nav` rectangles at widths above 960px. Check header actions stay at the right padding edge with long export-status text at 1280px,
900px and below 760px. Required numerical checks also include the emulated mobile CSS viewport width matching `innerWidth` and
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
vertical bounds. Inspect the title and control together at the affected desktop breakpoint:
both must have positive rendered width, stay inside the header and not overlap. Page-level overflow
checks alone cannot establish this. Check text for replacement characters or suspicious runs of
question marks against its source; warn and inspect rather than banning or replacing normal question
sentences and code operators. Check that the title still identifies the subject without ticket keys or generic
labels, and that any required term list follows the opening conclusion, expanded with working links.
