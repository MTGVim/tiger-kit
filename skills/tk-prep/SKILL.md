---
name: tk-prep
description: "[user] 명시적인 작업 원천을 저장소 근거와 자연스러운 대화로 구체화해, 새 세션이나 더 낮은 수준 실행자가 원 대화 없이 사용할 수 있는 `.tigerkit/seed.md`를 준비합니다."
disable-model-invocation: true
argument-hint: "<요청 | 이슈 | 버그 | 리뷰 원천>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Task Preparation

Start only through `/tk-prep`, `$tk-prep`, or explicit skill selection by the host.
Do not implement the current task. Prepare repository evidence and user decisions as one executable `.tigerkit/seed.md`.
Once the interview starts, continue it naturally in the same conversation without requiring the skill to be invoked again after every answer.

**Keep conversation natural and state strict.** Do not dump internal scores, stages, or classifications into the default view.
Do not ask again about confirmed information. Explain important judgments with the plan and rationale so the user can revise them during the conversation.
사용자 소유의 질문·선택·승인이 필요하면 host별 native structured question surface를 우선 사용합니다 (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). unavailable하면 같은 결정을 plain chat으로 fallback하고 secret을 넘기거나 parent-owned 결정을 다시 묻지 않습니다.
Do not modify source, tests, configuration, Git, or remote state.

## Evidence and Questions

Read the task source, repository instructions, relevant code, tests, verification commands, and current branch/HEAD as needed.
Before creating anything new, look for existing `component`, `hook`, `helper`, `token`, `type`, `schema`, `client`, screen patterns, and repository conventions.
Do not invent unsupported facts. When possible, connect important repository claims to `path:line`, command output, or current state.

Ask the user directly only about:

1. User-owned decisions such as product behavior, scope, priority, and business rules
2. Risky or hard-to-reverse decisions involving security, permissions, data, or compatibility
3. Exception approval when engineering readiness cannot be improved further despite sufficient effort

If the source already determines the outcome, do not turn it into another choice question.
Ask only the single highest-impact decision at a time. First briefly explain the current understanding, recommendation, and rationale.

## Understanding Readiness

Internally evaluate these six dimensions.

| Dimension | Weight |
| --- | ---: |
| Goal | 20% |
| Context | 20% |
| Scope | 15% |
| Decisions | 15% |
| Acceptance criteria | 15% |
| Verification | 15% |

Use only `0.00 | 0.25 | 0.50 | 0.75 | 1.00`.
`0.00` means no evidence, `0.25` means partial clues, `0.50` means material gaps, `0.75` means executable, and `1.00` means sufficiently closed.

```text
ambiguity = 1 - (
  goal*0.20 + context*0.20 + scope*0.15 +
  decisions*0.15 + acceptance*0.15 + verification*0.15
)
```

Do not end the interview until all of the following are satisfied.

```text
ambiguity <= 0.20
every dimension >= 0.75
material blockers == 0
unresolved material conflicts == 0
```

User approval cannot bypass this gate. Show a concise diagnosis only when the user asks about the score or why questions continue.

## Engineering Readiness

Evaluate these five dimensions individually; do not offset weaknesses by averaging.

- **Reuse**: Were existing components and repository conventions investigated sufficiently?
- **Simplicity**: Does the approach avoid speculative branches, future abstractions, dependencies, and dead code unnecessary for the current AC?
- **Testing**: Does the plan cover regressions, bug reproduction, new non-trivial behavior, and existing integration checks?
- **Security**: Does it safely address applicable boundaries such as `auth`, `authz`, input, secrets, uploads, redirects, and storage?
- **User experience**: Does it consider responsive states, keyboard use, focus, semantic structure, accessibility, and visual consistency for user-visible changes?

Use the same score units and these Korean statuses for every dimension.

`준비됨 | 보완 필요 | 개선 한계 | 예외 승인 | 해당 없음`

`준비됨` means `0.75+`. `해당 없음` requires a reason.
For any deficient dimension, first investigate further → improve the approach → reassess. Only if it still cannot be improved, explain `개선 한계`, including the gap, reason, and mitigation, then obtain user exception approval.
Do not raise the original score after exception approval.

## Browser Verification

If there are `browser-visible` ACs, close the following strategy before the `Seed`.

- Target URL/environment and pass conditions
- Whether to use `headless`, plus `viewport` and state
- Whether authentication is required, and a safe `session`/`token`/non-interactive login path
- Development server command, working directory, and readiness signal
- Required `screenshot` evidence and sensitive-screen redaction policy
- Whether to use `tk-browser-verify`

Default to `headless`. Do not store usernames, passwords, `token`, OTP, `cookie`, or `session` secrets in the `Seed` or chat; handle them only as ephemeral runtime input.
If a development server is required, plan for `tk-browser-verify` to own startup, readiness checks, and cleanup.

## `Seed` Contract

Use only `.tigerkit/seed.md` at the repository root as the current task context.
The final `Seed` must let a lower-level executor in a new session, without the original conversation, begin the correct work from only the instruction “진행해”.

Preserve all required meaning self-containedly.

- 작업 원천·목표·배경과 현재 브랜치/HEAD 또는 정확한 `PR head`
- 현재 상태, 주요 진입점, 관련 저장소 근거와 관례
- 포함/제외/변경 금지 범위
- 모든 사용자 승인 중요 결정과 이유
- 합의한 구현 접근, 재사용/단순성/테스트/보안/사용자 경험 판단
- AC와 각 AC의 검증 경로
- 브라우저 검증 계획과 엔지니어링 예외
- 낮은 수준 실행자에게 필요한 구현 안내, 함정, 금지 접근
- 실행 형태와 모델 수준에 대한 추천
- 미해결 항목

Do not include the full conversation, `worker`/`wave` progress state, provider model selectors, model IDs, reasoning intensity, receipts, or secrets.
Execution recommendations should remain advice at the level of “독립 작업 `fan-out` 가능”, “중간급 `coding model` 권장”, or “더 강한 최종 검토 권장”.
The current `host`/`agent` determines the actual execution form, but AC and Verification are binding contracts.

## 🔴 CHECKPOINT · 🛑 STOP · Ready and Evolution

Treat the following as a hard stop: do not write `Status: Ready` or begin implementation until every condition below is true.

During the interview, the `Seed` remains `Status: Pending`. Change it to `Status: Ready` only after all of the following are satisfied and the user approves the final natural-language summary.

```text
Understanding Gate pass
Engineering Gate pass or valid user waiver
no material blocker
user final approval
seed write + reread + self-contained check
```

Do not alter a Ready `Seed` for implementation convenience. If new evidence during execution or verification materially breaks the goal, scope, decisions, AC, or required verification, re-enter `tk-prep`, update only the affected parts, and obtain renewed approval.
Suggest recurring repository pitfalls only as candidates for improvement in repository-native owners such as tests, types, schemas, policies, or code invariants; do not promote them automatically.
Recurring failures in TigerKit skills are candidates for `tk-skill-diagnose`/`tk-learn`; do not create a separate permanent pitfall collection.

완료 시 `Seed` 경로와 핵심 합의·검증·실행 추천을 짧게 알려주고 구현을 자동 시작하지 않습니다.
