# Conversation-only orientation

Restore the reader's place in the current task, using only this conversation and evidence already available. If repository or branch identity is needed and not established, use one cheap read of current Git state. Do not investigate implementation details, enumerate other sessions/worktrees/repositories, or query remote PRs for a status recap. A requested comparison may use summaries the user supplied, with unknown or stale state labeled explicitly; never merge their goals or approvals.

Give one compact card in the user's language; for a requested comparison, give one labeled card per supplied session. Translate the field labels to that language. Prefer these five short lines, omitting an empty field rather than filling a quota:

```text
📍 <repository / branch when known> · <task goal>
완료: <latest verified outcome, or no verified completion yet>
지금: <paused task position or exact blocker>
다음: <one suggested action after the user resumes, not an action started now; or completed>
내가 할 일: <only required user action, or 없음>
```

Distinguish executed work from a plan, capture success from final verification, and local commits from confirmed publication. If context is missing, say what is unknown; ask only for the minimal task identifier needed for a useful answer. Do not invent percentages, timings, completed tests, or access to other sessions. Never infer medical status from this request.

A status request pauses task execution for orientation. Present the card as the final response and end the turn, even when an earlier task approval includes implementation, verification, commits or publication. Do not resume that work, dispatch workers, start checks, or schedule background continuation after the card. The next-action line is a suggestion for later, not execution authority. Wait for a subsequent user instruction to resume; do not add a routine approval question. This explicit reporting boundary takes precedence over an owner's ordinary phase-continuation rule. It does not revoke earlier scope approval: a later resume instruction can reuse it when the task still matches. This format does not persist to every future reply or truncate a requested detailed explanation.

Create no status ledger or handoff file, mutate no repository/remote state for the recap, and grant no additional authority. Durable handoff creation/resume belongs to `tk-handoff`; this branch only restores conversational orientation.

