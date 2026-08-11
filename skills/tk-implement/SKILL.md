---
name: tk-implement
description: "[user] 하나의 fresh Ready ticket과 .tigerkit/implement.md를 검증한 뒤 direct 또는 delegated로 정확한 범위만 구현하고, 필요한 review·검증을 통과할 때만 하나의 commit과 receipt를 만듭니다."
disable-model-invocation: true
argument-hint: "<Ready ticket 또는 tickets.md 경로>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# `Ready` 티켓 구현

명시적으로 `/tk-implement` 또는 `$tk-implement` 을 선택한 경우에만 실행한다.
현재 체크아웃의 저장소 루트를 `git rev-parse --show-toplevel`로 확인한 뒤
`<repository-root>/.tigerkit/tickets.md` 에서 정확히 하나의 `Status: Ready` 티켓과
`<repository-root>/.tigerkit/implement.md` 의 지시를 읽는다. 입력이 없거나 문서가
없으면 `Status: Unverifiable` 로 멈춘다.
`Pending`, 오래된 상태, 계보 불일치, 해소되지 않은 `model`/`effort` 는 각각 정확히
`Status: Blocked` 로 멈추고 변경·스테이징·commit·receipt를 만들지 않는다.

## 절차

1. 티켓의 최신 계보, 정확한 소유 경로, `Scope`, `R/AC`, `Verification`, 기호화된
   `model` 과 `effort` 가 모두 해소됐는지 확인한다. `delegated` 실행이면 `model`을
   worker 생성 전에 정하고, 선택 사항인 `.tigerkit/session.md`의 호스트별 라우팅을
   `skills/tk-drive/references/worker-dispatch.md#session-model-routing`의 정해진
   스키마로 검증해 `general-purpose` 구현자의 brief/report 경로를 준비한다.
   라우팅이 없거나 불완전하면 중첩 클래스별 `model`/`effort`의 정확한 Markdown
   추가와 `routing_state=decision-required`를 제안하고 `Status: Pending`으로
   멈춘다. 승인 화면에는 모델 클래스, 선택자, 노력 수준, 라우팅 출처가 모두
   있어야 한다. 구현 전 `git status --porcelain=v1`과
   `.tigerkit/implement.md`의 존재·바이트를 스냅샷하고, 사용자 변경·인덱스·기존 receipt의 기존 바이트는 바이트 단위로 보존하며
   성공 commit 뒤에만 덧붙인다. 소유 경로 밖은 읽기만 한다.
2. 제한된 저위험 단독 작업이면 `direct`를 추천하고, 위험·범위·격리·새
   컨텍스트가 필요하면 `delegated`를 사용한다. `delegated`가 필수인 경우
   `direct`로 조용히 대체하지 않는다. 어떤 `delegated` 실행이든 필수 worker를
   dispatch할 수 없으면 정확히 `Status: Blocked` 로 종료하고 변경·스테이징·commit·receipt를 만들거나 수정하지 않는다.
   `general-purpose` label은 의도된 worker 역할이며, 반환 label로 model/tier를
   사후 판정하지 않는다. `direct`는 subagent 없이 집중 검사와 자체 검토를 쓴다.
   `delegated`는 새 `general-purpose` reviewer가 `Spec compliance`와 `Task quality`를
   확인하기 전 commit을 성공으로 처리하지 않는다.
3. 구현자는 정확한 소유 경로만 수정하고 집중 검사를 먼저 실행한다.
4. `delegated` 또는 사용자/저장소 정책이 독립 검토를 요구할 때만 implementer
   이상의 capability를 가진 reviewer가 `Spec/AC` 및 `Standards/Style` 을 검사한다. 모든
   `direct` 실행에서는 이 reviewer를 생성하지 않는다. verbatim 또는 스타일 불일치는
   `Blocking` 이다.
5. 검증·review에서 gap이 나오면 매번 범위가 제한된 새 corrective worker로 수정하고
   다시 검증한다. 실패하면 `Status: Fail`/`Blocked` 로 종료하며 스테이징·commit·성공
   receipt를 만들지 않는다.
6. 모든 필수 검증과 review가 성공한 경우에만 현재 `branch`에 정확히 한 commit을 만들고,
   그 뒤 `implement.md`에 unit/ticket, changed paths, check/review/gap evidence,
   commit/ancestry, delegated `model_class`/`requested_selector`/`realized_model`/
   `reasoning_effort`/`worker_id`/`receipt_source`, `unresolved: none` receipt를 덧붙인다.
   호스트가 realized model을 노출하지 않으면 `unavailable`로 둔다. push, publish, 다른
   workflow/skill 호출은 금지한다.

출력은 receipt의 절대 경로와 `Status: Pass`/`Status: Pending`/`Status: Blocked`/`Status: Fail`/`Status: Unverifiable`만 간결히 보고한다. receipt 내부 증거를 채팅에 복사하지 않는다.
