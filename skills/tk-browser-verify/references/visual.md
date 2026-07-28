# 시각 검증

## Runtime evidence

Guard mode에서 렌더·레이아웃·스타일이 맞다고 주장하려면 실제 screenshot과 필요한 computed 상태를 함께 확인하세요. 단순 network·DOM 탐색에는 screenshot을 강제하지 않습니다. 진입 flow가 불안정해 순수 CSS 거동만 확인한다면 실제 production CSS class를 그대로 사용한 요소를 DOM에 주입할 수 있지만 그 우회를 명시하세요.

Verdict mode에서는 browser session을 시작한 뒤의 성공·실패·runtime 차단 최종 상태마다 screenshot을 저장하고 이미지 자체를 실제 분석하세요. 캡처만 했거나 이미지 분석이 없으면 해당 상태는 증거가 아니며 전체 판정은 `Unverifiable`입니다. Browser 실행 전에 intent 선택을 기다리는 preflight `Blocked`에는 screenshot을 요구하지 말고 `## Alignment` decision receipt를 남기세요.

## Instrumented evidence

Guard와 Verdict mode에서 대상 상태가 인증 gate 뒤에 있으면서 불안정한 외부 호출로만 발생하거나, 자동 해제 timer 때문에 관찰 창이 왕복 시간보다 짧을 때만 임시 계측을 허용하세요. Verdict evidence에는 `Evidence class: instrumented`와 이유를 기록하세요.

다음 최소 침습 순서를 지키고 다음 단계로 내려갈 때 직전 단계가 불가능한 근거를 남기세요.

1. source 변경 없는 기존 DOM/class/state toggle
2. 실제 production class를 사용한 격리 DOM 주입
3. source 임시 계측

Timer가 관찰 전에 상태를 지우면 정식 setter뿐 아니라 해제를 hold하는 임시 변형도 제공하세요. Source 계측은 ticket/run 식별자가 있는 `TEMP(<id>)` marker로 범위를 닫으세요. 관찰 뒤 원상복구하고 대상 파일의 `git diff --stat`이 계측 전 상태와 같음, marker 검색 0건, commit diff에 marker/계측 delta 없음의 세 증거를 실측하세요. 하나라도 확인할 수 없으면 `Residue check: unverifiable`과 전체 `Unverifiable`을 반환하세요.

구동원이 비결정적이라 agent가 재현할 수 없을 때만 사용자 육안 판정을 위임 evidence로 허용하세요. `Evidence class: user-observed`, `Computed: not recorded`, 위임 이유를 그대로 표시하고 computed 측정처럼 보고하지 마세요. 직접 관측이 값싸게 가능하면 위임으로 대체하지 마세요.

## Runtime diagnosis and controls

Runtime `Fail`에는 `change-related | pre-existing | environment` 원인 분류를 붙이세요. `pre-existing`은 배포 기준이나 기준 branch 같은 baseline 환경에서 동일 절차로 재현한 evidence가 있을 때만 허용하고, baseline에 접근할 수 없으면 미확인으로 남기세요.

선언값과 computed 값이 다르면 component logic을 먼저 탓하지 마세요. `document.styleSheets`를 순회해 실제로 이긴 selector와 `cssText`를 특정하고, 조상 state class가 원인이면 runtime에서 그 class가 해제되는지 실측하세요. jsdom처럼 CSS specificity를 구현하지 않는 DOM simulator는 cascade 판정 oracle이 아닙니다.

원인을 특정한 수정의 Verdict에는 같은 runtime에서 positive와 negative control을 모두 실행하세요. Production code를 되돌리지 말고 CSS는 구 selector 형태의 `<style>`과 probe를, logic은 구 구현을 별도 함수로 주입해 같은 입력의 실패를 재현하세요. 주입물은 위 instrumented residue gate로 제거합니다. Negative가 실패를 재현하지 않으면 causal explanation을 `Unverifiable`로 보고하고 `Pass` 근거로 사용하지 마세요.

## Viewport와 hover

Verdict mode의 기본 viewport 너비는 `500, 800, 1200, 1600, 1920, 2400`px입니다. 500px 미만을 지원하면 `375` 또는 `390`px를 추가하고, breakpoint `b`를 발견하면 `b-1`, `b`, `b+1`px를 추가하세요. Guard mode는 요청한 상태와 너비만 확인합니다.

Breakpoint 경계를 판정하기 전에 `window.innerWidth`를 실측하세요. 요청 너비와 다르면 목표 breakpoint를 확실히 넘는 값으로 재설정하세요. Hover 의존 CSS는 rest 상태 computed 값으로 판정하지 말고 trusted hover 후 다시 측정하세요.

각 Verdict mode 너비에서 overflow, clipping, overlap, wrapping, truncation, alignment, spacing, sticky/fixed 요소, off-screen control을 검사하고 결과를 기록하세요.

## Migration baseline

Component 또는 primitive 교체는 color와 size만 보지 말고 영향받는 `fontWeight`, `fontSize`, `borderRadius`, `justifyContent`, `padding` 등 전체 style 축을 baseline과 computed 비교하세요. Content-width와 full-width 또는 stretch 소비처를 모두 포함하고 rem 값을 비교하기 전에 양쪽 환경의 root font size가 같은지 확인하세요.

## Evidence

Verdict mode의 `## Evidence`에는 각 너비의 width, screenshot 경로, visual result를 남기고 누락된 너비·screenshot·분석은 `## Unverified`에 명시하세요. 발견 사항은 관찰된 이미지와 연결하고 발견 사항을 뒷받침하지 않는 캡처는 증거로 세지 마세요.
