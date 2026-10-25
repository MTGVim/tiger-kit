# Authoring and build

Keep curriculum.md, sources.md and course.json together. Design the explanation in curriculum.md
before encoding slides: each scene has a point, visible evidence, viewing order and connection.
Use schema 1 and stable lowercase ASCII IDs. Change the lesson revision for substantive changes;
read incremental.md before revising an existing course. Account for every supplied material as
used, partial, unavailable or omitted with reason in sources.md. Link supported claims to sources;
a local source uses local instead of url without exposing private source bytes in shared HTML.

## Course data

```json
{
  "schema": 1, "id": "request-order", "revision": "1",
  "title": "Search response order",
  "description": "Predict which response may update the displayed result",
  "level": "Developers familiar with promises",
  "objectives": [{"id": "predict", "description": "Explain an outdated response overwrite"}],
  "sources": [{"title": "Inspected source", "url": "https://example.org/spec"}],
  "lessons": [{
    "id": "race", "revision": "1", "title": "A late response overwrites the latest result",
    "section": "Response order", "kind": "slides", "prerequisites": [],
    "objective_ids": ["predict"], "narration": "browser",
    "notes": "Explain the shared case, mechanism and limits here.",
    "slides": [{
      "id": "commit-path", "type": "diagram", "title": "Check the request before updating the result",
      "objective_ids": ["predict"],
      "visual": {
        "nodes": [{"id": "response", "label": "Response", "row": 0, "column": 0},
                  {"id": "guard", "label": "Current request?", "row": 0, "column": 1},
                  {"id": "result", "label": "Update result", "row": 0, "column": 2}],
        "edges": [{"id": "check", "from": "response", "to": "guard"},
                  {"id": "commit", "from": "guard", "to": "result"}]
      },
      "narration": [{
        "id": "explain-guard",
        "speech": "Before updating the result, compare the response request number with the current request number.",
        "caption": "Before updating the result, compare the response request number with the current request number.",
        "focus": ["node-response", "node-guard", "node-result", "edge-check", "edge-commit"]
      }],
      "transcript": "Before updating the result, compare the response request number with the current request number."
    }],
    "questions": [{"id": "changed-order", "prompt": "May an older response update the result?",
      "choices": [["skip", "Keep the current result"], ["replace", "Always replace it"]],
      "answer": "skip", "explanation": "Only the current request may commit its response.",
      "objective_ids": ["predict"]}]
  }]
}
```

This is a schema example, not a complete lesson or a style sample. Expand the worked case and
explanation before delivery. description states the learner capability; level names the audience.
Optional readiness belongs only to material untaught prerequisites; see readiness.md.

Read slide-components.md for the representation selected by the scene plan. Components and their
slot bounds are renderer capabilities, not mandatory teaching forms. Every referenced focus target
must exist and every semantic target must have a cue. Concatenated captions equal transcript.
Draft and refine the complete explanation first; split sentence/phrase cues afterwards. Existing
long cues remain loadable, but require reauthoring or inspected alignment before precise captions.
Do not invent word times from text length. Covers, maps, greetings and closing roles are optional.

## Narration routes

Explicit narration is browser (recommended Web Speech API), generated (tk-tts file audio),
supplied (existing file audio), or none (silent reading). Reuse settled choices. Browser and none
need no synthesis engine, model download, FFmpeg or audio files for an image-free build. Browser
voices are discovered at playback; availability and pronunciation depend on that device. Do not
claim that HTML-contained speech text is embedded audio. Preserve legacy generated/none meanings.

For generated/supplied, attach a source-relative nonsymlink audio path to every cue. Partial or
missing selected file audio fails. For browser/none, omit audio; do not hide failed synthesis with
a mode change. Keep display spelling separate from spoken pronunciation. Read media.md for file
formats, codec capabilities, exact durations, player behavior and actual listening limits.

Video lessons use kind video, omit slides, and provide video with local MP4/WebM src, narration
embedded or none, optional poster and nonoverlapping captions [{id,start,end,caption}] in seconds.
Pass the accepted teaching scenes/script to tk-video. A voiced movie needs actual file audio;
browser speech cannot supply an exported audio track. The movie owns its clock and audio.

## Build and compatibility

Use build_course.py --input <topic>/course.json --output <topic>/build --dist <courses>/dist.
Working manifests stay in build. Default shared output contains a small <dist>/<topic>/index.html,
lessons/lesson-<id>.html and .js loader copies, content-addressed assets/image|audio|video/ and a public course-files.json
allowlist, plus a refreshed catalog even for one course. Media remain files; repeated assets are
copied once. --lesson-pages adds working direct pages and their media; --audio-format opus|mp3|wav
controls file-audio encoding only. --single-file embeds the whole course only when the final
UTF-8 HTML is at most 10 MB; an oversized export fails before delivery and directs the creator
to the default folder. The no-dist Python compatibility API retains its older single-file default;
pass single_file=False there for a folder. Originals stay intact. --previous <prior-built/course.json>
protects incremental identity, dates and media digests; build to reviewed staging before replacement.
See incremental.md for collection order, date provenance, plan preservation and sharing allowlists.

Browser courses show an unmeasured browser-voice duration in the catalog; measured file duration
is not a silence flag. The selected playback setting follows each lesson's authored narration.

The builder validates references, schema, geometry and selected files. It cannot certify meaning,
style, learning effectiveness or pronunciation. Review the full slide/script/answer sequence
separately before declaring completion. Build/source revision consistency preserves prior
completion and notes; unknown learner schemas remain recoverable rather than reset.

The default entry loads only the selected lesson through a classic script and puts its HTML in
a trusted srcdoc frame. A base URL resolves relative media from lessons/. This avoids fetch, ES
modules and a server while preserving the entry storage origin across lesson changes and existing
course progress. Keep source-bound postMessage navigation, static no-JavaScript lesson links/reading
and existing IDs. --single-file embeds all lessons and retains the same frame origin. Share the complete topic folder (or ZIP),
not index.html alone. An in-app preview must support sibling relative files; otherwise provide the
ZIP for extraction and browser opening rather than claiming its preview works. No private plan, setup detail, objective
ID, generated demo content or sharing control belongs in the teaching screen. Preserve notices.
Read media.md and slide-components.md for runtime and complete-frame acceptance. Inspect actual
pixels, cue order and caption coverage at the minimum intended viewport; bounds alone do not
establish readability. No vertical intra-slide scroll or resized canvas may conceal overflow.
Optional preview_slide uses existing {lesson_id,slide_id}; choose a distinguishing actual figure.

Optional course pacing accepts initialLeadInMs, postSlideHoldMs, slidePauseMs and sentencePauseMs,
finite numbers 0-5000. Defaults 5000/1800/1200/600 preserve 3000ms between slides; explicit zero
and legacy pacing keep their authored meaning. Presentation pacing changes neither fingerprints
nor progress. Captions remain within the actual image and leave essential evidence unobscured.
