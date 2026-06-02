# TigerKit

TigerKit(`tk`, plugin namespace `/tk:*`) helps reduce AI-induced source loss through a branch-scoped Spec / Gap / Verify / Reflect pipeline.

해당 workflow를 명시한 natural language request는 대응하는 `/tk:*` command contract로 처리합니다.

## Command Surface

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:spec` | 즉석 지시, 브레인스토밍, 회의 메모를 현재 브랜치의 Spec Patch로 저장합니다. | branch-local |
| `/tk:gap` | Product/Design Spec, implementation plan, current implementation을 비교해 JudgeMergerAgent가 확정한 actionable finding만 저장합니다. | branch-local |
| `/tk:verify-before-stop` | 작업 종료 전 최신 spec/gap 상태에 대한 verification evidence를 저장합니다. | branch-local |
| `/tk:reflect` | branch-local working memory에서 repo에 영구 보존할 insight만 추출하고 durable target에 반영합니다. | durable insight |

## Core Model

```text
spec = 현재 브랜치 전용 요건 패치 생성
gap = 현재 브랜치 전용 요건 대비 구현/계획 리뷰
verify-before-stop = 현재 브랜치 전용 종료 전 검증 evidence 저장
reflect = branch-local working memory에서 repo에 영구 보존할 insight만 추출/반영
```

`spec`, `gap`, `verify-before-stop` 산출물은 `.claude/tigerkit/branches/<branch-key>/` 아래의 generated working memory입니다. repo-wide durable knowledge가 아닙니다.

`reflect`만 durable insight를 생성합니다. 기본 durable target은 `.claude/tigerkit-reflections.md`입니다.

## Operational Docs

- [Usage](.tigerkit/docs/usage.md)
- [Artifact layout](.tigerkit/docs/artifact-layout.md)
- [Output contract](.tigerkit/docs/output-contract.md)

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
