---
description: requirements/task/API follow-up 상태를 깊게 점검하고 중복과 merge blocker를 보고합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 명령어, 파일 경로, 식별자, 오류 메시지는 원문 그대로 유지할 수 있습니다.

목표: `.tigerkit/{work_id}` ledger가 requirements와 맞는지 deeper audit로 report-only 점검합니다. `/tk:prep`의 light-gap보다 깊고, `/tk:task status`보다 분석적인 command입니다.

## 실행 시점

- 사용자가 명시적으로 호출할 때
- task 상태가 꼬였다고 판단될 때
- API follow-up이 여러 개 쌓였을 때
- requirements 대비 누락이 의심될 때
- merge/review readiness를 따져야 할 때

## 확인 항목

1. requirements 대비 누락 확인
2. task 상태 정리
3. `tasks.index.json`과 `tasks.md` 불일치 확인
4. API follow-up 중복 병합 후보 확인
5. `Shared Blockers` 상태 확인
6. unresolved blocker 확인
7. review/merge readiness 판단

## prep light-gap과 차이

- `/tk:prep` light-gap는 source-to-ledger 직후 sanity pass입니다.
- `/tk:gap`는 이미 존재하는 ledger를 깊게 감사하는 audit gate입니다.
- `/tk:gap`는 granularity, coverage, follow-up duplication, readiness를 더 자세히 봅니다.

## API follow-up 판단

- unresolved `TK-API-*`가 있으면 development progress와 merge readiness를 분리합니다.
- mock 가능으로 완료된 task는 development complete일 수 있습니다.
- unresolved `TK-API-*`는 merge blocker입니다.
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
점검했습니다.
- tasks: done 2, todo 1, review_required 1
- API: TK-API-001 mock_api_contract, merge blocker
- readiness: development OK, merge-ready NO
- 기록: `.tigerkit/search/tasks.md`, `.tigerkit/search/tasks.index.json`

다음 추천: /tk:task status
```

이 명령은 파일을 수정하지 않습니다.