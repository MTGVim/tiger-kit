---
name: tk-merge-conflict
description: "[user/auto] 의도 증거를 바탕으로 활성 `merge`, `rebase`, `cherry-pick`, `revert` 충돌을 해결하고 작업을 완료합니다. 활성 충돌이 없는 일반 파일 수정에는 적용하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Resolve Merge Conflicts

Apply only during an active `merge`, `rebase`, `cherry-pick`, or `revert` with conflicts.
Never apply to ordinary edits or operations that have not started.

## Contract

Before editing, inspect the operation state, `git status`, unmerged index entries, all
conflict markers, and both primary sources. If the operation goal and primary sources
do not determine intent, never guess; stop as `Blocked`. If required state or evidence
cannot be read, the result is `Unverifiable`.

First, check only for an active operation marker and unmerged index entries. If neither
exists, report `Blocked: no active conflict` once and stop without inspecting sources,
markers, or checks.

Use `Pass` only after confirming every completion signal in the command evidence.
Editing only the conflicted files is incomplete.

## 🔴 Checkpoint · 🛑 Stop · Resolve/Continue Boundary

Never `finalize`, `stage`, `continue`, or `abort` before proving the operation state,
all conflict hunks, both primary sources, and the basis for the resolution. Without
that basis, the result is `Blocked`. If the evidence requires choosing between
incompatible requirements, record the tradeoff and continue.

## Workflow

1. `operation state`: Identify the active operation's `kind`/`state`.
2. `conflict inventory`: List conflict paths/hunks and unmerged index entries.
3. `intent evidence`: Map each hunk and both primary sources to intent/evidence.
4. `resolution`: Edit only conflict files whose hunks are supported by evidence.
5. `stage and verify`: Prove markers and unmerged entries are gone, stage the exact
   paths, and run relevant verification.
6. `continue`: Run the operation-specific continue command and record the result.
7. `receipt`: Return `Pass | Fail | Blocked | Unverifiable`, unverified items, and
   references to the `operation`/`verification`/`follow-up` sections without copying them.

## Resolution `receipt` · Single Evidence Record

모든 해결 실행은 아래 하나의 `receipt`로 남깁니다. 이는 별도 결과 섹션이
아니라 `Operation` → `Resolution` → `Verification` → `Follow-up` 보고의 단일
증거 기록입니다. 알 수 없는 값은 `unavailable` 또는 `not run` 으로 적고
추측하지 않습니다.

```text
Operation: <merge | rebase | cherry-pick | revert> / <state + step>
Repository HEAD: <commit>
Conflict paths: <path list | none>
Index / markers: <unmerged count, marker count>
Intent basis: <source refs and hunk mapping | unavailable>
Resolution: <Path | Intent | Result rows>
Staged: <exact paths | none>
Verification: <checks and result | Unverifiable>
Continue: <exact continue command and result | not run>
Follow-up: <remaining work | none>
Status: Pass | Fail | Blocked | Unverifiable
```

Never proceed without the required preceding output. If new conflicts appear, restart
from `conflict inventory`.

Before analyzing intent, map index `stage` 1/2/3 to the actual base, current commit, and
operation target/replayed commit, and record commit IDs/paths. Especially for
`rebase`/`cherry-pick`/`revert`, never infer the user's branch or desired behavior from
`ours`/`theirs` alone; use operation metadata and actual commit contents.

### Command Evidence

| Evidence | Command contract | Completion signal | Failure path |
|---|---|---|---|
| Operation state | Check `MERGE_HEAD`, `rebase-merge`, `rebase-apply`, `CHERRY_PICK_HEAD`, and `REVERT_HEAD` via `git rev-parse --git-path`, then inspect only resolved paths. | Exactly one active operation kind and step match the status/worktree metadata. | Conflicting or unreadable markers are `Unverifiable`; do not infer from `.git/` paths. |
| Operation/index | Inspect `git status --short --branch`, `git diff --name-only --diff-filter=U`, and `git ls-files -u` together. | Kind, step, and HEAD match the freshness anchor, with no unreviewed paths. | Rebuild the inventory; unexplained state is `Unverifiable`. |
| Markers | Search every tracked conflict path for `^(<<<<<<<|=======|>>>>>>>)`. | Marker count is zero. | Remaining paths/hunks are `Fail`; do not continue. |
| Staging | Run `git add -- <supported-path...>`, then recheck the `staged diff` and unmerged index. | Only evidence-supported paths are staged, and unmerged entries are zero. | Staging failure or remaining entries are `Fail`; do not continue. |
| Verification | Run relevant tests, builds, and static checks. | Record commands, results, and scope, with no change-related failures. | If unavailable, `Unverifiable`; if failed, `Fail`. |
| Continue | Run exactly one matching `git merge --continue`, `git rebase --continue`, `git cherry-pick --continue`, or `git revert --continue`. | The operation finishes as intended without new conflicts. | Record the failure/new inventory and restart. |

### Operation Freshness Gate

From the first inventory, pin the operation kind, HEAD, Git-provided step/target,
unmerged paths, and existing `staged` paths. Stage only paths included in the resolution
evidence. Add new paths only after the inventory records their reason and intent basis.

Before verification/continue, reread metadata, HEAD, status, and index. If the operation
disappears, its kind/step/HEAD changes, or unreviewed unmerged/`staged` content appears,
the prior resolution is stale. Rebuild the inventory, evidence, and verification.
Unknown drift is `Unverifiable`; do not claim that a disappeared operation was completed
by this run.

Primary sources include commit messages, `issue`/`PR`, `spec`/`ticket`, adjacent tests,
and established branch behavior. Preserve both intents when compatible. Otherwise,
choose based on the operation goal/evidence, report the tradeoff, and do not invent new
behavior.

An explicit conflict-resolution request authorizes completing the active operation, but
does not automatically authorize `abort`, `reset --hard`, `clean`, force `push`, ordinary
`push`, unsupported bulk deletion, or unrelated formatting changes.

## Completion Report

비어 있지 않은 섹션만 `Operation`, `Resolution`, `Verification`, `Follow-up` 순서로
사용합니다. `Operation` 은 `kind`, `state`, `stage`, `status`, 미검증 항목, `reference`,
`continue` 결과를 소유하고, `Resolution` 은 충돌, 의도, 선택 결과를 소유하며,
`Verification` 은 테스트·표식·인덱스 검사를 소유합니다. `Follow-up`에는 남은
작업만 적습니다. 원격 반영에는 별도 요청이 필요합니다.

해결한 충돌 경로가 여러 개면 `Resolution` 을 간결한 `Path | Intent | Result`
표로 표시하고, 사용자에게 중요한 행이 하나면 문장으로 씁니다. 해결 결과부터
시작하며 해결 행을 반복하거나 메타데이터를 덧붙이지 않습니다. 복합 의도, 해결한
경로 묶음, 검증을 2~5개의 짧은 행/글머리표로 요약합니다. 경로가 8개 이상이면
상위 5~7개의 의도/결과 행으로 묶고 정확한 나머지 경로를 인용합니다. 할당량이
아니라 예산을 사용합니다.
