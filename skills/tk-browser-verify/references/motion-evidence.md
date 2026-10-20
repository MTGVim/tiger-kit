# Optional motion evidence

Read only for an explicitly requested or opted-in GIF/MP4 supplement. Screenshots and direct
assertions keep their existing acceptance and publication contracts. Optional-media failure never
changes a criterion verdict; report media separately as ready, omitted, failed or unverified.

Use current instructions first, then approved `.tigerkit/repository.json` over `tigerkit.config.json`.
The optional `evidenceMedia` object has `enabled: boolean`, `format: "auto" | "gif" | "mp4"`,
and `narration: boolean` (default false). Reject malformed values; absence means disabled.
These preferences authorize no installs, remote publication or extra test-data mutations.
Prep may suggest media in its existing runtime-plan approval summary, never a separate routine question.
Suggest GIF for a short flow around ten seconds; MP4 for longer demonstrations or explanation.
Duration is guidance, not an automatic verdict or mandatory cutoff.

## Capture and privacy

Capture only the approved, publication-safe scenario on the selected headless provider. Share frames
with the verification run only when its supported API permits it; do not switch providers, install
recorders or rerun a mutating scenario merely to produce media. Preserve monotonic actual capture
timestamps. Keep assertion screenshots independently captured at the inspected state; a nearby
screencast frame cannot replace one. No stream, fps or contact sheet proves a brief loading state
or precise debounce duration. Preserve DOM/runtime assertions and timing evidence for those claims.
Do not persist auth entry, secrets or unredacted intermediate states. Unsupported capture omits only media.

Store frames and outputs in the run-owned evidence directory. For movie assembly use a JSON file:

```json
{"frames": [{"path": "/absolute/run/frame-000.png", "timestamp_ms": 0}, {"path": "/absolute/run/frame-001.png", "timestamp_ms": 100}], "end_ms": 1000, "captions": [{"start_ms": 0, "end_ms": 1000, "text": "Observed result"}]}
```

Use actual timestamps, a fixed capture viewport, zero-padded filenames and a truthful end time.
The optional `scripts/build_movie.py` assembles a local GIF or MP4 at 10fps without compressing elapsed time;
it needs already-installed ffmpeg/ffprobe. It installs nothing. Run it with `--manifest <json>
--output <run-owned.mp4-or.gif>`; `--audio <wav>` accepts independently prepared audio. Audio that is invalid
or longer than the movie is omitted with a warning, leaving the captioned movie. No engine import
or download belongs to this assembler. If tools are absent, inspect supported alternatives and
follow prerequisite recovery; do not silently substitute a different requested deliverable.
When captions are requested, the assembler checks the installed subtitles filter. Without it,
it returns `media_status: blocked`, `prerequisite: ffmpeg-subtitles-filter` and exit 2 while
preserving a decodable video and matching SRT sidecar (plus a soft subtitle track for MP4).
Do not report burned captions or a finished captioned GIF. Route any user-only installation
step through `tk-wizard`; inspect package conflicts and PATH rather than assuming an OS recipe.
Encoding errors include bounded redacted diagnostics; inputs and unrelated outputs stay intact.

## GIF

For generation without publication, build a local GIF with the same assembler and inspect it before returning the optional artifact. ffmpeg is needed only for this local assembly route; if unavailable, omit media or follow prerequisite recovery. No upload is authorized.

Upload an already-built inspected GIF as an image through `tk-pr-media`, without reassembling it. If publication itself is explicitly selected and the reviewed extension is available, its upload-time assembly is also eligible: pass approved PNG/JPEG frames to `tk-pr-media` with uniform playback delay derived from their
timestamps, the proposed GIF name ending in `.gif`, and all capture/sampling limitations.
Use `gh attach --gif --delay <milliseconds> --name <name.gif>` only under its reviewed-extension
and publication contract. At 10fps the delay is 100ms, not the extension's default 80ms.
For irregular timestamps, first prepare a uniform presentation sequence without claiming precise
timing. Frame capping shortens playback in the pinned extension: disclose the source frame count,
retained count and altered timing. GIF is a flow illustration, never a latency measurement.
The 5MiB ceiling is a target: oversized output may still be uploaded. Surface every cap/reduction/
oversize warning and actual size. Use non-JSON stdout plus separately captured stderr at v0.7.0;
never lose warnings through `--json`. Do not upgrade to an unreviewed main/release for this feature.

## Inspection, publication and cleanup

Inspect the retained assertion screenshots plus a contact sheet or representative decoded frames.
Check captions against observed actions and the actual initial/final state. Decode the entire movie
with an installed media tool, check duration/dimensions and confirm any selected audio is present.
Report uninspected intervals and sampling; do not imply a complete visual inspection from a contact sheet.
Return optional supplements separately from required image manifests, with `media_type`, absolute path,
criterion IDs, duration, capture head, viewport, captions/observations, warnings, inspection limits
and `publication_selected: true | false`. Generation opt-in is not upload permission. Do not create
an `evidence_required: true` video in place of a required screenshot or visual-preservation pair.

After outputs decode and inspection is complete, delete only literal known run-owned transient
frames not retained as assertion/failure evidence. Preserve a valid output and the original failure
evidence on encoding failure; never delete unrelated input files or claim unverified cleanup.
Release owned capture/server resources on every exit through the existing lifecycle contract.

## Optional narration module

When narration is explicitly selected, read [narration](narration.md). Removing that module and
this pointer leaves GIF, captions, MP4 assembly and verification unchanged.
