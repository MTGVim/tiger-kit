---
description: 번들된 ui-diff 엔진 skill을 현재 repo의 `.claude/ui-diff/` profile과 함께 사용하는 direct QA surface입니다.
argument-hint: '"<screen or diff task>" [--mode <env-diff|figma-diff>] [--print-profile-template]'
---

이 문서는 TigerKit `/tk:ui-diff` command contract를 정의합니다.

사용자에게는 한글로 답합니다. 코드, path, URL, identifier, command, YAML/JSON field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:ui-diff`는 프로비저닝 command가 아니라 direct QA surface입니다. 번들된 ui-diff 엔진 skill 지식을 사용하고, 현재 repo의 `.claude/ui-diff/` profile을 읽어 visual QA / env diff / layout regression 검증을 수행합니다.

```text
ui-diff = bundled engine skill + current repo profile -> run visual QA workflow
```

## Core boundary

- 이 command는 user-level / repo-internal provisioning mode를 만들지 않습니다.
- engine install/update를 수행하지 않습니다.
- current repo의 profile만 읽습니다.
- profile이 없으면 필요한 파일 경로를 안내하고 중단합니다.
- `login.local.md`는 gitignored local override입니다.

## Profile contract

현재 repo에서 아래 경로를 찾습니다.

```text
<root>/.claude/ui-diff/env.md
<root>/.claude/ui-diff/login.md
<root>/.claude/ui-diff/login.local.md
<root>/.claude/ui-diff/screens/README.md
```

lookup 순서:

1. `env.md`
2. `login.md`
3. `login.local.md` (있으면 override)
4. `screens/README.md` 및 `screens/*.md`

없으면 profile missing으로 중단하고 필요한 파일 경로를 출력합니다.

## Engine source

이 command는 repo의 `templates/ui-diff/` 정본을 engine knowledge source로 사용합니다.

필수 source:

- `templates/ui-diff/SKILL.md`
- `templates/ui-diff/references/modes/env-diff.md`
- `templates/ui-diff/references/modes/figma-diff.md`
- `templates/ui-diff/references/screens/README.md`

## Supported modes

- `env-diff`
- `figma-diff`

명시하지 않으면 task wording과 profile context를 기준으로 적절한 mode를 고릅니다.

## Output contract

```text
UI Diff 준비 완료 | UI Diff 중단
Mode: env-diff | figma-diff
Profile path:
- <path or NONE>
Engine skill:
- templates/ui-diff/SKILL.md
다음 행동:
- <run diff / inspect missing profile / provide selectors>
```

## Examples

```text
/tk:ui-diff "QA와 로컬 화면 비교"
/tk:ui-diff "이 모달 레이아웃 회귀 확인"
/tk:ui-diff "figma랑 이 화면 맞는지 봐줘" --mode figma-diff
```

## Non-goals

- engine provisioning
- user-level profile provisioning
- repo-internal install/update workflow
- forced overwrite / merge of profile assets
