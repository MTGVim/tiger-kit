# TigerKit branch-local storage contract

이 문서는 TigerKit v8.0 branch/workspace-local working memory의 저장 위치, scope key, index, write safety, gap/launch/handoff/reflect 경계를 설명합니다. 산출물 전체 구조는 `.tigerkit/docs/artifact-layout.md`, command stdout 계약은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

## 기본 저장 위치

TigerKit branch-local working memory는 반드시 current worktree root 아래에 저장합니다.

```text
.claude/tigerkit/branches/<branch-key>/
```

Legacy Spec Patch 입력 위치:

```text
.claude/tigerkit/branches/<branch-key>/specs/
```

v8 MVP는 `/tk:spec` command를 공개하지 않습니다. 이 경로는 v7/v7.1에서 생성된 branch-local Spec Patch를 `/tk:gap` source material 후보로 읽기 위한 legacy 위치입니다.

Sealed workflow 기본 위치:

```text
.claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
.claude/tigerkit/branches/<branch-key>/gap/current.md
```

Launch run 기본 위치:

```text
.claude/tigerkit/branches/<branch-key>/launch/<LCH-ID>.md
.claude/tigerkit/branches/<branch-key>/launch/current.md
```

Gap Review compatibility 기본 위치:

```text
.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/
```

Handoff canonical 위치:

```text
.claude/tigerkit/branches/<branch-key>/handoffs/current.md
```

금지 저장 위치:

- `$GIT_COMMON_DIR/.claude/tigerkit`
- `.git/worktrees/*`
- user home global path
- `/tmp`
- current worktree root 밖 경로

`.claude/tigerkit/`은 generated branch/workspace-local working memory이며 repo-wide durable knowledge가 아닙니다.

## Scope key

브랜치명이나 workspace path를 디렉터리명으로 직접 쓰지 않습니다.

Normal branch:

1. `worktreeRoot = git rev-parse --show-toplevel`
2. `branchName = git symbolic-ref --quiet --short HEAD`
3. `fullRefName = refs/heads/<branchName>`
4. branch slug는 `/`, `\`, 공백, `:`, `*`, `?`, `"`, `<`, `>`, `|`를 `-`로 바꾸고 연속 `-`를 하나로 줄입니다.
5. 앞뒤 `-`를 제거하고 빈 값이면 `unknown`을 씁니다.
6. `shortHash = sha256(fullRefName).slice(0, 6)`
7. `branchKey = <branch-slug>--<shortHash>`

Detached HEAD:

```text
branchKey = detached-<shortHeadSha7>--<sha256(worktreeRoot).slice(0, 6)>
```

Detached 상태면 summary에 branch scope가 detached임을 알립니다.

Plain workspace fallback:

```text
scopeKind = workspace
scopeKey = workspace-<basename-slug>--<sha256(absWorkspaceRoot).slice(0, 8)>
```

`git rev-parse --show-toplevel`이 실패하면 current working directory를 `workspaceRoot`로 사용합니다. basename slug가 비거나 안전하지 않으면 `workspace--<hash>`를 씁니다. stdout과 machine-readable receipt에는 `Scope Kind: workspace`를 함께 표시합니다.

## Index files

기본적으로 아래 파일을 atomic write로 갱신합니다.

```text
.claude/tigerkit/branches/<branch-key>/branch-state.json
.claude/tigerkit/global-index.json
```

`branch-state.json`에는 최신 workflow, launch, reflect, handoff pointer를 기록할 수 있습니다. `global-index.json`에는 branch `lastUsedAt`과 최신 handoff pointer를 기록합니다. branch entry가 없으면 저장 또는 apply를 수행하는 command가 현재 branch 정보로 새 entry를 생성할 수 있습니다.

Legacy `.claude/tigerkit/branches/<branch-key>/specs/index.json`이 있으면 `/tk:gap`은 source material discovery에 사용할 수 있지만 v8 MVP command가 새 Spec Patch index를 생성해야 하는 것은 아닙니다.

## Lock and write safety

branch scope 작업 전 `.claude/tigerkit/branches/<branch-key>/.lock`을 exclusive create로 획득합니다.

- lock 내용에는 `pid`, `command`, `createdAt`을 기록합니다.
- 30분 미만 lock이 있으면 중단합니다.
- 30분 이상 lock은 stale warning 후 제거할 수 있습니다.
- `TIGERKIT_FORCE_LOCK=1`이면 즉시 override할 수 있습니다.

Atomic write 대상:

- `branch-state.json`
- `global-index.json`

절차:

1. `target.tmp.<pid>.<rand>`에 씁니다.
2. 가능하면 fsync합니다.
3. rename으로 target을 교체합니다.
4. 실패 시 tmp 파일을 삭제합니다.

## Path safety

TigerKit generated artifact 경로는 normalize 후 current worktree/workspace root 내부이면서 `.claude/tigerkit/branches/<scope-key>/` 아래여야 합니다. worktree root 밖이면 중단하고 아래 메시지를 사용합니다.

```text
Tiger Kit does not read or write files outside the current worktree by default.
```

## `/tk:gap` branch-local storage

기본 `/tk:gap`은 v8 sealed workflow builder입니다. `GAP_READY`이면 `.claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md` archive와 `gap/current.md` copy를 쓰고, `GAP_BLOCKED`이면 `.claude/tigerkit/branches/<branch-key>/gap/<GAP-ID>.md` blocked report를 쓰며 launch workflow block은 쓰지 않습니다.

`/tk:gap --review` compatibility mode만 v7 review layout인 `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md`와 `run.json`을 씁니다.

상세 artifact layout은 `.tigerkit/docs/artifact-layout.md`를 기준으로 합니다. 상세 stdout/report 계약은 `.tigerkit/docs/output-contract.md`를 기준으로 합니다.

`.claude/tigerkit/`은 generated branch/workspace-local working memory이며 repo-wide durable knowledge가 아닙니다.

## `/tk:gap` sealed workflow storage

기본 `/tk:gap`은 launch 가능 여부에 따라 아래 중 하나를 저장합니다.

```text
.claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md
.claude/tigerkit/branches/<branch-key>/gap/current.md
.claude/tigerkit/branches/<branch-key>/gap/<GAP-ID>.md
```

- `GAP_READY`이면 task별 `assumed_preconditions`와 봉인 전 `readonly_preflight` 결과를 포함한 sealed workflow archive와 `current.md` copy를 씁니다.
- `GAP_BLOCKED`이면 blocked report만 쓰고 `tigerkit-launch-workflow` block은 쓰지 않습니다.
- `branch-state.json`에는 `lastWorkflowId`, `lastWorkflowPath`, `lastWorkflowHash`, `lastGapStatus`를 기록할 수 있습니다.

## Worktree context proposal local context

TigerKit은 Claude Code `SessionStart` hook으로 worktree context를 세션 시작 시 한 번 read-only 점검합니다. Hook은 symlink/copy/hydration을 수행하지 않고 `TIGERKIT_SESSION_START` additional context만 주입합니다. `/tk:gap`은 이를 source grounding에 반영하고, `/tk:launch`와 `/tk:next`는 command마다 다시 묻지 않고 session context 또는 matching decline marker를 소비합니다.

Proposal safety contract:

- current worktree root 밖에는 쓰지 않습니다.
- `$GIT_COMMON_DIR`, `.git/worktrees/*`, user home, `/tmp`에는 쓰지 않습니다.
- target regular file과 different symlink를 덮어쓰지 않습니다.
- tracked file/directory는 기본적으로 symlink하지 않습니다.
- `.claude/` 전체 symlink와 `node_modules` symlink는 금지합니다.
- source worktree를 수정하지 않습니다.
- proposal 자체는 abort 사유가 아니지만, workflow가 context 적용을 required precondition으로 두고 승인/evidence가 없으면 `WORKTREE_CONTEXT_APPROVAL_REQUIRED`로 task 실행 전 중단합니다.
- 사용자가 같은 candidate signature를 거절하면 `.claude/tigerkit/local/session-start/worktree-context-declines.json`에 기록해 다시 묻지 않을 수 있습니다.

## `/tk:launch` branch-local context

`/tk:launch`는 실행 또는 abort 결과를 아래에 저장합니다.

```text
.claude/tigerkit/branches/<branch-key>/launch/<LCH-ID>.md
.claude/tigerkit/branches/<branch-key>/launch/current.md
.claude/tigerkit/branches/<branch-key>/reflect/<RFL-ID>.md
.claude/tigerkit/branches/<branch-key>/reflect/current.md
```

- launch run은 workflow hash, runtime harness, worktree context proposal status, task/precondition/gate 결과, abort code, commit decision을 기록합니다.
- `HUMAN_DECISION_REQUIRED` 또는 `VERIFICATION_FAILED` abort는 다음 `/tk:gap`이 입력으로 소비할 수 있는 structured feedback fact를 기록합니다.
- reflect archive와 `reflect/current.md`는 generated branch-local trace이며 durable apply가 아닙니다.
- `branch-state.json`에는 `lastLaunchId`, `lastLaunchPath`, `lastLaunchStatus`, `lastReflectId`, `lastReflectPath`를 기록할 수 있습니다.

## `/tk:handoff` branch-local context

`archive=true` 또는 사용자의 명시 archive 요청이 있으면 branch-local dated copy도 함께 생성합니다.

예:

```text
.claude/tigerkit/branches/<branch-key>/handoffs/2026-06-03-tigerkit-v7-gap.md
```

`.claude/tigerkit/global-index.json`의 current branch entry에는 `latestHandoffPath`와 `lastHandoffAt`을 기록합니다. 경로를 지정하지 않은 resume 지시는 이 index pointer를 1순위로 조회합니다.

`.claude/tigerkit/branches/<branch-key>/branch-state.json`에도 `latestHandoffPath`와 `lastHandoffAt`을 기록할 수 있습니다.

`.claude/handoffs/current.md`는 optional convenience pointer입니다. 생성하더라도 canonical handoff를 대체하지 않습니다.

`archive=true` 또는 사용자의 명시 요청이 없으면 dated archive를 만들지 않습니다.

최신 branch-local TigerKit artifact가 관측되면 handoff에 참조할 수 있습니다.

- legacy Spec Patch source material: `.claude/tigerkit/branches/<branch-key>/specs/SP-*.md`
- 최신 Gap Workflow: `.claude/tigerkit/branches/<branch-key>/gap/current.md`
- 최신 Gap Review: `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md`
- branch state: `.claude/tigerkit/branches/<branch-key>/branch-state.json`

handoff는 branch-local artifact 자체를 durable rule로 승격하지 않습니다. 다음 작업자가 읽을 continuation 요약만 작성합니다.

## `/tk:handoff` classification rule

항상 아래 분류를 구분합니다.

```text
Fact = directly observed
Decision = confirmed by user or source contract
Interpretation = inferred from fact
Unknown = not verified
Risk = possible failure mode
```

- 직접 확인한 사항만 `Fact`로 기록합니다.
- 사용자 또는 source contract가 확정한 사항만 `Decision`으로 기록합니다.
- 관찰한 사실에서 추론한 내용은 `Interpretation`으로 기록합니다.
- 확인하지 못한 내용은 `Unknown`으로 둡니다.
- 가능한 실패 모드나 주의점은 `Risk`로 기록합니다.

## `/tk:reflect` branch-local input/output preconditions

Reflect는 current branch scope의 branch-local working memory를 읽습니다.

```text
.claude/tigerkit/branches/<branch-key>/specs/  # legacy source material only
.claude/tigerkit/branches/<branch-key>/gap/
.claude/tigerkit/branches/<branch-key>/launch/
.claude/tigerkit/branches/<branch-key>/reflect/
.claude/tigerkit/branches/<branch-key>/runs/gap/  # only /tk:gap --review
.claude/tigerkit/branches/<branch-key>/branch-state.json
```

읽을 수 있는 evidence class:

- active/superseded Spec Patch metadata와 confirmed item
- accepted gap finding pattern
- rejected/downgraded observation reason
- source conflict와 resolution 상태
- 사용자 대화에서 명시적으로 확인된 TigerKit 운영 규칙
- current code/worktree context needed to classify repo-wide value

branch-local specs/gap 산출물이 없으면 산출물 기반 후보는 없는 것으로 처리합니다. 사용자 대화에서 명시적으로 확인된 TigerKit 운영 규칙은 후보가 될 수 있지만, 반복 관측 패턴이나 실행자 해석만으로 repo-wide durable insight를 만들지 않습니다.

Reflect는 branch-local working memory를 repo-wide durable knowledge 후보로 분류할 수 있지만, source code를 수정하지 않습니다.
