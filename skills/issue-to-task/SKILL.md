---
name: issue-to-task
description: Turn mid-work issue reports into TigerKit task insertions, Clarification Actions, or Shared Blockers without continuing implementation. Use when the user flags wrong direction, UI/design mismatch, missing requirements, scope concern, or newly discovered work during `/tk:do`, `/tk:do-all`, `/tk:review`, `/tk:review-fix`, or similar active workflow steps.
---

# Issue To Task

진행 중 제기된 이슈를 구현 계속 진행이 아니라 TigerKit workflow로 다시 넣습니다.

## 목표

- 사용자가 “이 방향이 틀림”, “UI 디자인이 잘못됨”, “이 요구가 빠짐”처럼 course correction을 제기하면 즉시 구현 momentum을 멈춥니다.
- 이슈를 작은 task, 기존 task 수정, `Clarification Actions`, 또는 `Shared Blockers` 중 하나로 분류합니다.
- 바로 해결하지 말고 `/tk:plan`으로 돌아가 실행계획과 task queue에 반영하게 합니다.

## Workflow

1. 현재 단계와 진행 중 task를 짧게 확인합니다.
2. 사용자가 제기한 이슈를 한 문장으로 다시 씁니다.
3. 코드베이스를 읽어 답할 수 있는 사실은 사용자에게 묻기 전에 확인합니다.
4. 모호함이 남으면 질문을 정확히 하나만 합니다.
5. 필요할 때만 2-3개 task framing을 제시하고 trade-off를 짧게 씁니다.
6. 아래 중 하나로 분류합니다.
   - `Task insertion`: 새 일반 task로 끼워 넣어야 함
   - `Task revision`: 진행 중이거나 기존 task의 완료 기준을 바꿔야 함
   - `Clarification Action`: `TK-CLARIFY-*`로 요구사항 모호함을 걷어내야 함
   - `Shared Blocker`: 외부 의존, 권한, API/contract, human decision이 필요함
7. 제안 wording을 짧게 보여주고, 다음 행동을 `/tk:plan`으로 둡니다.

## Output

아래만 짧게 출력합니다.

```text
Issue: ...
Classification: Task insertion | Task revision | Clarification Action | Shared Blocker
Proposed queue change: ...
Open clarification: ...
다음 추천: /tk:plan
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
- 외부에서만 풀 수 있는 상태만 `Shared Blockers` 후보로 둡니다.
- 이미 명확한 이슈면 질문 없이 적절한 분류의 queue wording을 제안합니다.
