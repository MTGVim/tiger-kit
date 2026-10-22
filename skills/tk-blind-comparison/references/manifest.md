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
  "items": [{"id": "sentence-01", "description": "같은 문장을 듣고 발음과 자연스러움을 평가해 주세요."}],
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
The helper checks literal names/IDs in shared labels and text; inspect logos, spoken names,
watermarks and other semantic cues manually. It cannot establish semantic anonymity.

After the package-local Artifact Paths checks, run:

```bash
python3 <package>/scripts/build_gallery.py build manifest.json --output <new-run-directory> --theme system
python3 <package>/scripts/build_gallery.py build manifest-v2.json --output <new-run-directory> --previous-key <old-run-directory>/answer-key.json --theme system
python3 <package>/scripts/build_gallery.py summarize ratings.json --key <matching-run-directory>/answer-key.json --output <new-evidence-directory>
```

Resolve `--theme` using HTML Output preferences before building. Output directories must be
new, under the checked ignored run path or an explicit destination. The executable refuses
symlink ancestors, existing destinations, and destinations containing an input file.
It relies on the preceding package-local Git exclusion checks, not a sibling import.
It embeds prepared files as data URLs in one offline HTML and also keeps neutral ASCII
`item-0001-slot-0001.ext` display copies. The answer key maps opaque tokens to original IDs,
names, item content fingerprints, private failures and seeded label order.

For incremental builds, reuse `--previous-key`; IDs map to random opaque tokens, not hashes
of easily guessed model names. Adding/removing candidates reshuffles each item using the new
candidate set; unchanged content fingerprints preserve scores. Do not reuse a study ID for
an unrelated comparison. Keep the new key with the exported revision. If moving the HTML,
export/import ratings explicitly rather than assuming local-file storage follows the file.
