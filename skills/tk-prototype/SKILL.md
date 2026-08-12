---
name: tk-prototype
description: "[user/auto] 비교로 불확실성을 줄일 수 있을 때 disposable UI 또는 logic prototype을 만들고 실행한다. production implementation이나 대화형 아이디어 탐색에는 적용하지 않는다."
disable-model-invocation: false
argument-hint: "<idea, screenshot, spec, ticket, code, or design reference>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 비교 프로토타입

명시적 `invocation` 또는 실행 가능한 `disposable` 비교/`harness` 요청에 적용한다.
`production implementation`이나 대화만으로 진행되는 탐색에는 자동 적용하지 않는다.

`prompt`, 아이디어, 스크린샷, `spec`, `ticket`, 코드 또는 디자인 reference를 입력으로
받는다. 임시 `route`/`harness`가 더 유용하지 않은 한 `.tigerkit/prototypes/<slug>/`
아래에 작성한다. 상위 디렉터리는 필요할 때만 만들고, 가능하면 원자적으로 교체하며,
자동으로 archive하거나 `.gitignore`를 편집하지 않는다. `scratch`가 tracked 상태이면
경고한다.

## 작업 흐름

1. `hypothesis/success criteria`: 아이디어, reference 및 verification question에서
   측정 가능한 기준을 도출한다.
2. `temporary path/boundary`: repository preflight를 검사하고 기존
   toolchain/UI stack/component/token, 임시 경로, artifact ownership 및
   `fake | real` integration boundary를 선택한다.
3. `variants/harness`: 실제 예시 I/O를 사용해 2–3개 `variant` 또는 `harness`를
   만든다.
4. `run`: 선택한 `variant`/`harness`를 실행하고 실제 output 또는 스크린샷과
   command result를 캡처한다.

각 run은 `## Tested` 아래 다음 receipt 필드로 기록한다. command를 요약하지 말고
실제 실행값을 적는다.

```text
Command: <exact command and arguments>
CWD: <absolute worktree or route path>
Exit code: <integer>
Output: <bounded summary or absolute output path>
Artifact: <absolute path | none>; ownership: run-owned | pre-existing
Screenshot: <absolute path | N/A>; actual inspection: yes | no | N/A
```

5. `compare`: evidence를 criteria에 매핑해 검증된 차이, 미검증 항목 및 다음 결정을
   정리한다. parent contract가 `PR evidence: required`를 기록하면 run-owned absolute
   `Screenshot: <path>`와 실제 이미지 inspection을 `## Tested` 아래 유지하고,
   `evidence_required: true`, criterion, evidence directory 및 producer
   `tk-prototype`을 포함한 제한된 handoff를 노출한다.
6. `terminal summary`: 해당하는 경우 `## Confirmed`, `## Production implication`,
   `## Tested`, `## Variants or harness` 및 `## Still fake`를 반환한다.
   provenance/status block은 추가하지 않는다.

해결되지 않은 UI 비교에서는 전환할 수 있고 실제로 다른 rendered alternative 2–3개를
만든다. 색상만 바꾸지 말고 information architecture, flow, hierarchy, navigation
또는 feedback을 바꾼다. logic에는 example input/output과 최소 adapter를 사용하는
작은 pure harness를 우선한다.

web prototype에서는 repository의 run command, 설치된 UI stack, component 및 design
token을 검사한다. 새 dependency나 manifest/lockfile 변경 없이 안전한 isolated
route/harness를 재사용한다. 없으면 작은
`.tigerkit/prototypes/<slug>/index.html`, `styles.css` 및 `app.js` 를 사용한다.

비교하는 동안 content, data 및 interaction state를 동일하게 유지하면서 decision-relevant
concept 2–3개를 비교한다. 기본값은 wide에서 side-by-side 2–3 columns, narrow에서
stacked다. simultaneous rendering이 concept 또는 minimum legibility를 해칠 때만
명시적 A/B 또는 A/B/C toggle을 사용한다. 세 번째가 independent value를 추가하지
않으면 A/B에서 멈춘다. repository evidence가 결정을 해결하면 prototype을 만들지
않는다.

`tk-browser-verify` Guard mode를 통해 web output을 검증하고 실제 interaction,
`run URL`/`command` 및 `success-criteria` 스크린샷을 포함한다. 개발 서버가 필요하면
정확한 `command`/`cwd`/대상 URL/`auth mode`/`readiness` 조건을 `handoff`하고 서버
시작·대기·종료는 `tk-browser-verify`가 소유한다. `hypothesis`가
responsiveness/layout에 관한 경우에만 wide와 narrow를 확인한다. run-owned tracked
`harness`만 정리하며 `existing route`, `dependency` 및 `production source`는 보존한다.

기본적으로 commit하지 않는다. production abstraction/error handling에 투자하지
않고, output을 production-ready라고 부르거나 auto-promote하지 않으며, 다른 user
skill을 invoke하지 않는다.

PR evidence handoff에서는 screenshot path, run-owned evidence directory, criterion 및
실제 이미지 inspection을 노출한다. 이는 prototype 비교를 증명하는 것이지 official
runtime verdict가 아니다.

## 실패 경로

작성하기 전에 pre-existing 임시 경로와 run-created file을 기록한다.

| 조건 | 첫 조치 | 계속 실패할 때 |
|---|---|---|
| interrupted/partial write | run-owned임이 입증된 불완전 artifact만 정리한다 | `Fail`; unsafe cleanup path와 restart condition을 보고한다 |
| server/harness failure | command, exit state, output 및 fake/real boundary를 보존한다 | `Fail`; production/dependency로 벗어나지 않는다 |
| 실행은 성공했지만 output/screenshot evidence를 사용할 수 없음 | 같은 boundary 안에서 capture를 한 번 재시도한다 | `Unverifiable`; success/Complete라고 주장하지 않는다 |
| ownership/state conflict with existing artifact | existing path를 보존하고 evidence를 기록한다 | `Blocked`; 쓰기 전에 다른 path를 선택한다 |
| cleanup failure | run-owned resource만 다시 식별하고 outcome을 보고한다 | `Fail | Unverifiable`; existing route/process를 보존한다 |
| scope가 production/promotion/commit으로 확장됨 | prototype을 중지하고 별도 implementation request로 분리한다 | `Blocked`; auto-promote하지 않는다 |

## 🔴 CHECKPOINT · 🛑 STOP · 실행 경계

실행 전에 임시 경로, fake/real data 및 verification question을 확인한다.
environment 또는 production-scope expansion이 발생하면 `Blocked | Unverifiable`에서
멈춘다.

보고 전에 command, 실제 output/screenshot, fake/real boundary 및 unverified scope를
대조한다. 하나라도 빠졌거나 실행이 실패하면 `Complete` 가 될 수 없다.
`Fail | Blocked | Unverifiable` 을 사용한다.

## 계약

결정에 필요한 status는 소유 섹션에서 한 번만 기록한다. `## Confirmed`로 시작한 뒤
`## Production implication`, `## Tested`, `## Variants or harness` 및 `## Still fake` 를
이어서 사용하며, 비어 있는 섹션은 생략한다. `Confirmed`는 evidence-backed
conclusion을 소유하고, `Production implication`은 discard/iterate/next decision을,
`Tested`는 command result를, `Variants or harness`는 alternative/path/run URL 및 최종
`kept | removed` state를, `Still fake`는 fake/real 및 unverified scope를 소유한다.
결정 이후에 command mechanics를 둔다.

여러 criteria 또는 variant를 비교할 때 `## Confirmed`를 간결한
`Criterion | A | B [| C] | Conclusion | Evidence` table로 렌더링한다. 사용자와
관련된 row가 하나면 sentence를 사용한다. content/data/state가 동일하게 유지됐는지
기록한다. 관찰하지 못한 차이에는 `not observed`, evidence가 없으면 `unverifiable` 을
사용한다. 감사되지 않은 aesthetic preference를 conclusion으로 승격하지 않는다.
결과와 selection rationale을 2–5개의 bullet 또는 option row로 요약한다.
observation이 8개 이상이면 상위 5–7개를 표시하고 나머지를 소유한 prototype 또는
evidence path를 인용한다. 이는 budget이지 quota가 아니다.

## 금지 패턴

- prototype을 production-ready라고 부르거나 auto-promote/commit하지 않는다.
- fake integration을 real이라고 보고하거나 run evidence 없이 success를 주장하지 않는다.
- color-only variant, dependency, manifest/lockfile edit, 불필요한 production
  abstraction 또는 가치 없는 세 번째 option을 추가하지 않는다.
