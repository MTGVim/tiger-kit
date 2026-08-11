# 시각적 근거

승인된 모든 visual claim에는 non-empty 런타임 screenshot과 실제 image
inspection이 필요합니다. DOM, accessibility-tree, network, computed-style
근거로 image를 대체할 수 없습니다. comparable 조건 또는 필수
캡처가 없으면 `Unverifiable`입니다.

design/screenshot basis가 있으면 승인된 viewport, DPR, browser, font, asset, zoom을
재현한 뒤 named region/state만 비교합니다. difference는 `defect`, approved
deviation, 환경 또는 `unverifiable`로 분류하며 design intent를 만들거나
일반적인 critique로 넓히지 않습니다.

## Verbatim visual 비교 축

승인된 reference와 그대로/fidelity 비교를 수행할 때는 같은 viewport, DPR, zoom,
font-loading 완료 상태의 reference/candidate screenshot을 실제 inspect하고 아래 축을
각각 `Pass | Fail | Unverifiable`로 기록합니다. 눈에 띄는 전체 인상이나 DOM 존재만으로
축을 대체하지 않으며 필수 축 하나라도 unchecked이면 aggregate `Pass`가 아닙니다.

1. **Asset presence/integrity** — logo, SVG, icon, favicon, raster image,
   background image가 누락·대체·중복되지 않았는지 확인합니다. SVG는 element 존재만
   보지 않고 rendered shape, `viewBox`, aspect ratio, fill/stroke와 clipping을 screenshot
   및 computed 근거로 확인합니다.
2. **Content** — 표시되는 text, label, number, badge와 순서가 누락·추가·오타 없이
   reference와 일치하는지 확인합니다.
3. **Geometry/layout** — position, dimensions, spacing, alignment, radius, border,
   overlap, clipping, wrapping, crop을 named region별로 비교합니다.
4. **Typography** — loaded font family/fallback, weight, rendered font size,
   line-height, letter-spacing, text transform와 줄바꿈을 비교합니다.
5. **Color/paint** — foreground/background/border, SVG `fill`/`stroke`, opacity,
   shadow와 gradient의 computed value 및 rendered appearance를 비교합니다.
6. **Imagery** — image request/load 성공, source, intrinsic dimensions,
   aspect ratio, `object-fit`/`object-position`, crop과 해상도를 확인합니다.
7. **Responsive/state** — 승인된 viewport와 hover/focus/active/disabled/loading/error
   state마다 위 축의 차이를 다시 확인합니다.

각 발견 사항에는 axis, named element/region, reference observation, 후보 observation,
viewport/state와 inspected screenshot 경로를 연결합니다. Pixel-perfect tolerance가
승인 criteria에 없으면 임의 threshold를 만들지 말고 명백한 mismatch를 보고하며
미세 차이는 `Unverifiable`로 남깁니다.

responsive AC에서는 실제 `window.innerWidth` 를 측정하고 named width와 breakpoint
edge를 테스트합니다. 승인된 criteria가 요구하는 경우에만 overflow, clipping,
overlap, wrapping, truncation, alignment, spacing, sticky/fixed element,
off-screen control을 inspect합니다. trusted 입력 후 hover/focus를 측정합니다.

temporary 런타임-only DOM/응답 mock은 저장소 근거가 정확한 production
envelope를 증명하고 승인된 criterion이 mocked backend가 아닌 presentation에
관한 경우에만 허용됩니다. bypass를 label하고 제거합니다. 검증을 위해
소스를 절대 수정하지 않습니다.

viewport, screenshot 경로, inspected 결과, limitation을 간결한 사실로
기록합니다. causal regression claim에는 comparable baseline 런타임 근거가
필요합니다. 그렇지 않으면 현재 관찰된 실패만 보고합니다.
