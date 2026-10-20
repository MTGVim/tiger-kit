# Optional ppaso narration

Read only when narration is explicitly selected. The isolated module is
`scripts/narration/ppaso.py` plus `ppaso-files.json`; the sole runtime pointer is in
SKILL.md. Remove those files, this reference and that pointer to remove narration; in the
source repository also remove its dedicated `scripts/test_optional_narration.py`. Retain the
assembler's no-narration regression.
No other verifier, prep, uploader or movie assembler imports this module. Subtitles, GIF,
MP4 and screenshot/assertion verification must still work without it or its dependencies.

Use ppaso v1 ONNX CPU at revision `53d09664c4f636a5fb6f2ebe3ec22cd83ee249b9`.
The JSON manifest pins full SHA256 for every required model, inference, config, dictionary,
license and attribution file. Require an exact snapshot file set and reject extra flat model
overrides, package initializers, bytecode or symlinks. Use a fresh process; the adapter binds
the runtime namespace and PPASO_LEXICON to the verified snapshot so ambient packages or
dictionary settings cannot override it. Verify actual bytes before executing inference code; a tag,
prefix, Git LFS pointer or arbitrary local directory is insufficient. Prefer an already
verified local snapshot; never depend on a personal/private mirror being publicly accessible.
Model files and binaries are not part of TigerKit's Git history or Releases.

On macOS/Linux, inspect installed `onnxruntime numpy soundfile python-mecab-ko`. If missing,
propose one run-owned virtual environment and its exact dependencies/model download, and reuse
matching user approval before installing. No global pip, cache or automatic installation is
authorized by selecting media. Put the environment, pip/HF caches and model snapshot under
the safe run-owned temporary directory. Windows is outside this module's support scope.

After download approval, run `ppaso.py --model-dir <run-owned-dir> --download --verify`.
Without `--download` it never accesses the network. A verified offline copy uses the same
manifest. Keep LICENSE and README_ko.md attribution, including MFA dictionary MIT and mecab-ko BSD
notices; do not package unrelated example avatars. Upstream unavailability omits narration and
continues the selected captioned MP4. Do not publish a new snapshot/release without separate authority.

Write the approved script in a run-owned UTF-8 text file; use `--text-file <file> --output <wav>`.
Optional `--user-dict <json>` maps exact terms to Korean pronunciations. Normalize numbers/English
in the authored script while preserving original UI literals in evidence and captions. The module
checks decodable, finite, nonempty, nonsilent audio. Listen to a representative sample for names,
numbers, clipped endings and meaning; determinism is not proof of correct pronunciation.
No ASR round trip or Whisper download is required. Bind captured-state claims to observed states; identify authored diagrams and concept explanation
as rendered scenes. Do not narrate an unobserved application outcome as fact.

Pass an accepted WAV to the independent assembler's generic full-track `--audio` input, or use
per-scene `audio_path` in `explainer`. Presentation holds may follow measured speech. For an
observed evidence timeline, retain subtitles and report omitted audio when it does not fit;
never cut speech, invent observed waiting time or silently change a timing claim. Retain an explicitly requested
but undelivered narration limitation. Clean only known run-owned temporary resources and report
residue; this module changes neither application acceptance nor screenshot publication.
