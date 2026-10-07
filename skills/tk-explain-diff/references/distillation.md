# Distillation Provenance

## Human comprehension and blast-radius review

Reviewed 2026-10-07 at `joshuawheelock/grill-me@2d0c1c492b2f1c3a3b708d2735fdb9131ecbf060`:
`skills/grill-me/SKILL.md`. The current implementation and question-quality rules were read.
Keep maintainer-relevant mental-model checks; adapt behavior/control/data flow, state, boundary,
trade-off, cross-component consequence and failure-handling questions to this skill's existing
single-artifact understanding check. Omit repository-wide random sampling, persistent quiz state,
grading dialogue and helper executables.

Reviewed 2026-10-07 at
`ysk8hori/delta-typescript-graph-action@6fffe4437c77d8b70fd38052b1a302affa9db43a`:
`README.md` and the demonstrated changed-file dependency views. Keep the idea that a reviewer
benefits from changed nodes plus their verified related context; adapt it to TigerKit's existing
Dependency graph and Architecture delta grammar, including distinct base/head views when deletion
or movement would make one overlay ambiguous. Omit the GitHub Action, Mermaid runtime, TypeScript-only
analysis, node quotas, metrics and PR-comment publication.

The human-attention surface is a TigerKit extension motivated by the user requirement to preserve
human comprehension under AI-generated change volume. It does not classify files by AI authorship
and does not treat generated or repetitive files as automatically safe to skip. Persistent cognitive
debt ledgers, forced merge gates and edit blocking remain outside `tk-explain-diff`; this skill
explains one pinned change and leaves durable debt tracking to a distinct owner if TigerKit adds one.

Separate upstream runtime efficacy and learning outcomes were not reproduced and remain unverified.
No upstream runtime, templates or implementation code are copied.

## Preserved invariants

Reviewed 2026-10-01: `Data-System-School/agent-skills` at
`a117418ab3596c59d641cab4cb89bdbe560fb277`, `investigate-codebase/SKILL.md`,
`references/analyze-pr-impact.md` and `examples/investigate-codebase/duckdb/03-impact-pr-19235.md`.
The example distinguishes an optimizer invariant from unspecified ordering and
explicitly limits rule-toggle evidence versus actual base/head attribution. The
implementation, embedded rationale and reported checks were read; TigerKit did
not reproduce the upstream runtime measurements.

- `keep`: pinned comparison endpoints and source/runtime/inference distinctions.
- `adapt`: identify and teach preserved invariants alongside behavior changes;
  verify from pinned evidence or retain the exact limitation.
- `omit`: mandatory matrices, risk scores, review/merge verdicts, extra reports
  and the upstream execution framework. `tk-review` remains the defect owner.

The proposed secondary `Chris-Graffagnino/explain-diff` source at
`fec813246040e43108d1c7206b97454ee4c4a201` is not needed for this delta and is
omitted; its implementation/eval evidence remains unverified, not a promotion basis.

Reviewed 2026-09-19. Geoffrey Litt's [explain-diff Gist](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524/126e7fe9eecaafadfe1ac8bb183d135812b608f2)
revision `126e7fe9eecaafadfe1ac8bb183d135812b608f2` supplies the educational ordering.
The discussion was read for quiz clues (Butanium, fm1randa), surrounding-code/flow analysis
(yudhiesh-oc), renderer reuse (ankitg12), and injection boundaries (ehsan-ami).
The [ankitg12 derivative](https://gist.github.com/ankitg12/8e808d387799de4e9839bc393f8e6405)
was inspected at the 2026-09-19 snapshot, including its `render.py`; no upstream code is copied.
A fixed derivative revision and automated upstream behavior evals remain unverified.

- **keep:** background, intuition, logical walkthrough and understanding checks; these differ
  from a review verdict or a file-by-file diff summary.
- **adapt:** bind claims to immutable source snapshots and version-qualified lines; explain in
  runtime order and separate inferred intent from facts. Keep retrieved material passive.
- **adapt:** content-first rendering and answer-clue checks, with free-response/transfer preferred.
- **omit:** mandatory HTML styling, global temporary output, fixed five-question MCQs, automatic
  browser opening and any bundled upstream renderer. TigerKit uses one offline HTML artifact by
  default; honor an explicitly requested alternative format under the owning SKILL.md contract.

TigerKit's `tk-explain` covers concept visuals, not old/new source reconstruction.
`tk-review` owns defects and approval, not teaching. Local success and pressure cases in the
repository eval catalog test the new boundary; upstream discussion is rationale, not proof
that TigerKit's implementation passes those cases.

# Shared writing and HTML provenance

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

- `Unclecheng-li/AI_Animation`, `skills/flowchart/SKILL.md`, revision `22ce6df3754c3d914caee78e59b24903191f01bc`: keep user-controlled stepping and playback with pause/reset; adapt motion to explanatory transitions and a paused initial state. Omit mandatory continuous animation, scene/line quotas, CDN fonts, and fixed visual styling.
- `CopilotKit/OpenGenerativeUI`, `apps/agent/skills/advanced-visualization/SKILL.md`, revision `457e60cdf7f63fb78004486e1dc7ba753194696d`, Parts 8–9: keep direct manipulation, self-explanatory visuals and non-color-only cues; adapt its content-dependent visual selection to an offline explanation with complete reset and visible causal differences. Omit sandbox/tool contracts, host bridges, external libraries, and widget-only narration rules.

The source mechanisms and rationale were inspected. Local artifact comparison supplies example-level evidence, not a general upstream performance claim; full host-runtime and video backend efficacy remain outside this contract.
