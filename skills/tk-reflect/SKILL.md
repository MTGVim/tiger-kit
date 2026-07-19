---
name: tk-reflect
description: "[user] 증거에서 재사용 가능한 규칙 또는 스킬 후보를 추출합니다. 사용자가 명시적으로 호출할 때만 사용합니다."
disable-model-invocation: true
argument-hint: "<대화, 수정, diff, 결과 또는 소스>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# 회고

사용자가 이 스킬을 명시적으로 호출할 때만 사용합니다. 자동으로 활성화하거나 다른 사용자 호출형 스킬을 호출하지 마세요.

현재 대화, 수정 사항, diff, 구현/테스트/검토 결과, 관련 `.tigerkit/` 산출물, 사용자가 지정한 소스를 읽으세요. 정확히 네 축, 즉 `repo rule`, `repo skill`, `user rule`, `user skill`로 분류하고 `propose | update | merge | no-op | discard` 중 하나를 선택하세요.

## Workflow

1. `evidence`: 입력은 대화·diff·결과·소스이고, 출력은 접근 실패를 포함해 네 축으로 분류된 경로/명령 기반 `verified | unverified` 사실입니다.
2. `interpretation`: 입력은 evidence이고, 출력은 사실과 분리된 재사용 가설입니다.
3. `confidence`: 입력은 evidence와 가설이고, 출력은 `high | medium | low` 및 근거입니다.
4. `action`: 입력은 후보와 기존 reuse map이고, 출력은 `propose | update | merge | no-op | discard` 중 하나입니다. 실제 문안은 별도 `초안`이 소유합니다.
5. `apply/receipt`: 입력은 후보·별도 승인·적용 전 대상 상태이고, 출력은 `reported | applied | pending` 상태와 해당 후보·evidence·재검증 경로의 참조입니다. 후보 본문을 receipt에 복사하지 마세요.

각 후보를 다음처럼 분리해 작성하세요.

- `Evidence`: 실제로 관찰한 diff·결과·반복 사례와 경로/명령을 적고 `verified | unverified`를 표시하세요.
- `Interpretation`: evidence에서 도출한 재사용 가설을 적으세요. 가설을 관찰 사실처럼 쓰지 마세요.
- `Confidence`: `high | medium | low`와 올린 이유를 적으세요. 증거가 부족하면 `low`로 두고 승격하지 마세요.
- `Action`: 중복이면 새로 만들지 말고 `merge` 또는 `no-op`을 우선하세요. 규칙은 짧은 상시 지침, 스킬은 트리거·반복 단계·입출력·독립적 가치를 가져야 합니다.

## 계약

저장소 대상은 코드베이스/도메인/도구/팀에 특화되고, 사용자 대상은 여러 저장소에서 반복됩니다. 기본은 `report-only`입니다. 후보를 DESIGN, reuse map, rule 또는 skill에 기록·수정·적용하려면 대상과 범위를 밝힌 별도의 명시적 사용자 동의를 먼저 받으세요. 침묵, 진행, 과거 유사 답변, reflect 호출 자체는 적용 동의가 아닙니다.

receipt는 `reported | applied | pending`을 구분하세요. 승인 전 후보와 적용은 `pending`, 보고만 한 결과는 `reported`, 명시적 승인 후 실제 파일에 반영한 결과만 `applied`로 기록하고 경로와 evidence를 남기세요. 사용자가 중단하면 `aborted`, 충돌 또는 적용 범위가 불명확하면 `Blocked`로 보고하세요.

기본적으로 파일을 수정하거나 원장/ID를 만들지 말고, 레거시 전역 상태를 탐색하거나 일회성 우회책을 일반화하지 마세요. 별도 명시적 동의가 있더라도 원시 자격 증명/로그/스크린샷을 규칙이나 스킬 후보로 그대로 승격하지 마세요.

필수 source를 읽을 수 없으면 경로와 오류를 `unverified`로 기록하고 해당 내용을 해석하거나 후보 근거로 사용하지 마세요. Verified evidence가 하나도 남지 않으면 `Unverifiable`로 멈춥니다. 별도 승인 후 적용·재검증이 실패하면 `applied`로 표시하지 말고 기존 대상을 보존하세요. 이번 실행의 변경을 정확히 복원하고 재검증할 수 없으면 추가 수정을 중단하고 실패 경로와 증거를 `Fail | Blocked | Unverifiable`로 보고하세요.

## CHECKPOINT / STOP

후보의 대상, evidence, confidence, action을 제시한 뒤 별도의 명시적 적용 동의를 받으세요. 동의 전에는 파일을 수정하거나 후보를 승격하지 말고 `pending` 또는 `reported`로 멈추세요.

비어 있지 않은 각 후보에 대해 `대상`, `Evidence`, `Interpretation`, `Confidence`, `이 대상인 이유`, `Action`, `초안`, `Receipt`를 한 번씩만 보고하세요. `Interpretation`이 학습 내용을, `Action`이 수행할 작업을 소유하므로 별도 `작업`·`학습 내용` 필드를 만들지 마세요. Receipt는 상태와 앞선 필드의 참조만 기록하고 내용을 반복하지 않습니다.

## DO NOT / ANTI-PATTERNS

- 해석이나 가설을 관찰 사실처럼 쓰거나 confidence를 근거 없이 높이지 마세요.
- 기존 후보와 중복되는 skill을 새로 만들거나 적용 동의 없이 파일을 수정하지 마세요.
- 원시 credential·log·screenshot과 일회성 우회책을 재사용 규칙으로 승격하지 마세요.
