# TigerKit

TigerKit(`tk`, plugin namespace `/tk:*`)은 sealed GAP → Launch → Reflect 흐름과 continuation handoff, generalized meta-feedback으로 AI-induced source loss를 줄입니다.

공개 실행 표면은 Claude Code plugin command입니다. 별도 repo-local skill 파일 없이 `commands/*.md`와 `.claude-plugin/plugin.json`이 `/tk:*` contract를 소유합니다.

v8 MVP scope는 Claude Code command 기능 안정화입니다. Hermes Agent, Codex CLI, `npx skills` 기반 command-skill adapter는 사전조사 대상이지만 현재 release artifact로 제공하지 않습니다. 특히 Hermes에서 `/gap`, `/launch`, `/reflect` 같은 native slash command를 제공하려면 `.hermes/plugins/<name>/plugin.yaml`과 `ctx.register_command()` 기반 plugin adapter가 별도로 필요하며, 이 PR 범위에는 포함하지 않습니다.

해당 workflow를 명시한 natural language request는 대응하는 `/tk:*` command contract로 처리합니다.

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

설치 후 Claude Code를 다시 시작하고 `/tk:spec`, `/tk:gap`, `/tk:launch`, `/tk:reflect`, `/tk:handoff`, `/tk:meta-feedback` 명령을 사용합니다.

## Command Surface

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:spec` | 즉석 지시, 브레인스토밍, 회의 메모를 source material로 저장하되 authority와 분리합니다. | branch-local |
| `/tk:gap` | source를 ground하고 ambiguity를 attack한 뒤 launch 가능한 sealed workflow를 만들거나 `GAP_BLOCKED`로 중단합니다. | branch-local |
| `/tk:gap --review` | v7 Contract-based Gap Review compatibility mode로 Actionable Finding과 Clarification Needed를 `report.md`와 `run.json`에 남깁니다. | branch-local |
| `/tk:launch` | sealed workflow만 실행하고 verification, abort receipt, reflect trace를 남깁니다. | branch-local execution |
| `/tk:reflect` | gap+launch trace와 branch-local working memory에서 repo에 영구 보존할 insight만 rubric으로 선별하고 durable target에 반영한 뒤 기본적으로 meta-feedback을 함께 제출합니다. | durable insight |
| `/tk:handoff` | 다음 세션이나 다음 작업자가 이어받을 continuation 문서와 pending follow-up queue를 작성합니다. | continuation |
| `/tk:meta-feedback` | 세션 내역에서 TigerKit command/skill 개선안을 일반화해 추출합니다. | generalized feedback |

## Core Model

```text
spec = 현재 브랜치 전용 요건 패치 생성
gap = source grounding + ambiguity attack + sealed launch workflow 생성
launch = sealed workflow 실행 + verification + abort/reflect receipt
reflect = gap+launch trace와 branch-local working memory에서 repo에 영구 보존할 insight만 추출/반영
handoff = 다음 세션/작업자용 continuation context
meta-feedback = 세션 내 TigerKit 개선 피드백 일반화
```

`spec`, `gap`, canonical `handoff` 산출물은 `.claude/tigerkit/branches/<branch-key>/` 아래의 branch-local generated working memory입니다. `/tk:handoff`는 경로 미지정 resume을 위해 `.claude/tigerkit/global-index.json`에 최신 handoff pointer도 기록합니다. repo-wide durable knowledge가 아닙니다.

`/tk:gap` 기본 실행은 `GAP_READY` 또는 `GAP_BLOCKED`로 끝납니다. `GAP_READY`에는 sealed `tigerkit-launch-workflow`가 포함되어야 하고, `GAP_BLOCKED`에는 unresolved decision/conflict/missing source 때문에 workflow block을 포함하지 않습니다. v7 review behavior는 `/tk:gap --review`에서 유지합니다.

`reflect`는 durable insight를 Frequency, Cost, Risk, Stability, Coverage rubric으로 평가하고 `apply=true`일 때 `CLAUDE.md` 또는 `.claude/rules/**/*.md`에 직접 반영합니다. 반영할 durable insight가 없으면 파일을 수정하지 않는 것도 정상 성공입니다. reflect 처리 직후 `/tk:meta-feedback`을 proposal-only로 제출하며, `--no-meta-feedback` 또는 `--meta-feedback=false`로 생략할 수 있습니다.

## Operational Docs

- [Usage](.tigerkit/docs/usage.md)
- [Artifact layout](.tigerkit/docs/artifact-layout.md)
- [Output contract](.tigerkit/docs/output-contract.md)
- [Gap baseline registry](.tigerkit/docs/gap-baselines.json)

## Generated State

`.claude/tigerkit/`은 branch-local generated state이므로 git ignore 대상입니다. `.claude/` 전체를 ignore하지 않습니다.

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
