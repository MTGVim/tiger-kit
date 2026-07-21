---
name: tk-implement
description: "[user] 요청받은 코드 변경을 구현하고 검증한 뒤 현재 브랜치에 커밋합니다. 사용자에게 보이는 UI 또는 browser behavior가 범위에 있으면 browser 도구보다 먼저 tk-browser-verify를 활성화하고 그 계약 안에서만 호출합니다. 사용자가 명시적으로 호출했을 때만 사용하세요."
disable-model-invocation: true
argument-hint: "<요청, 티켓 또는 명세> [direct|delegated] [tdd|no-tdd]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: implement
    relationship: adapted
---

# 구현

사용자가 이 스킬을 명시적으로 호출했을 때만 사용하세요. 자동으로 활성화하지 마세요.

## 계약

사용자의 명시적 지시는 기본값이나 권장안보다 우선하는 실행 계약입니다. 범위, 방법, 금지 사항, `direct|delegated`, `tdd|no-tdd`, 검증, commit 지시를 임의로 완화·확장·대체하거나 다시 승인받지 마세요. 지시가 서로 충돌하거나 안전하게 실행할 수 없을 때만 구체적 충돌을 설명하고 필요한 결정 하나를 요청하세요.

`understand → inspect → resolve strategy → implement → incremental verification → final verification → bounded review when warranted → commit → report` 순서를 지키세요. 실제로 읽지 않은 요구사항 출처나 실행하지 않은 검증을 확인·통과했다고 보고하지 마세요.

변경 관련 실패가 남으면 `Fail`, 필요한 입력·권한·결정이 없어 진행할 수 없으면 `Blocked`, 검증을 시도했지만 증거를 확보할 수 없으면 `Unverifiable`입니다. 이 상태에서는 완료로 보고하거나 commit하지 마세요. 위임 중첩, 자동 사용자 호출형 skill 실행, hook 우회, 검증 전 commit을 금지합니다.

정보 출처의 우선순위는 현재 요청, 대화에서 확인된 결정, 관련 `.tigerkit/tickets.md`, 관련 `.tigerkit/spec.md`, 저장소 지침, 코드/테스트 순입니다. 기존 파일이라고 해서 자동으로 관련 있는 것은 아닙니다.

관련 spec/ticket에 requirement 또는 acceptance ID가 있으면 구현 범위를 시작할 때 ID 목록을 확정하고, 완료 receipt에서 각 ID를 변경 동작과 검증 evidence에 연결하세요. Source에 ID가 없으면 임의로 만들지 말고 사용한 source 위치를 기록하세요.

## CHECKPOINT / STOP

source mutation 전 조사와 전략을 확정하세요. 요구사항 충돌, 위험한 권한, UI intent 불일치 또는 필수 결정이 남으면 구현하지 말고 해당 근거와 함께 `Blocked`로 멈추세요.

## 전략 결정

수정 전에 관련 코드, 테스트, 스크립트, 상태를 비파괴적으로 조사하세요. 이 단계에서는 파일을 만들거나 수정 또는 삭제하지 말고, 구현 에이전트를 실행하거나 커밋하지 마세요. context-mode, MCP, 검색, 샌드박스 같은 비에이전트 도구는 위임이 아니며 조사와 양쪽 실행 모드에서 사용할 수 있습니다. 브라우저 도구는 비에이전트 도구여도 아래 `tk-browser-verify` 선행 gate를 우회할 수 없습니다.

조사 후 사용자가 정하지 않은 실행 모드와 TDD 여부를 스스로 결정하고 이유를 짧게 알린 뒤 승인 질문 없이 즉시 구현하세요. 작은 변경, 공유 파일, 긴밀한 구현-검증 반복에는 `direct`를 선택하고, 독립 범위와 완료 조건이 명확하며 격리 가치가 큰 작업에만 `delegated`를 선택하세요. 공개 동작 경계, 테스트 인프라, 회귀 위험이 명확하면 TDD를 선택하고, 문구·설정·기계적 변경이나 유용한 테스트 경계가 없으면 non-TDD를 선택하세요.

사용자가 이미 정한 항목은 그대로 따르고, 일부만 정했다면 나머지만 자동 판단하세요. 요구사항 의미가 여러 최종 동작으로 갈리거나 위험하고 되돌릴 수 없는 권한이 필요한 경우에만 사용자 결정을 요청하세요. 구현 전략 자체를 승인 질문으로 막지 마세요. 권장 형식:

```text
구현 전략: direct, TDD 미사용 — 문구 변경이며 유용한 공개 테스트 경계가 없습니다. 구현과 검증을 진행합니다.
```

상세 판단과 위임 계약은 [위임](references/delegation.md)을 참고하세요.

Figma, screenshot 또는 디자인 명세가 예상 UI의 기준이면 source mutation이나 브라우저 도구 호출 전에 hybrid `tk-browser-verify`의 design intent preflight를 적용하세요. 기준과 요청이 충돌하거나 불명확하면 해당 skill의 `Blocked` 경계를 따르고, 정렬된 뒤에만 구현하세요.

## 구현과 검증

Direct에서는 현재 에이전트가 가장 작은 일관된 단위로 구현하고 focused verification을 반복하세요. Delegated에서는 implementor 한 명에게만 범위와 완료 조건을 전달하고 현재 에이전트가 diff와 검증을 확인하세요. 위임을 중첩하거나 하위 에이전트가 사용자 호출형 TigerKit 스킬을 호출하게 해서는 안 됩니다. Implementor에게 브라우저 도구 호출을 맡기지 말고 최종 browser 검증은 현재 에이전트가 소유하세요.

TDD로 결정되면 의미 있는 공개 동작 경계를 선택하고 수직 slice 하나의 focused test를 작성하세요. 테스트를 실제 실행해 red를 관찰한 뒤 최소 구현으로 green을 만들고, 같은 테스트와 관련 검증을 다시 실행하세요. 다음 slice가 있으면 반복하세요. 핵심 loop는 `red → green`이며 refactor를 매 cycle의 필수 단계로 강제하지 않습니다. 구현 후 테스트를 추가해 TDD라고 보고하거나, 이미 성공하는 테스트를 red로 표현하거나, 내부 구현 세부사항을 테스트하거나, 테스트를 위해 production API를 왜곡하지 마세요. 사용자가 TDD를 명시했는데 유용한 seam이 없으면 자동으로 non-TDD로 바꾸지 말고 seam 부재와 가능한 대안을 제시해 결정받으세요. 자동 판단에서는 유용한 seam이 없으면 TDD를 선택하지 마세요. Non-TDD에서도 검증을 생략하지 마세요.

### 🔴 HARD GATE · browser 도구

사용자에게 보이는 UI, layout, styling, responsive behavior, interaction, navigation, form submission 또는 browser network/final state가 범위에 있으면, **브라우저 도구나 검증용 server를 처음 호출하기 전에** hybrid `tk-browser-verify`를 현재 작업의 active verification contract로 적용하고 해당 `SKILL.md`의 mode 선택·launch configuration·안전 범위 checkpoint를 먼저 실행하세요. 단순히 skill 이름을 언급하거나 나중에 결과를 그 형식으로 포장하는 것은 적용이 아닙니다.

`tk-implement`가 Chrome MCP, Playwright, CDP 또는 native browser를 직접 선택·호출하는 것은 금지합니다. 이 수단들은 선행 gate를 통과한 `tk-browser-verify` 안에서만 선택할 수 있습니다. Gate 전에 현재 실행의 browser 호출이 이미 발생했다면 그 evidence는 무효이며, 나중에 skill 형식으로 포장해 복구하지 말고 `Fail`로 멈추며 commit하지 마세요. 사용자가 browser 검증을 금지하거나 skill을 로드·적용할 수 없으면 직접 도구 호출로 대체하지 말고 `Unverifiable`로 멈추며 완료로 보고하거나 commit하지 마세요. DOM, accessibility tree, unit test 또는 build 성공도 runtime screenshot과 실제 image 검사 계약을 대체하지 않습니다.

각 구현 slice 직후 focused test와 관련 정적 검사·build·필요한 브라우저/통합 검증을 실행하고, 다음 slice로 넘어가기 전에 결과를 확인하세요. 모든 slice가 끝나면 실행 가능한 가장 넓은 관련 검증을 한 번 실행하세요. 실패를 `change-related`, `pre-existing`, `environment`, `unverifiable`로 분류하고, 변경 관련 실패가 남으면 커밋하지 마세요.

Final verification에는 당시 branch·`HEAD`와 검증한 diff/path 범위를 함께 기록하세요. 커밋 직전에 현재 branch·`HEAD`·staged diff가 그 범위와 같은지 다시 확인하고, 예상하지 않은 drift나 검증하지 않은 staged 변경이 있으면 커밋하지 말고 사용자 변경을 건드리지 않은 채 영향받은 검증을 다시 실행하거나 `Blocked`로 보고하세요. Commit 자체가 실패하면 broad staging이나 우회 옵션으로 재시도하지 말고 실제 `HEAD`와 미커밋 상태를 `Fail` receipt에 남기세요.

인증·결제·개인정보·권한·마이그레이션·데이터 손실·동시성·공개 API·대규모 구조 변경 또는 테스트하지 않은 고위험 변경이면 독립 reviewer 한 명을 실행하세요. 그 밖의 변경은 review를 생략하고 이유를 report에 기록하세요. 최대 범위는 review 1회, fix 1회, regression verification 1회입니다. [리뷰 경계](references/review-boundary.md)를 참고하세요.

## 커밋과 보고

요청 범위가 완료되고 변경 관련 검증이 성공했으며 작업 diff를 기존 사용자 변경과 안전하게 분리할 수 있으면 현재 브랜치에 커밋하세요. 사용자가 커밋을 금지했거나 구현이 불완전하거나 변경 관련 검증이 실패했으면 커밋하지 마세요. Implementor는 커밋하지 않으며 현재 에이전트가 staged diff를 확인하고 커밋합니다.

별도 요청 없이는 push, PR 생성, merge, tag, release 또는 publish를 하지 마세요. 다른 사용자 호출형 스킬도 자동 실행하지 마세요.

`## Strategy`, `## Changed`, `## Verification`, `## Commit`, 비어 있지 않은 `## Remaining risks`, `## Receipt`를 보고하세요. 파일 목록만이 아니라 동작을 설명하고, 검증 명령과 결과, 실패 분류, 커밋 메시지 또는 미커밋 이유를 포함하세요. Strategy는 선택한 실행 방식·TDD·review와 그 선택 이유만 소유하고 변경 동작이나 검증 명령·결과를 예고·요약하지 않습니다. 변경 설명은 `## Changed`, 검증 명령·결과·실패 분류는 `## Verification`만 소유합니다. Receipt에는 상태(`Pass | Fail | Blocked | Unverifiable`), 미검증 항목과 requirement/acceptance ID별 `Changed`·`Verification` 참조만 기록하고 본문을 반복하지 마세요.

## DO NOT / ANTI-PATTERNS

- 검증 전 commit, 실패가 남은 변경의 commit, push 또는 PR 생성을 하지 마세요.
- 위임을 중첩하거나 하위 agent가 사용자 호출형 skill을 실행하게 하지 마세요.
- `tk-browser-verify`를 먼저 적용하지 않은 채 Chrome MCP·Playwright·CDP·native browser를 직접 호출하지 마세요.
- UI 변경에서 browser runtime evidence를 DOM·unit test·build 성공으로 대체하지 마세요.
