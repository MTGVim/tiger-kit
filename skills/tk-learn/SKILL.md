---
name: tk-learn
description: "[user] 제공된 경험이나 자료로 재사용 가능한 저장소 또는 사용자 스킬을 만듭니다. 사용자가 명시적으로 호출할 때만 사용합니다."
disable-model-invocation: true
argument-hint: "<대화, 메모, 경로, URL, 워크플로 또는 reflect 후보>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# 학습

사용자가 이 스킬을 명시적으로 호출할 때만 사용합니다. 자동으로 활성화하지 마세요.

현재 대화 내용, 메모, 파일/디렉터리, URL, 워크플로 또는 reflect 후보를 받습니다. `repo skill` 또는 `user skill`을 만드세요. 규칙 생성은 범위 밖입니다.

증거를 수집하고, 반복 가능한 동작을 추출하고, 중복을 검색하고, user-invoked/model-invoked/hybrid로 분류하고, 이름을 제안한 다음, 자체 완결된 최소 스킬을 작성하세요. 필요한 경우에만 references/scripts를 추가하세요. 긍정/부정 트리거를 검토하고 최소 예시 또는 eval을 추가하세요. [스킬 품질](references/skill-quality.md)을 따르세요.

대상/적용 의도가 불분명하면 `.tigerkit/skill-drafts/<skill-name>/` 아래에 초안을 작성하세요. 사용자가 저장소/사용자 대상과 적용을 명시적으로 지정한 경우에만 실제 호스트 고유 스킬 저장 위치에 적용하세요. 초안의 경우 상위 디렉터리는 필요할 때 만들고, 가능하면 원자적으로 교체하며, 자동으로 보관하거나 `.gitignore`를 편집하지 말고, 스크래치가 무시되지 않으면 경고하세요. 규칙이면 충분하거나, 증거가 일회성이거나, 동등한 스킬이 있거나, 기본 모델 기능이면 충분하거나, 트리거를 명시할 수 없으면 스킬을 만들지 마세요.

스킬 이름/종류/대상, 생성한 경로, 검증, 남은 우려 사항을 보고하세요.
