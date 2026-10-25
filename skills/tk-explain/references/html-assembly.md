# Document Assembly

For new document-like HTML, author content fragments and run the package-local builder.
Reuse generators for edits; specialized prototype/QA/gallery interfaces keep their generators.

Put fragments in authorized run scratch. The body contains the opening explanation and
`<section id="..."><h2>...</h2>...</section>` units with appropriate nested heading levels.
The builder supplies title/h1, topbar, reader controls, hierarchical TOC, movement links
and unchanged theme assets. Do not read/reproduce these assets merely to inline them;
inspect implementations only for a concrete defect/change.

```bash
python3 <package>/scripts/build_html.py --body <scratch>/body.html --title '<subject>' --output <final>.html
python3 <package>/scripts/package_html.py --root <final-directory> --name <filename>.html <filename>.html
```

Use resolved paths and an existing output directory. `--replace` requires overwrite authority.
Optional UTF-8 `--css`, `--script`, `--footer` files supply content-scoped styles, reviewed offline
figure code and provenance markup. Escape source/code and closing script/style sequences.
`--lang` changes language; `--theme` honors an explicit theme, otherwise settings resolve/bootstrap
per HTML Output. Carry printed creation/fallback notes into the receipt. Linked lessons use the
final collection export allowlist instead of the single-file command above.

Preflight checks fragment balance, section headings, IDs/targets and summary placement;
it is not full static/offline validation or a prose/render/learning verdict. Preserve all
owning content/source/practice and HTML Output checks. The composed shell still triggers
browser verification. Finalize content before the matrix; batch compatible checks in one
browser session, execute all exposed actions and reuse evidence under existing replay rules.
Edit fragments and rebuild affected outputs.
