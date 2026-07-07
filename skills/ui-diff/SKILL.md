---
name: ui-diff
description: computed style과 bounding rect 중심으로 visual regression을 검증합니다. `~/.tigerkit` repo profile을 읽습니다.
---

# UI Diff

시각 회귀(모달, 레이아웃, spacing, color, overlay)를 눈대중이 아니라 computed style / bounding rect 중심으로 검증합니다.

## Profile lookup

제품 특이값은 hard-code하지 않습니다. 실행 시 아래 순서로 profile을 찾습니다.

1. `~/.tigerkit/repos/<repo-key>/ui-diff/`
2. 없으면 bundled template(`skills/ui-diff/templates/`)를 source로 삼아 현재 repo에 대응하는 `~/.tigerkit/repos/<repo-key>/ui-diff/` 신규 생성 절차로 들어갑니다.

이 엔진은 user-global provisioning/install flow를 직접 수행하지 않습니다. 다만 현재 repo profile이 비어 있으면 repo-scoped missing 파일만 생성하는 bootstrap은 허용합니다.

## Mode overview

| Mode | Baseline | Target | Status |
|---|---|---|---|
| env-diff | QA/live runtime | local runtime | primary |
| figma-diff | design node/spec | local runtime | secondary |

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

## Feedback loop

실행 중 배운 내용은 아래 surface로 되먹임합니다.

- screen-specific knowledge -> `screens/*.md`
- login/context 변화 -> `login.md`, `login.local.md`, `env.md`
- product-agnostic engine lesson -> engine `SKILL.md` 또는 `references/modes/*`

원칙: 한 번 겪은 마찰은 다음 실행에서 그대로 반복되지 않게 합니다.
