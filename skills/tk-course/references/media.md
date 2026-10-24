# Course Media

Resolve the creator's choice before generating: local TTS, supplied audio or no narration.
Obtain current `tk-tts` options/readiness, including missing dependencies, device, model download,
cache, language/voice, cost and whether text leaves the machine. List supported uninstalled
options as requiring setup; module discovery alone is not readiness. Reuse an explicit parent
choice, not a stored voice preference as implicit narration consent. Request installation/download
approval only when missing; generation does not approve global installation or paid services.

For selected local narration, invoke `tk-tts` through supported skill loading/handoff and retain
actual normalized WAV paths, measured durations and pending pronunciation review. Keep authored caption
spelling separate from pronunciation-corrected speech. Each slide/cue has a stable semantic ID.
An opening cue previews the point; later cues refer to visible entities and explain why they
change. Every progressively revealed element must have a cue. Future elements are hidden,
prior context remains, backwards seeking reconstructs state, and reduced motion keeps manual
access and readable content. Do not claim pedagogical improvement from animation alone.

Slides use actual audio ended events, not guessed speech duration. A fresh lesson shows its first
slide paused. Only explicit Play starts the initial wait; opening from home, curriculum, next
lesson, resume or deep-link never calls the transport to play, even muted or when the previous
lesson was playing. Acknowledge Play immediately in its button/icon and a layout-free live region,
then start narration
after a 5000ms lead-in. At a slide boundary keep the completed slide/index/cue for 1800ms, show
the new slide for 1200ms, then narrate: 3000ms total between slides. These are adjustable product
defaults, not measured universal optima. Same-slide cues wait 600ms; the final cue ends without
an extra transition. Manual selection shows its requested slide immediately and uses only the
next-slide lead-in; seek/resume never repeats a fresh-entry wait. Pausing a wait saves only its
unconsumed time; selection/stop invalidate pending callbacks. Pacing/rate changes do not restart
an active wait. Waits are independent of speech speed. Explicit legacy/zero values keep their
authored meaning; see [authoring](authoring.md). Holds retain the prior visual/caption, while
lead-ins expose the new figure without an upcoming active cue. Do not pad WAVs or resynthesize
narration merely to change pacing; finished-video audio/time axes remain native.

File audio uses its media clock and immediate rate/volume; browser fallback may defer speed
until a natural cue and labels it as reserved. Browser boundaries are approximate and can repeat
text on output changes. Muting controls output, never whether the course can progress. Explicit
silent reading uses labeled reading intervals without pretending they are generated duration.

Use `tk-video` for an authorized finished video. Reuse sufficient original audio instead of
overlaying TTS. Selected narration is embedded with pauses, Korean captions where appropriate,
and scene timestamps on one timeline. Check actual audio streams/non-silence, decoded transitions
and human pronunciation; a silent preview is not a voiced delivery. Accept MP4/WebM files with
captions; video controls follow currentTime/ended/playbackRate. Do not swap per-scene clips or
restart a first poster between sentences. FFmpeg is also required when compressed narration is selected.

The player keeps a main slide/video and visible curriculum, notes/practice and a default-open transcript without focus theft,
floating white captions over rounded black inside the actual displayed slide/video frame, CC toggle, subtitle size and background opacity
(default 50%), volume, speed and fullscreen controls. First-visit sound is off and captions are on;
a combined entry toast shows both states and offers relevant actions. Stored preferences win.
Retry muted with guidance when audible playback is blocked. Reuse versioned
learner preferences across lessons/reloads independently of progress; unavailable storage must
not block playback. Preserve explicit silent mode. Dragging previews silently
and commits once on release; cancel restores prior transport state. Keep caption/marker/selection
contrast usable in both themes, and do not insert generic usage instructions or recurring
illustrative-data disclaimers into the instructor's script. Preserve material technical limits.

## Build audio

Accept mono PCM16 WAV and Opus WebM/Ogg, MP3 or AAC M4A narration. Build with `--audio-format
opus` (default: 32kbps mono, voice application), `mp3` (48kbps for targets with uncertain Opus
support), or `wav`. Originals stay untouched. Compressed inputs/outputs require both `ffprobe`
and `ffmpeg`: decode fully, reject corrupt/silent audio and duration drift over 0.1 seconds.
WAV-only builds use the standard `wave` path without external tools. The working manifest records
format, bitrate, source/encoded sizes and cue durations. Check Chrome, Firefox and Safari playback
and listen to representative cues before claiming compatibility/quality; encoding success and
synthetic test tones do not establish either. Report actual output size, not an estimated promise.

## Player navigation

For slides, Left/Right moves to the previous/next narration cue, and Shift+Left/Right moves to
the previous/next slide. For videos, Left/Right seeks five seconds on the native clock. Space/K
toggles playback, M sound, C captions and F fullscreen/expansion; `?` and the playback settings
open a modal help list. Do not intercept typing, composition, native range/select keys or browser
modifier shortcuts. Respect paused playback, cue boundaries and lesson bounds.

Delegate fullscreen to the generated trusted `srcdoc` frame with `allow="fullscreen *"` and
`allowfullscreen`: file origins may be opaque, so the default `src` allowlist can reject them.
This cannot override an enclosing host policy. Attempt native fullscreen from the learner's
gesture; on disabled/rejected APIs use a labeled in-window stage expansion with controls and
captions intact, keyboard focus containment, Escape exit and restored scrolling/focus. Do not
describe host policy rejection as universal Chrome incompatibility or bypass the embedding host.

The lesson shell uses the viewport height remaining after header/progress. Curriculum list,
content and transcript have independent scroll areas; the curriculum header/collapse stays
reachable. Lesson switches carry only in-memory curriculum scroll state inside the course frame,
restoring after layout with clamp; changed viewports additionally expose the selected item with
minimal movement. No new global preference is stored. Transcript shares the stage's fullscreen
subtree and clock, remains toggleable in native/fallback expansion and sits below media on small
screens rather than covering it. Home and no-JavaScript reading retain document scrolling.

## Stable media geometry

All slide types share one caption overlay within the media viewport. For contained video, keep
it within the actual image rather than the letterbox. Preserve two-line Korean captions, size,
CC and 50% opacity with the existing clock. Captions never create a normal-flow paragraph.
Size media from the transcript-open grid, reserving those columns/rows while it is closed;
same-mode transcript toggles keep both media and controls stable, including the image inside.
Recalculate only for actual viewport/orientation/fullscreen layout changes. Normal start,
sentence, hold and lead-in waits add no visible layout row; the button and off-flow live region
communicate them. Keep errors, unavailable/blocked media and completion announcements accessible
without shifting controls. No padded audio or extra scheduler is needed.
