---
name: tk-pr-sweep
description: "[user] 승인된 다중 PR 유지보수 배치를 하나 준비·실행하거나, `--report`로 결정론적 분류만 읽기 전용으로 보고합니다."
argument-hint: "[--report] [--recover-publication] [--repo owner/name]..."
disable-model-invocation: true
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Pull request Sweep(일괄 유지보수)

`/tk-pr-sweep`, `$tk-pr-sweep` 또는 호스트의 스킬 선택기로만 시작합니다. 일반 PR
상태 확인, 단일 PR 작업, 릴리스 또는 계속하기 요청으로는 시작하지 않습니다. Sweep는
다중 PR 조정자이며 한 PR의 Respond와 Rebase는 서로를 호출하지 않습니다.
기본 Sweep는 원격 발행을 하지 않습니다. 단, 이미 작업과 검증을 끝냈지만 호스트
권한 판정이 마지막 원격 쓰기만 막은 항목은 사용자가 정확히
`--recover-publication`을 명시한 별도 실행에서만 제한된 복구 경로를 사용할 수
있습니다.

## 결정론적 분류 및 보고 모드

초기·경로별·최종 분류에는 패키지 로컬 `scripts/triage.mjs`를 직접
실행합니다. 신원과 명시적 `--repo` 대상 또는
`$XDG_CONFIG_HOME/tigerkit/pr-triage.json`을 확인하고, 설정이 없으면 현재
origin을 bootstrap합니다. API 실패로 분류되지 않을 때만 한 번
재시도하며, 부분 snapshot을 합치거나 누락된 검사로 승인을 추론하지
않습니다.

`$tk-pr-sweep --report`는 triage를 한 번 실행하고 `지금 처리`, `검토 요청`,
`대기`로 그룹화해 클릭 가능한 근거와 다음 조치 하나를 보여준 뒤
반환합니다. 승인을 묻지 않고 장부·작업 트리·커밋·경로·GitHub 쓰기를
만들지 않으며, 허용된 상태 쓰기는 설정 bootstrap뿐입니다.

## 권한 및 불변식

대화형 Sweep는 하나의 계획/승인, `.tigerkit/pr-sweep.md`, 격리, 고정 경로, PR별
요약 하나, 전체 검증, 최종화를 소유합니다. 제품 변경은 직접 작성하지 않으며,
중첩된 `tk-pr-respond --ci`가 모든 주요/수정 편집에 `delegated` 새 작업자를 사용합니다.
Sweep는 직접 실행 선택지를 받지 않으며 하위 권한을 확장하거나 병합·종료·PR 생성·
태그·릴리스를 수행할 수 없습니다. `--recover-publication`은 이미 승인된 고정
refspec에 대한 마지막 `git push --force-with-lease`만 예외적으로 소유합니다.

```text
Prepare -> Execute -> Close gaps -> Finalize
```

## 준비(Prepare)

1. 새로 결정론적 triage를 실행하고 전달받은 대기열, 캐시된 보고서, 오래된
   장부, cursor는 무시합니다. 신원, PR/base/head 상태, 범주, 검사 제공자,
   검토, 댓글, 스레드, 요청된 검토자를 확인합니다.
2. 모든 항목을 `actionable`, `held`, `report-only`로 분류하고 닫힌 라우터를 사용합니다.

   | 새 evidence | 제한된 route |
   | --- | --- |
   | 동일 repository의 base/head와 명확한 ownership에 정확히 일치하는 maintenance conflict | `tk-pr-rebase --ci` |
   | repository가 유발한 GitHub Actions failure | `tk-pr-respond --ci` |
   | 하나라도 unresolved인 inline review thread | `tk-pr-respond --ci` |
   | 현재 actionable feedback/reply | `tk-pr-respond --ci` |
   | 외부·unknown·unverifiable check, review request, draft 또는 waiting | report-only |

   안전한 소유권/refspec/범위/경로가 없는 항목은 보류합니다. 제품 수정은 정확한
   범위와 새 작업자 검증 경로가 있을 때만 실행 가능으로 취급하며,
   반복적인 두 번째 “고위험 승인”은 유지하지 않습니다.
3. 되돌릴 수 있는 각 중요한 가정, 근거, 동작을 바꾸는 대안을 기록합니다. 계획이
   사용자 소유 결정으로 막힐 때만 `tk-grill-me`를
   사용합니다.
4. 저장소/PR/`head`/범주/경로/범위/위험/검증/조치와 제외를 고정합니다. 각 `actionable`
   항목에는 제한된 `feedback summary`, `apply direction`, `route/strategy`,
   추천 `model`/`effort`, 추천 근거와 검증 영향을 붙입니다. 독립성과
   호스트가 제공하는 격리가 함께 증명될 때만 동시성을 허용하고 웨이브를 도출합니다.
   불확실성은 직렬화하며 스케줄러는 만들지 않습니다. 실행 가능한 `delegated` 항목이
   있으면 선택 사항인 `.tigerkit/session.md`의 호스트 모델 라우팅을
   `skills/tk-pr-sweep/references/worker-dispatch.md#session-model-routing` 정본
   스키마로 검증합니다. 파일 또는 현재 호스트 `section`이 없고 확인된 제어값이 모두
   있으면 정확한 중첩 `block`을 `.tigerkit/session.md`에 원자적으로 초안 생성하고
   `Status: Pending`으로 둡니다. 기존 불완전·충돌 `block`은 덮어쓰지 않고 보존하며,
   정확한 보정안을 승인 표면에 제시합니다. 둘 다 `routing_state=review-required`로
   기록하고 사용자가 초안을 검토·승인하기 전에는 `worker`, 제품 파일, Git 또는
   `remote`를 변경하지 않습니다. 승인 뒤에만 `Status: Ready`로 바꾸고 `reread` 검증합니다.
   확인되지 않은 `selector`를 발명하지 않으며, 모든 실행 가능한 `delegated` 항목의
   모델 종류, 선택자, 노력도, 라우팅 출처를 추천 표면에 표시합니다.
5. `.tigerkit/pr-sweep.md`를 원자적으로 교체한 뒤 다시 읽습니다. `actionable`/`held`/`report-only`
   항목, 가정/모호성, 경로 웨이브, 검증, 위험, 작업 트리 소유권,
   제한된 원격 조치와 `원격 변경: 아직 없음`을 파일에 보존합니다. 다음
   계획 증거 필드도 한 번씩 보존합니다: `저장소 범위`, `분류 기준`,
   `항목 (PR # | head SHA | category | route)`, `경로 / 웨이브`, `검증`,
   `위험 / 제외`, `Worktree 소유권`, `권한`, `승인`,
   `원격 변경: 아직 없음`, `workspace_backend`, `worktree_backend`,
   `dispatch_backend`, `backend_evidence`, 호스트 라우팅 출처와
   `routing_state=review-required | ready`, `model class`/`selector`. `unknown`은
   `unavailable`로 두고 경로/권한을 추측하지 않습니다.
   각 `actionable`의 제한된 `feedback summary`와 `apply direction`, 추천 `model`/`effort`,
   추천 이유/검증 영향은 채팅 승인 표면과 장부에 보존합니다. 채팅에는 계획 전문이나
   `evidence field`를 반복하지 않습니다.

   산출물의 설명과 제목은 한국어로 작성하고, machine-readable key·status·ID·
   command·path·URL·exact literal만 원문으로 유지합니다. 산출물에는 work `Status`와
   별도로 `Disposition: reported | applied | pending`을 기록합니다. 원자적 쓰기와
   다시 읽기가 일치하면 `Disposition: applied`여도 승인 전 작업 `Status: Pending`은
   유지합니다. ledger가 missing/stale이거나 reread가 다르면 `Status: Blocked`,
   `Disposition: pending`으로 멈추고 recommendation, approval question, worktree,
   commit, remote mutation을 만들지 않습니다.

`🙋 sweep > plan · 응답 필요`를 하나만 표시하고, 산출물의 절대 경로와 `Status`,
`Disposition`, 항목/개수 요약, 그리고 모든 `actionable`에 대한 다음 간결한 표를
표시합니다: `PR/feedback ID` | `feedback summary` | `apply direction` | `route/strategy` |
`recommended model/effort` | `rationale/verification`. 전체 인용문이나 계획 전문은
복사하지 않습니다. 정확히 하나의 `👍 Recommendation:`과 하나의 일괄 승인
질문만 표시하며, 항목별 모델을 다시 고르게 하지 않습니다. 사용자는 표시된
추천을 일괄 승인하거나 한 번에 수정합니다. 승인 전에는 작업 트리/커밋을 만들거나
원격 쓰기를 수행하지 않습니다.
승인은 중첩된 Respond/Rebase에 정확히 제한된 권한을 제공하며, 중첩 소유자는 다시
묻지 않습니다.

기존 출력 호환성이 필요한 경우 간결한 보고서의 경로 표시에 `PR sweep 계획`을,
원격 상태에 `원격 변경: 아직 없음`을 사용할 수 있습니다. 이는 전체 증거 필드
출력이 아닙니다. 중요한 신원, PR head/state/category/scope/route, 검증기 또는
되돌릴 수 없는 결정이 바뀌면 해당 계획은 무효가 되어 Prepare로 돌아갑니다.
변경되지 않은 항목에는 일상 체크포인트를 다시 주지 않습니다.

## 실행(Execute)

고정된 웨이브를 처리합니다. 각 항목 전에 triage를 다시 실행하고 신원, PR 상태,
head/category/provider, refspec, 스레드, 검사를 증명합니다. 이미 완료된 작업은
하위 작업자/작업 트리 없이 `Skipped: already applied`로 처리합니다. 외부 변경 이탈은
Prepare로 돌아가게 하며, Sweep가 소유한 검증된 head는 승인된 범위 안에서만
계속합니다.

변경 전에 정확한 원격 head를 fetch하고 증명합니다. 먼저 하나의
`workspace_backend`를 선택해 작업 트리 생성과 작업자 배정을 함께 고정합니다.
`git-native`는 이 저장소에서 확인된 대체 경로로 `git worktree`와 현재 호스트의
새 작업자를 한 backend로 묶습니다. `orca`나 `paseo`는 현재 호스트가 작업 트리,
배정, 호스트 receipt를 모두 제공하는 것이 독립적으로 확인된 경우에만 선택하며,
CLI 설치나 전역 스킬 존재만으로 선택하지 않습니다. 작업 트리는 Orca로 만들고
작업자는 별도 native backend로 띄우는 조합은 금지합니다. 짝을 이루는 backend가
없으면 로컬/원격 변경 전에 항목을 `Blocked`로 둡니다. 고정된 설정은 한 번만 실행하고
패키지 캐시만 공유하며 의존성은 공유하지 않습니다.

현재 범주마다 정확히 한 소유자만 호출합니다. 변경이 있는
maintenance-rebase 항목은 `tk-pr-rebase --ci`를 새 격리 작업자/전문가로
배정해야 하며 Sweep 제어기 안에서 인라인 실행하지 않습니다. 호스트가
해당 작업자를 배정할 수 없으면 로컬 또는 원격 변경 전에 항목을
`Blocked`로 표시하며 직접 대체 경로는 없습니다. 고정된 PR/head/route, 발견
ID, R/AC, 범위/제외, 검증, 작업 트리 사실, 장부 소유자
`tk-pr-sweep`, 요약 예산을 전달합니다. Nested Respond, Rebase, 작업자,
검토자, 검증기는 하위 Markdown 장부를 쓰지 않고 간결한 증거를
`.tigerkit/pr-sweep.md`에 반환합니다. 제어기와 중첩 Respond는 제품 편집을
작성하지 않으며, 수정은 정본 정책
`skills/tk-pr-sweep/references/worker-dispatch.md`를 따르는 fresh worker를 사용합니다.
작업자 preflight가 실패하면 항목을 `Blocked`로 남기고, `general-purpose` 작업자 표시는
정상 역할로 처리합니다. 각 `delegated` 작업자의 요청 선택자, 호스트가 노출한
실제 모델과 추론 노력을 장부에 기록합니다. 작업자 신원의 정본 출처는 하위 작업자
자체 보고가 아니라 제어기가 받은 호스트 배정 표면이며, 배정 직후 작업자 ID/handle과
receipt 출처를 기록합니다. 하위 ID는 선택 사항이고 `unavailable`이어도 호스트
receipt가 있으면 실패가 아닙니다.

모든 변경 하위 작업자는 두 단계 인계입니다. 첫 호출은 `Preflight only`이며 하위 작업자가
고정된 전략, 모델 종류, 요청 선택자, 소유 경로를 정확한 `Frozen receipt`로
되돌릴 때까지 편집/커밋/원격 반영을 금지합니다. 제어기가 장부의 고정 항목과 필드별로
정확히 비교해 일치할 때만 같은 하위 작업자를 재개합니다. 누락·불일치는 새 판단으로
보정하지 않고 row를 `Blocked`로 남깁니다.

완료 뒤 제어기는 호스트 배정 receipt와 `Actual receipt`의 strategy, model class,
requested selector, changed path, `Plan deviations`를 고정 항목에 기계적으로
대조합니다. 호스트 배정 신원이 없거나 direct 실제 전략, 종류/선택자/범위 불일치,
빈 deviation field 또는 `scope-violating`이면 결과와 테스트가 정상이어도
`Blocked`입니다.

`transient-self-corrected` deviation은 제어기가 새 계보, 게시된 diff/tree,
고정 범위, 의도한 변경 집합과 필수 테스트/검사를 독립적으로 다시 읽어 순효과
0을 입증한 경우에만 `Pass with recorded deviation`으로 허용합니다. 이미 원격 반영된
항목도 이 판정이면 중첩 Respond 최종화를 끝까지 실행합니다. 입증 실패나
`scope-violating`이면 추가 발행을 멈추고, 새 하위 작업자가 정확한 고정 상태를
복원한 뒤 같은 검증을 통과해야 최종화를 재개하는 복구 조건을 장부에 남깁니다.
즉 이미 게시된 항목을 설명 없이 반쯤 열린 상태로 버리지 않습니다.

### 발행 차단 복구(`--recover-publication`)

하위 작업자가 제품 변경·검증·커밋을 끝냈지만 호스트 권한 판정이 마지막 원격 쓰기만
막은 경우는 작업자 배정 불가와 구분합니다. 일반 실행에서는 항목을
`Status: Blocked`, `Disposition: pending`으로 남기고 `publication_block`,
`remote_head_before`, `remote_head_after`, 고정 refspec, 권한 근거를 기록합니다.
원격 HEAD가 바뀌었거나, `Plan deviations: none`이 아니거나, 하위 작업자의
변경 경로·계보·검증이 고정 항목과 다르면 복구하지 않습니다.

사용자가 정확히 `--recover-publication`을 다시 호출하고 별도 approval을 주었을
때만 제어기가 승인된 고정 refspec에 대해 한 번의
`git push --force-with-lease`를 수행할 수 있습니다. push 직전 원격 HEAD를
재증명하고 성공 뒤 원격 HEAD·게시된 diff/tree·PR 상태를 다시 읽어 최종화를
끝냅니다. 어느 guard라도 빠지면 직접 대체가 아니라
`Status: Blocked`로 멈춥니다.

Sweep가 head, thread reply 또는 check-fix를 변경한 모든 PR은 row를 닫기 전에 정확히
한 번의 nested `tk-pr-respond --ci` finalization을 거칩니다. 최초 owner가 Respond면
그 child가 같은 호출 안에서 finalization까지 소유하고 두 번째 Respond를 만들지
않습니다. Rebase 등 다른 owner가 변경했으면 fresh head를 넘겨 Respond를 한 번
호출합니다. 이 finalization은 현재 finding별 reply를 게시하고, reply가 성공한 thread를
fresh GraphQL evidence 뒤 resolve하고, 모든 thread가 resolved인지 재확인하고, PR-level
summary budget을 정확히 한 번 소비한 뒤 eligible prior human reviewer에게 formal
re-review를 요청·재확인해야 합니다. 어느 단계든 빠지거나 실패하면 row는
`follow-up-queued` 또는 실패 상태이며 `Pass`/waiting으로 승격하지 않습니다.

각 child/finalization result 후 정확한 PR을 fresh-triage하고 `continue`를 묻지 않은 채 frozen
queue를 계속합니다. prompt-local bound를 유지합니다: 정확한 base/head pair마다
rebase 한 번, GitHub Actions corrective cycle 최대 세 번, fresh head마다 feedback
response 한 번, sweep-owned follow-up head 최대 두 개입니다. 반복해서 unchanged
이거나 소진된 작업은 추가 mutation이 아니라 `follow-up-queued`가 됩니다.
push 후 `IN_PROGRESS`는 fresh recheck를 최대 세 번 수행하고 여전히 완료되지
않으면 `waiting`으로 기록하고 worktree를 유지한 채 independent row를 계속합니다.
반환된 state가 실제로 external check 또는 re-review 대기를 요구하고 모든 inline
review thread가 resolved일 때만
`⏳ sweep · 대기`를 emit합니다.

unresolved identity, corrupt repository evidence, unprovable worktree ownership 같은
shared safety failure일 때만 이후 mutation을 멈춥니다. PR-local `Fail`, `Blocked`,
`Unverifiable`는 proven-independent row를 멈추지 않습니다. complete route가 fresh
Pass한 sweep-created clean worktree만 제거하고, 나머지 worktree는 모두 보존하고
보고합니다.

## 공백 닫기 및 최종화

각 approved row/R/AC를 `satisfied | missing | partial | unverifiable`로 분류합니다.
일반 review가 아니라 scope, route, test/check, publication,
ancestry/ownership, freshness만 확인합니다. 불확실한 AC evidence에는 stronger
fresh non-mutating reviewer를 한 번 사용할 수 있지만 모든 fix는 여전히 fresh
Respond worker를 사용합니다.

모든 initial row를 처리한 뒤 unbounded queue를 늘리지 않고 final deterministic
triage를 한 번 실행합니다. 예상하지 못한 newly actionable supported item은
`Blocked`, `waiting` 또는 `follow-up-queued`는 `Pending`이며, 그 외에는
`Fail > Blocked > Unverifiable > Pending > Pass` 순서로 aggregate합니다.
report-only unsupported row는 supported success 또는 failure가 되지 않습니다.

승인 snapshot, route/worker/verifier/commit 증거, 소비한 bound, summary budget,
worktree disposition, final triage, gap verdict만
`.tigerkit/pr-sweep.md`에 update합니다. credentials, transcript, full logs, resume
cursor는 저장하지 않습니다. Terminal output은 `## PR sweep`로 시작하고,
처리한 모든 PR과 남은 report-only/held item을 보여주며, 정확히 한 줄의
`Status: Pass | Fail | Blocked | Unverifiable | Pending`을 사용합니다. child
receipt는 생략하고, canonical ID/status/command/path/exact literal은 보존한 채
사용자 언어를 따릅니다.
