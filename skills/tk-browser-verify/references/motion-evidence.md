# Optional capture for video

Read only when the current request, accepted runtime-plan summary or approved repository opt-in
selects a GIF/MP4 supplement. Use current instructions first, then approved
`.tigerkit/repository.json` over `tigerkit.config.json`: optional `evidenceMedia` has
`enabled: boolean`, `format: auto | gif | mp4`, `narration: boolean` (default false).
Reject malformed values; absence means disabled. Preferences grant no installs or publication.

Keep screenshots, assertions, timing checks and publication manifests independent from media.
Capture approved publication-safe states on the selected headless provider in the verification
run only when its supported API permits sharing. Do not switch providers, install recorders or
rerun a mutating scenario for a movie. Unsupported capture omits only media. Preserve actual
monotonic timestamps, a fixed viewport, criterion/head provenance and a truthful final end time.
No nearby screencast frame replaces the independent assertion screenshot; brief loading states
and debounce claims still require direct runtime assertions.

Write an ordered capture manifest in the owned evidence run: `mode: evidence`, `frames` with
absolute PNG/JPEG `path` and `timestamp_ms` starting at zero, and `end_ms` after the last frame.
Include approved captions and capture identity in the handoff. Pass it to `tk-video` for selected
assembly, narration and finished-media inspection, without importing its script path. A missing
video skill or failed movie never changes the application verdict or required screenshots.
Return the explicit movie limitation and keep the manifest for resumption.

`tk-video` returns optional supplements separately from required screenshot manifests, including
media type, path, timing, source/criterion IDs, warnings, inspection limits and publication choice.
A generated movie is not selected for upload by default. `tk-pr-media` owns publication.
After accepted media decodes and inspection completes, delete only known owned transient frames
that are not assertion/failure evidence. Encoding failure preserves inputs and prior valid outputs.
This verifier owns capture/server cleanup on every exit and never deletes unrelated resources.
