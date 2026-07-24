---
name: tk-reflect
description: "[user/auto] 대화·diff·결과의 증거에서 재사용 가능한 rule 또는 skill 후보를 분류해 보고할 때 사용합니다. implicit mode는 report-only이며 단순 요약·구현 완료·자동 적용에는 사용하지 않습니다."
argument-hint: "<대화, 수정, diff, 결과 또는 소스>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 회고

명시 호출 또는 증거에서 재사용 후보를 추출해 달라는 명확한 요청에 사용합니다. 단순 요약·구현 완료에는 자동으로 활성화하지 말고, 다른 스킬을 호출하지 마세요. implicit mode는 항상 report-only입니다.

현재 대화, 수정 사항, diff, 구현/테스트/검토 결과, 관련 `.tigerkit/` 산출물, 사용자가 지정한 소스를 읽으세요. 정확히 네 축, 즉 `repo rule`, `repo skill`, `user rule`, `user skill`로 분류하고 `propose | update | merge | no-op | discard` 중 하나를 선택하세요.

## Workflow

1. `evidence`: 입력은 대화·diff·결과·소스이고, 출력은 접근 실패를 포함해 네 축으로 분류된 경로/명령 기반 `verified | unverified` 사실입니다.
2. `interpretation`: 입력은 evidence이고, 출력은 사실과 분리된 재사용 가설입니다.
3. `confidence`: 입력은 evidence와 가설이고, 출력은 `high | medium | low` 및 근거입니다.
4. `action`: 입력은 후보와 기존 reuse map이고, 출력은 repository candidate에 [배치 rubric](references/repository-placement.md)을 적용한 target 위치와 `propose | update | merge | no-op | discard` 중 하나입니다. 실제 문안은 별도 `초안`이 소유합니다.
5. `apply/receipt`: 입력은 후보·별도 승인·적용 전 대상 상태이고, 출력은 아래 상태 전이표의 상태와 후보·evidence·재검증 경로 참조입니다. 후보 본문을 receipt에 복사하지 마세요.

### 후보 상태 전이

| Candidate | Condition | Status | Mutation |
|---|---|---|---|
| Rule `propose | update | merge` | 별도 적용 승인 전 | `pending` | 없음 |
| Rule `no-op | discard` | 적용할 내용 없음 | `reported` | 없음 |
| Rule `propose | update | merge` | 별도 승인 후 정확한 target에 반영·재검증 성공 | `applied` | 승인 범위만 |
| Rule | 승인 후 적용·재검증 실패 | `Fail | Blocked | Unverifiable` | 기존 대상 보존, 추가 mutation 중단 |
| Skill 후보 | evidence·exact target·working draft 제시 | `pending` | 생성·semantic update·merge 없음 |
| 모든 후보 | verified evidence가 하나도 없음 | `Unverifiable` | 없음 |

각 후보를 다음처럼 분리해 작성하세요.

- `Evidence`: 실제로 관찰한 diff·결과·반복 사례와 경로/명령을 적고 `verified | unverified`를 표시하세요.
- `Interpretation`: Evidence ID에서 도출한 재사용 범위·경계 가설만 적고, 적용할 규칙 문안이나 `~해야 한다` 처방은 쓰지 마세요. 실제 처방은 초안만 소유합니다. 가설을 관찰 사실처럼 쓰지 마세요.
- `Confidence`: `high | medium | low`, `Basis: <Evidence IDs>`, 필요한 경우 `Uncertainty: ...`만 적으세요. source 종류·사례 수·관찰·가설을 다시 서술하지 마세요. 증거가 부족하면 `low`로 두고 승격하지 마세요.
- `Action`: 중복이면 새로 만들지 말고 `merge` 또는 `no-op`을 우선하세요. 규칙은 짧은 상시 지침, 스킬은 트리거·반복 단계·입출력·독립적 가치를 가져야 합니다.

`repo rule | repo skill` 후보에는 배치 rubric의 정규화된 raw 입력을 Evidence에, 재사용 범위와 root/nested/skill 경계 해석을 Interpretation에, 수행 선택을 Action에 기록하세요. 별도 배치 근거 필드를 만들지 마세요. Evidence를 읽을 수 없거나 threshold가 충돌하면 confidence를 `low`로 두고 후보를 승격하지 마세요.

Confidence는 다음 기준으로만 올리세요. `high`는 서로 다른 occurrence 또는 source type의 독립적인 verified Evidence ID가 2개 이상이고 미해결 conflict·counterexample이 없는 경우입니다. `medium`은 verified Evidence ID가 1개 이상이지만 반복성·독립성·적용 경계 중 하나가 아직 확인되지 않은 경우입니다. Verified evidence가 없거나 conflict·counterexample이 미해결이면 `low`이며 `propose | update | merge`로 승격하지 마세요.

## 계약

저장소 대상은 코드베이스/도메인/도구/팀에 특화되고, 사용자 대상은 여러 저장소에서 반복됩니다. 기본은 `report-only`입니다. Rule 후보를 DESIGN, reuse map 또는 rule에 기록·수정·적용하려면 대상과 범위를 밝힌 별도의 명시적 사용자 동의를 먼저 받으세요. 침묵, 진행, 과거 유사 답변, reflect 호출 자체는 적용 동의가 아닙니다.

신규 skill 생성과 기존 skill의 semantic update/merge는 `tk-learn`만 소유합니다. 이 skill은 skill 후보의 evidence, current-host native exact target, working draft와 `pending`까지만 보고하고, `tk-learn`을 자동 호출하거나 skill path를 직접 쓰지 않습니다.

사용자가 중단하면 `aborted`, 충돌 또는 적용 범위가 불명확하면 `Blocked`로 보고하세요. 후보별 `reported | pending | applied`와 실행 전체의 terminal status를 섞지 마세요.

기본적으로 파일을 수정하거나 영속 원장/식별자를 만들지 말고, 레거시 전역 상태를 탐색하거나 일회성 우회책을 일반화하지 마세요. 아래 `RF-##`는 이번 응답 안에서만 쓰는 출력용 후보 ID이며 원장 상태가 아닙니다. 별도 명시적 동의가 있더라도 원시 자격 증명/로그/스크린샷을 규칙이나 스킬 후보로 그대로 승격하지 마세요.

필수 source를 읽을 수 없으면 경로와 오류를 `unverified`로 기록하고 해당 내용을 해석하거나 후보 근거로 사용하지 마세요. 적용·재검증 실패와 verified evidence 부재는 후보 상태 전이표를 따르세요.

## CHECKPOINT / STOP

후보의 대상, evidence, confidence, action을 제시한 뒤 별도의 명시적 적용 동의를 받으세요. 동의 전에는 후보 상태 전이표의 `pending | reported` 경계에서 멈추세요.

비어 있지 않은 각 후보는 위 필드 계약에 따라 `대상`, ID가 붙은 `Evidence`, `Interpretation`, `Confidence`, `Action`, 필요할 때만 `초안`, `Receipt`를 한 번씩만 보고하세요. `이 대상인 이유`·`작업`·`학습 내용` 같은 중복 필드를 만들지 말고 Receipt에는 상태와 앞선 필드 참조만 기록하세요.

## Output contract

첫 후보부터 발견 순서대로 `RF-01`, `RF-02`, …를 한 번 부여하고 본문 제목을 `### RF-01 · <짧은 이름>`으로 쓰세요. 같은 후보의 `대상`, Evidence, Interpretation, Confidence, Action, 초안, Receipt와 마지막 Summary는 모두 동일한 `RF-##`를 사용합니다. 후보를 섹션마다 다시 번호 매기거나 ID 없는 후보·rule 항목을 출력하지 마세요.

응답의 마지막 섹션은 항상 아래 고정 형식의 `## Summary`입니다. 후보마다 정확히 한 행을 두고, `Rule`에는 후보의 짧은 이름과 `repo rule | repo skill | user rule | user skill` 축을, `한 줄 요약`에는 새 evidence를 추가하지 않는 한 문장을, `적용 타깃`에는 구체적인 파일/skill/user 범위 또는 `미확정 (<이유>)`를 적으세요. 상세 evidence·초안·작업을 표에 복사하지 마세요.

| No. | Rule | 한 줄 요약 | 적용 타깃 |
| --- | --- | --- | --- |
| RF-01 | `<짧은 이름> (<축>)` | `<한 문장>` | `<구체적 타깃 또는 미확정 (이유)>` |

후보가 없거나 `Unverifiable`이어도 Summary를 생략하지 말고 `| — | 없음 | 재사용 가능한 rule/skill 후보 없음 | 적용 없음 |` 한 행을 출력하세요.

## DO NOT / ANTI-PATTERNS

- 해석이나 가설을 관찰 사실처럼 쓰거나 confidence를 근거 없이 높이지 마세요.
- 기존 후보와 중복되는 skill을 새로 만들거나 적용 동의 없이 파일을 수정하지 마세요.
- 원시 credential·log·screenshot과 일회성 우회책을 재사용 규칙으로 승격하지 마세요.
- 후보 ID를 생략·재사용·재번호화하거나 Summary를 생략하지 마세요.
