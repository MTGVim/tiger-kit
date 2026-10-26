# Reader Formatting

Use with clear writing when composing or revising explanatory prose. Clear writing owns
sentence meaning; these defaults own document hierarchy. Explicit reader requirements and
the calling owner's required evidence, warning or verification structure take precedence.

## Density and repetition

Prefer one claim per sentence. Open with what happens, why and its consequence in a short
paragraph; preserve prerequisite and causal steps before cutting length. In multi-sentence
explanatory paragraphs, separate sentences with authored line breaks (`<br>` in HTML),
without fixed-width lines or splitting a sentence. Let each sentence reflow on narrow screens.
The summary identifies a point; the body develops its mechanism or evidence rather than
copying the summary. Omit irrelevant decisions, including rejected work unrelated to the question.

After a substantive analogy, map its elements to actual actors, values or events in a compact
two-column `비유 | 실제` table and state where the analogy stops matching. A passing comparison
that adds no explanatory mapping needs neither an analogy nor a table.

## Visible priority

- Default to at most one bold conclusion sentence per section. Replace repeated
  `**Label**: explanation` list prefixes with plain sentences, or a table for shared attributes.
- Reserve inline code for literals the reader must copy or search exactly. Merely mentioning
  a product, version or file does not require code styling; preserve exact technical spelling.
- Tables already separate attributes: omit decorative chips and repeated emphasis. Keep code
  where an exact identifier is necessary, and preserve meaningful status or warning distinctions.
- Use code blocks for executable commands, configuration and diffs. Do not combine emphasis,
  code and citation marks on ordinary sentences without a reader need. Audit authored `<strong>`,
  `<code>` outside `<pre>` and `<sup>` uses; remove weak signals, not evidence or required warnings.
- Citation placement and reference layout follow [HTML output](html-output.md); reducing marks
  must retain an unambiguous claim-source relationship.

## Supporting headings

Name one category per supporting section: `제한 사항` for functional boundaries,
`알려진 문제` for confirmed defects and workarounds, `주의 사항` for surprising behavior and
its reason, or `확인하지 않은 항목` for unverified claims and the deciding check.
Replace vague headings ending in `것` with the actual category; split mixed categories.
For example, replace `도입하고 나서 신경 쓸 것` with the applicable named sections.
Main explanatory headings still name the actual mechanism or subject; do not force these
supporting categories onto the whole document or create empty sections.

## Figure boundaries

Frame a composed explanatory figure, caption included, with one thin token-colored border
so its full extent is visible. Use `.ht-figure` on the owning `<figure>`; do not frame only
one inner row unless that box has a distinct meaning. Label each meaningful lane, row or panel
visibly, not only in SVG metadata or the caption. Reuse one box style for one meaning.
The shared stack keeps children shrinkable; retain a bounded inner scroller for wide figures.
Do not add nested decorative frames around tables, ordinary prose or every section.

## Provenance

Adapted from the supplied 2026-10-26 reader-feedback proposal. Its formatting rules were
applied manually to one accepted output (`applied-once`), not exercised by a fresh skill run.
Reference layout and citation bindings remain owned by HTML output, not a second rule set.
Public-source verification and keep/adapt/omit decisions are in `sources.md`.
