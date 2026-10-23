# Incremental Editing and Collections

Read the existing curriculum, source coverage, authored course JSON, media and version before
scoping a change. Verify topic/course identity and ownership; file presence is not permission
to merge. Preserve approved formats and unrelated artifacts. Add/revise only affected lessons
while checking the whole prerequisite graph, objectives, citations, captions and assessments.
A complete course does not require future editing; this is an optional branch.

Keep the prior built course.json: it records media digests before a same-path file changes.
A previous media-bearing authored file without a recorded digest cannot prove prior identity.
Use stable course and lesson IDs, independent of title/order, and explicit content revisions.
Retain revision for a cosmetic rename or reorder. Change the lesson revision for changed
outcomes, explanation, examples or assessment. Build to a new directory with `--previous
<old-course.json>`; substantive same-revision edits fail before writing. Review changes.json
and generated output before replacing an approved target. Do not auto-merge two course identities;
merging requires an explicit scope and a reviewed ID/progress mapping with original retention.

Progress is course-local manual completion, revision, notes and historical completions in this
browser. Renaming/reordering preserves it. A changed/deleted lesson retains historical completion
and notes; changed material needs review and removed lessons leave the current denominator.
Unknown schema, another course ID or corrupt JSON must not silently reset or overwrite storage.
The player blocks saving over unreadable state and exports the original for recovery; only a
valid explicit import resumes saving. Do not combine it with teach's demonstrated mastery.
Do not silently sync personal educational records or commit them.

## Shared distribution

Keep source files under `<courses>/<topic>/`, working manifests/changes under `<topic>/build/`,
and only shareable single-file HTML under `<courses>/dist/<topic>/index.html`. Both builders accept
`--dist <root>`; reuse the agreed root. `build_course.py` creates/refreshes the root's catalog after
each successful build, including one course. `--lesson-pages` creates optional direct pages only
in the working output. Never put source audio, dependencies or separate manifest JSON in `dist/`.

The course's first 64KB contains `tigerkit-course-manifest` JSON (public metadata, lesson titles,
preview, revision and measured audio length). `build_catalog.py --dist <root>` discovers only
`<root>/*/index.html` and reads that bounded prefix; it needs neither source nor working manifests.
Reject missing/corrupt manifests, duplicate IDs and symlinks; zero courses fails. Adding/removing
course folders and rebuilding updates the list. The root's marked catalog is replaced atomically;
unmarked HTML is preserved. Client search covers titles, descriptions, goals and lesson titles;
without JavaScript all cards remain readable. Preserve compact thumbnails and a one-row empty state.

Build revisions with `--previous <old-build/course.json>` to new work and distribution roots.
Review `changes.json`, HTML and media before explicitly replacing the prior shared course; retain
originals, then refresh the destination catalog. Existing shared course targets are refused rather
than silently overwritten. Catalog generation changes only its own marked output, never courses.
Use `--zip` to produce a sibling `<root-name>.zip` containing just the catalog/course HTML paths;
replace only archives bearing the TigerKit ZIP comment marker. Report path, size and course list.
A copied/extracted tree retains relative links. Each course verifies a local catalog by frame
handshake and hides that breadcrumb when shared alone; no fetch/server or external request is needed.

Progress remains course-local; preferences are learner-wide and never included in progress JSON.
File-origin storage varies by browser; JSON export/import is the portable path for progress.
Cross-device accounts/sync are separate requirements. Publication remains separately authorized.
