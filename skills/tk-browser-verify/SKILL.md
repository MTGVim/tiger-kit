---
name: tk-browser-verify
description: "[user/auto] 승인된 browser-visible acceptance criteria를 headless browser에서 검증합니다. 명시적 real-page verification 또는 정확한 parent verifier handoff에 사용하며 passive web research, generic design critique, implementation, screenshot-only request에는 사용하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 브라우저 검증

런타임 근거가 필요한 `browser-visible` acceptance criteria만 검증합니다.
명시 호출은 criteria를 직접 제공하고, 중첩 실행은 Ready `seed.md`, `tk-pr-respond`,
`tk-pr-sweep`, `tk-prototype` 등 상위 작업이 이미 정한 대상·시나리오·인증·근거 계획을 사용합니다.

읽기 전용 acceptance verifier입니다. product/test/configuration source, Git commit, remote state를 수정하지 않습니다.
Markdown lifecycle ledger를 만들지 않으며, 중첩 실행은 상위 작업에 compact evidence만 반환합니다.

## Headless 사전조건

필수 시나리오를 모두 headless로 실행할 수 있어야 합니다. 우선순위는 다음과 같습니다.

1. authentication 불필요
2. 이미 검증 가능한 안전한 run-owned authenticated session/profile 재사용
3. repository/application-supported header, cookie, storage bootstrap으로 user-supplied short-lived token/session material 일시 주입
4. OTP, MFA, SSO, CAPTCHA, passkey, device 승인이 없는 fully non-interactive login에서만 username/password 사용

인증 주입 방식을 추측하지 않습니다. 저장소/application evidence 또는 사용자가 명시한 method에 연결하고
resulting authenticated state를 검증합니다.

username, password, token, OTP, cookie, session value, recovery code, sensitive identity는
대화, `.tigerkit/*.md`, prompt, log, summary, child receipt에 저장하지 않습니다.
`auth mode: token-headless`, `authenticated state established` 같은 비민감 사실만 남깁니다.

안전한 headless authentication을 확립할 수 없으면 visible browser로 우회하지 않고 `Unverifiable`입니다.

## Parent handoff

상위 작업은 가능한 경우 다음을 넘깁니다.

- exact acceptance criterion
- target URL/environment
- headless requirement
- auth strategy와 secret-free bootstrap method
- viewport/state
- development server command/cwd/readiness
- 필요한 screenshot evidence
- sensitive capture/redaction rule
- Pass 조건

Ready Seed가 이 정보를 이미 소유하면 같은 결정을 다시 묻지 않습니다.
필수 값이 빠졌지만 repository evidence로 안전하게 확인할 수 있으면 보완합니다.
결과를 바꾸는 user-owned decision만 상위 owner에 반환합니다.

## 실행

1. **범위** — exact criteria, target/environment, current candidate, approved interaction boundary를 고정합니다.
2. **준비** — 필요한 reference만 읽습니다: [환경](references/environment.md), [동작](references/behavior.md), [visual](references/visual.md), [accessibility](references/accessibility.md), [safety](references/safety.md).
3. **실행 준비** — dependency를 새로 설치하지 않고 native, Playwright-compatible, MCP 또는 verified CDP 경로를 사용합니다. 새 Chrome/Chromium process는 effective `--headless=new`를 증명해야 합니다.
4. **서버** — parent가 development server를 요구하면 이 verifier가 background process의 start/readiness/cleanup을 소유합니다. PID/cwd/port/command와 bounded log를 run evidence로 관리하고 process exit가 아니라 readiness signal을 기다립니다.
5. **검증** — known state에서 시작해 required interaction과 final state를 inspect합니다. 결정과 관련된 각 최종 상태에 최소 하나의 non-empty run-owned screenshot을 캡처하고 실제로 inspect합니다.
6. **판정** — 각 criterion을 현재 evidence에 연결해 `Pass | Fail | Blocked | Unverifiable`로 판정합니다. visual 비교가 필요한 경우 asset/content/geometry/typography/color/imagery/responsive/state 축을 빠뜨리지 않습니다.
7. **정리** — run-owned browser/server/resource만 닫고 [session lifecycle](references/session-lifecycle.md)에 따라 residue를 확인합니다.

## 근거

이진 근거는 run-owned `.tigerkit/evidence/browser/<run-id>/`에 둘 수 있으며 Markdown file은 두지 않습니다.
user fixture를 이동하지 않고, 민감한 capture는 verified redaction과 residue absence를 확인한 경우에만 evidence로 사용합니다.

중첩 결과는 다음 정도로 제한합니다.

- status
- criterion별 사실
- non-sensitive auth mode
- absolute evidence directory
- inspected screenshot path
- limitation
- cleanup fact

PR evidence가 필수이면 `evidence_required: true`, 해당 criterion, producer `tk-browser-verify`도 반환하되 upload하지 않습니다.

독립 실행 결과는 `## Verdict`와 정확한 `Status: <token>`으로 시작하고 verified facts, 필요한 limitation, evidence path, cleanup fact를 보여줍니다.
필수 런타임 evidence가 없으면 절대 `Pass`로 올리지 않습니다.

| 상태 | 의미 |
| --- | --- |
| `Pass` | 승인된 모든 브라우저 기준에 현재 inspected evidence가 있음 |
| `Fail` | 현재 런타임 evidence가 criterion을 위반함 |
| `Blocked` | 실행 전에 user-owned safety/target decision이 필요함 |
| `Unverifiable` | 필수 headless auth, environment, evidence를 확립할 수 없음 |

승인되지 않은 결제, 외부 통신, destructive mutation, production-data mutation, 계정/권한 변경을 일으키지 않습니다.
