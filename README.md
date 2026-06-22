# TigerKit

<p align="center">
  <img src="assets/tigerkit-cute-cover.png" width="960" alt="TigerKit cute gap/reflect cover">
</p>

<p align="center">
  <em>먼저 gap을 보고, 계약을 만들고, 명시적으로 실행하고, 끝나면 reflect로 남긴다.</em>
</p>

TigerKit(`tk`, plugin namespace `/tk:*`)은 Claude Code용 경량 plugin입니다.
SoT(Source of Truth)가 있으면 `/tk:gap`으로 현재 구현과의 차이를 먼저 확인하고, 명시적 task는 `/tk:loop-spec`으로 `tigerkit.loop-spec/v2` 실행 계약을 생성할 수 있습니다. 사용자가 직접 `/tk:execute <spec>`를 호출하면 bounded execution dispatcher가 spec과 현재 context, hard-boundary proof를 검증한 뒤 실행 receipt를 남깁니다. 의미 있는 작업이 끝나면 `/tk:reflect`로 재사용 가능한 learning을 preview-first로 정리합니다.

```text
Check the gap. Write the spec. Execute only by request. Keep the learning.
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

설치 후 Claude Code를 다시 시작하고 `/tk:gap`, `/tk:reflect`, `/tk:loop-spec`, `/tk:execute` 명령을 사용합니다.

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없으면 먼저 SoT 제공을 제안합니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.
- `/tk:loop-spec`은 source를 수정하지 않고 LoopSpec v2 계약만 생성하거나 검증합니다.
- `/tk:execute`는 사용자만 명시적으로 호출할 수 있는 write boundary입니다.
- Stable execute support set은 `support/execute-support-matrix.json`이 소유합니다. 현재 package는 hook_gate architecture를 preview로 포함하며, public stable execution은 packaged CAP-01-CAP-10 hard-boundary proof가 있는 environment에서만 활성화됩니다.
- 의미 있는 작업이 끝나면 `/tk:reflect`로 재사용 가능한 learning을 정리합니다.
- `/tk:reflect` 기본값은 preview-only이며, `--apply=true`도 eligible `repo-local` 후보만 `<git-root>/CLAUDE.local.md`에 쓸 수 있습니다.

## Command Surface

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:gap` | SoT와 Current Implementation의 차이를 한 번 확인하고 missing, mismatch, overbuilt, ambiguous를 정리합니다. | optional external generated report |
| `/tk:loop-spec` | 명시적 task와 현재 worktree capability를 읽기 전용으로 분석해 `tigerkit.loop-spec/v2`를 생성하거나 검증합니다. | worktree-scoped generated spec |
| `/tk:execute` | LoopSpec v2 하나를 user-only bounded execution dispatcher로 검증하고 execution receipt를 저장합니다. | immutable execution receipt |
| `/tk:reflect` | 세션 결과와 execution receipt에서 재사용 가능한 learning을 canonical target으로 분류합니다. 기본값은 preview-only입니다. | promotion candidates |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:loop-spec "결제 모달 scroll 복구 버그 수정"
/tk:loop-spec validate <spec-id-or-path>
/tk:execute <spec-id-or-path>
/tk:reflect --target repo --apply=false
/tk:reflect --target repo-local --apply=true
```

## Execute boundary

`/tk:execute`는 stable public execution을 성공으로 표시하기 전에 아래를 요구합니다.

- `tigerkit.loop-spec/v2` schema와 execution-ready validation
- `readiness: complete`
- `execution.executorRecommendation: fast | reasoning`
- stale/legacy/blocked/invalid spec rejection
- current environment identity와 runtime binding helper capture
- `support/execute-support-matrix.json`의 matching public entry
- packaged capability proof `tigerkit.capability-proof/execute-write-boundary-v1`
- proof `tests[]`가 `CAP-01`부터 `CAP-10`까지 exact order로 모두 `passed`
- boundary component path set과 proof component digest set의 exact match
- dispatcher postflight verifier 재실행과 immutable receipt 저장

현재 repository package는 hook_gate boundary runtime component를 포함합니다.

```text
hooks/hooks.json
hooks/execute-write-boundary.py
```

proof가 없거나 preview environment만 있으면 `/tk:execute`는 `hard_enforcement_unavailable`로 reject하고 가능한 경우 `~/.tigerkit/.../executions/<execution-id>.yaml` receipt를 저장합니다.

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

Active generated state는 project repository 밖 `~/.tigerkit/` 아래의 file-only state입니다. `/tk:gap` report, `/tk:loop-spec` spec, `/tk:execute` receipt는 `~/.tigerkit/repos/<repo-key>/branches/<scope-key>/...` 아래에 둡니다. `.claude/tigerkit/`는 legacy/migration context로만 남기며 `.claude/` 전체를 ignore하지 않습니다.

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
