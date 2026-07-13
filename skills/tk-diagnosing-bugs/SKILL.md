---
name: tk-diagnosing-bugs
description: "[auto] 어려운 버그를 재현하고 최소화하며 가설을 검증하고 회귀 수정 사항을 확인하여 진단합니다."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: mattpocock/skills
    upstream-skill: diagnosing-bugs
    relationship: adapted
---

# 버그 진단

어렵거나 원인이 불분명한 실패에 사용하세요. [조사 루프](references/investigation.md)를 따르세요.

보고된 증상을 재현하기 전에 패치하지 마세요. 반증 가능한 가설을 여러 개로 구분하고 관찰 결과로 가설을 제거하며, 근본 원인과 증상을 분리하세요. 공통 원인을 수정하고, 유용하다면 올바른 경계에 회귀 검사를 추가한 다음 원래 재현 절차를 다시 실행하세요.

재현, 근본 원인, 수정 사항, 회귀 증거를 보고하세요.
