---
name: tk-to-spec
description: "[user] 원시 source evidence를 근거·결정·미확인·충돌로 구분해 repository-local spec.md 초안을 만든다. 추측하거나 구현·ticket 분해는 하지 않는다."
disable-model-invocation: true
argument-hint: "<source evidence 또는 요청>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Evidence를 spec으로 변환

명시적으로 `/tk-to-spec` 또는 `$tk-to-spec` 을 선택한 경우에만 실행한다. 입력은
대화, issue, artifact, repository 조사 결과 등 실제로 읽을 수 있는 source evidence다.
다른 skill을 호출하거나 구현·ticket·원격 상태를 수정하지 않는다.

## 출력 계약

항상 repository root의 `.tigerkit/spec.md` 에 쓰고, 결과에 parse-safe absolute path
`/home/tigeryoo/workspace/tiger-kit/.tigerkit/spec.md` 를 보고한다. 문서는 다음을
직접 포함하는 self-contained Markdown이어야 한다.

- `Status: Pending` (사용자가 명시적으로 승인하기 전에는 downstream이 소비하지 않음)
- source/R-AC와 lineage (각 주장과 출처의 연결)
- goal, scope, exclusions, constraints
- acceptance criteria와 verification 명령/증거
- facts, confirmed decisions, unverified claims를 별도 표시
- missing evidence와 conflicts 및 영향

## 절차

1. source를 읽고 각 문장을 `Fact | Confirmed decision | Unverified claim` 으로 분류한다.
2. 없는 정보는 채우지 말고 `Missing evidence` 로 적는다. 모순은 양쪽 근거와
   해결 owner를 `Conflict` 로 적고 상태를 `Blocked` 또는 `Unverifiable` 로 둔다.
3. goal/scope/제외/제약/acceptance/verification/lineage를 작성한다. 기술적 literal,
   변경 path, 실패 조건도 원문 그대로 둔다.
4. 저장 전 self-contained인지, 승인 경계가 있는지 확인한다. 사용자가 승인하면
   그 명시적 승인만으로 `Pending` 을 `Ready` 로 바꿀 수 있다.

정보가 부족해도 self-contained 문서를 만들고 부족한 항목과 절대 경로를 명시한 뒤
`Status: Unverifiable` 로 멈춘다. conflict가 해소되지 않으면 양쪽 근거를 보존해
`Status: Blocked` 로 멈춘다. `.tigerkit/` 외 state,
archive/current pointer/global 설정은 만들지 않는다.

## 경계

일반적인 계획 작성, 구현, ticket 분해, 단순 질문에는 trigger하지 않는다. 사실을
추론으로 승격하지 않으며, Pending 문서를 downstream 입력으로 전달하지 않는다.
