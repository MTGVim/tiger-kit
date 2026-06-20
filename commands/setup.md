---
description: TigerKit setup, AFK default, Patrons, Vowline opt-in, 추천 도구를 관리합니다.
argument-hint: "[show|vowline on|vowline off|patrons list|patrons install <id>|patrons enable <id>|patrons disable <id>|afk default on|afk default off|afk status|reflect show|reset]"
---

이 명령은 TigerKit Slim `/tk:setup` contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, repo, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:setup`은 TigerKit setup, preferences, Vowline bridge, Patron catalog, AFK default, reflect policy, optional recommended tools를 관리하는 유일한 active management command입니다.

```text
setup = wizard + config state source of truth + optional bridges
```

## Command surface

지원 명령:

```text
/tk:setup
/tk:setup show
/tk:setup vowline on
/tk:setup vowline off
/tk:setup patrons list
/tk:setup patrons install <id>
/tk:setup patrons enable <id>
/tk:setup patrons disable <id>
/tk:setup afk default on
/tk:setup afk default off
/tk:setup afk status
/tk:setup reflect show
/tk:setup reset
```

`/tk:config`는 active command surface가 아닙니다. 이전 `/tk:config ...` 사용자는 같은 하위 동작을 `/tk:setup ...`으로 실행해야 합니다.

## Config state

Config state가 source of truth입니다.

```text
~/.claude/tigerkit/config.json
```

권장 schema:

```json
{
  "version": 1,
  "afk": { "default": "off" },
  "vowline": { "enabled": false },
  "patrons": {
    "preset": "minimal",
    "enabled": ["reviewer", "tester", "security"],
    "installed": []
  },
  "reflect": {
    "repo_auto_write": ["CLAUDE.local.md"],
    "repo_suggest_only": ["CLAUDE.md"],
    "user_auto_apply": ["PROFILE.md", "CLAUDE.md", "skills"]
  },
  "recommended_tools": { "shown": false }
}
```

## Wizard policy

`/tk:setup`은 config state가 없거나 사용자가 setup을 요청하면 `askUserQuestion` 기반 단계형 wizard로 동작합니다.

단계:

1. AFK default: off 권장.
2. Patron preset: Minimal 권장.
3. Vowline bridge: opt-in.
4. Reflect policy 확인.
5. 기타 추천 도구 메뉴: 사용자가 선택한 경우에만 표시.

First-use setup suggestion:

- config가 없을 때 첫 `tk:*` 사용 시 non-blocking 권유만 보여줍니다.
- 스킬 실행을 막지 않습니다.
- 기본 선택은 “이번엔 그냥 진행”입니다.
- 선택지:
  - 지금 설정
  - 이번엔 그냥 진행
  - 오늘은 묻지 않기
  - 다시 묻지 않기

## AFK default

- `/tk:setup afk default on`: config state를 `on`으로 갱신하고 user `CLAUDE.md` TigerKit bridge 추가/갱신을 제안하거나 승인 후 적용합니다.
- `/tk:setup afk default off`: config state를 `off`로 갱신하고 bridge는 비활성 상태로 둡니다.
- `/tk:setup afk status`: config state와 bridge 상태를 분리해 보여줍니다.

Bridge는 activation aid입니다. config state가 source of truth입니다.

## Vowline integration

Vowline은 필수 의존성이 아닙니다. TigerKit core skill로 fork/reimplement하지 않습니다.

TigerKit은 Vowline을 자동 설치하지 않습니다. `/tk:setup vowline on`은 먼저 `vowline` skill이 이미 사용 가능한지 확인하고, 없으면 enable을 확정하지 않은 채 설치 안내만 제공합니다.

설치 안내 문구:

```text
Vowline skill이 아직 설치되어 있지 않습니다.

Install Vowline for yourself by following:
https://github.com/chojondocho/vowline/blob/main/INSTALL.md

Verify installation, then run `/tk:setup vowline on` again.
```

Opt-in bridge:

```md
<!-- vowline:start -->
Always use the skill `vowline` consistently, including for all sub-agents.
<!-- vowline:end -->
```

TigerKit block과 Vowline block은 독립적으로 관리합니다.

TigerKit managed block:

```md
<!-- tiger-kit:start -->
## TigerKit

TigerKit user-level guidance lives here.
<!-- tiger-kit:end -->
```

## Recommended tools

기타 추천 도구 메뉴에서 선택한 경우에만 보여줍니다. 기본 설치하지 않습니다.

공통 정책:

- TigerKit은 추천 외부 도구를 자동 설치하지 않습니다.
- upstream GitHub 문서에서 설치 방법이 확인되면 그 설치 문서를 안내합니다.
- 설치 방법이 명시되지 않았으면 repo/README 링크만 안내하고 사용자가 upstream 문서를 직접 확인하게 합니다.
- 설치 안내 뒤에는 verify installation 단계를 요구합니다.

| Tool | Repo | Purpose | Integration |
|---|---|---|---|
| Context Mode | mksglu/context-mode | AI coding agent의 context window 사용량을 줄이고 큰 tool output을 sandbox/index 기반으로 다루는 보조 도구 | recommendation-only |
| RTK | rtk-ai/rtk | 터미널 명령 출력 압축/필터링을 통한 컨텍스트 절약 보조 도구 | recommendation-only |
| Superpowers | obra/superpowers, obra/superpowers-marketplace | Claude Code용 추가 skills/workflows 컬렉션 | recommendation-only |

권장 안내 metadata:

```yaml
external_install_guidance:
  vowline:
    install_doc: https://github.com/chojondocho/vowline/blob/main/INSTALL.md
    verify: verify installation, then run `/tk:setup vowline on` again
    integration_level: semi-integrated

recommended_tools:
  context-mode:
    install_doc: https://github.com/mksglu/context-mode/blob/main/README.md
    verify: verify installation before continuing TigerKit recommended-tools setup

  rtk:
    install_doc: https://github.com/rtk-ai/rtk/blob/master/README.md
    verify: verify installation before continuing TigerKit recommended-tools setup

  superpowers:
    install_doc: https://github.com/obra/superpowers/blob/main/README.md
    marketplace_doc: https://github.com/obra/superpowers-marketplace/blob/main/README.md
    verify: verify installation before continuing TigerKit recommended-tools setup
```

설치 전에는 변경 범위와 설치 방식을 설명하고 사용자 승인을 받습니다.

## Reset

`/tk:setup reset`은 config state 제거 또는 초기화를 의미합니다. user `CLAUDE.md` bridge 제거는 별도 확인을 받아야 합니다.
