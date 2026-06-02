# Gap Analysis Rules

## GAP-001: Treat contracts as comparison material, not absolute truth

- Use `Contract` for normalized Product/Design/Design System/Engineering/QA/Analytics requirements used in the current comparison.
- Do not call any source or contract absolute truth.
- If source contracts conflict, record a `SourceConflict` with decision `clarification_needed`.
- If evidence is insufficient, reject the candidate as `unverifiable` instead of accepting a final finding.
- If external evidence is inaccessible, keep it as blocked/pending evidence and do not invent a requirement.
- Do not synthesize a new requirement by silently merging conflicting sources.

## GAP-002: Separate evidence from interpretation

- Label direct observations as Evidence.
- Label inferred conclusions as Interpretation.
- Label user-confirmed or source-confirmed items as Decision.
- Label proposed next steps as Suggestion.
- Keep raw source text and derived Spec Item or Contract text separate.

## GAP-003: Use the v7 `/tk:gap` finding schema

- Contract sources must be one of `product`, `design`, `design_system`, `engineering`, `qa`, or `analytics`.
- Candidate kind must be one of `plan_gap`, `implementation_gap`, or `red_team_candidate`.
- Accepted final severity must be one of `P0`, `P1`, or `P2`.
- Do not accept `P3` as a final finding.
- Rejected reason must be one of `P3_nit`, `duplicate`, `unverifiable`, `source_conflict`, `not_user_visible`, `not_actionable`, `low_confidence`, `missing_evidence`, or `superseded_source`.
- Source conflicts are not final findings. Record them as `SourceConflict` entries.
- Visible UI copy differences are actionable when confirmed contracts require exact copy. Meaning similarity is not enough unless the contract explicitly allows variation.

## GAP-004: Use v7 IDs consistently

- Spec Patch IDs use `SP-YYYYMMDD-HHmmss-RAND`.
- Spec Item IDs use `<PREFIX>-SP-YYYYMMDD-HHmmss-RAND-NN`, where prefix is `P`, `D`, `DS`, `E`, `QA`, or `A`.
- Gap Run IDs use `GAP-YYYYMMDD-HHmmss-RAND`.
- Candidate Finding IDs use `CAND-<KIND>-YYYYMMDD-HHmmss-RAND-NN`.
- Accepted Finding IDs use `FND-YYYYMMDD-HHmmss-RAND-NN`.
- Source Conflict IDs use `CONFLICT-YYYYMMDD-HHmmss-RAND-NN`.
- Rule IDs in this file, such as `GAP-001`, are repo rule IDs. They are not `/tk:gap` finding IDs.

## GAP-005: Match output to v7 storage and stdout contract

- Default stdout emits only summary receipt: run ID, branch scope, mode, strict status, report path, P0/P1/P2 counts, source conflict count, and rejected/downgraded count.
- Full report is stored at `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md`.
- Full report stdout is allowed only with `--print-report`.
- Run artifacts must include `input-manifest.json`, `contracts.json`, `candidates.json`, `judge-result.json`, and `report.md`.
- Do not store generated gap artifacts in `/tmp`, `$GIT_COMMON_DIR`, `.git/worktrees/*`, user home, or current worktree root outside `.claude/tigerkit/branches/<branch-key>/`.

## GAP-006: JudgeMergerAgent is the only final authority

- ProductContractAgent and DesignContractAgent may only produce contracts.
- PlanCoverageAgent, ImplementationComplianceAgent, and CriticalRedTeamAgent may only produce candidate findings or red-team objections.
- Subagent candidates are not final findings.
- JudgeMergerAgent alone accepts, rejects, downgrades, or merges candidates.
- Accepted findings must be user-visible, requirement-relevant, or interaction-affecting.
- Accepted findings must cite confirmed, non-superseded source contracts.
- Accepted findings must include concrete evidence and requiredChange that engineers can apply without guessing.

## GAP-007: Explore ambiguity before asking or deciding

Do not decide silently when any of these apply:

- Requirements document and code conflict.
- 2+ similar implementations exist with different patterns.
- Spec reference or source basis is inaccessible.
- reuse-map lacks an entry and repo-wide exploration is not sufficient yet.
- UI/UX intent cannot be confirmed by copy or screenshot alone.
- API response, DTO, permission, or state transition is unclear.
- Change scope can affect common modules.

Required handling:

- First explore code, docs, similar implementations, repo rules, and reuse-map more.
- If still unclear, create a source conflict, rejected candidate, or question instead of guessing.
- Each question must include recommendation and evidence.
- Split questions into `implementation-blocking` and `reference-only`.

## GAP-008: Check current implementation freshness before comparing

When the target means `current implementation`, current working tree, current branch, or local checkout:

- Identify the integration branch tip first. Prefer the repository default remote branch; use `origin/main` when that is the repository convention.
- Refresh or verify remote metadata when possible. If freshness cannot be verified, report base freshness as evidence.
- If local `HEAD` is behind the integration branch, check whether files in the requested scope or target evidence changed between `HEAD` and the integration tip.
- If behind changes affect the target area, compare against the integration branch tip shape instead of stale local `HEAD`, and report the base state in the manifest or report summary.
- If behind changes do not affect the target area, the local target may still be used, but report the freshness check briefly.
- If the user explicitly names a commit, branch, PR diff, or working tree state as the target, do not switch targets silently; report stale status as evidence instead.

## GAP-009: No unbounded loop

- Default mode runs no review loop.
- Auto mode runs CriticalRedTeamAgent once only when risk triggers exist.
- Strict mode runs CriticalRedTeamAgent exactly once.
- No-strict mode runs zero red-team passes.
- Never continue because of P3, nit, duplicate, unverifiable, or source conflict observations.
