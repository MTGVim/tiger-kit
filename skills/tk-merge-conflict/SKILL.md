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

`Pass`는 아래 Command evidence 표의 모든 completion signal이 확인된 경우에만 사용하세요. 검증하지 않은 상태나 conflict 파일만 수정한 상태를 완료로 보고하지 마세요.

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
7. `receipt`: 입력은 최종 operation 상태와 검증 결과이고, 출력은 `Pass | Fail | Blocked | Unverifiable`, 미검증 항목 및 operation·검증·후속 작업 출력의 참조입니다. 앞선 본문을 복사하지 마세요.

각 단계에서 필수 출력이 없으면 다음 단계로 진행하지 마세요. 추가 conflict가 생기면 `conflict inventory`부터 반복하세요.

### Command evidence

| Evidence | Command contract | Completion signal | Failure route |
|---|---|---|---|
| operation·index 상태 | `git status --short --branch`, `git diff --name-only --diff-filter=U`, `git ls-files -u`를 함께 확인 | operation 종류·step·`HEAD`가 freshness fixed point와 일치하고 unreviewed path가 없음 | stale이면 inventory부터 재작성; 설명 불가면 `Unverifiable` |
| conflict marker | tracked conflict path 전체에서 `^(<<<<<<<|=======|>>>>>>>)` 검색 | marker 0건 | 남은 path와 hunk를 `Fail`; continue 금지 |
| stage | resolution 근거에 기록된 path만 `git add -- <path...>` 후 staged diff·unmerged index 재확인 | 근거 있는 path만 staged, unmerged index 0건 | stage 실패·잔여 unmerged path를 `Fail`; continue 금지 |
| verification | conflict와 관련된 test·build·정적 검사를 실제 실행 | 실행 결과와 범위가 기록되고 변경 관련 실패 없음 | 실행 불가면 `Unverifiable`, 실패면 `Fail` |
| continue | active operation과 일치하는 `git merge --continue`, `git rebase --continue`, `git cherry-pick --continue`, `git revert --continue` 중 하나만 실행 | operation이 의도대로 종료되고 새 conflict 없음 | 실패 출력과 새 inventory를 수집해 conflict inventory부터 반복 |

### Operation freshness gate

첫 inventory에서 operation 종류, 현재 `HEAD`, Git이 제공하는 현재 step·target, unmerged path와 기존 staged path를 fixed point로 기록하세요. resolution 근거에 포함된 path만 stage하고, 새 path가 필요하면 이유와 의도 근거를 inventory에 추가하세요.

검증 직전과 continue 직전에 operation metadata, `HEAD`, `git status`, index를 다시 읽어 fixed point와 비교하세요. operation이 사라지거나 종류·step·`HEAD`가 바뀌었거나, 검토하지 않은 unmerged/staged path 또는 staged content가 생기면 이전 resolution과 검증은 stale입니다. continue하지 말고 실제 상태에서 inventory·intent evidence·검증을 다시 만드세요. drift를 설명하거나 새 상태를 검증할 수 없으면 `Unverifiable`로 멈추고, 사라진 operation을 자신이 완료했다고 보고하지 마세요.

## 실패 경로

- `operation state`에서 active operation이 없으면 이 skill을 적용하지 말고 `Not applicable`로 보고하세요.
- `conflict inventory` 또는 `intent evidence`를 완성할 수 없으면 파일을 stage하거나 수정하지 말고, 빠진 상태·hunk·primary source를 `Unverifiable` 또는 `Blocked`로 보고하세요.
- resolution이 끝난 뒤에도 marker 또는 unmerged 항목이 남거나 stage가 실패하면 continue하지 마세요. `git status`와 index를 다시 확인하고 실패한 명령·남은 경로·검증 결과를 `Fail`로 보고하세요.
- 관련 검증을 실행할 수 없으면 검증을 통과로 표시하지 말고 필요한 명령·권한·환경을 `Unverifiable`로 남기세요.
- continue가 실패하거나 새 conflict를 만들면 operation 종료를 주장하지 말고 실패 출력과 새 inventory를 수집한 뒤 `conflict inventory`부터 반복하세요.

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

`Operation`이 operation 종류·현재 상태·종료 여부를, conflict 파일·조사한 의도·resolution·남은 후속 작업이 각 해당 섹션을, `Stage/continue`가 실행한 stage/continue 명령과 그 직접 결과만, `Verification`이 관련 테스트·marker·index 외 검증 결과만 소유하도록 각각 한 번만 보고하세요. Verification에서 stage/continue 성공을 다시 묶어 쓰지 않고 Stage/continue에서 operation 종료 상태를 다시 판정하지 말며 각 소유 섹션을 참조하세요. Follow-up은 실제로 남은 작업만 기록하고 `push하지 않음`처럼 완료된 비행동 경계를 넣지 마세요. Receipt에는 상태(`Pass | Fail | Blocked | Unverifiable`), 미검증 항목과 앞선 보고 항목의 참조만 기록하고 수행 단계·근거·후속 작업 본문을 반복하지 마세요. Push는 별도 요청이 필요합니다.

## DO NOT / ANTI-PATTERNS

- 근거 없이 한쪽 hunk를 선택하거나 새로운 동작을 임의로 만들지 마세요.
- abort, `reset --hard`, `clean`, force push 또는 일반 push를 자동 실행하지 마세요.
- conflict 파일만 고치고 unmerged path·검증·operation 종료를 확인했다고 보고하지 마세요.
