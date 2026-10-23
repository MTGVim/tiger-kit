# Sources and Distillation

- TigerKit `68b14419cdef1ac9c2c93766c3926f0a192e2098`: keep offline HTML/theme/figure,
  publication and tutoring-state boundaries; adapt a distinct self-contained course artifact.
- [tobyilee/course-builder](https://github.com/tobyilee/course-builder/tree/1913b09bd1bf947b5ee2d1a75eab4396e669fbd3), MIT:
  adapt fixed main-player/curriculum layout, bounded slide components, audio-ended progression,
  cross-artifact checking and aligned script/caption. Retain its notice. Omit its multi-agent
  pipeline, service/runtime choices and unbounded generated HTML. Broken/soft upstream checks
  are not a quality guarantee.
- User-validated local course prototypes 1-15: adapt observed fixes for home/theme, readable
  markers, captions, controls, immediate start, explicit missing-audio recovery, native video
  clock and silent scrub preview. Static regression evidence is not browser/listening proof.
- User-reported course-home incident (2026-10-22), verified against TigerKit source:
  adapt a single course-brand title, lesson context, a distinct home-copy surface and a searchable
  sibling-course gallery with safe refresh/build paths. Keep course-local progress and offline
  boundaries. The gallery/search is a TigerKit extension, not course-builder provenance; no
  Udemy code, branding or visual skin was inspected or copied.
- [Plyr v3.7.8 captions](https://github.com/sampotts/plyr/blob/v3.7.8/src/sass/components/captions.scss):
  keep floating opaque white text/rounded translucent background as a pattern only. Adopt the
  user's adjustable 50% default, not a universal OSS value. Add no Plyr dependency.

Keep source research and learning claims distinct from pedagogical effectiveness, which was not
measured. Omit Marp, a hosted LMS, automatic mastery scoring, accounts and a shared runtime.

- Creator feedback (2026-10-23): reconsider prior default mute and minimum-two-course catalog
  decisions. Adapt sound-on intent with observed-playback feedback, learner preferences,
  collapsible navigation, compressed audio and HTML-only distribution metadata. Keep offline
  progress and reviewed incremental replacement. Report browser/listening coverage separately.
- [MDN play()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/play) and
  [postMessage()](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage), read 2026-10-23:
  adapt rejected-play promise handling and source-bound local-file frame messaging; a gesture
  is not proof of successful audible playback. Add no server or external runtime.
- [FFmpeg codec options](https://www.ffmpeg.org/ffmpeg-codecs.html) and
  [ffprobe](https://www.ffmpeg.org/ffprobe.html), read 2026-10-23: use local Opus voice encoding
  and metadata plus full PCM decoding. Successful encoding is not a browser compatibility or
  pronunciation verdict.
