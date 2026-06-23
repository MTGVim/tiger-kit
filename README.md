# TigerKit

<p align="center">
  <img src="assets/tigerkit-cute-cover.png" width="960" alt="TigerKit cute gap/reflect cover">
</p>

<p align="center">
  <em>먼저 gap을 보고, route를 고르고, 끝나면 reflect로 남긴다.</em>
</p>

TigerKit(`tk`, plugin namespace `/tk:*`)은 Claude Code용 경량 plugin입니다.
SoT(Source of Truth)가 있으면 `/tk:gap`으로 현재 구현과의 차이를 먼저 확인합니다. 다음 구현 route가 애매하면 `/tk:route`로 direct, subagent-driven, goal-driven 중 어떤 방식이 맞는지 얇게 정리합니다. 의미 있는 작업이 끝나면 `/tk:reflect`로 재사용 가능한 learning을 preview-first로 정리합니다.

```text
Check the gap. Pick the route. Keep the learning.
```

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

설치 후 Claude Code를 다시 시작하고 `/tk:gap`, `/tk:route`, `/tk:reflect` 명령을 사용합니다.

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없으면 먼저 SoT 제공을 제안합니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.
- `/tk:route`는 source를 수정하지 않고 direct, subagent-driven, goal-driven 같은 구현 경로를 비교합니다.
- 의미 있는 작업이 끝나면 `/tk:reflect`로 재사용 가능한 learning을 정리합니다.
- `/tk:reflect` 기본값은 preview-only이며, `--apply=true`도 eligible `repo-local` 후보만 `<git-root>/CLAUDE.local.md`에 쓸 수 있습니다.

## Command Surface

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:gap` | SoT와 Current Implementation의 차이를 한 번 확인하고 missing, mismatch, overbuilt, ambiguous를 정리합니다. | optional external generated report |
| `/tk:route` | 지금 이 task를 direct, subagent-driven, goal-driven 중 어떤 구현 route로 가져갈지 얇게 비교하고 첫 스텝을 정리합니다. | no persisted artifact by default |
| `/tk:reflect` | 세션 결과와 사용자 피드백에서 재사용 가능한 learning을 canonical target으로 분류합니다. 기본값은 preview-only입니다. | promotion candidates |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:route "결제 모달 scroll 복구 버그 수정"
/tk:route "이 작업을 subagent-driven으로 넘길지 /goal로 풀지 정리해줘"
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

## Operational Docs

- [Usage](.tigerkit/docs/usage.md)
- [Output Contract](.tigerkit/docs/output-contract.md)
- [Storage boundary](.tigerkit/docs/storage-boundary.md)
- [Reflect file policy](docs/reflect-file-policy.md)
- [Reflect promotion helper guide](.tigerkit/docs/reflect-promotion-helpers.md)

## Generated State

Active generated state는 project repository 밖 `~/.tigerkit/` 아래의 file-only state입니다. `/tk:gap` report는 `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/...` 아래에 둘 수 있고, `/tk:route`와 `/tk:reflect`는 기본적으로 persisted artifact를 만들지 않습니다. `.claude/tigerkit/`는 legacy/migration context로만 남기며 `.claude/` 전체를 ignore하지 않습니다.

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
