# Change walkthrough HTML

For a nonempty change, pin and inspect source as the skill requires, build the validated v1
model and supplied source bundle, and follow [grouping](change-grouping.md). Build with the
package-local adapter, then package the resulting HTML:

```bash
python3 <package>/scripts/build_change.py --model <scratch>/change.json --sources <scratch>/sources.json --intro <scratch>/intro.html --outro <scratch>/outro.html --output <artifact>.html --theme system
python3 <package>/scripts/package_html.py --root <artifact-directory> --name <artifact>.html <artifact>.html
```

`--intro` and `--outro` are optional reviewed fragments for background and understanding
checks; they must not add navigation units or duplicate model facts. Shared fragment checks
reject missing or duplicate anchors, forbidden structure and reserved IDs. `--theme`, `--lang`
and explicit `--replace` follow the common builder. Validate before output or preference writes.
Use actual snapshot IDs, source-bound evidence, uncertainty and the existing output path and
independent content-review contract. A successful model check is not a runtime or semantic verdict.

The change profile presents one continuous document: purpose and snapshot, logical groups,
side-by-side before/after on wide screens and sequential reading on narrow screens, claims and
canonical source excerpts. Group navigation uses only marked top-level group sections. Each claim
and group links to source evidence, whose numbered return links identify each origin. Copyable
code comes from the validated source bundle via the shared highlighter; metadata and unavailable
sources are labeled, never fabricated. Required content is visible without JavaScript. Optional
flow controls highlight one readable step at a time, stay stopped by default, and never hide the
list. They do not claim observed execution. Evidence, IDs and labels are escaped; source strings
are never evaluated. Preserve no-JS reading, native anchors, hash history, Find, print, reduced
motion, light/dark, 50-200% font scaling and offline export. Do not add a server, account, runtime
editor, autoplay, review decision or external runtime dependency.

For implementation regression verify model errors and output preservation, exact source text,
unique IDs and local targets, shared-evidence returns, graph-less and unavailable cases, export,
flow controls and keyboard/hash behavior at wide/narrow viewports. Separate unavailable browser
checks from passing static checks. Normal explanation calls retain the existing opt-in browser
verification rule; changing this renderer does not impose browser verification on every artifact.
