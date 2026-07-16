# 동작 검증

## 정확한 타겟과 trusted 입력

조작할 control을 정확히 식별하세요. 타겟을 찾지 못하면 유사 label의 button을 순회하지 말고 현재 mode, tab, scroll, toggle 상태를 먼저 조사하세요.

클릭과 입력은 browser provider의 trusted pointer·keyboard API를 사용하세요. `evaluate_script`는 상태, computed 값, 좌표 같은 관측에만 사용하고 `element.click()`, `form.submit()`, `dispatchEvent()`를 실제 상호작용 증거로 사용하지 마세요.

Mutation 성공을 주장하면 관련 network request와 response를 확인하세요. Verdict mode의 변경 작업은 UI transition, network request/response, 최종 UI 상태를 하나의 흐름으로 연관 지으세요. 요청이나 응답만, 또는 토스트·국소 DOM 변경만으로는 충분하지 않습니다.

## Gated 상태와 dialog

특정 API 상태에서만 보이는 UI는 실제 발송·저장 대신 가능한 경우 상호작용 전에 `initScript`로 response를 mock해 도달하세요. 성공·실패 mock은 애플리케이션이 실제 파싱하는 response envelope와 일치해야 하며, 소스에서 response mapping을 확인하지 않고 shape을 추정하지 마세요.

Native alert·confirm은 상호작용 전에 dialog handler를 준비하세요. 이미 blocking dialog가 열렸다면 accept 또는 dismiss로 처리한 뒤 계속하세요.

## Motion

Animation과 transition은 CDP round-trip polling snapshot만으로 부재를 단정하지 마세요. Trigger 전에 `animationstart`, `animationend`, `transitionstart`, `transitionend` listener와 필요한 `MutationObserver`를 등록하고, trusted 입력 후 event timeline을 한 번에 확인하세요.

합성 DOM probe는 순수 CSS 계산에만 사용하세요. Framework mount·unmount lifecycle이 관여하면 실제 component render cycle로 재생 여부를 확인하세요.

## Field clearing

Provider에서 `fill(uid, "")`가 기존 값을 지우는지 확인하세요. 빈 문자열 fill이 no-op이면 non-empty 값으로 fill한 뒤 trusted Backspace를 사용하거나, field 끝에서 실제 문자 수만큼 Backspace를 보내세요. 저장 전에 snapshot 또는 동등한 관측으로 value가 실제 빈 문자열인지 재확인하세요.
