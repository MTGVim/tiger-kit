# Native App Evidence

Read before capture, evidence write or executed phase return. Apply the [shared verification
contract](verification.md) and [artifact paths](artifact-paths.md). Native evidence is window-
bound rather than URL/DOM-bound. Store run-owned evidence under
`.tigerkit/evidence/tk-app-verify/<run-id>/` with `baseline/`, `after/` and immutable
`failed-<attempt>/` captures when applicable; the required bounded `README.md` is the sole Markdown AC/evidence index,
not a lifecycle ledger.

## Capture and annotations

Use the smallest readable window capture that contains the criterion and necessary context.
Do not capture an unrelated whole desktop by default. Whole-desktop capture needs a criterion
that requires it and verified redaction. Record process/app/build, window ID/title, OS, locale,
role, dimensions, scale, capture origin/method and UI state. Window titles/paths can be sensitive;
redact private values without claiming an omitted label was verified.

Replay baseline and after with matching window size/scale/fonts/state/capture boundary. For every
named region, classify `appear | disappear | change | remain unchanged` and apply the shared
outline table. Preserve the raw screenshot as immutable runtime evidence. On a native surface,
produce a labeled annotated derivative using target bounds from that same capture; record the
raw-to-annotated mapping and coordinate/scale transform. Never redraw UI, erase defects or pass
an annotation as original pixels. If accurate bounds or an annotation tool are unavailable,
return `Unverifiable` for the required visual contract rather than omitting outlines.
Inspect decoded raw and annotated images and confirm every required outline and label is visible.
A missing or clipped annotation is a failed capture: preserve it and recapture, rather than
accepting it with a limitation. Use the selected provider's supported capture/annotation route;
browser DOM mutation is not a native annotation mechanism.
`capture_only_mutation` identifies each outline/label and
redaction. A target beyond the captured window/scroll position is not evidence of its criterion.

Judge intended changes and preserved regions separately. Record all applicable shared visual
axes, reference/candidate/delta for geometry and typography, mismatch evidence and explicit
deviations. Native window sizing replaces browser breakpoints only when that is the approved
criterion. Do not invent computed CSS or a DOM source for a native screenshot. An unavailable
measurement is a stated limitation and blocks the corresponding strict fidelity claim.

## Result fields

An executed result includes:

- `status` per criterion and aggregate;
- `phase: baseline | after | acceptance`, `run_id`, candidate/build identity and replay procedure;
- `provider`, version/host/OS and observed capabilities/input delivery/permission state;
- non-sensitive app/process/window identity and ownership, auth mode, dimensions and scale;
- `visual_contract: applied | n/a` with the shared contract's applicable checks/reason;
- `capture_only_mutation: <description> | none` and redaction facts;
- ordered capture rows: absolute raw/annotated paths, criterion, window/state/region, capture method,
  effective dimensions/scale and actually inspected result, or the direct nonvisual evidence;
- per visual capture, `annotation: visible (pixel-checked) | none (remain unchanged) | none (target absent by intent)`
  for the target outline and `target in frame: yes | no`; absent sides require appear/disappear intent and visible context;
- comparable baseline provenance, per-axis verdicts/measurements and failures when a pair applies;
- `verification_complete`, exact `next_required`, limitations, focus effects and cleanup/residue;
- `automated_regression: protected | N/A | exception | unknown` from the parent/verified disposition.

For baseline/after comparisons, include one compact row per scene:
`scene | baseline observed value | after observed value | verdict`. Read each value from current
app/accessibility/runtime evidence at capture time and confirm visible claims in the image;
never invent a DOM measurement for a native surface. Use the same phase-specific observed-value
text as the capture label, with required redaction. Use `match`, `intended change` or
`pre-existing issue` only when supported; use `regression` or `unverifiable` for an unexpected
change or missing evidence. Preserve actual criterion statuses; a scene description is not a
waiver. Pixel-check labels even when no target outline is required. An out-of-frame target cannot
support its visual criterion; an absent appear/disappear side must show the surrounding context.

Keep full result fields, comparison rows and capture mapping in the evidence `README.md`.
An optional HTML gallery/contact sheet is a derived view, never a replacement for that index
or original-image inspection. Return absolute paths without opening evidence in the user's own
browser or through a desktop opener; open only on explicit user request. Preserve the selected
provider's focus and authorization requirements even for a requested open.

A preflight stop returns only the real status, missing prerequisites and next input; invent no
captures or completion fields. A baseline is capture-only with `baseline_capture: Pass`,
`verification_complete: false`, and `resume_parent: required` for an active parent. An after
result binds the same run/provenance/replay and completes only when every criterion is covered.
For standalone output lead with the exact `Status: <token>` and concise facts/limits/cleanup;
for nested execution return phase-local evidence and resume the owner without a final user reply.

When images materially support publication, use the [producer-neutral publication
manifest](publication-evidence.md), returning required baseline/after pairs for unchanged
regions too. Use a non-sensitive origin-free `display_route` only when the represented surface
actually has one; for native windows record an explicit native-surface omission and keep app/window
identity in ordinary evidence. Never invent a web route, upload evidence, or emit a `Pass`
manifest entry for an unverified/failing criterion.

## Optional video handoff

Only for requested or approved video, collect publication-safe frames with actual timestamps
when the selected native provider supports it. Keep app/window/build identity, scale and capture
origin in the handoff. Pass an owned `mode: evidence` manifest (`frames` with absolute `path` and
`timestamp_ms`, plus `end_ms`) to `tk-video`; do not call another package's script path.
The verifier retains actual capture, input, permissions, test data and resource lifecycle.
Missing Screen Recording permission or unsupported recording omits media without changing an
independently supported app verdict. If that same deficit also blocks required screenshots,
those visual criteria remain unverified. Never replace native capture with browser evidence.
No automatic installation, permission change or publication follows from this request.
