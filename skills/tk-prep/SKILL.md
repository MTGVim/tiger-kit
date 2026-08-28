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

**Keep conversation natural and state strict.** Do not expose durable-artifact classification or
execution routing as a form/report. Explain important judgments with recommendations and reasons. When a user-owned
question, choice, or approval is needed, prefer the host's native structured question surface (Claude Code: AskUserQuestion;
Codex: request_user_input; Hermes: clarify). If unavailable, fall back to plain chat; never ask again for a secret or a
parent-owned decision.

## Evidence and questions

Read the task source, instructions, code/callers, tests, commands, Git state, and only materially relevant existing
domain context. Lazy-load [domain context](references/domain-context.md) only when the work uses project-specific terms.
Do not scan or create a documentation lifecycle; if fresher code/test/runtime evidence conflicts, surface it and confirm the source of truth.
Before creating anything, find existing components, helpers, schemas, clients, patterns, and conventions; tie claims to `path:line`, command output, or fresh state. Before comparing a hard-to-reverse design, interface, schema, or migration choice, read only relevant ADR rationale and current evidence. Do not reopen a decision whose premise still holds; surface `revisit ADR` only when it changed, and never scan an unrelated ADR or context tree.

Ask one highest-impact question at a time only for:

1. user-owned product behavior, scope, priority, or business rules;
2. risky/hard-to-reverse security, permission, data, compatibility, or UX decisions;
3. an engineering exception after evidence shows readiness cannot be improved further.

If evidence or precedent decides, recommend it; only unresolved material hard-to-reverse choices lazy-load [design comparison](references/design.md), and optional fan-out never blocks.

If the approved outcome may include local implementation, read [local execution](references/local-execution.md) before
the final checkpoint. It owns checkout isolation, unrelated-work protection, direct execution, review, and local commit.
If user-visible text is in scope, read [UI text evidence](references/ui-text.md) before accepting or restating a label.

## Understanding readiness

Do not reach approval until the goal and scope are actionable, every material product/user-owned decision is resolved,
acceptance and verification are executable, and no material evidence conflict or blocker remains. User approval cannot
waive an evidence conflict or readiness blocker.

## Engineering and testing readiness

Evaluate Reuse, Simplicity, Testing, Security, and User experience independently as
`준비됨 | 보완 필요 | 개선 한계 | 예외 승인 | 해당 없음`. `해당 없음` needs a reason. Investigate → improve → reassess
before presenting `개선 한계`; only then explain gap/risk/mitigation and obtain an exception.

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

Choose only after repository investigation establishes a concrete implementation topology; tell the user the practical consequence, not a classification report.
Ticket length, raw file count, or the presence of both UI and API work never decides the shape.

- durable context `none`: same-session task is small/clear and conversation + repository state are sufficient;
- durable context `seed`: new-session handoff, compaction recovery, lower-capability execution, SDD, or complex
  verification benefits from a self-contained contract;
- execution `direct`: one coherent implementation/test/review judgment surface, including small same-shape changes that can be reviewed together, with or without a Seed;
- execution `sdd`: multiple material Units need independent implementation/test/review judgment loops; requires a Ready Seed;
- execution `handoff`: prepare a Ready Seed and stop for another session/executor.

Complexity may raise safeguards only: inline direct → Seed direct → SDD/re-prep. Never silently downgrade for convenience.
Direct/no-Seed never loads SDD guidance. Load [private SDD](references/sdd.md) only after SDD is selected.

When durable context is `seed`, execution is `sdd`, or the outcome is `handoff`, read the [Ready Seed contract](references/seed.md)
before approval. Preserve any existing Seed before approval; direct/no-Seed does not load the Seed contract merely to create ceremony.

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

For local execution, follow the already loaded local-execution reference. SDD additionally follows the private SDD
protocol. Return a compact result with the execution shape, Seed path or `none`, commits or handoff status, focused and
required verification, browser evidence, exceptions, review independence, and any blocker. Never claim remote publication.
