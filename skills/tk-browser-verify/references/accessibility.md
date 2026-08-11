# 조건부 접근성 검증

현재 범위에 form, dialog, navigation, keyboard shortcut 또는 focus 동작이
포함될 때만 적용합니다. visual-only layout check에 complete checklist를
강제하지 않습니다.

## 근거

- **Keyboard 경로:** 실제 흐름에 필요한 trusted `Tab`, `Shift+Tab`, `Enter`,
  `Space`, `Escape`, arrow-key 입력을 사용합니다.
- **Focus:** 표시되는 focus, 합리적인 초기 dialog 대상, 닫은 뒤 trigger로의
  복귀, modal focus containment를 확인합니다.
- **Accessible name:** control, link, dialog가 목적을 설명하는 name을
  노출하는지 관찰합니다.
- **Errors:** validation error가 해당 필드와 연결되고 focus 또는 announcement로
  발견 가능한지 확인합니다.
- **State:** expanded, selected, checked, disabled visual 상태가 semantic
  상태와 일치하는지 확인합니다.

Screenshot은 표시되는 focus와 layout 주장을 뒷받침하지만 keyboard reachability,
accessible name, error association을 증명하지는 않습니다. DOM/accessibility-tree
근거만으로는 표시되는 focus를 증명할 수 없습니다.

## 범위 사실

검사한 흐름, keyboard 경로, focus 결과, semantic 근거, 발견 사항, 제외한
범위를 기록합니다. 제한된 rule set이나 단일 흐름으로 full WCAG 또는
product-wide accessibility conformance를 주장하지 않습니다.
