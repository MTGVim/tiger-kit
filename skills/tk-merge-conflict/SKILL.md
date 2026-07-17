---
name: tk-merge-conflict
description: "[user/auto] 진행 중인 merge, rebase, cherry-pick 또는 revert conflict를 의도 기반으로 해결하고 operation을 완료합니다. active conflict가 없는 일반 파일 수정에는 사용하지 않습니다."
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 병합 충돌 해결

merge, rebase, cherry-pick 또는 revert가 실제로 진행 중이고 active conflict가 있을 때만 사용하세요. 일반 파일 수정이나 아직 시작하지 않은 operation에는 사용하지 마세요.

## 계약

편집 전에 operation 상태, `git status`, index의 unmerged 항목, 모든 conflict marker, 양쪽 primary source를 확인하세요. 양쪽 의도를 결정할 근거가 없거나 요구가 양립할 수 없으면 임의로 해결하지 말고 `Blocked`로 중단하세요. 필수 상태나 근거를 읽을 수 없으면 `Unverifiable`입니다.

`Pass`는 모든 marker 제거, unmerged 항목 해소, stage, 관련 검증 실행, operation 완료가 확인된 경우에만 사용하세요. 검증하지 않은 상태나 conflict 파일만 수정한 상태를 완료로 보고하지 마세요.

## 🔴 CHECKPOINT · 🛑 STOP resolution·continue 경계

operation 상태, 모든 conflict hunk, 양쪽 primary source, resolution 근거를 확인하기 전에는 파일을 확정하거나 stage·continue·abort하지 마세요. 근거가 부족하거나 의도가 충돌하면 `Blocked`로 멈추고 필요한 결정을 보고하세요.

## 절차

1. 현재 operation 상태를 확인하세요.
2. conflict 파일과 hunk를 나열하세요.
3. 양쪽 primary source를 조사하세요.
4. 각 side의 의도를 파악하세요.
5. 근거에 따라 hunk를 해결하세요.
6. 관련 없는 변경을 제거하세요.
7. 해결 파일을 stage하세요.
8. 관련 검사를 실행하세요.
9. merge commit 또는 현재 operation의 continue를 수행하세요.
10. 추가 conflict가 생기면 반복하세요.
11. operation 종료와 unmerged path 부재를 확인하세요.

Primary source는 commit message, 관련 issue/PR, spec/ticket, 주변 test, 각 branch의 기존 동작입니다. 가능한 경우 양쪽 의도를 모두 보존하세요. 양립할 수 없으면 현재 operation 목표와 근거에 따라 선택하고 trade-off를 보고하세요. 새로운 동작을 임의로 만들지 마세요.

사용자의 명시적 conflict 해결 요청은 현재 operation 완료까지 허용한 것으로 봅니다. 단, 다음은 자동 실행하지 마세요.

- abort
- `reset --hard`
- `clean`
- force push
- 일반 push
- 근거 없는 대규모 삭제
- 관련 없는 대규모 formatting

## 완료 보고

operation 종류와 상태, conflict 파일, 조사한 의도, resolution, stage/continue 결과, 검증, operation 종료 여부, 남은 후속 작업을 보고하세요. 수행 단계, 핵심 근거, 미검증 항목, 상태(`Pass | Fail | Blocked | Unverifiable`)를 receipt에 포함하세요. Push는 별도 요청이 필요합니다.
