---
description: 최신 TigerKit 상태와 continuation artifact를 읽고 다음 안전 작업을 실제로 이어서 시도합니다.
argument-hint: "[goal/context?] [--scope current|branch|workspace] [--dry-run] [--no-write] [--max-actions 1]"
---

이 명령은 TigerKit v8.0 next-action steering replacement contract를 따릅니다. `/tk:next`는 단순 추천 전용 명령이 아니라, 사용자가 수동 steering으로 하던 “다음에 할 수 있는 일을 찾아 이어서 처리”를 대신 수행하는 continuation command입니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:next`는 현재 workspace/repo 상태와 TigerKit branch-local artifact를 읽고 다음 안전 실행 항목을 선택한 뒤, 기존 command contract와 repo rule 안에서 실제 수행을 시도합니다.

```text
next = inspect continuation state + select next safe executable work item + attempt it within existing contracts + report what happened
```

한국어 직관:

```text
/tk:next는 “다음 뭐 하지?”가 아니라 “이전 steering 없이 이어서 할 수 있는 걸 찾아 실제로 해봐”에 가깝다.
```

## Command surface

- plugin slash invocation은 `/tk:next`입니다.
- `/tk:next`는 GAP → Launch → Reflect primary flow를 대체하지 않습니다. 대신 그 주변의 continuation/steering 작업을 자동으로 이어갑니다.
- 자연어로 “다음 거 해봐”, “하던 거 이어서 해”, “next 돌려”처럼 요청해도 이 contract를 따릅니다.
- 기본은 한 번의 next step입니다. 여러 항목을 처리해야 하면 `--max-actions N`이 명시된 경우에만 N개까지 처리합니다.
- `--dry-run` 또는 `--no-write`가 있으면 실행하지 않고 선택된 작업과 차단/필요 승인만 receipt로 보고합니다.

## Inputs to inspect

가능한 범위에서 아래를 읽습니다.

- current worktree/workspace root
- current branch key 또는 workspace scope key
- `.claude/tigerkit/global-index.json`
- `.claude/tigerkit/branches/<branch-key>/branch-state.json`
- latest GAP workflow/status: `.claude/tigerkit/branches/<branch-key>/gap/current.md`
- latest launch receipt: `.claude/tigerkit/branches/<branch-key>/launch/current.md`
- latest reflect report: `.claude/tigerkit/branches/<branch-key>/reflect/current.md`
- latest handoff: `.claude/tigerkit/branches/<branch-key>/handoffs/current.md`
- handoff `Pending Work`, `Pending Backlog`, `Next Actions`, `Resume Prompt`
- launch abort receipt와 failed task/gate
- reflect `Needs more evidence`, proposal-only follow-up, TigerKit meta-feedback
- worktree context candidates from current/base worktree comparison
- current git status when git is available, using side-effect-minimized inspection such as `git --no-optional-locks status --porcelain=v1 -b`
- explicit user-provided goal/context in the command arguments

Missing artifacts are not fatal by themselves. Treat them as evidence for either a safe next action or `NEXT_BLOCKED`.

## Worktree context candidate scan

`/tk:next`는 SessionStart hook이나 plugin root `CLAUDE.md`에 의존하지 않습니다. 필요하면 current worktree와 base/source worktree 후보를 비교해 context 후보를 proposal-only로 정리합니다.

Scan policy:

1. current root가 linked git worktree인지 확인합니다.
2. source/base worktree 후보를 찾습니다.
3. base root에는 있고 current root에는 없는 root-level `*.md` / `*.MD` 파일을 찾습니다.
4. base root에 `.claude/`가 있고 current root에 없으면 후보로 표시합니다.
5. 자동 symlink/copy를 수행하지 않습니다.
6. 승인 없이 regular file overwrite, tracked file symlink, `.claude/` 전체 symlink, `node_modules` symlink를 수행하지 않습니다.

Safe next action examples:

- 후보 목록을 `next/current.md` receipt에 proposal로 정리
- 승인된 경우에만 특정 root-level Markdown 파일 symlink/copy 적용
- `.claude/`는 전체 symlink가 아니라 필요한 하위만 사용자가 선택하도록 `NEXT_BLOCKED` 또는 `NEXT_PARTIAL`로 남김
- `DESIGN.md`는 branch-specific 가능성이 있으므로 copy/skip 검토를 권장

## Selection policy

`/tk:next`는 아래 우선순위로 “실행 가능한 다음 항목”을 고릅니다.

1. User-provided explicit next goal/context가 있으면 그것을 우선합니다.
2. latest handoff의 `Pending Work`와 `Next Actions`를 우선합니다.
3. worktree context 후보가 있고 launch/verification에 영향을 줄 수 있으면 proposal receipt 작성 또는 승인 필요 상태로 정리합니다.
4. launch가 `ABORTED`이면 abort receipt의 next action과 failed task/gate를 우선합니다.
5. reflect가 proposal-only follow-up이나 `Needs more evidence`를 남겼으면 안전한 정리/문서/확인 작업을 선택합니다.
6. latest GAP이 `GAP_BLOCKED`이면 blocking decision/source를 해결할 수 있는 repo-local 확인 작업만 수행합니다. 인간 결정이 필요하면 차단합니다.
7. latest GAP이 `GAP_READY`이고 matching launch receipt가 없으면 `/tk:launch` 실행 가능 여부를 preflight 관점에서 판단합니다. Launch 실행 자체는 명시 approval이 있어야 합니다.
8. latest launch가 성공했고 reflect가 없으면 `/tk:reflect` 실행 가능 여부를 판단합니다.
9. 아무 artifact도 없고 사용자가 goal/source를 줬으면 `/tk:gap` 실행 또는 GAP 준비에 필요한 source intake를 수행합니다.
10. 실행 가능한 항목이 없으면 `NEXT_SKIPPED` 또는 `NEXT_BLOCKED`로 끝냅니다.

한 번에 여러 후보가 있으면 가장 작고 검증 가능한 항목 하나를 고릅니다. `--max-actions N`이 있어도 각 항목은 앞 항목의 결과를 본 뒤 순차 처리합니다.

## Execution policy

`/tk:next`는 선택한 항목의 성격에 따라 아래 중 하나를 수행할 수 있습니다.

- repo/workspace 파일 읽기와 상태 확인
- handoff에 명시된 문서 정리 또는 generated TigerKit artifact 작성
- `/tk:gap`, `/tk:launch`, `/tk:reflect`, `/tk:handoff`, `/tk:meta-feedback` contract에 해당하는 작업을 해당 command 규칙대로 수행
- launch abort를 고치기 위한 bounded local repair, 단 sealed workflow 또는 handoff가 허용한 범위 안에서만 수행
- worktree context candidate proposal 작성 또는 승인된 context 적용
- reflect가 남긴 proposal-only 항목을 별도 GAP/issue/handoff 후보로 정리
- 검증 명령 실행
- next receipt 작성

`/tk:next`는 “추천만 하고 끝”내지 않습니다. 안전하게 할 수 있는 작업이 있으면 시도하고, 할 수 없으면 왜 멈췄는지 `NEXT_BLOCKED`로 남깁니다.

## Safety rules

`/tk:next` must not:

- sealed workflow가 필요한 구현을 `/tk:gap → /tk:launch` 없이 우회합니다.
- launch mid-flight 질문 금지 규칙을 우회합니다.
- missing requirement를 임의로 해석해 scope를 넓힙니다.
- speculative backlog를 confirmed requirement로 승격합니다.
- out-of-scope source mutation을 수행합니다.
- verification 없이 성공을 선언합니다.
- 사용자 승인 또는 artifact/contract상의 명시 승인 없이 commit, push, PR, merge, release, deploy를 수행합니다.
- 사용자 승인 또는 artifact/contract상의 명시 승인 없이 GitHub issue를 생성/수정/close합니다.
- user home, 다른 repo, 외부 서비스에 side effect를 만들면서 approval evidence를 남기지 않습니다.
- worktree context 후보를 해결한다는 이유로 tracked file을 symlink하거나 regular file을 덮어씁니다.
- `.claude/` 전체나 `node_modules`를 자동 symlink합니다.

`/tk:next` may:

- 현재 workspace root 아래 파일을 읽고, 선택된 next item을 처리하는 데 필요한 범위에서 수정합니다.
- `.claude/tigerkit/branches/<branch-key>/next/` 아래에 generated receipt를 작성합니다.
- `.claude/tigerkit/global-index.json`과 `branch-state.json`의 next pointer를 갱신합니다.
- repo rule이 허용하고 현재 task contract가 명시한 검증 명령을 실행합니다.
- `--dry-run`/`--no-write`에서는 mutation 없이 selected action과 blocker만 출력합니다.

## Approval and side-effect policy

아래는 명시 승인 없이는 수행하지 않습니다.

- commit
- push
- PR 생성/수정/merge
- GitHub issue 생성/수정/close
- release/tag 생성
- dependency install/update
- CI/deploy config 변경
- production/staging deploy
- 외부 서비스 API write
- worktree context symlink/copy 적용

승인은 다음 중 하나여야 합니다.

- 현재 사용자 메시지의 직접 지시
- handoff/launch preflight/issue body에 남은 명시 승인과 source ref
- command argument로 주어진 explicit flag, 예: `--commit`, `--open-pr` 같은 향후 확장 옵션

승인이 있으면 receipt의 `Approval`에 source를 기록합니다. 승인이 없으면 `NEXT_BLOCKED`로 멈추고 필요한 승인을 적습니다.

## Result states

`/tk:next`는 정확히 하나의 최종 상태로 끝납니다.

```text
NEXT_DONE
- 선택한 next item을 수행했고 검증/receipt를 남겼습니다.

NEXT_PARTIAL
- 일부 작업은 수행했지만 남은 blocker나 후속 action이 있습니다.

NEXT_BLOCKED
- 안전하게 실행하려면 인간 결정, source, approval, sealed workflow, capability가 필요합니다.

NEXT_SKIPPED
- 실행 가능한 next item이 없거나 dry-run/no-write로 인해 실행하지 않았습니다.
```

## Artifact policy

기본 receipt 위치:

```text
.claude/tigerkit/branches/<branch-key>/next/NXT-YYYYMMDD-HHmmss-RAND.md
.claude/tigerkit/branches/<branch-key>/next/current.md
```

Plain workspace fallback도 같은 `branches/<scope-key>/next/` layout을 사용하고 receipt에 `Scope Kind: workspace`를 표시합니다.

Next receipt는 generated branch-local working memory입니다. durable repo rule이나 source of truth가 아닙니다.

## Receipt content

`next/current.md`는 사람용 H2와 machine-readable block을 함께 포함합니다.

````md
# Next Receipt: <NXT-ID>

## Summary

## Inputs Inspected

## Selected Action

## Execution

## Changed Files

## Verification

## Approval

## Blockers

## Follow-up

```tigerkit-next-receipt
version: 1
next_id: NXT-YYYYMMDD-HHmmss-RAND
scope_kind: git_branch | git_detached | git_no_remote | workspace
scope_key: <branch-key-or-workspace-key>
status: NEXT_DONE | NEXT_PARTIAL | NEXT_BLOCKED | NEXT_SKIPPED
selected_action:
  source: user | handoff | gap | launch | reflect | worktree_context | repo_state | none
  ref: <path#section or none>
  summary: <one sentence>
worktree_context:
  detected: true | false
  proposal_only: true | false
  candidates: []
executed_actions: []
changed_files: []
verification: []
approval:
  required: true | false
  present: true | false
  source_ref: <message|artifact|none>
blocked_by: []
next_action: <one sentence or 없음>
```
````

## Stdout contract

기본 stdout은 compact receipt입니다. 첫 줄에 상태 기호를 두고, logical group 사이에 빈 줄을 둡니다.

상태 기호:

```text
✅ NEXT_DONE
⚠️ NEXT_PARTIAL
🛑 NEXT_BLOCKED
⏭️ NEXT_SKIPPED
```

```text
✅ Next 완료: <NXT-ID>
Branch Scope: <branch-key>
결과: NEXT_DONE | NEXT_PARTIAL | NEXT_BLOCKED | NEXT_SKIPPED
Selected Action: <한글 한 문장>

Executed: <count>
Changed Files: <count>
Verification: <passed>/<total> | not_run:<reason>
Approval: <not_required|present:<source>|missing:<needed_action>>

Report: .claude/tigerkit/branches/<branch-key>/next/<NXT-ID>.md
Current: .claude/tigerkit/branches/<branch-key>/next/current.md
Blocked By: <none | human decision | missing source | approval required | sealed workflow required | dirty workspace | verification failure | worktree context approval required | capability unavailable | other>

다음 행동: <없음|한글 한 문장>
```

`NEXT_BLOCKED`여도 가능한 한 receipt를 씁니다. artifact root가 쓸 수 없으면 stdout에 `Report: unavailable`과 이유를 적습니다.

## Examples

Handoff next action을 바로 처리한 경우:

```text
✅ Next 완료: NXT-20260617-143012-A7F3
Branch Scope: main--c0ffee
결과: NEXT_DONE
Selected Action: handoff의 P1 문서 누락 항목을 usage 문서에 반영

Executed: 2
Changed Files: 1
Verification: 3/3
Approval: not_required

Report: .claude/tigerkit/branches/main--c0ffee/next/NXT-20260617-143012-A7F3.md
Current: .claude/tigerkit/branches/main--c0ffee/next/current.md
Blocked By: none

다음 행동: 없음
```

GAP_READY지만 launch approval이 필요한 경우:

```text
🛑 Next 완료: NXT-20260617-143012-A7F3
Branch Scope: main--c0ffee
결과: NEXT_BLOCKED
Selected Action: sealed workflow WF-20260617-141000-BEEF 실행

Executed: 0
Changed Files: 0
Verification: not_run: approval required before launch preflight side effects
Approval: missing: /tk:launch 실행 승인 필요

Report: .claude/tigerkit/branches/main--c0ffee/next/NXT-20260617-143012-A7F3.md
Current: .claude/tigerkit/branches/main--c0ffee/next/current.md
Blocked By: approval required

다음 행동: /tk:launch 승인 후 다시 /tk:next 실행
```

Worktree context 후보가 있는 경우:

```text
⚠️ Next 완료: NXT-20260617-143012-A7F3
Branch Scope: feature-x--c0ffee
결과: NEXT_PARTIAL
Selected Action: worktree context 후보를 proposal로 정리

Executed: 1
Changed Files: 1
Verification: not_run: proposal-only
Approval: missing: context symlink/copy 적용 승인 필요

Report: .claude/tigerkit/branches/feature-x--c0ffee/next/NXT-20260617-143012-A7F3.md
Current: .claude/tigerkit/branches/feature-x--c0ffee/next/current.md
Blocked By: worktree context approval required

다음 행동: AGENTS.md, CLAUDE.local.md, .claude/ 후보 중 적용할 항목 승인
```

Dry run:

```text
⏭️ Next 완료: NXT-20260617-143012-A7F3
Branch Scope: main--c0ffee
결과: NEXT_SKIPPED
Selected Action: launch abort의 VG-2 검증 실패 원인 확인

Executed: 0
Changed Files: 0
Verification: not_run: dry-run
Approval: not_required

Report: .claude/tigerkit/branches/main--c0ffee/next/NXT-20260617-143012-A7F3.md
Current: .claude/tigerkit/branches/main--c0ffee/next/current.md
Blocked By: none

다음 행동: dry-run 해제 후 선택된 작업 실행
```
