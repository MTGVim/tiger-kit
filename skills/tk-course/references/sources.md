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
- Creator-supplied multi-course workflow and observed proposal-loss incident (2026-10-23),
  checked against the current per-course authoring and distribution contracts: adapt verbatim
  collection-level plans, stable deferred-scope links, build status and confirmed-choice reuse.
  Keep course-local progress and HTML-only distribution. Omit a program runtime, automatic
  sequencing, transcript recovery and inferred consent; this contract comes from the explicit
  reusable creator workflow, not course-builder upstream behavior.

- Creator incident (2026-10-24): the supplied evidence distinguishes a course-local auto-height
  override from shared canvas/evaluation gaps. Adapt fixed 16:9 media, intrinsic image containment,
  semantic splitting and whole-frame acceptance; keep independently scrolling documents. This
  deliberately changes the former content-grown/portrait renderer policy. The original course
  and its prior receipts were not modified or independently recovered by this maintenance.
- Rechecked primary upstream HEAD on 2026-10-24:
  [course-builder slide-authoring@1913b09](https://github.com/tobyilee/course-builder/blob/1913b09bd1bf947b5ee2d1a75eab4396e669fbd3/.claude/skills/slide-authoring/SKILL.md).
  Keep single-beat/type focus and cue remapping after slide changes; adapt semantic splitting and
  source-only editing. Omit Marp, fixed slide counts and character-count-only acceptance. This
  source does not explicitly mandate 16:9; upstream runtime/evals were not executed.
  The fixed canvas is the creator's requested course-media policy, not a universal pedagogical
  optimum or a measured learning-effect claim.

- Creator follow-up incident (2026-10-24), checked against the current source and existing
  figure/navigation evaluations: adapt explicitly requested real-screen imagery and separate
  teaching scenes; one contained caption overlay, layout-free
  waits, paused lesson entry and capability-scoped image validation. These revise the former
  below-figure caption oracle, responsive closed-rail expansion and entry-autoplay behavior.
  Keep the existing cue clock, offline/preservation and incremental staging contracts.
- Rechecked course-builder HEAD at `1913b09bd1bf947b5ee2d1a75eab4396e669fbd3`; read the pinned
  slide-authoring, coherence-review and `scripts/generate-player.py`. Keep semantic scene/cue
  correspondence and cross-asset checking. Adapt them to inspected real pixels and current
  media geometry; omit Marp, fixed counts, proportional caption timing, its runtime and review
  orchestration. Upstream runtime/evals and actual user-course backfill were not executed.
- Creator correction (2026-10-25), reproduced in the packaged player: adapt reclaimed transcript
  columns/rows and centered maximum-fit 16:9 media in native fullscreen and in-window expansion.
  This supersedes the 2026-10-24 transcript-open size reservation; keep caption containment,
  ordinary-wait geometry and the playback clock. Rechecked course-builder at the same pinned
  HEAD and read its player, slide-authoring and coherence-review contracts: keep aspect containment;
  omit its fixed three-column layout. The maximize/toggle correction is TigerKit-specific.

## Explanation-first rebuild (2026-10-25)

- Rechecked course-builder HEAD at 1913b09bd1bf947b5ee2d1a75eab4396e669fbd3:
  [orchestrator](https://github.com/tobyilee/course-builder/blob/1913b09bd1bf947b5ee2d1a75eab4396e669fbd3/.claude/skills/course-builder/SKILL.md)
  and coherence-review. Adapt the first coherent lesson pilot and slide/script/answer review;
  omit its runtime, fixed slide counts, provider routing, duration guesses and automatic
  approval rounds. Its presence/heuristic checks are not semantic quality evidence.
- [OpenMAIC lecture-style](https://github.com/THU-MAIC/OpenMAIC/blob/dff201b49857918885cc5ebadb4a8af254b6ae9d/skills/agent-runtime/lecture-style/SKILL.md)
  and stage-design, MIT, rechecked HEAD dff201b49857918885cc5ebadb4a8af254b6ae9d:
  adapt continuous explanation across scenes, recurring cases and explicit transmission of
  style/content into generation inputs. Omit its classroom runtime, roster, density quotas
  and tool protocol. No OpenMAIC implementation or instruction prose is copied.
- Creator-approved redesign: replace mandatory greeting/map/summary structure with outcome,
  explanation, scene plan, visuals, refined script and pilot/review. Keep the renderer/player
  boundary, fixed canvas, reviewed incremental replacement and prior progress preservation.
  Relationship diagrams are a TigerKit implementation, not an upstream renderer transplant.
- Creator selects Web Speech API as the recommended quickest HTML narration route, retaining
  optional generated/supplied file audio and explicit silence. Recommendation is not consent;
  file-synthesis setup is conditional and voiced movies still need actual file audio.
- [MDN getVoices](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesis/getVoices),
  [utterance end](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/end_event)
  and [localService](https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisVoice/localService),
  read 2026-10-25: retain local Korean voice discovery/voiceschanged and event-driven progression.
  Browser/device availability and human pronunciation remain separate from build success.

Earlier source entries describe historical policies. This section supersedes mandatory lesson
beats and generated-file-first/browser-fallback authoring; current SKILL.md and references own
behavior. Upstream runtime/learning-effect evaluations were not executed for this adaptation.
