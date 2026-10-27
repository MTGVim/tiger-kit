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

Preflight checks fragment balance, section headings, IDs/targets and summary placement,
and warns about classes absent from the shared theme;
it is not full static/offline validation or a prose/render/learning verdict. Preserve all
owning content/source/practice and HTML Output checks. A composed shell alone does not request
browser verification for explanation/lesson production. When screen/action checks are explicitly
requested, finalize content first, batch compatible checks and preserve existing replay rules.
Edit fragments and rebuild affected outputs.

## Presentation profiles

`--profile reader` is the default and preserves the existing reader. The closed choices
`lesson` and `change` use only the corresponding package-local shell, CSS and JS. Missing
assets fail before theme settings or output are changed; there is no reader fallback.
Only top-level sections marked `data-ht-nav-unit` become lesson/change navigation units;
at least one is required and markers cannot be nested. Reader navigation remains hierarchical.
Profile assets are injected after shared theme assets and before optional authored code.
The resulting `data-ht-profile` identifies presentation, not an in-page mode switch.
Specialized shells use `data-ht-document`, `data-ht-content`, `data-ht-section-nav`,
`data-ht-section-disclosure` and `data-ht-section-links` for shared behavior without
reusing reader geometry classes.
