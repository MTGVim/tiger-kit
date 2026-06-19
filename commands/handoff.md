---
description: Deprecated. TigerKit Slim에서 /tk:handoff는 active command surface가 아닙니다.
argument-hint: ""
---

`/tk:handoff`는 TigerKit Slim에서 제거된 continuation command입니다.

## Deprecated behavior

아래 책임은 TigerKit core에서 제거되었습니다.

- branch-local continuation handoff 작성
- pending backlog queue 유지
- global-index 기반 resume pointer 관리

## Migration

세션 인계가 필요하면 일반 작업 요약을 요청하세요. TigerKit core는 `/tk:gap`, `/tk:afk`, `/tk:reflect`, `/tk:config`에 집중합니다.
