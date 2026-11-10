---
name: tk-debug
description: "[user/auto] 오류·크래시·회귀·동작 실패의 원인을 묻거나 디버깅을 요청할 때 사용합니다. 일반 코드 리뷰와 신규 기능에는 사용하지 않으며, 진행 중인 tk-prep·tk-pr-respond 진단에는 개입하지 않습니다."
disable-model-invocation: false
argument-hint: "<error, symptom, or regression>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tw93/Waza
    relationship: adapted
    upstream-skill: hunt
---

# 오류 진단 진입점

현재 같은 작업을 `tk-prep` 또는 `tk-pr-respond`가 담당하면 해당 담당자에게 진단 근거를 반환하고
별도 워크플로를 시작하지 않습니다. 그렇지 않으면 현재 요청의 증상·기대 동작·접근 범위를 확인한 뒤
설치된 `tk-engineering`의 [진단](../tk-engineering/references/diagnosis.md)을 읽습니다.
소유자·참조가 없거나 식별이 다르면 해당 진단을 중단하고 `tk-setup-skills`를 안내합니다.
다른 설치본·기억·소스 checkout으로 대신하지 않습니다.

“왜 에러가 나지”, 조사·진단 요청은 읽기·보고 전용입니다. 현재 승인 범위 안의 안전한 재현과
비변경 탐침만 수행하고 제품 코드·설정·데이터를 수정하지 않습니다. 수정 요청이나 같은 미완료
작업의 유효한 수정 승인이 있을 때만 진단 문서의 원인·검증 조건을 충족한 범위에서 수정합니다.
진단 참조를 읽는 것은 설치·인증·비밀 접근·Git commit·원격 발행 권한이 아닙니다.

결과는 증상, 원인과 `file:line` 근거(미확인이면 가설), 실제 재현·검증 결과, 남은 공백을 짧게
보고합니다. 수정했다면 같은 유형 조사 결과도 포함합니다. 근거 없는 수정 반복을 멈추는 기준은
진단 문서가 소유합니다. 새 진단 장부·중앙 router·자동 설치를 만들지 않습니다.

유지보수 출처: [Waza 적용 판단](../tk-engineering/references/waza-sources.md).
