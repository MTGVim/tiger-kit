---
name: tk-audit
description: "[user] 저장소를 읽기 전용으로 감사하고, 다른 실행자나 `tk-prep`이 재사용할 수 있는 우선순위가 있는 근거 기반 `AUD-*` `finding`을 작성합니다."
license: MIT
argument-hint: "[quick|standard|deep] [security|perf|tests|architecture|branch|next]"
disable-model-invocation: true
metadata:
  tigerkit:
    kind: user-invoked
    origin: shadcn/improve
    upstream-skill: improve
    relationship: adapted
---

# Audit

Use only when `$tk-audit` or `/tk-audit` is explicitly selected.
This is read-only codebase advising and does not modify source, tests, configuration, or history.
소유하는 유일한 산출물은 저장소 로컬의 `.tigerkit/audit.md`입니다.

## Invocation

- `bare`: Audit all categories at standard depth.
- `quick | standard | deep`: Change the depth and bounded coverage.
- `security | perf | tests | architecture`: Focus on one category.
- `branch`: Inspect merge-base changes and direct consumers, and mark `introduced | pre-existing`.
- `next`: Separate evidence-backed direction candidates from defect findings.

Modifiers may be combined. Do not implement, write Seeds, publish issues, or create worktrees.
사용자 소유의 clarification이 필요하면 host별 native structured question surface를 우선 사용합니다 (Claude Code: AskUserQuestion; Codex: request_user_input; Hermes: clarify). unavailable하면 한 번의 clarification을 plain chat으로 fallback하고 read-only boundary를 유지합니다.

## Workflow

1. Read repository instructions, root configuration, verification commands, structure, and relevant Git history.
2. Check the selected categories using [audit-playbook.md](references/audit-playbook.md).
3. Reopen cited evidence to remove duplicates, intended behavior, and incorrect attribution.
4. Sort `finding`s by impact ÷ `effort`, then `confidence`, `fix risk`, and `dependency`.
5. `.tigerkit/audit.md`를 원자적으로 갱신하고 안정적인 `AUD-*` ID와 상태를 보존합니다.

## Failure Paths

- If repository instructions, the selected reference, or required evidence is unavailable, stop that scope and record it as unaudited; do not infer coverage.
- If cited evidence cannot be reproduced at the audited `HEAD`, mark the finding unverifiable or stale and do not claim verification.
- If the scope or modifier is invalid, ask one clarifying question before reading beyond the minimum needed to identify the problem.
- If the atomic `.tigerkit/audit.md` update fails, preserve the existing ledger, report the write failure, and do not fall back to an untracked or global copy.

## Finding Contract

각 열린 finding에는 최소한 다음이 있어야 합니다.

- 안정적인 `AUD-*` ID와 제목
- 범주와 정확한 `path/line` 또는 `symbol` 근거
- 영향, `effort`, `fix risk`, `confidence`
- 관련 진입점과 저장소 관례
- 검증 `baseline`
- 짧은 `fix sketch`
- `dependency/order hint`
- 다음 경로 추천: `prep | investigate | no-action`

`finding`은 후보일 뿐 `Seed`, 티켓, 구현 계획, 승인 자체가 아닙니다.
`secret` 값은 복사하지 않고 위치와 자격 증명 유형만 기록합니다.

## Next-Executor Handoff

모든 finding에는 [executor-handoff.md](references/executor-handoff.md)를 적용합니다.
다음 실행자가 `audit` 대화 없이 이해할 수 있도록 `audited HEAD`, 정확한 경로/`symbol`,
현재 근거, 저장소 규칙, `in/out` 경계, 가정, 검증 명령과 `drift handling`을 포함합니다.

[plan-template.md](references/plan-template.md)의 품질 기준은 이 계약을 보완하지만,
`tk-audit` 자체가 별도 plan lifecycle을 만들지는 않습니다.

작업을 실제로 준비하려면 사용자가 `$tk-prep AUD-003`처럼 현재 `finding`을 출처로 줄 수 있습니다.
`tk-prep`은 `finding`을 현재 저장소 증거와 다시 대조해 실행 가능한 `Seed`로 준비합니다.
`Audit finding`만으로 제품 변경이나 원격 권한이 생기지 않습니다.

## Safety

During a partial audit, do not delete existing findings; mark unaudited scope.
Do not claim verification when the evidence cannot be reproduced at the current HEAD.
`.tigerkit/`은 로컬 scratch이며 전역 archive나 current pointer를 만들지 않습니다.

완료 시 핵심 `finding`과 감사하지 못한 범위를 간결하게 요약합니다.
