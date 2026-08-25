---
name: tk-prep
description: "[user] 명시적인 작업 원천을 저장소 근거와 자연스러운 대화로 구체화하고, 작업 크기에 맞춰 direct/Ready Seed/SDD/handoff를 승인받아 local 구현·검증·commit까지 수행합니다."
disable-model-invocation: true
argument-hint: "<요청 | 이슈 | 버그 | 리뷰 원천>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: adapted
---

# Adaptive Task Preparation

Start only through `/tk-prep`, `$tk-prep`, or explicit host selection; then continue naturally without reinvocation.

Own conversational preparation and, only after the final checkpoint, the approved local execution path. Authority may
cover source/test/config edits, verification, isolated workspace setup, and local task commit(s). It never covers push,
merge, publication/release, destructive cleanup, secrets, or unrelated Git mutation.

**Keep conversation natural and state strict.** Do not expose internal scores, durable-artifact classification, or
execution routing as a form/report. Explain important judgments with recommendations and reasons. When a user-owned
question, choice, or approval is needed, prefer the host's native structured question surface (Claude Code: AskUserQuestion;
Codex: request_user_input; Hermes: clarify). If unavailable, fall back to plain chat; never ask again for a secret or a
parent-owned decision.

## Evidence and questions

Read the task source, instructions, code/callers, tests, commands, Git state, and only materially relevant existing `CONTEXT.md`/ADR/design/domain glossary.
Do not scan or create a documentation lifecycle; if fresher code/test/runtime evidence conflicts, surface it and confirm the source of truth.
Before creating anything, find existing components, helpers, schemas, clients, patterns, and conventions; tie claims to `path:line`, command output, or fresh state.

Ask one highest-impact question at a time only for:

1. user-owned product behavior, scope, priority, or business rules;
2. risky/hard-to-reverse security, permission, data, compatibility, or UX decisions;
3. an engineering exception after evidence shows readiness cannot be improved further.

If evidence or precedent decides, recommend it; only unresolved material hard-to-reverse choices lazy-load [design comparison](references/design.md), and optional fan-out never blocks.

## Workspace safety

Before the final approval, read-only establish:

- repository root, current branch/HEAD, default branch, and linked-worktree state;
- staged, unstaged, and untracked paths;
- whether unrelated user work exists;
- the test commands and browser/server readiness required by the likely execution path.

Never absorb, stage, commit, clean, stash, review, or overwrite unrelated work. Reuse an already safe non-default task
checkout. If execution would start from the default branch, final approval must explicitly cover creation/use of a fresh
isolated task checkout; if the host cannot create or prove one, return `Blocked` before product mutation. Review ranges
and commits belong to that execution checkout only.

## UI text evidence

For any user-visible label, title, tab, option, button, modal, or instruction, record the exact rendered string in quotes,
preserving language, case, punctuation, and spacing. Use the first applicable evidence:

1. current runtime-rendered text for the target environment/locale;
2. a component prop, i18n entry, or option source connected to the render path;
3. a supplied screenshot/reference with provenance;
4. ticket/spec wording;
5. identifier, enum, route, domain term, or i18n key inference — not label evidence.

Dynamic/server text that source cannot determine remains unverified. If no visible label exists, record the entry path
ending in an exact visible title. A value such as `BOTTOM` is valid only when the current render path displays it as-is.
All paths preserve verified literals exactly; conflicting downstream evidence returns to preparation instead of guessing.

## Understanding readiness

Internally score Goal 20%, Context 20%, Scope 15%, Decisions 15%, Acceptance criteria 15%, Verification 15% using only
`0.00 | 0.25 | 0.50 | 0.75 | 1.00`.

```text
ambiguity = 1 - (
  goal*0.20 + context*0.20 + scope*0.15 +
  decisions*0.15 + acceptance*0.15 + verification*0.15
)
```

Do not reach approval until `ambiguity <= 0.20`, every dimension is at least `0.75`, and material blockers/conflicts
are zero. User approval cannot waive this gate. Show scores only when asked why questions continue.

## Engineering and testing readiness

Evaluate Reuse, Simplicity, Testing, Security, and User experience independently as
`준비됨 | 보완 필요 | 개선 한계 | 예외 승인 | 해당 없음`. `준비됨` means at least `0.75`; `해당 없음`
needs a reason. Investigate → improve → reassess before presenting `개선 한계`; only then explain gap/risk/mitigation
and obtain an exception without inflating the score.

For every code-changing path, inspect real tests and load [behavior-first testing](references/testing.md) before approval. Close
observable behavior, regression/RED, focused command, required suite, mutation risk, and `N/A` versus engineering exception.
Do not add ceremonial tests for trivial/prose-only work; browser verification never substitutes for automated protection.
When the cause and exact RED seam are obvious, proceed directly. Lazy-load [diagnosis](references/diagnosis.md) only for hard, flaky, performance, or difficult-to-reproduce bugs and establish a red-capable loop before a fix hypothesis. If that is impossible, record why and do not apply a speculative fix.

## Browser verification

For browser-visible ACs, close target URL/environment, pass conditions, headless viewport/state, safe auth bootstrap,
server command/cwd/readiness, screenshot/redaction evidence, and the `tk-browser-verify` handoff. Default to headless.
Never store usernames, passwords, token, OTP, cookie, or session values in chat/Seed/artifacts; use ephemeral runtime
input. The verifier owns server startup, readiness, runtime acceptance evidence, and cleanup.

## Adaptive execution shape

Choose internally; tell the user the practical consequence, not a classification report.

- durable context `none`: same-session task is small/clear and conversation + repository state are sufficient;
- durable context `seed`: new-session handoff, compaction recovery, lower-capability execution, SDD, or complex
  verification benefits from a self-contained contract;
- execution `direct`: one coherent change/review surface, with or without a Seed;
- execution `sdd`: multiple material Units need independent implementation/review loops; requires a Ready Seed;
- execution `handoff`: prepare a Ready Seed and stop for another session/executor.

Complexity may raise safeguards only: inline direct → Seed direct → SDD/re-prep. Never silently downgrade for convenience.
Direct/no-Seed never loads SDD guidance. Load [private SDD](references/sdd.md) only after SDD is selected.

## Ready Seed contract

Write only `.tigerkit/seed.md`, only after approval, atomically, then reread it. Every new Seed starts with
`<!-- tigerkit:seed -->`, names a deterministic current-task identity, and is `Status: Ready`. It must be self-contained
for a fresh lower-capability executor and preserve:

- source, goal/background, exact checkout/PR head, current evidence/entry points;
- scope/exclusions/do-not-change and approved material decisions/reasons;
- implementation direction and Reuse/Simplicity/Tests/Security/Experience readiness;
- AC with per-AC verification, browser plan, exceptions, traps, and exact UI literals;
- execution recommendation; for SDD, exact `## Execution` grammar from the private protocol.

Never store transcript, provider/model ID, reasoning intensity, secrets, worker/wave routing, receipts, or progress in Seed.

Before approval, preserve any existing Ready Seed byte-for-byte and create no `Status: Pending` file. At approved write
time, replace only a proven TigerKit-owned Seed. For approved direct/no-Seed, remove only a marked stale TigerKit Seed
after confirming it is not current. An unmarked/legacy/identity-ambiguous Seed is never overwritten or deleted; return
`Blocked` before execution.

## 🔴 CHECKPOINT · 🛑 STOP · Approval and local mutation

Before approval perform no source/test/config/Seed/Git mutation. Present one natural summary covering goal, scope,
decisions, approach, testing/TDD, browser plan, execution shape, workspace setup, and local commit consequence.

Approval authorizes exactly the described local edits, verification, isolated checkout setup, and local task commit(s).
It explicitly excludes push, merge, publication/release, destructive cleanup, secrets, and unrelated work. Material
evidence/HEAD/scope drift invalidates approval and returns to preparation.

After approval:

- preparation-only/handoff → write+reread the Ready Seed and stop;
- direct/no-Seed → resolve marked stale Seed safely, then execute without `sdd.md`;
- direct/Seed → write+reread Ready Seed, then execute directly;
- SDD → write+reread grammar-valid Ready Seed, load the private protocol, and execute its Unit/review/fix loops.

## Local execution and completion

Applicable direct changes follow RED → verified failure → minimal GREEN → refactor while green → required relevant checks.
SDD follows the shared protocol. In both paths: preserve scope/UI literals, use the exact review range, run acceptance
review, compose automated regression tests, and create only approved local commit(s). For every browser-visible AC,
invoke `tk-browser-verify` during execution; do not replace the planned handoff with direct browser operation. Browser
verification remains separate from automated regression protection. A repeated blocker after meaningful correction
becomes `Fail | Unverifiable | Blocked`, not an infinite loop.

If material discovery changes Goal/Scope/approved Decision/AC/security/required Verification, stop and re-enter preparation
for revision + reapproval. Reversible engineering ambiguity may be resolved with a visible reason and cost-if-wrong.

Return a compact result: execution shape, Seed path or `none`, commits or handoff status, focused/required verification,
browser evidence status, exceptions, and any blocker. Do not claim remote publication.
