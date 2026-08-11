---
name: tk-to-tickets
description: "[user] `Ready` 상태의 새 사양을 독립적으로 관찰 가능한 세로형 티켓으로 분해하고 `tickets.md`를 작성합니다."
disable-model-invocation: true
argument-hint: "<Ready spec 경로 또는 source>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# 사양을 티켓으로 변환

명시적으로 `/tk-to-tickets` 또는 `$tk-to-tickets` 를 선택한 경우에만 실행한다.
먼저 현재 체크아웃에서 `git rev-parse --show-toplevel`로 저장소 루트를 확인하고
`<repository-root>/.tigerkit/spec.md` 를 읽는다. `Status: Ready` 이며
현재 요청과 계보가 일치하는 최신 사양만 소비한다. 필수 사양/증거가
누락되면 정확히 `Status: Unverifiable` 로 멈춘다. `Pending` 이면 정확히
`Status: Blocked` 로 멈추고 downstream ticket을 생성하지 않는다. stale spec 또는
lineage mismatch도 각각 정확히 `Status: Blocked` 로 멈춘다.

## 출력 계약

유효한 `Status: Ready` 사양만 `<repository-root>/.tigerkit/tickets.md`에
`self-contained` Markdown으로 쓰고, 루트를 실제 절대 경로로 치환해 보고한다.
필수 입력이 없거나 `Pending`/stale/lineage mismatch/coverage 누락인 경계 경로에서는
`tickets.md`를 만들지 않고 정확한 terminal status만 보고한다. ticket마다 다음 필드를
포함한다.

`Status`, `Goal`, `Coverage`(source/R-AC mapping), `Scope`, `Entry points`,
`Dependencies`(`none` when absent), `Acceptance`, `Verification`, `model`,
`effort`, `rationale`, `lineage`.

Coverage의 각 source/R-AC는 정확히 한 티켓에 매핑하거나 명시적으로 `uncovered`
사유를 적는다. 티켓은 계층만 나누는 단위가 아니라 독립적으로 관찰 가능한 세로형
조각이어야 한다. `model`과 `effort`는 제공자 이름이 아닌 작업 난이도 메타데이터로
제안하고 작업 근거를 적는다. 이후 SDD 작업자를 배정할 때 모델 선택의 근거로
사용하되 구체적인 선택자는 선택 사항인 `.tigerkit/session.md`의 호스트 라우팅이
소유한다. `general-purpose` 반환을 모델 선택 증거로 삼지 않고 호스트가 노출한 실제
모델 receipt만 기록한다. 호스트가 작업자 자체를 제공하지 않으면 매핑을 발명하지 말고
설정 선행 조건으로 표시하며 `tk-wizard`를 먼저 사용하도록 한다.

문서 끝에는 후속 소비 전에 사용자의 명시적 승인이 필요하다는 경계를 둔다.
- 설명 문장과 제목은 한국어로 작성하고, 정확한 필드·상태·ID·명령·경로·URL·리터럴만 원문으로 유지한다.
구현, 원격 issue, global archive/state, `.tigerkit/` 외 출력은 하지 않는다.

## 절차

1. 사양의 상태, 최신성, 계보, source/R-AC와 acceptance를 검증한다. 유효하지
   않으면 산출물을 쓰지 않고 해당 경계 상태에서 멈춘다.
2. coverage를 수집해 각 항목을 한 번만 세로형 티켓에 배치한다. 누락·충돌은
   멈추고 원문과 이유를 보존한다.
3. 각 티켓의 진입점부터 관찰 가능한 acceptance와 verification까지 작성한다.
4. 작업 난이도에 맞는 모델 메타데이터와 노력 근거를 제안하고 호스트 작업자
   availability를 명시한다.
5. `self-contained`, 절대 경로, 승인 경계를 확인한 뒤 저장한다.

## 경계

일반적인 계획, 구현, `Pending` 사양, 추정에 의한 티켓 생성에는 trigger하지 않는다.
`Ready`가 아니면 후속 단계에 전달하지 않는다. 필수 입력 누락은 `Status: Unverifiable`,
`Pending`/stale/lineage mismatch/coverage 누락은 각각 `Status: Blocked`로 종료하고
`.tigerkit/tickets.md`를 만들지 않는다.
