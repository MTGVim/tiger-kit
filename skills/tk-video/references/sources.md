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
