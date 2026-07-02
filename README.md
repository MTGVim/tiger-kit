# TigerKit

<p align="center">
  <img src="assets/tigerkit-cute-cover.png" width="960" alt="TigerKit cute gap/route/reflect/forge cover">
</p>

<p align="center">
  <em>먼저 gap을 보고, route를 고르고, 끝나면 reflect로 남기고, 필요하면 forge로 굳힌다.</em>
</p>

TigerKit(`tk`, plugin namespace `/tk:*`)은 Claude Code용 경량 plugin입니다.
SoT(Source of Truth)가 있으면 `/tk:gap`으로 현재 구현과의 차이를 먼저 확인합니다. 다음 구현 route가 애매하면 `/tk:route`로 direct, subagent-driven, goal-driven 중 어떤 방식이 맞는지 얇게 정리합니다. 의미 있는 작업이 끝나면 `/tk:reflect`로 재사용 가능한 learning을 분류하고 repo-local guidance에 반영할 수 있습니다. skill로 굳힐 가치가 있으면 `/tk:forge`가 그 후보를 실제 artifact로 생성합니다. UI diff 엔진은 번들 skill로 유지하고, `/tk:ui-diff`는 현재 repo의 `.claude/ui-diff/` profile을 읽는 direct surface입니다.

```text
Check the gap. Pick the route. Keep the learning. Forge the durable skill when needed.
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

설치 후 Claude Code를 다시 시작하고 `/tk:gap`, `/tk:route`, `/tk:reflect`, `/tk:forge`, `/tk:ui-diff` 명령을 사용합니다.

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없으면 먼저 SoT 제공을 제안합니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.
- `/tk:route`는 source를 수정하지 않고 direct, subagent-driven, goal-driven 같은 구현 경로를 비교합니다.
- `/tk:reflect`는 교훈을 canonical target으로 분류합니다. `repo-local`에 한해서는 기본 apply(opt-out)로 `CLAUDE.local.md`에 반영할 수 있습니다.
- `/tk:forge`는 `reflect`가 제안한 후보를 실제 artifact로 생성합니다. 1차 범위는 `skill only`입니다.
- `/tk:ui-diff`는 번들된 ui-diff 엔진 skill을 현재 repo의 `.claude/ui-diff/` profile과 함께 사용하는 direct QA surface입니다.

## Command Surface

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:gap` | SoT와 Current Implementation의 차이를 한 번 확인하고 missing, mismatch, overbuilt, ambiguous를 정리합니다. | optional external generated report |
| `/tk:route` | 지금 이 task를 direct, subagent-driven, goal-driven 중 어떤 구현 route로 가져갈지 얇게 비교하고 첫 스텝을 정리합니다. | no persisted artifact by default |
| `/tk:reflect` | 세션 결과와 사용자 피드백에서 재사용 가능한 learning을 canonical target으로 분류하고, repo-local guidance는 기본 apply(opt-out)로 반영할 수 있습니다. | machine-readable reflect ledger + compact summary |
| `/tk:forge` | `reflect`가 제안한 durable candidate를 실제 artifact로 생성합니다. 1차 범위는 `skill only`입니다. | user-level skill write + compact summary |
| `/tk:ui-diff` | 번들된 ui-diff 엔진 skill을 현재 repo의 `.claude/ui-diff/` profile과 함께 사용하는 direct QA surface입니다. | direct QA summary |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:route "결제 모달 scroll 복구 버그 수정"
/tk:reflect --target repo-local
/tk:reflect --target repo-local --apply=false
/tk:forge R3
/tk:forge --desc "이 CDP 검증 루틴을 skill로 굳혀줘"
/tk:ui-diff
/tk:ui-diff "QA와 로컬 화면 비교"
```

## Reflect write boundary

`/tk:reflect`가 파일을 쓸 수 있는 유일한 직접 대상은 eligibility를 통과한 `<git-root>/CLAUDE.local.md`입니다.

- repo shared `CLAUDE.md`: suggest-only
- user-global guidance: suggest-only
- skill: suggest-only from reflect, source generation is forge-owned
- hook: suggest-only
- command: suggest-only
- agent: suggest-only
- discard: no write

`PROFILE.md`, `automation`, `hookify`는 promotion target 이름이 아닙니다. Claude Code auto memory는 TigerKit이 쓰거나, mirror하거나, backup하지 않습니다.

## Forge scope

`/tk:forge`는 1차에서 `skill only`를 실제 생성합니다.

- same-session + same-ledger `candidate_id`만 읽습니다.
- 이름은 제안할 수 있지만 생성 전 사용자 확정이 필요합니다.
- `hook|command|agent`는 아직 reflect 제안 target으로만 남고, forge가 실제 생성하지 않습니다.

## UI Diff surface

`/tk:ui-diff`는 프로비저닝 command가 아니라 direct QA surface입니다.

- engine은 repo에 번들된 `templates/ui-diff/` 기준 지식을 사용합니다.
- profile은 현재 repo의 `<root>/.claude/ui-diff/`만 읽습니다.
- profile이 없으면 필요한 파일 경로를 안내하고 중단합니다.
- `login.local.md`는 gitignored local override입니다.

## Operational Docs

- [Usage](.tigerkit/docs/usage.md)
- [Output Contract](.tigerkit/docs/output-contract.md)
- [Storage boundary](.tigerkit/docs/storage-boundary.md)
- [Reflect file policy](docs/reflect-file-policy.md)
- [Reflect promotion helper guide](.tigerkit/docs/reflect-promotion-helpers.md)

## Generated State

Active generated state는 project repository 밖 `~/.tigerkit/` 아래의 file-only state입니다.

- `/tk:gap` report:
  - `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/...`
- `/tk:reflect` ledger:
  - `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml`
  - `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml`
- `/tk:route`는 기본적으로 persisted artifact를 만들지 않습니다.
- `/tk:ui-diff`는 별도 provisioning artifact를 만들지 않습니다.

`.claude/tigerkit/`는 legacy/migration context로만 남기며 `.claude/` 전체를 ignore하지 않습니다.

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
