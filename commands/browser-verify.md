---
description: 번들된 browser-verify 엔진 skill을 `~/.tigerkit` repo profile과 함께 사용하는 direct QA / behavior verification surface입니다.
argument-hint: '"<screen or verify task>" [--mode <env-diff|figma-diff|behavior-verify>] [--print-profile-template]'
---

이 문서는 TigerKit `/tk:browser-verify` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:browser-verify`는 프로비저닝 command가 아니라 direct QA surface입니다. 번들된 browser-verify 엔진 skill 지식을 사용하고, 현재 repo에 대응하는 `~/.tigerkit` repo-scoped profile을 읽어 visual QA / env diff / layout regression / SoT 대비 runtime behavior 검증을 수행합니다.

canonical skill:

```text
skills/browser-verify/SKILL.md
```

```text
browser-verify = bundled engine skill + repo-scoped profile -> run browser verification workflow
```

## Core boundary

- 이 command는 user-global provisioning mode를 만들지 않습니다.
- engine install/update를 수행하지 않습니다.
- current repo에 대응하는 `~/.tigerkit` profile만 읽고, profile이 없을 때만 같은 repo-scoped 경로에 missing profile 파일을 신규 생성합니다.
- `--print-profile-template`가 있으면 write 없이 템플릿과 경로만 출력합니다.
- 기존 profile 파일을 강제로 overwrite하지 않습니다.
- `login.local.md`는 tracked repo 밖 `~/.tigerkit` 아래에 두는 local override입니다.
- **legacy `ui-diff` profile이 남아 있으면 자동 migration도, 조용한 새 profile bootstrap도 하지 않습니다.** migration guide를 출력하고 사용자가 profile을 옮긴 뒤 다시 실행하게 합니다.

## Profile contract

현재 repo에 대응하는 아래 경로를 찾습니다.

```text
~/.tigerkit/repos/<repo-key>/browser-verify/env.md
~/.tigerkit/repos/<repo-key>/browser-verify/login.md
~/.tigerkit/repos/<repo-key>/browser-verify/login.local.md
~/.tigerkit/repos/<repo-key>/browser-verify/screens/README.md
```

`repo-key`는 `scripts/tigerkit_state.py browser-verify-paths` helper가 계산합니다.

legacy detection 경로:

```text
~/.tigerkit/repos/<repo-key>/ui-diff/
```

lookup 순서:

1. `browser-verify` profile이 있으면 그것을 사용합니다.
2. `browser-verify` profile은 없고 legacy `ui-diff` profile이 있으면 migration guide mode로 멈춥니다.
3. 둘 다 없으면 bundled template를 source로 삼아 신규 생성 절차로 들어갑니다.

lookup 파일 순서:

1. `env.md`
2. `login.md`
3. `login.local.md` (있으면 override)
4. `screens/README.md` 및 `screens/*.md`

신규 생성 source:

```text
skills/browser-verify/templates/env.md -> ~/.tigerkit/repos/<repo-key>/browser-verify/env.md
skills/browser-verify/templates/login.md -> ~/.tigerkit/repos/<repo-key>/browser-verify/login.md
skills/browser-verify/templates/login.local.md -> ~/.tigerkit/repos/<repo-key>/browser-verify/login.local.md
skills/browser-verify/templates/screens/README.md -> ~/.tigerkit/repos/<repo-key>/browser-verify/screens/README.md
```

규칙:

- 디렉토리가 없으면 `~/.tigerkit/repos/<repo-key>/browser-verify/`와 `screens/`를 먼저 만듭니다.
- missing 파일만 생성하고 기존 파일은 덮어쓰지 않습니다.
- `--print-profile-template`가 있으면 위 템플릿 내용을 preview만 하고 write는 하지 않습니다.
- 생성 직후에는 env/login/screens에 채워야 할 항목과 다음 실행 순서를 같이 안내합니다.
- legacy `ui-diff` profile 감지 시에는 새 `browser-verify` profile을 자동 생성하지 않습니다.

## Engine source

이 command는 repo의 `skills/browser-verify/` 정본을 engine knowledge source로 사용합니다.

필수 source:

- `skills/browser-verify/SKILL.md`
- `skills/browser-verify/references/modes/env-diff.md`
- `skills/browser-verify/references/modes/figma-diff.md`
- `skills/browser-verify/references/modes/behavior-verify.md`
- `skills/browser-verify/references/drivers/cdp-direct.md`
- `skills/browser-verify/references/screens/README.md`

## Supported modes

- `env-diff`
- `figma-diff`
- `behavior-verify`

명시하지 않으면 task wording과 profile context를 기준으로 적절한 mode를 고릅니다.

## Output contract

- section label은 항상 `🎯 Goal:`처럼 leading emoji를 붙인 `라벨:` 한 줄 뒤 바로 다음 줄에 내용을 둡니다. 라벨 뒤 빈 줄을 두지 않습니다.
- 같은 역할의 label은 가능하면 같은 emoji를 재사용합니다.
- compact는 유지하되 section 사이에는 한 줄 여백을 두어 읽힘을 확보합니다.
- 긴 설명은 가능하면 bullet을 쪼개서 한 줄에 한 뜻만 남깁니다.
- optional section은 비어 있으면 통째로 생략합니다. 의미 보존이 필요한 receipt가 아니면 `NONE`을 출력하지 않습니다.

```text
Browser Verify 준비 완료 | Browser Verify 프로필 생성 완료 | Browser Verify 프로필 템플릿 출력 | Browser Verify migration guide
🧭 Mode: env-diff | figma-diff | behavior-verify
[📁 Profile path:
- <path>]
[🗃️ Legacy profile path:
- <path>]
[📁 Created files:
- <path>]
[✍️ Write result:
- existing profile reused | profile files created | template only | blocked by legacy profile]
[🧭 Migration guide:
- <move legacy ui-diff profile to browser-verify path and rerun>]
🧠 Engine skill:
- skills/browser-verify/SKILL.md
▶️ Next step:
- <run verify / fill env-login-screen values / migrate profile and rerun>
```

## Examples

```text
/tk:browser-verify "QA와 로컬 화면 비교"
/tk:browser-verify "이 모달 레이아웃 회귀 확인"
/tk:browser-verify "figma랑 이 화면 맞는지 봐줘" --mode figma-diff
/tk:browser-verify "이 티켓 기준으로 저장 플로우가 실제로 동작하는지 검증" --mode behavior-verify
```

## Non-goals

- engine provisioning
- user-global profile provisioning
- full install/update workflow
- forced overwrite / merge of profile assets
- legacy profile auto-migration
