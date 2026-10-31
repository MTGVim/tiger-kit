# Reader Presentation

Apply these navigation and geometry rules only to shared-reader document portions selected by
the owning workflow. Explanation/research pages follow their renderer contract, not this legacy
shell; neither selected archify nor independently authored technique HTML inherits this builder.

## Document navigation

For long document-like artifacts, preserve meaningful stable `<section id="...">` elements and
native hash links for deep access, browser history and Find. Put the hierarchical table of contents
in a fixed left rail on desktop, with a separate lower-right top/bottom control. On narrow screens,
collapse the table of contents into a native disclosure at the lower left; keep the top/bottom
control at the lower right. A document with at most three section elements may omit both
navigators only when they add no value. A document with four or more sections includes both
navigators; never omit only one. Use the
shared `.ht-document`, `.ht-doc-content`, `.ht-doc-nav`, `.ht-doc-toc` and `.ht-doc-controls`
styles in the theme assets. The left rail and mobile disclosure must work without JavaScript.
Use the target heading's full text in each TOC link. Shorten an overlong heading itself,
or put a short label above the full heading in a `<small>` line inside the same link.
For selected shared-reader documents, use [document assembly](html-assembly.md) to insert `tk-writing`'s
[document shell](../assets/document-shell.html); specialized interfaces retain their generators.

Place the footer directly under `.ht-document`, after `main`; shared CSS centers it.
Separate source/version and date into paragraphs when present.

Inline the existing theme script after the markup for optional current-section marking,
Escape/outside dismissal, focus return and focus transfer to native anchor targets. Do not
intercept hash navigation or replace browser history. Native anchors remain usable without JS;
expose `aria-current="location"` with a non-color-only cue when JS is available. TOC and top/bottom
navigation must not leave a persistent outline around the destination section or heading,
including after programmatic focus transfer. Keep the shared static-target suppression and
arrival cue: JavaScript highlights the destination immediately, waits for scrolling to
settle plus about one second, then fades it. Repeated clicks restart it; another click cancels it.
Section links mark only the heading. Reduced motion removes the fade. Without JavaScript,
CSS `:target` briefly marks headings, but cannot replay the same hash or detect scroll completion. Custom static wrappers need the same narrowly scoped treatment. Never disable outlines globally: preserve
visible keyboard focus on links, buttons, inputs and other interactive controls. Keep the popup
within viewport and safe-area bounds at desktop/mobile widths and preserve keyboard order.
Smooth anchor scrolling is the default; reduced motion uses immediate scrolling. Set the
`--ht-anchor-offset` to the actual sticky header height plus breathing room, and verify targets
remain visible. Verification-only positioning uses instant scrolling. Required background and
conclusions stay expanded, readable and searchable; only secondary evidence may collapse.
Keep flex/grid children shrinkable with `min-width: 0`; wrap wide tables in `.ht-table-scroll`
and use `.ht-code` for wide code, never page-level clipping. Builder preflight warns about
undefined `ht-*` classes; fix typos and use document-specific names for additive components. Give the page canvas and `.ht-doc-content` visibly distinct
surface colors in light and dark themes; keep the content surface readable when cards or section
surfaces are nested inside it. Verify TOC open/close, all links, top/bottom, hash reload/back,
keyboard, no-JS, reduced motion and unobscured control/target geometry.
Keep the native disclosure open in the HTML so the left rail remains available without JavaScript;
the theme script may collapse it by default on narrow screens.

For selected shared-reader portions, including document portions of QA sheets, use the shared document shell as a
component contract, not a visual suggestion. Build the header
with `.ht-topbar` and `.ht-topbar-title`; put the theme fieldset inside it with
`.ht-theme-control`, `.ht-theme-label`, `.ht-theme-buttons` and `.ht-theme-option` around the native
radio inputs. Keep the document body, content, navigation, disclosure and controls on their shared
`.ht-document`, `.ht-doc-content`, `.ht-doc-nav`, `.ht-doc-toc` and `.ht-doc-controls` classes.
Reuse the shared theme CSS and script unchanged. Do not replace or override their shell geometry,
surface or control rules with page-level selectors, duplicate `.ht-doc-content` layout rules,
one-off theme tokens, or substitute class names. Add document-specific styles and scripts only as an additive, scoped layer; leave shell layout
and controls to the shared rules. If a default needs overriding or removal, report a shared-shell
defect rather than patching it per document. Rebuild and rerun class, anchor and external-request
checks after postprocessing. For a density/interaction example, assemble the optional
[reader example](../assets/reader-example.html) through the same builder; it is a content fragment,
not another shell or a mandatory section template. During user-led revisions, retain the
request count in the active conversation as an observational cost signal, not a quality verdict
or a new persistent ledger. The theme control's `data-ht-theme-control`
attribute alone is insufficient because it enables the script but does not apply the shared styling.

A document uses one continuous presentation. Prose and semantic tables are valid without a named
technique. Consult only a relevant [technique entry](explanation-techniques.md) for a requested
or unfamiliar format. Avoid duplicate
versions in modes or hidden tabs. Honor an explicit technique preference when it fits the content.


Separate document sections with 1px token-colored rules rather than nested section cards. Avoid
decorative thick borders; visible keyboard focus outlines are the exception. Keep the shared document
content panel as the only enclosing surface unless a specific figure needs a card.

