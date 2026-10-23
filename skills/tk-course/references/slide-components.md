# Slide component data

Read for the selected representation before writing `course.json`. All components are offline,
escaped SVG using theme tokens. Keep common slide fields, narration and objectives from
[authoring](authoring.md). Data figures use one conclusion in the title and a source/limitation
line; read [chart design](chart-design.md). No external chart runtime is loaded.

Each cue's `focus` lists rendered semantic target keys. Every data element must be covered by at
least one cue. An empty opening focus shows the entire slide; later cues can isolate details.
Unrevealed groups stay dim, including their labels, values and containing boxes. All/show and
highlight-only settings preserve the complete figure. Focus does not invent data or playback times.

## Numeric figures

All three types require `visual.unit`, `x_label`, `y_label`, `source` and numeric `visual.data`.
Values must be JSON numbers, finite and within +/-1e12; strings, booleans and unknowns fail.
Split missing or incomparable samples into separate views with explicit limitations. Exact original
values and units also appear in an accessible data table in lesson notes and the no-JS fallback.
Native SVG titles supplement visible labels; no essential value depends on hovering. Compact value labels may round long numbers; native titles and tables retain the original numeric precision.

| Type | Data and options | Cue keys |
| --- | --- | --- |
| `bar` | 1-6 `{label,value}` rows; `orientation`: `vertical` (default) or `horizontal`. Shared scale includes zero, including negative and all-zero data. | `bar-1` onward |
| `line` | 1-2 `{label,points:[{x,y},...]}` series, each with 2-8 points and the same strictly increasing numeric x values; also require `x_unit`. Actual x spacing is preserved; no curve smoothing. Use the second, dashed square-marker series for a stated reference. | `point-1` onward, numbered across series; `series-1` onward covers all its points |
| `stacked` | 1-6 nonnegative `{label,value}` rows with a positive total; all share the same denominator and unit. Exact value and computed percentage labels sit outside segments so small pieces remain readable. | `segment-1` onward |

Example worker timings and an explicitly modeled reference (not additional measurements):

```json
{"type":"line","visual":{
  "unit":"s","x_unit":"workers","x_label":"Workers","y_label":"Elapsed time",
  "source":"Three-run measurement; reference = 63.2 / workers, excluding overhead",
  "data":[
    {"label":"Measured","points":[{"x":1,"y":63.2},{"x":2,"y":34.0},{"x":4,"y":18.8},{"x":12,"y":13.4}]},
    {"label":"Ideal reference","points":[{"x":1,"y":63.2},{"x":2,"y":31.6},{"x":4,"y":15.8},{"x":12,"y":5.2666666667}]}
  ]}}
```

Focus `point-1` through `point-4` for the measured cases, then `series-2` for the whole reference;
alternatively cover all eight individual points. Reference assumptions belong in the source line.
Values below a line chart are aligned by x row, with series labels above their columns; direct
point labels are not crowded onto neighboring marks. The complete table retains source precision.

```json
{"type":"stacked","visual":{"unit":"s","x_label":"Run","y_label":"Stage time",
 "source":"Illustrative stage breakdown; same run, no excluded stage",
 "data":[{"label":"Transform","value":12},{"label":"Setup","value":8},{"label":"Tests","value":20}]}}
```

## Output, code and events

`output` uses `visual.data` as an array of original strings and requires `visual.source`.
This text component has no artificial numeric axis or unit requirement. `code` retains top-level
`code` (array of strings) and `visual.footnote`. Both show line numbers and accept 1-12 original
lines, each at most 100 weighted columns, with at most 20 soft-wrapped portrait rows. Blank lines,
indentation and escaped markup are preserved; no ellipses, hidden overflow or internal scroller.
Split at meaningful boundaries when either layout exceeds the budget. Narrow SVG soft wraps are
visual only; the original text remains available verbatim in lesson notes.

```json
{"type":"output","visual":{"source":"Vitest run, supplied terminal capture",
 "data":[" Test Files  4 passed (4)","      Tests  20 passed (20)","   Duration  1.21s (transform 300ms, setup 90ms, tests 110ms)"]}}
```

Use `line-1` onward for each nonblank original line, plus `takeaway` for a code footnote.
Legacy six-line code retains its original character allowance (up to 30 portrait rows for wide text). Legacy code aliases remain: line 1 `request-id`, 2 `await`, 3/4/6 `compare`, 5 `render`;
covering an alias covers the actual lines to which it maps. Lines 7-12 use their numbered keys.

`timeline` accepts `visual.lanes` (1-4 label strings) and `visual.events` (1-8
`{lane:0,label:"..."}` objects). Lane indexes are zero-based; event array order is displayed
top to bottom, not an invented duration scale. Use `event-1` onward and optional `callout` for
`visual.callout`. The original two-lane/four-string form retains its original lane mapping and
`request-a`, `request-b`, `response-b`, `response-a`, `overwrite` aliases.

`hook` accepts 1-2 `visual.title_lines`, 1-4 `visual.cards` with `label` and `value`, plus
`visual.question`. Values accept up to 32 weighted columns instead of three characters.
Use `card-1` onward; `first-search` and `latest-search` alias the first two complete cards.
Choose numeric charts for a measured relationship rather than expanding a list of number cards.

## Lesson plot figures

| Type | Visual fields | Cue keys |
| --- | --- | --- |
| `cover` | `number` (1-200), `question`; common slide title is the lesson title. | `title`, `question` |
| `course-map` | `lessons` (1-8 titles in this map), `current` (one-based current item). Split a longer itinerary into labeled parts. | `lesson-1` onward |
| `summary` | `items` (2-3 `{question,answer}` pairs). Add slide-level `role:"summary"` if it closes the lesson. | `answer-1` onward |

A map labels prior entries as previously covered and the current entry explicitly. These are
authored positions, separate from learner completion controls; never mark mastery from the map.
Greeting, connection and goals can share these figures; do not force every lesson to start with
the same cover. A final map may use `role:"closing"` with next-lesson preview narration.

## Bounds and verification

Text budgets are weighted columns (wide CJK and MWmw characters count two, tabs four); title, narration
and common metadata retain the existing course limits. Components validate their specific slots
and reject oversized data before output. Inspect both wide and purpose-built portrait layouts,
light/dark themes, captions on, first cue and each focus state. Captions for these figures sit
below the figure so they cannot cover axes or output lines. The 390px check includes label
bounding boxes, exact value reconciliation, complete original output and document width.

## Observed screens and spatial examples

Use `type:"image"` for a verified local PNG/JPEG/WebP teaching figure. `visual` requires
`src` (source-relative nonsymlink file), `alt`, `description`, `source` and `rights` (the verified
redistribution scope). Image authoring requires Pillow; detect readiness and report a missing
dependency before production rather than installing implicitly. The builder checks actual encoding and embeds pixels offline. It derives
aspect ratio from the image, preserving annotations in wide and portrait layouts. Catalog cards
use the description as a text preview to retain the small public-manifest budget; choose another
preview slide when its diagram better distinguishes the course.

Optional `regions` contains up to six `{id,label,x,y,width,height}` boxes, with stable ASCII IDs
and normalized coordinates inside the actual image (0-1, positive width/height). Crop/annotate
only inspected evidence; coordinates are author-verified, never inferred from uninspected pixels.
Cue key `image` covers the whole figure, and `region-<id>` covers each numbered box and its
legend. Every target needs a cue. Description, source and rights remain visible; focus follows
the existing cue/theme/reduced-motion behavior. Keep the decisive relation legible at the target
viewport; an image's mere presence does not establish teaching sufficiency.

For spatial alternatives use the same coordinates and initial conditions, or label the changed
condition. Distinguish visibility, occlusion, traversable boundaries and consumed resources; do
not give the learner an observer's hidden information. Connect before/after through stable
entities and show intermediate steps only when they expose a cause. Compare the actual rendered
figure and caption; preserve backward/reset and static explanation. Do not invent measured
travel time, distance or success rates, and do not require animation or MP4 when staged SVG or
static comparison already teaches the judgment.
