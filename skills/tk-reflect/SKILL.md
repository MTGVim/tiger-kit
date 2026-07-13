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

사용자가 이 스킬을 명시적으로 호출할 때만 사용합니다. 자동으로 활성화하지 마세요.

현재 대화, 수정 사항, diff, 구현/테스트/검토 결과, 관련 `.tigerkit/` 산출물, 사용자가 지정한 소스를 읽으세요. 정확히 네 축, 즉 `repo rule`, `repo skill`, `user rule`, `user skill`로 분류하고 `propose | update | merge | no-op | discard` 중 하나를 선택하세요.

규칙은 짧은 상시 지침입니다. 스킬에는 트리거, 반복 가능한 단계, 입력/출력, 독립적인 가치가 있습니다. 저장소 대상은 코드베이스/도메인/도구/팀에 특화되고, 사용자 대상은 여러 저장소에서 반복됩니다. 관찰한 증거와 해석을 분리하세요.

기본은 보고만 수행합니다. 파일을 수정하거나, 원장/ID를 만들거나, 다른 사용자 스킬을 호출하거나, 레거시 전역 상태를 탐색하거나, 원시 자격 증명/로그/스크린샷을 규칙이나 스킬 후보로 승격하거나, 일회성 우회책을 일반화하지 마세요. 중복에는 merge/no-op을 우선하세요.

비어 있지 않은 각 후보에 대해 대상, 작업, 학습 내용, 증거, 이 대상인 이유, 초안을 보고하세요.
