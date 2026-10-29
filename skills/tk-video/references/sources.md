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
