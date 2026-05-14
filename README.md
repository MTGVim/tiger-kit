# TigerKit

![TigerKit](assets/tigerkit-cover.png)

[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors)

TigerKit(`tiger-kit`, plugin `tk`)은 AI-induced source loss를 줄이기 위한 작은 Claude Code 플러그인입니다.

```text
source-of-truth references
→ reproducible code baseline comparison
→ session reflection
→ derived repo knowledge
```

TigerKit은 요구사항을 대신 쓰거나, 실행 대기열을 관리하거나, LLM의 절차 기억을 source of truth로 만들지 않습니다.

## Command Surface

| Command | 역할 |
| --- | --- |
| `/tk:prep` | source-of-truth reference와 사용자 인터뷰 원문을 `.tigerkit/requirements.md`에 인덱싱 |
| `/tk:gap` | indexed SOT reference와 reproducible code baseline을 비교해 `.tigerkit/gap.md`에 evidence-based gap 기록 |
| `/tk:reflect` | session-wide reflection으로 `.tigerkit/reflect.md`를 갱신하고 `DESIGN.md`/`reuse-map.md` 업데이트 제안 또는 적용 |

## Command Order

```mermaid
graph TD
    A[Start] --> B[/tk:prep]
    B --> C[.tigerkit/requirements.md]
    C --> D[/tk:gap]
    D --> E[.tigerkit/gap.md]
    E --> F[/tk:reflect]
    F --> G[.tigerkit/reflect.md]
    F --> H[DESIGN.md]
    F --> I[reuse-map.md]
```

권장 순서:

```text
/tk:prep
/tk:gap
/tk:reflect
```

## Mental Model

- `/tk:prep` = source index, not requirement rewrite
- `/tk:gap` = SOT reference vs commit/code comparison
- `/tk:reflect` = session-wide reconstruction and repo knowledge maintenance

## Artifact Layout

```text
.tigerkit/
  requirements.md
  gap.md
  reflect.md

DESIGN.md
reuse-map.md
```

| Artifact | 역할 |
| --- | --- |
| `.tigerkit/requirements.md` | source-of-truth reference index. 외부 source는 reference만 저장하고, 현재 session 사용자 인터뷰만 raw text로 보존 |
| `.tigerkit/gap.md` | specific SOT reference와 specific code baseline 사이 evidence-based comparison 기록 |
| `.tigerkit/reflect.md` | session-wide reflection. durable learning과 one-off correction 분리 |
| `DESIGN.md` | derived repo-level design knowledge. 외부 SOT 대체 금지 |
| `reuse-map.md` | 기존 component/hook/util/pattern 재사용 지도. inspect한 code만 기록 |

## Core Policy

TigerKit의 목표는 source loss 방지입니다.

source loss 예:

- 중요한 wording을 요약으로 잃음
- 외부 요구사항을 local pseudo-requirement로 재작성
- 별개 source를 하나의 synthetic requirement로 병합
- interpretation을 fact처럼 저장
- uncertainty를 숨김
- missing behavior를 추측
- stale summary 사용
- derived docs를 너무 일찍 업데이트
- evidence를 work item으로 바꿈

대신 아래를 따릅니다.

```text
store reference, not summary
record gap, not work plan
reflect later, not now
ask user, do not guess
```

## requirements.md

`requirements.md`는 source of truth가 아닙니다. source of truth 위치를 가리키는 index입니다.

외부 source는 reference만 저장합니다.

- URL
- file path
- ticket link
- Figma link
- PRD link
- issue link
- API docs link
- source code path
- commit hash

직접 사용자 인터뷰 내용만 local text로 저장할 수 있습니다. raw text와 derived interpretation을 분리합니다.

## gap.md

`gap.md`가 TigerKit의 중심입니다.

각 gap은 아래 비교를 기록합니다.

```text
specific SOT reference
vs
specific code baseline
```

working tree가 clean하지 않으면 gap 기록을 시작하지 않습니다. 먼저 commit하거나 변경을 정리해 reproducible baseline을 만듭니다.

각 gap은 evidence record입니다.

- compared SOT
- compared code baseline
- inspected files
- evidence
- finding
- interpretation, if any
- resolution
- required resolution

## reflect.md

`reflect.md`는 저장된 진행 상태 기반이 아닙니다. session 전체를 재구성합니다.

사용 대상:

- repeated failure patterns
- durable learnings
- one-off corrections
- proposed updates to `DESIGN.md`
- proposed updates to `reuse-map.md`

one-off correction은 future work에 영향을 줘야 한다는 evidence가 있을 때만 durable rule로 승격합니다.

## DESIGN.md / reuse-map.md

`DESIGN.md`와 `reuse-map.md`는 derived repo-level knowledge입니다. 외부 SOT를 대체하지 않습니다.

`DESIGN.md`에는 architecture, boundaries, data flow, UI/API conventions, stable constraints, non-goals, repo-specific decisions를 담을 수 있습니다.

`reuse-map.md`에는 reusable components, hooks, utilities, API clients, form/validation/UI/test patterns, deprecated patterns를 구체 path와 함께 담을 수 있습니다.

inspect하지 않은 capability, prop, behavior는 기록하지 않습니다.

## 검증

이 저장소에는 package manager 기반 build/test/lint 설정이 없습니다. TigerKit을 수정한 뒤에는 다음 검증을 우선 실행합니다.

```bash
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .
python3 -m json.tool evals/evals.json >/dev/null
git diff --check
```

`evals/evals.json`은 자동 실행 테스트가 아니라 명령 기대 동작 fixture입니다. 현재 저장소에는 이 fixture를 LLM에 넣어 pass/fail 판정하는 runner나 harness가 없습니다.

## Inspired by

TigerKit은 아래 project에서 아이디어를 참고해 source-loss prevention 목적에 맞게 축약했습니다.

- [`claude-reflect`](https://github.com/dontriskit/claude-reflect)
- [OACP `self-improve`](https://github.com/OpenAgentic/agentic-coding-protocol/tree/main/commands/self-improve)
- [Q00 `ouroboros`](https://github.com/Q00/ouroboros)

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
