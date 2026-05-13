---
name: issue
description: Draft TigerKit task-ledger issue proposals for explicit command-delegated use only. Do not auto-trigger from user natural language; use only when a TigerKit command explicitly needs a human-approved issue/task-ledger draft.
---

# Issue

TigerKit task ledger에 반영할 문제, 디자인 gap, 누락, API follow-up, blocker 후보를 draft로 정리합니다.

## Trigger boundary

자연어 자동 trigger는 없습니다.

- 사용자가 “문제 있음”, “이슈”, “디자인 갭”, “검수 필요”라고 말해도 이 skill을 자동 실행하지 않습니다.
- `/tk:do`, `/tk:next`, `/tk:gap`, `/tk:close` 같은 command가 명시적으로 issue draft가 필요하다고 판단할 때만 사용합니다.
- GitHub issue를 만들지 않습니다.

## 목표

- 현재 구현 momentum을 멈춥니다.
- 발견한 문제를 한 문장으로 재진술합니다.
- task에 섞어 고치지 않고 `.tigerkit/{work_id}/tasks.md` 변경 draft로 캡처합니다.
- TigerKit은 초안만 만듭니다. 최종 wording, task 상태, 승인 여부는 사람이 결정합니다.
- 사용자 승인 없이 코드, task 파일, commit, push, PR, GitHub issue를 만들지 않습니다.

## Workflow

1. 현재 단계와 진행 중 task를 짧게 확인합니다.
2. 제기된 issue를 한 문장으로 다시 씁니다.
3. 코드베이스를 읽어 답할 수 있는 사실은 사용자에게 묻기 전에 확인합니다.
4. 모호함이 남으면 질문을 정확히 하나만 합니다.
5. 아래 중 하나로 scope를 분류합니다.
   - `새 task 후보`
   - `기존 task 수정 후보`
   - `review_required 상태 전환 후보`
   - `TK-API follow-up 후보`
   - `Clarification Action 후보`
   - `Shared Blocker 후보`
6. `tasks.md`/`tasks.index.json` draft wording을 짧게 제안합니다.
7. 최종 반영은 human approval 필요로 표시합니다.

## review_required 기준

아래는 `done` 대신 `review_required` 후보입니다.

- 디자인/UX/Figma/source와 사람이 비교해야 함
- CSS, layout, spacing, color, typography 판단이 필요함
- user-visible copy가 brand/legal/product 판단을 가짐
- `mock_api_contract`로 구현했지만 실제 API contract 미확정
- auth/permission/billing/security 영향 있음
- automated test는 통과했지만 “맞는 경험인지” 검증 불가

## Output

```text
Issue Draft: ...
Scope: 새 task 후보 | 기존 task 수정 후보 | review_required 상태 전환 후보 | TK-API follow-up 후보 | Clarification Action 후보 | Shared Blocker 후보
Ledger draft: ...
Human approval needed: yes
Open question: ...
Next action: ...
```

필요 없는 항목은 `없음`으로 씁니다.

## Rules

- 코드를 수정하지 않습니다.
- 구현을 계속하지 않습니다.
- 긴 design doc을 만들지 않습니다.
- task 파일을 사용자 승인 없이 직접 수정하지 않습니다.
- commit, push, PR, GitHub issue 생성은 사용자 승인 없이 실행하지 않습니다.
- 질문은 한 번에 하나만 합니다.
- 모호함은 terminal `blocked`가 아니라 `Clarification Actions` 후보로 둡니다.
- API 부재가 mock으로 안전하게 진행 가능하면 task blocked가 아니라 `TK-API-*` follow-up 또는 `review_required` 후보로 둡니다.
- 외부에서만 풀 수 있는 상태만 `Shared Blocker` 후보로 둡니다.
