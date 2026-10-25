# Learning Paths and Retained Course Formats

Read for a dependent multi-lesson path, an explicit multi-chapter material request, an
existing-material rewrite, or packaging an appended lesson linked to retained HTML.
A focused unlinked lesson needs only the core teaching loop.

For a new dependent path, align the mission before deep research or curriculum generation,
even when past context shows technical experience. Surface target capability, demonstrated
versus declared knowledge, untaught gaps, depth/time budget, practice, constraints and exclusions.
Reuse explicit current answers; a no-interview or short-study request skips the round and
keeps unknowns visible. Do not infer a goal from professional expertise or demand a new gate.

Retain the mission with provenance in existing `curriculum.md`, `MISSION.md` or
`learner-profile.md`, even without an interview. Use the existing owner rather than copying
it into each file. Confirm actual mission changes with the learner. After an interview save
`learner-profile.md` in the verified home; separate claims, observations and unknowns.
Do not store a transcript, guessed progress, inferred mastery or global memory.

Work backward from what the learner should explain, judge or do. Map outcomes to
prerequisite-ordered units and checks, scope and exclusions in `curriculum.md`.
A path plan is not an obligation to generate all future lessons: normally build the next
small meaningful unit, with retrieval or transfer across relevant earlier dependencies.
Keep planned/covered material separate from demonstrated understanding.

When the user explicitly requests complete multi-chapter material now, retain that extent:
create coherent dependent chapters, reusable source in `chapters/`, curriculum, sources,
mission and a profile when interviewed. Teach the problem, mechanism, example and limits
in each chapter; do not split solely to reach a count. Use `index.html` as the default
complete document for that explicit format, with chapter anchors and separated answers,
unless another destination/structure is requested. Do not replace a complete-material
request with only a plan or one sample lesson. It is learning material, not a course player,
progress runtime or evidence that the learner completed it.

For an existing single HTML, Markdown or multi-chapter home, inspect its index and relevant
artifact notes first. Preserve the verified format, scope, lesson numbering and unrelated
content. Distinguish current material from samples/historical alternatives. Do not migrate
or split a legacy document merely because new topics use lesson files. Revise only the
requested unit and materially affected navigation; refresh full material only when requested.

## Package a linked collection

The common `scripts/package_html.py` rewrites every allowlisted HTML to embed its export
payload. On an append, do not run that mutating step over retained originals. Copy the
explicit public file allowlist, including linked dependencies, into a run-owned staging
directory under `.tigerkit/tmp/tk-teach/<run-id>/`, preserving relative paths. Use ordinary
copies, not symlinks or hard links; exclude private sources, profiles and learning records.
Run the existing packager with staging as `--root` and its normal filename/allowlist rules.
Publish back only the new lesson and an explicitly changed index or requested revision;
never copy the whole staged HTML set back over learning history. Preserve prior originals
even when their staged export payloads change. Check original hashes, relative links and
the new export's bytes/ZIP contents before delivery. Explicitly authorized whole-material
rewrites keep their existing overwrite scope.

Use only relevant lesson links, not a full future-course embed. The shared export contract
still duplicates allowlisted sources and can grow for large linked collections; preserve
its archive delivery/viewer-button limitation rather than claiming constant-size HTML.
Large media separation and a different export runtime remain outside this reconstruction.
