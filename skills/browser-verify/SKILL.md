---
name: browser-verify
description: browser-verify 엔진 트리거입니다.
---

# Browser Verify

시각 회귀(모달, 레이아웃, spacing, color, overlay)와 동작(상호작용 결과)을 눈대중이 아니라 computed style / bounding rect / network 관측 중심으로 검증합니다.

## Profile lookup

제품 특이값은 hard-code하지 않습니다. 실행 시 아래 순서로 profile을 찾습니다.

1. `~/.tigerkit/repos/<repo-key>/browser-verify/`
2. 신경로가 없고 legacy `~/.tigerkit/repos/<repo-key>/ui-diff/`가 있으면 **자동 이동하지 않고 migration guide로 멈춥니다.**
3. 둘 다 없으면 bundled template(`skills/browser-verify/templates/`)를 source로 삼아 현재 repo에 대응하는 신규 생성 절차로 들어갑니다.

이 엔진은 user-global provisioning/install flow를 직접 수행하지 않습니다. 다만 현재 repo profile이 비어 있으면 repo-scoped missing 파일만 생성하는 bootstrap은 허용합니다.

## Mode overview

| Mode | Baseline | Target | 비교물 | Status |
|---|---|---|---|---|
| env-diff | QA/live runtime | local runtime | computed style / rect | primary |
| figma-diff | design node/spec | local runtime | computed style / rect | secondary |
| behavior-verify | SoT(티켓/PRD/스펙/요청 서술) | local runtime | 상호작용 결과 | primary |

상세는 `references/modes/`를 봅니다.

## Engine / profile split

- engine: repo에 번들된 reusable procedural skill
- profile: 현재 repo에 대응하는 `~/.tigerkit` 아래 URL, login, context, screens catalog

엔진은 공용 지식을 제공하고, 프로젝트 특이값은 repo-scoped profile에만 둡니다.

## Login override

login data는 기본 `login.md`에서 읽고, local override가 있으면 `login.local.md`를 이어서 봅니다.

```text
login.md -> login.local.md
```

tracked repo에는 credential을 직접 커밋하지 않습니다.

## Driver policy

1. MCP driver가 있으면 사용할 수 있습니다.
2. 없으면 `cdp-direct` fallback으로 진행할 수 있어야 합니다.
3. 특정 driver가 필수라는 가정을 두지 않습니다.
4. CDP-direct 실행 레시피는 `references/drivers/cdp-direct.md`를 참조합니다.

## Driver-agnostic techniques

- 입력 주입(React 등): controlled input은 `el.value` 직접 대입이 안 먹을 수 있으므로 native value setter로 값을 넣고 `input`/`change` 이벤트를 dispatch합니다.
- 상호작용 실행 경계: 클릭 / 활성화 / submit 계열 상호작용은 driver가 제공하는 trusted 입력 surface로 실행합니다. 예를 들어 CDP에선 `Input.dispatchMouseEvent`, 필요할 때 `Input.dispatchKeyEvent`를 사용합니다. 이 규칙은 위 입력 주입 bullet과 별개로, 텍스트 입력 자체보다 클릭·제출 계열 상호작용에 적용합니다.
- 클릭 금지 경로: `element.click()`, `dispatchEvent(new MouseEvent(...))`, `form.submit()` 같은 합성 상호작용은 실행용 수단으로 사용하지 않습니다. 이런 경로는 실제 사용자 클릭에는 없는 submit / side-effect / write를 날조할 수 있으므로 허용하지 않습니다.
- `Runtime.evaluate` 역할: `Runtime.evaluate`는 computed style / bounding rect / 상태 read / 좌표 계산 같은 관측·계산 전용입니다. 클릭 / 활성화 / submit 계열 상호작용 실행용 surface로 사용하지 않습니다.
- 클릭: 실제 클릭은 press + release 좌표 클릭 같은 trusted 마우스 입력으로 수행합니다.
- native dialog 선준비: trusted 클릭 / 활성화 / submit 직전에 native dialog 대응을 먼저 준비합니다. 대상은 `alert`, `confirm`, `beforeunload`입니다.
- dialog 대응 규칙: native dialog가 뜨면 가능한 한 즉시 `accept` 또는 `dismiss`로 해제합니다. dialog 준비 없이 trusted 클릭부터 보내고 나중에 처리하는 흐름은 피합니다.
- overlay와 native dialog 구분: library overlay / custom modal 존재 여부 판별과 브라우저 native dialog 대응은 별도 경우로 다룹니다. overlay를 닫았다고 native dialog까지 처리된 것으로 간주하지 않습니다.
- 흐름 기대치: native dialog 때문에 `dialog opened` 같은 중간 상태로 장시간 멈춰 있지 않게 합니다. dialog 처리 준비는 클릭 성공 여부 확인보다 먼저 끝나 있어야 합니다.
- 뷰포트 밖 요소: 음수 y 또는 y > viewport height면 좌표 클릭이 무효가 될 수 있으므로 `scrollIntoView({block:'center'})` 후 rect를 다시 구합니다.
- 클릭 가로챔: 클릭이 안 먹으면 `document.elementFromPoint(x,y)`로 위에 겹친 요소(sticky, 캐러셀 등)를 확인합니다.
- 오버레이 종류 구분: 라이브러리 모달(예: Radix Dialog)은 `[role=dialog]`를 가질 수 있지만 커스텀 `div` 오버레이는 없을 수 있으므로 특정 프레임워크를 가정하지 않고 존재 여부로 판별합니다.
- scroll-lock 부작용: `body overflow:hidden`이 스크롤바를 제거하면 중앙정렬 기준폭이 스크롤바 폭만큼 넓어져 콘텐츠가 그 절반만큼 수평 이동할 수 있습니다. 폭 변화가 아니라 위치 시프트로 해석해야 합니다.
- 필수 비교축: 시각 일치 판정 전 아래 3축을 모두 확인합니다.
  - typography: `fontWeight`, `fontSize`, `lineHeight`
  - geometry: `borderRadius`, `height`, `padding`, `justifyContent`
  - color: `backgroundColor`, `color`, `borderColor`, `borderWidth`
- baseline 신뢰도 사다리: baseline 측정은 실제 렌더된 요소를 직접 재는 것을 1순위로 둡니다. class 주입 probe는 fallback으로만 허용합니다.
- probe 구성 규칙: fallback probe를 쓸 때는 `variant` class만 따로 재현하지 말고, 소비처에서 실제로 붙는 전체 `className`을 그대로 사용합니다. `variant + additional utility classes`처럼 override까지 포함된 최종 class 조합을 기준으로 둡니다.
- probe 해석 규칙: class 주입 probe는 inline style, CSS cascade, parent context, consumer override를 완전히 재현하지 못하므로 low-trust 측정으로 표시합니다. probe 결과만으로는 강한 회귀 단정이나 baseline parity 결론을 서두르지 않습니다.
- baseline provenance: baseline의 원본 타입이나 스타일 출처는 commit message, PR title, 라벨 같은 간접 힌트보다 pre-change source와 실제 렌더 근거를 우선합니다. 가능하면 `git show <base>:<file>` 같은 pre-change source와 그 렌더 결과로 baseline을 확인합니다.
- match 판정 게이트: typography / geometry가 맞아도 color 축(`backgroundColor`, `color`, `borderColor`, `borderWidth`)을 확인하기 전에는 `match`, `identical`, `일치` 같은 결론을 내리지 않습니다.
- 측정 기준: “비슷해 보이면 OK”로 끝내지 않고 computed style과 bounding rect를 px/hex/opacity 기준으로 대조합니다. 특히 color 축은 computed value 기준으로 확인하고, background / text / border 중 어느 축을 확인했는지 결과에 남깁니다.
- 결과 보고: 다른 값만 보고하되, color-only regression도 누락하지 않습니다. 최종 보고에는 최소한 `color-axis checked` 여부와 어떤 color 필드가 달랐는지 드러나야 합니다.
- HMR: dev 서버가 Fast Refresh를 지원하면 컴포넌트/모달 상태가 유지될 수 있으므로 고친 뒤 재오픈 없이 재측정할 수 있습니다. 닫혔으면 다시 엽니다.
- Driver: MCP driver(playwright/chrome-devtools 등)가 있으면 사용하고, 없으면 CDP-direct로 폴백합니다. 특정 driver를 필수로 가정하지 않습니다.

## Behavior 판정 규칙

behavior-verify mode뿐 아니라, 어떤 mode에서든 상호작용 결과를 근거로 결론을 내릴 때 적용합니다.

- verdict는 검증 항목 단위로 `pass` / `fail` / `unverifiable`을 사용합니다.
- mutation ground-truth: 저장 / 삭제 / 발송 같은 mutation 발생 판정은 DOM 상태(토스트, 알럿, 모달)만으로 내리지 않습니다. network 요청 관측(method / endpoint)을 필수 증거로 요구합니다.
- 합성 이벤트 증거 불인정: 합성 경로(`element.click()`, `dispatchEvent`, `form.submit()`)로 관측된 동작은 실제 사용자 입력에서는 일어나지 않는 phantom side-effect일 수 있으므로 pass / fail 증거로 인정하지 않습니다. trusted 입력으로 재현된 관측만 증거입니다.
- 관측 3축: UI 상태 전이, network 요청, 응답 후 결과 상태를 구분해 기록합니다. 어느 축을 확인했고 어느 축을 확인하지 못했는지 결과에 남깁니다.

## Mutation 안전

- 테스트 컨텍스트 봉인: mutation을 유발할 수 있는 상호작용은 profile `env.md`의 test mutation context에 명시된 계정 / 데이터 범위 안에서만 실제 실행합니다.
- 컨텍스트 미지정 시 차단: test mutation context가 비어 있으면 mutation 유발 상호작용을 실행하지 않고, 해당 검증 항목을 `unverifiable`(사유: 테스트 컨텍스트 부재)로 보고합니다.
- 비가역 side-effect: 외부 발송(SMS / 메일 / 푸시), 결제, 취소 불가 삭제는 테스트 컨텍스트 안이라도 실제 실행하지 않습니다. mock으로 상태에 도달하거나 사용자 확인을 받습니다.
- gated 상태 도달 mock: 특정 상태에서만 렌더되는 UI는 initScript로 `window.fetch` / `XMLHttpRequest`를 패치해 대상 endpoint 응답을 조작해 도달할 수 있습니다.
  - mock 응답 envelope는 앱이 실제로 파싱하는 구조와 일치시킵니다. 응답 매핑은 앱 소스에서 먼저 확인합니다.
  - mock은 상태 도달용입니다. 판정 대상 mutation 자체를 mock으로 대체해 `pass`를 내리지 않습니다.

## Evidence artifacts

핵심 결론의 근거는 computed evidence지만, 스크린샷 산출물의 생성과 제출은 모든 mode에서 필수입니다.

- 모든 실행은 run 산출물 디렉토리를 만듭니다: `~/.tigerkit/repos/<repo-key>/browser-verify/runs/<run-id>/`
- 판정에 쓰인 화면은 검증 항목 / finding 단위로 스크린샷을 저장합니다. 파일명은 의미 기반으로 짓습니다(`<screen>-<item>-<env>.png` 등).
- 최종 보고에는 run 디렉토리 경로와 스크린샷 파일 목록을 포함해 사용자에게 증거로 제출합니다. 스크린샷 없이 computed 수치만으로 보고를 끝내지 않습니다.
- 일부 MCP screenshot 도구는 저장 경로가 자체 workspace root 목록으로 제한되어 `~/.tigerkit` 절대경로를 거부할 수 있습니다. 이 경우 repo 하위 임시 경로에 저장한 뒤 run 디렉토리로 이동하고, repo tree에 잔재를 남기지 않습니다. cdp-direct는 `Page.captureScreenshot`(base64)로 임의 경로에 저장할 수 있습니다.

## Auth session reuse

2FA(OTP / SSO)가 걸린 환경은 로그인 자동화가 매 실행 뚫을 수 없습니다. "1회 수동 로그인 후 세션 재사용"을 기본 기법으로 안내합니다.

- 격리 프로필 재사용(권장): 브라우저를 repo-scoped 고정 `--user-data-dir`(예: `~/.tigerkit/repos/<repo-key>/browser-verify/browser-profile/`)로 기동합니다. 최초 1회는 사용자가 직접 로그인하고, 이후 실행은 같은 디렉토리를 재사용해 세션 만료 전까지 로그인 절차를 생략합니다.
- storage state export/import: driver가 cookies + localStorage 저장/복원을 지원하면 사용할 수 있습니다.
- 사용자의 실제 브라우저 프로필은 절대 재사용하지 않습니다. 검증 전용 격리 프로필만 사용합니다.
- 세션 프로필 디렉토리는 credential급 민감물로 취급합니다. `~/.tigerkit` 아래에만 두고 tracked repo에 커밋하지 않습니다.
- 세션 만료 신호(profile `login.md`의 expiry_signal)가 관측되면 자동 재시도하지 않고, 사용자에게 수동 로그인 1회를 요청한 뒤 이어갑니다.

## Feedback loop

실행 중 배운 내용은 아래 surface로 되먹임합니다.

- screen-specific knowledge -> `screens/*.md`
- login/context 변화 -> `login.md`, `login.local.md`, `env.md`
- product-agnostic engine lesson -> engine `SKILL.md` 또는 `references/modes/*`
- 동작 검증 중 발견한 판정/안전 lesson -> `references/modes/behavior-verify.md`

원칙: 한 번 겪은 마찰은 다음 실행에서 그대로 반복되지 않게 합니다.
