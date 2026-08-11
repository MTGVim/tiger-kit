---
name: tk-merge-conflict
description: "[user/auto] 의도 증거를 바탕으로 활성 `merge`, `rebase`, `cherry-pick`, `revert` 충돌을 해결하고 작업을 완료합니다. 활성 충돌이 없는 일반 파일 수정에는 적용하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 병합 충돌 해결

충돌이 있는 활성 `merge`, `rebase`, `cherry-pick`, `revert` 중에만 적용합니다. 일반
편집이나 시작되지 않은 작업에는 절대 적용하지 않습니다.

## 계약

편집 전에 작업 상태, `git status`, 병합되지 않은 인덱스 항목, 모든 충돌 표식,
양쪽 주요 원본을 확인합니다. 작업 목표와 주요 원본만으로
의도를 결정할 수 없으면 절대 추측하지 말고 `Blocked` 로 중지합니다. 필수
상태/증거를 읽을 수 없으면 `Unverifiable`입니다.

먼저 활성 작업 표식과 병합되지 않은 인덱스의 존재 여부만 확인합니다. 둘 다
없으면 `Blocked: no active conflict` 를 한 번 보고하고 원본·표식·검사를
하지 않은 채 중지합니다.

명령 증거의 모든 완료 신호를 확인한 뒤에만 `Pass` 를 사용합니다. 충돌 파일만
편집하는 것은 불완전합니다.

## 🔴 체크포인트 · 🛑 중지 · 해결/계속 경계

작업 상태, 모든 충돌 덩어리, 양쪽 주요 원본, 해결 근거를 입증하기 전에는
`finalize`, `stage`, `continue`, `abort`를 절대 하지 않습니다. 근거가 없으면 `Blocked`입니다.
증거가 양립할 수 없는 요구사항 중 하나를 선택하게 하면 절충점을 기록하고
계속합니다.

## 작업 흐름

1. `operation state`: 활성 작업의 `kind`/`state`를 확인합니다.
2. `conflict inventory`: 충돌 경로/덩어리와 병합되지 않은 인덱스 항목을 나열합니다.
3. `intent evidence`: 각 덩어리와 양쪽 주요 원본을 의도/근거에 연결합니다.
4. `resolution`: 각 덩어리의 증거가 뒷받침하는 충돌 파일만 편집합니다.
5. `stage and verify`: 표식/병합되지 않은 항목이 제거됐음을 입증하고, 정확한
   경로를 스테이징한 뒤 관련 검증을 실행합니다.
6. `continue`: 작업에 맞는 계속 명령을 실행하고 결과를 기록합니다.
7. `receipt`: `Pass | Fail | Blocked | Unverifiable`, 미검증 항목,
   `operation`/`verification`/`follow-up` 섹션 참조를 반환하되 내용을 복사하지 않습니다.

## 해결 `receipt` · 단일 증거 기록

모든 해결 실행은 아래 하나의 `receipt`로 남깁니다. 이는 별도 결과 섹션이
아니라 `Operation` → `Resolution` → `Verification` → `Follow-up` 보고의 단일
증거 기록입니다. 알 수 없는 값은 `unavailable` 또는 `not run` 으로 적고
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

필수 선행 출력이 없으면 절대 진행하지 않습니다. 새 충돌이 생기면
`conflict inventory`부터 다시 시작합니다.

의도 분석 전에 인덱스 `stage` 1/2/3을 실제 기준, 현재 커밋, 작업 대상/재생 커밋에
매핑하고 커밋 ID/경로를 기록합니다. 특히 `rebase`/`cherry-pick`/`revert`에서는
`ours`/`theirs`만으로 사용자 브랜치나 원하는 동작을 절대 추론하지 말고 작업
메타데이터와 실제 커밋 내용을 사용합니다.

### 명령 증거

| 증거 | 명령 계약 | 완료 신호 | 실패 경로 |
|---|---|---|---|
| 작업 상태 | `git rev-parse --git-path` 로 `MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD`, `REVERT_HEAD` 를 확인한 뒤 해소된 경로만 검사합니다. | 하나의 활성 작업 종류와 단계가 상태/작업 트리 메타데이터와 일치합니다. | 충돌하거나 읽을 수 없는 표식은 `Unverifiable` 이며, `.git/` 경로로 추론하지 않습니다. |
| 작업/인덱스 | `git status --short --branch`, `git diff --name-only --diff-filter=U`, `git ls-files -u` 를 함께 검사합니다. | 종류, 단계, HEAD가 최신성 고정점과 일치하고 검토하지 않은 경로가 없습니다. | 목록을 다시 만들며, 설명할 수 없는 상태는 `Unverifiable`입니다. |
| 표식 | 모든 추적된 충돌 경로에서 `^(<<<<<<<|=======|>>>>>>>)` 를 검색합니다. | 표식이 0개입니다. | 남은 경로/덩어리는 `Fail` 이며 계속하지 않습니다. |
| 스테이징 | `git add -- <supported-path...>` 를 실행한 뒤 `staged diff`/병합되지 않은 인덱스를 다시 확인합니다. | 증거가 뒷받침하는 경로만 스테이징되고 병합되지 않은 항목이 0개입니다. | 스테이징 실패 또는 잔여 항목은 `Fail` 이며 계속하지 않습니다. |
| 검증 | 관련 테스트·빌드·정적 검사를 실행합니다. | 명령/결과/범위를 기록하고 변경 관련 실패가 없습니다. | 사용할 수 없으면 `Unverifiable`, 실패하면 `Fail`입니다. |
| 계속 | 정확히 하나의 일치하는 `git merge --continue`, `git rebase --continue`, `git cherry-pick --continue`, `git revert --continue` 를 실행합니다. | 새 충돌 없이 작업이 의도대로 종료됩니다. | 실패/새 목록을 기록하고 다시 시작합니다. |

### 작업 최신성 게이트

첫 목록에서 작업 종류, HEAD, Git이 제공한 단계/대상, 병합되지 않은 경로,
기존 `staged` 경로를 고정합니다. 해결 증거에 포함된 경로만 스테이징하며, 새
경로는 목록에 사유/의도 근거가 생긴 뒤에만 추가합니다.

검증/계속 전에 메타데이터, HEAD, 상태, 인덱스를 다시 읽습니다. 작업이
사라지거나 종류/단계/HEAD가 바뀌거나 검토하지 않은 병합되지 않은/`staged` 내용이
생기면 이전 해결은 오래된 것입니다. 목록, 증거, 검증을 다시 만듭니다. 알 수
없는 드리프트는 `Unverifiable` 이며, 사라진 작업을 이번 실행에서
완료했다고 주장하지 않습니다.

## 실패 경로

- 불완전한 목록/의도: 편집/스테이징하지 않고 누락된 상태/덩어리/원본을
  `Unverifiable | Blocked` 로 보고합니다.
- 잔여 표식/병합되지 않은 항목 또는 스테이징 실패: 계속하지 않고 상태/인덱스를
  다시 확인한 뒤 명령, 경로, 검사를 `Fail` 로 보고합니다.
- 사용할 수 없는 검증: 통과로 표시하지 않고 필수 명령/접근/환경을
  `Unverifiable` 로 보고합니다.
- 계속 실패 또는 새 충돌: 완료를 주장하지 않고 출력을 캡처한 뒤 목록을 다시 시작합니다.

주요 원본은 커밋 메시지, `issue`/`PR`, `spec`/`ticket`, 인접 테스트, 확립된
브랜치 동작입니다. 양쪽 의도가 호환되면 모두 보존합니다. 그렇지 않으면
작업 목표/증거를 바탕으로 선택하고 절충점을 보고하며 새로운 동작을
만들지 않습니다.

명시적인 충돌 해결 요청은 활성 작업 완료 권한을 부여하지만, `abort`,
`reset --hard`, `clean`, 강제 `push`, 일반 `push`, 근거 없는 대량 삭제, 관련 없는
서식 수정까지 자동으로 허용하지는 않습니다.

## 완료 보고

비어 있지 않은 섹션만 `Operation`, `Resolution`, `Verification`, `Follow-up` 순서로
사용합니다. `Operation` 은 `kind`, `state`, `stage`, `status`, 미검증 항목, `reference`,
`continue` 결과를 소유하고, `Resolution` 은 충돌, 의도, 선택 결과를 소유하며,
`Verification` 은 테스트·표식·인덱스 검사를 소유합니다. `Follow-up`에는 남은
작업만 적습니다. 원격 반영에는 별도 요청이 필요합니다.

해결한 충돌 경로가 여러 개면 `Resolution` 을 간결한 `Path | Intent | Result`
표로 표시하고, 사용자에게 중요한 행이 하나면 문장으로 씁니다. 해결 결과부터
시작하며 해결 행을 반복하거나 메타데이터를 덧붙이지 않습니다. 복합 의도, 해결한
경로 묶음, 검증을 2~5개의 짧은 행/글머리표로 요약합니다. 경로가 8개 이상이면
상위 5~7개의 의도/결과 행으로 묶고 정확한 나머지 경로를 인용합니다. 할당량이
아니라 예산을 사용합니다.

## 금지 사항 / 안티패턴

- 증거 없이 한쪽을 선택하거나 동작을 만들어내지 않습니다.
- `abort`, `reset --hard`, `clean`, 강제 `push`, `push`를 자동 실행하지 않습니다.
- 병합되지 않은 상태, 검증, 작업 종료를 입증하지 않고 파일을 편집한 뒤
  완료를 주장하지 않습니다.
