# TigerKit

TigerKit(`tiger-kit`, plugin `tk`)은 branch-local source-of-truth reference indexing, reproducible gap recording, session reflection, and operational handoff를 통해 AI-induced source loss를 줄이기 위한 Claude Code 플러그인입니다.

TigerKit은 요구사항을 대신 재작성하거나 실행 대기열을 관리하지 않습니다. 필요한 운영 규칙과 상세 계약은 아래 문서를 기준으로 봅니다.

## Command Surface

| Command | 역할 |
| --- | --- |
| `/tk:prep` | source-of-truth reference와 직접 사용자 인터뷰를 branch-local requirements index에 기록 |
| `/tk:gap` | branch-local indexed SOT reference와 clean HEAD baseline을 비교해 evidence-based gap 기록 |
| `/tk:checkpoint` | ambiguity, user decision, unverifiable source, conflict, self-resolvable item을 분리하는 Decision Gate |
| `/tk:review` | TigerKit 준수룰 위반을 적대적으로 검토하는 artifact-free compliance review |
| `/tk:reflect` | session을 재구성해 branch-local reflection을 기록하고 durable artifact 격상 후보 제안 |
| `/tk:handoff-write` | 다음 모델/세션을 위한 branch-local continuation contract 작성 |
| `/tk:handoff-read` | handoff와 artifact map을 읽고 현재 repo 상태와 stale risk 확인 |

## Operational Docs

- [Usage](.tigerkit/docs/usage.md)
- [Artifact layout](.tigerkit/docs/artifact-layout.md)
- [Output contract](.tigerkit/docs/output-contract.md)

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
