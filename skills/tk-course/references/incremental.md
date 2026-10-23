# Incremental Editing and Collections

Read the existing curriculum, source coverage, authored course JSON, media and version before
scoping a change. Verify topic/course identity and ownership; file presence is not permission
to merge. Preserve approved formats and unrelated artifacts. Add/revise only affected lessons
while checking the whole prerequisite graph, objectives, citations, captions and assessments.
A complete course does not require future editing; this is an optional branch.

## Program plans

When a supplied plan spans multiple courses or chapters and this run builds only part, create
`<courses>/<program>.plan.md` before authoring the first part. Use a stable ASCII program slug;
keep the file at the collection root, outside topic/build/dist trees. This is creator context,
not learner progress or a new course JSON schema. Do not require it for an unrelated standalone
course or infer a program from neighboring folders alone.

Use these sections (expand the table to every planned course/chapter):

````markdown
# Program: <program-id>

## Supplied plan
Received: <ISO-8601 timestamp with timezone>
```text
<complete user-supplied plan, verbatim>
```

## Status
| ID / planned ID | Title | Status | Recommended order | Prerequisites | Shared practice project | Plan item |
|---|---|---|---|---|---|---|
| course-01 | <title> | planned | 1 | none | <project ID/path or none> | [course-01](#course-01) |

## Confirmed decisions
- <confirmed order, track grouping, narration/TTS model/voice, distribution root, practice method>

## course-01
<scope, original-plan mapping, track, practice/capstone/material references and authored path when available>
````

Preserve the complete original wording, order, lists and links without summarizing or silently
rewriting them; choose a fence longer than any fence in the supplied text. Record the observed
receipt time; if the historical time is unavailable, label it unknown and record preservation
time separately. Append later supplied revisions with their own receipt times and retain earlier
originals. Keep confirmed decisions separate from the original proposal and mark unresolved
choices as unresolved, never as consent. Retain priority separately when it differs from order.
Use stable item headings/anchors, including chapter IDs scoped by course, so links survive reordering.

Before scoping any invocation in the same collection, inspect root `*.plan.md` and existing
`sources.md` links, then read the matching plan. Resolve identity from the requested program,
course IDs and paths; ask only if multiple matches remain ambiguous. Present remaining `planned`
items by recommended order, noting unmet prerequisites and any `in_progress` work before starting
another item. A supplied target still controls scope. Reuse confirmed common narration consent,
TTS model/voice, shared root and practice decisions without repeating the interview. Check current
media readiness separately; if a choice is unavailable or conflicts with a new request, explain
the concrete issue and resolve only that changed decision.

Initialize every item as `planned`; set only the selected part to `in_progress` when authoring
starts. After a successful build and required verification/review (plus accepted replacement for revisions),
mark that part `built` and retain its actual course/lesson ID, authored path and revision.
A failed/interrupted build stays `in_progress`; report pending verification rather than marking
it built. Keep unrelated rows unchanged. Use `dropped` only for a user-confirmed removal with a
reason, retaining the original plan. For a chapter-only run, update only that chapter; do not mark
its unfinished parent course built. Save confirmed decision/order/track changes when agreed and
update the plan after each build using a reviewed atomic replacement under Artifact Paths checks.

In each course's `sources.md`, retain the supplied corpus accounting and link every deferred
course/chapter scope to its exact plan item. For label `course-02`, the relative link target
would be `../reliability.plan.md#course-02`.
An omission reason alone cannot replace deferred content. Keep plans and these private source
links out of learner notes, public course sources, embedded manifests, catalog HTML and ZIPs.
Share only the existing HTML distribution allowlist, never the collection's authoring tree.

## Course revisions

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
