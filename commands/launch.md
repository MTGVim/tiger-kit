---
description: Deprecated. TigerKit Slim에서 /tk:launch는 active command surface가 아닙니다.
argument-hint: ""
---

`/tk:launch`는 TigerKit Slim에서 제거된 launch-era command입니다.

현재 active flow는 아래입니다.

```text
/tk:gap      # SoT ↔ Current one-shot gap analysis
/tk:afk      # temporary Patron decision delegation
/tk:reflect  # session learning extraction
/tk:setup    # setup and preferences
```

## Deprecated behavior

아래 실험은 종료되었습니다.

- sealed launch workflow execution
- workflow freezing
- mandatory `tk-runner`
- autopilot recovery
- embedded acceptance review loop
- launch receipt as primary pipeline

## Migration

기존 `/tk:launch`가 하던 “실행 계획 수행”은 TigerKit core가 담당하지 않습니다. `/tk:gap`은 수정 방향을 보고하고, 실제 구현은 사용자의 명시 지시와 현재 세션의 일반 작업 흐름을 따릅니다.

필요하면 `/tk:afk`로 불확실한 decision point만 Patron에게 위임하고, `/tk:reflect`로 세션 learning을 정리합니다.
