# Visual evidence

Every approved visual claim needs a non-empty runtime screenshot plus actual
image inspection. DOM, accessibility-tree, network, or computed-style evidence
cannot replace the image. Missing comparable conditions or required capture is
`Unverifiable`.

For a design/screenshot basis, reproduce the approved viewport, DPR, browser,
font, assets, and zoom, then compare only the named regions/states. Classify a
difference as `defect`, approved deviation, environment, or unverifiable; never
invent design intent or broaden into generic critique.

For responsive AC, measure actual `window.innerWidth` and test named widths and
breakpoint edges. Inspect overflow, clipping, overlap, wrapping, truncation,
alignment, spacing, sticky/fixed elements, and off-screen controls only where the
approved criteria require them. Measure hover/focus after trusted input.

Temporary runtime-only DOM/response mocks are allowed only when repository
evidence proves their exact production envelope and the approved criterion is
about presentation rather than the mocked backend. Label the bypass and remove
it. Never edit source for verification.

Record viewport, screenshot path, inspected result, and any limitation as compact
facts. A causal regression claim requires comparable baseline runtime evidence;
otherwise report only the observed current failure.
