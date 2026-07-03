---
name: ui-diff
description: computed style과 bounding rect 중심으로 visual regression을 검증합니다. 현재 repo의 `.claude/ui-diff/` profile을 읽습니다.
---

# UI Diff

시각 회귀(모달, 레이아웃, spacing, color, overlay)를 눈대중이 아니라 computed style / bounding rect 중심으로 검증합니다.

## Profile lookup

제품 특이값은 hard-code하지 않습니다. 실행 시 아래 순서로 profile을 찾습니다.

1. `<root>/.claude/ui-diff/`
2. 없으면 profile missing으로 중단하고 필요한 파일 경로를 안내합니다.

이 엔진은 현재 repo profile만 읽고 provisioning/install flow를 직접 수행하지 않습니다.

## Mode overview

| Mode | Baseline | Target | Status |
|---|---|---|---|
| env-diff | QA/live runtime | local runtime | primary |
| figma-diff | design node/spec | local runtime | secondary |

상세는 `references/modes/`를 봅니다.

## Engine / profile split

- engine: repo에 번들된 reusable procedural skill
- profile: 현재 repo의 URL, login, context, screens catalog

엔진은 공용 지식을 제공하고, 프로젝트 특이값은 repo-local profile에만 둡니다.

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
- 클릭: programmatic `element.click()`만으로는 프레임워크 핸들러를 신뢰성 있게 깨우지 못할 수 있으므로 실제 마우스 이벤트(press + release 좌표 클릭)를 우선합니다.
- 뷰포트 밖 요소: 음수 y 또는 y > viewport height면 좌표 클릭이 무효가 될 수 있으므로 `scrollIntoView({block:'center'})` 후 rect를 다시 구합니다.
- 클릭 가로챔: 클릭이 안 먹으면 `document.elementFromPoint(x,y)`로 위에 겹친 요소(sticky, 캐러셀 등)를 확인합니다.
- 오버레이 종류 구분: 라이브러리 모달(예: Radix Dialog)은 `[role=dialog]`를 가질 수 있지만 커스텀 `div` 오버레이는 없을 수 있으므로 특정 프레임워크를 가정하지 않고 존재 여부로 판별합니다.
- scroll-lock 부작용: `body overflow:hidden`이 스크롤바를 제거하면 중앙정렬 기준폭이 스크롤바 폭만큼 넓어져 콘텐츠가 그 절반만큼 수평 이동할 수 있습니다. 폭 변화가 아니라 위치 시프트로 해석해야 합니다.
- 측정 기준: “비슷해 보이면 OK”로 끝내지 않고 computed style과 bounding rect를 px/hex/opacity 기준으로 대조하고, 다른 값만 보고합니다.
- HMR: dev 서버가 Fast Refresh를 지원하면 컴포넌트/모달 상태가 유지될 수 있으므로 고친 뒤 재오픈 없이 재측정할 수 있습니다. 닫혔으면 다시 엽니다.
- Driver: MCP driver(playwright/chrome-devtools 등)가 있으면 사용하고, 없으면 CDP-direct로 폴백합니다. 특정 driver를 필수로 가정하지 않습니다.

## Feedback loop

실행 중 배운 내용은 아래 surface로 되먹임합니다.

- screen-specific knowledge -> `screens/*.md`
- login/context 변화 -> `login.md`, `login.local.md`, `env.md`
- product-agnostic engine lesson -> engine `SKILL.md` 또는 `references/modes/*`

원칙: 한 번 겪은 마찰은 다음 실행에서 그대로 반복되지 않게 합니다.
