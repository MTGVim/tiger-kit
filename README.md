# TigerKit

[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors)

TigerKit(`tiger-kit`, plugin `tk`)은 요구사항 정제, 긴 답변 해독, 요구사항 대비 갭 확인, 실행 task 분해, 세션 정리, 응답 초압축, 그리고 가벼운 저장소 knowledge layer 유지보수를 위한 Claude Code 플러그인입니다.

제공 기능은 slash command 중심입니다. 자연어 trigger가 중요한 기능은 skill로도 제공합니다. `caveman`은 `/tk:caveman` alias도 있고, `write-a-skill`은 장황한 skill creator 대체용 경량 skill입니다. 일부 command는 plugin-packaged agent로 API 확인, review, bounded implementation, UI prototype, visual artifact 분석을 분담할 수 있습니다.

- Workflow
  - `/tk:help` — 권장 loop와 command 선택 기준을 짧게 안내합니다.
  - `/tk:prep` — 외부 요구사항 소스와 대화 맥락을 `requirements.md` 기준 문서로 정리합니다.
  - `/tk:gap` — `requirements.md` 대비 현재 구현, 문서, 테스트의 남은 차이를 확인합니다.
  - `/tk:plan` — `gap.md` 기준으로 구현 전략과 순서를 정리합니다.
  - `/tk:breakdown` — `gap.md` 또는 `plan.md`를 작은 실행 task로 분해합니다.
  - `/tk:do` — 현재 task 1건을 구현하고 검증합니다.
  - `/tk:do-all` — 실행 가능한 task를 끝날 때까지 하나씩 구현합니다.
  - `/tk:close` — 세션 종료 전 남은 gap, task, 검증, cleanup 후보를 정리합니다.
- Utility
  - `/tk:state` — `.tigerkit/{work_id}` 전체 상태를 요약합니다.
  - `/tk:next` — 지금 해야 할 다음 command 또는 다음 task 하나를 추천합니다.
  - `/tk:auto` — `prep` 이후 `gap -> plan -> breakdown -> do-all -> gap` 1사이클을 자율주행합니다.
  - `/tk:mwhat` — 긴 답변이나 애매한 설명을 짧고 실행 가능하게 풀어줍니다.
  - `/tk:grill-me` — `prep`이나 `plan`에서 deep interview가 필요할 때 씁니다.
  - `/tk:caveman` — `caveman` skill alias입니다. 기술 정확도를 유지하며 응답을 초압축합니다.
  - `/tk:prototype` — FE 화면 결정을 브라우저에서 비교 가능한 throwaway UI variants로 검증합니다.
  - `/tk:review` — 구현 직후나 merge 전에 review 맥락을 정리하고 코드 리뷰를 요청합니다.
  - `/tk:review-fix` — 받은 리뷰 피드백을 검증하고 맞는 것만 순서대로 반영합니다.
- Skills
  - `mwhat` — 사용자가 `뭣?`이라고 할 때만 답변 해독을 자동 실행합니다. `/tk:mwhat`은 명시 alias입니다.
  - `caveman` — 자연어 요청으로 응답 초압축 모드를 켭니다. `/tk:caveman`도 같은 alias입니다.
  - `write-a-skill` — 새 skill을 짧고 실용적인 `SKILL.md` 중심으로 작성합니다.
- Agents
  - `tk-api-librarian` — 실제 API, 공식 contract, `mock_api_contract`, `TK-API-*` 확인을 돕습니다.
  - `tk-reviewer` — review, YAGNI, architecture risk, correctness 판단을 돕습니다.
  - `tk-fixer` — 명확히 scope가 잡힌 task 구현을 돕습니다.
  - `tk-designer` — UI/UX, prototype variant, visual polish 작업을 돕습니다.
  - `tk-observer` — screenshot, PDF, diagram 같은 visual artifact를 구조화합니다.
- Maintenance
  - `/tk:reflect` — 현재 세션에서 드러난 반복 패턴, convention, 교정 포인트를 짧게 회고합니다.
  - `/tk:improve` — 저장소의 knowledge layer를 가볍게 점검해 audit finding과 patch proposal을 정리합니다.

이 흐름은 이슈 트래커 티켓, 지식베이스 문서, PRD, 디자인 문서, 사용자가 작성한 브리프, 스크린샷, 코드 참조, 간단한 메모를 모두 입력 자료로 사용할 수 있게 설계되어 있습니다.

## 권장 흐름

권장 loop는 아래입니다.

```text
/tk:prep
/tk:gap
/tk:plan
/tk:breakdown
/tk:do 또는 /tk:do-all
/tk:gap
... 반복
/tk:close
```

가장 자주 쓰는 유틸:

```text
/tk:state   # 지금 상태
/tk:next    # 다음에 할 것 1개 추천
/tk:auto    # gap -> plan -> breakdown -> do-all -> gap 1사이클 자율주행
```

실제 loop는 `prep -> gap -> plan -> breakdown -> do/do-all -> gap -> ... -> close`입니다. `next`는 실행이 아니라 추천용입니다. `do-all` 뒤에는 gap을 한 번만 다시 확인하고, 새 gap이 있으면 다시 `plan`부터 이어갑니다. `다음 추천: ...`은 core workflow command와 상태 조회 command에만 붙이고, `reflect`나 `improve` 같은 maintenance 보고서에는 기본으로 붙이지 않습니다.

`/tk:mwhat`, `/tk:grill-me`, `/tk:caveman`, `/tk:prototype`, `/tk:review`, `/tk:review-fix`는 core workflow 밖에서 쓰는 독립 유틸리티입니다. `mwhat`, `caveman`, `write-a-skill`은 자연어 요청에도 켜질 수 있는 skill이며, `mwhat`의 자연어 trigger는 `뭣?`으로만 제한합니다. `grill-me`는 주로 `prep`이나 `plan`에서 모호성을 줄일 때 보조로 사용합니다.

`/tk:reflect`와 `/tk:improve`는 maintenance 유틸리티입니다. 둘 다 자동으로 대규모 수정을 적용하지 않으며, 사용자가 명시적으로 승인한 patch만 선택적으로 반영합니다.

## 설치

### Marketplace로 설치

Claude Code 안에서 이 저장소를 marketplace로 추가한 뒤 `tk` 플러그인을 설치합니다.

```text
/plugin marketplace add MTGVim/tiger-kit
/plugin install tk@tiger-kit
/reload-plugins
```

> 이 저장소에는 marketplace 등록에 필요한 `.claude-plugin/marketplace.json`과 플러그인 매니페스트 `.claude-plugin/plugin.json`이 포함되어 있습니다.

### 로컬 플러그인 디렉터리로 사용

이 저장소를 Claude Code 플러그인 디렉터리로 직접 지정할 수 있습니다.

```bash
claude --plugin-dir ./tiger-kit
```

## 산출물 구조

작업 산출물은 기본적으로 현재 프로젝트의 `.tigerkit/{work_id}/` 아래에 저장합니다. 입력 자료는 `.tigerkit/{work_id}/inputs/`에 둘 수 있고, 주요 산출물은 `requirements.md`, `requirements.meta.json`, `gap.md`, `gap.meta.json`, `plan.md`, `tasks.md`, `close.md`입니다. 자세한 파일 구조는 `docs/artifact-layout.md`를 참고하세요.

`main`, `master`, `develop` 같은 기반 브랜치에서 작업을 시작했다면, 실제 변경 전에 작업 브랜치나 작업 ID를 정하는 것을 권장합니다.

command 문서, `skills/*/SKILL.md`, `agents/*.md`는 재사용 가능한 작업 흐름 지침입니다. agent는 command를 대체하지 않고 command 내부의 탐색, 검토, 구현, 시각 분석을 보조합니다. 실행 중 만들어지는 산출물은 프로젝트 로컬 작업 노트로 취급합니다. commit, push, PR 생성은 제안할 수 있지만 사용자 승인 없이 실행하지 않습니다.

## 검증

이 저장소에는 package manager 기반 build/test/lint 설정이 없습니다. TigerKit을 수정한 뒤에는 다음 검증을 우선 실행합니다.

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
git diff --check
python3 -m json.tool evals/evals.json >/dev/null
```

`evals/evals.json`은 자동 실행 테스트가 아니라 명령/스킬 기대 동작을 적어둔 fixture입니다. 현재 저장소에는 이 fixture를 LLM에 넣어 pass/fail 판정하는 runner나 harness가 없습니다. 따라서 변경 시에는 JSON 문법 검증과 fixture 내용 수동 검토만 수행합니다.

## 설계 원칙

- 입력 자료 수집은 특정 도구나 문서 형식에 묶이지 않게 유지합니다.
- 모든 입력은 분석 전에 요구사항 기준 스냅샷으로 정리합니다.
- 갭 분석은 요구사항 기준과 현재 상태의 차이를 찾는 데 집중합니다.
- 실행계획과 task 분해는 구현을 자동 시작하지 않고 사용자가 다음 행동을 고르게 돕습니다.
- 분석 이후의 구현, 보류, 추가 확인은 사용자가 결과를 보고 선택합니다.

## Inspired by

TigerKit은 아래 작업 흐름과 skill/repo에서 아이디어를 참고해 목적에 맞게 축약하거나 재구성했습니다.

- [`claude-reflect`](https://github.com/dontriskit/claude-reflect) — `reflect`
- [OACP `self-improve`](https://github.com/OpenAgentic/agentic-coding-protocol/tree/main/commands/self-improve) — `improve`
- [Matt Pocock `prototype`](https://github.com/mattpocock/skills/tree/main/skills/engineering/prototype) — `prototype`
- [Matt Pocock `tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd) — `do`, `do-all`
- [Matt Pocock `write-a-skill`](https://github.com/mattpocock/skills/blob/main/skills/productivity/write-a-skill/SKILL.md) — `write-a-skill`
- [Q00 `ouroboros`](https://github.com/Q00/ouroboros) — `prep -> gap -> plan -> breakdown -> do/do-all -> gap` loop와 ambiguity reduction 관점
- [superpowers `executing-plans`](https://github.com/pcvelz/superpowers/blob/main/skills/executing-plans/SKILL.md) — execute 단계의 task 처리 기준
- [superpowers `requesting-code-review`](https://github.com/pcvelz/superpowers/tree/main/skills/requesting-code-review) — `review`
- [superpowers `receiving-code-review`](https://github.com/pcvelz/superpowers/blob/main/skills/receiving-code-review) — `review-fix`

외부 워크플로를 그대로 복제하지 않고, TigerKit 목적에 맞게 command-first 구조와 `.tigerkit/` 산출물 loop에 맞춰 조정했습니다. 또한 어떤 patch든 사용자 승인 없이 자동 적용하지 않고, 사용자가 고른 변경만 반영합니다.

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

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind are welcome.
