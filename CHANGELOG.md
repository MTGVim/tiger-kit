# Changelog

## Unreleased

- refactor: rename the read-only `tk-improve` advisor to `tk-audit` with an `AUD-*` ledger

## 2026.08.07-1 — Release

- docs: streamline README invocation notes

## 2026.08.06-9 — Release

- feat: add cost-aware model routing and zero-context cheaper-model handoffs
- feat: add the read-only `tk-improve` evidence ledger and downstream finding routes
- refactor: make standalone progress optional with three core markers for orchestrators

## 2026.08.06-8 — Release

- feat: standardize universal car-based compact progress output across tk-* skills
- fix: render PR/thread URLs as clickable links and normalize GitHub break tags for TUI
- test: enforce the shared progress contract in the deterministic release gate

## 2026.08.06-7 — Release

- fix: align tk-pr-open hybrid natural-language routing with its publication gate
- docs: make tk-ask-repo entry and host invocation flags explicit
- remove: delete unused tk-adhd utility

## 2026.08.06-6 — Release

- feat: streamline orchestration progress

## 2026.08.06-5 — Release

- test: migrate sweep approval contracts
- fix: clarify sweep output and local times

## 2026.08.06-4 — Release

- fix: align pr-open conversational trigger

## 2026.08.06-3 — Release

- test: guard resume mutation boundaries
- docs: retain decisive compact progress tokens
- test: tighten resume safety coverage
- test: migrate compact progress contracts
- fix: resume workflows with compact progress

## 2026.08.06-2 — Release

- fix: clarify drive blocked state

## 2026.08.06-1 — Release

- fix: clarify drive orchestration status

## 2026.08.05-3 — Release

- fix: complete PR response workflow

## 2026.08.05-2 — Release

- feat: gate PR sweep mutations

## 2026.08.05-1 — Release

- compress tk skills: reduce contract prose
- optimize tk-github-image-upload: consolidate risks
- optimize tk-pr-open: encode failure paths
- optimize tk-implement: consolidate anti-patterns

## 2026.08.04-3 — Release

- refactor: simplify orchestration release checks
- fix: make eval recorder executable
- fix: stabilize respond CI commit path
- fix: require respond canary commit
- fix: accept safe equivalent eval scripts
- fix: secure verified eval commit scripts
- fix: run prepared Codex eval fixtures
- fix: accept current Codex message events
- fix: harden PR sweep lifecycle
- fix: surface outstanding PR feedback
- fix: keep orchestration visibly moving

## 2026.08.04-2 — Release

- feat: add bounded PR sweep orchestrator
- feat: add sweep CI mode to PR rebase
- feat: add CI mode to PR response

## 2026.08.04-1 — Release

- fix(workflows): continue through every successful implementation unit

## 2026.08.03-9 — Release

- fix(skills): restore the `tk-grill-me` invocation label in Codex

## 2026.08.03-8 — Release

- fix(docs): keep README skill catalog complete and release-neutral
- fix(skills): use canonical `tk-*` names in skill pickers

## 2026.08.03-7 — Release

- optimize tk-pr-open: mark publication checkpoint
- optimize tk-skill-diagnose: own evidence ledger
- optimize tk-grooming: align summary contract
- optimize tk-pr-triage: mark read-only handoff
- optimize tk-adhd: mark safety checkpoint
- feat: strengthen implementation review convergence

## 2026.08.03-6 — Release

- feat(pr): add safe rebase workflow

## 2026.08.03-5 — Release

- feat(ux): render skill questions directly in chat

## 2026.08.03-4 — Release

- feat(pr): own PR evidence decisions in preparation

## 2026.08.03-3 — Release

- fix(pr): allow verified image upload handoffs

## 2026.08.03-2 — Release

- feat(pr): restore user-first PR workflows

## 2026.08.03-1 — Release

- optimize tk-pr-triage: retry incomplete API collection
- optimize tk-to-tickets: define core ticket fields
- optimize tk-pr-respond: discover PR from selected comments
- optimize tk-browser-verify: discover local verification routes
- optimize tk-implement: resolve standalone targets from repo evidence

## 2026.08.02-1 — Release

- fix(tooling): clarify catalog audit disposition
- perf(docs): shrink README cover

## 2026.08.01-4 — Release

- feat(workflow): hand off required PR evidence

## 2026.08.01-3 — Release

- feat(skill): add GitHub PR image upload skill

## 2026.08.01-2 — Release

- feat: split PR lifecycle into canonical skills

## 2026.08.01-1 — Release

- fix: validate date release snapshots
- perf: make live release canary opt-in
- docs: refresh README cover and bytecode hygiene

## 21.0.10 — Release

- fix: align stable README snapshot

## 21.0.9 — Release

- Issue #224 removes the retired reflection skill and ends `tk-drive` directly
  after aggregate verification; `tk-learn` now solely owns skill
  `create | improve | merge`, while diagnosis emits `learn-ready` and grooming
  is limited to repository/user skills.
- Every started `tk-browser-verify` Guard or Verdict run now requires a
  non-empty screenshot, actual image inspection, and an absolute
  `Evidence directory: /...` when resolvable.
- Added explicit eval-contract retirement evidence and ADR 0003 for the new
  ownership and browser-evidence boundaries.

## 21.0.8 — Eval SSOT and Empirical Quality

- Made skill-local trigger and behavior JSON the single source of truth, removed generated Darwin prompt projections and root fixture mirrors, and replaced hardcoded catalog snapshots with auto-discovery.
- Added a built-in project-local Codex → Claude Code → Hermes Agent quality adapter that preserves authentication without mutating user skill folders; unavailable live hosts remain visible `Advisory` evidence.
- Added exact-candidate `tk-drive` versus explicit-composition A/B experiments and an evidence-derived catalog audit; retained all 15 skills because no measured removal evidence was available.
- Added local release-critical and catalog gates around the new schema while keeping GitHub Actions absent.

## 21.0.7 — Zero-crust Contracts

- Replaced validator magic-phrase checks with structural checks for user decisions, terminal output, response language, and learning-loop ownership.
- Reduced `tk-browser-verify`, `tk-reflect`, `tk-to-spec`, and `tk-to-tickets` to their unique trigger, authority, evidence, state, and failure contracts.
- Preserved browser launch/capture safety, reflection apply authority, Ready traceability, vertical ticket ownership, behavior evals, and package compatibility while reducing eager instruction weight.

## 21.0.6 — Lean Core Skills

- Compressed `tk-drive` into a thin orchestration recipe while preserving its
  preparation, unit execution, aggregate verification, amendment, and
  non-success boundaries.
- Compressed `tk-implement` into one unit workflow and moved conditional test,
  source-writing, browser, review, and commit detail into a lazily loaded
  execution-gates reference.
- Preserved current trigger, status, ledger, verification, review, commit, and
  cross-host contracts while reducing eager hot-path instructions.

## 21.0.5 — Lean Terminal Normalization

- Normalized `pending`, `Draft`, `Unresolved split report`, and `aborted`
  before terminal drive finalization, preserving bounded recovery edges and
  preventing child receipts from becoming accidental terminal output.
- Moved detailed non-success accounting into one owned reference while keeping
  the drive entry and procedure graph compact.
- Made `tk-drive non-success finalization` the sole downstream writer for
  bounded ticket-attempt evidence and kept implementation receipts with
  `tk-implement`.
- Added contract and eval coverage for pending decisions, aborted decisions,
  terminal Draft, unresolved split, and writer ownership.

## 21.0.4 — Read-only Non-success Finalization

- Added one internal `tk-drive non-success finalization` node after alternate
  edges are exhausted, freezing product mutation and preserving the originating
  `Fail | Blocked | Unverifiable` status.
- Accounted verified, stopped, dependency-blocked, unattempted, and unverified
  scope from existing artifacts and Git evidence with one deterministic
  recovery action, without adding a public skill, partial status, run ledger,
  scheduler, or automatic cleanup.
- Extended `tk-implement` and `tk-to-tickets` non-success handoffs and added
  validator and eval coverage for terminal graph edges, stale receipts, bounded
  ledger evidence, and portable Claude Code, Codex, and Hermes Agent behavior.

## 21.0.3 — Direct Procedure Graph and Portable Validation

- Kept decision closure unified in `tk-grill-me` and replaced parent-return
  orchestration with one validated direct `tk-drive → tk-grill-me →
  tk-to-spec → tk-to-tickets (conditional) → tk-implement` procedure graph.
- Replaced the mutable prep lifecycle, claim/finalize scripts, phase receipt
  recorder, and stored resume cursor with a compact secret-free
  `.tigerkit/prep.md`, invocation-only eval evidence, and current-evidence
  resume decisions.
- Bounded corrective execution with mechanical procedure-count assertions and
  one remaining-failure report after the third unsuccessful correction.
- Restricted drive-tail reflection auto-apply to one exact pre-existing ignored
  user-managed rule target and added a guarded secure-backup, atomic-write,
  validation, and exact-rollback executor; tracked and unsafe targets remain
  pending.
- Documented that Agent Skill continuation is prompt-directed and
  probabilistic, not durable scheduling or replay, and retained portable
  Claude Code, Codex, and Hermes Agent distribution.

## 21.0.2 — ADHD Utility and Reflection Boundary

- Renamed the explicit output utility from `tk-recap` to `tk-adhd` and made it
  one-shot: each explicit invocation shapes only its current response, with no
  activation, stop command, or cross-turn state.
- Narrowed `tk-reflect` selection metadata and trigger coverage so summaries,
  output-style utilities, and explicit invocation of another skill cannot route to
  reflection.

## 21.0.1 — Terminal Opening, Browser Preflight, and Recap Mode

- Removed the terminal Markdown `---` separator from every distributed skill;
  terminal responses now begin directly with the owning canonical result
  heading or result sentence while internal receipts remain hidden.
- Added a material-only strategy preflight to `tk-drive` Preparing, including
  conditional `required | optional | N/A` browser routing, non-identifying
  account/profile hints, authentication and safe-interaction planning, and an
  explicit cold-start re-request marker for intentionally omitted identities.
- Renamed the explicit persistent output utility from `tk-focus` to
  `tk-recap`, including picker metadata, stop language, routing, and evals, to
  avoid collision with host-provided focus features.

## 21.0.0 — Single-Drive Preparation and Explicit Focus

- Kept one public `tk-drive <source>` entry point and expanded the canonical
  catalog to 15 skills: 3 user-invoked and 12 hybrid, including the explicit
  persistent `tk-focus` adaptation.
- Added strict, atomic `.tigerkit/prep.md` creation with task, repository,
  source, dirty, instruction, spec, ticket, and verification-profile identity
  digests as an internal Preparing boundary.
- Changed `tk-drive` to continue automatically from Preparing into Executing,
  permit one bounded late Preparing amendment and at most three post-initial
  corrective cycles, and finalize the same claim before terminal output.
- Preserved raw `/tk-drive <source>` as the only public full-run command;
  direct standalone `tk-implement` remains supported and old scratch is not
  migrated.
- Added task-anchored discovery of at most seven durable prior-art items,
  preferred prevention-owner and host-dependency classification, and semantic
  `adopted | already-satisfied | not-applicable | conflict` R/AC disposition.
- Added strict state-race, cross-skill wire-compatibility, recovery, eval
  migration, Codex cold-start and prepared-continuation paths, and three-host
  package coverage.
- Removed the shared actionable-output presentation gate; `tk-focus` owns the
  adapted ADHD-oriented rules and is never selected implicitly. All other
  skills retain the terminal `---` boundary, user-language behavior, and
  internal-only phase receipts.

## 20.3.1 — Terminal Transition-Debt Gate

- Added an explicit last-mile `tk-drive` transition-debt check immediately
  before terminal `---` output. A consumed successful child receipt with an
  unexecuted `Outstanding transition` can no longer become a response
  boundary.
- Added a deterministic contract mutation test while preserving the existing
  host-generic event-order assertion and Codex continuation canary.

## 20.3.0 — Terminal Summaries and Internal Receipts

- Added the same actionable-output hard gate to all 14 self-contained skills:
  canonical output schemas stay authoritative while free-form prose leads with
  the answer, outcome, or action, keeps live state visible, reports
  evidence-based recovery, and omits ceremonial closers or invented next
  actions.
- Added deterministic gate validation, representative Codex behavior
  assertions, and upstream attribution without adding a skill, persistent
  mode, shared runtime reference, or catalog migration.
- Added one exact terminal-summary boundary to all 14 skills: every terminal
  user response begins after one Markdown `---` separator, while progress and
  same-turn phase continuation remain unseparated.
- Removed bottom receipt blocks and the repeated `Outcome:` label from terminal
  user output. Existing artifacts and ledgers retain durable provenance, and
  active-drive phase receipts remain internal handoff envelopes.
- Kept read-only skills read-only and rejected a universal receipt ledger, so
  the release adds no shared runtime surface, scratch archive, or write
  expansion.
- Added exact-block, ordering, mutation, obsolete-rendering, and representative
  behavior coverage for the new boundary while preserving status semantics,
  result budgets, phase liveness, and the 14-skill catalog.

## 20.2.0 — Implementation Quality, Optimistic Reflection, and Bounded Results

- Added a `tk-implement` design-fit preflight that chooses reuse, extension,
  local ownership, or evidence-backed shared abstraction before mutation.
- Added one behavior-preserving simplify pass after initial GREEN and before
  final verification, while keeping Standards and Spec review independent.
- Added bounded `.tigerkit/implementation.md` evidence for repository fit,
  simplify disposition, verification, and current-agent review.
- Routed successful aggregate drive work through exactly one fixed-point
  `drive-optimistic` reflection tail.
- Limited optimistic mutation to high-confidence existing repository rules,
  with separate tracked-commit and ignored/local before-image rollback.
- Kept skill candidates report-only as promotion packets and preserved the
  human-readable `ID | Candidate | Action | Target | Why` reflection table.
- Replaced strict one-line result compression across all 14 skills with
  decision-first, cardinality-aware bounded summaries and nonduplicative
  receipts.
- Recorded the durable ownership, rollback, fixed-point, and supersession
  rationale in ADR 0001 without adding skills, runtime surfaces, or release
  automation.
- Added the same response-language hard gate to all 14 skills so the latest
  explicit language instruction controls every free-form user-facing sentence
  while canonical tokens and exact source literals remain byte-stable.
- Added evidence-based `tk-drive` verification profiles that keep low-risk
  work silent, derive deterministic obligations for material risk, preserve
  phase ownership, and reconcile those obligations before aggregate `Pass`.

## 20.1.7 — Repository Answers, Drive Liveness, and Concise Receipts

- Expanded the catalog to 14 canonical skills with the user-invoked
  `tk-ask-repo` investigation desk, including source-located value, structure,
  existence, impact, and attribution traversals.
- Fixed `tk-drive` child-receipt liveness so successful phase-owner handoffs
  carry their next transition, and required every drive run to pass through a
  Ready spec without a small-task exception.
- Made terminal output decision-first across the catalog, removed empty or
  duplicate narration, and kept raw logs and detailed evidence in their owned
  artifacts or bounded ledgers.
- Added conditional itemized result tables for multi-item implementation,
  verification, diagnosis, conflict, prototype, and ticket results while
  keeping single-item output as one sentence.
- Added one localized `Outcome` sentence to every receipt-bearing contract so
  users can understand the result before status and provenance fields.
- Preserved `tk-reflect` report-only behavior, drive/spec/ticket phase
  ownership, approval and mutation boundaries, and all prior safety and
  terminal-state contracts.

## 20.1.6 — Structured User Decision Questions

- Standardized a self-contained user-decision question contract across all 13
  canonical skills, with one question at a time, two or three mutually
  exclusive proposals, material tradeoffs, and exactly one localized
  recommendation marker.
- Required `Question` to precede `Recommendation` and to explain the
  evidence-derived context, decision impact, and unresolved axis in readable
  user-facing prose instead of requiring users to decode raw evidence.
- Required native structured user-input tools whenever the active host exposes
  one, with explicit Claude Code `AskUserQuestion`, Codex
  `request_user_input`, and Hermes Agent `clarify` examples and prose fallback
  only when no such tool is available.
- Made supported option previews and prototype cards proactive aids when they
  clarify a decision without expanding the owning skill's authority.
- Added repository validation, unit coverage, and the required
  `grill-uses-native-question-tool` behavior-eval contract to prevent drift in
  ordering, readability, tool gating, option count, and recommendation
  labeling.

## 20.1.5 — Empirical Agent Skill Diagnosis and Catalog Reliability

- Expanded the catalog from 12 to 13 canonical skills while retaining one
  user-invoked skill and moving to 12 hybrid skills.
- Added adapted `tk-skill-diagnose` for observed correctness, stability,
  compatibility, evaluation, and efficiency incidents with clean reproduction,
  failure-plane isolation, one-theme temporary candidates, and holdout gates.
- Added the single conditional `tk-reflect → tk-skill-diagnose` handoff and
  blocked reverse calls, repeated equivalent blockers, and sibling loops.
- Added an opt-in empirical diagnostic pass to `run_skill_evals.py` with
  answer-free prompt composition, marker-delimited structured traces, separate
  metrics/records/ledger, and unchanged normal behavior when disabled.
- Added external consumer provenance, anonymization, and upstream issue-draft
  contracts without issue creation or canonical skill mutation.
- Strengthened `tk-drive` same-turn phase continuation and source-UI literal
  routing, and required more precise browser runtime evidence.
- Standardized canonical skill bodies and operational references in English
  while preserving user-language progress and receipts, and added persistent
  memory as the fifth `tk-reflect` classification axis.
- Refined all 13 skills through independent paired ratchets: deterministic
  failure terminals, delegation fallback, atomic writes, worktree-safe Git
  state discovery, artifact ownership, and executable spec/ticket evals.
- Audited post-commit hook drift in isolated eval runs and kept vendor-owned
  artifacts report-only instead of treating them as candidate mutations.
- Preserved every existing explicit invocation name and the Agent Skills-only
  distribution; this patch adds no workflow runtime, plugin surface, or
  release-time live-eval requirement.

## 20.1.4 — Conditional Decision Orchestration and Skill Refinement

- Made `tk-drive` the single user-invoked workflow entry point and converted
  `tk-grill-me` to a narrowly triggered hybrid decision phase owner.
- Replaced drive's one-question inline gate with conditional `tk-grill-me`
  handoff, while skipping grill entirely for source that already supports a
  Ready spec.
- Routed decision-related spec or ticket failures back through drive and grill,
  using an explicit `User decision` receipt signal, then required Ready-spec
  revalidation before downstream ticket rederivation and blocked repeated
  equivalent decision loops.
- Kept phase owners from invoking siblings, preserved standalone grill/spec/
  ticket/implementation use, retained 12 canonical skills, and did not add
  `tk-prep`.
- Refined every canonical skill with one conservative, independently paired
  improvement: cheaper negative conflict exits, precise browser blockers,
  direct no-ticket handoffs, deterministic decision ranking, canonical receipt
  ownership, and reduced duplicated safety wording.
- Tightened grooming classification, candidate naming, bounded evidence retry,
  atomic handoff replacement, and hypothesis-scoped prototype viewport
  evidence without changing skill names, invocation kinds, or distribution.
- Refreshed decision-flow evals for drive resume, Ready-source grill skipping,
  active-drive decision handoffs, and spec/ticket decision returns.

## 20.1.3 — Phase-Owner Improvements

- Made `tk-drive` a thin orchestrator that explicitly hands spec creation to
  `tk-to-spec`, conditional vertical decomposition to `tk-to-tickets`, and each
  implementation unit to `tk-implement`, with strict receipt propagation and
  no inline phase fallback.
- Converted `tk-implement` to narrowly triggered hybrid invocation while
  preserving direct selection, and changed drive execution from one final
  commit to one verified commit per ticket or no-ticket single slice.
- Required durable automated tests for production behavior, observed red
  regression tests when a meaningful bug seam exists, existing repository
  coverage gates when available, and explicit named exceptions before any
  testless production-behavior commit.
- Split ticket-level Standards/Spec review from drive-wide ancestry, R/AC,
  cross-ticket, and broad verification; bounded final correction to one
  additive corrective ticket and commit without history rewriting.
- Standardized the four phase-owner operational contracts and references in
  English while keeping user-facing progress and final receipt prose in the
  user's language.
- Refined all 12 skill contracts with bounded evidence, mutation, approval,
  placement, recovery, and resumability guidance while retaining their
  existing names and explicit invocation paths.
- Required TDD red evidence to fail for the expected missing behavior, bounded
  mocks to unavoidable external side-effect boundaries, and made vertical
  tickets executable from cited sources without hidden conversation context.
- Preserved all 12 canonical skill names, changed the distribution to
  1 user-invoked / 11 hybrid, and added static and executable cross-host
  routing, phase handoff, failure, test, coverage, and commit regressions.

## 20.1.2 — Deterministic Routing and Failure Contracts

- Added critical routing coverage for `tk-learn` versus reflection/grooming and `tk-drive` versus handoff/generic continuation, with repository validation that requires both boundaries.
- Promoted merge-conflict and interview safety paths to executable evals, and split unreadable UI text, conflicting UI text, commit-command failure, and pre-commit drift into deterministic `tk-drive` terminal states.
- Reduced repeated terminal, approval, and output-field guidance in `tk-implement`, `tk-learn`, and `tk-reflect`, then used a two-judge Darwin ratchet and canonical full tests to keep `tk-learn`'s unresolved identity branch explicitly `pending` and write-safe.
- Preserved all 12 canonical skill names, the 2 user-invoked / 10 hybrid distribution, self-contained resources, and local-only verification boundary.

## 20.1.1 — Explicit Recovery and Freshness Contracts

- Refined all 12 canonical skill contracts with explicit terminal-state, failure-recovery, freshness, and command-evidence tables while preserving their names, invocation kinds, and ownership boundaries.
- Tightened decision, resume, apply, prototype, handoff, browser-verdict, and conflict-resolution paths so drift and incomplete evidence stop at one well-defined checkpoint without discarding valid partial work.
- Reduced duplicated status guidance by assigning each outcome and receipt to one owning section, keeping the 2 user-invoked / 10 hybrid distribution surface unchanged.

## 20.1.0 — Cross-Host Parity and Eval Evidence

- Made `tk-drive` explicit start host-neutral across slash commands, Codex `$` invocation, and skill pickers, and carried exact source UI writing through spec, tickets, implementation, staged diff, and rendered evidence.
- Made `tk-learn` the sole semantic skill writer, limited reflect/grooming to proposal-only semantic changes, resolved only current-host native targets, and simplified handoff state to one `.tigerkit/handoff.md` snapshot.
- Added browser capture sensitivity, redaction, and residue gates that keep unverified sensitive evidence out of repo-local scratch.
- Strengthened evals with exact terminal states, content/path/diff assertions, independent baseline/candidate contracts, deletion/weakening drift checks, catalog selection metadata, and a Claude Code/Codex/Hermes Agent critical routing matrix.
- Locked the deterministic repository placement rubric from #182 with mechanical safety-token, sibling-threshold, override, fallback, and missing-evidence regression coverage while preserving all 12 canonical skill names and invocation kinds.

## 20.0.3 — Headless Verification and Numbered Reports

- Made `tk-browser-verify` launch Chrome with the exact `--headless=new` argument by default, permit headed mode only for user-completed interactive authentication, and resume verification headlessly with the same persistent profile.
- Made design alignment conditional on an available design basis and shortened pre-session stops without weakening launch, authentication, or TigerKit capture-ledger evidence.
- Standardized `tk-reflect` and `tk-grooming` outputs with stable per-item IDs, mandatory final summary tables, one-line rule summaries, explicit application targets, and empty-result rows.

## 20.0.2 — Verbatim Fidelity and Capture Ledger

- Hardened `tk-implement`, `tk-to-spec`, and `tk-to-tickets` to preserve source-provided UI labels, buttons, guidance, column names, and related writing as exact literals through implementation artifacts and verification.
- Made `tk-browser-verify` move run-owned captures from tool or user scratch into a repo-local TigerKit run ledger, preserve user-owned inputs, and block verdicts without custody and residue evidence.
- Improved all 12 canonical skills with stricter draft/apply boundaries, executable conflict evidence, deduplicated output contracts, aligned receipts, and regression coverage while preserving the 2 user-invoked / 10 hybrid surface.

## 20.0.1 — Local-Only Verification

- Removed the GitHub Actions validator, eval preview, and latest-CLI canary workflows so repository verification runs only on maintainers' local machines.
- Documented the complete local validation sequence and kept three-host packaging smoke installation as a release requirement.
- Updated repository and release contracts to reject CI validation workflows and bind release evidence to exact locally validated trees without requiring CI provenance.

## 20.0.0 — Drive-Centered Skill Surface

- Changed the canonical surface to 12 self-contained skills: 2 user-invoked and 10 hybrid.
- Added explicit-start, same-conversation-resumable `tk-drive` with inline one-question ambiguity handling, optional ticket ledger, bounded nested skills, built-in review parity, one final commit, and partial-failure preservation.
- Converted planning, prototype, reflection, learning, grooming, and handoff artifact skills to narrowly triggered hybrid contracts.
- Folded unknown-cause investigation and fixed-point Standards/Spec review into `tk-implement`, then removed their standalone skill surfaces.
- Added deterministic root/nested rule versus repo-skill placement and disposable wide/narrow web A/B/C prototype guidance.
- Made skill eval automation API-free and opt-in by removing the unconfigured scheduled live comparison while retaining manual dry-run previews.

## 19.0.17 — Bounded Large-Diff Review

- Added stat/numstat preflight and deterministic file/line thresholds before `tk-code-review` reads diff content.
- Routed large or size-unknown diffs through bounded inspection while preserving complete file/hunk coverage before `Pass`.
- Added static and executable regression coverage for large-diff context safety and source immutability.

## 19.0.16 — Enforced Browser Routing and Skill Ratchets

- Made `tk-implement` activate `tk-browser-verify` before any browser tool or verification server, prohibited direct Chrome MCP/Playwright/CDP/native selection, and invalidated browser evidence created before the gate.
- Ratcheted all 13 canonical skills with clearer workflow ownership, failure-state routing, confidence evidence, checkpoint visibility, and section structure while reverting an attempted safety regression.
- Added browser-routing behavior/eval fixtures and static validation so bypasses fail deterministic repository checks.

## 19.0.15 — Output Contract Deduplication

- Assigned each substantive result to one named output section across ten canonical skills instead of restating it under overlapping labels.
- Limited receipts to terminal or disposition status, unresolved items, and references while preserving skill-specific evidence and verification fields.
- Added primary eval assertions that reject semantically duplicated output across the affected skill contracts.
- Moved the maintainer-only `tigerkit-release` helper to user scope and removed its repository-tracked skill and fixture surfaces from consumer discovery.

## 19.0.14 — Existing Structure Hardening

- Required stable releases to originate from validated `origin/main` and verify main, peeled tag, GitHub Release, and CI provenance before completion.
- Added reproducible pinned-CLI validation, a latest-CLI canary, Python regression tests in CI, and an explicit portable-core/host-extension compatibility profile.
- Made executable trigger and structured behavior eval contracts canonical for all 13 skills, retained generated Darwin prompt projections, and added an isolated baseline comparison runner with scheduled/manual evidence workflow.
- Strengthened existing handoff, traceability, conditional high-risk review, browser accessibility, and skill-learning contracts without adding canonical skills.
- Hardened all 13 canonical skill contracts with verified recovery, freshness, and post-write evidence gates while preserving their names and invocation kinds.
- Reworked the maintainer release flow around intent-aware candidate reconciliation, exact PR and final-main CI evidence, PR merge, tag, and GitHub Release checkpoints.

## 19.0.13 — Canonical Skill Boundary Refinements

- Added explicit failure outcomes across the canonical skills for missing evidence, unresolved decisions, unsafe runtime conditions, and incomplete verification.
- Added compact workflow input/output, evidence, receipt, and state-check guidance without expanding the 13-skill catalog.
- Preserved runtime-neutral distribution, invocation boundaries, and mutation safety.

## 19.0.12 — Release Checkpoint and Validation Hardening

- Added explicit STOP checkpoints before remote changes, Promote integration, release mutations, and post-release main cleanup.
- Hardened the maintainer release fixtures and validator contract for promotion, resume, dry-run, and post-release branch reconciliation.
- Preserved the 13-skill distribution and runtime-neutral release workflow.

## 19.0.11 — Canonical Skill Workflow Optimization

- Improved all 13 canonical skills with clearer workflow inputs, outputs, checkpoints, failure states, and verification receipts.
- Added Darwin evaluation prompt fixtures for each canonical skill to support repeatable quality checks.
- Preserved explicit invocation boundaries, mutation safety, and no-repeat decision guards while tightening implementation and conflict-resolution verification.

## 19.0.10 — Release Promotion and Resume Safety

- Added an explicit promotion flow for named remote release branches with merge-tree preview and no-ff merge.
- Added partial-success resume rules that preserve existing tags and GitHub Releases without overwriting them.
- Added dry-run boundaries and maintainer release behavior fixtures.

## 19.0.9 — Structured Grilling and Decision Closure

- Added a conversation-only `Scope`, `Constraints`, `Outputs`, and `Verification` ambiguity ledger to `tk-grill-me`.
- Separated exact code facts from user judgment, preserved decision boundaries, and added explicit one-sentence goal approval before closure.
- Expanded static behavior coverage for fact routing, boundary preservation, targeted reconfirmation, and closure behavior.

## 19.0.8 — Evidence Checkpoint Refinements

- Tightened explicit stop boundaries for prototype execution, user decisions, review start, bug hypotheses and patches, and conflict resolution continuation.
- Preserved truthful `Blocked`, `Unverifiable`, `Fail`, and `pending` outcomes when required evidence or user decisions are missing.

## 19.0.7 — Checkpoints and Anti-Patterns

- Added explicit CHECKPOINT / STOP gates to canonical skills so missing evidence, unresolved decisions, and unsafe execution boundaries end in a truthful blocked or unverifiable state.
- Added DO NOT / ANTI-PATTERNS guidance for mutation safety, review scope, verification evidence, delegation, and release boundaries.
- Tightened workflow receipts and decision-field requirements across grooming, handoff, learning, prototyping, specification, ticketing, and conflict resolution.
- Disabled implicit invocation for the maintainer-only `tigerkit-release` skill.

## 19.0.6 — Guarded Browser Verification Modes

- Added lightweight Guard mode for temporary HTML, prototypes, and exploratory UI checks without forcing responsive matrices or formal verdicts.
- Preserved the full Verdict mode evidence contract for persistent user-visible source changes, explicit invocation, and formal verification requests.
- Added a compact P1–P10 router for trusted input, CDP ownership, visual baselines, API-gated states, screenshot paths, responsive checks, cleanup, motion timelines, field clearing, and server auto-open behavior.
- Clarified automatic trigger exclusions versus explicit invocation and expanded static trigger, behavior, and validation coverage.

## 19.0.5 — Automatic Browser Verification Routing

- Routed user-visible UI and browser behavior changes from `tk-implement` through hybrid `tk-browser-verify` without another approval request.
- Required design intent preflight before source mutation when Figma, screenshots, or design specifications define the expected UI.
- Required runtime screenshot capture and actual image inspection after implementation, with commit blocked unless browser verification passes.
- Updated skill descriptions, documentation, trigger fixtures, behavior fixtures, and canonical validation for the routing contract.

## 19.0.4 — Safe Browser Launch and Autonomous Implementation

- Prevented browser verification from auto-launching until headless execution and a temporary isolated profile are confirmed; otherwise it returns `Unverifiable`.
- Made explicit user scope, method, prohibitions, execution mode, TDD, verification, and commit decisions binding in `tk-implement`.
- Made unspecified execution mode and TDD choices resolve automatically after inspection without a strategy approval round trip.
- Updated static behavior fixtures and canonical validation for both contracts.

## 19.0.3 — Browser Design Intent Gate

- Fixed the distribution smoke install to exercise standard discovery without explicitly selecting internal maintainer skills.
- Added a required design-intent preflight before browser execution when Figma, screenshots, or design specifications are provided.
- Decomposed visible spacing into nested frame, container, component, and child layers instead of treating the total offset as one padding value.
- Blocked conflicting or unclear user and design expectations until the user explicitly selects a concrete final UI; silence cannot approve a deviation.
- Separated pre-browser `Blocked` decisions from runtime `Unverifiable` evidence failures while retaining screenshot capture and actual image inspection for runtime terminal states.
- Required an `Alignment` receipt with design basis, spacing stack, relation, expected implementation, user decision, and status.

## 19.0.1 — Procedural Contracts and Release Safety

- Strengthened all 13 canonical skills with explicit preconditions, required sequences, completion gates, failure states, forbidden shortcuts, and evidence receipts.
- Made browser verification headless by default, limited headed mode to interactive authentication, and required inspected terminal-state screenshots for successful visual verdicts.
- Added responsive width and breakpoint-edge checks plus evidence-based Figma deviation classification.
- Allowed ignored repo-local `.tigerkit/` scratch while rejecting tracked or packaged scratch, with regression tests for all three cases.
- Added the repository-local `tigerkit-release` maintainer skill without changing the 13-skill distribution catalog.

## 19.0.0 — Skill Consolidation and Follow-up Boundaries

TigerKit 19 is a major release that reduces the canonical catalog from 18 skills to 13 while preserving the `v18.0.4` implementation and browser contracts.

### Removed

- Removed redundant micro-skills `tk-grill-with-docs`, `tk-grilling`, `tk-domain-modeling`, `tk-tdd`, and `tk-codebase-design`.
- Removed the model-only invocation category.
- Removed automatic feature-branch `CONTEXT.md`, domain document, glossary, and ADR mutation contracts.

### Merged

- Merged fact-first, one-question-at-a-time grilling discipline into `tk-grill-me`.
- Merged public-behavior `red → green` TDD into the `tk-implement` TDD branch.
- Merged diff-grounded structure checks into `tk-code-review` Standards review.
- Merged regression-seam assessment into `tk-diagnosing-bugs`.

### Changed

- Changed `tk-code-review`, `tk-diagnosing-bugs`, and `tk-merge-conflict` from model-only to hybrid.
- Added fixed-point validation and separate Standards/Spec axes to `tk-code-review`.
- Added a red-capable feedback-loop gate, regression seam reporting, cleanup, and explicit standalone/embedded commit boundaries to `tk-diagnosing-bugs`.
- Extended `tk-merge-conflict` through staging, continue/merge commit, repeated conflicts, verification, and operation completion.
- Made ordinary follow-up feedback continue in the current conversation; separate implementation, diagnosis, review, and learning boundaries escalate to their respective skills.
- Restricted ADR creation to explicit requests for long-lived repository constraints.
- Added README use scenarios and maintainer-only skill-existence criteria in `AGENTS.md`.

### Validation

- Validate exactly 13 canonical skills: 9 user-invoked and 4 hybrid.
- Split user-invoked `examples` fixtures from hybrid `positive`/`negative` fixtures.
- Validate behavior cases as a required subset with duplicate, required-field, and unknown-skill checks.

## 18.0.4 — Implementation and Browser Contracts

- Added explicit `direct`/`delegated` and TDD strategy approval before `tk-implement` modifies files.
- Restored incremental verification, bounded review, and verified current-branch commit behavior while keeping push and release actions separately authorized.
- Defined single-level implementation delegation and kept MCPs, sandboxes, browsers, and context-management tools available in either execution mode.
- Documented ownership and cleanup rules for browser sessions launched or attached by `tk-browser-verify`.
- Extended static behavior fixtures and repository validation for these contracts.

## 18.0.3 — Korean Skill Documentation

- Localized skill instructions and the README for Korean users while preserving canonical skill names and invocation labels.

## 18.0.2 — Invocation Labels

- Prefixed skill descriptions with `[user]`, `[auto]`, or `[user/auto]` so picker entries communicate their intended invocation.
- Mirrored `[user]` in Codex interface descriptions for explicitly invoked skills.
- Enforced invocation labels in repository validation without renaming skills or changing invocation kinds.

## 18.0.1 — README Invocation Guide

- Distinguished user-invoked, model-invoked, and hybrid skills throughout the README catalog.
- Restored the cute TigerKit cover image and displayed it at the top of the README.
- Updated the immutable installation example to `v18.0.1`.

## 18.0.0 — Agent Skills Reboot

TigerKit 18 is a breaking distribution and runtime reboot.

### Breaking changes

- Ended new support for the Claude Code plugin runtime and removed plugin manifests, command wrappers, central state helpers, legacy schema/evidence machinery, and common emoji output contracts from `main`.
- Switched distribution to 18 self-contained `skills/tk-*/` Agent Skills installed with `npx skills`.
- Added initial host support for Claude Code, Codex, and Hermes Agent.
- Replaced legacy `/tk:*` namespace calls with `tk-*` skill names; see `MIGRATION.md` for the mapping.
- Stopped all automatic discovery or migration of legacy global TigerKit state.
- Moved optional work state to repo/worktree-local `.tigerkit/` scratch with no repo/worktree keys, ledgers, archives, or current pointers.

### Skill catalog

User-invoked: `tk-grill-me`, `tk-grill-with-docs`, `tk-to-spec`, `tk-to-tickets`, `tk-implement`, `tk-prototype`, `tk-reflect`, `tk-learn`, `tk-grooming`, `tk-handoff`.

Hybrid: `tk-browser-verify`.

Model-invoked: `tk-grilling`, `tk-domain-modeling`, `tk-tdd`, `tk-diagnosing-bugs`, `tk-code-review`, `tk-merge-conflict`, `tk-codebase-design`.

### Installation

```bash
npx skills add "MTGVim/tiger-kit#v18.0.0" \
  --global \
  --agent claude-code \
  --agent codex \
  --agent hermes-agent \
  --skill '*'
```

### Attribution

Ten skills are adapted from `mattpocock/skills` and retain their upstream names with the `tk-` prefix. See `NOTICE.md`.

### Release status

This entry is the prepared GitHub Release body. Creating tag `v18.0.0`, publishing the GitHub Release, and any remote push remain separate explicit release actions.
