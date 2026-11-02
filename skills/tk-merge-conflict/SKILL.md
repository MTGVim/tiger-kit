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

<a id="resolve-merge-conflicts"></a>
# merge 충돌 해결

<a id="shared-references"></a>
## 공통 참조

현재 설치된 담당 스킬에서 해당 분기의 조건에 따라 기준을 읽습니다. 소유자나 자원이 없거나 일치하지 않으면
해당 작업을 중단합니다. 기억, 다른 설치본이나 승인되지 않은 설치 대신 `tk-setup-skills`를 사용합니다.
참조 읽기는 워크플로 실행이나 변경 권한을 부여하지 않습니다.

- 사용자 소유 결정·누락된 승인·미충족 선행 조건을 질문이나 질문 도구 입력으로 제시하기 직전에 [질문 라운드](../tk-questioning/references/questions.md)를 이번 작업에서 읽었는지 확인하고 누락했으면 먼저 읽습니다. 독립적인 결정과 승인은 각각 별도 질문으로 두며, 승인 선택지를 결정 질문에 섞지 않습니다.
- 사용자에게 완료 보고, 산출물 경로 인계나 여러 속성을 비교하는 대화 응답을 전달하기 전에 [대화 전달](../tk-writing/references/delivery.md)을 읽습니다. 작업별 구체적인 출력 계약이 우선합니다.

<a id="approval-continuity"></a>
## 승인 연속성

같은 작업에 대한 유효한 승인을 턴과 자식 단계(baseline/after 포함) 전반에 재사용하고,
기존 담당자를 통해 승인된 작업만 계속합니다. 자식·baseline 근거를 반환하고 승인된 담당 작업을 재개합니다.
단계 상태는 완료를 뜻하지 않습니다. 새로운 중대한 결정, 범위·권한 변경이나 사용자만 제공할 수 있는
입력이 누락된 경우에만 질문합니다. 호출과 복구된 산출물은 권한을 부여하지 않습니다. 원격 작업과
파괴적 작업에는 행동·대상에 대한 명시적 승인이 필요하며, 로컬 승인에서 추론하지 않습니다.

충돌이 있는 활성 `merge`, `rebase`, `cherry-pick` 또는 `revert` 중에만 적용합니다.
일반 수정이나 아직 시작하지 않은 작업에는 적용하지 않습니다.

<a id="contract"></a>
## 계약

수정 전에 작업 상태, `git status`, 병합되지 않은 index 항목, 모든
충돌 마커와 양쪽 1차 출처를 확인합니다. 작업 목표와 1차 출처로
의도를 확정할 수 없다면 추측하지 말고 `Blocked`로 중단합니다. 필요한 상태나 근거를
읽을 수 없다면 결과는 `Unverifiable`입니다.

먼저 활성 작업 마커와 병합되지 않은 index 항목만 확인합니다. 둘 다
없다면 `Blocked: no active conflict`를 한 번 보고하고, 출처,
마커나 검사를 살펴보지 않은 채 중단합니다.

명령 근거에서 모든 완료 신호를 확인한 뒤에만 `Pass`를 사용합니다.
충돌 파일만 수정한 상태는 완료가 아닙니다.

<a id="-checkpoint---stop--resolvecontinue-boundary"></a>
## 🔴 점검 지점 · 🛑 중단 · 해결/계속 경계

작업 상태, 모든 충돌 hunk, 양쪽 1차 출처와 해결 근거를 입증하기 전에는
`finalize`, `stage`, `continue`, `abort`를 수행하지 않습니다.
근거가 없으면 결과는 `Blocked`입니다. 근거에 따라 양립할 수 없는 요구사항 중 하나를
선택해야 한다면 절충을 기록하고 계속합니다.

<a id="workflow"></a>
## 워크플로

1. `operation state`: 활성 작업의 `kind`/`state`를 식별합니다.
2. `conflict inventory`: 충돌 경로·hunk와 병합되지 않은 index 항목을 나열합니다.
3. `intent evidence`: 각 hunk와 양쪽 1차 출처를 의도·근거에 대응시킵니다.
4. `resolution`: hunk에 근거가 있는 충돌 파일만 수정합니다.
5. `stage and verify`: 해결된 내용에 실제 충돌 마커가 없음을 입증하고, 근거가 뒷받침하는 정확한 경로를 stage한 뒤, 병합되지 않은 index가 비었음을 입증하고 staged diff를 확인합니다. 계속하기 전에 관련 검증을 실행합니다. 내용만 수정해도 병합되지 않은 index 항목이 사라지는 것은 아닙니다.
6. `continue`: 작업에 맞는 계속 명령을 실행하고 결과를 기록합니다.
7. `receipt`: `Pass | Fail | Blocked | Unverifiable`, 미검증 항목과
   `operation`/`verification`/`follow-up` 섹션의 참조를 반환하며, 해당 내용을 복사하지 않습니다.

<a id="resolution-receipt--single-evidence-record"></a>
## 해결 `receipt` · 단일 근거 기록

모든 해결 실행을 아래 단일 `receipt`에 기록합니다. 별도 결과 섹션이 아니라
`Operation` → `Resolution` → `Verification` → `Follow-up` 보고의 유일한
근거 기록입니다. 알 수 없는 값에는 `unavailable`이나 `not run`을 사용하며 추측하지 않습니다.

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

필요한 앞선 출력이 없으면 진행하지 않습니다. 새 충돌이 나타나면
`conflict inventory`부터 다시 시작합니다.

의도를 분석하기 전에 index `stage` 1/2/3을 실제 base, 현재 커밋과
작업 대상·재적용 커밋에 대응시키고 커밋 ID와 경로를 기록합니다. 특히
`rebase`/`cherry-pick`/`revert`에서는 `ours`/`theirs`만으로 사용자의 브랜치나 원하는 동작을
추론하지 않습니다. 작업 메타데이터와 실제 커밋 내용을 사용합니다.

<a id="command-evidence"></a>
### 명령 근거

| 근거 | 명령 계약 | 완료 신호 | 실패 경로 |
|---|---|---|---|
| 작업 상태 | `git rev-parse --git-path`로 `MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`를 확인한 뒤, 해석된 경로만 살펴봅니다. | 정확히 하나의 활성 작업 종류와 단계가 status·worktree 메타데이터와 일치합니다. | 마커가 충돌하거나 읽을 수 없으면 `Unverifiable`입니다. `.git/` 경로에서 추론하지 않습니다. |
| 작업/index | `git status --short --branch`, `git diff --name-only --diff-filter=U`, `git ls-files -u`를 함께 확인합니다. | 종류, 단계와 HEAD가 최신성 기준점과 일치하며, 검토하지 않은 경로가 없습니다. | 목록을 다시 구성합니다. 설명되지 않은 상태는 `Unverifiable`입니다. |
| 마커 | 추적되는 모든 충돌 경로에서 `^(<<<<<<<\|=======\|>>>>>>>)`를 검색합니다. | 실제 충돌 마커가 남아 있지 않습니다. 정상적인 Markdown 구분선은 충돌이 아니므로 일치 항목을 맥락 속에서 확인합니다. | 충돌 hunk가 남아 있으면 `Fail`이며 계속하지 않습니다. |
| stage | `git add -- <supported-path...>`를 실행한 뒤 `staged diff`와 병합되지 않은 index를 다시 확인합니다. | 근거가 뒷받침하는 경로만 stage되어 있으며, 병합되지 않은 항목 수가 0입니다. | stage 실패나 남은 항목이 있으면 `Fail`이며 계속하지 않습니다. |
| 검증 | 관련 테스트, 빌드와 정적 검사를 실행합니다. | 명령, 결과와 범위를 기록하며, 변경과 관련된 실패가 없습니다. | 실행 불가능하면 `Unverifiable`, 실패하면 `Fail`입니다. |
| 계속 | 작업에 맞는 `git merge --continue`, `git rebase --continue`, `git cherry-pick --continue`, `git revert --continue` 중 정확히 하나를 실행합니다. | 새 충돌 없이 의도대로 작업이 끝납니다. | 실패·새 목록을 기록하고 다시 시작합니다. |

<a id="operation-freshness-gate"></a>
### 작업 최신성 관문

첫 목록에서 작업 종류, HEAD, Git이 제공한 단계·대상,
병합되지 않은 경로와 기존 `staged` 경로를 고정합니다. 해결 근거에 포함된 경로만
stage합니다. 새 경로는 그 이유와 의도 근거를 목록에 기록한 뒤에만 추가합니다.

검증·계속 전에 메타데이터, HEAD, status와 index를 다시 읽습니다. 작업이
사라지거나 종류·단계·HEAD가 바뀌거나 검토하지 않은 미병합 내용 또는 `staged` 내용이 나타나면,
이전 해결은 오래된 상태입니다. 목록, 근거와 검증을 다시 구성합니다.
원인을 알 수 없는 변동은 `Unverifiable`입니다. 사라진 작업을 이번 실행에서 완료했다고
주장하지 않습니다.

1차 출처에는 커밋 메시지, `issue`/`PR`, `spec`/`ticket`, 인접 테스트와
확립된 브랜치 동작이 포함됩니다. 양립할 수 있다면 양쪽 의도를 보존합니다. 그렇지 않으면
작업 목표·근거에 따라 선택하고 절충을 보고하며 새 동작을 만들어 내지 않습니다.

명시적인 충돌 해결 요청은 활성 작업의 완료를 허용하지만,
`abort`, `reset --hard`, `clean`, 강제 `push`, 일반
`push`, 근거 없는 일괄 삭제나 무관한 서식 변경을 자동으로 허용하지는 않습니다.

<a id="completion-report"></a>
## 완료 보고

비어 있지 않은 섹션만 `Operation`, `Resolution`, `Verification`, `Follow-up` 순서로 사용합니다.
`Operation`에는 `kind`, `state`, `stage`, `status`, 미검증 항목, `reference`와
`continue` 결과를 넣습니다. `Resolution`에는 충돌, 의도와 선택한 결과를 넣고, `Verification`에는
테스트, 마커 검사와 index 검사를 넣습니다. `Follow-up`에는 남은 작업만 넣습니다. 원격 발행에는
별도 요청이 필요합니다.

해결한 충돌 경로가 여러 개라면 `Resolution`을 간결한 `Path | Intent | Result`
표로 표시합니다. 사용자에게 중요한 행이 하나뿐이면 문장으로 작성합니다. 해결 결과부터 제시하고
행을 반복하거나 메타데이터를 덧붙이지 않습니다. 복합 의도, 해결한 경로 그룹과
검증을 짧은 행·목록으로 요약합니다. 여러 경로가 같은 의도를 공유하면 하나의
의도·결과 행으로 묶고 해당 행이 다루는 정확한 경로를 인용합니다.

<a id="artifact-paths"></a>
## 산출물 경로

승인된 산출물 쓰기, checkout·전송·Git 제외 설정이나 임시 입력 소비 전에
[산출물 경로](../tk-artifacts/references/artifact-paths.md)를 읽습니다. 저장소 임시 파일에는 안전하고 소유권이 확인된 심볼릭 링크가 아닌 경로와
입증된 Git 제외를 사용합니다. 검사에 실패하면 해당 파일 분기를 중단합니다. 명시적인 최종 목적지와
담당자별 기본값을 보존합니다. 미리 채워진 입력은 완료된 입력이 아닙니다.
정리는 기록된 리터럴 형태의 해석 완료된 실행 소유 절대 경로만 대상으로 하며, cwd 상대 경로나 glob을 사용하지 않습니다.
