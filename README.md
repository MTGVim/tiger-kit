# TigerKit

TigerKit(`tk`, plugin namespace `/tk:*`)은 branch-scoped Spec / Gap / Reflect pipeline과 continuation handoff, generalized meta-feedback으로 AI-induced source loss를 줄입니다.

공개 실행 표면은 Claude Code plugin command입니다. 별도 repo-local skill 파일 없이 `commands/*.md`와 `.claude-plugin/plugin.json`이 `/tk:*` contract를 소유합니다.

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

설치 후 Claude Code를 다시 시작하고 `/tk:spec`, `/tk:gap`, `/tk:reflect`, `/tk:handoff`, `/tk:meta-feedback` 명령을 사용합니다.

## Command Surface

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:spec` | 즉석 지시, 브레인스토밍, 회의 메모를 현재 브랜치의 Spec Patch로 저장합니다. | branch-local |
| `/tk:gap` | Product/Design Spec, implementation plan, current implementation을 비교해 사용자가 바로 고칠 Actionable Finding과 답할 Clarification Needed를 `report.md`와 `run.json`에 남깁니다. | branch-local |
| `/tk:reflect` | branch-local working memory에서 repo에 영구 보존할 insight만 추출하고 durable target에 반영합니다. | durable insight |
| `/tk:handoff` | 다음 세션이나 다음 작업자가 이어받을 continuation 문서를 작성합니다. | continuation |
| `/tk:meta-feedback` | 세션 내역에서 TigerKit command/skill 개선안을 일반화해 추출합니다. | generalized feedback |

## Core Model

```text
spec = 현재 브랜치 전용 요건 패치 생성
gap = 현재 브랜치 전용 요건 대비 구현/계획 리뷰
reflect = branch-local working memory에서 repo에 영구 보존할 insight만 추출/반영
handoff = 다음 세션/작업자용 continuation context
meta-feedback = 세션 내 TigerKit 개선 피드백 일반화
```

`spec`, `gap`, canonical `handoff` 산출물은 `.claude/tigerkit/branches/<branch-key>/` 아래의 branch-local generated working memory입니다. `/tk:handoff`는 경로 미지정 resume을 위해 `.claude/tigerkit/global-index.json`에 최신 handoff pointer도 기록합니다. repo-wide durable knowledge가 아닙니다.

`/tk:gap` 기본 실행은 사용자-facing `report.md`와 `run.json`만 필수로 생성합니다. TigerKit 자체 성능개선이나 regression 검증을 위한 proof artifact는 maintainer-only `--maintainer-proof` 옵션에서만 생성합니다.

`reflect`는 durable insight를 생성하고 `apply=true`일 때 `CLAUDE.md` 또는 `.claude/rules/**/*.md`에 직접 반영합니다.

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
