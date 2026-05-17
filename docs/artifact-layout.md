# 산출물 구조

TigerKit은 절차 상태 파일에 의존하지 않습니다. 기본 산출물은 branch-local source reference, gap evidence, reflection record, handoff contract입니다.

## 기본 구조

```text
.tigerkit/
  branches/
    feature__example/
      requirements.md
      gap.md
      reflect.md
      handoff.md

DESIGN.md        # existing-only, not created by TigerKit
reuse-map.md
CLAUDE.md        # repo instruction; managed section은 없으면 강한 반영 추천 후보
```

`.tigerkit/branches/{escaped-branch}/`는 TigerKit working material입니다. `DESIGN.md`와 `reuse-map.md`는 repo-level derived knowledge입니다. `CLAUDE.md`는 repo instruction이며 TigerKit managed section 후보를 가질 수 있습니다. managed section이 없으면 `/tk:prep`와 `/tk:reflect`는 이후 반영을 강하게 추천할 고우선 후보로 다뤄야 합니다.

Root-level `.tigerkit/requirements.md`, `.tigerkit/gap.md`, `.tigerkit/reflect.md` are deprecated artifacts. TigerKit commands should treat them as migration candidates, not active write targets.

`{escaped-branch}` is collision-safe path encoding of current git branch. ASCII letter, digit, `.`, `_`, `-` stay unchanged; other bytes encode as `~HH` uppercase hex. Example: `feature/foo` → `feature~2Ffoo`, `feature__foo` → `feature__foo`.

TigerKit branch-local artifacts are not written on detached HEAD or protected branches (`main`, `master`, `develop`). Switch to a feature branch before running write commands.

## 파일 책임

| 파일 | 역할 |
| --- | --- |
| `.tigerkit/branches/{escaped-branch}/requirements.md` | source-of-truth reference index. 외부 source는 reference만 저장하고 현재 session 직접 사용자 인터뷰만 local text로 보존 |
| `.tigerkit/branches/{escaped-branch}/gap.md` | specific SOT reference와 specific code baseline 사이 evidence-based comparison 기록 |
| `.tigerkit/branches/{escaped-branch}/reflect.md` | session-wide reflection. durable learning, one-off correction, escalation candidate 분리 |
| `.tigerkit/branches/{escaped-branch}/handoff.md` | 다음 모델/세션을 위한 continuation contract, artifact map, baseline checkpoint |
| `CLAUDE.md` | repo instruction. TigerKit managed section은 사용자 승인 후만 추가/갱신 |
| `DESIGN.md` | architecture, boundaries, data flow, UI/API conventions, stable constraints, non-goals 같은 derived repo-level design knowledge. 파일이 없으면 생성하지 않으며, 반영할 derived design knowledge가 있을 때만 초기화 필요를 알림 |
| `reuse-map.md` | reusable component/hook/util/API client/pattern/test helper와 deprecated pattern reference |

## requirements.md

`requirements.md`는 source of truth가 아닙니다. source of truth 위치를 가리키는 branch-local index입니다.

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

- feature branch
- clean working tree
- HEAD commit hash

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

`reflect.md`는 session-wide reconstruction입니다. 현재 대화 context를 primary source로 사용하고, artifact와 git evidence는 보조 근거로만 사용합니다.

권장 구조:

```md
# TigerKit Reflection

## Session Evidence Reviewed

- Current conversation context: primary
- Explicit user confirmation
- .tigerkit/branches/{escaped-branch}/requirements.md: supporting evidence
- .tigerkit/branches/{escaped-branch}/gap.md: supporting evidence
- .tigerkit/branches/{escaped-branch}/handoff.md: supporting evidence, if present
- Diff or commit: supporting evidence
- 확인 불가: context에 남아 있지 않은 내용

## Durable Learnings

- Evidence가 있는 future-facing learning

## One-off Corrections

- 이번 session에만 해당하는 correction

## Escalation Candidates

### CLAUDE.md

- repo instruction 또는 TigerKit managed section 후보
- managed section이 없으면 약한 후보가 아니라 실제 반영을 강하게 추천할 고우선 candidate

### MEMORY.md

- 사용자 preference, project direction, reference, feedback 후보

### DESIGN.md

- architecture, boundary, data flow, stable design decision 후보

### reuse-map.md

- inspect한 component/hook/util/API/pattern 재사용 정보 후보
```

`reflect.md` 갱신과 durable artifact 반영은 분리합니다. 사용자 승인 전에는 `CLAUDE.md`, `MEMORY.md`, `DESIGN.md`, `reuse-map.md`를 수정하지 않습니다.

## handoff.md

`handoff.md`는 다음 모델/세션을 위한 continuation contract입니다. task queue가 아니며, handoff-read는 현재 repo 상태로 stale 여부를 먼저 확인해야 합니다.

권장 구조:

```md
# TigerKit Handoff

## Current Goal

## Write-Time Context

- Branch:
- HEAD:
- Working tree:
- Last verification:

## TigerKit Artifact Map

### Requirements Index

- Path:
- Status:
- Relevant entries:

### Gap Records

- Path:
- Status:
- Open gaps:
- Resolved gaps:

### Reflection

- Path:
- Status:
- Escalation candidates:

## Decisions

## Evidence

## Interpretation

## Not Confirmed

## Ambiguities

## Open Questions

## Next Safe Actions

## Do Not Do

## Key Files To Read First
```

## CLAUDE.md

TigerKit은 `CLAUDE.md`에 managed section 추가 또는 갱신을 제안할 수 있습니다. 특히 managed section이 없으면 단순 optional suggestion이 아니라 실제 반영을 강하게 추천할 고우선 후보로 제시합니다. 직접 반영은 `/tk:reflect` escalation gate에서 사용자 승인 후에만 수행합니다.

Marker:

```md
<!-- TIGERKIT:START -->
<!-- TIGERKIT:END -->
```

`CLAUDE.md`가 없으면 TigerKit이 자동 생성하지 않습니다.

## DESIGN.md

`DESIGN.md`는 derived repo-level knowledge입니다. 외부 SOT를 대체하지 않습니다. 파일이 없으면 TigerKit이 생성하지 않습니다. `DESIGN.md`에 넣을 derived design knowledge가 있으면 사용자에게 초기화 필요를 알립니다.

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

## 분류 규칙

```text
Decision = 사용자 또는 SOT가 확정
Evidence = 직접 관찰
Interpretation = evidence에서 추론
Not Confirmed = 아직 확인하지 않음
Ambiguity = 확인했지만 source가 결론을 지지하지 않거나 source끼리 충돌
```

모호하지 않은 항목을 ambiguity로 승격하지 않습니다. 아직 확인하지 않은 항목은 `Not Confirmed`로 둡니다.
