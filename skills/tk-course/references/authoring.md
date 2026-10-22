# Authoring and Build

Keep curriculum.md, sources.md and the authored course.json together. Use schema 1. IDs use
lowercase ASCII letters/digits/hyphens and remain stable across renames/reordering. Revisions
are explicit strings and change when learning content changes. Each supplied source needs its
used/partial/unavailable/omitted extent in sources.md; course JSON sources links the used claims. A supplied local source may use local instead of url; its inspected provenance is retained without copying private source bytes into the shared HTML.

Minimal authored shape (expand the taught explanation and transfer practice for a real course):

```json
{
  "schema": 1, "id": "example-course", "revision": "1", "title": "A complete course",
  "description": "Target capability and audience", "level": "Introduction",
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

The content component allows 1-4 items (label <=36, text <=60 characters); slide title <=45.
These are template slot limits, not universal instructional rules. `item-1` etc link cues to
revealed items; an opening cue may use an empty focus. Every visible target must be covered.
Caption concatenation must equal transcript. The packaged hook/timeline/code/comparison/prediction
components retain bounded slots in build_course.py; inspect a selected component rather than
inventing fields. Keep templates fixed; use more slides rather than overflowing a slot. Never
use character counts alone as a visual-quality or teaching check.

For local generated narration set narration to generated and add a relative audio WAV path to
every cue; partial/missing selected audio fails. Explicit none enables silent reading, with
browser-local voice only as a learner-selected fallback. Do not use none to conceal synthesis
failure. Audio paths stay under the source directory, are nonsymlink mono PCM16 and embedded.

For a video lesson use kind video, omit slides, and provide video with src (local MP4/WebM),
narration (embedded or explicitly none), optional poster (PNG/JPEG/WebP), and non-overlapping
captions [{id,start,end,caption}] in seconds. ffprobe verifies video duration and required audio
stream before building. Actual decode/non-silence/listening is owned by tk-video/tk-tts and is
still required; an audio stream alone is not proof of intelligible narration. Keep questions,
notes, prerequisites and objective_ids as for slides. No per-scene clip swapping or live TTS.

Keep authored files in `<topic>/` and initially build to `<topic>/build/`; for later versions,
use a new output directory and review it before replacing an approved build. Build with build_course.py. It validates before writing,
embeds media and the fixed player, and produces course.json, changes.json, index.html and direct
lesson-<id>.html pages. Built course.json records per-lesson content fingerprints including
referenced outcomes and media digests, plus measured narration seconds for gallery metadata;
keep it as the previous version for incremental edits. For an existing multi-course home, pass
`--collection-home <relative-html-path>` to add its return link to all pages and the no-JS fallback.
The single-file index uses a same-origin local srcdoc frame to isolate each
lesson's media lifecycle; it has no server/framework/network dependency. Switching lessons
releases the prior document/media. Required reading has a static no-JavaScript fallback.
Test the bundle and direct lesson navigation in the actual browser, including local-file storage
and fullscreen permissions; do not assume all browsers support file-origin persistence.

For an incremental version pass --previous <prior/course.json>. New directory construction is
atomic; existing targets/input files are preserved. Substantive same-revision edits, unsafe
media paths, duplicate IDs, prerequisite inversions, uncovered outcomes and caption/cue mismatch
fail before output. There is no automatic source discovery, merge, commit or publication.
