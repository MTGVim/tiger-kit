---
name: tk-grilling
description: "[auto] 근거와 권고를 제시하며 중대한 설계 질문을 한 번에 하나씩 합니다."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: mattpocock/skills
    upstream-skill: grilling
    relationship: adapted
---

# 집중 검증 원칙

설계나 계획을 구현하기 전에 결정이 필요할 때 사용합니다.

- 사용자에게 묻는 대신 코드에서 확인 가능한 사실을 조사하세요.
- 사용자의 판단이 필요한 질문만 한 번에 하나씩 하세요.
- 모든 질문에 권고와 짧은 이유를 포함하세요.
- 이미 답한 질문을 반복하거나 합의 전에 구현하지 마세요.

출력: 질문, 권고, 이유. 중대한 사용자 결정이 남지 않았거나 사용자가 중단하면 완료합니다.
