---
name: tk-implement
description: "[user/auto] Implement, test, review, and create one current-branch commit for one independently verifiable unit. Apply only on explicit standalone selection or an exact handoff from tk-drive or tk-pr-respond; never auto-trigger from an ordinary implementation request."
argument-hint: "<request, ticket, or spec> [direct|delegated] [tdd|no-tdd]"
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: implement
    relationship: adapted
---

# Implement

Use only for explicit `/tk-implement`, `$tk-implement`, host-picker selection, exact active `tk-drive` handoff with one ticket or no-ticket unit plus R/AC, or exact active `tk-pr-respond` handoff with one resolution unit, comment/thread IDs, PR head SHA, R/AC, and verification obligations. Ordinary implementation requests, generic continuation, artifacts, or parent-workflow presence alone do not activate it.

## Unit contract

One invocation owns one independently verifiable unit and, after verification/review, exactly one current-branch commit. With tickets: `one ticket = one unit = one commit`. Standalone multi-ticket input must select one ticket or use `$tk-drive`; never recreate drive orchestration.

Explicit user instructions outrank defaults. Never weaken or reconfirm settled scope, method, prohibitions, strategy, verification, or commit instructions. Ask only for conflicting instructions or material decisions required for safe execution.

For active drive or PR response, preserve task identity, unit ID, source IDs, initial `HEAD`, pre-existing dirty paths, and four fields of material verification profile. PR response also preserves repository, PR number, PR head SHA, and exact comment/thread IDs. Follow owner mapping in [review-boundary.md](references/review-boundary.md); never recompute/weaken it. Return unit ID, native status, commit when present, and verification/review evidence to parent. Never emit terminal user result or own cross-unit verification, remote publication, or finalization.

| Status | Meaning | Commit |
| --- | --- | --- |
| `Pass` | Unit behavior, required tests/checks, and review match final candidate | Exactly one, when separable from user changes |
| `Fail` | Change-related failure, invalid evidence, unauthorized UI drift, or commit failure | None |
| `Blocked` | Required input/authority/decision missing or safe ownership conflicts | None |
| `Unverifiable` | Required verification attempted but cannot establish verdict | None |

A drive non-success handoff includes actual branch/`HEAD`, changed/uncommitted paths, executed/unavailable verification, blocker/failure, and one recovery condition. It grants no cleanup, continuation, commit, downstream specialist, or finalization authority.

## Workflow

1. **Inspect** — resolve source, unit, R/AC or source anchors, branch, initial `HEAD`, relevant code/tests/instructions, and pre-existing dirty paths. For standalone natural-language input, use repository evidence to resolve one target and derive working R/AC; missing paths or prewritten R/AC alone is not `Blocked`. Continue when target and expected behavior are unambiguous; otherwise stop before mutation.
2. **Choose strategy and review route** — select `direct | delegated` by transferability/isolation value, classify risk separately, and determine `required | not-required | unknown-until-diff` Additional review. Choose TDD only with meaningful public-behavior seam.
3. **Implement** — change only unit, prove coherent behavior slices, reach initial green.
4. **Simplify** — run exactly one behavior-preserving reuse/simplicity/ownership pass through [review-boundary.md](references/review-boundary.md).
5. **Verify and review** — apply relevant [execution-gates.md](references/execution-gates.md) sections, run Built-in Standards/Spec review, and exactly one compatible Additional review when required. Resolve accepted blocking findings through bounded fix/verification/scoped-re-review loop in [review-boundary.md](references/review-boundary.md).
6. **Commit and report** — recheck branch, `HEAD`, staged ownership, and evidence; commit once only for `Pass`; update `.tigerkit/implementation.md` and return bounded result.

## Strategy

Inspect before mutation. Decide unspecified `direct | delegated` and `tdd | no-tdd` without approval ceremony. Implementation strategy and product/change risk are separate; delegation implies neither low nor high risk.

- Prefer `direct` when any direct condition in [delegation.md](references/delegation.md) applies.
- Consider `delegated` only when every transferability condition there holds and exactly one bounded implementor is available. If inferred delegation unavailable, use direct. If user required it, return `Blocked`.
- For unknown-cause bugs, intermittent failures, or performance regressions, load [investigation.md](references/investigation.md). Never guess-patch; skip full investigation when cause is established.
- Current agent owns final evidence, review, staging, and commit.

## Applicable gates

Load [execution-gates.md](references/execution-gates.md) selectively:

- **Tests/coverage** for behavior changes, bugs, regressions, and repository thresholds.
- **Source UI writing** when source material defines exact user-visible text.
- **Browser verification** for visible UI, interaction, navigation, responsive behavior, or browser final state.
- **Final review/commit** for every unit.

Before mutation and after initial green, use [review-boundary.md](references/review-boundary.md) for design fit, one simplify pass, fixed candidate/staged evidence, review-route selection, finding adjudication, bounded convergence, implementation ledger ownership, and post-commit hook drift. Required-but-unavailable Additional review is `Unverifiable`, never permission to drop obligation.

## CHECKPOINT / STOP

Before editing, stop `Blocked` for conflicting requirements, unsafe authority, unresolved exact UI intent, or required user decision. During execution, apply status table; never convert unavailable evidence into `Pass`.

## Do not

- Never invent source access, test execution, review, or passing evidence.
- Never broaden unit, stage pre-existing user changes, or create extra commits.
- Never nest delegation or let implementor invoke a user-invoked TigerKit skill.
- Never commit non-`Pass` unit or bypass hooks for convenience.
- Never push, open a PR, merge, tag, release, publish, or own parent finalization.

## Commit and result

Commit exactly once only when status is `Pass` and commit is not prohibited. Preserve pre-existing user changes.

Lead with `## Changed`, then `## Verification`, `## Review`, and optional `## Strategy` or `## Remaining risks`. Include `## Review` in successful/non-successful standalone results: implementation strategy, Built-in review, Additional review route or `not required | unavailable`, fix rounds, finding disposition counts, and actual review-driven fixes. Clean small/low-risk result may compress this to one sentence. Successful unit: 2–5 short behavior-oriented bullets under `Changed`; 1–4 verification-result bullets under `Verification`. If results exceed budget, retain decision-relevant items and cite `.tigerkit/implementation.md`. Record commit once. Summarize commands and results; never paste logs, reviewer prompts, chain of thought, model tiers, provider internals, authentication details, or credentials. Keep detailed mappings/provenance in ledger.

For active drive, return only internal unit ID, status (`Pass | Fail | Blocked | Unverifiable`), commit, R/AC references, verification/review evidence, and unverified items.

### 🔴 HARD GATE · terminal user summary

Separate progress commentary, internal procedure evidence, and terminal user response. Begin every terminal user-facing response directly with skill's canonical result heading or, if result schema has no heading, canonical result sentence. Never place standalone separator, ceremonial preamble, or progress recap before opening. Never emit terminal user-summary opening between successful consecutive active-drive procedure invocations.

Never render receipt heading, `Outcome:` label, phase-success token, caller-return instruction, or terminal provenance/status block in user summary. When result requires terminal status, emit single exact `Status: <token>` line in owning result section, not bottom metadata block. Expose path, ID, commit, or recovery detail only when it changes user action or canonical result schema requires it.

Persist provenance only in workflow-owned artifact/ledger. Read-only skill remains read-only. Never require shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before user-facing progress, question, or summary, resolve language from latest explicit user language instruction; otherwise current user message's language. Write every free-form user-facing sentence and prose result value in that language. Never switch to English due to sources, skill bodies, tools, or code. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted/source literals byte-stable; explain around preserved token in resolved language. Before return, scan all free-form user prose and rewrite drift.

## User decision questions

When user-owned decision blocks progress, ask one self-contained `Question` before any `Recommendation`. Show only decision-relevant evidence, two or three mutually exclusive options with material tradeoffs, and exactly one label ending `(Recommended)` or `(추천)`.

Render question, recommendation, and options directly in chat; never call structured question/input tools. Preserve `Pending | Blocked` until answer. This changes presentation, not authority or stop gates.
