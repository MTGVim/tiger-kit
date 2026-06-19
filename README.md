# TigerKit

![TigerKit Slim cover](assets/tigerkit-slim-cover.png)

TigerKit(`tk`, plugin namespace `/tk:*`)은 AI-induced source loss를 줄이기 위한 작은 Claude Code 메타 스킬 키트입니다. 기존 sealed GAP → Launch → Review 흐름은 종료되었고, TigerKit Slim은 `gap`, `grill`, `afk`, `reflect`, `config` 중심으로 동작합니다.

공개 실행 표면은 Claude Code plugin command입니다. 별도 repo-local skill 파일 없이 `commands/*.md`와 `.claude-plugin/plugin.json`이 `/tk:*` contract를 소유합니다.

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

설치 후 Claude Code를 다시 시작하고 `/tk:gap`, `/tk:grill`, `/tk:afk`, `/tk:reflect`, `/tk:config`, `/tk:setup` 명령을 사용합니다.

## TigerKit Slim

```text
Core:
  tk:gap
  tk:afk
  tk:reflect

Optional active:
  tk:grill

Management:
  tk:config
  tk:setup -> tk:config init
```

`/tk:grill`은 이번 release의 active manifest에 포함된 optional micro command입니다. 설계, 계획, 변경안, reviewer 판단을 작은 질문 렌즈로 압박 검증합니다.

## Command Surface

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:gap` | SoT와 Current Implementation을 한 번 비교해 누락, 불일치, 과잉 구현, 모호성을 보고합니다. Evidence, impact, priority, suggested fix를 포함하며 workflow를 만들지 않습니다. | optional branch/workspace-local report |
| `/tk:grill` | 설계, 계획, 변경안, reviewer 판단을 작은 질문 렌즈로 압박 검증합니다. 코드와 문서에서 답할 수 있는 질문은 먼저 닫고, owner decision이 필요한 질문만 남깁니다. | optional branch/workspace-local report |
| `/tk:afk` | 현재 세션에서 사용자에게 물어볼 중대하거나 불확실한 decision point를 temporary Patron에게 위임합니다. Driver는 계속 작업하고 Patron decision은 ledger에 기록합니다. | branch/workspace-local decision ledger |
| `/tk:reflect` | 세션 내용, 실제 변경 결과, 사용자 피드백, Patron ledger에서 재사용 가능한 learning을 추출합니다. Repo shared `CLAUDE.md`는 suggest-only이고 repo auto-write는 `CLAUDE.local.md`로 제한합니다. | user/repo improvement candidates |
| `/tk:config` | TigerKit setup, AFK default, Patron catalog, Vowline opt-in, recommended tools를 단계형 wizard와 subcommands로 관리합니다. | user-level config |
| `/tk:setup` | `/tk:config init` alias입니다. | user-level config |

## Core Model

```text
gap = SoT ↔ Current one-shot gap analysis
grill = proposal/review context ↔ evidence ↔ sharp questions
afk = current-session decision delegation with temporary Patrons
reflect = session learning and improvement extraction
config = setup, preferences, Vowline, Patrons, recommended tools
```

`/tk:gap`은 더 이상 sealed workflow를 생성하지 않습니다. `/tk:launch`, workflow freezing, mandatory advisor/runner, autopilot, `/tk:next`, `/tk:handoff`, `/tk:meta-feedback` command surface는 launch-era 실험으로 deprecated 처리되었습니다.

## `/tk:gap`

`/tk:gap`은 Product Spec, Design Spec, Engineering Constraint, QA note, API docs, issue, screenshot/export, pasted notes, legacy branch-local Spec Patch 같은 SoT 후보와 current implementation을 비교합니다.

기본 출력:

```md
## Gap Summary

| Area | SoT | Current | Gap | Impact | Priority |
|---|---|---|---|---|---|

## Findings

### 1. ...
- SoT:
- Current:
- Evidence:
- Impact:
- Priority:
- Suggested fix:

## Recommended Next Steps
1. ...
```

분류:

- `missing`: SoT 요구가 Current에 없음.
- `mismatch`: SoT와 Current가 다름.
- `overbuilt`: SoT 밖 구현이 위험이나 유지보수 비용을 만듦.
- `ambiguous`: source conflict, missing owner decision, inaccessible source, producer evidence 부족.

## `/tk:afk`와 Patrons

AFK는 background async 작업이 아닙니다. 현재 세션의 decision point를 Patron에게 위임하는 mode입니다.

기본 Patrons:

| Patron | 용도 |
|---|---|
| reviewer | code quality / merge readiness |
| tester | verification / test scope |
| security | security boundary / permissions |
| webperf | web runtime performance |
| steward | repo convention / reuse |
| simplifier | simplification / scope reduction |
| cartographer | visual explanation / structure map |

AFK guardrails:

- 배포, 삭제, 비용 발생, 권한 변경, secrets 변경, destructive action은 사용자 승인 없이는 금지합니다.
- repo shared `CLAUDE.md`는 직접 수정하지 않습니다.
- Security Patron이 Critical/High risk를 판단하면 사용자 승인 gate로 되돌립니다.

## `/tk:reflect`

Reflect는 세션 learning을 안전한 target에만 반영합니다.

| Target | Policy |
|---|---|
| repo `CLAUDE.local.md` | auto apply |
| repo `CLAUDE.md` | suggest only |
| user `PROFILE.md` | auto apply |
| user `CLAUDE.md` | auto apply |
| user skills | auto apply |
| Patron profiles | auto apply candidates or improvements |

Reflect는 `candidate`, `confirmed`, `session-local`, `deprecated` 상태를 구분하고 중복 규칙은 병합합니다.

## `/tk:config`

지원 명령:

```text
/tk:config
/tk:config init
/tk:config show
/tk:config vowline on
/tk:config vowline off
/tk:config patrons list
/tk:config patrons install <id>
/tk:config patrons enable <id>
/tk:config patrons disable <id>
/tk:config afk default on
/tk:config afk default off
/tk:config afk status
/tk:config reflect show
/tk:config reset
/tk:setup
```

First-use config suggestion은 non-blocking입니다. 기본 선택은 “이번엔 그냥 진행”입니다.

Vowline은 필수 의존성이 아니며 `/tk:config`에서 opt-in으로 연결합니다. TigerKit은 Vowline skill을 자동 설치하지 않습니다.

`vowline` skill이 아직 없으면 `/tk:config vowline on`은 bridge를 확정하지 않고 설치 안내만 제공합니다.

```text
Install Vowline for yourself by following:
https://github.com/chojondocho/vowline/blob/main/INSTALL.md

Verify installation, then run `/tk:config vowline on` again.
```

Recommended tools는 optional이며 기본 설치하지 않습니다. `Context Mode`, `RTK`, `Superpowers`는 `/tk:config`의 기타 추천 도구 메뉴에서 사용자가 선택한 경우에만 안내합니다. 설치 방법이 upstream GitHub 문서에 있으면 그 링크를 먼저 보여주고, 설치 후 verify installation을 요청합니다.

## Operational Docs

- [Usage](.tigerkit/docs/usage.md)
- [Artifact layout](.tigerkit/docs/artifact-layout.md)
- [출력 계약](.tigerkit/docs/output-contract.md)
- [Launch migration](docs/migration-from-launch.md)
- [Patron catalog](docs/patron-catalog.md)
- [Patron lifecycle](docs/patron-lifecycle.md)
- [Reflect file policy](docs/reflect-file-policy.md)
- [AFK default](docs/afk-default.md)
- [Vowline integration](docs/vowline-integration.md)
- [Recommended tools](docs/recommended-tools.md)

## Generated State

`.claude/tigerkit/`은 branch/workspace-local generated state이므로 git ignore 대상입니다. `.claude/` 전체를 ignore하지 않습니다.

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
