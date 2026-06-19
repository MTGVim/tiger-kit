---
description: Deprecated. TigerKit Slim에서 /tk:next는 active command surface가 아닙니다.
argument-hint: ""
---

`/tk:next`는 TigerKit Slim에서 제거된 launch-era continuation command입니다.

## Deprecated behavior

아래 책임은 TigerKit core에서 제거되었습니다.

- steering replacement continuation
- latest artifact 기반 자동 next action 선택
- safe continuation execution receipt
- handoff/launch/reflect trace를 이어서 자동 처리

## Migration

다음 작업을 정해야 하면 사용자가 직접 목표를 제시하거나 `/tk:gap`으로 SoT와 current implementation 차이를 다시 확인합니다. 불확실한 결정만 `/tk:afk`로 위임할 수 있습니다.
