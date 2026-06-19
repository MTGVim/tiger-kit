# Launch 중심 구조에서 TigerKit Slim으로 migration

TigerKit Slim은 sealed launch workflow 실험을 종료하고 작은 메타 스킬 키트로 축소한다.

## 종료된 실험

- gap 기반 자율주행
- `/tk:launch`
- workflow freezing
- mandatory advisor/runner 구조
- `/tk:next`, `/tk:handoff`, `/tk:meta-feedback` 같은 launch-era continuation command
- 외부 도구 직접 내장

## 새 중심 구조

```text
gap     = SoT ↔ Current one-shot gap analysis
grill   = 설계/계획/변경안 압박 검증용 optional active micro command
afk     = Patron 기반 사용자 의사결정 위임
reflect = 세션 학습과 개선 추출
config  = TigerKit 설정, Patron, Vowline, 추천 도구 관리
```

## Command migration

| 기존 | Slim 처리 | 대체 |
|---|---|---|
| `/tk:launch` | deprecated, manifest에서 제거 | 사용자의 명시 구현 지시 + 일반 세션 작업 흐름 |
| `/tk:next` | deprecated, manifest에서 제거 | 사용자가 다음 목표를 제시하거나 `/tk:gap` 재실행 |
| `/tk:handoff` | deprecated, manifest에서 제거 | 일반 작업 요약 요청 |
| `/tk:meta-feedback` | deprecated, manifest에서 제거 | `/tk:reflect`의 learning 후보 |
| `/tk:review` | deprecated, manifest에서 제거 | `/tk:gap` 또는 `/tk:afk` reviewer Patron |
| `/tk:gap --review` | compatibility 계약 제거 | `/tk:gap` one-shot report |

## 보존되는 원칙

- evidence와 interpretation을 분리한다.
- source conflict를 조용히 병합하지 않는다.
- producer absence claim에는 producer-side evidence를 요구한다.
- UI copy는 confirmed contract가 exact copy를 요구하면 exact match로 비교한다.
- generated artifact는 durable repo rule이 아니다.

## 제거된 책임

- workflow artifact hash seal
- launch preflight와 runner dispatch
- `tk-runner` 필수 실행
- `tk-reviewer` embedded acceptance loop
- autopilot recovery
- branch-local continuation queue
- launch receipt 기반 reflect trace

## Migration 결과 기준

Slim manifest에는 active command로 `/tk:gap`, `/tk:afk`, `/tk:reflect`, `/tk:config`, `/tk:setup`과 optional active micro command `/tk:grill`을 포함한다. Deprecated command 파일은 기록과 migration 안내를 위해 남길 수 있지만 active plugin surface가 아니다.
