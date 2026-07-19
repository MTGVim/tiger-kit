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
2. `materiality`: 입력은 drift/conflict 목록이고, 출력은 `none | non-material | material` 분류와 근거입니다.
3. `continue or checkpoint`: `none | non-material`이면 명시적 resume 호출을 계속 승인으로 보고 진행하고, `material`이면 사용자에게 필요한 결정 하나와 `pending | Blocked` 상태를 출력합니다.
4. `continue or stop`: 입력은 no-drift 승인 또는 material drift에 대한 명시적 확인이고, 출력은 계속할 작업 또는 중단 사유입니다.

## 계약

작성: `evidence → schema → write → receipt`. 재개: `현재 상태 대조 → drift/conflict와 materiality 표시 → 일치하면 계속, material이면 명시적 확인 → 계속 또는 중단`.

새 인수인계의 기본 작성 대상은 `.tigerkit/handoff.md`입니다. 다음 필수 schema를 사용하세요.

- `Goal`: 목표와 범위
- `Status`: 작업 진행 상태인 `pending | in_progress | completed | aborted | Blocked`
- `Decisions`: 사용자 답변/승인과 연결된 결정만 `confirmed`로, 나머지는 `pending`
- `Changed files`: 실제로 확인한 경로만
- `Commands`: 실제로 실행한 명령 문자열만
- `Verification`: Commands를 포함한 검증 항목별 결과, `verified | unverified`와 증거 위치
- `Remaining work`: 아직 끝나지 않은 전체 작업
- `Open questions`: 진행 전에 답이 필요한 결정
- `Risks`: 질문과 별개로 남은 실패·회귀 가능성
- `Next step`: Remaining work에서 선택한 즉시 실행할 한 단계
- `Resume hints`: Next step을 반복하지 말고 재개에만 필요한 환경·순서·명령

`verified`는 현재 실행에서 확인한 증거가 있을 때만 사용하세요. 이전 handoff의 주장, 계획, 모델 추론, 실행하지 않은 명령은 `unverified`로 유지하고 성공했다고 표현하지 마세요. Commands는 과거에 실제 실행한 명령만 소유하며 Next step·Resume hints의 미래 명령을 미리 복사하지 않습니다. 실행 성공·실패는 Verification만 소유하고 Commands에 결과를 덧붙이지 마세요. Verification의 handoff 내용·schema 재확인과 Receipt의 handoff 작성 상태는 서로 다른 상태이므로 각각 한 번만 기록하고 다른 쪽에서는 참조하세요. Receipt의 `reported | applied | pending`은 handoff 작성·적용 상태이며 작업 진행 `Status`와 섞지 마세요. Receipt에는 작성·적용 상태와 내용이 있는 섹션의 증거 위치만 참조하고 `Commands`, `Verification` 또는 미래 작업 본문을 복사하지 마세요. 빈 섹션은 생략하고, 기존 spec/ticket/diff 경로는 복사하지 말고 참조하세요.

## CHECKPOINT / STOP

`--resume` 자체는 현재 handoff를 재개하라는 명시적 승인입니다. 현재 상태가 일치하거나 결과를 바꾸지 않는 non-material drift만 있으면 추가 승인 질문 없이 계속하세요. Branch/목표 scope, confirmed decision, changed-file ownership 또는 verification 결과를 바꾸는 material drift/conflict가 있으면 차이와 선택지를 제시하고 사용자의 결정 전에는 `pending` 또는 `Blocked`로 멈추세요.

상위 스크래치 디렉터리는 필요할 때 만들고, 가능하면 임시 파일 작성 후 이름을 바꾸며, 보관본/현재 포인터를 만들거나 `.gitignore`를 편집하지 말고, 스크래치가 무시되지 않으면 경고하세요. 인수인계 파일 작성 자체가 요청된 출력이라도 미확정 결정을 `confirmed`로 바꾸지는 않습니다.

재개/계속 의도일 때 인수인계를 읽고 현재 Git 및 파일 상태를 검사하세요. 기존 handoff와 현재 상태의 파일, 브랜치, 목표, 결정, 검증 결과 차이를 `drift`로 표시하고 서로 다른 의도나 결과는 `conflict`로 표시하세요. Timestamp, 출력 순서처럼 결과를 바꾸지 않는 차이는 non-material로 보고 계속할 수 있습니다. Branch/목표 scope, confirmed decision, changed-file ownership, verification 결과를 바꾸는 material drift/conflict는 자동 해결하지 말고 사용자 결정을 받으세요. 재개 후에도 현재 확인한 증거가 없는 항목은 `unverified`로 유지하세요.

장기 작업에는 전체 목표, 현재/완료된 작업 조각, 차단 요소/경계, 최근 결정, 다음 구체적 작업, 재개 힌트를 담은 `.tigerkit/work-map.md`를 유지하세요.

## 실패 복구

| 트리거 | 1차 처리 | 계속 실패하면 |
| --- | --- | --- |
| 기존 handoff가 없거나 읽을 수 없음 | 경로와 접근 실패를 보고하고 새 작성과 재개를 구분합니다. | 재개에 필요한 상태를 복원할 증거가 없으면 `Unverifiable`로 멈추고 내용을 추정하지 않습니다. |
| 임시 파일 작성·교체 실패 | 기존 handoff를 그대로 보존하고 이번 실행이 만든 임시 파일만 정리하며 `pending`으로 보고합니다. | 기존 파일 보존 여부를 확인할 수 없으면 추가 쓰기를 중단하고 `Blocked`로 남깁니다. |
| 작성 후 재검증이 schema·실제 상태와 불일치 | `applied`로 표시하지 않고 불일치 항목을 `unverified`로 되돌립니다. | 안전하게 다시 읽어 대조할 수 없으면 `Unverifiable`로 종료합니다. |
| handoff와 work-map이 branch·scope·결정에서 충돌 | material conflict로 표시하고 어느 상태를 기준으로 할지 한 가지 결정을 요청합니다. | 사용자 결정 전에는 어느 파일도 자동 수정하거나 작업을 계속하지 않습니다. |

대화 기록을 복사하거나, 보관본/현재 포인터를 만들거나, 자동으로 커밋하거나 게시하지 마세요.

## DO NOT / ANTI-PATTERNS

- 실행하지 않은 명령·검증·결정을 `verified` 또는 `confirmed`로 기록하지 마세요.
- material drift/conflict를 사용자 확인 없이 해결된 것으로 간주하거나 작업을 계속하지 마세요.
- 보관본, 현재 포인터, 자동 commit 또는 publish를 만들지 마세요.
