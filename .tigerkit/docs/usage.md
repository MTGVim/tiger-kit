# TigerKit 운영 사용법

이 문서는 TigerKit command surface 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash, contract field name은 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = gap + reflect + loop-spec
```

- `gap`: SoT와 Current Implementation의 차이를 한 번 분석합니다. evidence-first로 읽고, source conflict나 근거 부족은 `ambiguous`로 남깁니다.
- `reflect`: 세션 result와 feedback에서 재사용 가능한 learning을 preview-first promotion result로 분류합니다.
- `loop-spec`: 명시적 task를 read-only worktree scan 기반의 실행 없는 LoopSpec recommendation으로 컴파일하거나 검증합니다.

Core `tk` plugin은 hook-free입니다. Active command surface는 `/tk:gap`, `/tk:reflect`, `/tk:loop-spec`입니다.

## Core guidance

- SoT가 있으면 구현 전에 `/tk:gap`을 먼저 고려합니다.
- SoT가 없으면 먼저 SoT 제공을 제안합니다.
- 사용자가 바로 진행을 원하면 `/tk:gap` 없이 진행할 수 있지만, 그 경우 가정과 불확실성을 명시합니다.
- 의미 있는 작업이 끝나면 `/tk:reflect`를 고려합니다.
- `/tk:reflect` 기본값은 preview-only입니다.

## Command Surface

| Command | 역할 | 저장 성격 |
|---|---|---|
| `/tk:gap` | SoT와 Current를 비교해 missing, mismatch, overbuilt, ambiguous를 보고합니다. | optional external generated report |
| `/tk:reflect` | session result와 feedback에서 개선 후보를 canonical target으로 분류합니다. | promotion candidates |
| `/tk:loop-spec` | 명시적 task와 현재 worktree capability를 읽기 전용으로 분석해 LoopSpec recommendation을 생성하거나 검증합니다. | worktree-scoped generated spec |

## 사용 예시

```text
/tk:gap "PRD와 현재 구현 차이 봐줘" --target src/auth
/tk:reflect --target repo --apply=false
/tk:reflect --target repo-local --apply=true
/tk:loop-spec "결제 모달 scroll 복구 버그 수정"
/tk:loop-spec validate <spec-id-or-path>
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

Write eligibility는 아래를 요구합니다.

- fixed invocation cwd
- discovered git root
- all Git checks via `git -C <git-root>`
- root-relative literal path operand `CLAUDE.local.md`
- reject non-git workspace
- reject tracked local file
- reject not ignored local file
- reject symlink
- reject path outside repo
- reject Git command errors

Apply는 current invocation apply plan, exact apply set, base/result sha256, planned result bytes, exact unified diff, all-or-nothing, stale plan rejection, post-write verification, rollback receipt를 요구합니다.

## Generated state

Active TigerKit generated state는 project repository 밖 `~/.tigerkit` 아래의 file-only state입니다. `.claude/tigerkit`는 legacy/migration context로만 남기고 새 runtime write path로 사용하지 않습니다.

실제 active write helper는 현재 작업 repo 상대경로가 아니라 **설치된 plugin root**를 기준으로 호출합니다.

```bash
python3 "${CLAUDE_PLUGIN_ROOT:?CLAUDE_PLUGIN_ROOT is not set}/scripts/tigerkit_state.py" write-gap --repo-root "$PWD" --report-file /absolute/path/to/final-gap-report.md
```

주요 active path:

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/loop-specs/<spec-id>/spec.yaml
```

## Legacy state

Core `tk` plugin은 active `SessionStart` hook을 제공하지 않습니다. 기존 decline marker는 inactive legacy state로만 보존하며 core command/runtime이 읽거나 쓰지 않습니다.

```text
~/.tigerkit/local/session-start/worktree-context-declines.json
.claude/tigerkit/local/session-start/worktree-context-declines.json
```

이 legacy marker는 자동 삭제하거나 자동 이관하지 않으며 core command/runtime이 읽거나 쓰지 않습니다.
