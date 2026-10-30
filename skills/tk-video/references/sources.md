# Design sources

The source review read `obra/superpowers` PR #2214 at merge
`dd53fe0b57223bbbbb8ceae0bda2ba8a26d1c29a`: SKILL.md, rendering-stills.md and assembling.md.
[Original design](https://github.com/obra/superpowers/tree/dd53fe0b57223bbbbb8ceae0bda2ba8a26d1c29a/skills/proving-it-works-with-a-movie)
was removed by [#2335](https://github.com/obra/superpowers/pull/2335) before release for code-quality
reasons. It is prior art, not a supported runtime dependency or imported implementation.

Keep: stills for sequences, measured narration holds, truthful capture boundaries and finished-cut
inspection. Adapt: explicit explanation mode, deterministic basic media checks, libass preflight
and soft-caption fallback. Preserve explicit narration opt-in and independent application verdict.
Omit: ASR verification, automatic tool/model acquisition, terminal/log reels, Windows support and
mandatory committed movie pipelines. Authoring and evidence stay under TigerKit's artifact policy.

TigerKit introduced shared 10fps GIF/MP4 encoding in `1d6630284a9f14491967f2bb5f87f0a62e87571c`;
its code and change record name the rate but give no MP4-specific rationale. The original
assembling examples above use `-r 30`, not a shared 10fps requirement. Keep 10fps as GIF's compact
default alongside its 5MiB size warning and for stills; MP4 capture rate follows source metadata
or disclosed timestamp estimation, capped at 30fps. This is a product tradeoff, not a size guarantee.


## Optional presentation effects

Reviewed 2026-10-28: [FFmpeg zoompan source](https://github.com/FFmpeg/FFmpeg/blob/c69954c34522c53234dfd43fa7a0cb3b02f39e47/libavfilter/vf_zoompan.c),
its filter documentation and the installed FFmpeg 6.1 implementation;
[libass format guidance](https://github.com/libass/libass/wiki/ASS-File-Format-Guide) and
[Aegisub drawing tags](https://aegisub.org/docs/latest/ass_tags/). Keep original timing and
fixed output dimensions; adapt input-frame-based zoom expressions, actual glyph-ink measurement
and ASS vector cards. Use RGB crop input and upward-rounded origins to preserve edge borders;
integer crop positions remain a motion limitation.
Square boxes use libass's `BorderStyle=4` extension, verified by decoded-frame tests; portable
ASS playback compatibility is not claimed. The delivery is already burned video plus plain SRT.

The supplied four-variant experiment is single-creator preference evidence. Adapt its combined
callout/zoom treatment as opt-in; omit a universal style change. [Openscreen](https://github.com/siddharthvaddem/openscreen)
provides cursor-following automatic zoom as prior art only; no desktop recorder, runtime or code
is imported. Keep source-coordinate handoff under the existing capture owner.

For existing wait/loudness policies, [Fluent Spinner](https://fluent2.microsoft.design/components/web/react/core/spinner/usage)
and [Wait UX](https://fluent2.microsoft.design/wait-ux) support the one-second threshold;
[Primer loading](https://primer.style/product/ui-patterns/loading/) supports indeterminate
feedback but does not establish that exact threshold. [EBU R128](https://tech.ebu.ch/publications/r128)
supports -23 LUFS programme loudness; preserve -18 as tk-tts's default and actual listening.

## Presentation planning, slides and captions-off (2026-10-29)

Fresh [FFmpeg filter documentation](https://github.com/FFmpeg/FFmpeg/blob/31ba826726fd0d1547f2c22e041848d1d7f3f860/doc/filters.texi)
was inspected at current HEAD `31ba826726fd0d1547f2c22e041848d1d7f3f860`, including subtitles/libass,
zoompan's explicit size/rate/timing and the installed FFmpeg encode/decode behavior. Keep existing
capture-coordinate and text-effect checks; adapt captions-off by omitting subtitle filters/tracks
while preserving audio validation. Omit new renderers, tool installation and implicit effects.
The shared media-choice/save contract extends TigerKit's existing runtime-verification preference
contract; the supplied repeated-assembly incident motivates one first-round resolution across
parents and direct video, without adding a runtime dispatcher or new standing authority.

Slide copy criteria selectively adapt TigerKit's `tk-explain` clear-writing/reader-formatting
contracts (source baseline `e672abcc0fedc8b91766266c8117a21496f02cbe`) to predicate completeness,
consistent register, caption/narration semantics and comparison visibility. Keep actual frame and
listening checks separate; omit a sibling-package runtime import or full prose-review pipeline.
Light slides and in-slide emphasis are authoring fallbacks for this workflow, not empirical claims
of universally better learning. Explicit/saved choices take precedence.

## External Manim and selectable captions (issue 486)

Inspected [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill/tree/cef045011722d285692e3381d12d4d637da56e18)
at its verified current HEAD: composer and ManimCE skill entrypoints, CLI/config/text rules,
test guidance/utilities and MIT license. Keep these as unchanged external dependencies, not
vendored guidance or templates. Adapt only the caller's source/readiness contract, selected
runtime handoff and continuous-media boundary; omit ManimGL, automatic setup and preview.
The upstream lacks verified SemVer release metadata; installer folder hashes are not commits.

The installed ManimCE 0.20.1 Docker runtime's actual render help owns tested CLI syntax; it is
not claimed to be latest. FFmpeg's [stream selection/streamcopy](https://ffmpeg.org/ffmpeg.html)
and [HTML track element](https://html.spec.whatwg.org/multipage/media.html#the-track-element)
inform explicit audio mapping and browser WebVTT delivery. Keep fractional source rates and
native audio, adapt selectable mov_text plus sidecars, and omit a universal player or silent
retiming. Inspect emitted default disposition: clearing it does not guarantee the MP4 muxer
leaves the first subtitle initially disabled. Report actual browser/player checks separately
from encoding, source inspection, synthetic audio and human listening. Upstream's full example
test suite was not run; use bounded real-render and regression evidence for this integration.


## Answer-first opening and visible CC (issue 490)

The supplied React/Dijkstra viewer feedback in [#490](https://github.com/MTGVim/tiger-kit/issues/490)
is a concrete correction to those delivered cuts, not evidence of universal learning gains.
The external composer's narrative patterns at the verified revision above retain mystery/payoff
examples. Keep its short question hook and progressive object motion; adapt the caller's accepted
question → immediate answer/reason → worked-example order. Omit an external-skill rewrite, a
mandatory suspense arc and a new global caption preference.

FFmpeg's [pad filter](https://ffmpeg.org/ffmpeg-filters.html#pad-1) and decoded regression frames
support extending the existing UI-preserving band to explicitly selected hard animation captions.
Keep source pixels, rate and timing, disclose added height, and inspect longest/multiline cues.
Soft/off defaults and independent listening remain unchanged.

## Native Manim explanation, not screenshot substitution (2026-10-30)

Rechecked the upstream default branch at the same `cef045011722d285692e3381d12d4d637da56e18`.
The original composer's visual-continuity/progressive-revelation guidance and ManimCE's scene
rules remain external and unchanged. Keep native object transformations and meaningful state
continuity; adapt the caller's renderer choice, before/operation/after inspection and source
provenance to the accepted React/Dijkstra workflow. Omit copied upstream templates, universal
Manim prerequisites, decorative-motion quotas and animation-count quality claims. The two
delivered cuts establish an actual native-render path, not universally maximal use or learning
gains. Explicit HTML/still output and observed UI retain their own owners and approval boundaries.
