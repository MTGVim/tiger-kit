# Provenance

Maintenance record for upstream distillation; not part of the skill's reading path.

## clear-writing.md

- `docwriter-org/plain-writing-skill`, `f0d3630983ac7a82aa580f1c1509d72df739ee12`: relevant background, concrete subjects, coherent explanation, consistent terminology. Rules 3 and 15 also inform the Korean empty-emphasis and middle-dot requirements; adapt them to supported specifics and protected literals, without importing unrelated formatting bans.
- `hjongc/humanizer-kr`, `a1a7069a32f669afe4b10e35e9522ff504a13263`: reader/register fit, contextual editing, restrained claims, internal naturalness review.
- `snflkd/fluent-korean`, `ce8683f0eba8cddb91de4dcd151425ff73e60498`: Korean sentence components, particles/endings, accurate vocabulary, literal-expression boundaries. This is a selective adaptation with rationale and examples, not a replacement for the upstream global output style.

- `evergreentree97/K-Humanizer`, `324435d561ba48d53de6b7d3fb3dd72cf77030dc`: preserve useful paragraph links without inventing relationships.
- `epoko77-ai/im-not-ai`, `9747f036cdc28a1a8aea4dc71fef1f7846eb96f7`: contextual strength, selective density-based editing, avoiding newly introduced style defects, and conservative correction when empirical evidence contradicts a presumed pattern. Taxonomy, authorship judgments, and numeric thresholds are not imported.

- `conorbronsdon/avoid-ai-writing`, `c4783463cf019a8943364c1ef5f80e0a4c8bff94`: candidate-to-justified-edit scope, preservation of unaffected passages, and valid zero-edit outcomes; no detector, taxonomy, pass budget, or public audit trail is imported.

- `conorbronsdon/avoid-ai-writing`, `5dd2e4ab72b9e0b7e125e5cb592af87033da4fda` (compared with `9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43`): separate mechanical and semantic preservation, equivalent numeric notation, and honest incomplete verification. Keep the two internal passes and one final result; adapt only these safeguards. Omit the upstream validator, detector, handoff envelope, repair budget, and public verification report.

Style-sample factual boundaries also draw on `addyosmani/clarity`,
`e27ceeff60368cf6966b4ea00a5b9b36418ee9a0`: `SKILL.md`, `references/edit.md` and
`evals/cases.json` (`voice_sample_controls_style_not_facts`). Keep truth preservation;
adapt expression-only sample use; omit co-writing, detectors and public review reports.
Project familiarity is an independently authored extension of the existing audience/context
contract, not a claim of a verified upstream project-familiarity rule.

Original MIT notices are in the calling package's `LICENSE.txt`.

Evaluative intensity versus certainty draws on `dotoricode/korean-humanizer`, `4fc566b7d7ded76887f7a85c0886e44796e5e38c` (`references/ko-ai-signals.md` and native-skill QA). Concession preservation draws on `conorbronsdon/avoid-ai-writing`, `bdeb726580634868b254972d8eab1a9340d9db16` (`FALSE_CONCESSION`, PR #359 and its fixtures). Adapt semantic preservation and must-not-overcorrect cases; omit detector regexes, taxonomy, output templates and runtime tooling.

Claim-evidence binding also draws on `AIScientists-Dev/academic-humanizer`,
`94b88b23703bed7df507acae7d6d5876209a0cdf`; evidence addition, academic taxonomy and venue rules are omitted.

Meaningful modality also draws on `epoko77-ai/im-not-ai`,
`92b2936956d65d62ff4b19b75cccad8e3429bf43`: A-10/G-2 and their correction history motivate preserving claim strength even under repetition. Apply semantic equivalence across genres; omit domain-only exceptions, fixed repetition thresholds, hedge dictionaries, marker counts, and runtime restoration.

Rewriting-only scope draws on `dotoricode/korean-humanizer`, `93580567d4c965024e5b9eb1fb96ace3e7b45907` (`SKILL.md`, PR #6 and package-skill QA). Adapt the editing-only boundary while preserving explicitly requested advice; omit fixed output sections and distribution/runtime tooling.

## html-output.md

Live-figure provenance (2026-10-05): `nicobailon/visual-explainer` at
`5846f5aef34a23c8fea389d2f23ce56224cbf840`, `plugins/visual-explainer/SKILL.md`,
`references/diagrams.md` (Live figure) and `templates/page.html` under that package.
Keep lightweight interaction and readable static state; adapt shared pure-model
calculation, small controls, verified defaults and simplified-model disclosure.
Omit upstream templates, external dependencies, forced figure-first presentation
and automatic opening. Separate upstream behavior evals and runtime efficacy are
unverified; the calling package's `LICENSE.txt` preserves the MIT notice.

## interactive-examples.md

Sources inform behavior; their runtime and stylistic instructions are not dependencies or authority.

- Live-figure selection (issue #460): rechecked `nicobailon/visual-explainer` at
  `5f378868e0ea745a6284b51e710c390f0c76f72c`, `plugins/visual-explainer/SKILL.md`
  (figure selection), `references/motion.md` (Live figure), and `eval/` methodology,
  prompts and judge. Keep parameter-driven consequences; adapt selection examples
  to the existing static/step-through boundary. Shared calculation, small controls,
  assumptions and static fallback already belong to `html-output.md` and existing
  evals; do not duplicate them. Omit kit, renderer, templates and figure-first
  defaults. No live-figure-specific upstream behavior eval or efficacy result was
  found; upstream runtime efficacy was not reproduced. Existing MIT notice applies.

- `Unclecheng-li/AI_Animation`, `skills/flowchart/SKILL.md`, revision `22ce6df3754c3d914caee78e59b24903191f01bc`: keep user-controlled stepping and playback with pause/reset; adapt motion to explanatory transitions and a paused initial state. Omit mandatory continuous animation, scene/line quotas, CDN fonts, and fixed visual styling.
- `CopilotKit/OpenGenerativeUI`, `apps/agent/skills/advanced-visualization/SKILL.md`, revision `457e60cdf7f63fb78004486e1dc7ba753194696d`, Parts 8–9: keep direct manipulation, self-explanatory visuals and non-color-only cues; adapt its content-dependent visual selection to an offline explanation with complete reset and visible causal differences. Omit sandbox/tool contracts, host bridges, external libraries, and widget-only narration rules.

The source mechanisms and rationale were inspected. Local artifact comparison supplies example-level evidence, not a general upstream performance claim; full host-runtime and video backend efficacy remain outside this contract.

## Document navigation (2026-10-07)

Reviewed `EveryInc/compound-engineering-plugin@142dbabc23c86884f2e353502eb20a5fdd2a6d3d`,
`skills/ce-ideate/references/html-rendering.md` (navigation/self-contained invariants) and
`docs/plans/2026-05-11-001-feat-output-html-mode-plan.md` (single-file and package-local
copy rationale). Adapt semantic sections, sticky/compact native navigation, hashes and details;
omit donor templates/styles, CDN fonts, default tracked commits and orchestration. Runtime
efficacy was not reproduced. The canonical contract is `tk-explain/references/html-output.md`;
installed copies are synchronized and the MIT notice is in this package's `LICENSE.txt`.

## HTML quality extension (2026-10-07)

The supplied recurring-artifact proposal and TigerKit baseline `56c8a50603bd1649465a74b2e8af373a0e51a8a9`
provide explicit reusable intent and inspectable contract/template gaps. Keep offline reading and
hash navigation; adapt neutral QA theme structure and whole-project projections; omit domain-specific
scripts and raw session details. The reported proprietary `dataviz` bundle is reference-only:
no wording, code, palettes or validation script is included. Its distribution/license and upstream
behavior were not independently verified here; the general chart rules and neutral tokens are
independently authored. Runtime/provider observations remain conditional, not compatibility claims.

## Verification outcome structure (2026-10-13)

The inspected report-generation incident and explicit reusable-output request establish the gap:
final status injection merged static success and unavailable screen verification into one plain
paragraph. W3C WAI [Content Structure](https://www.w3.org/WAI/tutorials/page-structure/content/),
retrieved 2026-10-13, supports semantic paragraphs and separate list items for related information.
Keep semantic grouping; adapt independently authored bold check labels and a lower-document summary
to the user's scanning needs. Omit upstream example content, styles and runtime machinery. The WAI
guidance does not itself mandate bold labels or summary placement. Template markup and mutation
checks establish structural protection only, not browser rendering or model compliance rates.

## Content-only document assembly (2026-10-25)

Reviewed current `nicobailon/visual-explainer@5f378868e0ea745a6284b51e710c390f0c76f72c`:
`plugins/visual-explainer/SKILL.md`, `templates/page.html`, and `eval/README.md`; also
`mattpocock/skills@5beb35b040e3de97e54fa9e386d7e42d15c295c2`,
`skills/productivity/teach/SKILL.md` (Assets and scoped lessons). The implementation and
embedded design rationale favor local asset injection, reuse and small source edits; the
visual-explainer evaluation separates correctness from token use. Upstream runtime and
end-to-end timing were not reproduced.

- **keep:** local insertion of shared presentation, reusable semantic components, source edits.
- **adapt:** an independently authored stdlib builder and shell under the existing offline
  HTML, settings, export and browser-verification contracts. Default it only for new ordinary
  explanation/lesson documents; retained generators and specialized interfaces keep ownership.
- **omit:** donor kit/code/templates, external fonts/CDNs, automatic browser opening,
  figure-first/prose quotas, extra Markdown, consumer runtimes and render-check exemptions.

TigerKit's gap was executable shell assembly: it already supplied CSS/JS and navigation
markup instructions, but agents still had to construct that markup and inline assets.
Reduced authored markup is an observable mechanism, not an end-to-end speed claim.
The current user request explicitly preserves one-step HTML and content/verification quality.

## Independent artifact review and recognition/action coverage (2026-10-26)

Reviewed current `mattpocock/skills@5beb35b040e3de97e54fa9e386d7e42d15c295c2`
(`skills/productivity/teach/SKILL.md`, retained in context and main identity rechecked) and
`obra/superpowers@2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`
(`skills/requesting-code-review/SKILL.md`, `code-reviewer.md`). The latter's implementation
and rationale use fresh reviewer context, inspected evidence, severity and correction before
proceeding. A separate upstream content-review eval was not established; a tests/README.md
lookup was unavailable, and upstream runtime/learning efficacy were not reproduced.

- **keep:** scoped teaching goals, complete worked material and evidence-based independent review.
- **adapt:** the current explicit user workflow to one read-only adversarial content reviewer,
  current-artifact identity, goal-blocking omissions, repair/re-review and honest unavailable
  execution. Teach recognition inputs, spatial actors/routes and exact pre-reveal question state.
- **omit:** code-review/merge verdicts, Git-range templates, author assessments as reviewer context,
  orchestration runtime, new skills, reviewer cascades, stylistic quotas and mastery inference.

Earlier causal prose, spatial-layout coverage, verifier preflight and inline references already
exist and are retained. Browser checks now require explicit user scope for explanation/lesson
production; separately requested checks retain the existing provider/evidence/safety contract.
Other HTML owners keep their scoped UI checks. Source checks and content review remain required.
The instructions and fixtures are independently authored; no donor code/template is copied.

## Reader formatting and bounded figures (2026-10-26)

The original reader-formatting bundle documents repeated feedback on one explanation and a
manual `applied-once` result. A subsequent supplied comparison reports that the reader preferred
the control to the first skill run. Its revised run restored context, an early figure and a check,
but reader comparison remains pending. Shortening as a cause is a supported hypothesis, not an
isolated causal result. Keep `applied-once`; do not promote this evidence to `field-tested`.
The grid overflow hypothesis was checked separately with a 360px wide-SVG baseline/replay.
Neither result establishes reader comprehension or end-to-end speed.

Reviewed GitHub Docs' `Troubleshooting content type` and `LICENSE` at
`github/docs@564868161b9cd8bb75f789079690fb44a4a5149d`
(`content/contributing/style-guide-and-content-model/troubleshooting-content-type.md`,
CC BY 4.0, https://creativecommons.org/licenses/by/4.0/). GitHub's content distinguishes
known issues from broader troubleshooting and gives category-based titles. The four-way
Korean supporting-section taxonomy is independently adapted from the supplied proposal;
it is not a GitHub mandate. No upstream prose, implementation or template is copied.
A separate upstream evaluation was not established.

- **keep:** concrete causal explanation, independent content review, exact identifiers when needed,
  public source provenance, required warnings/verification structures and offline output.
- **adapt:** sparse emphasis, sentence breaks, category headings, visible figure boundaries,
  package-local synchronized reference copies, safe grid shrinkage and two logical reference rows.
  Shortness applies to sentences: retain needed scenarios, early figures, causal steps, selected
  summaries/checks and exact comparison values. Put a motivating situation before the mechanism
  with the main figure nearby in reading order; preserve responsive layout and optional checks.
  This reconsiders the older single-line reference default; natural multi-line wrapping remains.
  Immediate citations may be reduced only when exact supported sections/claims remain identifiable;
  research's checker-owned citation/backlink coverage is unchanged.
- **omit:** copied private examples, hard two-physical-line limits, blanket code bans in tables,
  uncertain external license claims, broad writing-rule duplication and new document runtimes.
  A mandatory summary box and a stricter opening-sentence rule remain unverified proposals;
  do not add those defaults from this single comparison.

Only the GitHub primary text and license above were verified here. The bundle also names Google
Cloud, Red Hat, Oracle and Splunk as concept-level influences; their pages, exact editions and
licenses were not verified in this change, and no content from them is incorporated.
