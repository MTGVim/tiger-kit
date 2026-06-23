# TigerKit 운영 사용법

이 문서는 TigerKit command surface 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`, 패키징 메타데이터는 `support/execute-support-matrix.json`을 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash, contract field name은 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = gap + route + reflect
```

- `gap`: SoT와 Current Implementation의 차이를 한 번 분석합니다. evidence-first로 읽고 source conflict나 근거 부족은 `ambiguous`로 남깁니다.
- `route`: 지금 task를 direct, subagent-driven, goal-driven 중 어떤 route로 가져갈지 얇게 비교하고 첫 스텝을 정리합니다.
- `reflect`: 세션 result와 사용자 피드백에서 재사용 가능한 learning을 preview-first promotion result로 분류합니다.

TigerKit은 일반 autopilot 또는 sealed workflow engine이 아니라 gap, route, reflect 중심의 가벼운 surface를 제공합니다.

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없으면 먼저 SoT 제공을 제안합니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.
- `/tk:route`는 source를 수정하지 않고 route만 정합니다.
- legacy LoopSpec/execute helper가 남아 있더라도 active `/tk:*` surface로 권하지 않습니다.
- `/tk:reflect` 기본값은 preview-only입니다.

## Command Surface

| Command | 역할 | 저장 성격 |
|---|---|---|
| `/tk:gap` | SoT와 Current를 비교해 missing, mismatch, overbuilt, ambiguous를 보고합니다. | optional external generated report |
| `/tk:route` | 지금 이 task를 어떤 구현 route로 가져갈지 얇게 비교하고 첫 스텝을 정리합니다. | no persisted artifact by default |
| `/tk:reflect` | session result와 feedback에서 개선 후보를 canonical target으로 분류합니다. | promotion candidates |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:route "결제 모달 scroll 복구 버그 수정"
/tk:route "이 작업을 subagent-driven으로 넘길지 /goal로 풀지 정리해줘"
/tk:reflect --target repo --apply=false
/tk:reflect --target repo-local --apply=true
```

## Reflect target model

Canonical target enum:

```text
repo-local, repo-shared, user-global, skill, hook, command, agent, discard
```

Legacy selector:

- `--target repo`는 `repo-local`, `repo-shared`로 확장하고 deprecation warning을 출력합니다.
- `--target user`는 `user-global`로 확장하고 deprecation warning을 출력합니다.
- `--target all --apply=true`는 eligible `repo-local`만 write set에 넣을 수 있습니다.

`PROFILE.md`, `automation`, `hookify`는 target 이름이 아닙니다.

## Reflect write model

`/tk:reflect --apply=true`가 파일을 쓸 수 있는 유일한 target은 eligibility를 통과한 `<git-root>/CLAUDE.local.md`입니다.

Apply는 current invocation apply plan, exact apply set, base/result sha256, planned result bytes, exact unified diff, all-or-nothing, stale plan rejection, post-write verification, rollback receipt를 요구합니다.

## Generated state

Active TigerKit generated state는 project repository 밖 `~/.tigerkit` 아래의 file-only state입니다. `.claude/tigerkit`는 legacy/migration context로만 남기고 새 runtime write path로 사용하지 않습니다. `/tk:route`와 `/tk:reflect`는 기본적으로 persisted artifact를 만들지 않습니다.

주요 active path:

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json
```

## Legacy state

기존 decline marker는 inactive legacy state로만 보존하며 core command/runtime이 읽거나 쓰지 않습니다.

```text
~/.tigerkit/local/session-start/worktree-context-declines.json
.claude/tigerkit/local/session-start/worktree-context-declines.json
```
