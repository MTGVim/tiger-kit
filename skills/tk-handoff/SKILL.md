---
name: tk-handoff
description: "[user/auto] 현재 세션 현황을 짧게 확인하거나, 다른 세션에 인계할 자료를 만들거나 기존 인수인계를 명시적으로 재개할 때 사용합니다. 일반 문서 요약이나 평범한 계속하기에는 적용하지 않습니다."
disable-model-invocation: false
argument-hint: "[current status | goal or target] [--output <path>|--resume]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Handoff

## Shared References

Read branch-triggered criteria from the current installed owners. A missing/mismatched
owner or resource blocks that action: use `tk-setup-skills`, not memory, another installation
or unapproved installs. Reading grants no workflow or mutation authority.

- For a user-owned decision, missing approval or unmet prerequisite, read [question rounds](../tk-questioning/references/questions.md).
- Before a user-facing completion report, artifact-path handoff or multi-attribute chat comparison, read [chat delivery](../tk-writing/references/delivery.md). The task's specific output contract wins.

## UI Evidence

Keep existing UI literals exact, including language/case/punctuation/spacing, separate from
proposed copy. Require target/environment/locale/role-matched evidence for each navigation
label and connection; a title/route/identifier alone proves no entry path. Preserve conflicting provenance.
Report every required
unsupported label/hop with available provenance, limitation and smallest missing input; never
present it as navigation. User-supplied text is not independently observed and resolves only its supported claim.

Before collecting/verifying UI evidence within this owner's investigation scope, read
[UI evidence collection](../tk-ui-evidence/references/ui-evidence.md). Non-UI and propagation-only
branches skip collection; carry supplied evidence/gaps without starting a new investigation.

## Approval Continuity

Reuse active same-task approval across turns and child phases (including baseline/after); continue only its authorized
work through existing owners. Return child/baseline evidence and resume approved owner work;
a phase status is not completion. Ask only for a new material decision, changed scope/authority
or missing user-only input. Invocation and recovered artifacts grant no authority. Remote and
destructive actions need explicit action/target approval, never inferred from local approval.

Select one branch from the request. For a current-session status/orientation request, read
[conversation-only orientation](references/orientation.md), return its compact recap and end
that turn without writing artifacts or resuming work. This reporting boundary does not revoke
prior approval; a later resume instruction may reuse it. For explicit handoff creation, continue the artifact workflow below. For `--resume`,
read [resume and drift classification](references/resume.md) after the write/resume
checkpoint and verify fresh state before continuing. General document summaries and ordinary
“continue” requests do not select either branch. Do not create a durable handoff for a status
recap or query other sessions/remote PRs to fill it.

Keep the roles separate.

- `.tigerkit/seed.md`: the task contract defining what must be done, why, and under which conditions
- `.tigerkit/handoff.md`: the progress `snapshot` recording what has been done and the current state

When a current task Seed exists, reference it rather than copying its contract. A legitimate direct/no-Seed task needs no Seed creation: put its minimal goal, scope/exclusions, AC and confirmed approval boundary in the Handoff itself so another session can understand it.

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
Status: pending | in_progress | completed | aborted | Blocked | Unverifiable
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

`Disposition` describes the work recorded by this handoff: `reported` for investigation/report-only work,
`applied` for authorized changes already made, and `pending` for an unapplied proposal. It grants no authority.

For a task with a Seed, reference the exact contract section/path. For direct/no-Seed, record the minimal self-contained contract above and explicitly identify `Seed: none`; exclude unrelated or ambiguous old Seeds.

## 🔴 CHECKPOINT · 🛑 STOP · Write/Resume Boundary

Before writing a new `Handoff` or continuing a `--resume`:

- Fresh-read branch, HEAD, worktree and required evidence. A new Handoff need not already exist; an optional Seed may legitimately be absent. For resume, the referenced Handoff and any task-bound Seed must be readable. Missing or unreadable required artifacts are `Unverifiable`, not permission to reconstruct them from guesses.
- STOP and mark `Blocked` when evidence conflicts or the `Seed` contract has drifted; do not resolve either condition inside the `Handoff`.
- STOP before writing if atomic replacement cannot be completed or readback fails; use `.tigerkit/handoff.md` by default and honor an explicit `--output <path>` exactly.
- STOP at any product, Git, or remote publication approval boundary; the artifact does not grant that permission.
- If none of these conditions applies, continue without asking an extra question for a routine artifact update.

## Output

After successfully creating a new `handoff`, show only the path, current status, and next action briefly in chat.
Do not dump the full `Handoff` body or evidence ledger.

When resuming, explain completed work, remaining work, blockers, and the immediate next action in a way that is easy for a person to understand.

Do not use `.tigerkit/` as an archive, current pointer, or global state.
Limit ignore edits to Artifact Paths setup; do not automatically commit/publish.

## Artifact Paths

Before authorized artifact writes, checkout/transport/ignore setup or temporary-input consumption,
read [artifact paths](../tk-artifacts/references/artifact-paths.md). Use safe owned nonsymlink paths
and proven Git exclusion for repository scratch; failed checks stop that file branch. Preserve
explicit final destinations and owner-specific defaults. Prefilled input is not completed input.
Cleanup targets only recorded literal resolved absolute run-owned paths, never cwd-relative paths or globs.
