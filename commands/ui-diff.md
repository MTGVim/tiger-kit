---
description: 번들된 ui-diff 엔진 skill을 `~/.tigerkit` repo profile과 함께 사용하는 direct QA surface입니다.
argument-hint: '"<screen or diff task>" [--mode <env-diff|figma-diff>] [--print-profile-template]'
---

이 문서는 TigerKit `/tk:ui-diff` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:ui-diff`는 프로비저닝 command가 아니라 direct QA surface입니다. 번들된 ui-diff 엔진 skill 지식을 사용하고, 현재 repo에 대응하는 `~/.tigerkit` repo-scoped profile을 읽어 visual QA / env diff / layout regression 검증을 수행합니다.

canonical skill:

```text
skills/ui-diff/SKILL.md
```

```text
ui-diff = bundled engine skill + repo-scoped profile -> run visual QA workflow
```

## Core boundary

- 이 command는 user-global provisioning mode를 만들지 않습니다.
- engine install/update를 수행하지 않습니다.
- current repo에 대응하는 `~/.tigerkit` profile만 읽고, 없으면 같은 repo-scoped 경로에 missing profile 파일만 신규 생성합니다.
- `--print-profile-template`가 있으면 write 없이 템플릿과 경로만 출력합니다.
- 기존 profile 파일을 강제로 overwrite하지 않습니다.
- `login.local.md`는 tracked repo 밖 `~/.tigerkit` 아래에 두는 local override입니다.

## Profile contract

현재 repo에 대응하는 아래 경로를 찾습니다.

```text
~/.tigerkit/repos/<repo-key>/ui-diff/env.md
~/.tigerkit/repos/<repo-key>/ui-diff/login.md
~/.tigerkit/repos/<repo-key>/ui-diff/login.local.md
~/.tigerkit/repos/<repo-key>/ui-diff/screens/README.md
```

`repo-key`는 `scripts/tigerkit_state.py ui-diff-paths` helper가 계산합니다.

lookup 순서:

1. `env.md`
2. `login.md`
3. `login.local.md` (있으면 override)
4. `screens/README.md` 및 `screens/*.md`

누락 파일이 있으면 bundled template를 source로 삼아 신규 생성 절차로 들어갑니다.

```text
skills/ui-diff/templates/env.md -> ~/.tigerkit/repos/<repo-key>/ui-diff/env.md
skills/ui-diff/templates/login.md -> ~/.tigerkit/repos/<repo-key>/ui-diff/login.md
skills/ui-diff/templates/login.local.md -> ~/.tigerkit/repos/<repo-key>/ui-diff/login.local.md
skills/ui-diff/templates/screens/README.md -> ~/.tigerkit/repos/<repo-key>/ui-diff/screens/README.md
```

규칙:

- 디렉토리가 없으면 `~/.tigerkit/repos/<repo-key>/ui-diff/`와 `screens/`를 먼저 만듭니다.
- missing 파일만 생성하고 기존 파일은 덮어쓰지 않습니다.
- `--print-profile-template`가 있으면 위 템플릿 내용을 preview만 하고 write는 하지 않습니다.
- 생성 직후에는 env/login/screens에 채워야 할 항목과 다음 실행 순서를 같이 안내합니다.

## Engine source

이 command는 repo의 `skills/ui-diff/` 정본을 engine knowledge source로 사용합니다.

필수 source:

- `skills/ui-diff/SKILL.md`
- `skills/ui-diff/references/modes/env-diff.md`
- `skills/ui-diff/references/modes/figma-diff.md`
- `skills/ui-diff/references/drivers/cdp-direct.md`
- `skills/ui-diff/references/screens/README.md`

## Supported modes

- `env-diff`
- `figma-diff`

명시하지 않으면 task wording과 profile context를 기준으로 적절한 mode를 고릅니다.

## Output contract

- section label은 항상 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
UI Diff 준비 완료 | UI Diff 프로필 생성 완료 | UI Diff 프로필 템플릿 출력
Mode: env-diff | figma-diff
[Profile path:
- <path>]
[Created files:
- <path>]
[Write result:
- existing profile reused | profile files created | template only]
Engine skill:
- skills/ui-diff/SKILL.md
Next step:
- <run diff / fill env-login-screen values / rerun ui-diff>
```

## Examples

```text
/tk:ui-diff "QA와 로컬 화면 비교"
/tk:ui-diff "이 모달 레이아웃 회귀 확인"
/tk:ui-diff "figma랑 이 화면 맞는지 봐줘" --mode figma-diff
```

## Non-goals

- engine provisioning
- user-global profile provisioning
- full install/update workflow
- forced overwrite / merge of profile assets
