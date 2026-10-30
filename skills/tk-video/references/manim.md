# External Manim dependency and rendering

Read only for selected Manim work. `manim-composer` plans scenes; `manimce-best-practices`
guides Manim Community Edition implementation. Both are external dependencies from
[adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill). Locate installed paths
through the host's supported skill catalog/loader and read their original `SKILL.md` and
requested references. Keep them unchanged: no TigerKit copies, rewritten substitutes,
automatic install/update or required ManimGL dependency.

## Identity and freshness

Verify exact installed names and readable references, not only folder names. Establish source
identity from an installer lock or a matching Git checkout. Skills CLI lock v3's `source`,
`sourceType` and `skillPath` identify claimed source; `skillFolderHash` is not a Git commit or
SemVer. A surrounding application's Git remote is not the skill's origin.

Query the current upstream default-branch commit and selected skill tree on this route only.
For a Git install, record actual commit and local changes. For a copied install, compare the
complete selected skill's regular file paths/bytes with that upstream tree; record
`content_matches_revision`, not an invented installed commit. Verify needed referenced files.
Preserve modified/mismatched installed files. This upstream has no verified Archify-style
release manifest/version gate: do not require `skill-release.json` or invent a version.

Distinguish missing install, unknown/modified content, verified older content and unavailable
network. Report actual versus latest verifiable state and propose the current source/commit.
Unknown source is not a pass; stop that Manim branch without switching renderers. A failed latest
lookup is `Unverifiable`, not an update grant. Reuse a verified installed snapshot offline only
under the user's explicitly accepted offline scope.

## Runtime and setup handoff

Inspect only the selected route: dedicated native Python's `-m manim --version` and render help,
or an already available Docker engine/image and that image's ManimCE version/help. Confirm
`manim`, not `manimlib`/ManimGL. Do not start Docker or install native dependencies merely to
offer both routes. Installation, image tags and version strings alone do not prove a render.

For missing setup, inspect current upstream installation guidance and selected release metadata,
such as [Manim PyPI metadata](https://pypi.org/pypi/manim/json). Report skill source/revision,
selected environment/image, missing capabilities and known/unknown download versus installed
footprint. Require FFmpeg for assembly, fonts for selected text, LaTeX only for TeX objects and
`tk-tts` only for selected synthesis. No global pip install, model download or Docker pull follows.

For necessary user action/permission, hand `tk-wizard` the exact consumer `tk-video`, selected
Manim criterion, host/runtime/source facts, proposed setup scope, missing capability, user action
and completion signal. Recheck identity, version, relevant capabilities and a small actual render
after that action, then resume. Routine authorized CLI work stays with the implementation owner.

## Author and render

Resolve enabled captions' `soft`/explicit `hard` delivery in the existing initial media-choice
round, reusing answered choices and captions-off. Pass manifest `caption_delivery`; add no saved
preference key. Slide-only theme/emphasis defaults do not recolor or retime continuous video.

Pass accepted audience/claim, scene facts, media choices and owned output paths to the external
composer, then load the external ManimCE guidance. Reuse answered questions; neither external
skill expands installation, preview, publication or filesystem authority. Keep scene code and
caches in the calling run, outside either skill. Render headlessly without preview/auto-open,
using actual installed CLI syntax. Preserve selected theme, resolution, FPS and timeline rather
than applying light-slide/10fps defaults. Compare performance only with identical scene/rate/audio
conditions and measured time/peak memory; never invent sizes.

Keep screen literals `2` and `DOM` separate from spoken readings `이` and `돔`, checking meaning
in context. Use native scene emphasis, captions' safe region and a rendered-source tag. Inspect
initial/final states, transitions and narrated beats; retain pronunciation/clipping as pending
until heard. No ASR is added. Supply one complete MP4 to [animation assembly](assembly.md#continuous-rendered-video).
Author multiple beats in that render instead of freezing, retiming or mixing unrelated movies.
If speech does not fit, return to scene authoring with measured audio. Preserve inputs/code;
dependency and encoding checks do not prove explanatory quality or subtitle-player support.
