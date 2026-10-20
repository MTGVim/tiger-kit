# Video assembly

Use this package's `scripts/build_movie.py` with already installed ffmpeg and ffprobe. Never
install tools automatically. The safe input/output rules apply independently of package location.

## Inputs and timing

Use an absolute, regular nonsymlink JSON manifest and nonempty PNG/JPEG frames within its owned
run directory. Shared capture input may retain the producing verifier's run directory when that
handoff authorizes the output there. For combined sources, copy approved frame bytes into one
video run and preserve their original paths/hashes in the handoff. Do not recapture a mutating flow.

An observed capture keeps the existing schema and actual elapsed time:

```json
{"mode":"evidence","frames":[{"path":"/absolute/run/frame-0.png","timestamp_ms":0},{"path":"/absolute/run/frame-1.png","timestamp_ms":100}],"end_ms":1000,"captions":[{"start_ms":0,"end_ms":1000,"text":"Observed result"}]}
```

A stills explanation uses explicit holds; absent narration/hold defaults to 3000ms:

```json
{"mode":"explainer","frames":[{"path":"/absolute/run/diagram.png","source_kind":"rendered","caption":"The request enters the queue","hold_ms":3000},{"path":"/absolute/run/actual-state.png","source_kind":"capture","caption":"Observed result","hold_ms":4000}]}
```

For observed per-scene narration, add `scenes: [{"start_ms": 0, "audio_path": "/absolute/run/scene.wav"}]`
to the `evidence` manifest. Starts must be strictly increasing actual scene boundaries inside
`end_ms`; measured clips must fit before the next scene/end. Initial gaps and silent scenes are
preserved. Do not assign scene audio to individual evidence frames. Narration-paced recapture
belongs to the capture owner and is limited to authorized non-mutating scenarios.

For per-scene audio in `explainer`, add `audio_path` to that frame. The helper measures its
actual duration and defaults the hold to `max(3000ms, audio duration + 250ms)`, pads each scene
to its hold and joins the clips in order. Explicit holds shorter than their audio are rejected.
`narration_requested: true` retains a failed media result for missing or silent selected narration;
use false only when narration was not selected or a caption-only fallback was accepted.
Do not combine scene audio with the separate full-track `--audio` input. Never guess duration
from character count. Bind audio only to accepted current scene text and ensure
captions cover it. No narration failure authorizes invented observed waiting time. `evidence`
returns `timing: observed`; `explainer` returns `timing: presentation`. Neither is a timing assertion.

Run `python3 <loaded-package>/scripts/build_movie.py --manifest <json> --output <owned.mp4-or.gif>`.
Optional `--audio <wav>` accepts a separately prepared track. The assembler has no engine import. `--ffmpeg <path>` overrides `TIGERKIT_FFMPEG` and
automatic discovery. It checks PATH first and, when subtitles are missing and no override was
selected, an installed Homebrew `ffmpeg-full` keg via `brew --prefix ffmpeg-full`. It never installs
a package or changes PATH. Receipts report `ffmpeg_path` and `ffprobe_path`.
A mismatched or too-long optional track is omitted with a warning; retain any selected-but-missing
narration limitation. Retain original sources independently of output and screenshot manifests.

## Quality and recovery

The helper checks actual codec, duration and full decode, and reports media quality separately
from the legacy `verification_status: not-assessed` application field. It cannot judge factual
content or prove that a person heard the narration. Inspect the contact sheet and actual frames.
Repeated-frame warnings concern `evidence`; holding stills in `explainer` is intentional.

For hard captions, preflight the actual `subtitles` filter and use its named `filename` option.
Without the filter, exit 2 returns `media_status: blocked`, prerequisite
`ffmpeg-subtitles-filter`, a matching SRT and decodable movie. MP4 also includes a soft subtitle
track; GIF has only its sidecar. Those are recoverable outputs, not burned-caption success.
Present the `tk-wizard` installation-guidance question with the exact missing capability before
returning a blocked result or considering a workaround. Do not implement frame-composited captions. Inspect existing
package/PATH conflicts before proposing a platform-specific package such as ffmpeg-full.

For UI recordings (`evidence`), hard captions use an appended black lower band (`pad`) and fixed
libass `force_style` (Korean-capable font, size, margin and alignment), preserving the original UI
area. Inspect decoded frames for glyph support, wrapping and band overflow; shorten/split captions
if needed. Rendered explainer cards retain their authored layout.

Encoding failure returns exit 1 and bounded redacted diagnostics, preserving inputs and prior
outputs. Ready output returns exit 0. Never overwrite an unrelated file or lose an oversized GIF:
5MiB is a target with a visible warning. A prebuilt inspected GIF uploads through `tk-pr-media`
as an image; extension-side `--gif` assembly requires separately selected publication.
