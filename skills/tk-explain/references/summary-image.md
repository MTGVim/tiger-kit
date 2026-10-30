# Summary image for PRs and issues

Produce one compact static PNG when the requested infographic/summary is destined for a
PR body or issue. Reuse the pinned evidence and audience; do not first build a long page or
ask the user to choose PNG versus an artifact link. An explicit page request wins.

Choose a bounded canvas (typically 1200 wide, 500-800 high), a conclusion-led title, two to
four groups of the essential measurements or relationships, and readable labels. Keep units,
baselines, denominator, measured versus illustrative status, and material limitations next to
claims. Preserve conditions that change the conclusion; reduce scope rather than shrink text
or crop away qualifications. Do not invent measurements to complete a layout.

Author a static self-contained SVG or HTML in the run's temporary directory. SVG follows
[scene figures](scene-figures.md)'s inert asset restrictions; use explicit dimensions and
`scripts/svg_to_png.mjs`. For bounded HTML use
`node scripts/capture_page.mjs input.html new-output.png [width] [height]`, for example
`node scripts/capture_page.mjs input.html new-output.png 1200 580`. Height is optional:
without it the viewport fits the document, including documents shorter than 900px; explicit
height fixes the viewport while capture still includes the whole document. Give a height for
viewport-dependent layouts that cannot converge. Constrain the document to the intended
canvas and check the actual PNG dimensions. These
image paths do not require archify, its author-check HTML or its finalize command.

Inspect the final decoded PNG for clipping, readable text at PR display size, contrast and
agreement with the pinned numbers, units, labels and relationships. Perform the clear-writing
and reader-formatting checks on authored text. Apply step 4's independent accuracy review
policy, including the default review for change explanations, to the final PNG and its evidence.
Bind all checks/rechecks to final bytes. Missing Chrome or unavailable required review is
Blocked/Unverifiable, never a successful image or a silent HTML substitution.

Deliver the PNG with a concise description suitable for alt text and actual verification.
Keep source/evidence in the run directories; create no extra explanation page by default.
Creation does not upload an attachment or open a PR. Pass the verified local image and
its evidence to the authorized `tk-pr-open`/`tk-pr-media` owner; respect its manifest contract
when requested, without claiming that an infographic substitutes for required runtime evidence.
