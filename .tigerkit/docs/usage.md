# TigerKit 운영 사용법

이 문서는 TigerKit command surface 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`, 패키징 메타데이터는 `support/execute-support-matrix.json`을 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash, contract field name은 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = gap + route + reflect + forge + ui-diff
```

- `gap`: SoT와 Current Implementation의 차이를 한 번 분석합니다. evidence-first로 읽고 source conflict나 근거 부족은 `ambiguous`로 남깁니다.
- `route`: 지금 task를 direct, subagent-driven, goal-driven 중 어떤 route로 가져갈지 얇게 비교하고 첫 스텝을 정리합니다.
- `reflect`: 세션 result와 사용자 피드백에서 재사용 가능한 learning을 canonical target으로 분류하고, repo-local guidance는 기본 apply(opt-out)로 반영할 수 있습니다.
- `forge`: reflect가 제안한 durable candidate를 실제 artifact로 생성합니다. 1차 범위는 `skill only`입니다.
- `ui-diff`: 번들된 ui-diff 엔진 skill을 현재 repo의 `.claude/ui-diff/` profile과 함께 사용하는 direct QA surface입니다.

TigerKit은 일반 autopilot 또는 sealed workflow engine이 아니라 gap, route, reflect, forge, ui-diff 중심의 가벼운 surface를 제공합니다.

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없으면 먼저 SoT 제공을 제안합니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.
- `/tk:route`는 source를 수정하지 않고 route만 정합니다.
- `/tk:reflect`는 repo-local guidance를 기본 apply(opt-out)로 반영할 수 있습니다.
- `/tk:forge`는 reflect가 제안한 candidate를 source로 굳히는 surface입니다.
- `/tk:ui-diff`는 개인 설치와 repo-owned 팀 설치를 나누는 provisioning surface입니다.

## Command Surface

| Command | 역할 | 저장 성격 |
|---|---|---|
| `/tk:gap` | SoT와 Current를 비교해 missing, mismatch, overbuilt, ambiguous를 보고합니다. | optional external generated report |
| `/tk:route` | 지금 이 task를 어떤 구현 route로 가져갈지 얇게 비교하고 첫 스텝을 정리합니다. | no persisted artifact by default |
| `/tk:reflect` | session result와 feedback에서 개선 후보를 canonical target으로 분류하고 repo-local guidance는 기본 apply로 반영할 수 있습니다. | reflect ledger + compact summary |
| `/tk:forge` | reflect가 제안한 candidate를 실제 artifact로 생성합니다. | user-level skill write + compact summary |
| `/tk:ui-diff` | ui-diff 엔진과 profile을 mode에 맞게 설치/갱신합니다. | provisioning summary + optional writes |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:route "결제 모달 scroll 복구 버그 수정"
/tk:reflect --target repo-local
/tk:reflect --target repo-local --apply=false
/tk:forge R3
/tk:forge --desc "이 CDP 검증 루틴을 skill로 굳혀줘"
/tk:ui-diff
/tk:ui-diff "QA와 로컬 비교"
```

## Reflect target model

Canonical target enum:

```text
repo-local, repo-shared, user-global, skill, hook, command, agent, discard
```

Legacy selector:

- `--target repo`는 `repo-local`, `repo-shared`로 확장하고 deprecation warning을 출력합니다.
- `--target user`는 `user-global`로 확장하고 deprecation warning을 출력합니다.
- `--target all`은 전체 canonical target을 가리키지만, direct write는 repo-local만 가능합니다.

`PROFILE.md`, `automation`, `hookify`는 target 이름이 아닙니다.

## Reflect write model

`/tk:reflect`가 파일을 쓸 수 있는 유일한 target은 eligibility를 통과한 `<git-root>/CLAUDE.local.md`입니다.

- option 생략 = 기본 apply
- `--apply=false` = preview-only
- exact `apply_plan`은 ledger에 기록
- stdout은 compact summary만 유지

## Forge model

- same-session + same-ledger candidate만 읽습니다.
- 1차 범위는 `skill only`입니다.
- 이름은 생성 전 사용자 확정이 필요합니다.
- `hook|command|agent`는 reflect 후보 target으로만 남습니다.

## UI Diff provisioning model

mode별 설치 위치:

- user-level
  - engine: `~/.claude/skills/ui-diff/`
  - profile: `~/.claude/ui-diff/profiles/<repo-key>/`
- repo-internal
  - engine: `<root>/.claude/skills/ui-diff/`
  - profile: `<root>/.claude/ui-diff/`

lookup 우선순위:

1. repo-internal profile
2. user-level profile
3. 없으면 `tk:ui-diff`가 필요한 파일 경로를 안내하고 중단

재실행 기본 동작은 abort입니다. 기존 자산이 있으면 차이 요약을 보여주고, 사용자가 명시적으로 update를 선택할 때만 진행합니다.

## Generated state

Active TigerKit generated state는 project repository 밖 `~/.tigerkit` 아래의 file-only state입니다. `.claude/tigerkit`는 legacy/migration context로만 남기고 새 runtime write path로 사용하지 않습니다.

주요 active path:

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml
```

`/tk:route`는 기본적으로 persisted artifact를 만들지 않습니다.
