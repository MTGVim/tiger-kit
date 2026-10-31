---
name: tk-adhd
description: "[user/auto] 답변과 작업 결과에서 핵심·실행할 단계·확인된 완료 상태를 쉽게 찾도록 출력 구조를 정리할 때 사용합니다. 세션 현황 복원, 인수인계 작성, 작업 실행, 의료 조언이나 스킬 유지보수의 담당자는 아닙니다."
disable-model-invocation: false
argument-hint: "<answer or task output to make actionable>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
---

# Actionable output

## Shared References

Read branch-triggered criteria from the current installed owners. A missing/mismatched
owner or resource blocks that action: use `tk-setup-skills`, not memory, another installation
or unapproved installs. Reading grants no workflow or mutation authority.

- For a user-owned decision, missing approval or unmet prerequisite, read [question rounds](../tk-questioning/references/questions.md).
- Before a user-facing completion report, artifact-path handoff or multi-attribute chat comparison, read [chat delivery](../tk-writing/references/delivery.md). The task's specific output contract wins.

Shape the requested answer or the active owner's progress/result so the reader can find
what matters and act on it. This is presentation assistance, not a workflow, task executor,
medical inference or a session-status owner. Apply it to this response only; it neither stays
on across turns nor changes the active task's authority, checks or continuation rules.

Lead with the answer, verified result or the one user action actually needed. If the agent
already has authority and capability to do the work, keep doing it through its owner; do not
turn its tasks into commands the user must carry out or add a routine permission question.
For several user-performed steps, use a short numbered sequence of bounded actions. Group
long lists by relevance while retaining every requested item, material risk, caveat and source.
A small visible working set must not cap investigation, candidate generation or completeness.

Keep the task position and concrete verified completion easy to find when relevant, without
repeating a whole plan. Distinguish plans from execution, baseline capture from acceptance,
and local commits from confirmed publication. Describe an error's cause, impact and supported
next action calmly; retain uncertainty and blockers. Do not invent times, progress or success.
When no user action remains, end with the result; do not manufacture a follow-up task.

Explain fully when requested, using clear sections when useful. Suppress unrelated tangents
without silently omitting necessary alternatives or safety information. Preserve exact code,
commands, URLs, UI labels, terms and source qualifications. Output shaping never overrides
harness instructions, evidence, authorization or the requested depth/format.

A request for current-session orientation belongs to `tk-handoff`'s conversation-only branch;
durable handoff writing/resume belongs to its artifact branch. Do not inspect repositories,
other sessions or remote state merely to shape an answer, create a status ledger, or impose
an orientation card on unrelated future replies. Session learning and improvement diagnosis belong to `tk-retro`; implementation belongs to the authorized change owner
and its authorized implementation owner, not this output-shaping invocation.

For maintenance provenance, see [distillation](references/distillation.md).

## Artifact Paths

This skill creates no artifacts. Do not create temporary files, write reports, or edit ignore rules for this invocation; return the result in the conversation.
