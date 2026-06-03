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
- Rejected reason must be one of `P3_nit`, `duplicate`, `unverifiable`, `source_conflict`, `not_user_visible`, `not_actionable`, `low_confidence`, `missing_evidence`, `missing_producer_evidence`, or `superseded_source`.
- Source conflicts are not final findings. Record them as `SourceConflict` entries.
- Visible UI copy differences are actionable when confirmed contracts require exact copy. Meaning similarity is not enough unless the contract explicitly allows variation.

## GAP-004: Separate machine IDs from user-facing refs

- Spec Patch machine IDs use `SP-YYYYMMDD-HHmmss-RAND`.
- Spec Item machine IDs use `<PREFIX>-SP-YYYYMMDD-HHmmss-RAND-NN`, where prefix is `P`, `D`, `DS`, `E`, `QA`, or `A`.
- Gap Run machine IDs use `GAP-YYYYMMDD-HHmmss-RAND`.
- Candidate Finding machine IDs use `CAND-<KIND>-YYYYMMDD-HHmmss-RAND-NN`.
- Accepted Finding machine IDs use `FND-YYYYMMDD-HHmmss-RAND-NN`.
- Source Conflict machine IDs use `CONFLICT-YYYYMMDD-HHmmss-RAND-NN`.
- User-facing finding tables use run-local short refs instead of long machine IDs: `G<N>` for accepted findings, `R<N>` for rejected/downgraded observations, `C<N>` for source conflicts, and `Q<N>` for clarifications.
- Run artifacts should preserve the mapping with `displayRef` or an equivalent ref map so users can say `G1`/`R1` while artifacts keep canonical IDs.
- Rule IDs in this file, such as `GAP-001`, are repo rule IDs. They are not `/tk:gap` finding IDs.

## GAP-005: Match output to v7 storage and stdout contract

- Default stdout emits summary receipt plus compact tables: run ID, branch scope, quality gates, analysis depth, expansion reasons, verification escalation, status, report path, performance proof, P0/P1/P2 counts, compact Actionable Findings table, compact Rejected/Downgraded table, source conflict count, clarification-needed count, and rejected/downgraded count.
- Use `품질 gate: evidence precision + producer evidence + ambiguity + JudgeMerger` and `분석 깊이` by default. Do not use preset labels as primary output.
- Do not use ambiguous labels like `선택모드`, `실행모드`, `실행 preset`, and `추천 preset`.
- State that the run is complete for the 단일 `/tk:gap` 실행; do not imply the gap is unfinished.
- Full report is stored at `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md`.
- Compact stdout tables may include accepted finding and rejected/downgraded observation summaries, but they must use run-local `Ref` values rather than long canonical Candidate/Finding IDs.
- Detailed evidence, source contract detail, and canonical ID mapping remain in `report.md` or JSON artifacts unless `--print-report` is used.
- Full report stdout is allowed only with `--print-report`.
- Run artifacts must include `input-manifest.json`, `contracts.json`, `candidates.json`, `judge-result.json`, and `report.md`.
- `input-manifest.json` or `judge-result.json` must record `qualityGates`, `analysisDepth`, `depthReasons`, `riskScore`, `sideEffectConfidence`, `verificationEscalation`, `compatibilityFlags`, dispatch skips, blocked clarifications, Candidate Intake Gate summary, and performance proof.
- Do not store generated gap artifacts in `/tmp`, `$GIT_COMMON_DIR`, `.git/worktrees/*`, user home, or current worktree root outside `.claude/tigerkit/branches/<branch-key>/`.

## GAP-006: JudgeMergerAgent is the only final authority

- ProductContractAgent and DesignContractAgent may only produce contracts.
- PlanCoverageAgent, ImplementationComplianceAgent, and CriticalRedTeamAgent may only produce candidate findings or red-team objections.
- Subagent candidates are not final findings.
- JudgeMergerAgent alone accepts, rejects, downgrades, or merges candidates.
- Accepted findings must be user-visible, requirement-relevant, or interaction-affecting.
- Accepted findings must cite confirmed, non-superseded source contracts.
- Accepted findings must include concrete evidence and requiredChange that engineers can apply without guessing.

## GAP-007: Explore ambiguity, then use user consent gate

Do not decide silently when any of these apply, even if one interpretation looks likely:

- Requirements document and code conflict.
- Product Spec, Design Spec, API contract, QA expectation, or source priority can be read more than one way.
- 2+ similar implementations exist with different patterns.
- Spec reference or source basis is inaccessible.
- reuse-map lacks an entry and bounded exploration is not sufficient yet.
- UI/UX intent cannot be confirmed by copy or screenshot alone.
- API response, DTO, permission, persistence, or state transition is unclear.
- Change scope can affect common modules.
- The decision belongs to user, PM, Design, BE owner, QA, or another department.

Required handling:

- First explore code, docs, similar implementations, repo rules, and reuse-map according to the selected discovery depth.
- If still unclear, do not accept a final finding from the likely interpretation.
- Create a `SourceConflict`, rejected candidate (`unverifiable` or `missing_evidence`), or `ClarificationNeeded` entry instead of guessing.
- Mark decision-needed items as temporarily blocked until user consent or user-mediated owner confirmation.
- The blocked state applies to the ambiguous finding path only; continue other clear checks.
- Split questions into `implementation-blocking` and `reference-only`.
- Each question must include options, evidence, impact, recommendation, and status.
- Use compact tables for ambiguity resolution.
- For UI decisions, include TUI/ASCII prototypes when useful. Right borders must align; account for Korean full-width glyphs and padding.

## GAP-008: Check current implementation freshness before comparing

When the target means `current implementation`, current working tree, current branch, or local checkout:

- Identify the integration branch tip first. Prefer the repository default remote branch; use `origin/main` when that is the repository convention.
- Refresh or verify remote metadata when possible. If freshness cannot be verified, report base freshness as evidence.
- If local `HEAD` is behind the integration branch, check whether files in the requested scope or target evidence changed between `HEAD` and the integration tip.
- If behind changes affect the target area, compare against the integration branch tip shape instead of stale local `HEAD`, and report the base state in the manifest or report summary.
- If behind changes do not affect the target area, the local target may still be used, but report the freshness check briefly.
- If the user explicitly names a commit, branch, PR diff, or working tree state as the target, do not switch targets silently; report stale status as evidence instead.

## GAP-009: Use 단일 `/tk:gap` 실행 with analysis depth heuristic

- `/tk:gap`은 하나의 실행으로 동작합니다.
- `lite`, `strict`, `preset`, and `mode` are not user-facing quality concepts.
- `--lite` and `--strict` are compatibility flags only and must not skip evidence precision, producer evidence, ambiguity, or JudgeMerger gates.
- Analysis depth is one of `direct`, `bounded`, `expanded`, or `exhaustive-capped`.
- Use `direct` only when one explicit source/target maps to one local surface and no API/DTO/state/auth/payment/data mutation/shared component/ambiguity trigger exists.
- Use `bounded` for single screen/component/command with nearby 1-depth usage lookup or representative usage samples up to 3.
- Use `expanded` for shared component, design-system, API/DTO/state transition, source conflict risk, inaccessible reference, ambiguous Product/API/Design decision, or divergent similar implementations.
- Use `exhaustive-capped` for P0/P1 candidate, auth/permission/payment/data mutation/destructive action, release gate, or cross-module impact.
- Record `analysisDepth`, `depthReasons`, `riskScore`, `sideEffectConfidence`, and any compatibility flags in `input-manifest.json` or `judge-result.json`.
- `--legacy`, `--deep`, and `--no-strict` are not active v7.2.4 modes. v6-era legacy behavior is unsupported history, not a `lite` alias.

## GAP-010: No unbounded loop

- Direct, bounded, expanded, and exhaustive-capped analysis depths run no review loop.
- CriticalRedTeamAgent runs at most once as targeted verification.
- Never continue because of P3, nit, duplicate, unverifiable, source conflict, or clarification-needed observations.
- Re-run only when the user explicitly asks with new source, changed target, or a different `--analysis-depth`.

## GAP-011: Confirm candidate evidence coordinates before judge merge

- Before any candidate enters the JudgeMergerAgent queue, including targeted red-team candidates, read back every file:line or module-path evidence coordinate against the current target surface.
- If the cited coordinate matches the candidate claim, record it as confirmed in the run artifact evidence precision gate summary.
- If the cited coordinate is stale but the same target surface contains the correct span, repair the coordinate and record the repair evidence.
- If the current target surface cannot support the cited claim, downgrade candidate confidence to `low` and let JudgeMergerAgent reject it as `low_confidence`, `missing_evidence`, or `unverifiable`.
- Do not rely on CriticalRedTeamAgent to repair stale coordinates. Targeted red-team should attack finding validity after the Candidate Intake Gate runs.

## GAP-012: Require producer evidence for producer-absence claims

- A producer-absence claim says a backend, API, serializer, DTO, data layer, or other producer does not provide, persist, transform, expose, or cover a required value or behavior.
- Do not infer producer absence from consumer-side UI shape, fallback/default branch, empty state, mock, fixture, mapper, or missing consumer usage alone.
- Before a producer-absence candidate can become P0/P1/P2 or `SourceConflict`, it must cite direct producer-side evidence such as API contract, schema, serializer, endpoint response, data model, persistence logic, backend test fixture, or owner-confirmed producer behavior.
- If only consumer-side evidence exists, keep the observation as a rejected candidate with `missing_producer_evidence`, `missing_evidence`, or `unverifiable` instead of an accepted finding or `SourceConflict`.
- If the producer may provide equivalent data through another serialization or transformation path, treat the claim as ambiguous until producer evidence confirms absence.

## GAP-013: Run Candidate Intake Gate before JudgeMergerAgent

- No candidate may enter JudgeMergerAgent until CandidateShapeGate, EvidencePrecisionGate, ProducerEvidenceGate, and ConflictClarificationGate have run.
- Gate failures must route to rejected observation, SourceConflict, or ClarificationNeeded instead of accepted finding path.
- Candidate gate results must be recorded in `input-manifest.json`, `candidates.json`, or `judge-result.json`.
- JudgeMergerAgent remains the only final authority for accepted/rejected/downgraded final decisions among candidates that reach the judge queue.
