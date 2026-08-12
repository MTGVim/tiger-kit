---
name: tk-drive
description: "[user] 하나의 승인으로 product-change source를 준비하고, direct 또는 fresh-worker로 실행해 acceptance gap을 닫고, 검증된 unit commit과 finalization까지 수행한다."
disable-model-invocation: true
argument-hint: "<source, request, issue, or approved active run> [--direct]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Drive 실행

사용자가 `/tk-drive`, `$tk-drive`, 또는 소스가 포함된 호스트 스킬 picker를
명시적으로 선택했을 때만 시작한다. 소스 없이 다시 호출하면, 같은 대화에서
현재 소스, 장부, Git, 저장소 근거가 하나의 approved 또는 pending run을
명확히 가리킬 때만 재개한다. 일반 요청, 산출물, 새 session은 Drive를
시작하거나 재개하지 않는다.

## 권한과 불변식

승인된 계획 하나로 preparation, `direct` 또는 `delegated` 단위 실행, 필수
검증, 승인된 단위마다 하나의 검증된 현재 브랜치 커밋, 최대 세 번의
수정 라운드, 종합 검증, 최종화를 수행할 수 있다. push, PR, merge, tag, release, 발행, 이력 재작성은 포함하지 않는다.

Drive는 controller다. Delegated strategy에서는 **product, test, 설정 변경을
직접 작성하지 않고** bounded 단위를 새 작업자에게 보낸다. Direct strategy에서는
현재 컨텍스트가 controller 역할을 잠시 내려놓고 승인된 단 하나의 단위 실행자가
되며, 동결된 소유 경로만 수정한다. 이것은 controller의 대체 경로가 아니다. 이 스킬은 user-invoked이므로 명시적 `/tk-drive` 또는
`$tk-drive` 호출 자체가 호스트의 user-requested AgentTool 조건을 충족한다.
Mechanical Git bookkeeping은 최종 후보가 통과한 뒤에만 controller가 맡을 수 있다.
호스트가 사용할 수 있는 작업자를 delegated strategy로 dispatch하지 못하면 `Blocked` 로
중단한다. Direct strategy는 승인된 계획 기록 뒤 변경을 시작하며, 작업자를 사용할 수 없을 때의 암묵적 대체 경로가 아니다.
Executor는 다른 user-owned TigerKit 워크플로를 orchestrate하거나 호출하지 않는다.

## 생명주기(Lifecycle)

```text
Prepare -> Execute -> Close gaps -> Finalize
```

Drive가 이 생명주기를 소유한다. Child receipt는 내부 자료이며 `continue`,
`/clear`, model switching, second invocation을 요구하지 않는다. 호스트/프로세스
경계를 지난 뒤에는 cursor나 lifecycle claim이 아니라 새 근거에서 다음
행동을 도출한다.

## 원천 우선순위

현재 대화의 명시적 사용자 요구와 같은 대화에서 확정된 결정은 가장 최신의
정본 원천이다. 우선순위는 다음과 같다.

```text
현재 대화의 명시적 요구
> 같은 대화의 확정 결정
> 승인된 활성 run
> 현재 source와 일치하는 Ready 작업 문서
> 과거 terminal 문서와 durable prior-art
```

과거 `Status: Pass` 장부나 완료 문서는 현재 요청을 덮어쓰지 못한다. 현재
대화가 완전한 원천이고 목표·범위·R/AC·검증 의무를 도출할 수 있으면, 과거
문서가 낡았거나 계보가 달라도 `supersedes` 근거를 기록하고 현재 작업
문서 세 개를 새 계보로 발급한다. 현재 원천이 불완전·모순·위험하거나
사용자 결정이 필요한 경우에만 `Blocked`다.

작업자에게는 대화 자체가 아니라 현재 원천을 반영한 자체 완결형 작업 문서를
전달한다. 따라서 과거 문서를 읽었다는 이유만으로 현재 요구를 누락하지 않으며,
현재 원천이 대화 안에 있다는 이유만으로 작업 문서의 완전성 검사를 생략하지
않는다.

## 준비(Prepare)

1. 완전한 소스와 적용되는 저장소 지침을 읽는다. 먼저 현재 대상
   checkout에서 `git rev-parse --show-toplevel`로 저장소 루트를 확인하고, 그
   결과를 `<repository-root>`로 치환해 다음 네 absolute 경로를 파생하고 모두 읽는다:
   `<repository-root>/.tigerkit/drive.md`, `<repository-root>/.tigerkit/spec.md`,
   `<repository-root>/.tigerkit/tickets.md`, `<repository-root>/.tigerkit/implement.md`.
   Optional `<repository-root>/.tigerkit/session.md`가 있으면 모델 라우팅 소스로 읽되,
   누락 자체는 작업 문서 차단 사유로 취급하지 않는다.
   `drive.md` 는 progress, 승인, receipt만 소유한다. 상세 요구와 지시는 세 작업
   문서에만 둔다. 먼저 현재 대화 원천의 식별자와 명시적 지시를 고정하고,
   과거 종료 문서는 선행 근거로 분류한다.
   [문서 규칙](references/documents.md)과
   [작업자 원천 규칙](references/worker-source.md)에 따라 현재 원천이 완전하면
   누락 문서와 낡은/계보 불일치 종료 문서를 새 `Pending` 작업 문서로
   발급하고 `supersedes`를 기록한다. 사용자가 표시된 계획을 승인하면 그 문서를
   `Ready`로 갱신한다. 현재 원천이 불완전·모순·위험하거나 문서가 Pending인데
   승인되지 않은 경우에만 정확한 상태로 `Blocked`하고 작업자를 배정하거나
   제품을 수정하지 않는다. 브랜치, 기준선 `HEAD`, 작업 트리,
   `pre-existing` 변경 경로, 그리고 관련 영속 선행 근거를 최대 일곱 개까지
   기록한다.
2. 근거와 안전한 기본값으로 되돌릴 수 있는 모호성을 해결한다. 모든
   중요한 controller 선택, 근거, 동작을 바꾸는 대안을 기록한다.
   사용자 소유 결정이 안전한 실행 계획을 막을 때만 `tk-grill-me` 를
   호출한다. 질문이 `pending`인 동안에는 `🙋 drive > grill-me · 응답 필요` 를
   출력하고 작업자를 dispatch하지 않는다. 제한된 비교로 해당
   결정을 닫을 수 있을 때만 `tk-prototype` 을 사용한다.
3. 현재 원천 식별자와 대체 계보, 범위, 제외, 동결된 사용자 표시 리터럴, 검증
   의무를 포함해 `Ready` 요구사항과 acceptance criteria를 작성한다.
4. 독립적으로 검증 가능한 `1..N` 단위, 의존성 그래프, wave를 도출한다.
   결합되었거나 불확실한 단위는 직렬화한다. 호스트가 이미 격리된
   checkout/작업 트리를 제공하는 경우에만 독립성이 입증된 단위를 병렬화한다.
   스케줄러를 만들거나 작업자가 변경 가능한 작업 트리를 동시에 공유하게 하지 않는다.
5. 테스트/검사를 분류한다. `browser-visible` AC라면 정확한
   시나리오, 대상, 민감하지 않은 인증 모드, prerequisite, limitation을
   계획한다. 그 외에는 `not-required` 로 기록한다. 필수 headless auth를
   사용할 수 없으면 mutation 전에 `Unverifiable` 이다.
6. [worker-dispatch.md](references/worker-dispatch.md)에 따라 각 단위의 실행
   strategy와 최소 model을 선택한다. 티켓에 이미 확정된 `model`/`effort`가 있으면
   계획 metadata로 소비하고 조용히 덮어쓰지 않는다. 격리 없는 bounded known-pattern이면
   session model을 유지하는 `strategy=direct`를 우선 추천하고, 새 컨텍스트·격리·검토자
   handoff·설계 중심 추론이면 `delegated`와 근거를 추천한다. Delegated는
   현재 호스트 section이 있는 `.tigerkit/session.md` routing을
   `skills/tk-drive/references/worker-dispatch.md#session-model-routing`의 정경
   schema로 검증해 사용한다. section이 없거나 불완전하면 중첩된 class별
   model/effort 정확한 Markdown 추가와 `routing_state=decision-required`를 같은
   승인 표면에 제안하고 승인 전에는 파일을 쓰거나 작업자를 dispatch하지
   않는다. 실행 가능한 delegated 단위의 승인에는 model class, selector, effort,
   routing 소스가 모두 보여야 하며 누락되면 `Blocked`다. `general-purpose` implementer와
   새 task 검토자를 한 쌍으로 사용하며 반환 label은 tier 판정에 사용하지 않는다.
   Model class/selector/effort 선택은 delegated 전용이다. Direct 승인과 장부에는
   `cheapest | standard | strongest` tier를 어떤 label로도 붙이지 않고
   `model_class=n/a`, `requested_selector=n/a`, 호스트가 노출한 세션 `realized_model` 또는
   `unavailable`, `reasoning_effort=inherited`를 기록한다.
7. [ledger.md](references/ledger.md)에 따라 `.tigerkit/drive.md`의 현재 진행 상태를 원자적으로
   교체하고 다시 읽은 뒤 하나의 간결한 승인 표면을 제시한다. Ledger에는
   현재 원천 식별자, `supersedes` 대상, 저장소 상태, 네 작업 문서와 선택적 세션 경로와 상태, 문서
   status/lineage check, 승인 snapshot, 단위/dispatch/검증 receipt만 둔다. Goal, 범위, 동결된 리터럴,
   R/AC, 구현 지침은 세 작업 문서에서 소유하며 unknown은
   `unavailable` 로 둔다. `👍 Recommendation:` 에는 strategy, model class, selector,
   effort, 라우팅 소스를 포함하며,
   사용자가 이 계획을 승인하는 것이 direct strategy의 명시적 승인이다.
   별도 direct 확인은 묻지 않는다. 이는 별도 생명주기 출력이 아닌 승인 근거이다.

승인 질문이 작업 표면이다. `🙋 drive · 응답 필요` 와 정확히 하나의
`👍 Recommendation:` 을 보여 준다.
Approval은 표시된 snapshot에만 적용된다. 중요한 소스, 범위, 브랜치/head,
remote 상태, verifier prerequisite, 되돌릴 수 없는 결정의 drift가 생기면
승인은 무효가 되어 Prepare로 돌아간다. 계획이 변하지 않았다면 일상적인 두 번째 승인을 받지 않는다.

## 실행(Execute)

각 의존성 wave마다 동결된 strategy를 적용한다. Delegated 단위는 새
`general-purpose` implementer가 맡고, direct 단위는 현재 컨텍스트가 단 하나의
bounded 실행자로 맡는다.
Executor에게는 ID/goal, 정확한 R/AC, 소스/티켓 범위, 범위/exclusion, 관련
   경로와 현재 대상 checkout에서 resolve한 `<repository-root>/.tigerkit/` 아래 네
absolute 경로, 검증 obligation, 브랜치/head/diff 소유권을 전달한다.
Direct 단위는 subagent를 spawn하지 않고 focused test와 self-review 뒤 후보를
controller에 돌려준다. Delegated 단위는 dispatch 전에 호스트 작업자 capability와 승인된
session selector를 확인하고 native model control에 명시한다. Implementer에는 task
brief/report 경로를 주고 질문·구현·focused test·self-review·commit 후 짧은 report를
받는다. 그 뒤 새 `general-purpose` 검토자에게 diff package를 주고 `Spec
compliance`와 `Task quality` 두 verdict를 받기 전에는 delegated 단위를 완료로 처리하지
않는다. 각 delegated 작업자 뒤에는 requested selector와 호스트가 노출한 realized model
receipt를 기록하며, 미노출 값은 `unavailable`로 둔다. `general-purpose` 반환 자체는
실패가 아니다. 다음 불변식을 지킨다.

```text
candidate -> required tests/checks/browser verifier -> Close gaps
          -> bounded fresh correction when needed -> one verified unit commit
```

필수 verifier는 커밋 전에 최종 후보를 대상으로 실행한다. 검증된 소유 경로만
stage하고 `pre-existing` 사용자 변경을 보존한다. Direct 단위의 격리된 gap은 같은 동결 단위와 소유 경로 안에서 현재 실행자가 닫고, delegated
단위의 gap은 새 corrective 작업자를 dispatch해 영향받은 의무를 다시
실행한다. 최대 세 round를 우선한다. 누락된 컨텍스트는 model upgrade 없이
보충한다. 입증된 추론 실패가 있을 때만 한 단계 강한 새
작업자를 한 번 사용한다. 변하지 않거나, 원인을 격리할 수 없거나, 충돌하거나,
범위를 넓히는 실패가 반복되면 mutation을 중단한다.

통합 충돌은 독립성이 틀렸다는 뜻이다. 영향받은 단위를
직렬화하거나 다시 Prepare한다. 작업자는 의미 병합을 임의로 만들지
않는다. 격리, 통합 순서, stale-base/conflict detection, 정리는
Drive가 소유한다.

## 공백 닫기(Close gaps)

승인된 각 R/AC에 대해 관찰된 근거를 `satisfied`, `missing`, `partial`,
`unverifiable` 중 하나로 분류한다. Acceptance와 관련된 범위/exclusion,
단위, verifier, 외부에 표시되는 동작, commit/ancestry, dirty 경로
소유권, 근거 freshness만 확인한다. 그 acceptance 사실과 무관한
발견 사항은 생략한다.

근거만으로 확신할 수 있는 판정을 내릴 수 없을 때는 동일한 좁은 R/AC brief를
사용하는 더 강한 새 비변경 검토자를 최대 한 번 dispatch한다.
사용자/저장소 정책이 독립 검토를 요구할 때만 사용 가능한
built-in 또는 third-party 검토자를 쓴다. Required review를 사용할 수
없으면 `Unverifiable` 이다. 모든 수정은 여전히 새 corrective 작업자에게
보낸다.

## 최종화(Finalize)

Delegated 단위가 하나라도 있거나 승인된 계획이 독립적인 최종 검토를 요구할 때만
새 `general-purpose` 전체 브랜치 검토자를 한 번 dispatch해 전체 diff의 Spec/AC와
품질을 확인한다. 모든 direct 실행은 aggregate checks와 self-review만 사용한다. delegated
검토에서 발견 사항이 있으면 하나의 새 corrective 작업자와 한 번의 scoped re-review만
수행하고, load-bearing residual은 `Blocked`로 남긴다.
모든 verified 단위 commit 뒤에 aggregate R/AC traceability, 저장소 check,
ancestry, exclusion, freshness를 다시 확인한다. Unit commit, verifier/gap
근거, 수정 라운드, 종합 결과, 복구 사실을 포함하도록
`.tigerkit/drive.md` 를 갱신한다. 성공이 아니면 mutation을 동결하고
[non-success-finalization.md](references/non-success-finalization.md)를 따른다.

성공이면 간결한 동작 결과, 유용한 단위 커밋, 종합 검증
한 개에서 네 개, 정확히 `Status: Pass` 를 출력한다. 활성 실행의 terminal
응답은 Drive만 출력한다. Child receipt, raw log, dispatch model,
progress marker는 생략한다.
