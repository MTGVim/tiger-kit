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
| `/tk:review` | TigerKit 준수룰 위반을 적대적으로 검토하는 artifact-free compliance review |
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
- `/tk:review`: TigerKit command/docs/evals/artifact/implementation 변경에서 source-loss, reuse exploration, baseline, Decision Gate, handoff/reflect contract 위반을 검토할 때 사용합니다.
- `/tk:reflect`: project policy나 repeated user preference를 durable하게 남길 필요가 있을 때 사용합니다.

이어받는 세션은 `/tk:handoff-read`로 시작합니다.

## Mental Model

- `/tk:prep` = source index, not requirement rewrite
- `/tk:gap` = SOT reference vs commit/code comparison + workflow status guidance
- `/tk:checkpoint` = decision gate for ambiguity, access, verification, and user decisions
- `/tk:review` = adversarial compliance review, with reuse exploration omissions as high-priority findings
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

IMPLEMENTATION_POLICY.md  # binding project policy SOT candidate, existing-only
DESIGN.md                 # existing-only, not created by TigerKit
COMPONENT_REUSE_MAP.md    # preferred derived reuse map, existing-only
reuse-map.md              # legacy alias / migration candidate only
CLAUDE.md                 # optional TigerKit managed section proposal
```

Root-level `.tigerkit/requirements.md`, `.tigerkit/gap.md`, `.tigerkit/reflect.md` are deprecated artifacts. TigerKit commands treat them as migration candidates, not active write targets.

`{escaped-branch}` is collision-safe path encoding of current git branch. ASCII letter, digit, `.`, `_`, `-` stay unchanged; other bytes encode as `~HH` uppercase hex. Example: `feature/foo` → `feature~2Ffoo`, `feature__foo` → `feature__foo`.

| Artifact | 역할 |
| --- | --- |
| `.tigerkit/branches/{escaped-branch}/requirements.md` | source-of-truth reference index. 외부 source는 reference만 저장하고, 현재 session 사용자 인터뷰만 raw text로 보존 |
| `.tigerkit/branches/{escaped-branch}/gap.md` | specific SOT reference와 specific code baseline 사이 evidence-based comparison 기록 |
| `/tk:checkpoint` output | artifact가 아니라 chat Decision Gate. ambiguity, access, verification, user decision, self-resolvable item 분리 |
| `/tk:review` output | artifact가 아니라 chat compliance review. TigerKit 준수룰 위반 finding 또는 `NO_FINDINGS` 출력 |
| `.tigerkit/branches/{escaped-branch}/reflect.md` | session-wide reflection. durable learning과 one-off correction 분리, escalation 후보 기록 |
| `.tigerkit/branches/{escaped-branch}/handoff.md` | 다음 모델/세션을 위한 continuation contract, artifact map, baseline checkpoint |
| `CLAUDE.md` | optional TigerKit managed section. repo workflow guidance 후보는 사용자 승인 후만 반영 |
| `DESIGN.md` | derived repo-level design knowledge. 외부 SOT 대체 금지. 파일이 없으면 생성하지 않으며, 반영할 derived design knowledge가 있을 때만 초기화 필요를 알림 |
| `COMPONENT_REUSE_MAP.md` | preferred derived map of inspected reusable components, hooks, utilities, API clients, adapters, form patterns, validation patterns, UI composition patterns, test helpers, and avoid/deprecated patterns. source of truth 아님 |
| `reuse-map.md` | legacy alias / migration candidate only. active source of truth나 preferred active artifact로 다루지 않음 |

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

`requirements.md`는 source of truth가 아닙니다. source of truth 위치와 access status를 가리키는 branch-local index입니다.

외부 source는 reference와 accessibility metadata만 저장합니다.

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

### SOT accessibility

SOT reference는 접근 가능하고 inspect되기 전까지 binding-auditable로 다루지 않습니다.

- URL은 image/document/design을 실제로 본 것과 같지 않습니다.
- inaccessible URL, image, Figma/design link, screenshot URL, local path는 pending SOT entry로 기록합니다.
- pending entry에는 `access_status`, original reference, represents, binding 여부, needed fallback을 기록합니다.
- fallback은 file upload, local path, screenshot/export, pasted content 중 하나를 요청합니다.
- binding visual SOT는 stable local asset reference를 선호합니다. 예: `./docs/assets/sot/requirements/1.1.1.png`
- 기존 `docs/SOT_MANIFEST.md`, `docs/REQUIREMENTS.md`, `docs/DESIGN.md`, `IMPLEMENTATION_POLICY.md`, `docs/assets/sot/`는 source category candidate로 intake하고 단일 `SOT.md`로 합치지 않습니다.
- `IMPLEMENTATION_POLICY.md`가 있으면 binding project policy SOT candidate로 다룹니다.
- `COMPONENT_REUSE_MAP.md`는 target repo가 명시적으로 SOT로 정의한 경우가 아니면 derived reuse map입니다. `reuse-map.md`는 legacy alias 또는 migration candidate로만 읽습니다.

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

`/tk:gap`은 `SOT Access Coverage`, `Coverage Inventory`, `Gap Table`, `Decision Gate`를 통해 scoped SOT item 중 무엇을 실제 비교했는지 보여줍니다. Low-severity copy, label, placeholder, tooltip, modal, table column, status label, visible format, line break, policy mismatch도 audit scope에 있으면 inventory에 포함합니다. `Not verifiable`은 `Match`가 아닙니다.

inaccessible SOT는 내용을 추측하지 않고 `notVerifiable`, `pending_user_asset`, 또는 `BLOCKED_BY_ACCESS`로 다룹니다. dependent item을 evidence 없이 `Match`로 표시하지 않습니다. `/tk:gap`은 `SOT Access Coverage`를 포함하고, inaccessible binding SOT가 있으면 audit이 partial임을 명시합니다.

## SOT priority and conflict rule

| Priority | Source | Applies to |
|---|---|---|
| P0 | Current explicit user instruction in the current session | 현재 요청에 직접 적용되는 최신 사용자 지시 |
| P1 | Binding project policy / architecture decisions / user-confirmed durable feedback | project policy, architecture, durable user-confirmed rule |
| P2 | Design SOT | visible UI, layout, spacing, border, typography, visual states, visible copy |
| P3 | Requirements / PRD / business spec | business logic, validation, permissions, workflow, data semantics, API behavior |
| P4 | Existing code baseline | actual evidence only, not authority over active SOT |
| P5 | Model inference | explicitly marked assumption only |

Existing code는 active policy/design/requirements SOT 위반을 정당화하지 않습니다. visible UI/copy/layout/style conflict에서는 design SOT가 explicit visible target을 제공하면 일반적으로 design SOT가 우선합니다. business logic, validation, permission, workflow, API behavior, data semantics는 requirements SOT가 우선하며, design SOT가 functional behavior를 명시적으로 override할 때만 예외입니다. 우선순위로 해결되지 않으면 `sot_conflict`로 기록합니다.

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

## review

`/tk:review`는 artifact를 쓰지 않는 chat compliance review입니다. TigerKit command, docs, evals, branch-local artifacts, implementation changes가 TigerKit 준수룰을 지키는지 적대적으로 검토합니다.

High-priority finding 예:

- repo-wide reuse exploration 없이 새 component/hook/util/mapper/API client/layout primitive/UI pattern 생성
- `COMPONENT_REUSE_MAP.md` miss를 reusable module 없음의 evidence로 사용
- `reuse-map.md` legacy alias를 active source of truth 또는 preferred artifact처럼 사용
- common module 수정 전 callsite impact analysis와 explicit user approval 누락
- 외부 SOT를 local requirement로 요약, 복사, 재작성
- inaccessible SOT 내용을 추측하거나 dependent item을 evidence 없이 `Match` 처리
- pending SOT entry나 accessible fallback 요청 누락
- SOT access coverage 없이 gap audit을 complete처럼 표시
- dirty/staged diff를 reproducible baseline처럼 사용
- gap을 work queue로 변환
- severity와 resolvability 혼합
- `/tk:reflect`를 default next command로 추천
- command/docs/evals/manifest command surface drift

finding이 없으면 `NO_FINDINGS`만 출력합니다. `/tk:review`는 수정, commit, push, PR 생성을 하지 않습니다.

## reflect.md

`reflect.md`는 현재 대화 context를 primary source로 사용합니다. artifact와 git evidence는 보조 근거이며, context에 없는 내용은 `확인 불가`로 둡니다. Reflection 후에는 `CLAUDE.md`, `MEMORY.md`, `DESIGN.md`, `COMPONENT_REUSE_MAP.md` escalation 후보를 제안하고, 사용자 승인 전에는 durable artifact를 수정하지 않습니다. `reuse-map.md`는 legacy fallback/migration candidate로만 다룹니다.

사용 대상:

- repeated failure patterns
- durable learnings
- one-off corrections
- proposed updates to `DESIGN.md`
- proposed updates to `COMPONENT_REUSE_MAP.md`

one-off correction은 future work에 영향을 줘야 한다는 evidence가 있을 때만 durable rule로 승격합니다.

## DESIGN.md / IMPLEMENTATION_POLICY.md / COMPONENT_REUSE_MAP.md

`DESIGN.md`와 `COMPONENT_REUSE_MAP.md`는 derived repo-level knowledge입니다. 외부 SOT를 대체하지 않습니다.

`DESIGN.md`에는 architecture, boundaries, data flow, UI/API conventions, stable constraints, non-goals, repo-specific decisions를 담을 수 있습니다. 파일이 없으면 TigerKit이 생성하지 않고, 넣을 내용이 생겼다는 notification만 남깁니다.

`IMPLEMENTATION_POLICY.md`가 target repo에 있으면 binding project policy SOT candidate입니다. Architecture decision, dependency policy, required/avoided/banned/deprecated/preferred component or pattern, user-confirmed durable feedback, implementation constraint, non-goal, policy exception을 담을 수 있습니다. TigerKit은 자동 생성하지 않고, 외부 SOT 내용을 사용자 승인 없이 복사하지 않습니다.

`COMPONENT_REUSE_MAP.md`에는 reusable components, hooks, utilities, API clients, adapters, form/validation/UI composition/test patterns, avoid/deprecated patterns를 구체 path와 함께 담을 수 있습니다. `reuse-map.md`가 있으면 legacy alias 또는 migration candidate로만 읽고, 둘 다 있으면 duplicate reuse maps can diverge 경고가 필요합니다.

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
