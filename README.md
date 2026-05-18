# TigerKit

![TigerKit](assets/tigerkit-cover.png)

[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors)

TigerKit(`tiger-kit`, plugin `tk`)은 AI-induced source loss를 줄이기 위한 작은 Claude Code 플러그인입니다.

```text
source-of-truth references
→ reproducible code baseline comparison
→ decision gate
→ session reflection
→ operational handoff
→ derived repo knowledge
```

TigerKit은 요구사항을 대신 쓰거나, 실행 대기열을 관리하거나, LLM의 절차 기억을 source of truth로 만들지 않습니다.

## Command Surface

| Command | 역할 |
| --- | --- |
| `/tk:prep` | source-of-truth reference와 직접 사용자 인터뷰를 branch-local requirements index에 기록 |
| `/tk:gap` | branch-local indexed SOT reference와 clean HEAD baseline을 비교해 evidence-based gap 기록, workflow step과 해야 할 일 안내 |
| `/tk:checkpoint` | ambiguity, user decision, unverifiable source, conflict, self-resolvable item을 분리하는 Decision Gate |
| `/tk:reflect` | session을 재구성해 branch-local reflection을 기록하고 durable artifact 격상 후보 제안 |
| `/tk:handoff-write` | 다음 모델/세션을 위한 branch-local continuation contract 작성 |
| `/tk:handoff-read` | handoff와 artifact map을 읽고 현재 repo 상태와 stale risk 확인 |

## Command Flow

```text
/tk:prep           -> .tigerkit/branches/{escaped-branch}/requirements.md
/tk:gap            -> .tigerkit/branches/{escaped-branch}/gap.md
/tk:handoff-write  -> .tigerkit/branches/{escaped-branch}/handoff.md
/tk:handoff-read   -> verified handoff intake in next session
```

조건부 명령:

- `/tk:checkpoint`: high-impact ambiguity, inaccessible SOT, SOT conflict, user decision, external dependency, broad refactor risk가 있을 때 Decision Gate로 사용합니다.
- `/tk:reflect`: project policy나 repeated user preference를 durable하게 남길 필요가 있을 때 사용합니다.

이어받는 세션은 `/tk:handoff-read`로 시작합니다.

## Mental Model

- `/tk:prep` = source index, not requirement rewrite
- `/tk:gap` = SOT reference vs commit/code comparison + workflow status guidance
- `/tk:checkpoint` = decision gate for ambiguity, access, verification, and user decisions
- `/tk:reflect` = session-wide reconstruction and escalation proposal
- `/tk:handoff-write` = continuation contract and artifact map
- `/tk:handoff-read` = verified handoff intake before acting

## Artifact Layout

```text
.tigerkit/
  branches/
    feature__example/
      requirements.md
      gap.md
      reflect.md
      handoff.md

DESIGN.md        # existing-only, not created by TigerKit
reuse-map.md
CLAUDE.md        # optional TigerKit managed section proposal
```

Root-level `.tigerkit/requirements.md`, `.tigerkit/gap.md`, `.tigerkit/reflect.md` are deprecated artifacts. TigerKit commands treat them as migration candidates, not active write targets.

`{escaped-branch}` is collision-safe path encoding of current git branch. ASCII letter, digit, `.`, `_`, `-` stay unchanged; other bytes encode as `~HH` uppercase hex. Example: `feature/foo` → `feature~2Ffoo`, `feature__foo` → `feature__foo`.

| Artifact | 역할 |
| --- | --- |
| `.tigerkit/branches/{escaped-branch}/requirements.md` | source-of-truth reference index. 외부 source는 reference만 저장하고, 현재 session 사용자 인터뷰만 raw text로 보존 |
| `.tigerkit/branches/{escaped-branch}/gap.md` | specific SOT reference와 specific code baseline 사이 evidence-based comparison 기록 |
| `/tk:checkpoint` output | artifact가 아니라 chat Decision Gate. ambiguity, access, verification, user decision, self-resolvable item 분리 |
| `.tigerkit/branches/{escaped-branch}/reflect.md` | session-wide reflection. durable learning과 one-off correction 분리, escalation 후보 기록 |
| `.tigerkit/branches/{escaped-branch}/handoff.md` | 다음 모델/세션을 위한 continuation contract, artifact map, baseline checkpoint |
| `CLAUDE.md` | optional TigerKit managed section. repo workflow guidance 후보는 사용자 승인 후만 반영 |
| `DESIGN.md` | derived repo-level design knowledge. 외부 SOT 대체 금지. 파일이 없으면 생성하지 않으며, 반영할 derived design knowledge가 있을 때만 초기화 필요를 알림 |
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
checkpoint on high-impact ambiguity
reflect only when durable context matters
ask user, do not guess
```

## requirements.md

`requirements.md`는 source of truth가 아닙니다. source of truth 위치를 가리키는 branch-local index입니다.

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

working tree가 clean하지 않으면 gap 기록을 시작하지 않습니다. 먼저 commit하거나 변경을 정리해 reproducible baseline을 만듭니다. Detached HEAD 또는 `main`, `master`, `develop`에서는 branch-local artifact를 기록하지 않고 feature branch 전환을 요청합니다.

각 gap은 evidence record입니다.

- compared SOT
- compared code baseline
- inspected files
- evidence
- finding
- interpretation, if any
- resolution
- required resolution

`/tk:gap`은 severity와 resolvability를 분리합니다. `selfResolvable`, `requiresUserDecision`, `externalDependency`, `notVerifiable`, `needsVerification`, `largeOrRiskyRefactor`, `shouldPauseBeforeFix`, `blocker`, `safeAutoFixReason` 같은 Decision Gate field를 필요할 때 기록합니다.

inaccessible SOT는 내용을 추측하지 않고 `notVerifiable` 또는 `BLOCKED_BY_ACCESS`로 다룹니다. dependent item을 evidence 없이 `Match`로 표시하지 않습니다.

## checkpoint

`/tk:checkpoint`는 artifact를 쓰지 않는 chat Decision Gate입니다.

사용 대상:

- high-impact ambiguity
- inaccessible SOT
- SOT / policy conflict
- user decision required
- assumption before implementation
- backend/API/infrastructure/external dependency
- broad or risky refactor
- code/type/schema/data verification need

출력은 `Blocking Questions`, `User Decisions Needed`, `Assumptions Being Made`, `Not Verifiable Items`, `SOT / Policy Conflicts`, `Self-resolvable Items`, `Items Not Safe to Auto-resolve`, `Continue / Pause Judgment`를 포함합니다.

마지막 status는 아래 중 하나입니다.

```text
CLEAR
PROCEED_WITH_ASSUMPTIONS
PAUSE_FOR_USER_DECISION
BLOCKED_BY_ACCESS
NEED_VERIFICATION
```

`/tk:checkpoint`는 구현, commit, push, PR 생성을 하지 않습니다. 사소하고 SOT가 명확한 low-risk fix마다 사용자에게 묻기 위한 명령도 아닙니다.

## reflect.md

`reflect.md`는 현재 대화 context를 primary source로 사용합니다. artifact와 git evidence는 보조 근거이며, context에 없는 내용은 `확인 불가`로 둡니다. Reflection 후에는 `CLAUDE.md`, `MEMORY.md`, `DESIGN.md`, `reuse-map.md` escalation 후보를 제안하고, 사용자 승인 전에는 durable artifact를 수정하지 않습니다.

사용 대상:

- repeated failure patterns
- durable learnings
- one-off corrections
- proposed updates to `DESIGN.md`
- proposed updates to `reuse-map.md`

one-off correction은 future work에 영향을 줘야 한다는 evidence가 있을 때만 durable rule로 승격합니다.

## DESIGN.md / reuse-map.md

`DESIGN.md`와 `reuse-map.md`는 derived repo-level knowledge입니다. 외부 SOT를 대체하지 않습니다.

`DESIGN.md`에는 architecture, boundaries, data flow, UI/API conventions, stable constraints, non-goals, repo-specific decisions를 담을 수 있습니다. 파일이 없으면 TigerKit이 생성하지 않고, 넣을 내용이 생겼다는 notification만 남깁니다.

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
