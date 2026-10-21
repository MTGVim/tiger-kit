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

For several topics, use `scripts/build_catalog.py --root <collection-dir> --output
<new-catalog.html>` to inspect immediate child course.json files and produce a static linked
home. Validate course IDs and local target paths. Preserve each course's own home/content/progress;
there is no global learner database. Do not add an empty collection layer to one course. The
catalog includes titles, goals and links, without copying progress values that can become stale.
File-origin storage varies by browser; JSON export/import is the portable path. Cross-device
accounts/sync are a separate product requirement. Publication remains separately authorized.
