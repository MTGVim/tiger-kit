---
name: tk-code-review
description: "[auto] 고정된 diff를 편집하지 않고 명세 준수 여부와 코드 품질을 리뷰합니다."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: mattpocock/skills
    upstream-skill: code-review
    relationship: adapted
---

# 코드 리뷰 규율

변경 범위를 고정하고 그 범위만 검사하세요. 요청/명세 준수 여부와 코드 품질을 구분하세요. 코드를 편집하거나 자동 재리뷰를 시작하지 마세요.

모든 발견 사항에는 `Critical | Important | Minor`, 제목, `file:line` 증거를 포함하세요. 발견 사항이 없으면 없다고 명시하세요.

`## Findings`와 `## Verdict`를 `Pass | Changes requested`와 함께 출력하세요.
