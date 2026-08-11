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

런타임 근거가 필요한 `browser-visible` acceptance criteria에만 사용합니다.
명시적 호출은 criteria를 직접 제공하며, 중첩된 Drive/Respond 경로는 이미 승인된
scenarios, 대상, auth 계획, limitations만 사용합니다.

읽기 전용 acceptance verifier입니다. product/test/설정 소스를 수정하거나 표시되는
browser를 열거나 Markdown 생명주기 장부를 만들지 않습니다. 중첩 실행은
top-level 소유자의 장부에 간결한 사실과 근거 경로를 반환합니다.

## Headless 사전조건

product mutation 전에 모든 필수 시나리오가 headless로 실행될 수 있음을
확인합니다. 지원되는 경로 중 먼저 해당하는 것을 사용합니다.

1. authentication이 필요하지 않음;
2. 현재 headless 상태를 검증할 수 있는, 이미 사용 가능한 안전하고
   run-owned인 authenticated session/profile을 재사용함;
3. 요청 header, cookie, storage bootstrap 같은 저장소/application-supported
   mechanism을 통해 user-supplied short-lived token/session material을 일시적으로
   주입함;
4. OTP, MFA, SSO, CAPTCHA, passkey, device 승인이 없는 저장소-supported
   fully non-interactive login에서만 username/password를 사용함.

injection mechanism을 절대 추측하지 않습니다. 저장소/application 근거 또는
명시적으로 사용자가 제공한 method에 연결한 뒤 resulting authenticated 상태를
검증합니다. interactive authentication이 필요하면 사용 가능한 ephemeral
secret-입력 channel을 통해 적합한 short-lived material을 요청합니다. 안전한
headless authentication을 여전히 확립할 수 없으면 product mutation 전에
`Unverifiable` 을 반환하며 visible browser 대체 경로를 절대 열지 않습니다.

인증 값은 운영 입력으로만 취급합니다. usernames, passwords, tokens,
OTPs, cookies, session values, recovery codes, sensitive identity, secret-bearing
명령, 원시 인증/네트워크 캡처를 대화, `.tigerkit/*.md`, prompts, logs,
요약, 하위 receipt에 절대 출력하거나 저장하지 않습니다. `auth mode: token-headless`,
`authenticated state established` 같은 사실만 기록합니다.

## 🔴 CHECKPOINT / STOP · 브라우저 실행 허가

`🔴 CHECKPOINT` 에서 정확한 기준, 대상/환경, 부모 승인 사실, auth mode,
effective headless argument와 근거 디렉터리를 먼저 고정한다. 이 항목이 검증되기
전에는 브라우저 상호작용이나 product mutation을 시작하지 않는다.

`🛑 STOP` — 안전한 headless authentication 또는 effective `--headless=new` 를 증명할 수
없으면 visible browser 대체 경로를 열지 말고 `Unverifiable` 을 반환한다. 실행 후
criterion별 현재 근거와 실제 inspect한 screenshot이 없으면 `Pass` 를 반환하지
않고 해당 상태를 `Unverifiable` 로 유지한다.

## 작업 흐름

1. **범위(Scope)** — 정확한 기준, 대상 URL/환경, 안전한 interaction
   boundary, 현재 후보 식별자, 부모 승인 사실을 고정합니다.
   일반적인 시각적 비평으로 넓히거나 결정된 product 결정을 다시 열지 않습니다.
2. **준비(Prepare)** — 적용되는 참고 문서만 로드합니다: [환경](references/environment.md),
   [동작](references/behavior.md), [visual](references/visual.md),
   [accessibility](references/accessibility.md), [safety](references/safety.md).
   상위 작업자가 product 상태를 변경하기 전에 auth prerequisite를 증명합니다.
3. **실행 준비(Launch)** — 의존성을 설치하지 않고 사용 가능한 native,
   Playwright-compatible, MCP 또는 verified CDP 경로를 사용합니다. 새
   Chrome/Chromium 프로세스는 첫 browser call 전에 정확한 effective argument
   `--headless=new` 를 반드시 증명해야 합니다. 그렇지 않으면 직접 시작한
   verified headless endpoint에 연결하거나 `Unverifiable` 을 반환합니다.
4. **실행(Run)** — 현재-작업 트리 serving 소스를 증명하고 known 상태에서
   시작하며 trusted interaction을 사용합니다. 필수 요청/응답과 final
   상태를 inspect하고 결정과 관련된 모든 최종 상태에 대해 최소 하나의
   non-empty run-owned screenshot을 캡처합니다. 인용한 이미지는 모두 실제로
   inspect합니다. 승인된 visual 원문/reference 비교에서는
   [visual](references/visual.md)의 asset, content, geometry, typography, color,
   imagery, responsive/상태 축을 각각 검사하고 축 하나라도 생략하지 않습니다:
   logo/SVG/icon/raster/백그라운드의 presence와 rendered integrity; 표시되는 text;
   위치/크기/간격/정렬/자르기; 로드된 글꼴 계열/굵기/크기/줄 높이/
   letter-spacing; 전경/배경/테두리/SVG fill·stroke/opacity/shadow/gradient;
   이미지 소스/로드/고유 크기/비율/object-fit·position; 승인된 viewport와
   hover/focus/활성/disabled/loading/error 상태입니다.
5. **판정(Verdict)** — 승인된 각 criterion과 visual comparison axis를 근거에
   연결하고 `Pass`,
   `Fail`, `Blocked`, `Unverifiable` 를 보고합니다. 근거가 origin을 뒷받침할
   때만 observed 실패를 `change-related`, `pre-existing`, `environment`,
   `unverifiable` 로 분류합니다. 필수 visual axis가 unchecked이면 aggregate
   `Pass`를 반환하지 않습니다.
6. **정리(Cleanup)** — run-owned resource만 닫고 [session lifecycle](references/session-lifecycle.md)을
   사용해 캡처/redaction residue를 확인합니다.

장시간 실행되는 검증 서버는 소유한 백그라운드 프로세스로 실행합니다.
PID/cwd/port/명령과 bounded log 경로를 기록하고, timeout이 있는 구체적인
readiness signal을 poll합니다. 프로세스 exit를 기다리지 말고 readiness 이후
계속합니다.

## 근거와 결과

이진 근거는 run-owned `.tigerkit/evidence/browser/<run-id>/` 디렉터리에
둘 수 있으며, 그곳에 Markdown 파일을 두지 않습니다. proven run-owned 캡처만
이동하고 user fixture는 절대 이동하지 않습니다. 민감한 캡처는 verified
redaction과 residue absence를 확인한 뒤에만 사용할 수 있습니다. 그렇지 않으면
`Unverifiable` 을 반환하고 secret을 보존하지 않습니다.

중첩 결과에는 status, per-criterion 사실, non-sensitive auth mode, absolute
근거 디렉터리, inspected screenshot 경로, limitations, 정리 사실만
포함합니다. 승인된 PR 근거가 필수이면 `evidence_required: true`, 해당
criterion, 생산자 `tk-browser-verify`도 반환하되 upload하지 않습니다.

독립 실행 결과는 `## Verdict` 로 시작하고 `Status: <token>`, `## Verified`,
선택적인 제한된 발견 사항/unverified 사실, `## Evidence`, 정리 사실을
포함합니다. `## Evidence` 에는 absolute 근거 디렉터리와 inspected screenshot을
모두 적습니다. 필수 런타임 근거가 없으면 `Unverifiable` 이며 절대
`Pass` 가 아닙니다.

| 상태 | 의미 |
| --- | --- |
| `Pass` | 승인된 모든 브라우저 기준에 현재 inspected 근거가 있음 |
| `Fail` | 현재 런타임 근거가 승인된 criterion을 위반함 |
| `Blocked` | run 전에 user-owned safety 또는 대상 결정이 필요함 |
| `Unverifiable` | 필수 headless auth, 환경 또는 근거를 확립할 수 없음 |

승인되지 않은 결제, 외부 통신, 파괴적 변경, production-data
mutation, 계정/권한 변경을 절대 일으키지 않습니다. commit, 발행,
product 소스 수정도 절대 하지 않습니다.
