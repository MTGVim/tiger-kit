---
name: tk-browser-verify
description: "[user/auto] 실제 페이지의 UI 정확성이나 interaction을 브라우저로 확인할 때 사용합니다. 임시 HTML·prototype·layout·hover·form 탐색은 Guard mode로 함정을 선제 방지하고, 사용자에게 보이는 source 변경·명시적 호출·공식 판정 요청은 Verdict mode로 runtime evidence를 검증합니다. Passive web research, 문서 읽기, URL 내용 추출, 단순 screenshot 저장에는 자동 적용하지 않습니다. Source mutation을 소유하거나 browser 없이 충분한 정적 검증을 대체하지 않습니다."
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 브라우저 검증

실제 페이지의 UI 정확성이나 interaction을 browser로 판단할 때 직접 사용하거나 관련 구현 중에 사용하세요. Passive web research, 문서 읽기, URL 내용 추출, 단순 screenshot 저장에는 자동 적용하지 마세요. 사용자가 skill을 명시적으로 호출하면 작업 종류와 관계없이 Verdict mode를 선택하세요.

## 모드 선택

Browser 도구를 호출하거나 검증용 server를 실행하기 전에 다음 중 하나를 선택하고 [선제 UI Verification](references/ui-verification.md)에서 현재 작업에 해당하는 항목만 적용하세요. Form, dialog, navigation 또는 keyboard/focus 동작이 범위에 있으면 [접근성](references/accessibility.md)도 선택하세요. Figma, screenshot 또는 디자인 명세가 실제 입력으로 제공된 경우에만 design intent preflight를 수행하고 `same | different | unclear`를 판정하세요. 디자인 기준이 없으면 alignment는 `N/A`이며 `unclear`, `Blocked` 또는 `## Alignment` receipt를 만들지 마세요.

- **Guard mode**: 임시 HTML, prototype, 탐색처럼 지속되는 사용자 노출 source 변경이나 공식 판정이 없는 UI 확인입니다. Responsive matrix나 공식 verdict를 만들지 않고, 시각적 성공을 주장할 때만 screenshot을 실제 검사하세요.
- **Verdict mode**: 지속되는 사용자 노출 UI source 변경, 명시적 호출 또는 공식 판정 요청입니다. 아래 전체 계약을 따르세요.

Guard mode를 Verdict mode 완료 gate의 우회로 사용하지 마세요. Guard mode에서는 적용하지 않은 항목의 N/A receipt를 만들지 말고 요청한 결과와 필요한 증거만 보고하세요.

요청을 이해하고 실행 가능한 환경을 찾은 뒤 네이티브 브라우저, Playwright 호환 드라이버, MCP 또는 CDP 드라이버 중 가장 단순한 수단을 선택하세요. 기본 검증은 임시·격리 profile을 사용하며 인증 profile 재사용은 아래 interactive auth 예외에서만 선택 사항입니다.

## 🔴 HARD GATE · Chrome `--headless=new`

Guard와 Verdict mode 모두 첫 browser 관련 도구 호출 전에 launch route를 고정하세요. 새 브라우저를 시작하는 기본 route는 임시·격리 profile을 사용하는 owned Chrome/Chromium이며, 실제 launch arguments에 정확한 token `--headless=new`가 있음을 도구 configuration 또는 process argv로 증명해야 합니다. Binary, effective arguments, profile 경로와 소유권을 environment evidence에 기록하세요.

`headless`, `headless: true`, provider 기본값, 도구 이름 또는 스킬 지침만으로 `--headless=new` 적용을 추정하지 마세요. Auto-launch 도구가 정확한 argument의 주입과 확인을 지원하지 않으면 그 도구를 첫 호출로 사용하지 말고, Chrome을 `--headless=new`로 직접 시작해 확인된 CDP endpoint에 연결하세요. 이 route도 만들 수 없으면 headed browser를 열지 말고 Verdict mode는 `Unverifiable`, Guard mode는 진행할 수 없는 이유를 보고하세요.

Credential 직접 입력, OTP, 2FA/2-step verification, passkey, CAPTCHA, device approval처럼 사용자가 직접 로그인을 완료해야 하는 interactive auth가 실제로 필요한 경우에만 headed 예외를 허용하세요. 인증 장벽, 사용자 직접 입력 필요성, 사용자 승인을 browser launch 전에 기록하세요. 단순 visible/headed 요청, headless launch 실패, 빈 화면, timeout, provider 편의 또는 디버깅은 예외가 아니며 headed를 먼저 열거나 자동 fallback하지 마세요.

Interactive login에는 repo 밖 user-local persistent profile을 사용하세요. 사용자가 로그인을 완료하면 headed owned browser를 정상 종료해 profile lock이 해제됐음을 확인하고, 같은 binary와 동일한 `user-data-dir`을 사용해 Chrome을 `--headless=new`로 다시 시작한 뒤 effective arguments를 재검증하고 나머지 검증을 이어가세요. Headed session에서는 로그인 외의 제품 검증·capture를 수행하지 마세요. 같은 인증 profile로 headless 재개를 증명할 수 없으면 headed 상태로 계속하지 말고 `Unverifiable`로 멈추세요. Profile 경로·내용, credential, OTP, cookie 또는 token은 출력·capture·복사·commit하지 마세요. 사용자가 Firefox/Safari 같은 다른 browser를 명시한 경우에만 그 browser의 확인된 native headless mode로 대체하되 headed-first 금지는 그대로 유지하세요.

## Workflow

1. `mode/scope`: 입력은 요청 종류·대상·성공 조건이고, 출력은 Guard/Verdict mode와 안전한 상호작용 범위입니다.
2. `preflight`: 입력은 mode·intent와 선택적 디자인 기준이고, 출력은 필요한 사용자 결정·적용할 reference 축 및 디자인 기준이 있을 때만 `same | different | unclear`, 없으면 `N/A`입니다.
3. `environment`: 입력은 실행 환경과 launch configuration이고, 출력은 browser binary·effective arguments의 정확한 `--headless=new`·격리 profile·headed 예외 부재 또는 승인 확인입니다.
4. `run/evidence`: 입력은 확인된 환경과 범위이고, 출력은 대상 identity·안전한 사전 상태와 탐색·상호작용·network·최종 상태·screenshot·실제 image 검사 및 조건부 keyboard/focus/semantic 증거입니다.
5. `verdict`: 입력은 runtime evidence와 성공 조건이고, 출력은 `Pass | Fail | Blocked | Unverifiable` 및 미검증 항목입니다.
6. `receipt/cleanup`: 입력은 판정과 생성한 세션·증거이고, 출력은 필요한 receipt와 이번 실행이 만든 browser/context/window만 정리한 결과입니다.

새 브라우저를 시작하면 [세션 수명주기](references/session-lifecycle.md)를 따르세요. 브라우저 자체의 최초 실행·로그인·동기화 안내는 가능한 실행 옵션으로 억제하고, 남아 있으면 로그인하지 말고 안전하게 건너뛰거나 닫으세요. 종료 시 이번 실행이 직접 만든 브라우저·컨텍스트·창만 정리하고 기존 사용자 세션은 건드리지 마세요.

현재 작업에 관련된 관점만 선택하세요. [시각](references/visual.md), [동작](references/behavior.md), [환경](references/environment.md), [디자인](references/design.md) 또는 [접근성](references/accessibility.md)을 사용하고 [안전](references/safety.md)을 따르세요.

## CHECKPOINT / STOP

브라우저 도구나 검증용 server를 호출하기 직전에 mode, launch configuration, 정확한 `--headless=new` evidence와 안전한 상호작용 범위를 확인하세요. 이 launch evidence 없이 browser 도구를 호출하지 마세요. 제공된 디자인 기준과 intent가 `different | unclear`이면 사용자의 명시적 선택 전 `Blocked`로 멈추고, runtime 증거를 만들 수 없으면 `Unverifiable`로 멈춥니다.

### Browser 시작 전 종료 출력

Browser session을 만들기 전에 멈추면 실행 예정 checklist 전체나 빈 evidence section을 나열하지 마세요. 디자인 결정이 원인이면 `## Alignment`와 한 개의 선택 질문만, 그 밖의 경우에는 terminal status·한 줄 원인·재개에 필요한 입력만 보고하세요. 재개 조건에는 정확한 `--headless=new` launch proof와 첫 capture 전 TigerKit ledger 지정을 한 줄로 명시하세요. 생성한 resource가 없으면 cleanup은 한 문장으로 끝내세요.

## 🔴 HARD GATE · capture ledger

Guard와 Verdict mode 모두 첫 capture 전에 `.tigerkit/browser-verify/runs/<run-id>/`를 이번 실행의 유일한 capture ledger로 정하고 이번 실행이 생성할 screenshot, trace, video, network/HAR, console dump의 destination을 기록하세요. 가능하면 browser 도구의 출력 경로를 처음부터 ledger 안으로 지정하세요.

도구가 capture를 tool temp, 기본 download, 사용자 scratch 또는 ledger 밖의 다른 경로에 강제로 만들면 capture 직후 이번 실행 소유권이 확인된 파일만 ledger로 옮기세요. 사용자 제공 screenshot·fixture, 기존 파일, 다른 실행의 artifact는 입력 evidence로 참조할 뿐 이동·이름 변경·삭제하지 마세요. 소유권이나 원본 경로가 불명확하면 추정해 옮기지 말고 `Blocked`로 멈추세요.

Verdict 또는 Guard 결과를 보고하기 전에 capture inventory의 각 항목에 종류, 원본 경로, ledger 경로, 소유권, 이동 결과를 기록하고 다음을 모두 확인하세요.

- ledger 파일이 존재하고 비어 있지 않습니다.
- 이번 실행이 생성한 capture가 tool temp·기본 download·사용자 scratch 등 ledger 밖에 남아 있지 않습니다.
- receipt와 판정은 ledger 경로만 인용합니다.

이동·존재·잔존 여부 중 하나라도 확인할 수 없으면 capture를 evidence로 사용하지 말고 `Unverifiable`로 멈추세요. 정리 실패를 숨기거나 ledger 밖 경로를 최종 evidence로 보고하지 마세요. 상위 `.tigerkit/`이 version control에서 제외되지 않으면 경고하되 `.gitignore`를 수정하지 마세요.

## Verdict mode 계약

아래 계약은 Verdict mode에만 적용합니다. 검증 전에 대상 URL, 실행 환경, 성공 조건, 안전한 상호작용 범위를 확인하고 위 Chrome `--headless=new` gate를 통과하세요. Interactive auth 예외에서만 사용자 승인 후 headed로 전환하고 사용자에게 로그인을 요청하세요. 로그인 완료 직후 headed browser를 종료하고 동일한 persistent profile을 `--headless=new`로 재개한 뒤에만 검증을 계속하세요.

Figma, screenshot 또는 디자인 명세가 기준으로 주어지면 탐색이나 상위 구현을 진행하기 전에 [디자인](references/design.md)의 intent preflight를 수행하세요. 보이는 inset이나 간격을 한 요소의 padding으로 단정하지 말고 frame, container, component, child의 중첩 spacing 결과로 분해하세요. 사용자 지시를 해석한 예상 결과와 디자인 기준이 다르거나 불명확하면 양쪽 선택의 구체적 최종 UI, 충족·위반하는 기준, 근거를 제시하고 하나를 명시적으로 선택하도록 요청하세요. 답을 받을 때까지 구현과 browser 실행을 시작하지 않고 `Blocked`로 반환합니다. 침묵은 동의가 아니며 확인되지 않은 차이를 `documented deviation`으로 만들지 마세요. 디자인 기준이 입력되지 않았다면 이 paragraph 전체를 적용하지 마세요.

### 실행 증거와 중단

`design intent preflight → 필요 시 사용자 확인 → 환경 확인 → 탐색 → 상호작용 → UI 전환 관찰 → network 확인 → final state 확인 → screenshot capture → 실제 image 검사 → 판정` 순서를 지키세요. intent가 `same`이면 불필요한 재확인 없이 runtime 검증으로 진행하세요. DOM, accessibility tree, network 성공, 예상 유사성은 screenshot과 실제 시각 검사를 대체하지 않습니다.

Intent preflight의 미결정 `Blocked`는 browser session 전 의사결정 상태입니다. browser를 시작하지 않았으므로 screenshot을 요구하거나 screenshot 부재를 이유로 `Unverifiable`로 바꾸지 말고 `## Alignment` decision receipt를 남기세요. browser session이 시작된 뒤의 성공·실패·runtime 차단 terminal state에는 screenshot capture와 실제 image 검사가 모두 필요합니다. 필요한 viewport와 breakpoint 경계를 검사하지 못했거나 runtime screenshot을 캡처·분석하지 못하면 `Pass`가 아니라 `Unverifiable`입니다. 관찰된 요구사항 위반은 `Fail`, preflight에 필요한 사용자 결정이 없으면 `Blocked`, 안전한 실행 권한이나 환경이 없어 runtime 증거를 만들 수 없으면 `Unverifiable`입니다.

Browser 연결 중단, page crash, navigation timeout 또는 성공 조건에 없는 route/tab 변경으로 흐름이 끊기면 그 실행의 부분 증거를 판정에 합치지 마세요. 같은 대상·환경·안전한 사전 상태를 다시 확인할 수 있을 때만 새 흐름으로 한 번 재시도하고, 그렇지 않으면 Verdict mode는 `Unverifiable`, Guard mode는 진행하지 못한 범위를 보고하세요. 중단 여부와 관계없이 owned resource cleanup은 시도하고 결과를 receipt에 남기세요.

변경 작업에는 UI 전환, 네트워크 요청/응답, 최종 UI 상태가 모두 필요합니다. 토스트나 국소적인 DOM 변경만으로는 충분하지 않습니다. 위험하고 되돌릴 수 없는 작업에 안전한 환경이나 명시적 권한이 없으면 `Unverifiable`을 반환하세요.

### 증거 보관과 보고

유용한 증거만 capture ledger 아래에 보관하고 빈 파일은 만들지 마세요. Run ID는 가능하면 `YYYYMMDD-HHmmss-<short-slug>`를 사용하세요. 확인된 민감하지 않은 사실은 필요할 때 `.tigerkit/browser-verify/env.md` 또는 `.tigerkit/browser-verify/screens/<screen>.md`에 기록하세요. 상위 디렉터리는 필요할 때 만들고 가능하면 원자적으로 교체하세요. `login.local.md`를 자동으로 만들지 마세요. 사용자가 명시적으로 요청하면 내용을 출력하지 말고 가능하면 모드 `0600`을 사용하세요. 레거시 전역 TigerKit 상태를 검사하거나 마이그레이션하지 마세요.

프로덕션 코드를 편집하거나 증거를 규칙/스킬로 승격하지 마세요. 디자인 기준이 있으면 `## Alignment`를 생략하지 말고 `Instruction`, `Design basis`, `Spacing stack`, `Relation` (`same | different | unclear`), `Expected implementation`, `User decision`, `Status`를 기록하세요. Alignment의 `Status`는 사용자 정렬 상태인 `confirmed | pending | Blocked`이며 runtime `Verdict`가 아닙니다. `different` 또는 `unclear`이면 각 선택의 최종 UI 결과를 별도로 적고 명시적 선택 질문으로 끝내세요. `same`이면 이후 screenshot capture와 실제 image 검사 계획을 기록하세요. `## Verdict`는 전체 판정, `## Verified`는 성공 조건별 확인 결과, `## Findings`는 편차·실패, `## Evidence`는 이를 뒷받침하는 경로·관찰·capture, `## Unverified`는 검사하지 못한 범위, `## Cleanup`은 owned resource 정리 결과만 소유합니다. 이 내용이 있는 섹션들이 receipt 전체이므로 별도 `## Receipt`를 만들거나 Verdict를 다시 쓰지 마세요. 각 사실은 가장 구체적인 한 섹션에만 쓰고 다른 섹션에서는 참조하며, 비어 있는 Findings·Unverified·Cleanup은 생략하세요.

## DO NOT / ANTI-PATTERNS

- launch configuration 없이 자동 브라우저를 호출하지 마세요.
- 정확한 `--headless=new` evidence 없이 Chrome/Chromium browser 도구를 호출하거나 headed browser를 먼저 열지 마세요.
- Headless 실패를 headed retry나 provider auto-launch fallback으로 우회하지 마세요.
- 사용자가 직접 완료해야 하는 interactive login 없이 visible/headed 요청만으로 headed 예외를 만들지 마세요.
- 로그인 완료 뒤 headed session에서 제품 검증을 계속하거나 다른 profile의 headless session으로 인증 상태를 잃지 마세요.
- 이번 실행이 생성한 capture를 tool temp·기본 download·사용자 scratch에 남기거나 ledger 밖 경로를 최종 evidence로 보고하지 마세요.
- 사용자 제공 screenshot·fixture 또는 소유권이 불명확한 artifact를 ledger로 이동하지 마세요.
- DOM, accessibility tree 또는 network 성공을 screenshot 실제 검사 대신 사용하지 마세요.
- 실제 결제·삭제·외부 발송처럼 되돌릴 수 없는 동작을 안전한 환경과 명시적 권한 없이 실행하지 마세요.
- Keyboard/focus/semantic evidence를 screenshot으로 대체하거나 제한된 flow 검사로 전체 WCAG 준수를 주장하지 마세요.
