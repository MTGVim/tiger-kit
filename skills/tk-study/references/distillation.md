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
- **omit:** at this snapshot, mandatory mission interviews; see the scoped reassessment below.
  Root-level workspace scaffolding, automatic browser
  launch, default background dispatch and rigid HTML/quiz formats.

`tk-research` owns decision support; `tk-explain` owns a known concept visualization;
`tk-learn` authors skills. Neither subsumes unfamiliar-topic research followed by teaching
and observed retrieval feedback. Repository evals cover this distinction and unavailable sources.

## Course mission alignment (#416)

Reviewed 2026-10-05 at `mattpocock/skills` revision
`24fe0ef7737efae15c87225755e9f6f5965e4888`,
`skills/productivity/teach/SKILL.md` (The Mission) and `MISSION-FORMAT.md`.
Both the current implementation and the rationale connecting mission to teaching
choices were read. Separate upstream behavior evals and learning efficacy remain
unverified. This reassessment supersedes only the old mandatory-interview omission.

- `keep`: capability-led goals, explicit constraints/exclusions and teaching tied to the mission.
- `adapt`: a default mission-alignment round for a new dependent-chapter course;
  current explicit answers satisfy it, no fixed questionnaire or extra confirmation follows.
  Save the mission and declared versus demonstrated knowledge with provenance in
  the existing topic-local curriculum/profile, then connect it to prerequisites and checks.
- `omit`: a mandatory interview for explicit short/no-interview requests, focused
  explanations or identity-verified continuation; never invent agreement when skipped.
  Retain existing omissions of root workspace scaffolding, automatic opening,
  background dispatch and rigid lesson formats.

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

## Finite corpus coverage (#380)

Reviewed `Lum1104/video-to-skill` at `5e9f97e89855a8a0ea998ba85e179fbc1765d4b7`:
`docs/ambitious-startups-v1-v2-product-audit.md` and `docs/generated-skill-v2.md`.
The artifact audit separates source retention from instructional quality; the current design
requires explicit dispositions and reasons. Upstream runtime/eval execution was not reproduced.

- **keep:** material source omissions must be visible and completeness claims evidence-bounded.
- **adapt:** record source-level dispositions only for a user-specified finite set in existing
  `sources.md`; retain the open-ended research path and useful partial teaching.
- **omit:** semantic-unit ledgers, evidence database, compiler, IDs, manifests and coverage metrics.

TigerKit fixtures independently cover unavailable, partial, intentional omission, complete-corpus
and open-ended cases; no upstream implementation or fixture is copied.

## Executable exercise discrimination (#386)

Reviewed `matlab/agent-skills-playground` at `7b14a7756bf2765a31840699bc27c8d7240083ac`:
`demos/course-generation/skills/matlab-create-course-activity/references/matlab-validation-rules.md`,
`demos/assessment-generation-for-matlab-grader/evals/README.md` (EV-G3, G4, G7, G9),
and merged PR #26 (`3fc3d57a1568d0dcf8f9b59b5186accdb075e779`). The implementation,
PR design rationale and scenario criteria were inspected; upstream MATLAB execution is unverified.

- **keep:** a passing reference alone does not establish discrimination of the intended outcome.
- **adapt:** actual reference-pass plus at least one valid-running plausible-wrong-fail, conditional
  on an already available safe runtime; repair weak checks, tie feedback to observed failure,
  preserve honest unavailable execution and use existing transient scratch.
- **omit:** MATLAB MCP requirement, fixed two mutants, grader profile, instructor gate, line locks,
  assessment ledger, runtime installation and durable validation report.

The focused Python fixtures are independently authored; no upstream code or fixtures are copied.
