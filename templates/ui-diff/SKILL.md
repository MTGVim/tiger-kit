---
name: ui-diff
description: >
  UI Diff. QA 배포본과 로컬, 또는 design spec과 로컬을 비교할 때
  computed style과 bounding rect를 evidence-first로 읽고 시각 회귀를 검증합니다.
  제품별 URL, 로그인, 화면 카탈로그는 현재 repo의 `.claude/ui-diff/` profile에서 로드합니다.
---

# UI Diff

시각 회귀(모달, 레이아웃, spacing, color, overlay)를 눈대중이 아니라 computed style / bounding rect 중심으로 검증합니다.

## Profile lookup (먼저)

엔진은 제품 특이값을 hard-code하지 않습니다. 실행 시 아래 순서로 profile을 찾습니다.

1. `<root>/.claude/ui-diff/`
2. 없으면 profile missing으로 중단하고 필요한 파일 경로를 안내합니다.

이 엔진은 현재 repo profile만 읽고, provisioning/install flow를 직접 수행하지 않습니다.

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

## Feedback loop

실행 중 배운 내용은 아래 surface로 되먹임합니다.

- screen-specific knowledge -> `screens/*.md`
- login/context 변화 -> `login.md`, `login.local.md`, `env.md`
- product-agnostic engine lesson -> engine `SKILL.md` 또는 `references/modes/*`

원칙: 한 번 겪은 마찰은 다음 실행에서 그대로 반복되지 않게 합니다.
