# 시각 검증

## Runtime evidence

Guard mode에서 렌더·레이아웃·스타일이 맞다고 주장하려면 실제 screenshot과 필요한 computed 상태를 함께 확인하세요. 단순 network·DOM 탐색에는 screenshot을 강제하지 않습니다. 진입 flow가 불안정해 순수 CSS 거동만 확인한다면 실제 production CSS class를 그대로 사용한 요소를 DOM에 주입할 수 있지만 그 우회를 명시하세요.

Verdict mode에서는 browser session을 시작한 뒤의 성공·실패·runtime 차단 최종 상태마다 screenshot을 저장하고 이미지 자체를 실제 분석하세요. 캡처만 했거나 이미지 분석이 없으면 해당 상태는 증거가 아니며 전체 판정은 `Unverifiable`입니다. Browser 실행 전에 intent 선택을 기다리는 preflight `Blocked`에는 screenshot을 요구하지 말고 `## Alignment` decision receipt를 남기세요.

## Viewport와 hover

Verdict mode의 기본 viewport 너비는 `500, 800, 1200, 1600, 1920, 2400`px입니다. 500px 미만을 지원하면 `375` 또는 `390`px를 추가하고, breakpoint `b`를 발견하면 `b-1`, `b`, `b+1`px를 추가하세요. Guard mode는 요청한 상태와 너비만 확인합니다.

Breakpoint 경계를 판정하기 전에 `window.innerWidth`를 실측하세요. 요청 너비와 다르면 목표 breakpoint를 확실히 넘는 값으로 재설정하세요. Hover 의존 CSS는 rest 상태 computed 값으로 판정하지 말고 trusted hover 후 다시 측정하세요.

각 Verdict mode 너비에서 overflow, clipping, overlap, wrapping, truncation, alignment, spacing, sticky/fixed 요소, off-screen control을 검사하고 결과를 기록하세요.

## Migration baseline

Component 또는 primitive 교체는 color와 size만 보지 말고 영향받는 `fontWeight`, `fontSize`, `borderRadius`, `justifyContent`, `padding` 등 전체 style 축을 baseline과 computed 비교하세요. Content-width와 full-width 또는 stretch 소비처를 모두 포함하고 rem 값을 비교하기 전에 양쪽 환경의 root font size가 같은지 확인하세요.

## Evidence

Verdict mode의 `## Evidence`에는 각 너비의 width, screenshot 경로, visual result를 남기고 누락된 너비·screenshot·분석은 `## Unverified`에 명시하세요. 발견 사항은 관찰된 이미지와 연결하고 발견 사항을 뒷받침하지 않는 캡처는 증거로 세지 마세요.
