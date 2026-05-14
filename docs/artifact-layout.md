# 산출물 구조

TigerKit은 절차 상태 파일에 의존하지 않습니다. 기본 산출물은 source reference, gap evidence, reflection record입니다.

## 기본 구조

```text
.tigerkit/
  requirements.md
  gap.md
  reflect.md

DESIGN.md
reuse-map.md
```

`.tigerkit/`는 TigerKit working material입니다. `DESIGN.md`와 `reuse-map.md`는 repo-level derived knowledge입니다.

## 파일 책임

| 파일 | 역할 |
| --- | --- |
| `.tigerkit/requirements.md` | source-of-truth reference index. 외부 source는 reference만 저장하고 현재 session 직접 사용자 인터뷰만 local text로 보존 |
| `.tigerkit/gap.md` | specific SOT reference와 specific code baseline 사이 evidence-based comparison 기록 |
| `.tigerkit/reflect.md` | session-wide reflection. durable learning, one-off correction, derived doc proposal 분리 |
| `DESIGN.md` | architecture, boundaries, data flow, UI/API conventions, stable constraints, non-goals 같은 derived repo-level design knowledge |
| `reuse-map.md` | reusable component/hook/util/API client/pattern/test helper와 deprecated pattern reference |

## requirements.md

`requirements.md`는 source of truth가 아닙니다. source of truth 위치를 가리키는 index입니다.

외부 source는 reference만 저장합니다.

- URL
- file path
- ticket link
- Figma link
- PRD link
- issue link
- API docs link
- source code path
- commit hash

직접 사용자 인터뷰는 local text로 저장할 수 있습니다. raw와 derived interpretation을 분리합니다.

```md
# TigerKit Requirements Index

## External Sources

- PRD: https://...
- Figma: https://...
- GitHub Issue: https://...
- Source Code: src/...
- Commit: abc1234

## Interviewed Requirements

### Raw

> 사용자 원문에 가까운 내용

### Derived Interpretation

- 명시적으로 파생 해석임을 표시

## Ambiguities

- 확인되지 않은 점과 확인이 필요한 source
```

## gap.md

`gap.md`는 TigerKit의 중심 기록입니다.

각 gap은 아래 비교를 명시합니다.

```text
specific SOT reference
vs
specific code baseline
```

baseline 기준:

- clean working tree + HEAD commit hash

각 gap shape:

```md
## GAP-001 — Short title

Type: mismatch | missing | ambiguity | drift | unknown
Resolution: open | resolved | needs-confirmation

### Compared SOT

- Source: PRD
- Reference: https://...
- Section: ...

### Compared Code

- Baseline: abc1234
- Files inspected:
  - src/...

### Evidence

SOT:
> exact excerpt or pointer

Code:
> exact excerpt or pointer

### Finding

관찰된 차이.

### Interpretation

증거에서 파생한 해석. 없으면 생략 가능.

### Required Resolution

확인 또는 변경 기준. 실행 대기열 아님.
```

## reflect.md

`reflect.md`는 session-wide reconstruction입니다. 저장된 진행 상태에 의존하지 않습니다.

권장 구조:

```md
# TigerKit Reflection

## Session Evidence Reviewed

- Conversation/session
- .tigerkit/requirements.md
- .tigerkit/gap.md
- Diff or commit: ...

## Durable Learnings

- Evidence가 있는 future-facing learning

## One-off Corrections

- 이번 session에만 해당하는 correction

## Proposed DESIGN.md Updates

- 제안 또는 적용 내역

## Proposed reuse-map.md Updates

- 제안 또는 적용 내역
```

## DESIGN.md

`DESIGN.md`는 derived repo-level knowledge입니다. 외부 SOT를 대체하지 않습니다.

담을 수 있는 것:

- architecture overview
- feature boundaries
- data flow
- UI conventions
- API integration patterns
- stable constraints
- non-goals
- repo-specific design decisions

## reuse-map.md

`reuse-map.md`는 기존 code 재사용을 돕는 leverage map입니다.

구체 reference를 선호합니다.

```md
## Components

### Button

Path:
- src/components/Button.tsx

Use when:
- Standard button UI가 필요할 때.

Known variants:
- primary
- secondary
- ghost

Example usage:
- src/features/example/ExampleForm.tsx
```

inspect하지 않은 capability, prop, behavior를 기록하지 않습니다.
