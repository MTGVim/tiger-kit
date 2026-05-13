---
description: 완료/잔여 task, API follow-up, blocker, merge-ready 여부를 handoff로 정리합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 작업 산출물도 한글로 작성합니다. 단, 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}/`의 task ledger를 닫으며 다음 세션 재진입용 handoff와 readiness 판단을 남깁니다.

기본 산출물:
- `.tigerkit/{work_id}/handoff.md`

## 확인 항목

- 완료한 task
- review_required task
- 남은 task
- unresolved API follow-ups
- Shared Blockers
- pending implementation context correction 또는 Clarification Actions
- 검증 상태
- Development progress 여부
- Merge-ready 여부
- 다음 세션 첫 행동

## readiness 정책

```text
unresolved TK-API-* 있음
→ development may be complete
→ merge-ready는 아님
```

API follow-up이 `mock_api_contract`이면 task 자체는 완료됐을 수 있지만 close/merge blocker로 남깁니다. `review_required` task가 남아 있으면 final human approval 전이므로 merge-ready가 아닙니다.

## handoff.md 권장 형식

```md
# TigerKit Handoff

## Done

- T-003 사용자 검색 UI 구현

## Review Required

- T-004 검색 empty state 디자인 검수 필요

## Remaining

- 없음

## Unresolved API Follow-ups

- TK-API-001 사용자 검색 API contract 불명
  - affected: T-003, T-004
  - mock: src/mocks/users.ts
  - merge blocker: true

## Shared Blockers

- 없음

## Readiness

- Development progress: OK
- Merge-ready: NO

## Next Session

- 실제 API contract 확인 후 TK-API-001 처리
```

## 금지

- PR 생성
- branch merge
- remote push
- deploy
- production readiness 최종 선언
- 사용자 승인 없는 branch 생성, commit, 파일 삭제

## 출력

```text
Close Summary

Done:
- T-003 사용자 검색 UI 구현

Unresolved API Follow-ups:
- TK-API-001 사용자 검색 API contract 불명

Readiness:
- Development progress: OK
- Merge-ready: NO

Handoff: `.tigerkit/search/handoff.md`

No PR opened.
No merge performed.
No remote push performed.
No deploy performed.
```
