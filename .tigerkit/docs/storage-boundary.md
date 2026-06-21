# TigerKit storage boundary

이 문서는 TigerKit generated state의 현재 repo-inside layout과 계획된 external-state 방향을 구분한다.

## Core rule

```text
current/legacy repo-inside state = .claude/tigerkit/ branch/workspace-local generated state only
```

`.claude/tigerkit/`는 durable repo guidance, shared team rule, user-global guidance, user skill source의 canonical home이 아니다.

## Planned direction (not active contract)

RFC 방향으로는 TigerKit runtime state를 project repository 밖 `~/.tigerkit/` 아래로 외부화할 수 있다. 다만 현재 저장소에는 해당 runtime write path 구현이 없으므로, 이 문서는 그 external-state sublayout이나 scoping rule을 활성 contract로 정의하지 않는다.

## Current/legacy generated contents

현재 문서화된 repo-inside generated layout은 gap report와 branch pointer만 포함한다. 이 layout은 기존 호환을 위한 current/legacy 상태이며, 향후 external-state 방향은 project repository 밖의 `~/.tigerkit/` 아래에 TigerKit state를 두는 것이다.

```text
.claude/tigerkit/branches/<scope-key>/gap/<GAP-ID>.md
.claude/tigerkit/branches/<scope-key>/gap/current.md
.claude/tigerkit/branches/<scope-key>/branch-state.json
```

역할:

- `/tk:gap` one-shot report archive
- latest gap report pointer
- branch/workspace-local generated index

Reflect는 현재 이 문서에서 active file layout을 갖지 않는다. `/tk:reflect`가 파일을 쓰는 구현을 갖게 되면, 해당 command receipt는 쓴 path를 출력해야 한다.

## Not stored here

`.claude/tigerkit/`에는 아래를 canonical source로 저장하지 않는다.

- repo `CLAUDE.md`
- repo `CLAUDE.local.md`
- repo shared docs 본문
- user `CLAUDE.md`
- user `PROFILE.md`
- user skill source
- hook settings
- command source
- agent source
- source code
- product artifact

## Promotion boundary

`/tk:reflect`는 learning을 분류할 수 있지만, `.claude/tigerkit/`가 promotion target 자체를 소유하지 않는다.

| Target | Canonical owner |
|---|---|
| repo-local guidance | repo `CLAUDE.local.md` |
| shared repo rule candidate | suggest-only diff/proposal |
| user-global guidance | user-level guidance/profile surface |
| user skill candidate | user skill surface outside `.claude/tigerkit/` |
| hook / command / agent candidate | suggest-only proposal |

`.tigerkit/docs/reflect-promotion-helpers.md` 같은 helper docs는 선택형 참고 문서다. Runtime write path, installer, generator, generated state layout을 선언하지 않는다.

## Receipt boundary

Command가 파일을 쓰면 receipt는 changed path를 출력한다. 파일을 쓰지 않으면 `NONE`으로 표시한다.

Receipt가 proposal을 포함해도 아래를 뜻하지 않는다.

- hook installed
- settings updated
- command generated
- agent generated
- user skill generated under `.claude/tigerkit/`
- plugin manifest modified

## Git policy

현재/legacy `.claude/tigerkit/` repo-inside state는 generated state이므로 git ignore 대상이다.

```gitignore
.claude/tigerkit/
```

`.claude/` 전체를 ignore 대상으로 확대하지 않는다. 계획된 `~/.tigerkit/` external state는 project repository 밖에 있으므로 repo `.gitignore` 대상이 아니다.

## Review checklist

`.claude/tigerkit/`에 새 파일/하위트리를 추가하려 할 때 확인한다.

1. generated working state인가?
2. branch/workspace-local인가?
3. canonical durable source는 다른 표면이 소유하는가?
4. 파일을 쓴 command receipt가 changed path를 출력하는가?
5. user-global guidance, shared repo rule, skill source를 복제하지 않는가?

## Bottom line

`.claude/tigerkit/`는 현재/legacy branch/workspace-local generated state 영역이다. Durable guidance와 user skill source의 canonical storage로 확장하지 않는다. 향후 external-state 방향은 repo 밖 `~/.tigerkit/`로 이동하는 것이지만, 이 저장소의 현재 runtime write path는 아직 그 구현을 제공하지 않는다.
