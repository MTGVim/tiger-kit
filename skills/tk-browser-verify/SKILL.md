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

Browser 도구를 호출하거나 검증용 server를 실행하기 전에 다음 중 하나를 선택하고 [선제 UI Verification](references/ui-verification.md)에서 현재 작업에 해당하는 항목만 적용하세요.

- **Guard mode**: 임시 HTML, prototype, 탐색처럼 지속되는 사용자 노출 source 변경이나 공식 판정이 없는 UI 확인입니다. Responsive matrix나 공식 verdict를 만들지 않고, 시각적 성공을 주장할 때만 screenshot을 실제 검사하세요.
- **Verdict mode**: 지속되는 사용자 노출 UI source 변경, 명시적 호출 또는 공식 판정 요청입니다. 아래 전체 계약을 따르세요.

## 🔴 CHECKPOINT · 🛑 STOP browser launch 경계

browser 또는 검증용 server를 호출하기 전에 mode, 대상 URL, 성공 조건, launch configuration, 안전한 상호작용 범위와 필요한 design intent 결정을 확인하세요. 하나라도 미확정이면 호출하지 말고 `Blocked` 또는 `Unverifiable` receipt에서 멈추세요.

Guard mode를 Verdict mode 완료 gate의 우회로 사용하지 마세요. Guard mode에서는 적용하지 않은 항목의 N/A receipt를 만들지 말고 요청한 결과와 필요한 증거만 보고하세요.

요청을 이해하고 실행 가능한 환경을 찾은 뒤 네이티브 브라우저, Playwright 호환 드라이버, MCP 또는 CDP 드라이버 중 가장 단순한 수단을 선택하세요. 기본 검증은 임시·격리 profile을 사용하며 인증 profile 재사용은 아래 interactive auth 예외에서만 선택 사항입니다.

브라우저 도구를 처음 호출하기 전에 auto-launch 여부와 실제 launch configuration을 확인하세요. 자동 실행 도구는 headless와 임시·격리 profile이 configuration에서 명시적으로 확인될 때만 호출하세요. 스킬 지침, 도구 이름 또는 일반적인 provider 기본값만으로 이를 추정하지 마세요. 조건을 충족하는 대체 수단이 없으면 Verdict mode는 `Unverifiable`로 반환하고 Guard mode는 진행할 수 없는 이유를 보고하세요.

새 브라우저를 시작하면 [세션 수명주기](references/session-lifecycle.md)를 따르세요. 브라우저 자체의 최초 실행·로그인·동기화 안내는 가능한 실행 옵션으로 억제하고, 남아 있으면 로그인하지 말고 안전하게 건너뛰거나 닫으세요. 종료 시 이번 실행이 직접 만든 브라우저·컨텍스트·창만 정리하고 기존 사용자 세션은 건드리지 마세요.

현재 작업에 관련된 관점만 선택하세요. [시각](references/visual.md), [동작](references/behavior.md), [환경](references/environment.md) 또는 [디자인](references/design.md)을 사용하고 [안전](references/safety.md)을 따르세요.

## Verdict mode 계약

아래 계약은 Verdict mode에만 적용합니다. 검증 전에 대상 URL, 실행 환경, 성공 조건, 안전한 상호작용 범위를 확인하세요. 기본은 headless이며 OTP, passkey, CAPTCHA, device approval처럼 사용자 상호작용이 필요한 인증에서만 headed로 전환하고 사용자에게 로그인을 요청하세요. 인증 profile은 repo 밖 사용자 로컬 경로에서 재사용하고 credential, cookie, token, profile 내용을 출력·복사·commit하지 마세요.

Figma, screenshot 또는 디자인 명세가 기준으로 주어지면 탐색이나 상위 구현을 진행하기 전에 [디자인](references/design.md)의 intent preflight를 수행하세요. 보이는 inset이나 간격을 한 요소의 padding으로 단정하지 말고 frame, container, component, child의 중첩 spacing 결과로 분해하세요. 사용자 지시를 해석한 예상 결과와 디자인 기준이 다르거나 불명확하면 양쪽 선택의 구체적 최종 UI, 충족·위반하는 기준, 근거를 제시하고 하나를 명시적으로 선택하도록 요청하세요. 답을 받을 때까지 구현과 browser 실행을 시작하지 않고 `Blocked`로 반환합니다. 침묵은 동의가 아니며 확인되지 않은 차이를 `documented deviation`으로 만들지 마세요.

`design intent preflight → 필요 시 사용자 확인 → 환경 확인 → 탐색 → 상호작용 → UI 전환 관찰 → network 확인 → final state 확인 → screenshot capture → 실제 image 검사 → 판정` 순서를 지키세요. intent가 `same`이면 불필요한 재확인 없이 runtime 검증으로 진행하세요. DOM, accessibility tree, network 성공, 예상 유사성은 screenshot과 실제 시각 검사를 대체하지 않습니다.

Intent preflight의 미결정 `Blocked`는 browser session 전 의사결정 상태입니다. browser를 시작하지 않았으므로 screenshot을 요구하거나 screenshot 부재를 이유로 `Unverifiable`로 바꾸지 말고 `## Alignment` decision receipt를 남기세요. browser session이 시작된 뒤의 성공·실패·runtime 차단 terminal state에는 screenshot capture와 실제 image 검사가 모두 필요합니다. 필요한 viewport와 breakpoint 경계를 검사하지 못했거나 runtime screenshot을 캡처·분석하지 못하면 `Pass`가 아니라 `Unverifiable`입니다. 관찰된 요구사항 위반은 `Fail`, preflight에 필요한 사용자 결정이 없으면 `Blocked`, 안전한 실행 권한이나 환경이 없어 runtime 증거를 만들 수 없으면 `Unverifiable`입니다.

변경 작업에는 UI 전환, 네트워크 요청/응답, 최종 UI 상태가 모두 필요합니다. 토스트나 국소적인 DOM 변경만으로는 충분하지 않습니다. 위험하고 되돌릴 수 없는 작업에 안전한 환경이나 명시적 권한이 없으면 `Unverifiable`을 반환하세요.

유용한 증거만 `.tigerkit/browser-verify/runs/<run-id>/` 아래에 저장하고, 빈 파일은 만들지 마세요. 가능하면 `YYYYMMDD-HHmmss-<short-slug>`를 사용하세요. 확인된 민감하지 않은 사실은 필요할 때 `.tigerkit/browser-verify/env.md` 또는 `.tigerkit/browser-verify/screens/<screen>.md`에 기록하세요. 상위 스크래치 디렉터리는 필요할 때 만들고, 가능하면 원자적으로 교체하며, `.gitignore`를 절대 편집하지 말고, 스크래치가 무시되지 않으면 경고하세요. `login.local.md`를 자동으로 만들지 마세요. 사용자가 명시적으로 요청하면 내용을 출력하지 말고 가능하면 모드 `0600`을 사용하세요. 레거시 전역 TigerKit 상태를 검사하거나 마이그레이션하지 마세요.

프로덕션 코드를 편집하거나 증거를 규칙/스킬로 승격하지 마세요. 디자인 기준이 있으면 `## Alignment`를 생략하지 말고 `Instruction`, `Design basis`, `Spacing stack`, `Relation` (`same | different | unclear`), `Expected implementation`, `User decision`, `Status`를 기록하세요. `different` 또는 `unclear`이면 각 선택의 최종 UI 결과를 별도로 적고 명시적 선택 질문으로 끝내세요. `same`이면 이후 screenshot capture와 실제 image 검사 계획을 기록하세요. `## Verdict` (`Pass | Fail | Blocked | Unverifiable`), `## Verified`, `## Findings`, `## Evidence`, `## Unverified`를 출력하고 빈 섹션은 생략하세요.
