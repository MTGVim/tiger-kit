---
description: 코드 리뷰 피드백을 검증하고, 맞는 것만 순서대로 반영합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 명령어, 파일 경로, reviewer 코멘트, 오류 메시지는 원문 그대로 유지할 수 있습니다.

목표: 받은 코드 리뷰 피드백을 감정적으로 받아치지 않고, 기술적으로 검증한 뒤 맞는 항목만 순서대로 반영합니다. 코드 수정이 포함되면 검증 통과 후 local commit으로 남깁니다.

## 기본 원칙

- 검증 전 수용 금지
- 모호한 피드백은 구현 전에 clarification
- reviewer가 틀릴 수 있다고 가정하되, 무시하지는 않음
- performative agreement 금지

피할 표현:
- "완전히 맞습니다"
- "좋은 포인트네요"
- "바로 반영하겠습니다"

대신:
- 요구사항을 기술적으로 다시 적기
- 코드베이스 현실과 맞는지 검증하기
- 맞으면 고치기
- 틀리면 근거를 들어 되묻기

## 처리 순서

1. 피드백 전체를 끝까지 읽습니다.
2. 각 항목을 자기 말로 기술적으로 다시 적습니다.
3. unclear item이 하나라도 있으면 먼저 질문합니다.
4. 코드베이스와 현재 diff 기준으로 검증합니다.
5. 맞는 항목만 하나씩 고칩니다.
6. 각 수정 뒤 검증합니다.
7. 코드 수정이 포함됐고 검증이 통과했으면 관련 변경 파일만 stage해 새 commit을 만듭니다.
8. 완료/보류/반박 항목을 나눠 짧게 보고합니다.

## 구현 순서 권장

- blocking issue
- security/correctness
- simple fix
- complex refactor

## 반박이 필요한 경우

- reviewer가 맥락을 놓침
- suggestion이 기존 기능을 깨뜨림
- YAGNI
- stack/compatibility와 충돌
- human partner의 prior decision과 충돌

이 경우에는 기술 근거를 짧게 제시합니다.

## 출력

기본 출력은 `Review Response`입니다.

반드시 포함:
- Clarified items
- Fixed
- Rejected or questioned
- Verification
- Commit
- `다음 추천: /tk:do`, `/tk:do-all`, 또는 `/tk:review`

코드 수정이 포함된 review fix의 local commit은 검증 통과 후 수행합니다. push, PR 생성, branch 생성은 사용자 승인 없이 실행하지 않습니다.
