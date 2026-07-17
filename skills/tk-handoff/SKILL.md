---
name: tk-handoff
description: "[user] 검증된 작업 인수인계를 작성하거나 재개합니다. 사용자가 명시적으로 호출할 때만 사용합니다."
disable-model-invocation: true
argument-hint: "[목표 또는 대상] [--output <경로>|--resume]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# 인수인계

사용자가 이 스킬을 명시적으로 호출할 때만 사용합니다. 자동으로 활성화하거나 다른 사용자 호출형 스킬을 호출하지 마세요.

## Workflow

새 작성은 다음 순서로 진행하세요.

1. `evidence`: 입력은 현재 브랜치·파일·명령 결과이고, 출력은 경로가 붙은 확인 사실과 `verified | unverified` 목록입니다.
2. `schema`: 입력은 확인 사실과 사용자의 승인이고, 출력은 필수 섹션별 초안과 `confirmed | pending` 결정 목록입니다.
3. `write`: 입력은 승인된 초안과 출력 경로이고, 출력은 실제로 작성된 파일 경로입니다.
4. `receipt`: 입력은 작성 결과와 재검증 결과이고, 출력은 `reported | applied | pending` 및 증거 위치가 구분된 인수인계입니다.

재개는 다음 순서로 진행하세요.

1. `state check`: 입력은 기존 인수인계와 현재 Git·파일 상태이고, 출력은 일치 항목과 `drift | conflict` 목록입니다.
2. `checkpoint`: 입력은 drift/conflict 목록이고, 출력은 사용자에게 필요한 재개 확인 또는 `pending | Blocked` 상태입니다.
3. `continue or stop`: 입력은 명시적 확인이고, 출력은 계속할 작업 또는 중단 사유입니다.

## 계약

작성: `evidence → schema → write → receipt`. 재개: `현재 상태 대조 → drift/conflict 표시 → 명시적 확인 → 계속 또는 중단`.

새 인수인계의 기본 작성 대상은 `.tigerkit/handoff.md`입니다. 다음 필수 schema를 사용하세요.

- `Goal`: 목표와 범위
- `Status`: `pending | in_progress | completed | aborted | Blocked`
- `Decisions`: 사용자 답변/승인과 연결된 결정만 `confirmed`로, 나머지는 `pending`
- `Changed files`: 실제로 확인한 경로만
- `Commands`: 실제로 실행한 명령과 결과
- `Verification`: 항목별 `verified | unverified`와 증거 위치
- `Remaining work`, `Open questions`, `Risks`, `Next step`, `Resume hints`

`verified`는 현재 실행에서 확인한 증거가 있을 때만 사용하세요. 이전 handoff의 주장, 계획, 모델 추론, 실행하지 않은 명령은 `unverified`로 유지하고 성공했다고 표현하지 마세요. receipt에는 무엇이 `reported`되었는지, 사용자의 명시적 승인을 받아 무엇이 `applied`되었는지, 무엇이 `pending`인지와 각 증거/미검증 항목을 구분해 적으세요. 빈 섹션은 생략하고, 기존 spec/ticket/diff 경로는 복사하지 말고 참조하세요.

## CHECKPOINT / STOP

`--resume`에서는 drift와 conflict를 대조한 뒤 사용자의 재개 확인을 받으세요. 확인 전에는 작업을 계속하거나 상태를 해결된 것으로 표시하지 말고 `pending` 또는 `Blocked`로 멈추세요.

상위 스크래치 디렉터리는 필요할 때 만들고, 가능하면 임시 파일 작성 후 이름을 바꾸며, 보관본/현재 포인터를 만들거나 `.gitignore`를 편집하지 말고, 스크래치가 무시되지 않으면 경고하세요. 인수인계 파일 작성 자체가 요청된 출력이라도 미확정 결정을 `confirmed`로 바꾸지는 않습니다.

재개/계속 의도일 때 인수인계를 읽고 현재 Git 및 파일 상태를 검사하세요. 기존 handoff와 현재 상태의 파일, 브랜치, 목표, 결정, 검증 결과 차이를 `drift`로 표시하고 서로 다른 의도나 결과는 `conflict`로 표시하세요. 사용자가 명시적으로 resume을 확인하기 전에는 drift/conflict를 해결한 것으로 간주하거나 작업을 계속하지 마세요. 확인이 없으면 `pending` 또는 `Blocked`로 receipt를 종료하세요. 재개 후에도 현재 확인한 증거가 없는 항목은 `unverified`로 유지하세요.

장기 작업에는 전체 목표, 현재/완료된 작업 조각, 차단 요소/경계, 최근 결정, 다음 구체적 작업, 재개 힌트를 담은 `.tigerkit/work-map.md`를 유지하세요.

대화 기록을 복사하거나, 보관본/현재 포인터를 만들거나, 자동으로 커밋하거나 게시하지 마세요.

## DO NOT / ANTI-PATTERNS

- 실행하지 않은 명령·검증·결정을 `verified` 또는 `confirmed`로 기록하지 마세요.
- drift/conflict를 사용자 확인 없이 해결된 것으로 간주하거나 작업을 계속하지 마세요.
- 보관본, 현재 포인터, 자동 commit 또는 publish를 만들지 마세요.
