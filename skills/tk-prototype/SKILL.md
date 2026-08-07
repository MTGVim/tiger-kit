---
name: tk-prototype
description: "[user/auto] 비교로 불확실성을 줄일 수 있을 때 disposable UI 또는 logic prototype을 만들고 실행한다. production implementation이나 대화형 아이디어 탐색에는 적용하지 않는다."
argument-hint: "<idea, screenshot, spec, ticket, code, or design reference>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Prototype(프로토타입)

명시적 invocation 또는 실행 가능한 disposable comparison/harness 요청에 적용한다.
production implementation이나 대화만으로 진행되는 exploration에는 자동 적용하지
않는다.

prompt, idea, screenshot, spec, ticket, code 또는 design reference를 입력으로 받는다.
temporary route/harness가 더 유용하지 않은 한 `.tigerkit/prototypes/<slug>/` 아래에
작성한다. 상위 디렉터리는 필요할 때만 만들고, 가능하면 원자적으로 교체하며, 자동으로
archive하거나 `.gitignore`를 편집하지 않는다. scratch가 tracked 상태이면 경고한다.

## 작업 흐름

1. `hypothesis/success criteria`: 아이디어, references 및 verification question에서
   measurable criteria를 도출한다.
2. `temporary path/boundary`: repository preflight를 검사하고 기존
   toolchain/UI stack/components/tokens, temp path, artifact ownership 및
   `fake | real` integration boundary를 선택한다.
3. `variants/harness`: real example I/O를 사용해 2–3개 variants 또는 harness를
   만든다.
4. `run`: 선택한 variants/harness를 실행하고 actual output 또는 screenshots와
   command result를 캡처한다.
5. `compare`: evidence를 criteria에 매핑해 verified differences, unverified items
   및 next decision을 정리한다. parent contract가 `PR evidence: required`를
   기록하면 run-owned absolute `Screenshot: <path>`와 actual image inspection을
   `## Tested` 아래 유지하고, `evidence_required: true`, criterion, evidence
   directory 및 producer `tk-prototype`을 포함한 제한된 handoff를 노출한다.
6. `terminal summary`: 해당하는 경우 `## Confirmed`, `## Production implication`,
   `## Tested`, `## Variants or harness` 및 `## Still fake`를 반환한다.
   provenance/status block은 추가하지 않는다.

해결되지 않은 UI comparison에서는 switch가 있는, 실질적으로 다른 rendered
alternatives 2–3개를 만든다. color만 바꾸지 말고 information architecture, flow,
hierarchy, navigation 또는 feedback을 바꾼다. logic에는 example inputs/outputs와
minimal adapter를 사용하는 small pure harness를 우선한다.

web prototype에서는 repository의 run commands, installed UI stack, components 및
design tokens를 검사한다. 새 dependency나 manifest/lockfile 변경 없이 안전한
isolated route/harness를 재사용한다. 없으면 작은
`.tigerkit/prototypes/<slug>/index.html`, `styles.css` 및 `app.js`를 사용한다.

비교하는 동안 content, data 및 interaction state를 동일하게 유지하면서 decision-relevant
concept 2–3개를 비교한다. 기본값은 wide에서 side-by-side 2–3 columns, narrow에서
stacked다. simultaneous rendering이 concept 또는 minimum legibility를 해칠 때만
명시적 A/B 또는 A/B/C toggle을 사용한다. 세 번째가 independent value를 추가하지
않으면 A/B에서 멈춘다. repository evidence가 decision을 해결하면 prototype을 만들지
않는다.

`tk-browser-verify` Guard mode를 통해 web output을 검증하고 actual interaction,
run URL/command 및 success-criteria screenshots를 포함한다. hypothesis가
responsiveness/layout에 관한 경우에만 wide와 narrow를 확인한다. run-owned tracked
harness와 temporary server만 정리하며 existing routes, dependencies 및 production
source는 보존한다.

기본적으로 commit하지 않는다. production abstractions/error handling에 투자하지
않고, output을 production-ready라고 부르거나 auto-promote하지 않으며, 다른 user
skill을 invoke하지 않는다.

PR evidence handoff에서는 screenshot path, run-owned evidence directory, criterion 및
actual image inspection을 노출한다. 이는 prototype comparison을 증명하는 것이지
official runtime verdict가 아니다.

## 실패 경로

작성하기 전에 pre-existing temp path와 run-created file을 기록한다.

| 조건 | 첫 조치 | 계속 실패할 때 |
|---|---|---|
| interrupted/partial write | run-owned임이 입증된 불완전 artifact만 정리한다 | `Fail`; unsafe cleanup path와 restart condition을 보고한다 |
| server/harness failure | command, exit state, output 및 fake/real boundary를 보존한다 | `Fail`; production/dependencies로 벗어나지 않는다 |
| run succeeds but output/screenshot evidence is unavailable | 같은 boundary 안에서 capture를 한 번 재시도한다 | `Unverifiable`; success/Complete라고 주장하지 않는다 |
| ownership/state conflict with existing artifact | existing path를 보존하고 evidence를 기록한다 | `Blocked`; 쓰기 전에 다른 path를 선택한다 |
| cleanup failure | run-owned resource만 다시 식별하고 outcome을 보고한다 | `Fail | Unverifiable`; existing route/process를 보존한다 |
| scope expands into production/promotion/commit | prototype을 중지하고 별도 implementation request로 분리한다 | `Blocked`; auto-promote하지 않는다 |

## 🔴 CHECKPOINT · 🛑 STOP · 실행 경계(execution boundaries)

실행 전에 temp path, fake/real data 및 verification question을 확인한다.
environment 또는 production-scope expansion이 발생하면 `Blocked | Unverifiable`에서
멈춘다.

보고 전에 command, actual output/screenshot, fake/real boundary 및 unverified scope를
대조한다. 하나라도 빠졌거나 실행이 실패하면 `Complete`가 될 수 없다.
`Fail | Blocked | Unverifiable`을 사용한다.

## 계약(Contract)

결정에 필요한 status는 소유 섹션에서 한 번만 기록한다. `## Confirmed`로 시작한 뒤
`## Production implication`, `## Tested`, `## Variants or harness` 및 `## Still fake`를
이어서 사용하며, 비어 있는 섹션은 생략한다. `Confirmed`는 evidence-backed
conclusion을 소유하고, `Production implication`은 discard/iterate/next decision을,
`Tested`는 command result를, `Variants or harness`는 alternative/path/run URL 및 최종
`kept | removed` state를, `Still fake`는 fake/real 및 unverified scope를 소유한다.
결정 이후에 command mechanics를 둔다.

여러 criteria 또는 variants를 비교할 때 `## Confirmed`를 간결한
`Criterion | A | B [| C] | Conclusion | Evidence` table로 렌더링한다. 사용자와
관련된 row가 하나면 sentence를 사용한다. content/data/state가 동일하게 유지됐는지
기록한다. 관찰하지 못한 차이에는 `not observed`, evidence가 없으면 `unverifiable`을
사용한다. 감사되지 않은 aesthetic preference를 conclusion으로 승격하지 않는다.
결과와 selection rationale을 두 개에서 다섯 개의 bullet 또는 option row로 요약한다.
observation이 8개 이상이면 상위 5–7개를 표시하고 나머지를 소유한 prototype 또는
evidence path를 인용한다. 이는 budget이지 quota가 아니다.

## DO NOT / 금지 패턴(ANTI-PATTERNS)

- prototype을 production-ready라고 부르거나 auto-promote/commit하지 않는다.
- fake integration을 real이라고 보고하거나 run evidence 없이 success를 주장하지 않는다.
- color-only variant, dependency, manifest/lockfile edit, 불필요한 production
  abstraction 또는 가치 없는 세 번째 option을 추가하지 않는다.
