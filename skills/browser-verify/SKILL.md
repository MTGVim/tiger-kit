---
name: browser-verify
description: browser-verify 엔진 트리거입니다.
---

# Browser Verify

`/tk:browser-verify`를 위한 번들 engine skill입니다. public command contract와 output shape의 source of truth는 `commands/browser-verify.md`입니다.

## Use when

- 시각 회귀(modal, layout, spacing, color, overlay)를 검증해야 할 때
- SoT 대비 runtime behavior를 직접 확인해야 할 때
- `env-diff`, `figma-diff`, `behavior-verify` 중 한 모드로 QA를 진행할 때

## Engine boundary

- 이 skill은 repo에 번들된 reusable engine knowledge입니다.
- project-specific 값은 tracked repo가 아니라 `~/.tigerkit/repos/<repo-key>/browser-verify/` profile에서 읽습니다.
- legacy `~/.tigerkit/repos/<repo-key>/ui-diff/`가 남아 있으면 자동 migration하지 않고 migration guide로 멈춥니다.
- missing profile만 bootstrap할 수 있고, 기존 profile을 강제로 덮어쓰지 않습니다.
- red-loop-first: fix 판단 전에 실패 재현과 관측 축을 먼저 고정합니다.

## Load these references when needed

- `references/modes/env-diff.md`
- `references/modes/figma-diff.md`
- `references/modes/behavior-verify.md`
- `references/drivers/cdp-direct.md`
- `references/screens/README.md`
- `templates/env.md`
- `templates/login.md`
- `templates/login.local.md`
- `templates/screens/README.md`

## Wrapper rule

상세 절차, profile lookup, artifact path, output contract는 `commands/browser-verify.md`를 그대로 따릅니다. 이 SKILL.md에는 긴 driver/playbook을 다시 복제하지 않습니다.
