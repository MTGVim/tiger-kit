# TigerKit

TigerKit(`tiger-kit`, plugin namespace `/tk:*`) helps reduce AI-induced source loss by comparing basis materials with implementation or PR artifacts, reflecting durable feedback into repo rules, and writing safe handoffs.

해당 workflow를 명시한 natural language request는 대응하는 `/tk:*` command contract로 처리합니다.

## Command Surface

| Command | 역할 |
| --- | --- |
| `/tk:gap` | Compare basis materials with a target artifact and produce gap analysis or PR-ready review comments. |
| `/tk:reflect` | Propose updates to `CLAUDE.md` and `.claude/rules/*` from durable feedback, repeated mistakes, gap findings, or review findings. |
| `/tk:handoff` | Write `.claude/handoffs/current.md` so the next session can continue safely. |

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
