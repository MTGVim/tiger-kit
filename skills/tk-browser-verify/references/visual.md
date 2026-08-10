# Visual evidence

승인된 모든 visual claim에는 non-empty runtime screenshot과 실제 image
inspection이 필요합니다. DOM, accessibility-tree, network, computed-style
evidence로 image를 대체할 수 없습니다. comparable condition 또는 required
capture가 없으면 `Unverifiable`입니다.

design/screenshot basis가 있으면 승인된 viewport, DPR, browser, font, asset, zoom을
재현한 뒤 named region/state만 비교합니다. difference는 `defect`, approved
deviation, environment 또는 unverifiable로 분류하며 design intent를 만들거나
generic critique로 넓히지 않습니다.

responsive AC에서는 실제 `window.innerWidth` 를 측정하고 named width와 breakpoint
edge를 테스트합니다. 승인된 criteria가 요구하는 경우에만 overflow, clipping,
overlap, wrapping, truncation, alignment, spacing, sticky/fixed element,
off-screen control을 inspect합니다. trusted input 후 hover/focus를 측정합니다.

temporary runtime-only DOM/response mock은 repository evidence가 exact production
envelope를 증명하고 승인된 criterion이 mocked backend가 아닌 presentation에
관한 경우에만 허용됩니다. bypass를 label하고 제거합니다. verification을 위해
source를 절대 수정하지 않습니다.

viewport, screenshot path, inspected result, limitation을 compact fact로
기록합니다. causal regression claim에는 comparable baseline runtime evidence가
필요합니다. 그렇지 않으면 현재 관찰된 failure만 보고합니다.
