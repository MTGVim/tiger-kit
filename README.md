# TigerKit

<p align="center">
  <img src="assets/tigerkit-cute-cover.png" width="960" alt="TigerKit cute gap/reflect cover">
</p>

<p align="center">
  <em>먼저 gap을 보고, 끝나면 reflect로 남긴다.</em>
</p>

TigerKit(`tk`, plugin namespace `/tk:*`)은 Claude Code용 경량 plugin입니다.
SoT(Source of Truth)가 있으면 `/tk:gap`으로 현재 구현과의 차이를 먼저 확인하고, 의미 있는 작업이 끝나면 `/tk:reflect`로 재사용 가능한 learning을 preview-first로 정리합니다. `gap`은 evidence-first로 읽고, source conflict나 근거 부족은 `ambiguous`로 남깁니다.

```text
Check the gap first. Keep the learning.
```

공개 실행 표면은 `/tk:gap`, `/tk:reflect` 두 명령입니다. Core `tk` plugin은 hook-free이며 workflow runner, subagent orchestrator, setup wizard를 제공하지 않습니다. `commands/*.md`와 `.claude-plugin/plugin.json`이 `/tk:*` contract를 소유합니다.

## Installation

Claude Code에서 TigerKit marketplace를 등록한 뒤 `tk` plugin을 설치합니다.

```bash
claude plugin marketplace add MTGVim/tiger-kit
claude plugin install tk@tiger-kit --scope user
```

설치 여부와 사용 가능한 명령을 확인합니다.

```bash
claude plugin list --available --json
claude plugin details tk
```

프로젝트 단위로만 설치하려면 설치 명령의 scope를 `project`로 바꿉니다.

```bash
claude plugin install tk@tiger-kit --scope project
```

설치 후 Claude Code를 다시 시작하고 `/tk:gap`, `/tk:reflect` 명령을 사용합니다.

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없으면 먼저 SoT 제공을 제안합니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.
- 의미 있는 작업이 끝나면 `/tk:reflect`로 재사용 가능한 learning을 정리합니다.
- `/tk:reflect` 기본값은 preview-only이며, `--apply=true`도 eligible `repo-local` 후보만 `<git-root>/CLAUDE.local.md`에 쓸 수 있습니다.

## Command Surface

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:gap` | SoT와 Current Implementation의 차이를 한 번 확인하고 missing, mismatch, overbuilt, ambiguous를 정리합니다. evidence-first로 읽고 source conflict는 `ambiguous`로 남깁니다. | optional external generated report |
| `/tk:reflect` | 세션 결과와 사용자 피드백에서 재사용 가능한 learning을 canonical target(`repo-local`, `repo-shared`, `user-global`, `skill`, `hook`, `command`, `agent`, `discard`)으로 분류합니다. 기본값은 preview-only입니다. | promotion candidates |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:reflect --target repo --apply=false
/tk:reflect --target repo-local --apply=true
```

## Reflect write boundary

`/tk:reflect --apply=true`가 파일을 쓸 수 있는 유일한 대상은 eligibility를 통과한 `<git-root>/CLAUDE.local.md`입니다.

- repo shared `CLAUDE.md`: suggest-only
- user-global guidance: suggest-only
- skill: suggest-only
- hook: suggest-only
- command: suggest-only
- agent: suggest-only
- discard: no write

`PROFILE.md`, `automation`, `hookify`는 promotion target 이름이 아닙니다. Claude Code auto memory는 TigerKit이 쓰거나, mirror하거나, backup하지 않습니다.

## What TigerKit does not do

TigerKit은 아래를 active surface로 제공하지 않습니다.

- `grill`
- `afk`
- `setup`
- launch / review / next / handoff workflow
- mandatory runner or autopilot
- Patron / subagent delegation
- active `SessionStart` hook
- hook settings, command source, agent source 자동 생성

## Operational Docs

- [Usage](.tigerkit/docs/usage.md)
- [Output Contract](.tigerkit/docs/output-contract.md)
- [Storage boundary](.tigerkit/docs/storage-boundary.md)
- [Reflect file policy](docs/reflect-file-policy.md)
- [Reflect promotion helper guide](.tigerkit/docs/reflect-promotion-helpers.md)

## Generated State

Active generated state는 project repository 밖 `~/.tigerkit/` 아래의 file-only state입니다. `/tk:gap` report와 branch pointer는 `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/...` 아래에 둡니다. Core `tk` plugin은 active `SessionStart` hook을 제공하지 않으며, 기존 SessionStart decline marker는 legacy/inactive state로만 보존되고 core command/runtime이 읽거나 쓰지 않습니다. `.claude/tigerkit/`는 legacy/migration context로만 남기며 `.claude/` 전체를 ignore하지 않습니다.

## Contributors

Thanks goes to these wonderful people:

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MTGVim"><img src="https://avatars.githubusercontent.com/u/6271133?v=4?s=100" width="100px;" alt="Taekwon Yoo"/><br /><sub><b>Taekwon Yoo</b></sub></a><br /><a href="https://github.com/MTGVim/tiger-kit/commits?author=MTGVim" title="Code">💻</a> <a href="https://github.com/MTGVim/tiger-kit/commits?author=MTGVim" title="Documentation">📖</a> <a href="#ideas-MTGVim" title="Ideas, Planning, & Feedback">🤔</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org/) specification. Contributions of any kind are welcome.
