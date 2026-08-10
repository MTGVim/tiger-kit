---
name: tk-handoff
description: "[user/auto] verified handoff artifact를 작성하거나 기존 handoff를 명시적으로 재개합니다. 일반 요약, 상태 질문, 일반적인 continuation에는 적용하지 않습니다."
disable-model-invocation: false
argument-hint: "[goal or target] [--output <path>|--resume]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 인수인계 (Handoff)

명시적 invocation 또는 명확한 handoff write/resume 요청에 적용합니다. 요약,
상태 질문, 일반적인 continuation에는 자동 적용하지 않으며 다른 skill을
invoke하지 않습니다.

## 작업 흐름

### 새 handoff

1. `evidence`: 현재 branch, files, command results를 path-cited fact와
   `verified | unverified`로 매핑합니다.
2. `schema`: fact와 사용자 승인을 required-section draft 및
   `confirmed | pending` decision으로 매핑합니다.
3. `write`: 승인된 draft와 output path를 written file로 매핑합니다.
4. `receipt`: write/revalidation 결과를
   `reported | applied | pending` 및 evidence location으로 매핑합니다.

### 재개(Resume)

1. `state check`: existing handoff를 current Git/files와 비교하고 일치 항목과
   `drift | conflict`를 나열합니다.
2. `materiality`: evidence와 함께 resume table로 분류합니다.
3. `continue or checkpoint`: table의 continuation/stop result를 따릅니다.
4. `continue or stop`: no-drift approval 또는 명시적 material-drift
   confirmation으로 next work 또는 stop reason을 생성합니다.

### 재개 결정표(Resume decision table)

| Classification | Evidence | Action |
|---|---|---|
| `none` | branch, goal, decisions, ownership, verification이 current evidence와 일치함 | `--resume`을 approval로 간주하고 추가 질문 없이 계속 |
| `non-material` | 결과를 바꿀 수 없는 timestamp/order 차이 | 기록하고 추가 질문 없이 계속 |
| `material drift` | branch/goal scope, confirmed decisions, changed-file ownership 또는 verification result가 다름 | 필수 decision 하나를 묻고 `pending | Blocked`에서 중지 |
| `conflict` | handoff와 current source가 양립할 수 없는 intent/result를 요구함 | 두 evidence set과 선택지를 제시하고 `Blocked`에서 중지 |
| `unverified` | 필요한 Git/file state를 확인할 수 없음 | 추론하지 말고 `Unverifiable`에서 중지 |

## 계약(Contract)

기본 대상 `.tigerkit/handoff.md`에는 다음이 포함됩니다:

- `Goal`: goal과 scope
- `Status`: `pending | in_progress | completed | aborted | Blocked`
- `Repository state`: current branch, HEAD, worktree
- `Handoff path`: 정확히 write/read한 path
- `Decisions`: answer/approval과 연결된 decision만 `confirmed`; 나머지는 `pending`
- `Changed files`: 관찰된 path만
- `Commands`: 실제 실행한 exact command
- `Verification`: check별 result, `verified | unverified`, evidence location
- `Remaining work`: 완료되지 않은 모든 work
- `Open questions`: 진행 전에 필요한 decision
- `Risks`: question과 분리한 남은 failure/regression risk
- `Next step`: Remaining work에서 선택한 하나의 즉시 action
- `Resume hints`: Next step을 반복하지 않고 resume에 필요한 environment/order/command만

`handoff.md`는 아래 single snapshot skeleton을 사용합니다. 각 field는 artifact가
한 번만 소유하며, 실행하지 않은 값은 `unverified` 또는 `pending`으로 둡니다.

```text
Goal: <goal and scope>
Status: pending | in_progress | completed | aborted | Blocked
Repository state: <branch, HEAD, worktree>
Handoff path: <exact path>
Decisions: <confirmed | pending decisions>
Changed files: <observed paths | none>
Commands: <exact executed commands | none>
Verification: <check/result/evidence location>
Remaining work: <unfinished work | none>
Open questions: <required decisions | none>
Risks: <failure/regression risks | none>
Next step: <one exact immediate action>
Resume hints: <environment/order/command>
Disposition: reported | applied | pending
```

`Next step`은 conversation을 재구성하지 않고 실행 가능해야 합니다: exact
target, satisfied prerequisite 또는 section reference, observable completion
evidence를 포함합니다. open question이 work를 막으면 Next step은 downstream
execution이 아니라 해당 decision을 얻는 action이어야 합니다.

이번 실행에서 확인한 evidence에만 `verified`를 사용합니다. 이전 handoff claim,
plan, model inference, 실행하지 않은 command는 `unverified`로 둡니다. 소유권은
엄격히 지킵니다: Repository state는 branch/HEAD를, Handoff path는 path를,
Commands는 실행한 command string만, Verification은 outcome을,
Next step/Resume hints는 future command를 소유합니다. `reported | applied | pending`은
artifact disposition이지 work Status가 아닙니다. atomic write와
reread가 current repository state와 일치한 뒤에만 `applied`를 사용합니다.
artifact write가 필요 없는 verified no-drift resume/report에는 `reported`를
사용합니다. 그 외에는 `pending` 또는 해당 recovery-table stop state를 사용합니다.

Handoff artifact가 disposition과 section reference를 소유합니다. Terminal
summary에는 path, Git state, command, result, future work를 중복하지 않으며
metadata도 넣지 않습니다. 빈 section은 생략하고, 기존 spec/ticket/diff를
복사하지 말고 참조합니다. compound result는 current state, completed work,
next action, blocker를 2–5개의 짧은 bullet로 요약하고, 하나의 result는 1–3개의
짧은 줄로 작성할 수 있습니다. underlying item이 8개 이상이면 상위 5–7개만
보여주고 전체 inventory를 소유한 artifact path를 제시합니다. 이는 quota가
아니라 budget입니다.

`.tigerkit/handoff.md`만 resume snapshot입니다. Drive가 source run을 소유하면
`.tigerkit/drive.md`의 durable R/AC 및 multi-unit ID를 참조합니다. 절대로
`.tigerkit/work-map.md`, archive, current pointer 또는 global state를 만들지
않습니다. 기존 work-map은 legacy scratch로 취급하며 수정·migrate·delete하지
않습니다.

## CHECKPOINT / STOP (승인·중단 지점)

`--resume`은 resume을 authorize하며, continuation은 resume table만 따릅니다.

scratch parent는 필요할 때만 만들고, 같은 directory의 temporary file에 쓴 뒤
atomic rename하고 reread합니다. 실패하면 recovery table을 따릅니다. archive/
current pointer를 만들거나 `.gitignore`를 수정하지 않습니다. scratch가 ignore되지
않았으면 경고합니다. 요청된 handoff file이 unresolved decision을
`confirmed`로 만들지는 않습니다.

Resume 시 handoff와 current Git/files를 읽고 classify합니다. current evidence가
없는 내용은 `unverified`로 유지합니다.

## 실패 복구(Failure recovery)

| Trigger | First action | If still failing |
|---|---|---|
| handoff missing/unreadable | path/access를 보고하고 new write와 resume를 구분 | evidence로 resume state를 재구성할 수 없으면 `Unverifiable`에서 중지 |
| temp write/replace failure | 기존 handoff를 보존하고 run-owned temp만 정리한 뒤 `pending`을 보고 | 보존 여부를 알 수 없으면 추가 write를 중지하고 `Blocked` |
| reread disagrees with schema/current state | `applied`로 표시하지 말고 mismatch를 `unverified`로 되돌림 | 안전한 reread가 불가능하면 `Unverifiable`에서 중지 |
| legacy work-map exists | legacy scratch로 무시 | current handoff/spec/ticket evidence만 사용하고 절대 mutate하지 않음 |

대화 history를 복사하거나 archive/current pointer를 만들지 않으며, 자동으로
commit/publish하지 않습니다.

## 금지 사항 / 안티패턴

- 실행하지 않은 command, check 또는 decision을 `verified | confirmed`로 표시하지 않습니다.
- material drift/conflict를 resolve하거나 confirmation 없이 계속하지 않습니다.
- archive, current pointer, automatic commit 또는 publication을 만들지 않습니다.
