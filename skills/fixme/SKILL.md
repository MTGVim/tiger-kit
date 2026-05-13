---
name: fixme
description: Capture mid-work discoveries of wrong, incomplete, or mismatched implementation as TigerKit task-ledger change candidates without immediately fixing them. Use when the user says something is implemented wrong, missing, mismatched with requirements/design, or needs to be fixed during `/tk:do`, `/tk:next`, `/tk:gap`, `/tk:close`, or similar active TigerKit steps.
---

# Fixme

진행 중 발견한 잘못 구현됨, 누락됨, 요구사항 또는 디자인과 다름, 고쳐야 함 같은 신호를 즉시 구현하지 않고 `.tigerkit/{work_id}/tasks.md` ledger 변경 후보로 되돌립니다.

## 목표

- 현재 구현 momentum을 멈춥니다.
- 발견한 수정 필요사항을 한 문장으로 재진술합니다.
- 현재 task에 섞어 고치지 않고 task ledger 변경 후보로 캡처합니다.
- 사용자 승인 없이 코드, task 파일, commit, push, PR을 만들지 않습니다.
- 수정사항의 scope에 맞는 다음 행동을 추천합니다.

## Workflow

1. 현재 단계와 진행 중 task를 짧게 확인합니다.
2. 사용자가 발견한 fixme를 한 문장으로 다시 씁니다.
3. 코드베이스를 읽어 답할 수 있는 사실은 사용자에게 묻기 전에 확인합니다.
4. 모호함이 남으면 질문을 정확히 하나만 합니다.
5. 필요할 때만 2-3개 task-ledger framing과 trade-off를 짧게 제시합니다.
6. 아래 중 하나로 scope를 분류합니다.
   - `새 task 후보`
   - `기존 task 수정`
   - `TK-API follow-up 후보`
   - `Clarification Action 후보`
   - `Shared Blocker 후보`
7. `tasks.md`/`tasks.index.json` wording을 짧게 제안하고 scope에 맞는 다음 행동을 추천합니다.

## Next recommendation

- `새 task 후보` 또는 `기존 task 수정`: task ledger 갱신 승인 요청
- `TK-API follow-up 후보`: API Follow-ups 갱신 승인 요청
- `Clarification Action 후보`: targeted question
- `Shared Blocker 후보`: blocker 해소 action
- 상태만 다시 봐야 하면 `다음 추천: /tk:next` 또는 `/tk:gap`

## Output

```text
Fixme: ...
Scope: 새 task 후보 | 기존 task 수정 | TK-API follow-up 후보 | Clarification Action 후보 | Shared Blocker 후보
Ledger change: ...
Open question: ...
Next action: ...
```

필요 없는 항목은 `없음`으로 씁니다.

## Rules

- 코드를 수정하지 않습니다.
- 구현을 계속하지 않습니다.
- 긴 design doc을 만들지 않습니다.
- task 파일을 사용자 승인 없이 직접 수정하지 않습니다.
- commit, push, PR 생성은 사용자 승인 없이 실행하지 않습니다.
- 질문은 한 번에 하나만 합니다.
- 모호함은 terminal `blocked`가 아니라 `Clarification Actions` 후보로 둡니다.
- API 부재가 mock으로 안전하게 진행 가능하면 task blocked가 아니라 `TK-API-*` follow-up 후보로 둡니다.
- 외부에서만 풀 수 있는 상태만 `Shared Blocker` 후보로 둡니다.
