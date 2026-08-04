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

Use only for explicit `/tk-implement`, `$tk-implement`, host-picker selection, an exact active `tk-drive` handoff containing one ticket or no-ticket unit and its R/AC, or an exact active `tk-pr-respond` handoff containing one resolution unit, its comment/thread IDs, PR head SHA, R/AC, and verification obligations. Ordinary implementation requests, generic continuation, artifacts, or parent-workflow presence alone do not activate it.

## Unit contract

One invocation owns one independently verifiable unit and, after verification and review, exactly one current-branch commit. With tickets: `one ticket = one unit = one commit`. Standalone multi-ticket input must select one ticket or use `$tk-drive`; do not recreate drive orchestration.

Explicit user instructions outrank defaults. Do not weaken or reconfirm settled scope, method, prohibitions, strategy, verification, or commit instructions. Ask only when instructions conflict or safe execution requires a material user decision.

For active drive or PR response, preserve task identity, unit ID, source IDs, initial `HEAD`, pre-existing dirty paths, and a material verification profile's four fields. A PR response handoff also preserves repository, PR number, PR head SHA, and exact comment/thread IDs. Follow the owner mapping in [review-boundary.md](references/review-boundary.md); never recompute or weaken it. Return the unit ID, native status, commit when present, and verification/review evidence to the parent. Do not emit a terminal user result or take ownership of cross-unit verification, remote publication, or finalization.

| Status | Meaning | Commit |
| --- | --- | --- |
| `Pass` | Unit behavior, required tests/checks, and review match the final candidate | Exactly one, when separable from user changes |
| `Fail` | Change-related failure, invalid evidence, unauthorized UI drift, or commit failure | None |
| `Blocked` | Required input/authority/decision is missing or safe ownership conflicts | None |
| `Unverifiable` | Required verification was attempted but cannot establish a verdict | None |

A drive non-success handoff includes actual branch/`HEAD`, changed or uncommitted paths, executed and unavailable verification, blocker/failure, and one recovery condition. It grants no cleanup, continuation, commit, downstream specialist, or finalization authority.

## Workflow

1. **Inspect** — resolve source, unit, R/AC or source anchors, branch, initial `HEAD`, relevant code/tests/instructions, and pre-existing dirty paths. For standalone natural-language input, use repository evidence to resolve one target and derive working R/AC; missing paths or prewritten R/AC alone is not `Blocked`. Continue only when the target and expected behavior become unambiguous; otherwise stop before mutation.
2. **Choose strategy and review route** — select `direct | delegated` by transferability and isolation value, classify risk separately, and determine `required | not-required | unknown-until-diff` Additional review. Choose TDD only with a meaningful public-behavior seam.
3. **Implement** — change only the unit, prove coherent behavior slices, and reach initial green.
4. **Simplify** — run exactly one behavior-preserving reuse/simplicity/ownership pass through [review-boundary.md](references/review-boundary.md).
5. **Verify and review** — apply the relevant sections of [execution-gates.md](references/execution-gates.md), run Built-in Standards/Spec review, and run exactly one compatible Additional review when required. Resolve accepted blocking findings through the bounded fix/verification/scoped-re-review loop in [review-boundary.md](references/review-boundary.md).
6. **Commit and report** — recheck branch, `HEAD`, staged ownership, and evidence; commit once only for `Pass`; update `.tigerkit/implementation.md` and return the bounded result.

## Strategy

Inspect before mutation. Decide unspecified `direct | delegated` and `tdd | no-tdd` without an approval ceremony. Implementation strategy and product/change risk are separate axes; delegation never implies either low or high risk.

- Prefer `direct` when any direct condition in [delegation.md](references/delegation.md) applies.
- Consider `delegated` only when every transferability condition there holds and exactly one bounded implementor is available. If inferred delegation is unavailable, fall back to direct. If the user required it, return `Blocked`.
- For unknown-cause bugs, intermittent failures, or performance regressions, load [investigation.md](references/investigation.md). Do not guess-patch; skip the full investigation loop when the cause is already established.
- The current agent owns final evidence, review, staging, and commit.

## Applicable gates

Load [execution-gates.md](references/execution-gates.md) selectively:

- **Tests/coverage** for behavior changes, bugs, regressions, and repository thresholds.
- **Source UI writing** when source material defines exact user-visible text.
- **Browser verification** for visible UI, interaction, navigation, responsive behavior, or browser final state.
- **Final review/commit** for every unit.

Before mutation and after initial green, use [review-boundary.md](references/review-boundary.md) for design fit, one simplify pass, fixed candidate/staged evidence, review-route selection, finding adjudication, bounded convergence, implementation ledger ownership, and post-commit hook drift. Required-but-unavailable Additional review is `Unverifiable`, not permission to drop the obligation.

## CHECKPOINT / STOP

Before editing, stop `Blocked` when requirements conflict, authority is unsafe, exact UI intent is unresolved, or a required user decision remains. During execution, apply the status table without converting unavailable evidence into `Pass`.

## Do not

- Do not invent source access, test execution, review, or passing evidence.
- Do not broaden the unit, stage pre-existing user changes, or create extra commits.
- Do not nest delegation or let an implementor invoke a user-invoked TigerKit skill.
- Do not commit a non-`Pass` unit or bypass hooks for convenience.
- Do not push, open a PR, merge, tag, release, publish, or own parent finalization.

## Commit and result

Commit exactly once only when status is `Pass` and commit is not prohibited. Preserve pre-existing user changes.

Lead with `## Changed`, then `## Verification`, `## Review`, and optional `## Strategy` or `## Remaining risks`. Include `## Review` in successful and non-successful standalone results: report implementation strategy, Built-in review, Additional review route or `not required | unavailable`, fix rounds, finding disposition counts, and actual review-driven fixes. A clean small/low-risk result may compress this to one sentence. For a successful unit, use 2–5 short, behavior-oriented bullets under `Changed` and 1–4 verification-result bullets under `Verification`. When underlying results exceed the budget, keep only the most decision-relevant items and cite `.tigerkit/implementation.md`. Record the commit once. Summarize commands and results; never paste logs, reviewer prompts, chain of thought, model tiers, provider internals, authentication details, or credentials. Keep detailed mappings and provenance in the ledger.

For active drive, return only the internal unit ID, status (`Pass | Fail | Blocked | Unverifiable`), commit, R/AC references, verification/review evidence, and unverified items.

### 🔴 HARD GATE · terminal user summary

Treat progress commentary, internal procedure evidence, and the terminal user response as distinct surfaces. Begin every terminal user-facing response directly with the skill's canonical result heading or, when its result schema owns no heading, its canonical result sentence. Do not emit a standalone separator, ceremonial preamble, or progress recap before that opening. Do not emit a terminal user-summary opening between successful consecutive active-drive procedure invocations.

Do not render a receipt heading, `Outcome:` label, phase-success token, caller-return instruction, or terminal provenance/status block in the user summary. When the result requires a terminal status, emit the single exact `Status: <token>` line in the owning result section instead of a bottom metadata block. Expose a path, ID, commit, or recovery detail only when it changes user action or the canonical result schema requires it.

Persist provenance only in an artifact or ledger already owned by the workflow. A read-only skill remains read-only. Never require a shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

Before any user-facing progress, question, or summary, resolve the response language from the latest explicit user language instruction; otherwise use the current user message's language. Write every free-form user-facing sentence and every prose result value in that resolved language, and do not switch to English because sources, skill bodies, tools, or code are English. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted or source literals byte-stable; explain them in the resolved language around the preserved token. Before returning, scan all free-form user-facing prose and rewrite any sentence that drifts from the resolved language.

## User decision questions

When a user-owned decision blocks progress, ask one self-contained `Question` before any `Recommendation`. Show only decision-relevant evidence, two or three mutually exclusive options with material tradeoffs, and exactly one label ending `(Recommended)` or `(추천)`.

Render the question, recommendation, and options directly in the chat response; do not call structured question or input tools. Preserve `Pending | Blocked` until the user answers. This changes presentation, not authority or stop gates.
