# Explicit standalone animated SVG

Read only for an explicitly requested single looping SVG explanation. The explanation owner,
source investigation, clear writing and independent content review remain `tk-explain`; no new
skill, player, daemon or browser startup is needed. Static diagrams remain static by default.
Use HTML for reader-controlled interactions or a document, `tk-explain` change mode for a change, and
`tk-video` for requested audio/video. Never infer an animated-SVG request from a generic diagram.

Choose one mechanism whose event order, wait or propagation needs motion. Establish the actual
actors, initial state, events and causal dependencies from source evidence; label hypothetical
timing as illustrative. Keep the nodes, directed connectors and complete ordered event captions
understandable without motion. A packet is emphasis, not the only source of meaning. Preserve a
readable static frame for reduced-motion and image-only readers. Do not turn a loop into a claim
that the production system repeats or completes at the illustrative speed.

Use the existing artifact-path/durable-root checks and choice. An explicit `.svg` target wins.
Otherwise obtain the explanation directory from `scripts/durable_artifacts.py resolve`; select a
new `<topic-slug>.svg` there with a numeric suffix on collision, without creating a dummy HTML.
Recheck the final SVG path and parent under the same safety/ignore rules; the returned HTML
filename is only a location hint for this branch. Keep the small editable scene JSON beside the
SVG when useful, or in run-owned scratch when only the SVG was requested. Do not overwrite either
file without authority, commit, publish, auto-open a browser or install a renderer.

## Scene and shared clock

The optional stdlib-only `scripts/build_animated_svg.py` compiles one scene. Its exact JSON keys:

- `title`, `description`: grounded text for the visible title and accessible whole-story description.
- `width`, `height`, `loop`: numeric canvas dimensions and a common loop duration in seconds.
- `nodes`: objects with `id`, `label`, `x`, `y`, `width`, `height`.
- `edges`: objects with `id`, `from`, `to`, `points`; points are orthogonal `[x,y]` coordinates
  touching their named node boundaries. Route around unrelated nodes and text.
- `events`: objects with `id`, `edge`, `label`, `travel` and exactly one of `at` or `after`.
  `after` names an earlier event; optional non-negative `gap` is added after its arrival.

Use concise real names, one shared clock and a rest gap. The helper limits scenes to 9 nodes,
12 edges and 8 events; split larger mechanisms instead of shrinking labels. Its visible static
sequence includes actor names, event labels and start/arrival times. Repeated traversal of an
edge may show retry/backoff; explicitly simultaneous `at` values may show fan-out. Node geometry,
event text and edge crossings remain author decisions, not an automatic layout-quality proof.

Generate with `python3 <package>/scripts/build_animated_svg.py --spec <scene.json> --output <new.svg>`.
Validate the saved output with the same command plus `--check`. The checker compares the exact
deterministic SVG to the validated scene; it is not a sanitizer for arbitrary edited SVG. Revise
the JSON and regenerate to a new approved target. IDs/numbers are constrained and text is escaped;
the emitted file has one style block, CSS keyframes, accessible title/description, static captions
and a reduced-motion rule that hides packets. It contains no script, SMIL, external font/image,
foreign object or network reference. The Python helper is needed for authoring, never playback.

## Verify and deliver

Check the saved XML, complete keyframes and schedule, causal order, rest gap, self-containment and
static frame. Inspect Korean labels, named endpoints, arrow directions, unrelated crossings and
caption fit. The helper's conservative text-space guards cannot establish actual font metrics or
visual clarity. Run the existing independent content review on the exact SVG and scene, including
the static sequence and motion logic, before delivery; keep missing review evidence `Unverifiable`.

Browser rendering/playback checks run only when explicitly requested. For this branch's initial
capability validation, verify browser playback, reduced motion and SVG-in-image embedding when a
local renderer is available. A static rasterizer cannot prove animation; XML/keyframe success
cannot prove GitHub's image proxy or sanitization behavior. Preserve failed evidence and distinguish
executed browser/GitHub checks from unavailable ones. Do not promise that all Markdown hosts,
mobile apps, email clients or social services retain SVG animation. Do not publish a fixture just
to test GitHub without publication authority. Offer `tk-video` only for an accepted video need.

Return the standalone SVG link, optional editable scene and concise actual verification limits.
Do not silently wrap the requested SVG in HTML or assert playback from static checks alone.
