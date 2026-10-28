# Optional capture for video

Read when a demo capture is requested or the current request, accepted runtime-plan summary or
approved opt-in selects a GIF/MP4 supplement. Resolve `evidenceMedia` per field in this order:
current explicit request, `.tigerkit/repository.json`, user
`${XDG_CONFIG_HOME:-~/.config}/tigerkit/settings.json`, team `tigerkit.config.json`, then defaults.
Missing upper fields retain lower values. Optional keys are `enabled: boolean`,
`format: auto | gif | mp4`, `narration: boolean`, `voice: serena | sohee`.
Defaults are `enabled: false`, `format: auto`, `narration: false`, `voice: sohee`.
Reject a malformed `evidenceMedia` object and use these safe defaults for the run; disclose the
invalid setting and preserve its file rather than silently enabling media through a lower layer.
Pass the resolved voice to `tk-video` only when narration is selected. Preferences grant no installs
or publication, and a missing movie never blocks verification.

## Media-only phase

Use `phase: media-capture` for `tk-video` demo or explanation captures without an acceptance basis,
including a video-only joint invocation without a QA sheet, ticket criteria or Seed. Resolve the
target and bounded scenario from the request/current change; resolve only material unknown choices
with the user. Do not manufacture a QA inventory or pass self-authored acceptance criteria.
Explicit acceptance verification uses the existing inventory and visual contract instead.

Retain headless/provider selection, authentication, safe inputs, approved data-mutation scope,
server readiness, capture redaction and owned-resource cleanup. Follow environment, behavior,
safety and session-lifecycle references when their branches apply. Capture actual states without
acceptance outlines or assertion substitutions. Stop immediately when a required element/state
cannot be found; retain partial captures and the concrete limitation rather than recording guesses.
Record scene-boundary times and final DOM/runtime values separately from the movie.

For selected human-facing input displays, read [tutorial overlays](tutorial-overlays.md) and
inject this package's removable helper only for capture. Treat it as `capture_only_mutation`;
remove it before any independent acceptance screenshot.

Return only `phase: media-capture`, the capture manifest/provenance, observed final-state facts,
limitations and actual cleanup/residue facts. An incomplete run retains its missing-capture reason
and next required input. Do not emit `Status: Pass/Fail`, criterion verdicts, `visual_contract` or
`verification_complete`; the capture is not an acceptance result. Return to `tk-video` for assembly.

## Capture and handoff

Keep screenshots, assertions, timing checks and publication manifests independent from media.
Capture approved publication-safe states on the selected headless provider in the verification
run only when its supported API permits sharing. Do not switch providers, install recorders or
rerun a mutating scenario for a movie. Unsupported capture omits only media. Preserve actual
monotonic timestamps, a fixed viewport, criterion/head provenance and a truthful final end time.
No nearby screencast frame replaces the independent assertion screenshot; brief loading states
and debounce claims still require direct runtime assertions.

On the already selected CDP-capable provider, use `Page.startScreencast` (PNG/JPEG), consume
`Page.screencastFrame`, and acknowledge every event using `Page.screencastFrameAck` with its
`sessionId`. Stop the screencast on every exit. Verify supported protocol parameters rather than
installing another recorder or switching providers. Preserve actual monotonic event timestamps;
prefer PNG for text-heavy UI at the accepted viewport resolution and avoid extra lossy conversions.
Use a reduced capture size only when selected; preserve any existing JPEG source as supplied.
Normalize the first frame to zero and record the real capture end. A stable screen may send no
new frames: hold its last frame until the next timestamp/end instead of fabricating frame times.
The API has no crop-region option; apply approved post-capture crops, recording each scene's
region and source provenance. Before a full-view-to-crop transition, highlight the next region
in the full view. Normalize differing crops to one canvas without distorting aspect ratio.
Do not replace this with repeated `Page.captureScreenshot` calls for
movie frames or add Puppeteer just for `page.screencast()`. Other selected providers may use their
existing supported capture API; unsupported capture remains a media limitation.

For narration-paced recapture, accept measured per-scene minimum holds only for an authorized
non-mutating scenario. Record the new actual scene starts/end and diagnostic final values.
Do not rerun a mutating flow, slow existing evidence or claim deliberate waits measure latency.

Write an ordered capture manifest in the owned evidence run: `mode: evidence`, `frames` with
absolute PNG/JPEG `path` and `timestamp_ms` starting at zero, and `end_ms` after the last frame.
Sort by the original event time before conversion to milliseconds; after rounding, collapse
same-millisecond frames deterministically (retain the last observed state), verify strictly
increasing timestamps and preserve the actual end after the final frame. Do not fabricate time
or mask a clock discontinuity; report it and stop if ordering cannot be established.
Include approved captions and capture identity in the handoff. Include `source_fps` only when
the provider exposes a real capture-rate value; do not invent
one from idle gaps or a requested output rate. Otherwise retain frame timestamps for estimation.
Pass it to `tk-video` for selected assembly, narration and finished-media inspection,
without importing its script path. A missing
video skill or failed movie never changes the application verdict or required screenshots.
Return the explicit movie limitation and keep the manifest for resumption.

`tk-video` returns optional supplements separately from required screenshot manifests, including
media type, path, timing, source/criterion IDs, warnings, inspection limits and publication choice.
A generated movie is not selected for upload by default. `tk-pr-media` owns publication.
Keep reusable frames, audio and manifests until the user explicitly confirms the selected result;
report retained frame bytes while selection is pending. Only after that confirmation and successful
decode/inspection, delete known owned transient frames that are not assertion/failure evidence.
Encoding failure preserves inputs and prior valid outputs.
This verifier owns capture/server cleanup on every exit and never deletes unrelated resources.
