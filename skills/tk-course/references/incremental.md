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
and the shareable course folder under `<courses>/dist/<topic>/`. Its small `index.html` loads only
the chosen lesson; `lessons/` contains standalone HTML and classic-script loader copies, and
`assets/` contains content-addressed media. `course-files.json` lists public files explicitly. Both builders accept
`--dist <root>`; reuse the agreed root. `build_course.py` creates/refreshes the root's catalog after
each successful build, including one course. `--lesson-pages` creates optional direct pages only
in the working output with their media. Copy only selected rendered assets, never source trees,
plans, learner records or dependencies. Keep public delivery metadata separate from working
course.json/changes.json. `--single-file` retains small embedded exports (10 MB maximum).

## Collection order and dates

Before authoring siblings, distinguish each card by its learner capability and an actual teaching
preview. Choose the opening from its explanation; a useful form can recur without copying the
same generic description. Use preview_slide when another authored scene better distinguishes it.

Order belongs to a collection, not `course.json`; do not rename stable IDs or rebuild course HTML
just to change it. Optional `<dist>/catalog.json` uses this public shape:

```json
{"schema":1,"title":"Frontend Reliability Engineering","order":["frontend-test-speed","flaky-test-hunting"],"requires":{"flaky-test-hunting":["frontend-test-speed"]}}
```

`schema` is required; `title`, `order` and `requires` are optional. Without the file, retain folder
order. With it, list named IDs first and unlisted courses by title then ID, number the recommended
positions and show actual prerequisite titles separately. Reject duplicate/unknown IDs, malformed
settings, self/cyclic dependencies or a final order that places a prerequisite after its dependent.
Multiple entry points are allowed; numbers do not imply additional dependencies. Keep tracks/groups
out of schema 1. Removing a course requires removing its settings references before refresh.

Before adding a new course to such a root, reuse a predeclared position or the program plan;
ask only if the position is unresolved. The noninteractive builder refuses unresolved placement
before writing and accepts `--catalog-position <1-based position>` as the resolved decision,
updating the collection settings atomically. A course ID already present in `order` needs no
second confirmation. Staged revisions copy the agreed settings and build all referenced courses
before final catalog validation. Standalone refresh rejects IDs missing from the shared tree.

Run `build_catalog.py --dist <dist>` after editing settings. It changes only its marked catalog,
never existing course HTML or dates. `--zip` includes the validated optional `catalog.json` plus
the explicit public course-file allowlists, so an extracted collection can regenerate its recommended path.
Keep private plans, sources, learner data and raw audio out of that public file.

Cards and course homes show registration and update dates, omitting a duplicate update date and
unknown legacy dates. The catalog offers recommended order, recent update and recent registration;
ties follow recommended order and missing dates stay last in either direction. Date direction
defaults to newest first and is disabled for recommended order. Persist sort/direction locally
without blocking on denied/corrupt storage; search and no-JavaScript reading remain available.
Keep all card text readable with wrapping and content-driven height. Use shared fluid grid columns
inside a centered group, retaining tracks during filtering instead of recentering every row or
stretching the last search result; reserve scrollbar space to avoid extra horizontal shifts.

The course's first 64KB contains `tigerkit-course-manifest` JSON (public metadata, lesson titles,
preview, revision and measured audio length). `build_catalog.py --dist <root>` discovers only
`<root>/*/index.html` and reads that bounded prefix, then validates the optional public course-files.json allowlist;
it needs neither source nor working manifests.
Reject missing/corrupt manifests, duplicate IDs and symlinks; zero courses fails. Adding/removing
course folders and rebuilding updates the list. The root's marked catalog is replaced atomically;
unmarked HTML is preserved. Client search covers titles, descriptions, goals and lesson titles;
without JavaScript all cards remain readable. Preserve compact thumbnails and a one-row empty state.

Build revisions with `--previous <old-build/course.json>` to new work and distribution roots.
Review `changes.json`, HTML and media before explicitly replacing the prior shared course; retain
originals, then refresh the destination catalog. Existing shared course targets are refused rather
than silently overwritten. Catalog generation changes only its own marked output, never courses.
Use `--zip` to produce a sibling `<root-name>.zip` with the catalog, listed lesson/media files and optional public settings;
replace only archives bearing the TigerKit ZIP comment marker. Report path, size and course list.
A copied/extracted tree retains relative links. Share each complete topic folder, or the complete
collection ZIP, rather than copying only index.html. Legacy and explicit small single-file courses
remain valid catalog entries. The ZIP reads only the explicit public allowlist, refuses missing,
symlinked or unsafe paths, and excludes unlisted files even inside assets/. Each course verifies a local catalog by frame
handshake and hides that breadcrumb when shared alone; no fetch/server or external request is needed.

Progress remains course-local; preferences are learner-wide and never included in progress JSON.
File-origin storage varies by browser; JSON export/import is the portable path for progress.
Cross-device accounts/sync are separate requirements. Publication remains separately authorized.


## Backfill teaching visuals and pacing

Inspect authored `course.json`, curriculum/sources, prior built manifest and original media before
backfilling an existing course. Name the outcomes missing observed screen/spatial/state evidence;
add meaningful supported figures only there, updating descriptions, provenance, rights and cues.
For requested real-screen lessons, replace affected card topics with distinct inspected screen
scenes; an original schematic or asset count cannot satisfy that request. Keep outcomes with
unavailable essential real screens incomplete. Inspect remaining reported card scenes as well.
If authored input or prior media identity is missing, report the required input rather than
claiming automatic recovery. Image-byte changes at the same path enter the persisted fingerprint.

For legacy growing/portrait slide media, inspect the source and split overfull content into
meaningful questions/states on the fixed 16:9 canvas. Preserve layout/entity IDs across A/B scenes;
remap each cue's order, caption and emphasis target to its scene and verify the actual clips.
Removing a height override while containing the same unreadably dense composite is insufficient;
opening a scroller is also insufficient. Validate the complete media frame in fresh staging at
each supported viewport before replacement, with independent notes/transcript scrolling intact.

Reuse raw/normalized cue audio when the explanation still matches the new figure. Synthesize only
changed speech at new paths and update its caption/transcript/targets together; never split audio
by character-count timing. Pacing alone requires no synthesis or learning-content revision.
Preserve course/lesson/cue IDs, manual completions, notes, unknown progress and date provenance;
raise lesson revisions only for substantive teaching changes. Numeric saved slide/cue indices
can change meaning after splitting: bind saved positions to the content revision, preserve
legacy records and use a labeled recheck starting point rather than pretending an old index
restores the same scene. Keep explicit legacy/zero pacing.

Preserve original authored files and approved HTML; build a fresh work/dist staging tree with
`--previous <prior-built-course.json>`. Review changes.json, media digests, the actual visual
question/figure correspondence, initial/hold/lead-in boundaries, pause/seek and progress import.
Replace only the authorized target after review and refresh the catalog; preserve sibling courses
and third-party notices. Report unavailable real course inputs or pending human visual/listening
review. Fixture rebuilds prove the migration path, not completion of a user's unseen course.
