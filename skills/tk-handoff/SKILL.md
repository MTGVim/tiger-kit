---
name: tk-handoff
description: "[user/auto] 진행 중 작업의 verified handoff snapshot을 작성하거나 기존 handoff를 명시적으로 재개합니다. 작업 목표 계약은 `seed.md`, 진행 상태는 `handoff.md`가 소유합니다. 일반 요약이나 평범한 continuation에는 적용하지 않습니다."
disable-model-invocation: false
argument-hint: "[goal or target] [--output <path>|--resume]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 인수인계

명시적 handoff 작성·재개 요청에 적용합니다. 일반 요약, 상태 질문, 평범한 “계속해”에는 자동 적용하지 않습니다.

역할을 분리합니다.

- `.tigerkit/seed.md`: 무엇을 왜 어떤 조건으로 해야 하는지에 대한 작업 계약
- `.tigerkit/handoff.md`: 이미 무엇을 했고 현재 어디까지 왔는지에 대한 진행 snapshot

Handoff는 Seed를 대체하거나 복사하지 않습니다.

## 새 handoff

현재 repository evidence를 읽습니다.

- branch / HEAD / worktree
- 현재 Seed가 있으면 exact path와 status
- 실제 changed files
- 실제 실행한 commands
- 실제 verification 결과
- 완료한 작업과 남은 작업
- 현재 blocker와 다음 행동

관찰한 사실만 `verified`, 사용자와 확정한 결정만 `confirmed`로 표시합니다.
실행하지 않은 command, 과거 주장, 모델 추론은 `unverified`입니다.

기본 경로는 `.tigerkit/handoff.md`입니다. 같은 디렉터리의 temp file에 쓴 뒤 원자적으로 교체하고 reread합니다.
산출물 작성 자체는 product/Git/remote mutation authority가 아닙니다.

Handoff에는 최소한 다음 의미를 보존합니다.

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

Seed의 goal/scope/AC/implementation guidance를 Handoff에 다시 복사하지 않습니다.
필요하면 exact Seed section/path를 참조합니다.

## 재개

`--resume`은 handoff snapshot을 현재 Git/files와 비교해 재개하는 요청입니다.

먼저 다음을 fresh-read합니다.

- current Seed와 handoff
- branch/HEAD/worktree
- changed files
- relevant verification evidence
- PR이 있다면 current remote state

그 뒤 drift를 분류합니다.

| 분류 | 조치 |
| --- | --- |
| 없음 | 추가 질문 없이 `Next step`부터 계속 |
| 비본질적 drift | 기록하고 계속 |
| material progress drift | 현재 evidence 기준으로 Handoff를 갱신하고 필요한 결정만 확인 |
| Seed contract drift | Handoff에서 해결하지 않고 `tk-prep` 재진입 필요성을 보고 |
| conflict | 양립할 수 없는 evidence를 보여주고 `Blocked` |
| unverified | 필요한 상태를 확인할 수 없으면 `Unverifiable` |

`--resume`은 계속 작업을 승인할 수 있지만 Seed의 goal/scope/decision/AC 변경 승인이나 remote publication authority를 대신하지 않습니다.

## 출력

새 handoff 작성 성공 시 채팅에는 경로와 현재 상태, 다음 행동 정도만 짧게 보여줍니다.
Handoff 본문 전체나 evidence 장부를 덤프하지 않습니다.

재개 시에는 현재까지 완료한 것, 남은 것, blocker, 바로 다음 행동을 사람이 이해하기 쉽게 설명합니다.

`.tigerkit/`를 archive, current pointer, global state로 사용하지 않습니다.
`.gitignore`를 수정하지 않고 자동 commit/publish하지 않습니다.
