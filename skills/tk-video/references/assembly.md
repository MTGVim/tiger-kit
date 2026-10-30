# Video assembly

- [Inputs and timing](#inputs-and-timing)
- [Continuous rendered video](#continuous-rendered-video)
- [Optional captions, callouts and zoom](#optional-captions-callouts-and-zoom)
- [Quality and recovery](#quality-and-recovery)

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

MP4 uses optional positive numeric `source_fps` from actual capture metadata, capped at 30fps.
Without it, estimate the cadence from the median adjacent frame-timestamp interval (excluding
the final hold); report `fps_source: timestamps` and the event-driven/idle-capture uncertainty.
Fewer than three frames cannot establish cadence and fall back to 10fps with a warning. GIF and
`explainer` default to 10fps; a still's hold is not a capture-rate measurement.
`--fps <number>` explicitly selects a positive output rate up to 30 for either format without
changing source timestamps, scene holds or audio offsets. The result distinguishes measured
encoded `fps`, `selected_fps`, `fps_source` and `encoded_duration_ms` from the manifest's duration.
Fractional rates remain fractional. Encoding quantizes the final endpoint to a frame interval;
retain duration/decode checks with tolerance of at most the greater of 150ms and one frame.
The private generated concat list uses a microsecond image time base so 25fps image defaults
cannot discard sub-40ms capture intervals before the selected-rate filter runs.

A stills explanation uses explicit holds. Without a hold, use the greatest of 3000ms,
125ms per caption character and measured narration plus 800ms. This reading-time heuristic
needs audience inspection; an explicit selected hold still wins:

```json
{"mode":"explainer","frames":[{"path":"/absolute/run/diagram.png","source_kind":"rendered","source_in_picture":true,"caption":"The request enters the queue","hold_ms":3000},{"path":"/absolute/run/actual-state.png","source_kind":"capture","caption":"Observed result","hold_ms":4000}]}
```

For rendered cards, `source_in_picture: true` declares an inspected source tag already present
in the image and suppresses the caption prefix. The declaration never marks the frame as capture.
Without it, `source_label` supplies a nonempty label in the audience's language; the Korean default
is `렌더링 장면`. Empty narration captions still fail the subtitle coverage check even when
source provenance appears in the image, unless the user explicitly selected `caption_style: none`.
With captions disabled, keep the source tag inside every rendered card.

For observed per-scene narration, add `scenes: [{"start_ms": 0, "audio_path": "/absolute/run/scene.wav"}]`
to the `evidence` manifest. Starts must be strictly increasing actual scene boundaries inside
`end_ms`; measured clips must fit before the next scene/end. Initial gaps and silent scenes are
preserved. Do not assign scene audio to individual evidence frames. Narration-paced recapture
belongs to the capture owner and is limited to authorized non-mutating scenarios.

For per-scene audio in `explainer`, add `audio_path` to that frame. The helper measures its
actual duration and defaults the hold using the reading/narration rule above, pads each scene
to its hold and joins the clips in order. Explicit holds shorter than their audio are rejected.
`narration_requested: true` retains a failed media result for missing or silent selected narration;
use false only when narration was not selected or a caption-only fallback was accepted.
Do not combine scene audio with the separate full-track `--audio` input. Never guess duration
from character count. Bind audio only to accepted current scene text and ensure
captions cover it when enabled. No narration failure authorizes invented observed waiting time. `evidence`
returns `timing: observed`; `explainer` returns `timing: presentation`. Neither is a timing assertion.

Keep frames, scene WAVs and output inside the manifest directory; output must be a new path.
Run `python3 <loaded-package>/scripts/build_movie.py --manifest <json> --output <owned.mp4-or.gif>`.
Optional `--audio <wav>` accepts a separately prepared track. The assembler has no engine import. `--ffmpeg <path>` overrides `TIGERKIT_FFMPEG` and
automatic discovery. It checks PATH first and, when subtitles are missing and no override was
selected, an installed Homebrew `ffmpeg-full` keg via `brew --prefix ffmpeg-full`. It never installs
a package or changes PATH. Receipts report `ffmpeg_path` and `ffprobe_path`.
A mismatched or too-long optional track is omitted with a warning; retain any selected-but-missing
narration limitation. Retain original sources independently of output and screenshot manifests.

## Continuous rendered video

After the selected [Manim route](manim.md), use a regular MP4 inside this run instead of
extracting PNG frames. This route consumes one complete constant-frame-rate render; compose
multiple beats there. Mixed frame/video manifests and authored `end_ms` are rejected. Variable
or ambiguous rates need an explicitly selected conversion, not guessing. This is rendered
animation, never observed application timing.

```json
{"mode":"animation","video_path":"/absolute/run/render.mp4","caption_delivery":"soft","captions":[{"start_ms":0,"end_ms":2000,"text":"Version 2 and DOM"}]}
```

Default MP4 FPS comes from the stream, including fractional rates and rates above 30. Preserve
duration/resolution; H.264/yuv420p pads odd dimensions to even pixels and reports it. Explicit
`--fps` conversion and GIF's 10fps/audio omission are reported too. Video re-encodes at selected
CRF: this is not byte-identical/lossless output. Receipts separate `source_video`, actual output
geometry/rate/duration and rendered timing.

Embedded audio uses stream copy, retaining channels rather than silently downmixing/replacing
it. Additional `scenes` narration or `--audio` conflicts and fails; select one audio source.
Without embedded audio, reuse measured scene offsets or a full track. Too-long/unavailable
animation audio fails rather than being silently omitted. Silent selected narration and short
subtitle coverage remain failures. No TTS engine is imported.

Resolve `caption_delivery: none | soft | hard` in the existing media-choice round. Animation
defaults enabled captions to `soft`; frame routes retain their hard-caption default.
`caption_style: none` or delivery `none` disables tracks/sidecars, not narration guards. Do not
combine enabled delivery with style `none`. Animation captions are ordered, nonoverlapping and
inside measured duration. Screen text keeps notation, not TTS spelling.

Soft MP4 has an unforced `mov_text` track and SRT/WebVTT sidecars, needs no libass and does not
burn text into pixels. Deliver selected sidecars with the movie. Muxers/players can mark a track
default; report measured `subtitle_default`, not promised initial hiding. Browsers generally
need a same-origin WebVTT `<track>`, not only embedded MP4 text. Verify cue loading and actual
on/off controls in the selected player. Use an owned local HTTP origin when file-origin rules
block WebVTT; otherwise report that player unsupported and retain separate files. No universal
player UI is added. Explicit hard delivery uses selected style and the existing libass/fallback
contract; missing support stays blocked. Differing sidecars, movies and contact sheets are
never overwritten.

## Optional captions, callouts and zoom

Resolve these fields before production through [media choices](media-preferences.md), including
saved values and the first-round save offer. Use them only for the selected presentation treatment. Defaults retain the existing
`band` captions and untransformed frames. A single evaluator's variant preferences support that
creator's choice, not a universal default or evidence of improved learning.

```json
{
  "caption_style": "overlay-rounded",
  "callouts": [{"start_ms": 1000, "end_ms": 4000, "x": 620, "y": 340, "text": "Revenue, margin and orders", "size": 24}],
  "highlights": [{"start_ms": 1000, "end_ms": 4000, "rects": [{"x": 120, "y": 320, "w": 420, "h": 120}], "zoom": true, "margin": 32, "max_scale": 2}]
}
```

All coordinates are pixels in equal-sized original capture frames, before even padding, zoom or
caption band. Convert the recorder's viewport `cue_targets` using its actual screenshot scale,
crop origin and frame dimensions; retain that mapping and capture-only provenance. Reuse observed
beat times and refresh coordinates after scroll/layout changes. Split intervals when geometry
changes; a stale rectangle cannot protect a moving target. `rects` describe already captured
highlights; assembly does not invent UI state or draw disappearance badges. Include any required
in-picture source tag in the protected rectangles or retain a source label in the captions.

- `caption_style`: `none` (explicit user choice: no hard/soft captions, band or SRT),
  `band` (default), `overlay` (square 50% black libass box) or
  `overlay-rounded` (50% black ASS vector box and white text). Overlays preserve source height
  except existing even padding. Default text size is 5% of that height; `--caption-size` still
  applies. Boxes sit 6% above the bottom. SRT sidecars remain unchanged by styling.
  With `none`, keep `narration_requested: true` for selected narration; only subtitle coverage
  is skipped. Missing/silent audio still fails. The receipt returns `subtitles: none`,
  `subtitles_reason: user-disabled`, `captions_path: null` and no sidecar. Caption-only reading time is excluded from default holds; measured audio plus
  breathing room and explicit holds still apply. Authored caption text
  may remain in the source but is not rendered. Callouts remain separately selected and still
  need libass; captions-off does not disable selected callouts or their checks.
- `callouts`: original-frame top-left `x/y`, plain `text`, observed interval and optional nominal
  `size` (default 2.5% of source height, minimum 12px). Render a white card with a thin border,
  left accent, dark text and light shadow. Actual libass glyph bounds determine wrapping and
  padding; no extra imaging library is needed. Overlarge cards, missing glyphs, overlapping
  cards or a card covering an active target fail with an authoring correction.
- `highlights`: ordered, nonoverlapping intervals; combine simultaneous groups in one `rects`
  list. `zoom` defaults to true; false protects targets from captions without enlargement.
  Union every rectangle and every callout that overlaps the interval, add `margin` (default
  32px, at least 2px internally for integer cropping), fit the output aspect ratio and clamp
  to the source. Scale is capped by the region fit and `max_scale` (default 2, allowed 1-10).
  Fixed-size `zoompan` uses input frame number/output fps, with 500ms smoothstep at each end;
  intervals shorter than one second use half their duration per transition. No source timing
  is stretched. Integer cropping can still cause slight motion jitter. RGB cropping with bounded, upward-rounded
  origins retains borders flush with the source edge before final 4:2:0 encoding.

The filter order is fps/even padding, callouts, fixed-canvas zoom, optional band, then captions;
cards scale with the UI while captions keep their size. Variable-size `scale` followed by `crop`
can reinitialize filters and reset their time/frame counters; do not use it for animated zoom.

For each overlay caption, test protected target/card geometry across its full interval and zoom
transitions, using effective ASS centisecond boundaries (reported alongside requested times).
If the lower box intersects it, use the upper position and record
`caption moved to top to keep highlights visible: <time>`. If both positions collide, fail and
use `band` or recapture with a clear safe region. Read the returned `presentation` geometry and
inspect decoded frames: a geometry check cannot prove cue facts, glyph readability or aesthetics.
Check each callout's middle frame and each zoom's transition/middle frames; compare actual box
padding (caption left/right difference at most 30% of text size, card top/bottom at most 20%).
Keep the original capture frames for alternate styling. Missing libass blocks required text
effects and dependent zooms; it never authorizes installing dependencies or claiming completion.

## Quality and recovery

MP4 uses `libx264`, `yuv420p` and explicit CRF 18. `--crf <integer>` selects 0-51 for MP4 only;
lower values retain more detail at potentially larger size. GIF rejects an explicit `--crf`.
For equal-sized source frames, retain their dimensions with only even-dimension padding and the
default evidence caption band (selected overlay styles omit it); avoid resolution changes during authoring or capture. The receipt reports `encoder`, requested `crf`, encoded `width`/`height`
and `pixel_format`. CRF is an encoder setting, not a measured visual-quality score or lossless claim;
4:2:0 color conversion can soften fine colored text even at CRF 0. Inspect the actual cut.

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

For UI recordings (`evidence`), default hard captions use an appended black lower band (`pad`), preserving
the complete UI. Default nominal text size is 5% of final output height; `--caption-size <px>`
overrides it (positive, at most half the source height). The band holds two text heights, with
a 48px minimum; the helper converts size and centered vertical margin into libass's 288-unit
SRT coordinate system. Receipts expose nominal `caption_size_px` and `caption_band_px`;
actual glyph bounds depend on the installed font. Soft captions remain player-styled.
Inspect decoded frames for glyph support, wrapping and band overflow; shorten/split captions
if needed. Rendered explainer cards retain their authored layout.

Encoding failure returns exit 1 and bounded redacted diagnostics, preserving inputs and prior
outputs. Ready output returns exit 0. Never overwrite an unrelated file or lose an oversized GIF:
5MiB is a target with a visible warning. A prebuilt inspected GIF uploads through `tk-pr-media`
as an image; extension-side `--gif` assembly requires separately selected publication.
