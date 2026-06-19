---
description: Deprecated. TigerKit Slim에서 /tk:review는 active command surface가 아닙니다.
argument-hint: ""
---

`/tk:review`는 TigerKit Slim에서 active command surface가 아닙니다.

## Deprecated behavior

아래 launch-era loop 책임은 제거되었습니다.

- frozen workflow target 대비 post-launch verdict
- `REVIEW_PASS`, `REVIEW_PARTIAL`, `REVIEW_FAIL`, `REVIEW_BLOCKED` loop
- launch receipt 기반 duplicate review guard

## Migration

SoT와 Current Implementation의 차이는 `/tk:gap`으로 확인합니다. 설계, 계획, 변경안, reviewer 판단을 압박 검증해야 하면 active optional command인 `/tk:grill`을 사용합니다. 코드 품질이나 merge readiness 판단 위임이 필요하면 `/tk:afk`에서 `reviewer` Patron을 decision point 단위로 호출합니다.
