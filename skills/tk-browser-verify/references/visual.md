# 시각 검증

기본 viewport 너비는 `500, 800, 1200, 1600, 1920, 2400`px입니다. 500px 미만을 지원하면 `375` 또는 `390`px를 추가하고, breakpoint `b`를 발견하면 `b-1`, `b`, `b+1`px를 추가하세요. 각 너비에서 overflow, clipping, overlap, wrapping, truncation, alignment, spacing, sticky/fixed 요소, off-screen control을 검사하고 너비별 결과를 기록하세요.

Browser session을 시작한 뒤의 성공·실패·runtime 차단 최종 상태마다 screenshot을 저장하고 screenshot 이미지 자체를 실제 분석하세요. 캡처만 했거나 이미지 분석이 없으면 해당 상태는 증거가 아니며 전체 판정은 `Unverifiable`입니다. browser 실행 전에 intent 선택을 기다리는 preflight `Blocked`에는 screenshot을 요구하지 말고 `## Alignment` decision receipt를 남기세요. 관련 뷰포트에서 레이아웃, 반응형 동작, 오버레이, z-index, 타이포그래피 및 눈에 보이는 회귀를 함께 검사하세요.

`## Evidence`에는 각 너비의 width, screenshot 경로, visual result를 남기고, 누락된 너비·screenshot·분석은 `## Unverified`에 명시하세요. 발견 사항은 관찰된 이미지와 연결하고, 발견 사항을 뒷받침하지 않는 캡처는 증거로 세지 마세요.
