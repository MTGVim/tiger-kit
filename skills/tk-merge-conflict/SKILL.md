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

편집 전에 operation 상태, `git status`, index의 unmerged 항목, 모든 conflict marker, 양쪽 primary source를 확인하세요. 양쪽 의도를 결정할 근거가 없고 operation 목표·primary source로도 선택할 수 없으면 임의로 해결하지 말고 `Blocked`로 중단하세요. 필수 상태나 근거를 읽을 수 없으면 `Unverifiable`입니다.

`Pass`는 모든 marker 제거, unmerged 항목 해소, stage, 관련 검증 실행, operation 완료가 확인된 경우에만 사용하세요. 검증하지 않은 상태나 conflict 파일만 수정한 상태를 완료로 보고하지 마세요.

## 🔴 CHECKPOINT · 🛑 STOP resolution·continue 경계

operation 상태, 모든 conflict hunk, 양쪽 primary source, resolution 근거를 확인하기 전에는 파일을 확정하거나 stage·continue·abort하지 마세요. 근거가 부족하고 operation 목표·primary source로도 선택할 수 없으면 `Blocked`로 멈추세요. 요구가 양립하지 않더라도 근거로 선택할 수 있으면 trade-off를 기록하고 절차를 계속하세요.

## Workflow

각 단계의 출력이 다음 단계의 입력이 되도록 진행하세요.

1. `operation state`: 입력은 현재 저장소와 사용자의 conflict 요청이고, 출력은 진행 중인 operation 종류와 상태입니다.
2. `conflict inventory`: 입력은 operation 상태이고, 출력은 conflict 파일·hunk·index의 unmerged 항목 목록입니다.
3. `intent evidence`: 입력은 각 conflict hunk와 양쪽 primary source이고, 출력은 양쪽 의도와 resolution 근거입니다.
4. `resolution`: 입력은 hunk별 근거와 operation 목표이고, 출력은 관련 없는 변경 없이 수정된 conflict 파일입니다.
5. `stage and verify`: 입력은 수정된 파일과 관련 검증 기준이고, 출력은 marker 제거·unmerged 항목 해소·stage 및 검증 결과입니다.
6. `continue`: 입력은 검증된 index와 현재 operation이고, 출력은 merge commit 또는 operation의 continue 결과입니다.
7. `receipt`: 입력은 최종 operation 상태와 검증 결과이고, 출력은 종료 여부·남은 conflict·후속 작업을 포함한 상태 보고입니다.

각 단계에서 필수 출력이 없으면 다음 단계로 진행하지 마세요. 추가 conflict가 생기면 `conflict inventory`부터 반복하세요.

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

## DO NOT / ANTI-PATTERNS

- 근거 없이 한쪽 hunk를 선택하거나 새로운 동작을 임의로 만들지 마세요.
- abort, `reset --hard`, `clean`, force push 또는 일반 push를 자동 실행하지 마세요.
- conflict 파일만 고치고 unmerged path·검증·operation 종료를 확인했다고 보고하지 마세요.
