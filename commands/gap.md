---
description: requirements/task/API follow-up 상태를 점검하고 중복과 close/merge blocker를 보고합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 명령어, 파일 경로, 식별자, 오류 메시지는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}` ledger가 requirements와 맞는지 report-only로 점검합니다.

## 실행 시점

- 사용자가 명시적으로 호출할 때
- close 전
- task 상태가 꼬였다고 판단될 때
- API follow-up이 여러 개 쌓였을 때
- requirements 대비 누락이 의심될 때

## 확인 항목

1. requirements 대비 누락 확인
2. task 상태 정리
3. `tasks.index.json`과 `tasks.md` 불일치 확인
4. API follow-up 중복 병합 후보 확인
5. `Shared Blockers` 상태 확인
6. unresolved blocker 확인
7. close/merge readiness 판단

## API follow-up 판단

- unresolved `TK-API-*`가 있으면 development progress와 close/merge readiness를 분리합니다.
- mock 가능으로 완료된 task는 development complete일 수 있습니다.
- unresolved `TK-API-*`는 close/merge blocker입니다.
- 같은 API 문제로 보이는 follow-up이 여러 개 있으면 병합 후보로만 보고하고 자동 병합하지 않습니다.

## 금지

- 구현
- task 자동 생성
- API taxonomy 생성
- follow-up 자동 병합
- commit, push, PR 생성, merge, deploy
- production readiness 최종 선언

## 출력

```text
TigerKit Gap

Tasks:
- done: 2
- todo: 1
- blocked: 0

API Follow-ups:
- TK-API-001 mock_api_contract, merge blocker
- duplicate candidate: 없음

Readiness:
- Development progress: OK
- Merge-ready: NO

No PR opened.
No merge performed.
No remote push performed.
No deploy performed.

다음 추천: /tk:close
```
