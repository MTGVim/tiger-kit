# Manifest and commands

Use UTF-8 JSON. Paths resolve relative to the manifest. Build from identity-neutral,
normalized copies, never raw producer HTML. All item/candidate pairs must be present;
represent missing/failed generation explicitly. Keep study/item/candidate IDs stable.

```json
{
  "study_id": "voice-study-01",
  "version": "2",
  "seed": "fixed-study-seed",
  "title": "한국어 문장 청취 비교",
  "transformations": ["동일한 음량 기준으로 조정했습니다."],
  "favorite": true,
  "candidates": [{"id": "engine-one", "name": "Engine One"}, {"id": "engine-two", "name": "Engine Two"}],
  "items": [{"id": "sentence-01", "title": "발음과 자연스러움", "script": "오늘은 맑고 따뜻합니다.", "description": "같은 문장을 듣고 발음과 자연스러움을 평가해 주세요."}],
  "outputs": [
    {"item_id": "sentence-01", "candidate_id": "engine-one", "kind": "audio", "path": "prepared/one.wav"},
    {"item_id": "sentence-01", "candidate_id": "engine-two", "kind": "audio", "error": "생성 실패", "diagnostic": "private producer error"}
  ]
}
```

Kinds: `audio` (WAV/MP3), `image` (PNG/JPEG/WebP), `video` (MP4/WebM), `text`
(inline `text`). Use a neutral shared title/item descriptions/transformations;
put private producer errors only in `diagnostic`. All failed cards show the same neutral
failure message; source reasons remain in the separate key. Text is escaped, never executed.
Use optional item `title` for the evaluation topic and `script` for the exact shared source
text; `description` supplies the evaluation guide. These neutral fields stay in the active
item's sticky context. Long contexts scroll internally and remain keyboard accessible.
The helper checks literal names/IDs in shared labels and text; inspect logos, spoken names,
watermarks and other semantic cues manually. It cannot establish semantic anonymity.

After the package-local Artifact Paths checks, run:

```bash
python3 <package>/scripts/build_gallery.py build manifest.json --output <new-run-directory> --theme system
python3 <package>/scripts/build_gallery.py build manifest-v2.json --output <new-run-directory> --previous-key <old-run-directory>/answer-key.json --theme system
python3 <package>/scripts/build_gallery.py summarize ratings.json --key <matching-run-directory>/answer-key.json --output <new-evidence-directory>
python3 <package>/scripts/build_gallery.py summarize - --key <matching-run-directory>/answer-key.json --blind
```

Resolve `--theme` using HTML Output preferences before building. Output directories must be
new, under the checked ignored run path or an explicit destination. The executable refuses
symlink ancestors, existing destinations, and destinations containing an input file.
It relies on the preceding package-local Git exclusion checks, not a sibling import.
It embeds prepared files as data URLs in one offline HTML and also keeps neutral ASCII
`item-0001-slot-0001.ext` display copies. The answer key maps opaque tokens to original IDs,
names, item content fingerprints, private failures and seeded label order.
For chat-only aggregation, pass pasted JSON through stdin (`ratings: -`) and omit `--output`:
the command prints the validated summary without saving inputs or results. `--blind` replaces
key-derived identities with opaque IDs and anonymous candidate aliases; these aliases are not
the per-item shuffled display labels. Omit it only for an authorized identity disclosure.

For incremental builds, reuse `--previous-key`; IDs map to random opaque tokens, not hashes
of easily guessed model names. Adding/removing candidates reshuffles each item using the new
candidate set; unchanged content fingerprints preserve scores. Do not reuse a study ID for
an unrelated comparison. Keep the new key with the exported revision. If moving the HTML,
export/import ratings explicitly rather than assuming local-file storage follows the file.

## Additional public evidence

An output may include `annotation` (nonempty plain text) and `links`:
`[{"label": "Mobile capture", "path": "prepared/mobile.png"}]`.
Links accept prepared PNG/JPEG/WebP, HTML, TXT or PDF copies. Make linked HTML self-contained;
normalize document metadata, titles, scripts, alt text, embedded content and visible identity
cues before building. The builder checks literal candidate names/IDs in annotation, labels
and UTF-8 HTML/TXT contents (including decoded HTML entities). Binary metadata, PDF text,
encoded/pixel/semantic identity still needs manual inspection; compressed bytes are not text. Never supply raw producer HTML or the answer key as a public link.
Source filenames remain private; copied names use `item-NNNN-slot-NNNN-link-NNNN.ext`.

Image cards always link their neutral display copy at original size in a new tab. Keep the
HTML and display copies together for these local links; embedded primary media still works
when only the HTML is moved. Annotation is escaped text, not HTML. No source file is modified.
Legacy outputs without these fields retain the exact fingerprint algorithm. Adding/changing
public evidence changes that card's fingerprint, so old scores cannot silently apply to a
changed evaluation surface. Rebuilding unchanged evidence preserves it.


## Optional modes and split delivery

`build --mode gallery|versus --delivery single|split` defaults to `gallery` and `single`.
The options are independent. Versus uses the same prepared media/text manifest, opaque
identities, per-item seeded shuffle and evidence fingerprints. Read [versus](versus.md)
for interaction, export and replay rules. Do not create primary `kind: html` outputs:
use normalized screenshots plus explicitly prepared, identity-neutral, self-contained
HTML `links` for original inspection. The builder does not sandbox or recursively collect
HTML dependencies, execute producer pages, or traverse arbitrary linked files.

```bash
python3 <package>/scripts/build_gallery.py build manifest.json --output <new-run-directory> --mode versus --theme system
python3 <package>/scripts/build_gallery.py build manifest.json --output <new-run-directory> --mode versus --delivery split --theme system
python3 <package>/scripts/build_gallery.py build manifest.json --output <new-run-directory> --delivery split --theme system
```

Single delivery retains `gallery.html`, neutral display/link files and `answer-key.json`.
Default single-gallery rendering and rating schema are unchanged, including its legacy
encoded reveal mapping. Versus single delivery has no embedded mapping and requires a
separately selected matching key, like split delivery.

Split delivery writes `index.html`, `assets/item-NNNN-slot-NNNN.ext` and optional
`assets/item-NNNN-slot-NNNN-link-NNNN.ext`, `comparison.zip`, and separate `answer-key.json`.
The ZIP contains only `index.html` and the referenced neutral assets. It never includes the
answer key or an encoded candidate-name mapping. Inline theme/application assets need no
network request. Extract the ZIP before opening `index.html` via `file://`; do not open it
inside an archive viewer. Keep `assets/` beside `index.html`. Missing or modified extracted
assets require a fresh intact extraction and verification, not reuse of ratings for altered
material. The builder validates prepared inputs but does not continuously hash extracted files.

Distribute only `comparison.zip`, not the enclosing output directory. Keep the key private
until disclosure is authorized. `정답표 선택` reads an explicitly chosen key in memory and
checks study, version, every opaque output identity/fingerprint and failure state. It does
not reveal names by itself or save key contents to storage/exports. `결과 공개` is a separate
explicit action; partial comparison still asks for confirmation. A prior `revealed` flag is
history, never permission for the agent to disclose identities.

Choose split delivery on request or actual environment evidence, without a media-size cutoff
or invented explanation of a browser failure. Review the entire distribution, including linked
HTML, metadata and encoded/pixel/semantic cues. Styles can suggest techniques even when exact
names and mappings remain private. Packaging is not cryptographic anonymity or HTML sanitization.
