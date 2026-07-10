# TigerKit 운영 사용법

이 문서는 TigerKit command surface 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash, contract field name은 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = help + gap + route + next + quiz + reflect + learn + grill + grooming + prototype + wayfinder + arch-review + merge-conflict + handoff + handon + to-prd + to-issues + browser-verify
```

- `help`: 지금 어떤 command를 먼저 열어야 하는지 정리하는 navigation surface입니다.
- `gap`: SoT와 Current Implementation의 차이를 한 번 분석합니다. evidence-first로 읽고 source conflict나 근거 부족은 `ambiguous`로 남깁니다. SoT가 없으면 blindspot 질문 목록으로 discovery를 시작할 수도 있습니다.
- `route`: 지금 task를 direct, subagent-driven, goal-driven 중 어떤 route로 가져갈지 얇게 비교하고 첫 스텝을 정리합니다. 실행 시 계약 블록과 ledger path를 복사 가능한 형태로 제안할 수 있습니다.
- `next`: 현재 task나 current artifact 상태를 보고 다음 command 1개만 고르는 conductor surface입니다.
- `quiz`: merge 전 diff + ledger 기반 이해도 게이트를 여는 surface입니다.
- `reflect`: 세션 result와 사용자 피드백에서 재사용 가능한 learning을 canonical target으로 분류하고, repo-local/user-global 기본 apply와 명시적 skill materialize를 처리합니다. 실패 유형을 먼저 분류하고 stdout에는 compact evidence pointer를 남깁니다.
- `learn`: path, URL, 현재 대화, notes, 또는 reflect candidate를 source로 받아 reusable skill을 직접 만듭니다. 완료 판정은 `RED → GREEN → REFACTOR` evidence와 `pos3 / neg2 / owner` eval coverage를 같이 요구합니다.
- `grill`: 계획, 설계, RFC, 개선안을 수렴형 질문으로 압박 검증하고, 사용자가 답을 모른다고 **직접 말할 때만** 후보를 최대 3개까지 제안할 수 있습니다.
- `grooming`: guidance 파일을 report-only로 평가하고, 승인된 user-global 변경만 직접 반영하며 나머지는 suggestion-only로 남깁니다. `guidanceBudgetBytes` budget, footprint, archive/demotion 제안을 함께 다룹니다.
- `prototype`: UI 또는 logic/state 가설을 throwaway prototype으로 빠르게 검증합니다.
- `wayfinder`: 긴 작업의 shared map과 reopen hint를 worktree-scoped current-first artifact로 남깁니다.
- `arch-review`: boundary, ownership, coupling, 반복 마찰을 evidence-first로 검토하는 report-only architecture review입니다.
- `merge-conflict`: merge/rebase conflict를 ours/theirs intent 기준으로 해결합니다.
- `handoff`: 다음 세션이나 다른 에이전트가 바로 이어받을 수 있는 handoff를 만듭니다.
- `handon`: 현재 repo/worktree의 저장된 handoff를 다시 읽습니다.
- `to-prd`: 현재 대화나 요구사항을 draft-only PRD로 정리합니다.
- `to-issues`: plan/PRD를 independently grabbable vertical-slice issue draft로 분해합니다.
- `browser-verify`: 번들된 browser-verify 엔진 skill을 현재 repo에 대응하는 `~/.tigerkit/repos/<repo-key>/browser-verify/` profile과 함께 사용하는 direct QA / behavior verification surface입니다.

TigerKit은 일반 autopilot 또는 sealed workflow engine이 아니라 help, gap, route, next, quiz, reflect, learn, grill, grooming, prototype, wayfinder, arch-review, merge-conflict, handoff, handon, to-prd, to-issues, browser-verify 중심의 가벼운 surface를 제공합니다.

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- entrypoint가 막연하면 `/tk:help`로 먼저 navigation을 잡습니다.
- `/tk:next`는 다음 command 1개만 고르는 conductor이고, 자동 연쇄 실행은 하지 않습니다.
- `/tk:quiz`는 merge 전 diff + ledger 기반 이해도 게이트입니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.
- `/tk:route`는 source를 수정하지 않고 route만 정합니다.
- `/tk:reflect`는 repo-local guidance 기본 apply, user-global apply, skill materialize를 모두 처리합니다.
- `/tk:learn`은 source-to-skill surface이며 `skill only` 경계로 user skill surface에만 씁니다.
- `/tk:grill`은 질문 루프로 전제를 압박 검증하는 surface이고, 사용자가 답을 모른다고 **직접 말할 때만** 후보를 최대 3개까지 제안할 수 있습니다.
- `/tk:grooming`은 guidance 파일을 report-only로 평가하고, 승인된 user-global 변경만 direct apply하며 나머지는 suggestion-only로 남깁니다.
- `/tk:prototype`은 throwaway 검증용 surface입니다.
- `/tk:wayfinder`는 긴 작업의 shared map과 reopen hint를 current-first artifact로 남깁니다.
- `/tk:arch-review`는 evidence-first 구조 리뷰 surface입니다.
- `/tk:merge-conflict`는 conflict 해결 전용 surface입니다.
- `/tk:handoff`는 repo-scoped `~/.tigerkit` root 아래 worktree-scoped current-first handoff 생성 surface입니다.
- `/tk:handon`은 repo-scoped `~/.tigerkit` root 아래 worktree-scoped current-first handoff read surface입니다.
- `/tk:to-prd`는 draft-only PRD 생성 surface입니다.
- `/tk:to-issues`는 vertical-slice issue draft 생성 surface입니다.
- `/tk:browser-verify`는 번들된 browser-verify 엔진 skill을 현재 repo에 대응하는 `~/.tigerkit/repos/<repo-key>/browser-verify/` profile과 함께 사용하는 direct QA / behavior verification surface입니다.

## Shared command boundaries

아래 경계는 여러 TigerKit command가 공통으로 따릅니다.

- command가 직접 소유한 artifact surface가 아니면 source tree, plugin manifest, command source를 임의 수정하지 않습니다.
- preview-only / report-only / draft-only surface는 그 경계를 유지하고 구현 완료처럼 포장하지 않습니다.
- 승인 우회, silent publish, chat dump, endless questioning, fake success 같은 운영 노이즈를 만들지 않습니다.
- 이미 코드나 artifact에서 직접 확인 가능한 사실은 다시 묻거나 장문 복붙으로 반복하지 않습니다.

개별 command 문서는 이 공통 경계를 반복 나열하는 대신, command-specific guidance와 output contract에 집중합니다.

## Command Surface

| Command | 역할 | 저장 성격 |
|---|---|---|
| `/tk:help` | 지금 어떤 command를 먼저 열어야 하는지와 다음 연결 후보를 정리합니다. | generated help-map summary |
| `/tk:gap` | SoT와 Current를 비교해 missing, mismatch, overbuilt, ambiguous를 보고합니다. | optional external generated report |
| `/tk:route` | 지금 이 task를 어떤 구현 route로 가져갈지 얇게 비교하고 첫 스텝을 정리합니다. | no persisted artifact by default |
| `/tk:next` | 현재 task나 current artifact 상태를 바탕으로 다음 command 1개만 추천합니다. | no persisted artifact by default |
| `/tk:quiz` | merge 전 diff + ledger 기반 이해도 게이트를 실행합니다. | worktree-scoped quiz report under repo-scoped `~/.tigerkit` root |
| `/tk:reflect` | session result와 feedback에서 개선 후보를 canonical target으로 분류하고 repo-local/user-global 기본 apply와 explicit skill materialize를 처리합니다. | reflect ledger + compact summary |
| `/tk:learn` | path, URL, 현재 대화, notes, 또는 reflect candidate에서 reusable skill을 직접 만듭니다. | skill draft / user skill source |
| `/tk:grill` | 계획, 설계, RFC, 개선안을 수렴형 질문으로 압박 검증하고, 사용자가 답을 모른다고 **직접 말할 때만** 후보를 최대 3개까지 제안할 수 있습니다. | inline questioning + compact summary |
| `/tk:grooming` | guidance 파일을 report-only로 평가하고, 승인된 user-global 변경만 direct apply하며 나머지는 suggestion-only로 남깁니다. | guidance audit + compact summary |
| `/tk:prototype` | UI 또는 logic/state 가설을 throwaway prototype으로 검증합니다. | prototype files + compact summary |
| `/tk:wayfinder` | 긴 작업의 shared map과 reopen hint를 current-first artifact로 정리합니다. | worktree-scoped wayfinder map under repo-scoped `~/.tigerkit` root |
| `/tk:arch-review` | boundary, ownership, coupling, 반복 마찰을 evidence-first로 검토하는 report-only architecture review입니다. | inline architecture review |
| `/tk:merge-conflict` | merge/rebase conflict를 상태 확인 → intent 추적 → 검증 순서로 해결합니다. | conflict resolution summary |
| `/tk:handoff` | 다음 세션이나 다른 에이전트가 바로 이어받을 수 있는 handoff를 만듭니다. | worktree-scoped handoff artifact under repo-scoped `~/.tigerkit` root |
| `/tk:handon` | 현재 repo/worktree의 최신 handoff draft를 다시 읽습니다. | read-only current handoff reopen under repo-scoped `~/.tigerkit` root |
| `/tk:to-prd` | 현재 대화나 요구사항을 draft-only PRD로 정리합니다. | worktree-scoped PRD draft under repo-scoped `~/.tigerkit` root |
| `/tk:to-issues` | plan/PRD를 independently grabbable vertical-slice issue draft로 분해합니다. | worktree-scoped issue draft set under repo-scoped `~/.tigerkit` root |
| `/tk:browser-verify` | browser-verify 엔진 skill을 현재 repo에 대응하는 `~/.tigerkit/repos/<repo-key>/browser-verify/` profile과 함께 사용하는 direct QA / behavior verification surface입니다. | direct QA summary |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:route "결제 모달 scroll 복구 버그 수정"
/tk:reflect --target repo-local
/tk:learn "what we just did"
/tk:reflect --target repo-local --apply=false
/tk:reflect R3 --target skill --apply=true
/tk:grill "이 설계 전제 허점 짚어줘"
/tk:grooming --scope all
/tk:prototype "이 flow를 throwaway로 확인해줘" --ui
/tk:arch-review "이 모듈 경계가 왜 자꾸 새는지 검토해줘"
/tk:merge-conflict
/tk:handoff "다음 세션용 handoff 만들어줘"
/tk:handon "남은 작업만 짧게"
/tk:to-prd "이 요구를 PRD로 정리해줘"
/tk:to-issues "이 PRD를 issue draft로 쪼개줘"
/tk:reflect --target skill --apply=true --desc "이 CDP 검증 루틴을 skill로 굳혀줘"
/tk:browser-verify
/tk:browser-verify "QA와 로컬 비교"
```

## Reflect target model

Canonical target enum:

```text
repo-local, repo-shared, user-global, skill, hook, command, agent, discard
```

`PROFILE.md`, `automation`, `hookify`는 target 이름이 아닙니다.

## Reflect write model

`/tk:reflect`가 기본적으로 direct write할 수 있는 target은 지원 host의 `repo-local` 또는 `user-global` guidance surface입니다.

- option 생략 = 기본 apply
- `--apply=false` = preview-only
- 기본 apply 대상 = `repo-local`, `user-global`
- exact `apply_plan`은 ledger에 기록
- stdout은 compact summary만 유지

## Reflect skill-materialize model

- same-session + same-ledger candidate만 읽습니다.
- reflect candidate는 ledger를 source of truth로 읽습니다.
- 1차 범위는 `skill only`입니다.
- 이름은 생성 전 사용자 확정이 필요합니다.
- 생성 target은 agent가 지원하는 user skill surface입니다. Claude Code 계열이면 `~/.claude/skills/<name>/SKILL.md`가 예시입니다.
- `hook|command|agent`는 reflect 후보 target으로만 남습니다.

## Learn model

- source mode는 `direct` 또는 `reflect-candidate`입니다.
- direct source는 path / directory / URL / 현재 대화 / notes 입니다.
- 기본은 preview-only 입니다.
- explicit apply일 때만 user skill surface에 씁니다.
- `repo-local`, `user-global`, `hook`, `command`, `agent`는 이 surface가 직접 쓰지 않습니다.

## Arch-review model

- report-only입니다.
- 자동 refactor, rename, docs rewrite를 완료처럼 말하지 않습니다.
- boundary, ownership, coupling, repeated pain을 evidence-first로 구분합니다.

## Grill model

- 한 번에 하나의 질문만 던집니다.
- 코드베이스에서 직접 확인 가능한 것은 먼저 확인합니다.
- hard cap 대신 5회 이상 길어지면 hint를 노출합니다.

## Prototype model

- `ui` 또는 `logic` mode로 빠르게 검증합니다.
- 기본은 no-commit입니다.
- fake와 real 연결을 구분해 보고합니다.

## Merge-conflict model

- merge/rebase 상태 확인이 먼저입니다.
- ours/theirs intent를 추적합니다.
- `reset --hard`, `clean`, force push는 금지입니다.

## Handoff model

- 기본은 repo-scoped `~/.tigerkit` root 아래 worktree-scoped current-first write입니다.
- Goal / Current state / Decisions / Changed files / Commands / Verification / Remaining tasks / Open questions / Risks / Suggested next skills / Do-not-repeat context를 포함합니다.

## Handon model

- 기본은 repo-scoped `~/.tigerkit` root 아래 worktree-scoped current-first read입니다.
- source of truth는 `handoffs/current.md` 저장본입니다.
- handoff가 없으면 missing path를 숨기지 않습니다.

## To-PRD model

- 기본은 draft-only 입니다.
- approval 전 publish 하지 않습니다.
- acceptance criteria를 포함합니다.

## To-Issues model

- 기본은 draft-only 입니다.
- vertical slice only입니다.
- blocked-by / dependency를 명시합니다.

## Browser Verify surface model

`/tk:browser-verify`는 provisioning command가 아니라 direct QA / behavior verification surface입니다.

- engine source: repo에 번들된 `skills/browser-verify/`
- profile source: 현재 repo에 대응하는 `~/.tigerkit/repos/<repo-key>/browser-verify/`
- 신 profile이 없고 legacy `~/.tigerkit/repos/<repo-key>/ui-diff/`가 있으면 migration guide를 출력하고 멈춥니다.
- 둘 다 없으면 `tk:browser-verify`가 bundled template 기준으로 `~/.tigerkit/repos/<repo-key>/browser-verify/` 신규 생성 절차로 들어가고 missing 파일만 만듭니다.
- `login.local.md`는 tracked repo 밖 `~/.tigerkit` 아래에 두는 local override입니다.
- 구체적인 이동 절차는 `.tigerkit/docs/browser-verify-migration.md`를 봅니다.

## Generated state

Active TigerKit runtime generated state는 project repository 밖 `~/.tigerkit` 아래의 file-only state입니다. repo-scoped draft artifact는 `~/.tigerkit/repos/<repo-key>/worktrees/<worktree-key>/` 아래의 handoff / prd / issues current 경로를 사용하고, `/tk:handon`은 그 handoff current 경로를 읽습니다. `/tk:browser-verify` profile은 `~/.tigerkit/repos/<repo-key>/browser-verify/`를 사용합니다.

주요 active path:

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml
```

`/tk:route`는 기본적으로 persisted artifact를 만들지 않습니다.
