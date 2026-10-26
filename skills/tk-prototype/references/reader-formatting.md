# Reader Formatting

Use with clear writing when composing or revising explanatory prose. Clear writing owns
sentence meaning; these defaults own document hierarchy. Explicit reader requirements and
the calling owner's required evidence, warning or verification structure take precedence.

## Density and repetition

Keep sentences short, not the document: prefer one claim per sentence. Preserve needed scenarios,
early figures, summary boxes, causal steps and chosen understanding checks; remove repetition
instead. Summary boxes and checks remain optional under the caller's contract, never cut solely
for brevity. When a realistic situation motivates the topic, put it before the mechanism and
place the main figure beside it in reading order, without forcing horizontal layout.
Separate sentences in explanatory paragraphs with `<br>` in HTML; let each reflow naturally.
The summary identifies a point; the body develops its mechanism or evidence without copying it.
Omit irrelevant decisions and rejected work unrelated to the question.
Open with at most two short lede sentences and a compact account of the mechanism or decision.
Use lists for parallel points, without replacing causal explanation with fragments. When the
reader chooses between alternatives, include each option's main downside in the summary;
recommend one only when the deciding conditions are known. Preserve the caller's learning
objectives and required evidence rather than imposing a decision summary on every lesson.

After a substantive analogy, map its elements to actual actors, values or events in a compact
two-column `비유 | 실제` table and state where the analogy stops matching. A passing comparison
that adds no explanatory mapping needs neither an analogy nor a table.

## Visible priority

- Default to at most one bold conclusion sentence per section. Replace repeated
  `**Label**: explanation` list prefixes with plain sentences, or a table for shared attributes.
- Reserve inline code for literals the reader must copy, search or compare exactly. Merely mentioning
  a product, version or file does not require code styling; preserve exact technical spelling.
- Tables already separate attributes: omit decorative chips and repeated emphasis. Code or chips
  may distinguish exact cell values being compared (hashes, versions, keys) from explanations.
  Preserve meaningful status or warning distinctions.
- Use code blocks for executable commands, configuration and diffs. Do not combine emphasis,
  code and citation marks on ordinary sentences without a reader need. Audit authored `<strong>`,
  `<code>` outside `<pre>` and `<sup>` uses; remove weak signals, not evidence or required warnings.
- Citation placement and reference layout follow [HTML output](html-output.md); reducing marks
  must retain an unambiguous claim-source relationship.

Spend emphasis where it carries information. Badges, cards, dividers and numbering need a
semantic role; prefer spacing and typography to a badge per item or a card per section.
Tooltips supplement the visible explanation rather than carrying required definitions.

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

The supplied 2026-10-26 proposal was manually accepted once (`applied-once`). Its first comparative
skill run was rejected; the revised run awaits reader judgment. Do not label it `field-tested`.
Source verification and keep/adapt/omit decisions are in `sources.md`.
