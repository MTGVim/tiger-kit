---
name: tk-merge-conflict
description: "[user/auto] intent evidence를 바탕으로 active merge, rebase, cherry-pick, revert conflict를 해결하고 operation을 완료합니다. active conflict가 없는 일반 파일 수정에는 적용하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Merge-conflict 해결

conflict가 있는 active merge, rebase, cherry-pick, revert 중에만 적용합니다. 일반 편집이나 시작되지 않은 operation에는 절대 적용하지 않습니다.

## 계약

편집 전에 operation state, `git status`, unmerged index entry, 모든 conflict marker, 양쪽 primary source를 확인합니다. operation goal과 primary source만으로 intent를 결정할 수 없으면 절대 추측하지 말고 `Blocked`로 중지합니다. 필수 state/evidence를 읽을 수 없으면 `Unverifiable`입니다.

먼저 active-operation marker와 unmerged index 존재 여부만 확인합니다. 둘 다 없으면 `Blocked: no active conflict`를 한 번 보고하고 source, marker, test 조사를 하지 않은 채 중지합니다.

Command evidence의 모든 완료 신호를 확인한 뒤에만 `Pass`를 사용합니다. conflict 파일만 편집하는 것은 불완전합니다.

## 🔴 체크포인트 · 🛑 중지 · resolution/continue 경계

operation state, 모든 conflict hunk, 양쪽 primary source, resolution basis를 입증하기 전에는 finalize, stage, continue, abort를 절대 하지 않습니다. basis가 없으면 `Blocked`입니다. evidence가 양립할 수 없는 요구사항 중 하나를 선택하게 하면 trade-off를 기록하고 계속합니다.

## 작업 흐름

1. `operation state`: active operation의 kind/state를 확인합니다.
2. `conflict inventory`: conflict path/hunk와 unmerged index entry를 나열합니다.
3. `intent evidence`: 각 hunk와 양쪽 primary source를 intent/basis에 연결합니다.
4. `resolution`: 각 hunk의 evidence가 뒷받침하는 conflict 파일만 편집합니다.
5. `stage and verify`: marker/unmerged entry가 제거됐음을 입증하고, 정확한 path를 stage한 뒤 관련 verification을 실행합니다.
6. `continue`: operation에 맞는 continue command를 실행하고 결과를 기록합니다.
7. `receipt`: `Pass | Fail | Blocked | Unverifiable`, 미검증 항목, operation/verification/follow-up section 참조를 반환하되 내용을 복사하지 않습니다.

## resolution receipt · 단일 evidence record

모든 resolution run은 아래 하나의 receipt로 남깁니다. 이는 별도 결과 section이
아니라 `Operation` → `Resolution` → `Verification` → `Follow-up` 보고의 단일
evidence record입니다. 알 수 없는 값은 `unavailable` 또는 `not run`으로 적고
추측하지 않습니다.

```text
Operation: <merge | rebase | cherry-pick | revert> / <state + step>
Repository HEAD: <commit>
Conflict paths: <path list | none>
Index / markers: <unmerged count, marker count>
Intent basis: <source refs and hunk mapping | unavailable>
Resolution: <Path | Intent | Result rows>
Staged: <exact paths | none>
Verification: <checks and result | Unverifiable>
Continue: <exact continue command and result | not run>
Follow-up: <remaining work | none>
Status: Pass | Fail | Blocked | Unverifiable
```

필수 선행 output이 없으면 절대 진행하지 않습니다. 새 conflict가 생기면 `conflict inventory`부터 다시 시작합니다.

intent 분석 전에 index stage 1/2/3을 실제 base, current commit, operation target/replayed commit에 매핑하고 commit ID/path를 기록합니다. 특히 rebase/cherry-pick/revert에서는 `ours`/`theirs`만으로 user branch나 desired behavior를 절대 추론하지 말고 operation metadata와 실제 commit content를 사용합니다.

### 명령 증거

| 증거 | 명령 계약 | 완료 신호 | 실패 경로 |
|---|---|---|---|
| operation state | `git rev-parse --git-path`로 `MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`를 확인한 뒤 resolved path만 검사합니다. | 하나의 active operation kind와 step이 status/worktree metadata와 일치합니다. | 충돌하거나 읽을 수 없는 marker는 `Unverifiable`이며, `.git/` path로 추론하지 않습니다. |
| operation/index | `git status --short --branch`, `git diff --name-only --diff-filter=U`, `git ls-files -u`를 함께 검사합니다. | kind, step, HEAD가 freshness fixed point와 일치하고 검토하지 않은 path가 없습니다. | inventory를 다시 만들며, 설명할 수 없는 state는 `Unverifiable`입니다. |
| markers | 모든 tracked conflict path에서 `^(<<<<<<<|=======|>>>>>>>)`를 검색합니다. | marker가 0개입니다. | 남은 path/hunk는 `Fail`이며 continue하지 않습니다. |
| stage | `git add -- <supported-path...>`를 실행한 뒤 staged diff/unmerged index를 다시 확인합니다. | evidence가 뒷받침하는 path만 stage되고 unmerged entry가 0개입니다. | stage 실패 또는 잔여 entry는 `Fail`이며 continue하지 않습니다. |
| verification | 관련 test/build/static check를 실행합니다. | command/result/scope를 기록하고 변경 관련 failure가 없습니다. | 사용할 수 없으면 `Unverifiable`, 실패하면 `Fail`입니다. |
| continue | 정확히 하나의 일치하는 `git merge --continue`, `git rebase --continue`, `git cherry-pick --continue`, `git revert --continue`를 실행합니다. | 새 conflict 없이 operation이 의도대로 종료됩니다. | failure/new inventory를 기록하고 다시 시작합니다. |

### Operation 최신성 게이트

첫 inventory에서 operation kind, HEAD, Git-provided step/target, unmerged path, 기존 staged path를 고정합니다. resolution evidence에 포함된 path만 stage하며, 새 path는 inventory에 reason/intent basis가 생긴 뒤에만 추가합니다.

verification/continue 전에 metadata, HEAD, status, index를 다시 읽습니다. operation이 사라지거나 kind/step/HEAD가 바뀌거나 검토하지 않은 unmerged/staged content가 생기면 이전 resolution은 stale입니다. inventory, evidence, verification을 다시 만듭니다. 알 수 없는 drift는 `Unverifiable`이며, 사라진 operation을 이 run에서 완료했다고 주장하지 않습니다.

## 실패 경로

- 불완전한 inventory/intent: edit/stage하지 않고 missing state/hunk/source를 `Unverifiable | Blocked`로 보고합니다.
- 잔여 marker/unmerged entry 또는 stage failure: continue하지 않고 status/index를 다시 확인한 뒤 command, path, check를 `Fail`로 보고합니다.
- 사용할 수 없는 verification: passed로 표시하지 않고 required command/access/environment를 `Unverifiable`로 보고합니다.
- continue 실패 또는 새 conflict: 완료를 주장하지 않고 output을 캡처한 뒤 inventory를 다시 시작합니다.

Primary source는 commit message, issue/PR, spec/ticket, adjacent test, established branch behavior입니다. 양쪽 intent가 호환되면 모두 보존합니다. 그렇지 않으면 operation goal/evidence를 바탕으로 선택하고 trade-off를 보고하며 새로운 behavior를 만들지 않습니다.

명시적인 conflict-resolution 요청은 active operation 완료 권한을 부여하지만, abort, `reset --hard`, `clean`, force push, ordinary push, 근거 없는 mass deletion, 관련 없는 formatting까지 자동으로 허용하지는 않습니다.

## 완료 보고

비어 있지 않은 section만 `Operation`, `Resolution`, `Verification`, `Follow-up` 순서로 사용합니다. `Operation`은 kind, state, stage, status, 미검증 항목, reference, continue outcome을 소유하고, `Resolution`은 conflict, intent, 선택 결과를 소유하며, `Verification`은 test, marker, index check를 소유합니다. Follow-up에는 남은 작업만 적습니다. Push에는 별도 요청이 필요합니다.

해결한 conflict path가 여러 개면 `Resolution`을 간결한 `Path | Intent | Result` 표로 표시하고, user-relevant row가 하나면 문장으로 씁니다. 해결 결과부터 시작하며 resolution row를 반복하거나 metadata를 덧붙이지 않습니다. compound intent, 해결한 path group, verification을 2–5개의 짧은 row/bullet로 요약합니다. path가 8개 이상이면 상위 5–7개의 intent/result row로 묶고 정확한 나머지 path를 인용합니다. quota가 아니라 budget을 사용합니다.

## 금지 사항 / ANTI-PATTERNS

- evidence 없이 한쪽을 선택하거나 behavior를 만들어내지 않습니다.
- abort, `reset --hard`, `clean`, force push, push를 자동 실행하지 않습니다.
- unmerged state, verification, operation 종료를 입증하지 않고 파일을 편집한 뒤 완료를 주장하지 않습니다.
