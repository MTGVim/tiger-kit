---
description: Deprecated. TigerKit Slim에서 /tk:meta-feedback는 active command surface가 아닙니다.
argument-hint: ""
---

`/tk:meta-feedback`는 TigerKit Slim에서 active command surface가 아닙니다.

## Deprecated behavior

아래 별도 command 책임은 제거되었습니다.

- TigerKit command/skill friction만 별도 command로 일반화
- privacy gate 기반 issue draft 출력
- handoff/next/reflect와의 routing command surface 유지

## Migration

TigerKit 자체 개선 learning은 `/tk:reflect`가 세션 learning 후보로 추출합니다. repo shared `CLAUDE.md`는 suggest-only이며, user-level 또는 Patron profile 개선은 reflect policy에 따릅니다.
