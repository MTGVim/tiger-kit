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

## 계약

새 인수인계의 기본 작성 대상은 `.tigerkit/handoff.md`입니다. 다음 필수 schema를 사용하세요.

## 🔴 CHECKPOINT · 🛑 STOP 작성·재개 경계

작성하거나 재개하기 전에 현재 브랜치, 파일, 목표, 결정, 검증 증거를 대조하세요. drift 또는 conflict가 있으면 해결된 것으로 간주하지 말고 `pending` 또는 `Blocked` receipt에서 멈추세요.

- `Goal`: 목표와 범위
- `Status`: `pending | in_progress | completed | aborted | Blocked`
- `Decisions`: 사용자 답변/승인과 연결된 결정만 `confirmed`로, 나머지는 `pending`
- `Changed files`: 실제로 확인한 경로만
- `Commands`: 실제로 실행한 명령과 결과
- `Verification`: 항목별 `verified | unverified`와 증거 위치
- `Remaining work`, `Open questions`, `Risks`, `Next step`, `Resume hints`

`verified`는 현재 실행에서 확인한 증거가 있을 때만 사용하세요. 이전 handoff의 주장, 계획, 모델 추론, 실행하지 않은 명령은 `unverified`로 유지하고 성공했다고 표현하지 마세요. receipt에는 무엇이 `reported`되었는지, 사용자의 명시적 승인을 받아 무엇이 `applied`되었는지, 무엇이 `pending`인지와 각 증거/미검증 항목을 구분해 적으세요. 빈 섹션은 생략하고, 기존 spec/ticket/diff 경로는 복사하지 말고 참조하세요.

상위 스크래치 디렉터리는 필요할 때 만들고, 가능하면 임시 파일 작성 후 이름을 바꾸며, 보관본/현재 포인터를 만들거나 `.gitignore`를 편집하지 말고, 스크래치가 무시되지 않으면 경고하세요. 인수인계 파일 작성 자체가 요청된 출력이라도 미확정 결정을 `confirmed`로 바꾸지는 않습니다.

재개/계속 의도일 때 인수인계를 읽고 현재 Git 및 파일 상태를 검사하세요. 기존 handoff와 현재 상태의 파일, 브랜치, 목표, 결정, 검증 결과 차이를 `drift`로 표시하고 서로 다른 의도나 결과는 `conflict`로 표시하세요. 사용자가 명시적으로 resume을 확인하기 전에는 drift/conflict를 해결한 것으로 간주하거나 작업을 계속하지 마세요. 확인이 없으면 `pending` 또는 `Blocked`로 receipt를 종료하세요. 재개 후에도 현재 확인한 증거가 없는 항목은 `unverified`로 유지하세요.

장기 작업에는 전체 목표, 현재/완료된 작업 조각, 차단 요소/경계, 최근 결정, 다음 구체적 작업, 재개 힌트를 담은 `.tigerkit/work-map.md`를 유지하세요.

대화 기록을 복사하거나, 보관본/현재 포인터를 만들거나, 자동으로 커밋하거나 게시하지 마세요.
