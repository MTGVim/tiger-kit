---
description: caveman skill을 활성화해 기술 정확도는 유지하면서 응답을 초압축합니다.
---

TigerKit의 `caveman` skill을 켭니다.
이 command는 skill alias입니다. 자연어로 `caveman mode`, `talk like caveman`, `use caveman`, `less tokens`, `be brief`처럼 요청해도 같은 규칙을 적용합니다.

중단:
- `normal mode`
- `stop caveman`

명료성 예외:
- 보안 경고
- 되돌리기 어려운 action 확인
- 순서가 중요해 오해 위험이 큰 절차
- 사용자가 설명을 다시 요청한 경우

세부 규칙과 표현 방식은 `skills/caveman/SKILL.md`를 단일 source로 따릅니다.
