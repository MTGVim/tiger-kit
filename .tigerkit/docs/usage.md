# TigerKit 운영 사용법

이 문서는 TigerKit command surface 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash, contract field name은 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = gap + route + reflect + grill + prototype + arch-review + merge-conflict + handoff + to-prd + to-issues + ui-diff
```

- `gap`: SoT와 Current Implementation의 차이를 한 번 분석합니다. evidence-first로 읽고 source conflict나 근거 부족은 `ambiguous`로 남깁니다.
- `route`: 지금 task를 direct, subagent-driven, goal-driven 중 어떤 route로 가져갈지 얇게 비교하고 첫 스텝을 정리합니다.
- `reflect`: 세션 result와 사용자 피드백에서 재사용 가능한 learning을 canonical target으로 분류하고, repo-local/user-global 기본 apply와 명시적 skill materialize를 처리합니다.
- `grill`: 계획, 설계, RFC, 개선안을 수렴형 질문으로 압박 검증합니다.
- `prototype`: UI 또는 logic/state 가설을 throwaway prototype으로 빠르게 검증합니다.
- `arch-review`: boundary, ownership, coupling, 반복 마찰을 evidence-first로 검토하는 report-only architecture review입니다.
- `merge-conflict`: merge/rebase conflict를 ours/theirs intent 기준으로 해결합니다.
- `handoff`: 다음 세션이나 다른 에이전트가 바로 이어받을 수 있는 handoff를 만듭니다.
- `to-prd`: 현재 대화나 요구사항을 draft-only PRD로 정리합니다.
- `to-issues`: plan/PRD를 independently grabbable vertical-slice issue draft로 분해합니다.
- `ui-diff`: 번들된 ui-diff 엔진 skill을 현재 repo의 `.claude/ui-diff/` profile과 함께 사용하는 direct QA surface입니다.

TigerKit은 일반 autopilot 또는 sealed workflow engine이 아니라 gap, route, reflect, grill, prototype, arch-review, merge-conflict, handoff, to-prd, to-issues, ui-diff 중심의 가벼운 surface를 제공합니다.

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없으면 먼저 SoT 제공을 제안합니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.
- `/tk:route`는 source를 수정하지 않고 route만 정합니다.
- `/tk:reflect`는 repo-local guidance 기본 apply, user-global apply, skill materialize를 모두 처리합니다.
- `/tk:grill`은 질문 루프로 전제를 압박 검증하는 surface입니다.
- `/tk:prototype`은 throwaway 검증용 surface입니다.
- `/tk:arch-review`는 evidence-first 구조 리뷰 surface입니다.
- `/tk:merge-conflict`는 conflict 해결 전용 surface입니다.
- `/tk:handoff`는 repo-local handoff 생성 surface입니다.
- `/tk:to-prd`는 draft-only PRD 생성 surface입니다.
- `/tk:to-issues`는 vertical-slice issue draft 생성 surface입니다.
- `/tk:ui-diff`는 번들된 ui-diff 엔진 skill을 현재 repo의 `.claude/ui-diff/` profile과 함께 사용하는 direct QA surface입니다.

## Command Surface

| Command | 역할 | 저장 성격 |
|---|---|---|
| `/tk:gap` | SoT와 Current를 비교해 missing, mismatch, overbuilt, ambiguous를 보고합니다. | optional external generated report |
| `/tk:route` | 지금 이 task를 어떤 구현 route로 가져갈지 얇게 비교하고 첫 스텝을 정리합니다. | no persisted artifact by default |
| `/tk:reflect` | session result와 feedback에서 개선 후보를 canonical target으로 분류하고 repo-local/user-global 기본 apply와 explicit skill materialize를 처리합니다. | reflect ledger + compact summary |
| `/tk:grill` | 계획, 설계, RFC, 개선안을 수렴형 질문으로 압박 검증합니다. | inline questioning + compact summary |
| `/tk:prototype` | UI 또는 logic/state 가설을 throwaway prototype으로 검증합니다. | prototype files + compact summary |
| `/tk:arch-review` | boundary, ownership, coupling, 반복 마찰을 evidence-first로 검토하는 report-only architecture review입니다. | inline architecture review |
| `/tk:merge-conflict` | merge/rebase conflict를 상태 확인 → intent 추적 → 검증 순서로 해결합니다. | conflict resolution summary |
| `/tk:handoff` | 다음 세션이나 다른 에이전트가 바로 이어받을 수 있는 handoff를 만듭니다. | repo-local handoff artifact |
| `/tk:to-prd` | 현재 대화나 요구사항을 draft-only PRD로 정리합니다. | repo-local PRD draft |
| `/tk:to-issues` | plan/PRD를 independently grabbable vertical-slice issue draft로 분해합니다. | repo-local issue draft set |
| `/tk:ui-diff` | ui-diff 엔진 skill을 현재 repo의 `.claude/ui-diff/` profile과 함께 사용하는 direct QA surface입니다. | direct QA summary |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:route "결제 모달 scroll 복구 버그 수정"
/tk:reflect --target repo-local
/tk:reflect --target repo-local --apply=false
/tk:reflect R3 --target skill --apply=true
/tk:grill "이 설계 전제 허점 짚어줘"
/tk:prototype "이 flow를 throwaway로 확인해줘" --ui
/tk:arch-review "이 모듈 경계가 왜 자꾸 새는지 검토해줘"
/tk:merge-conflict
/tk:handoff "다음 세션용 handoff 만들어줘"
/tk:to-prd "이 요구를 PRD로 정리해줘"
/tk:to-issues "이 PRD를 issue draft로 쪼개줘"
/tk:reflect --target skill --apply=true --desc "이 CDP 검증 루틴을 skill로 굳혀줘"
/tk:ui-diff
/tk:ui-diff "QA와 로컬 비교"
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
- 1차 범위는 `skill only`입니다.
- 이름은 생성 전 사용자 확정이 필요합니다.
- 생성 target은 agent가 지원하는 user skill surface입니다. Claude Code 계열이면 `~/.claude/skills/<name>/SKILL.md`가 예시입니다.
- `hook|command|agent`는 reflect 후보 target으로만 남습니다.

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

- 기본은 repo-local write입니다.
- Goal / Current state / Decisions / Changed files / Commands / Verification / Remaining tasks / Open questions / Risks / Suggested next skills / Do-not-repeat context를 포함합니다.

## To-PRD model

- 기본은 draft-only 입니다.
- approval 전 publish 하지 않습니다.
- acceptance criteria를 포함합니다.

## To-Issues model

- 기본은 draft-only 입니다.
- vertical slice only입니다.
- blocked-by / dependency를 명시합니다.

## UI Diff surface model

`/tk:ui-diff`는 provisioning command가 아니라 direct QA surface입니다.

- engine source: repo에 번들된 `skills/ui-diff/`
- profile source: 현재 repo의 `<root>/.claude/ui-diff/`
- profile이 없으면 `tk:ui-diff`가 bundled template 기준으로 `.claude/ui-diff/` 신규 생성 절차로 들어가고 missing 파일만 만듭니다.
- `login.local.md`는 gitignored local override입니다.

## Generated state

Active TigerKit runtime generated state는 project repository 밖 `~/.tigerkit` 아래의 file-only state입니다. repo-local draft artifact는 `.claude/tigerkit/` 아래의 handoff / prd / issues 경로를 사용합니다.

주요 active path:

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml
```

`/tk:route`는 기본적으로 persisted artifact를 만들지 않습니다.
