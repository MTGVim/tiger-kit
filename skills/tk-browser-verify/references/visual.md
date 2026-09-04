# Visual evidence

Every approved visual claim requires a non-empty runtime screenshot and actual image
inspection, except when an exact bounded-region candidate file is byte-identical to an
already inspected comparable baseline under the contract below. DOM, accessibility-tree,
network, or computed-style evidence cannot replace the image. Without comparable conditions
or a required capture, return `Unverifiable`.

When a design/screenshot basis exists, reproduce the approved viewport, DPR, browser,
font, assets, and zoom before comparing only the named region/state. Classify a
difference as a `defect`, approved deviation, environment issue, or `unverifiable`.
Do not invent design intent or broaden the work into generic critique.

## Visual intent and baseline pairs

When a candidate can affect rendered output, visual regression coverage is required even
when its stated behavior must remain unchanged. Classify every approved visual region by
where its intended evidence exists:

| Intent | Baseline evidence | After evidence | Outline location |
| --- | --- | --- | --- |
| appear | surrounding context before insertion | new target and context | after only |
| disappear | old target and context | surrounding context after removal | baseline only |
| change | old target and context | new target and context | both corresponding targets |
| remain unchanged | complete comparison region | complete comparison region | none |

The outlined `intended-change` region and the remaining `must-not-change` region are separate
judgment surfaces. An observed difference in `must-not-change` is `Fail` by default. Only an
explicit approved deviation may convert it to acceptance. A behavior-preserving refactor may
consist entirely of `remain unchanged`; the absence of a design node, mockup, or changed visual
AC never disables this branch.

Use a parent-supplied inspected baseline when its provenance and environment are comparable. When
invoked before the first product edit, prove and record the current HEAD plus relevant worktree
fingerprint, capture that exact current tree directly under `baseline/`, and preserve the run ID for
the after call. When invoked after candidate edits without a baseline, identify the exact pre-change
source from the approved change range and repository evidence, safely materialize it in a run-owned
OS temporary tree without modifying the current checkout, commits, refs, or shared Git metadata,
and capture the baseline first. Do not guess the pre-change ref or silently compare against an
unrelated branch. If pre-existing work makes that source ambiguous, the pre-change tree cannot be
run, or comparable conditions cannot be reproduced, record that limitation and do not claim absence
of visual regression.

For a shared component, inventory affected consumers and sample by distinct layout context rather
than prop pattern alone. Include at least one affected consumer for every present parent-sizing
context such as flex item, grid cell, table cell, absolute positioning, or another size-constraining
container. Record uncovered known contexts as limitations; do not generalize a sampled `Pass` to them.

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
AC-to-file/state table, capture order when relevant, source provenance, and a replay procedure.
For each paired capture, record the target URL, ordered navigation/input with stable selectors or
verified element identity, scroll anchor and offset, capture boundary, viewport, DPR, zoom,
completed font-loading state, browser, and UI state. Declare carousel slides, relative-time text,
random ordering, animation, or other intrinsically nondeterministic regions before comparison and
exclude only those exact regions with a reason. Record any capture-only element removal/hiding.
This file is evidence metadata, not a progress ledger.
Return the same explicit AC/file/state mapping and capture order in the verification result.
Do not compress multiple captures into an undifferentiated path list: report one ordered row
per capture with its AC, file, viewport, state/region, and inspected result.
Each result row must state that the screenshot was non-empty after actual image inspection, or that
the candidate bounded-region file was byte-identical to its named already-inspected baseline.
State any capture-only mutation in the index and result, including `none` when no element was
hidden, removed, or annotated.

Replay the same indexed procedure for baseline and after. A matching viewport alone is insufficient
when navigation, scroll, state, font readiness, capture boundary, or deterministic content differs.
Store paired captures under `baseline/` and `after/`. Before replacing a failed after capture,
preserve the complete failing evidence in a new unique immutable `failed-<attempt>/` directory.

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

For a `must-not-change` element or bounded region capture, first compare the exact files byte for
byte only when encoding, capture boundary, and indexed replay conditions match. Byte identity is a
sufficient one-way oracle for visual equality and discharges further axis inspection for that exact
region. Non-identity does not prove a defect; inspect the eight axes below. Do not use byte identity
as the primary oracle for a full viewport or a capture containing declared nondeterministic regions,
animation, or environment-sensitive antialiasing.

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

Record the baseline provenance, replay procedure, viewport, paired screenshot paths, inspected
result, and limitation as concise facts.
A causal regression claim requires comparable baseline runtime evidence; otherwise,
report only the currently observed failure.
