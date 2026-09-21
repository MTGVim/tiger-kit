# Distillation Provenance

Reviewed 2026-09-19 at Matt Pocock skills revision
`c55ee46073ed923f86ce59a5eb3b6d895095d1b7`:
[teach](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/teach/SKILL.md)
and [research](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/research/SKILL.md).
Both implementations and their inline rationale were read. Separate upstream behavior evals
were not verified. This is independent distillation, not copied code or a workspace framework.

- **keep:** a practical learning goal, trustworthy sources, level-appropriate examples,
  retrieval, feedback based on actual answers, and reusable terminology.
- **adapt:** scoped courses retain curriculum, sources and chapters; interviews also retain a
  topic-local learner profile. Prior records require topic, goal and provenance checks.
- **adapt:** research becomes a prerequisite-aware course rather than a recommendation report.
  Rendering follows teaching design; `.tigerkit/study/` owns automatic output.
- **omit:** mandatory mission interviews, root-level workspace scaffolding, automatic browser
  launch, default background dispatch and rigid HTML/quiz formats.

`tk-research` owns decision support; `tk-explain` owns a known concept visualization;
`tk-learn` authors skills. Neither subsumes unfamiliar-topic research followed by teaching
and observed retrieval feedback. Repository evals cover this distinction and unavailable sources.

## Course redesign (#375)

Reviewed `lowwwbank/anything-to-course` at `f11bbf21572a9864759929946c2c3da6857e1744`:
`SKILL.md`, `references/course-blueprint.md`, `references/practice-design.md` and
`references/quality-rubrics.md` provide implementation, rationale and author quality criteria.
Separate executable behavior evals were not found; learning-outcome efficacy was not reproduced.

- **keep:** capability-based curriculum, dependency order, first-use definitions, retrieval,
  transfer and feedback separated from attempts.
- **adapt:** fading support, cumulative checkpoints and spaced retrieval fit the actual course
  scope rather than fixed module/question counts. A bounded reconnaissance pass and learner-owned
  questions select a deeper research pass. Interview profiles stay topic-local under `.tigerkit/`.
- **omit:** mandatory sample-lesson approval, fixed review offsets, automatic tutoring invitation,
  global progress and wholesale course scaffolding.

Reviewed `MisterBrookT/vividoc` at `32c7cf963e90c06b00143330f2ad5c6e2366b549`:
`docs/method.md`, `prompts/executor_prompt.py` (text and interaction stages), and `docs/eval.md`.
The evaluation design separates content quality from render/interaction correctness; upstream
benchmark results and runtime execution remain unverified, not evidence of TigerKit performance.

- **keep:** content-led visual interaction and separate content/render verification.
- **adapt:** one offline HTML artifact with chapter anchors and keyboard-accessible answer reveals
  through the canonical `tk-explain` HTML reference, synchronized into each installed package.
- **omit:** provider pipeline, style planner, fixed knowledge-unit count, server/runtime and
  external renderer dependencies. No upstream code or templates are vendored.

The existing `tk-grill` question frontier informs prerequisite-aware scoping only; its separate
shared-understanding gate and product-decision workflow are not imported. `tk-explain` remains
focused; `tk-explain-diff` retains exact comparison evidence while sharing HTML conventions.
