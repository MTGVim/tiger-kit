# Visual evidence

Every approved visual claim requires a non-empty runtime screenshot and actual image
inspection. DOM, accessibility-tree, network, or computed-style evidence cannot replace
the image. Without comparable conditions or a required capture, return `Unverifiable`.

When a design/screenshot basis exists, reproduce the approved viewport, DPR, browser,
font, assets, and zoom before comparing only the named region/state. Classify a
difference as a `defect`, approved deviation, environment issue, or `unverifiable`.
Do not invent design intent or broaden the work into generic critique.

## Capture method and evidence map

Prefer the smallest readable evidence that proves the AC while retaining enough surrounding
layout context. Default to a normal viewport screenshot containing the criterion and its
necessary context. If the criterion is below the fold, scroll to it and capture that viewport.
When one AC requires separated regions or states, use multiple ordered viewport captures and
map every file to its AC, region/state, and order. Do not default to a context-destroying
element-only crop or reuse undifferentiated captures for unrelated criteria.

Use `fullPage` only as an explicit exception when the AC itself requires page-wide composition
or long-page continuity and bounded viewport captures cannot prove it. Do not resize the
viewport height to the document height. When applying the exception, label the capture method
`fullPage` and state why bounded captures cannot prove the AC in both the evidence index and
verification result. Store a bounded `README.md` beside the images with an
AC-to-file/state table, capture order when relevant, viewport provenance, and any capture-only
element removal/hiding. This file is evidence metadata, not a progress ledger.
Return the same explicit AC/file/state mapping and capture order in the verification result.
Do not compress multiple captures into an undifferentiated path list: report one ordered row
per capture with its AC, file, viewport, state/region, and inspected result.
Each result row must state that the screenshot was non-empty after actual image inspection.
State any capture-only mutation in the index and result, including `none` when no element was
hidden, removed, or annotated.

Before capture, inspect whether an empty off-screen alert, toast, or similar framework
container expands or contaminates the image. Remove only a verified empty, non-criterion
container at runtime and disclose it in the evidence index. For annotations, attach an
`outline` directly to the target element. Place the label as an absolute child of `body`
and clamp its position to the page width so target `overflow: hidden` cannot clip it.
Do not calculate a detached overlay from coordinates that may change during scrolling,
`fullPage` layout, or capture.

If fixed navigation obscures the criterion, first use the framework's compact/collapsed
mode and verify that the content position remains unchanged. If it still obscures the
criterion, hide only that navigation for capture and disclose the change in `README.md`.

## Verbatim visual comparison axes

For a verbatim/fidelity comparison against an approved reference, actually inspect
reference and candidate screenshots under the same viewport, DPR, zoom, and completed
font-loading state. Record each axis as `Pass | Fail | Unverifiable`. Do not replace an
axis with a general visual impression or DOM presence. If any required axis remains
unchecked, the aggregate result is not `Pass`.

1. **Asset presence/integrity**: Verify that logos, SVGs, icons, favicons, raster images,
   and background images are not missing, substituted, or duplicated. For SVGs, inspect
   the rendered shape, `viewBox`, aspect ratio, fill/stroke, and clipping through the
   screenshot and computed evidence rather than checking only element presence.
2. **Content**: Verify that visible text, labels, numbers, badges, and order match the
   `reference` without omissions, additions, or typos. The basis must contain the exact
   visible string. If it paraphrases an element name or contains only a `code identifier`
   or `enum` value, do not guess the element; record `Unverifiable`.
3. **Geometry/layout**: Compare position, dimensions, spacing, alignment, radius,
   borders, overlap, clipping, wrapping, and crop for each named region.
4. **Typography**: Compare loaded font family/fallback, weight, rendered font size,
   line-height, letter-spacing, text transform, and wrapping.
5. **Color/paint**: Compare computed values and rendered appearance for foreground,
   background, border, SVG `fill`/`stroke`, opacity, shadow, and gradient.
6. **Imagery**: Verify successful image request/load, source, intrinsic dimensions,
   aspect ratio, `object-fit`/`object-position`, crop, and resolution.
7. **Responsive**: Recheck the preceding axes for each approved viewport and breakpoint
   edge, including overflow, wrapping, clipping, and off-screen controls.
8. **State**: Recheck the preceding axes for each approved
   hover/focus/active/disabled/loading/error state.

For geometry and typography, record the reference value, candidate measurement, and
delta for every named element whose value can be measured. Report every measured
mismatch regardless of magnitude; when tolerance is absent, do not silently accept it.
If the repository has an appropriate design token but the candidate uses a different
token or computed value, record a `Color/paint` mismatch even when the colors look close.
Only an explicit approved deviation can convert a measured mismatch into acceptance.

For every finding, connect the axis, named element/region, reference observation,
candidate observation, viewport/state, and inspected screenshot path. When the approved
criteria do not define pixel-perfect tolerance, do not invent a threshold. Report clear
mismatches and leave subtle differences as `Unverifiable`.

For a responsive AC, measure the actual `window.innerWidth` and test the named width and
breakpoint edge. Inspect overflow, clipping, overlap, wrapping, truncation, alignment,
spacing, sticky/fixed elements, and off-screen controls only when approved criteria
require them. Measure hover/focus after trusted input.

A temporary runtime-only DOM/response mock is allowed only when repository evidence
proves the exact production envelope and the approved criterion concerns presentation
rather than the mocked backend. Label and remove the bypass. Never modify source code
for verification.

Record the viewport, screenshot path, inspected result, and limitation as concise facts.
A causal regression claim requires comparable baseline runtime evidence; otherwise,
report only the currently observed failure.
