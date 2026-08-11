---
name: tk-browser-verify
description: "[user/auto] 승인된 browser-visible acceptance criteria를 headless browser에서 검증합니다. 명시적 real-page verification 또는 정확한 parent verifier handoff에 사용하며, passive web research, generic design critique, implementation, screenshot-only request에는 사용하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 브라우저 검증

runtime evidence가 필요한 browser-visible acceptance criteria에만 사용합니다.
명시적 호출은 criteria를 직접 제공하며, nested Drive/Respond route는 이미 승인된
scenarios, target, auth plan, limitations만 사용합니다.

read-only acceptance verifier입니다. product/test/config source를 수정하거나 visible
browser를 열거나 Markdown lifecycle ledger를 만들지 않습니다. nested run은
top-level owner의 ledger에 compact facts와 evidence paths를 반환합니다.

## Headless 사전조건

product mutation 전에 모든 required scenario가 headlessly 실행될 수 있음을
확인합니다. 지원되는 route 중 먼저 해당하는 것을 사용합니다.

1. authentication이 필요하지 않음;
2. current headless state를 검증할 수 있는, 이미 사용 가능한 safe하고
   run-owned인 authenticated session/profile을 재사용함;
3. request header, cookie, storage bootstrap 같은 repository/application-supported
   mechanism을 통해 user-supplied short-lived token/session material을 일시적으로
   주입함;
4. OTP, MFA, SSO, CAPTCHA, passkey, device approval이 없는 repository-supported
   fully non-interactive login에서만 username/password를 사용함.

injection mechanism을 절대 추측하지 않습니다. repository/application evidence 또는
명시적으로 사용자가 제공한 method에 연결한 뒤 resulting authenticated state를
검증합니다. interactive authentication이 필요하면 사용 가능한 ephemeral
secret-input channel을 통해 적합한 short-lived material을 요청합니다. safe
headless authentication을 여전히 확립할 수 없으면 product mutation 전에
`Unverifiable` 을 반환하며 visible-browser fallback을 절대 열지 않습니다.

Auth values는 operational input으로만 취급합니다. usernames, passwords, tokens,
OTPs, cookies, session values, recovery codes, sensitive identity, secret-bearing
commands, raw auth/network captures를 chat, `.tigerkit/*.md`, prompts, logs,
summaries, child receipts에 절대 echo하거나 persist하지 않습니다. `auth mode: token-headless`,
`authenticated state established` 같은 fact만 기록합니다.

## 🔴 CHECKPOINT / STOP · browser 실행 허가

`🔴 CHECKPOINT` 에서 exact criteria, target/environment, parent approval facts, auth mode,
effective headless argument와 evidence directory를 먼저 고정한다. 이 항목이 검증되기
전에는 browser interaction이나 product mutation을 시작하지 않는다.

`🛑 STOP` — safe headless authentication 또는 effective `--headless=new` 를 증명할 수
없으면 visible-browser fallback을 열지 말고 `Unverifiable` 을 반환한다. 실행 후
criterion별 current evidence와 실제 inspect한 screenshot이 없으면 `Pass` 를 반환하지
않고 해당 상태를 `Unverifiable` 로 유지한다.

## 작업 흐름

1. **범위(Scope)** — exact criteria, target URL/environment, safe interaction
   boundary, current candidate identity, parent approval facts를 고정합니다.
   generic visual critique로 넓히거나 결정된 product decision을 다시 열지 않습니다.
2. **준비(Prepare)** — 적용되는 reference만 로드합니다: [environment](references/environment.md),
   [behavior](references/behavior.md), [visual](references/visual.md),
   [accessibility](references/accessibility.md), [safety](references/safety.md).
   parent worker가 product state를 변경하기 전에 auth prerequisite를 증명합니다.
3. **실행 준비(Launch)** — dependency를 설치하지 않고 사용 가능한 native,
   Playwright-compatible, MCP 또는 verified CDP route를 사용합니다. 새
   Chrome/Chromium process는 첫 browser call 전에 exact effective argument
   `--headless=new` 를 반드시 증명해야 합니다. 그렇지 않으면 직접 시작한
   verified headless endpoint에 연결하거나 `Unverifiable` 을 반환합니다.
4. **실행(Run)** — current-worktree serving source를 증명하고 known state에서
   시작하며 trusted interaction을 사용합니다. required request/response와 final
   state를 inspect하고 decision-relevant한 모든 final state에 대해 최소 하나의
   non-empty run-owned screenshot을 capture합니다. 인용한 image는 모두 실제로
   inspect합니다. 승인된 visual verbatim/reference 비교에서는
   [visual](references/visual.md)의 asset, content, geometry, typography, color,
   imagery, responsive/state 축을 각각 검사하고 축 하나라도 생략하지 않습니다:
   logo/SVG/icon/raster/background의 presence와 rendered integrity; visible text;
   position/dimensions/spacing/alignment/crop; loaded font family/weight/size/line-height/
   letter-spacing; foreground/background/border/SVG fill·stroke/opacity/shadow/gradient;
   image source/load/intrinsic size/aspect/object-fit·position; 승인된 viewport와
   hover/focus/active/disabled/loading/error state입니다.
5. **판정(Verdict)** — 승인된 각 criterion과 visual comparison axis를 evidence에
   연결하고 `Pass`,
   `Fail`, `Blocked`, `Unverifiable` 를 보고합니다. evidence가 origin을 뒷받침할
   때만 observed failure를 `change-related`, `pre-existing`, `environment`,
   `unverifiable` 로 분류합니다. required visual axis가 unchecked이면 aggregate
   `Pass`를 반환하지 않습니다.
6. **정리(Cleanup)** — run-owned resource만 닫고 [session lifecycle](references/session-lifecycle.md)을
   사용해 capture/redaction residue를 확인합니다.

Long-running verification server는 owned background process로 실행합니다.
PID/cwd/port/command와 bounded log path를 기록하고, timeout이 있는 concrete
readiness signal을 poll합니다. process exit를 기다리지 말고 readiness 이후
계속합니다.

## Evidence와 result

Binary evidence는 run-owned `.tigerkit/evidence/browser/<run-id>/` directory에
둘 수 있으며, 그곳에 Markdown file을 두지 않습니다. proven run-owned capture만
이동하고 user fixture는 절대 이동하지 않습니다. Sensitive capture는 verified
redaction과 residue absence를 확인한 뒤에만 사용할 수 있습니다. 그렇지 않으면
`Unverifiable` 을 반환하고 secret을 보존하지 않습니다.

nested result에는 status, per-criterion facts, non-sensitive auth mode, absolute
evidence directory, inspected screenshot paths, limitations, cleanup facts만
포함합니다. 승인된 PR evidence가 required이면 `evidence_required: true`, 해당
criterion, producer `tk-browser-verify`도 반환하되 upload하지 않습니다.

standalone result는 `## Verdict` 로 시작하고 `Status: <token>`, `## Verified`,
선택적인 bounded findings/unverified facts, `## Evidence`, cleanup facts를
포함합니다. `## Evidence` 에는 absolute evidence directory와 inspected screenshot을
모두 적습니다. required runtime evidence가 없으면 `Unverifiable` 이며 절대
`Pass` 가 아닙니다.

| 상태 | 의미 |
| --- | --- |
| `Pass` | 승인된 모든 browser criterion에 current inspected evidence가 있음 |
| `Fail` | current runtime evidence가 승인된 criterion을 위반함 |
| `Blocked` | run 전에 user-owned safety 또는 target decision이 필요함 |
| `Unverifiable` | required headless auth, environment 또는 evidence를 확립할 수 없음 |

unauthorized payment, external communication, destructive change, production-data
mutation, account/permission change를 절대 일으키지 않습니다. commit, publish,
product source 수정도 절대 하지 않습니다.
