---
name: tk-status
description: "[user/auto] 세션을 오가다 현재 작업의 맥락을 놓쳤거나 지금 어디까지 했는지 짧게 확인할 때 사용합니다. 코드 동작 설명, 원격 PR 현황 조사, 인수인계 파일 작성에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "[현재 작업 | 제공한 세션 요약]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
---

# Session Orientation

Restore the reader's place in the current task, using only this conversation and evidence already available. If repository or branch identity is needed and not established, use one cheap read of current Git state. Do not investigate implementation details, enumerate other sessions/worktrees/repositories, or query remote PRs for a status recap. A requested comparison may use summaries the user supplied, with unknown or stale state labeled explicitly; never merge their goals or approvals.

Give one compact card in the user's language. Prefer these five short lines, omitting an empty field rather than filling a quota:

```text
📍 <repository / branch when known> · <task goal>
완료: <latest verified outcome, or no verified completion yet>
지금: <active action or exact blocker>
다음: <one concrete agent-owned next action, or completed>
내가 할 일: <only required user action, or 없음>
```

Distinguish executed work from a plan, capture success from final verification, and local commits from confirmed publication. If context is missing, say what is unknown; ask only for the minimal task identifier needed for a useful answer. Do not invent percentages, timings, completed tests, or access to other sessions. Never infer medical status from this request.

During an active authorized task, answer the orientation question as a progress update, then continue that task in the same turn unless the user explicitly pauses or changes it. Do not ask whether to continue or transfer agent-owned commands to the user. For a standalone status request, stop after the read-only card. This format does not persist to every future reply and does not truncate a requested detailed explanation.

Create no status ledger or handoff file, mutate no repository/remote state for the recap, and grant no additional authority. Durable handoff creation/resume belongs to `tk-handoff`; this skill only restores conversational orientation.
