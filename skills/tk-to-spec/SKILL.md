---
name: tk-to-spec
description: "[user] 현재 결정과 근거를 종합해 구현 명세를 작성합니다. 사용자가 명시적으로 호출한 경우에만 사용합니다."
disable-model-invocation: true
argument-hint: "<대화, 소스 또는 요청> [--output <경로>|--print-only]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: to-spec
    relationship: adapted
---

# 명세 작성

사용자가 이 스킬을 명시적으로 호출한 경우에만 사용하세요. 자동으로 활성화하지 마세요.

소스 우선순위: 사용자가 지정한 소스, 현재 결정, 티켓/문서, 관련 코드, 기존 `.tigerkit/spec.md` 순입니다. 인터뷰를 시작하거나, 티켓을 생성하거나, 게시하거나, 구현하지 마세요.

사용자가 지정한 경로에 쓰거나, 출력 전용이면 결과만 출력하고, 그 외에는 `.tigerkit/spec.md`에 작성하세요. 기존 명세가 같은 작업을 다룬다면 유효한 결정을 유지하고, 그렇지 않으면 아카이브 없이 교체하세요. `.tigerkit/`에 출력할 때는 필요할 때만 상위 디렉터리를 만들고, 가능하면 같은 디렉터리의 임시 파일에 쓴 뒤 이름을 바꾸며, 절대 `.gitignore`를 수정하지 말고, 임시 경로가 무시되지 않으면 짧게 경고하세요. 사실, 결정, 가정, 미해결 충돌을 구분하세요.

필수 섹션: 문제, 목표, 범위(포함/제외), 요구사항, 인수 기준, 검증. 유용할 때 상태, 기존 동작, 기대 동작, 제약, 결정, 가정, 미해결 사항을 추가하세요.

경로, Draft/Ready 상태, 미해결 항목을 보고하세요.
