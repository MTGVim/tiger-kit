---
name: tk-to-tickets
description: "[user] Ready 상태의 fresh spec을 독립적으로 관찰 가능한 vertical ticket으로 분해하고 tickets.md를 작성합니다."
disable-model-invocation: true
argument-hint: "<Ready spec 경로 또는 source>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Spec을 ticket으로 변환

명시적으로 `/tk-to-tickets` 또는 `$tk-to-tickets`를 선택한 경우에만 실행한다.
먼저 `/home/tigeryoo/workspace/tiger-kit/.tigerkit/spec.md`를 읽고, `Status: Ready`이며
현재 요청과 lineage가 일치하는 fresh spec만 소비한다. required spec/evidence가
누락되면 정확히 `Status: Unverifiable`로 멈춘다. `Pending`이면 정확히
`Status: Blocked`로 멈추고 downstream ticket을 생성하지 않는다. stale spec 또는
lineage mismatch도 각각 정확히 `Status: Blocked`로 멈춘다.

## 출력 계약

항상 `/home/tigeryoo/workspace/tiger-kit/.tigerkit/tickets.md`에 self-contained
Markdown을 쓰고 absolute path를 보고한다. ticket마다 다음 필드를 포함한다.

`Status`, `Goal`, `Coverage`(source/R-AC mapping), `Scope`, `Entry points`,
`Dependencies`(`none` when absent), `Acceptance`, `Verification`, `model`,
`effort`, `rationale`, `lineage`.

Coverage의 각 source/R-AC는 정확히 한 ticket에 매핑하거나 명시적으로 `uncovered`
사유를 적는다. ticket은 layer-only가 아니라 independently observable한 vertical
slice여야 한다. `model`과 `effort`는 provider 이름이 아닌 symbolic capability tier로
제안하고 rationale을 적는다. host mapping이 없으면 mapping을 발명하지 말고
setup prerequisite로 표시하며 `tk-wizard`를 먼저 사용하도록 한다.

문서 끝에는 downstream 소비 전 사용자의 명시적 approval이 필요하다는 경계를 둔다.
구현, 원격 issue, global archive/state, `.tigerkit/` 외 출력은 하지 않는다.

## 절차

1. spec의 상태, freshness, lineage, source/R-AC와 acceptance를 검증한다.
2. coverage를 수집해 각 항목을 한 번만 vertical ticket에 배치한다. 누락·충돌은
   멈추고 원문과 이유를 보존한다.
3. 각 ticket의 entry point부터 observable acceptance와 verification까지 작성한다.
4. capability tier와 effort tier를 제안하고 host mapping 유무를 명시한다.
5. self-contained, absolute path, approval boundary를 확인한 뒤 저장한다.

## 경계

일반적인 planning, 구현, Pending spec, 추정에 의한 ticket 생성에는 trigger하지 않는다.
Ready가 아니면 downstream에 전달하지 않는다. required 입력 누락은 `Status: Unverifiable`, Pending/stale/lineage mismatch/coverage 누락은 각각 `Status: Blocked`로 종료한다.
