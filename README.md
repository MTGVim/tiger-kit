# TigerKit

<p align="center">
  <img src="assets/tigerkit-cute-cover.png" width="960" alt="TigerKit cute gap/reflect cover">
</p>

<p align="center">
  <em>먼저 gap을 보고, 끝나면 reflect로 남긴다.</em>
</p>

TigerKit(`tk`, plugin namespace `/tk:*`)은 Claude Code용 경량 plugin입니다.
SoT(Source of Truth)가 있으면 `/tk:gap`으로 현재 구현과의 차이를 먼저 확인하고, 의미 있는 작업이 끝나면 `/tk:reflect`로 재사용 가능한 learning을 정리합니다. `gap`은 evidence-first로 읽고, source conflict나 근거 부족은 `ambiguous`로 남깁니다.

```text
Check the gap first. Keep the learning.
```

공개 실행 표면은 `/tk:gap`, `/tk:reflect` 두 명령입니다. TigerKit은 workflow runner, subagent orchestrator, setup wizard를 제공하지 않으며, `commands/*.md`와 `.claude-plugin/plugin.json`이 `/tk:*` contract를 소유합니다.

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

## Command Surface

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:gap` | SoT와 Current Implementation의 차이를 한 번 확인하고 missing, mismatch, overbuilt, ambiguous를 정리합니다. evidence-first로 읽고 source conflict는 `ambiguous`로 남깁니다. | optional branch/workspace-local report |
| `/tk:reflect` | 세션 결과와 사용자 피드백에서 재사용 가능한 learning을 분류하고 hook / hookify, command, agent proposal을 분리해 제안합니다. 파일을 쓰면 changed path를 출력합니다. | user/repo improvement candidates |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:reflect --dry-run
```

## What TigerKit does not do

TigerKit은 아래를 active surface로 제공하지 않습니다.

- `grill`
- `afk`
- `setup`
- launch / review / next / handoff workflow
- mandatory runner or autopilot
- Patron / subagent delegation

## Operational Docs

- [Usage](.tigerkit/docs/usage.md)
- [출력 계약](.tigerkit/docs/output-contract.md)
- [Storage boundary](.tigerkit/docs/storage-boundary.md)
- [Reflect file policy](docs/reflect-file-policy.md)
- [Reflect promotion helper guide](.tigerkit/docs/reflect-promotion-helpers.md) (optional)
- [RFC: gap/reflect core simplification](docs/rfcs/2026-06-gap-reflect-core-slim.md)

## Generated State

`.claude/tigerkit/`은 branch/workspace-local generated state이므로 git ignore 대상입니다. 현재 문서화된 active generated layout은 gap report와 branch pointer만 포함합니다. `.claude/` 전체를 ignore하지 않습니다.

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
