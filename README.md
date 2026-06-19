# TigerKit

TigerKit(`tk`, plugin namespace `/tk:*`)은 sealed GAP → Launch → Review → Reflect 흐름과 steering replacement `/tk:next`, continuation handoff, 조건부 meta-feedback으로 AI-induced source loss를 줄입니다. GitHub PR/commit은 선택 capability이며, plain workspace에서도 workflow 작성·실행·회고가 가능해야 합니다.

공개 실행 표면은 Claude Code plugin command입니다. 별도 repo-local skill 파일 없이 `commands/*.md`와 `.claude-plugin/plugin.json`이 `/tk:*` contract를 소유합니다.

현재 release scope는 Claude Code command 기능 안정화입니다. Hermes Agent, Codex CLI, `npx skills` 기반 command-skill adapter는 사전조사 대상이지만 현재 release artifact로 제공하지 않습니다. 특히 Hermes에서 `/gap`, `/launch`, `/review`, `/reflect` 같은 native slash command를 제공하려면 `.hermes/plugins/<name>/plugin.yaml`과 `ctx.register_command()` 기반 plugin adapter가 별도로 필요하며, 이 PR 범위에는 포함하지 않습니다.

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

설치 후 Claude Code를 다시 시작하고 `/tk:gap`, `/tk:launch`, `/tk:review`, `/tk:reflect`, `/tk:next`, `/tk:handoff`, `/tk:meta-feedback` 명령을 사용합니다. 현재 command surface에서 source intake와 spec normalization은 `/tk:gap`이 담당하므로 `/tk:spec`은 공개 command surface에서 제거되었습니다.

## Command Surface

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:gap` | 즉석 지시, 브레인스토밍, 회의 메모, URL, ticket, 기존 branch-local Spec Patch를 source material로 intake하고, source를 ground하고 ambiguity를 attack한 뒤 launch 가능한 sealed workflow를 만들거나 `GAP_BLOCKED`로 중단합니다. | branch-local |
| `/tk:gap --review` | v7 Contract-based Gap Review compatibility mode로 조치 필요 항목과 확인 필요 항목를 `report.md`와 `run.json`에 남깁니다. | branch-local |
| `/tk:launch` | sealed workflow만 `tk-runner` subagent로 실행하고 검증합니다. workflow의 `review_policy`가 `required`이면 read-only `tk-reviewer` 수용 검토까지 실행하고, execution·verification·acceptance review·overall status를 분리한 receipt를 남깁니다. | branch-local execution |
| `/tk:review` | frozen goal/spec 또는 sealed workflow 대비 launch 결과와 현재 구현을 검증해 `REVIEW_PASS`, `REVIEW_PARTIAL`, `REVIEW_FAIL`, `REVIEW_BLOCKED` verdict를 남깁니다. standalone review는 current diff, branch diff, PR, file/artifact, claim, latest launch receipt를 target으로 pin할 수 있습니다. | branch-local review |
| `/tk:reflect` | gap+launch trace와 branch-local working memory에서 repo에 영구 보존할 insight만 rubric으로 선별하고 durable target에 반영합니다. TigerKit-level friction이 있을 때만 proposal-only meta-feedback을 남기고, 그렇지 않으면 `Meta-feedback: NONE`을 출력합니다. | durable insight |
| `/tk:next` | 현재 TigerKit 상태와 workspace/repo context를 읽고 다음 안전 실행 항목 하나를 실제로 이어서 시도하며 receipt를 남깁니다. | branch/workspace-local continuation execution |
| `/tk:handoff` | 다음 세션이나 다음 작업자가 이어받을 continuation 문서와 pending follow-up queue를 작성합니다. | continuation |
| `/tk:meta-feedback` | 세션 내역에서 TigerKit-level command/skill workflow friction만 일반화해 추출합니다. | generalized feedback |

## Core Model

```text
gap = source intake + source grounding + ambiguity attack + sealed launch workflow 생성
launch = sealed workflow 실행 + verification + abort/reflect receipt
review = frozen goal/spec 대비 구현 결과 검증 + Pass/Partial/Fail/Blocked verdict
reflect = gap+launch+review trace와 branch-local working memory에서 repo에 영구 보존할 insight만 추출/반영
next = continuation state를 읽고 다음 안전 작업을 실제로 이어서 시도
handoff = 다음 세션/작업자용 continuation context
meta-feedback = TigerKit-level workflow/tooling friction만 조건부 일반화
```

`gap`, `review`, canonical `handoff` 산출물은 `.claude/tigerkit/branches/<branch-key>/` 아래의 branch-local generated working memory입니다. 기존 branch-local Spec Patch가 있으면 `/tk:gap`의 source material로 읽을 수 있지만, 현재 command surface는 `/tk:spec` command를 노출하지 않습니다. `/tk:handoff`는 경로 미지정 resume을 위해 `.claude/tigerkit/global-index.json`에 최신 handoff pointer도 기록합니다. repo-wide durable knowledge가 아닙니다.


`/tk:review`는 review/correction loop를 TigerKit 용어로 흡수한 post-launch 검증 command입니다. 별도 브랜드나 별도 command surface를 추가하지 않고, frozen target 대비 닫힌 gap, 남은 gap, drift/risk, 다음 loop 결정을 기록합니다.

`/tk:gap` 기본 실행은 git/GitHub가 없는 workspace에서도 `GAP_READY` 또는 `GAP_BLOCKED`로 끝날 수 있습니다. `GAP_READY`에는 task별 `assumed_preconditions`, 봉인 전 `readonly_preflight` 결과, sealed `tigerkit-launch-workflow`가 포함되어야 하고, `GAP_BLOCKED`에는 unresolved decision/conflict/missing source/preflight failure 때문에 workflow block을 포함하지 않습니다. v7 review behavior는 `/tk:gap --review`에서 유지합니다.

GitHub remote, git branch, commit 가능 여부는 launch preflight capability로 기록하며 prerequisite가 아닙니다. commit/PR이 불가능해도 workflow가 commit/PR을 요구하지 않으면 `/tk:launch`는 `Commit: skipped_not_git_repo` 같은 명시 skip reason으로 성공할 수 있습니다. Git worktree context는 Superpowers-style `SessionStart` read-only hook이 세션 시작 시 한 번 점검하고, base/source worktree에만 있는 root-level Markdown과 `.claude/` 후보를 `additionalContext`로 proposal-only 제안합니다. `/tk:gap`은 이 context를 source grounding에 포함하고, `/tk:launch`와 `/tk:next`는 command마다 같은 후보를 다시 묻지 않습니다. 사용자가 거절한 동일 candidate signature는 `.claude/tigerkit/local/session-start/worktree-context-declines.json`로 suppress합니다.

`/tk:next`는 primary execution pipeline을 대체하지 않는 steering replacement continuation command입니다. 현재 TigerKit artifact와 workspace 상태를 읽어 handoff/trace의 다음 안전 작업을 실제로 이어서 시도하고, commit/push/PR/merge/release/deploy/GitHub issue write 같은 외부 side effect는 사용자 승인 또는 artifact상의 명시 approval 없이는 수행하지 않습니다.

`reflect`는 durable insight를 Frequency, Cost, Risk, Stability, Coverage rubric으로 평가하고 `apply=true`일 때 `CLAUDE.md` 또는 `.claude/rules/**/*.md`에 직접 반영합니다. 반영할 durable insight가 없으면 파일을 수정하지 않는 것도 정상 성공입니다. reflect 결과는 `Repo Insight`, `사용자 루틴 스킬 검토`, `Meta-feedback`를 분리하며, TigerKit-level issue가 없으면 `Meta-feedback: NONE`을 출력합니다. `--no-meta-feedback` 또는 `--meta-feedback=false`가 있으면 meta-feedback 판단 자체를 생략할 수 있습니다.

## Operational Docs

- [Usage](.tigerkit/docs/usage.md)
- [Artifact layout](.tigerkit/docs/artifact-layout.md)
- [출력 계약](.tigerkit/docs/output-contract.md)
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
