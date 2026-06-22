# TigerKit 운영 사용법

이 문서는 TigerKit command surface 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`, 실행 support set은 `support/execute-support-matrix.json`을 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash, contract field name은 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = gap + loop-spec + execute + reflect
```

- `gap`: SoT와 Current Implementation의 차이를 한 번 분석합니다. evidence-first로 읽고 source conflict나 근거 부족은 `ambiguous`로 남깁니다.
- `loop-spec`: 명시적 task를 read-only worktree scan 기반 `tigerkit.loop-spec/v2` 실행 계약으로 컴파일하거나 검증합니다.
- `execute`: 사용자가 직접 호출한 LoopSpec v2 하나를 bounded execution dispatcher로 검증하고 execution receipt를 저장합니다.
- `reflect`: 세션 result와 persisted execution receipt에서 재사용 가능한 learning을 preview-first promotion result로 분류합니다.

TigerKit은 bounded execution surface를 제공하지만 general autopilot 또는 workflow engine이 아닙니다.

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없으면 먼저 SoT 제공을 제안합니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.
- `/tk:loop-spec`은 source를 수정하지 않습니다.
- `/tk:execute`는 user-only write boundary입니다.
- Legacy LoopSpec은 자동 변환하지 않고 regenerate해야 합니다.
- `/tk:reflect` 기본값은 preview-only입니다.

## Command Surface

| Command | 역할 | 저장 성격 |
|---|---|---|
| `/tk:gap` | SoT와 Current를 비교해 missing, mismatch, overbuilt, ambiguous를 보고합니다. | optional external generated report |
| `/tk:loop-spec` | 명시적 task와 현재 worktree capability를 읽기 전용으로 분석해 LoopSpec v2를 생성하거나 검증합니다. | worktree-scoped generated spec |
| `/tk:execute` | LoopSpec v2 하나를 user-only bounded execution dispatcher로 검증하고 receipt를 저장합니다. | immutable execution receipt |
| `/tk:reflect` | session result, feedback, execution receipt에서 개선 후보를 canonical target으로 분류합니다. | promotion candidates |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:loop-spec "결제 모달 scroll 복구 버그 수정"
/tk:loop-spec validate <spec-id-or-path>
/tk:execute <spec-id-or-path>
/tk:reflect --target repo --apply=false
/tk:reflect --target repo-local --apply=true
```

## Execute model

`/tk:execute`는 아래 순서를 따릅니다.

1. spec ID/path 하나를 resolve합니다.
2. `tigerkit.loop-spec/v2`만 허용합니다.
3. `readiness: complete`와 `executorRecommendation: fast | reasoning`을 요구합니다.
4. stale, legacy, blocked, invalid spec을 reject합니다.
5. current environment key와 runtime binding을 helper가 canonicalize합니다.
6. `support/execute-support-matrix.json`의 matching public entry와 packaged proof를 확인합니다.
7. hard-boundary proof가 없으면 `hard_enforcement_unavailable`로 reject합니다.
8. proof가 있으면 정확히 하나의 executor에 위임합니다.
9. dispatcher가 required verifier를 postflight로 재실행합니다.
10. receipt를 `~/.tigerkit/.../executions/<execution-id>.yaml`에 atomic write합니다.

현재 package는 `hook_gate` boundary component를 포함하지만 public stable execution proof는 support matrix에서 `preview`로 표시됩니다.

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

Active TigerKit generated state는 project repository 밖 `~/.tigerkit` 아래의 file-only state입니다. `.claude/tigerkit`는 legacy/migration context로만 남기고 새 runtime write path로 사용하지 않습니다.

주요 active path:

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/loop-specs/<spec-id>/spec.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/executions/<execution-id>.yaml
~/.tigerkit/capabilities/execute-write-boundary/<plugin-version>/<environment-key>/proof.yaml
```

## Legacy state

기존 decline marker는 inactive legacy state로만 보존하며 core command/runtime이 읽거나 쓰지 않습니다.

```text
~/.tigerkit/local/session-start/worktree-context-declines.json
.claude/tigerkit/local/session-start/worktree-context-declines.json
```
