# Document Assembly

Use this legacy shared document builder only when the owning workflow selects the shared
reader shell. It is not the default renderer for explanation/research pages or a fallback for
selected archify; independently authored technique HTML does not inherit its shell requirement.
For selected shared-reader documents, author fragments and run the installed `tk-writing` builder.
Reuse generators for edits; specialized prototype/QA/gallery interfaces keep their generators.

Put fragments in authorized run scratch. The body contains the opening explanation and
`<section id="..."><h2>...</h2>...</section>` units with appropriate nested heading levels.
The builder supplies title/h1, topbar, reader controls, hierarchical TOC, movement links
and unchanged theme assets. Do not read/reproduce these assets merely to inline them;
inspect implementations only for a concrete defect/change.

```bash
python3 <tk-writing>/scripts/build_html.py --body <scratch>/body.html --title '<subject>' --output <final>.html
python3 <tk-writing>/scripts/package_html.py --root <final-directory> --name <filename>.html <filename>.html
```

Resolve `<tk-writing>` to that owner in the current installed collection, not the caller or a source checkout. Keep scratch and final output outside installed packages, and use an existing output directory. `--replace` requires overwrite authority.
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

## Reader compatibility

`--profile reader` is the only supported profile and remains the default; navigation stays
hierarchical. The former `lesson` and `change` builder choices had no bundled assets and
could not build documents; they are removed, not replaced by a fallback. This does not
change `tk-explain`'s workflow modes or its selected renderer.
