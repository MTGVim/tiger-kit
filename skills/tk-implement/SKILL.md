---
name: tk-implement
description: "[user/auto] Implement, test, review, and create one current-branch commit for one independently verifiable unit. Apply only on explicit standalone selection or an exact handoff from tk-drive or tk-pr-respond; never auto-trigger from an ordinary implementation request."
argument-hint: "<request, ticket, or spec> [direct|delegated] [tdd|no-tdd] | --config [--show|--migrate|--reset|--repo]"
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

For active drive or PR response, preserve task identity, unit ID, source IDs, initial `HEAD`, pre-existing dirty paths, and four fields of material verification profile. PR response also preserves repository, PR number, PR head SHA, and exact comment/thread IDs. Follow owner mapping in [review-boundary.md](references/review-boundary.md); never recompute/weaken it. Return unit ID, native status, commit when present, and verification/review evidence to parent. Never emit terminal user result or own cross-unit verification, remote publication, or finalization. A standalone invocation uses its own `## Implement` result and emits no `drive >` or `sweep >` marker; the active parent owns that final orchestration marker.

| Status | Meaning | Commit |
| --- | --- | --- |
| `Pass` | Unit behavior, required tests/checks, and review match final candidate | Exactly one, when separable from user changes |
| `Fail` | Change-related failure, invalid evidence, unauthorized UI drift, or commit failure | None |
| `Blocked` | Required input/authority/decision missing or safe ownership conflicts | None |
| `Unverifiable` | Required verification attempted but cannot establish verdict | None |

A drive non-success handoff includes actual branch/`HEAD`, changed/uncommitted paths, executed/unavailable verification, blocker/failure, and one recovery condition. It grants no cleanup, continuation, commit, downstream specialist, or finalization authority.

## Cost-aware routing

`strategy` and `tier` are independent:

- `strategy`: `direct | delegated` — whether implementation ownership transfers.
- `tier`: `cheap | standard | most_capable` — the lowest sufficient reasoning
  level for the unit.

Ready, independently transferable implementation units default to
`delegated + cheap` on hosts with per-call model support. Use `direct` when
briefing/isolation costs more than implementation, context cannot be safely
transferred, the cause/design/scope is open, or no compatible implementor is
available. Use `standard` for multi-file integration or ordinary debugging;
use `most_capable` or controller recovery for design, unknown-cause, or
security-critical decisions. Escalate once for context, sizing, or reasoning;
do not retry a design decision as a cheaper implementation.

## Model delegation configuration

`$tk-implement --config` manages the host mapping described in
[model-routing.md](references/model-routing.md). `--show` is read-only,
`--migrate` is a real preview/apply flow, not show-only: for Claude Code it
must present one choice from `Map tiers to existing agent types` (Recommended),
`Add effort-only agent definitions`, or `Keep effort: inherit without
definitions`, and wait for the selected option plus explicit apply before
writing,
`--reset` removes that mapping at the selected scope, and `--repo` selects the
current-repository override. Repository override wins over user host context,
which wins over the inherited current model. `per_call_effort` is the exact
three-state capability `per_call | definition_only | unavailable` for an
available adapter; a missing adapter reports `unknown`. `--show` reports each
tier's `resolved implementor`, dispatch model, effective effort, and selection
reason rather than claiming an inert value is applied. Delegated work rejects
read-only candidates, prefers a writable v2 `agent` mapping or stable host
roster match, and records the resolution before dispatch. Claude Code prefers
existing writable agent types; generated definitions have no baked model and
must preserve the Implementor contract. Codex emits the selected implementor,
`model`, and `reasoning_effort` together on every spawn. A required override
that the host cannot satisfy is `Blocked`; an inferred optimization falls back
to safe direct/current execution and is never claimed as applied.
Hermes CLI exposes `--model`, `--reasoning`, and `--provider`, but the current
TigerKit adapter forwards only `-q` and `--toolsets terminal,skills`; it reports
that routing as `unknown`, resolves writable `hermes-chat` only when the
toolset/permission evidence exists, and uses the same safe direct/current or
required-override `Blocked` fallback. CLI support is not claimed as effective
adapter behavior until the wiring and host eval change together.

Once an explicit `$tk-implement` activation or exact active handoff is
accepted, the unit's resolved `direct | delegated` strategy, tier, and
implementor are user-authorized without a second approval. This authorization
is bounded to that unit: `--config` alone never activates implementation or
unrelated dispatch, and a user-required delegation that cannot be satisfied is
still `Blocked`.

## Workflow

1. **Inspect** — resolve source, unit, R/AC or source anchors, branch, initial `HEAD`, relevant code/tests/instructions, and pre-existing dirty paths. For standalone natural-language input, use repository evidence to resolve one target and derive working R/AC; missing paths or prewritten R/AC alone is not `Blocked`. Continue when target and expected behavior are unambiguous; otherwise stop before mutation.
2. **Choose strategy and review route** — select `direct | delegated` by transferability/isolation value, classify risk separately, and determine `required | not-required | unknown-until-diff` Additional review. Choose TDD only with meaningful public-behavior seam.
3. **Implement** — change only unit, prove coherent behavior slices, reach initial green.
4. **Simplify** — run exactly one behavior-preserving reuse/simplicity/ownership pass through [review-boundary.md](references/review-boundary.md).
5. **Verify and review** — apply relevant [execution-gates.md](references/execution-gates.md) sections, run Built-in Standards/Spec review, and exactly one compatible Additional review when required. Resolve accepted blocking findings through bounded fix/verification/scoped-re-review loop in [review-boundary.md](references/review-boundary.md).
6. **Commit and report** — recheck branch, `HEAD`, staged ownership, and evidence; commit once only for `Pass`; update `.tigerkit/implementation.md` and return bounded result.

## Strategy

Inspect before mutation. Decide unspecified `direct | delegated` and `tdd | no-tdd` without approval ceremony. Implementation strategy and product/change risk are separate; delegation implies neither low nor high risk. Record the selected strategy and its reason in the implementation ledger; record the transition and reason when an inferred route falls back.

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

Lead with `## Changed`, then mandatory `## Strategy`, `## Verification`, `## Review`, and optional `## Remaining risks`. `## Strategy` is present in every terminal user-facing result and states `Strategy: direct | delegated` plus `Strategy reason: ...`; delegated work also states `Resolved implementor: ...`. When a route falls back, state `Fallback: delegated -> direct` and `Fallback reason: ...`; otherwise state `Fallback: none`. Include `## Review` in successful/non-successful standalone results: Built-in review, Additional review route or `not required | unavailable`, fix rounds, finding disposition counts, and actual review-driven fixes. Clean small/low-risk result may compress each section to one sentence. Successful unit: 2–5 short behavior-oriented bullets under `Changed`; 1–4 verification-result bullets under `Verification`. If results exceed budget, retain decision-relevant items and cite `.tigerkit/implementation.md`. Record commit once. Summarize commands and results; never paste logs, reviewer prompts, chain of thought, model tiers, provider internals, authentication details, or credentials. Keep detailed mappings/provenance in ledger.

For active drive, return only internal unit ID, status (`Pass | Fail | Blocked | Unverifiable`), resolved strategy/reason/fallback evidence, commit, R/AC references, verification/review evidence, and unverified items.

### 🔴 HARD GATE · terminal user summary

Separate progress commentary, internal procedure evidence, and terminal user response. Begin every terminal user-facing response directly with skill's canonical result heading or, if result schema has no heading, canonical result sentence. Never place standalone separator, ceremonial preamble, or progress recap before opening. Never emit terminal user-summary opening between successful consecutive active-drive procedure invocations.

Never render receipt heading, `Outcome:` label, phase-success token, caller-return instruction, or terminal provenance/status block in user summary. When result requires terminal status, emit single exact `Status: <token>` line in owning result section, not bottom metadata block. Expose path, ID, commit, or recovery detail only when it changes user action or canonical result schema requires it.

Persist provenance only in workflow-owned artifact/ledger. Read-only skill remains read-only. Never require shared runtime reference outside this skill.

### 🔴 HARD GATE · response language

When a user-facing result includes an absolute time, convert it to the user's local timezone and label the timezone; keep raw machine timestamps only in owned evidence. Progress is optional and nonterminal: standalone execution is silent by default; emit `🙋 response/approval needed` only when user action is required, `⏳ wait` only when external waiting is next, or `🚗 meaningful boundary` only for long-running work. Put one space after each marker, omit no-op rows, and keep terminal responses free of progress markers while preserving any required terminal `Status: <token>`.

Before user-facing progress, question, or summary, resolve language from latest explicit user language instruction; otherwise current user message's language. Write every free-form user-facing sentence and prose result value in that language. Never switch to English due to sources, skill bodies, tools, or code. Keep canonical headings, status tokens, IDs, commands, paths, code, and exact quoted/source literals byte-stable; explain around preserved token in resolved language. Before return, scan all free-form user prose and rewrite drift.

## User decision questions

When user-owned decision blocks progress, ask one self-contained `Question` before any `Recommendation`. Show only decision-relevant evidence, two or three mutually exclusive options with material tradeoffs, and exactly one label ending `(Recommended)` or `(추천)`.

Render question, recommendation, and options directly in chat; never call structured question/input tools. Preserve `Pending | Blocked` until answer. This changes presentation, not authority or stop gates.
## Progress

Standalone skills are silent by default. Emit no progress for routine start or success; use `🙋 implement · 응답 필요` only for a user decision/approval, `⏳ implement · 대기` only when external waiting is next, and `🚗 implement · <short state>` only at a meaningful long-running boundary. Omit `tk-` from display names; a parent owns `🚗 parent > implement`. Terminal responses contain no progress marker; keep `Status: <token>` unchanged.
