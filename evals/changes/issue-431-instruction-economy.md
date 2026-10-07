# Issue #431: Instruction economy audit

Baseline: `main@4f329539f234334278eeaecd465eeb0cccb1fa50` (28 installed `tk-*` skills).
Scope: current `SKILL.md` bodies and shared block ownership; this is a static audit, not measured model-token or elapsed-time efficiency.

## Inventory

| Measure | Baseline |
| --- | ---: |
| SKILL.md bodies | 28 |
| UTF-8 characters | 352,779 |
| Four synchronized shared blocks | 84,678 |
| Ratio (four blocks only) | 24.0% |
| Largest unique/remaining body | tk-prep 20,693; tk-pr-respond 19,936; tk-pr-open 17,429; tk-browser-verify 16,866 |
| Highest common-block proportion | tk-adhd 51.1%; tk-rewrite 40.6% |

Four blocks = Artifact Paths, Output Notation, User Questions, Skill Feedback. Other repeated runtime, approval and UI-evidence blocks are excluded; total duplication is not inferred from those figures.

## Evidence-based decisions

- **Tighten: shared Output Notation / user input**. JSON shape, secret file permissions, incomplete-template rule and secure consumption already have a branch-specific canonical owner in each writing skill's `references/artifact-paths.md`. In #432, the 28 always-loaded copies and generator now contain a short conditional pointer instead of re-describing that procedure. Patch shape: 29 files, one replaced line each.
- **Tighten: cross-skill feedback**. Old common Skill Feedback forced a `tk-learn` proposal lifecycle for any reusable feedback. #430 removes that writer and routes opt-in session diagnosis to `tk-retro`. The synchronized pointer preserves the prohibition against auto-edits, automatic publication and silent invocation. It no longer forces per-run file creation.
- **Tighten: tk-handoff UI propagation**. Its former local propagation paragraph duplicated the installed UI Evidence block's unverified-path, provenance and investigation boundaries; preserve the shared block and delete only the duplicate paragraph.
- **Disclose: tk-handoff resume**. Resume and drift classification is a branch reached only by explicit `--resume`; it now has an explicit conditional pointer to `references/resume.md`. The underlying drift table and authorization limits are preserved.
- **Disclose: tk-grooming failure paths**. Ownership, access, scope and verification failure handling now belongs to `references/failure-paths.md`, read only when a checkpoint fails. Existing stop/reversal guidance and report-only default remain.
- **Keep: tk-prep, tk-pr-respond, tk-pr-open, tk-browser-verify, tk-pr-sweep**. These are execution/publication owners with behavioral authority, freshness, UI evidence and recovery pressure. Length alone is not evidence of redundant instructions; no broad rewrite without a reproducible pressure case.
- **Keep: tk-adhd, tk-rewrite, tk-grill, tk-roadmap common question/notation boundaries** until positive/negative routing shows that a concrete rule is inactive. The audit does not assume read-only or user-invoked means a shared question contract is a no-op.
- **Retire: tk-learn + tk-skill-diagnose** under #430 only after routing/eval/installation migration to `tk-retro`, rather than as a line-count optimization.

## Evaluation and exclusions

Static checks required: no missing installation packages, eval-directory parity, no stale active skill references, generated shared-block consistency, catalog and release-critical references, local reference-link existence and review of actual changed files. These checks do not prove runtime behavior.

Before claiming behavioral speedup or safely dropping any additional guard, replay representative success/negative/pressure scenarios in an available Claude Code, Codex or Hermes host. Until then, report actual harness execution as **not run**; do not claim a token or latency gain from character counts.

Do not strip publication approvals, permission boundaries, secret handling, fresh-head checks or independently verified behavior simply to meet a size threshold.
