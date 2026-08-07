# 조건부 accessibility 검증

현재 scope에 form, dialog, navigation, keyboard shortcut 또는 focus behavior가
포함될 때만 적용합니다. visual-only layout check에 complete checklist를
강제하지 않습니다.

## Evidence

- **Keyboard path:** 실제 flow에 필요한 trusted `Tab`, `Shift+Tab`, `Enter`,
  `Space`, `Escape`, arrow-key input을 사용합니다.
- **Focus:** visible focus, 합리적인 initial dialog target, close 후 trigger로의
  return, modal focus containment를 확인합니다.
- **Accessible name:** control, link, dialog가 목적을 설명하는 name을 expose하는지
  관찰합니다.
- **Errors:** validation error가 해당 field와 연결되고 focus 또는 announcement로
  discoverable한지 확인합니다.
- **State:** expanded, selected, checked, disabled visual state가 semantic state와
  일치하는지 확인합니다.

Screenshot은 visible-focus와 layout claim을 지원하지만 keyboard reachability,
accessible name, error association을 증명하지는 않습니다. DOM/accessibility-tree
evidence만으로는 visible focus를 증명할 수 없습니다.

## Scope facts

inspected flow, keyboard path, focus result, semantic evidence, findings, omitted
scope를 기록합니다. 제한된 rule set이나 단일 flow로 full WCAG 또는 product-wide
accessibility conformance를 주장하지 않습니다.
