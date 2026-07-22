# Changelog

## 20.0.0 — Drive-Centered Skill Surface

- Changed the canonical surface to 12 self-contained skills: 2 user-invoked and 10 hybrid.
- Added explicit-start, same-conversation-resumable `tk-drive` with inline one-question ambiguity handling, optional ticket ledger, bounded nested skills, built-in review parity, one final commit, and partial-failure preservation.
- Converted planning, prototype, reflection, learning, grooming, and handoff artifact skills to narrowly triggered hybrid contracts.
- Folded unknown-cause investigation and fixed-point Standards/Spec review into `tk-implement`, then removed their standalone skill surfaces.
- Added deterministic root/nested rule versus repo-skill placement and disposable wide/narrow web A/B/C prototype guidance.

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
- Preserved the 13 canonical skill distribution and runtime-neutral release workflow.

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
