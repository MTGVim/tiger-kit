---
name: tk-handoff
description: "[user/auto] 진행 중 작업의 검증된 `handoff snapshot`을 작성하거나 기존 `handoff`를 명시적으로 재개합니다. 작업 목표 계약은 `seed.md`, 진행 상태는 `handoff.md`가 소유합니다. 일반 요약이나 평범한 계속하기에는 적용하지 않습니다."
disable-model-invocation: false
argument-hint: "[goal or target] [--output <path>|--resume]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Handoff

Apply this skill to explicit requests to create or resume a `handoff`. Do not auto-apply it to general summaries, status questions, or ordinary “continue” requests.

Keep the roles separate.

- `.tigerkit/seed.md`: the task contract defining what must be done, why, and under which conditions
- `.tigerkit/handoff.md`: the progress `snapshot` recording what has been done and the current state

A `Handoff` neither replaces nor copies the `Seed`.

## New handoff

Read the current repository evidence.

- `branch` / `HEAD` / `worktree`
- the exact `path` and `status` of the current `Seed`, if present
- actual changed files
- commands actually executed
- actual verification results
- completed and remaining work
- current blockers and next action

Mark only observed facts as `verified` and only decisions confirmed with the user as `confirmed`.
Commands not executed, prior claims, and model inferences are `unverified`.

The default path is `.tigerkit/handoff.md`. Write to a temporary file in the same directory, atomically replace the target, and read it back.
Creating the artifact itself does not grant permission to change the product, Git, or remote state.

Preserve at least the following meaning in the Handoff.

```text
Goal/Seed: <seed path 또는 current goal reference>
Status: pending | in_progress | completed | aborted | Blocked
Repository state: <branch, HEAD, worktree>
Decisions: <confirmed progress-relevant decisions>
Changed files: <observed paths | none>
Commands: <actually executed commands | none>
Verification: <check/result/evidence>
Completed work: <done items | none>
Remaining work: <unfinished items | none>
Open questions: <required decisions | none>
Risks: <remaining failure/regression risk>
Next step: <one executable immediate action>
Resume hints: <environment/order/command hints>
Disposition: reported | applied | pending
```

Do not copy the `Seed`’s `goal/scope/AC/implementation guidance` into the `Handoff`.
When needed, reference the exact `Seed` `section/path`.

## 🔴 CHECKPOINT · 🛑 STOP · Write/Resume Boundary

Before writing a new `Handoff` or continuing a `--resume`:

- STOP and report `Unverifiable` when the current `Seed`, `Handoff`, branch, `HEAD`, worktree, or required verification cannot be fresh-read.
- STOP and mark `Blocked` when evidence conflicts or the `Seed` contract has drifted; do not resolve either condition inside the `Handoff`.
- STOP before writing if atomic replacement cannot be completed or readback fails; use `.tigerkit/handoff.md` by default and honor an explicit `--output <path>` exactly.
- STOP at any product, Git, or remote publication approval boundary; the artifact does not grant that permission.
- If none of these conditions applies, continue without asking an extra question for a routine artifact update.

## Resume

`--resume` requests resuming work by comparing the `handoff snapshot` against the current Git and files.

First, fresh-read:

- the current `Seed` and `handoff`
- `branch`/`HEAD`/`worktree`
- changed files
- relevant verification evidence
- current remote state, if a `PR` exists

Then classify drift.

| Classification | Action |
| --- | --- |
| None | Continue from `Next step` without additional questions |
| Nonessential `drift` | Record it and continue |
| Significant progress `drift` | Update the `Handoff` from current evidence and confirm only the necessary decisions |
| `Seed` contract `drift` | Do not resolve it in the `Handoff`; report that re-entering `tk-prep` is required |
| Conflict | Show the incompatible evidence and mark `Blocked` |
| unverified | If the required state cannot be confirmed, mark `Unverifiable` |

`--resume` may authorize continuing the work, but it does not replace approval to change the `Seed`’s `goal/scope/decision/AC` or permission to publish remotely.

## Output

After successfully creating a new `handoff`, show only the path, current status, and next action briefly in chat.
Do not dump the full `Handoff` body or evidence ledger.

When resuming, explain completed work, remaining work, blockers, and the immediate next action in a way that is easy for a person to understand.

Do not use `.tigerkit/` as an archive, current pointer, or global state.
Do not modify `.gitignore` or automatically commit/publish.
