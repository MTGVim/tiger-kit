# Authoring and Build

Keep curriculum.md, sources.md and the authored course.json together. Use schema 1. IDs use
lowercase ASCII letters/digits/hyphens and remain stable across renames/reordering. Revisions
are explicit strings and change when learning content changes. Each supplied source needs its
used/partial/unavailable/omitted extent in sources.md; course JSON sources links the used claims. A supplied local source may use local instead of url; its inspected provenance is retained without copying private source bytes into the shared HTML.

Minimal authored shape (expand the taught explanation and transfer practice for a real course):

```json
{
  "schema": 1, "id": "example-course", "revision": "1", "title": "A complete course",
  "description": "What the learner will be able to do, distinct from sibling courses", "level": "Introduction; intended audience",
  "objectives": [{"id": "outcome-1", "description": "Predict an outcome and explain why"}],
  "sources": [{"title": "Primary source", "url": "https://example.org/spec"}],
  "lessons": [{
    "id": "first-lesson", "revision": "1", "title": "A worked mechanism",
    "section": "Foundations", "kind": "slides", "prerequisites": [],
    "objective_ids": ["outcome-1"], "narration": "none", "notes": "Mechanism, example and limits.",
    "slides": [{
      "id": "first-slide", "type": "content", "title": "Explain the mechanism", "eyebrow": "Foundations",
      "objective_ids": ["outcome-1"],
      "visual": {"items": [{"label": "Entity and action", "text": "The visible consequence"}]},
      "narration": [{"id": "opening", "speech": "First explain the question, then the mechanism.",
        "caption": "First explain the question, then the mechanism.", "focus": ["item-1"]}],
      "transcript": "First explain the question, then the mechanism."
    }],
    "questions": [{"id": "transfer", "prompt": "Predict a changed case.", "choices": [["a", "A"], ["b", "B"]],
      "answer": "a", "explanation": "Connect the changed conditions to the outcome.", "objective_ids": ["outcome-1"]}]
  }]
}
```

Write `description` as a learner capability distinct from sibling course cards; put the intended audience in `level`.

The content component allows 1-4 items (label <=36, text <=60 characters); slide title <=45.
These are template slot limits, not universal instructional rules. `item-1` etc link cues to
revealed items; an opening cue may use an empty focus. Every visible target must be covered.
Caption concatenation must equal transcript. Read [slide components](slide-components.md) for
data, output, plot and generalized component fields, bounded slots and legacy focus aliases.
Use more slides rather than overflowing a slot. Never
use character counts alone as a visual-quality or teaching check.

Set optional course-level `preview_slide` to `{"lesson_id":"stable-lesson-id","slide_id":"stable-slide-id"}`
to select an existing slide for the catalog. IDs are scoped to that lesson; invalid references fail.
Absent this field, the first slide of the first lesson is used (video uses a textual cover).
The built public metadata contains only the chosen visual and no narration/audio. Choose a preview
that distinguishes sibling courses, and review their opening forms and description first sentences
together. Preview selection does not alter the playback order.

For newly authored lessons follow [lesson plot](lesson-plot.md), including the brief greeting with
lesson number, connection, goal, practice, summary and next-lesson preview. Set the final slide's
`role` to `summary` or `closing`. Older courses without it or with repeated opening forms still
build, with review warnings. Existing cue/objective validation remains mandatory.

Author each narration cue and matching caption as one sentence; split a long sentence at meaningful
phrase boundaries if it would obscure the slide or exceed about two readable caption lines at
the smallest target viewport. Generate a separate clip for each such cue through `tk-tts`, then
normalize the batch under its postprocessing contract. Keep the transcript's wording and order
complete, with stable semantic IDs and matching visual focus. A single long clip must be
resynthesized or aligned with inspected timestamps before splitting its captions; never invent
sentence times from character counts or divide spoken text by guessed duration. Existing authored
long cues remain loadable, but flag them for authoring correction rather than claiming they meet
the sentence-caption contract. Apply the same short-segment rule to timestamped video captions.

For local generated narration set narration to generated and add a relative audio path to
every cue; partial/missing selected audio fails. Explicit none enables silent reading, with
browser-local voice only as a learner-selected fallback. Do not use none to conceal synthesis
failure. Audio paths stay under the source directory and are nonsymlink, validated and embedded. WAV inputs use mono PCM16; compressed formats and build codecs follow [media](media.md).

For a video lesson use kind video, omit slides, and provide video with src (local MP4/WebM),
narration (embedded or explicitly none), optional poster (PNG/JPEG/WebP), and non-overlapping
captions [{id,start,end,caption}] in seconds. ffprobe verifies video duration and required audio
stream before building. Actual decode/non-silence/listening is owned by tk-video/tk-tts and is
still required; an audio stream alone is not proof of intelligible narration. Keep questions,
notes, prerequisites and objective_ids as for slides. No per-scene clip swapping or live TTS.

Keep authored files in `<courses>/<topic>/` and working manifests in `<topic>/build/`.
Build with `build_course.py --input <topic>/course.json --output <topic>/build --dist <root>`;
the CLI defaults the shared root to the source collection's `dist/`. Only `<root>/<topic>/index.html`
and the automatically refreshed `<root>/index.html` go to the shared tree, even for one course.
Use `--lesson-pages` for direct pages in the working output, and `--audio-format opus|mp3|wav`
for the build-only encoding. Built `course.json` records lesson fingerprints/media digests,
measured duration and audio encoding sizes; retain it for `--previous`. Embedded public gallery
metadata stays at the start of the shared HTML, not in a separate file. Read [incremental](incremental.md)
for safe reviewed replacement, catalog rediscovery and ZIP sharing.
The single-file index uses a same-origin local srcdoc frame to isolate each
lesson's media lifecycle; it has no server/framework/network dependency. Switching lessons
releases the prior document/media. Required reading has a static no-JavaScript fallback.
Test the bundle and direct lesson navigation in the actual browser, including local-file storage
and fullscreen permissions; do not assume all browsers support file-origin persistence.

For an incremental version pass --previous <prior/course.json>. New directory construction is
atomic; existing targets/input files are preserved. Substantive same-revision edits, unsafe
media paths, duplicate IDs, prerequisite inversions, uncovered outcomes and caption/cue mismatch
fail before output. There is no automatic source discovery, merge, commit or publication.

Built manifests and embedded metadata own `created_at`/`updated_at` as local build dates
(`YYYY-MM-DD`), not filesystem times or creator-supplied overrides. The first build sets both;
`--previous` preserves creation and preserves update when all lessons are retained. Content or
lesson-revision changes and added/removed lessons update the date. Cosmetic renames/reordering
with unchanged revisions retain it. A legacy previous build's missing dates remain unknown until
a real update supplies `updated_at`; never guess the original creation date. See collections for
date display and sorting. Keep dates out of fingerprints and learner progress.
