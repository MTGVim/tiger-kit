# 디자인 충실도

Figma frame, screenshot, 이전 프로덕션 또는 명세가 기준으로 주어지면 구현이나 browser 검증 전에 intent preflight를 수행하세요.

## Intent preflight

1. 사용자 지시를 viewport, state, region별 예상 결과로 요약하세요.
2. 디자인에서 대응 frame과 node를 찾고 실제 보이는 간격을 page/frame inset, layout container padding·gap, component padding, child margin·gap, border·stroke의 중첩 결과로 분해하세요. 측정된 전체 간격을 한 요소의 padding으로 단정하지 마세요.
3. `Instruction | Design basis | Spacing stack | Relation | Expected implementation | User decision | Status`를 비교하고 `Relation`은 `same | different | unclear`, 사용자 정렬 `Status`는 `confirmed | pending | Blocked`로 기록하세요. Status를 runtime Verdict로 사용하지 마세요.
4. `same`이면 재확인을 요구하지 말고 runtime screenshot capture와 실제 image 검사 계획으로 진행하세요.
5. `different` 또는 `unclear`이면 상호 배타적인 선택지를 제시하세요. 각 선택에 viewport·region별 visibility, 위치와 spacing을 포함한 구체적 최종 UI, 충족하는 기준, 위반하거나 deviation이 되는 기준을 적고 사용자에게 하나를 명시적으로 선택하도록 질문하세요.
6. 명시적 답을 받을 때까지 구현과 browser 실행을 시작하지 말고 `## Verdict`를 `Blocked`로 반환하세요. 이는 browser session 전 의사결정 상태이므로 screenshot이 필요하지 않으며 screenshot 부재를 이유로 `Unverifiable`로 바꾸지 않습니다. 침묵은 동의가 아니며 `User decision: pending`, `Status: Blocked`를 유지하세요.
7. 사용자가 차이를 승인한 경우에만 답변 근거와 적용 범위를 기록하고 `documented deviation`으로 분류하세요. 승인하지 않았으면 디자인 기준에 맞추고, 선택이 없으면 미해결 상태를 유지하세요.

## Visual comparison

Figma 대응 frame이 있으면 확인된 intent를 기준으로 동일한 viewport, DPR, browser, font, assets, zoom을 재현하고 overlay 또는 pixel diff를 사용하세요.

비교에서 발견한 모든 차이는 `defect`, `documented deviation`, `unverifiable` 중 하나로 분류하세요. 설명되지 않은 차이는 `Fail`입니다. deviation을 기록할 때는 `region`, `difference`, `reason`, `basis`를 모두 적고, `basis`에는 사용자 확인 또는 기존 명세 근거를 포함하세요.

디자인 기준이 있으면 `## Alignment`를 필수로 출력하고 intent 비교와 사용자 결정을 기록하세요. `## Evidence`에는 Figma 대상과 비교 screenshot, viewport 조건, visual result를 함께 기록하고, `deviation matrix`에 각 차이의 분류와 필수 필드를 남기세요. browser session을 시작한 뒤 대응 frame, spacing 계층 또는 동일 조건을 확보할 수 없으면 비교를 추정하지 말고 `Unverifiable`로 보고하세요.
