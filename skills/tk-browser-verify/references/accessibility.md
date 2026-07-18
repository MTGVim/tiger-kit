# 조건부 접근성 검증

Form, dialog, navigation, keyboard shortcut 또는 focus 동작이 현재 scope에 있을 때만 적용하세요. 일반 visual-only layout 검증에 전체 checklist를 강제하지 마세요.

## Evidence

- **Keyboard path**: trusted `Tab`, `Shift+Tab`, `Enter`, `Space`, `Escape`, 방향키 중 실제 flow에 필요한 입력으로 도달·동작 가능성을 확인합니다.
- **Focus**: focus가 시각적으로 식별되고, dialog open 시 합리적인 시작점으로 이동하며, 닫힌 뒤 trigger로 복귀하는지 확인합니다. Modal이면 focus가 배경으로 빠지지 않는지 확인합니다.
- **Accessible name**: form control, button, link, dialog가 목적을 설명하는 accessible name을 갖는지 DOM/accessibility observation으로 확인합니다.
- **Errors**: validation error가 관련 field와 연결되고 focus 또는 announcement 경로에서 발견 가능한지 확인합니다.
- **State**: expanded, selected, checked, disabled 같은 상태가 시각 표현과 semantic state에서 일치하는지 확인합니다.

Screenshot은 visible focus와 layout evidence에는 유용하지만 keyboard 도달성, accessible name, error association을 대신하지 않습니다. 반대로 DOM/accessibility tree만으로 시각적 focus 성공을 주장하지 마세요.

## Scope receipt

검사한 flow, keyboard path, focus 결과, semantic evidence, 발견 사항, 미검사 범위를 기록하세요. 자동 도구가 제공하는 제한된 규칙 통과나 한 flow의 성공을 전체 WCAG conformance 또는 제품 전체 접근성 통과로 표현하지 마세요.
