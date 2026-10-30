# Optional contact sheet

Read only when an overview of already indexed captures is explicitly requested. Keep this
opt-in until a real comparison demonstrates useful navigation savings. This branch never
starts a browser, expands verification scope, installs a dependency or uploads anything.
Ordinary explain/diff/teach HTML creation retains its explicit browser-request boundary.

Use only captures owned by the current approved run, reviewed as non-sensitive after the
existing pre-capture mask/clip policy. Never compose a sensitive original or an unreviewed
image. Labels must also be publication-safe; omit account details, origins and query values.
The helper cannot detect secrets in pixels: `safe_for_sheet` records the verifier's completed
safety review, not an automatic redaction claim.

In the existing evidence `README.md`, add one fenced `contact-sheet-captures` block containing
a JSON array in capture order. This is an optional view of the same capture index, not a second
manifest or state ledger. Every row uses exactly these keys, for example:

```contact-sheet-captures
[
  {"path":"baseline/form.png","criterion_id":"BV-001","phase":"baseline","state_region":"form light","viewport":"1440x900","safe_for_sheet":true},
  {"path":"after/form.png","criterion_id":"BV-001","phase":"after","state_region":"form light","viewport":"1440x900","safe_for_sheet":true}
]
```

Run the installed package's `scripts/contact_sheet.py --run-dir <absolute-run-directory>`.
It uses optional existing Pillow, with no browser/canvas dependency or external service.
Only ignored, untracked `.tigerkit/evidence/tk-browser-verify/<run-id>/` directories are accepted.
Use concise ASCII labels (64 characters per metadata field, 160 for paths); retain complete
human-readable provenance in the ordinary index. Paths must point to indexed PNGs under their
matching `baseline/`, `after/` or `failed-<attempt>/` phase. Keep paired replay parity explicit
in the ordinary index; placing two thumbnails together does not establish comparability.

The helper makes at most four tiles per sheet, preserves order and aspect ratio, links every
tile to its original in the same README and creates unique outputs without overwriting files.
It bounds input count/size and rejects unsafe paths, symlinks, sensitive flags and corrupt images.
Zero/one capture is skipped; `--single` is only for an explicit one-capture request. Missing
Pillow, invalid input or composition failure skips this optional view. Record that skip in the
existing README, preserve originals and verdicts, and continue ordinary verification. Do not
automatically install a tool, switch provider, rerun the browser or invent an acceptance failure.

Inspect the generated sheet through the image tool to navigate, then inspect each required original through the existing
image tool. Preserve `reread-image`, ordered capture/criterion rows, immutable failure evidence
and per-AC verdicts. A sheet is not a PR acceptance image or proof of readable text, exact geometry,
interaction or regression absence. Do not infer a Pass from thumbnails. Report only measured
navigation/composition cost; synthetic images do not establish real-work speed improvements.
