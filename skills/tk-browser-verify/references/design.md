# 디자인 충실도

제공된 Figma frame, screenshot, 이전 프로덕션 또는 명세와 비교하세요. Figma 대응 frame이 있으면 동일한 viewport, DPR, browser, font, assets, zoom으로 재현하고 overlay 또는 pixel diff를 사용하세요.

비교에서 발견한 모든 차이는 `defect`, `documented deviation`, `unverifiable` 중 하나로 분류하세요. 설명되지 않은 차이는 `Fail`입니다. deviation을 기록할 때는 `region`, `difference`, `reason`, `basis`를 모두 적으세요.

`## Evidence`에 Figma 대상과 비교 screenshot, viewport 조건, visual result를 함께 기록하고, `deviation matrix`에 각 차이의 분류와 필수 필드를 남기세요. 대응 frame이나 동일 조건을 확보할 수 없으면 비교를 추정하지 말고 `Unverifiable`로 보고하세요.
