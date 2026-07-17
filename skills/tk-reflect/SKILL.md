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

각 후보를 다음처럼 분리해 작성하세요.

- `Evidence`: 실제로 관찰한 diff·결과·반복 사례와 경로/명령을 적고 `verified | unverified`를 표시하세요.
- `Interpretation`: evidence에서 도출한 재사용 가설을 적으세요. 가설을 관찰 사실처럼 쓰지 마세요.
- `Confidence`: `high | medium | low`와 올린 이유를 적으세요. 증거가 부족하면 `low`로 두고 승격하지 마세요.
- `Action`: 중복이면 새로 만들지 말고 `merge` 또는 `no-op`을 우선하세요. 규칙은 짧은 상시 지침, 스킬은 트리거·반복 단계·입출력·독립적 가치를 가져야 합니다.

## 계약

저장소 대상은 코드베이스/도메인/도구/팀에 특화되고, 사용자 대상은 여러 저장소에서 반복됩니다. 기본은 `report-only`입니다. 후보를 DESIGN, reuse map, rule 또는 skill에 기록·수정·적용하려면 대상과 범위를 밝힌 별도의 명시적 사용자 동의를 먼저 받으세요. 침묵, 진행, 과거 유사 답변, reflect 호출 자체는 적용 동의가 아닙니다.

receipt는 `reported | applied | pending`을 구분하세요. 승인 전 후보와 적용은 `pending`, 보고만 한 결과는 `reported`, 명시적 승인 후 실제 파일에 반영한 결과만 `applied`로 기록하고 경로와 evidence를 남기세요. 사용자가 중단하면 `aborted`, 충돌 또는 적용 범위가 불명확하면 `Blocked`로 보고하세요.

## 🔴 CHECKPOINT · 🛑 STOP 적용 경계

후보를 DESIGN, reuse map, rule 또는 skill에 기록하거나 실제 파일에 적용하기 전에 사용자의 별도 승인을 확인하세요. 승인이 없으면 후보는 `reported` 또는 `pending`으로만 남기고 파일을 쓰지 마세요.

기본적으로 파일을 수정하거나 원장/ID를 만들지 말고, 레거시 전역 상태를 탐색하거나 일회성 우회책을 일반화하지 마세요. 별도 명시적 동의가 있더라도 원시 자격 증명/로그/스크린샷을 규칙이나 스킬 후보로 그대로 승격하지 마세요.

비어 있지 않은 각 후보에 대해 대상, 작업, 학습 내용, `Evidence`, `Interpretation`, confidence, 이 대상인 이유, action, 초안, receipt를 보고하세요.
