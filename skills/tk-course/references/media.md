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

Slides use actual audio ended events, not guessed speech duration. First play starts immediately;
later slide/sentence gaps default to 1200/600ms, configurable independently of speed. File audio
uses the media clock and immediate rate/volume; browser fallback may defer speed until a natural
cue and labels it as reserved. Browser boundaries are approximate and can repeat text on output
changes. Muting controls output, never whether the course can progress. Explicit silent reading
uses labeled reading intervals without pretending they are generated audio duration.

Use `tk-video` for an authorized finished video. Reuse sufficient original audio instead of
overlaying TTS. Selected narration is embedded with pauses, Korean captions where appropriate,
and scene timestamps on one timeline. Check actual audio streams/non-silence, decoded transitions
and human pronunciation; a silent preview is not a voiced delivery. Accept MP4/WebM files with
captions; video controls follow currentTime/ended/playbackRate. Do not swap per-scene clips or
restart a first poster between sentences. FFmpeg is also required when compressed narration is selected.

The player keeps a main slide/video and visible curriculum, optional notes/transcript/practice,
floating white captions over rounded black, CC toggle, subtitle size and background opacity
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
