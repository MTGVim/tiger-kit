# Archify renderer contract

Dependency: `archify >= 3.2.0` (stable SemVer), from `tt-a1i/archify`.
Verified upstream: `d6059331abbddb49bca380ff46dca8ce33158b04`, version `3.2.0`.
Use the host's installed skill location and read its `skill-release.json` and `SKILL.md`;
verify `skillId`, repository identity and version rather than inferring them from a folder.
Unknown or incomparable metadata is not a pass. Missing/older dependencies return `Blocked`
with installed/required versions and a `tk-wizard` install/update handoff. Do not install,
update or vendor archify. Explanation and research pages never fall back to TigerKit's
legacy document builder/report template, including when interaction is requested.

Read the installed `references/explainer-authoring.md` before drafting. Work entirely in
the calling owner's `.tigerkit/tmp/<skill>/<run-id>/`; use unique panel/block IDs and same-directory image/spec
files. Respect installed syntax rather than copying implementation or a cached example.
Run:

```sh
node <archify>/bin/archify.mjs finalize explainer candidate.archify.md <final.html> --json
```

Use `--repo-root <repo>` for committed code excerpts and verified repository references.
The `@code` source must exist at the pinned commit/path/lines. Do not present worktree bytes
or base lines as head excerpts; use version-qualified sources and literal diff/code blocks
when one document spans snapshots. Add the matching revision to repository metadata.
Explainer 3.2.0 finalize runs validate/deliver/check, not a browser gate. Save its receipt;
never claim browser execution from finalize alone. Regenerate after corrections. Confirm
single-file/offline output, including images; retain source URLs as references only.

Consume finalize's update receipt instead of issuing a duplicate update check. If an update
notice is required, show it once; prefer the user's verified bulk-update routine when known.
Never execute an update. A sufficiently new version is not proof its generated output passed.
The archify page owns its theme and does not read TigerKit `html.theme`; that preference
continues to apply to separate QA, gallery, prototype and visual-question interfaces.

For requested interaction, read [interactive examples](interactive-examples.md). Native
diagram selection, guided steps, focus and route exploration remain live in archify;
do not flatten them into images. Image conversion is for spatial figures the native
diagram grammar cannot express, under [scene figures](scene-figures.md).

For non-software subjects, begin with native `@diagram` plus meaningful `meta.legend`
entries (or the supported explicit hidden legend), using the installed schema. Compact
software defaults can teach false categories. Do not wait for that error before choosing
custom labels. Verify every node label; an ID is not an explanatory label.

Known 3.2.0 limits: explainer chrome falls back to English outside Chinese; compact workflow
branch lanes can contain Chinese; compact semantic legends are software-oriented; `@image`
accepts PNG/JPEG/GIF/WebP, not SVG. Embed a scene PNG using `path`, `alt`, `caption`.
Record immutable UI wording as renderer-owned P/R findings. Fix authored labels/meaning,
not upstream dictionaries or the user's register. Preserve finalize writing diagnostics,
but reject a proposed wording fix that removes a factual qualification.
