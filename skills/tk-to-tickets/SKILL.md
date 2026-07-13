---
name: tk-to-tickets
description: "[user] 요청이나 명세를 독립적으로 검증 가능한 수직 티켓으로 나눕니다. 사용자가 명시적으로 호출한 경우에만 사용합니다."
disable-model-invocation: true
argument-hint: "<명세, 계획 또는 요청> [--output <경로>]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: to-tickets
    relationship: adapted
---

# 티켓 작성

사용자가 이 스킬을 명시적으로 호출한 경우에만 사용하세요. 자동으로 활성화하지 마세요.

소스 우선순위: 사용자가 지정한 소스, 현재 대화, `.tigerkit/spec.md`, 요청, 관련 코드 순입니다. 독립적인 인수 기준과 검증을 갖춘 결과 중심의 수직 동작 단위를 만드세요. 동작의 테스트는 해당 티켓에 포함하고, 수평적인 type/API/UI/test-only 티켓을 만들지 마세요.

사용자가 지정한 경로 또는 `.tigerkit/tickets.md`에 `# <Feature> Tickets` 형식으로 작성한 뒤, 목표, 범위, 의존성, 인수 기준, 검증, 선택적 참고 사항으로 티켓을 구성하세요. `.tigerkit/`에 출력할 때는 필요할 때만 상위 디렉터리를 만들고, 가능하면 임시 파일에 쓴 뒤 이름을 바꾸며, 절대 타임스탬프 아카이브를 생성하거나 `.gitignore`를 수정하지 말고, 임시 경로가 무시되지 않으면 경고하세요. 구현하거나 원격 트래커에 게시하지 마세요.

경로, 티켓 수, 의존성, 미해결 분할 문제를 보고하세요.
