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

For two or more topics, use `scripts/build_catalog.py --root <collection-dir>`; the default output
is `<collection-dir>/index.html`. An explicit `--output` must stay directly in that root.
Discover a direct child course.json/index.html pair first, otherwise the child's build/ pair.
The built manifest owns metadata, including measured narration seconds; do not read source media
paths from a different directory. Reject duplicate IDs and unsafe/missing entries. Replace only
an HTML file carrying `<meta name="tigerkit-course-catalog">`, atomically; preserve unmarked files.
The offline gallery shows the first slide preview, title, description, level, lesson count and
recorded audio length (or an explicit unavailable label for older builds). Client-side search
filters titles, descriptions, goals and lesson titles. Without JavaScript all cards remain readable.
Use the returned per-course `collection_home` value with `build_course.py --collection-home
<relative-html-path>` when building each course from its authored input to a new output directory.
For `<collection-dir>/<topic>/build/`, that value is `../../index.html`. The header link exits the
single-file bundle's frame as well as working from direct lesson pages; review replacement of
the prior build, then refresh the catalog. Catalog generation itself does not mutate course files.
Preserve each course's own home/content/progress; there is no global learner database. Do not add
an empty collection layer to one course. Do not copy progress values into the catalog.
File-origin storage varies by browser; JSON export/import is the portable path. Cross-device
accounts/sync are a separate product requirement. Publication remains separately authorized.
