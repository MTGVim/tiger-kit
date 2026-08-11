# 동작 검증

## 정확한 대상과 신뢰된 입력

정확한 control을 식별합니다. 찾지 못하면 비슷한 label의 button을 반복 탐색하지
말고 mode, tab, scroll, toggle 상태를 inspect합니다.

provider-native trusted pointer와 keyboard API를 사용합니다. `evaluate_script` 는
상태, computed value, coordinate를 관찰할 때만 사용합니다. `element.click()`,
`form.submit()`, `dispatchEvent()` 를 interaction 근거로 절대 취급하지
않습니다.

mutation claim에는 관련 network request와 response가 필요합니다. Acceptance
검증은 하나의 흐름에서 UI transition, request/response, 최종 UI 상태를
연결합니다. response, toast 또는 local DOM change만으로는 불충분합니다.

## 조건부 상태와 대화상자

특정 API 상태에서만 UI가 나타나면 실제 전송이나 저장보다 `initScript`
response mock을 우선합니다. application이 실제로 parse하는 envelope에 맞추고,
shape를 추측하지 말고 소스 mapping을 inspect합니다.

interaction 전에 native alert/confirm handler를 설치합니다. blocking dialog가
이미 열려 있으면 계속하기 전에 accept하거나 dismiss합니다.

## 모션

CDP round-trip snapshot에 animation이 없다는 이유만으로 추론하지 않습니다.
trigger 전에 `animationstart`, `animationend`, `transitionstart`, `transitionend`,
필요한 `MutationObserver` 를 등록한 뒤 trusted 입력 후 하나의 event timeline을
inspect합니다.

Synthetic DOM probe는 pure CSS calculation에만 유효합니다. framework
mount/unmount lifecycle이 중요하면 실제 component render cycle을 통한 replay를
검증합니다.

## 필드 비우기

provider `fill(uid, "")` 가 value를 지우는지 확인합니다. empty fill이 no-op이면
nonempty value를 fill한 뒤 trusted Backspace를 사용하거나 필드 끝에서 실제
character마다 Backspace를 한 번씩 보냅니다. 저장 전에 empty value를 다시
observe합니다.
