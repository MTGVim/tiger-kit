# HTML 테마 마크업과 목차 계약 보완

사용자가 제공한 생성 HTML 사고 근거를 공용 HTML 계약과 기존 보고서 검사에 반영한다.
CSS의 `input + span` 계약과 기존 QA 템플릿을 기준으로 상단 바 예시를 보강한다.
목차에는 목적지 제목 전문을 보존하며, 영구 테두리 억제는 유지하고 제목에만 1.5초 표시를 추가한다.
모션 감소 설정에서는 애니메이션 없이 배경으로 목적지를 표시한다.

- 보존(`keep`): 네이티브 라디오와 해시 이동·방문 기록, 링크와 입력의 키보드 포커스, 인용 복귀 테두리 억제.
- 반영(`adapt`): 실제 사고에서 확인된 마크업 예시와 검사, 제목 전문 대응, 제목의 일시 표시.
- 제외(`omit`): 새 템플릿·검사 프레임워크·스크립트 재실행 로직. 동일 해시를 다시 클릭하면 애니메이션을 재실행하지 않는다.
- 근거: 사용자 제공 사고 기록, 기존 `tk-qa-sheet/assets/qa-sheet-template.html`, `tk-explain/assets/html-theme.css`.
- 외부 동작 확인: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:target (2026-10-19 확인).
- 정적 회귀: 필수 `span` 누락·빈 `span`·잘못된 인접 요소/입력 타입·목차 제목 누락을 실패 처리하고, 전체 제목을 포함한 짧은 라벨과 공백 정규화는 허용한다.
- `README`: 공개 카탈로그 변경 없음. 이름·설명·호출·카탈로그는 그대로이며, 변경 대상은 6개 HTML 소비 패키지의 `references/html-output.md`, `assets/html-theme.css`, 두 기존 템플릿과 `tk-research/scripts/check_report.py`이다.
