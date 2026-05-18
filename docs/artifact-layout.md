# 산출물 구조

TigerKit은 절차 상태 파일에 의존하지 않습니다. 기본 산출물은 branch-local source reference, gap evidence, 회고 기록, 인계 계약입니다.

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

Root-level `.tigerkit/requirements.md`, `.tigerkit/gap.md`, `.tigerkit/reflect.md`는 deprecated artifact입니다. TigerKit 명령은 이를 active write target이 아니라 migration candidate로만 다룹니다.

`{escaped-branch}`는 현재 git branch의 collision-safe path encoding입니다. ASCII letter, digit, `.`, `_`, `-`는 그대로 두고 다른 byte는 `~HH` uppercase hex로 encode합니다. 예: `feature/foo` → `feature~2Ffoo`, `feature__foo` → `feature__foo`.

TigerKit branch-local artifact는 detached HEAD나 protected branch(`main`, `master`, `develop`)에서 쓰지 않습니다. write command 실행 전 feature branch로 전환합니다.

## 파일 책임

| 파일 | 역할 |
| --- | --- |
| `.tigerkit/branches/{escaped-branch}/requirements.md` | source-of-truth reference index. 외부 source는 reference만 저장하고 현재 session 직접 사용자 인터뷰만 local text로 보존 |
| `.tigerkit/branches/{escaped-branch}/gap.md` | 특정 SOT reference와 특정 code baseline 사이 evidence-based comparison 기록 |
| `.tigerkit/branches/{escaped-branch}/reflect.md` | session-wide reflection. 지속 학습, 일회성 correction, escalation candidate 분리 |
| `.tigerkit/branches/{escaped-branch}/handoff.md` | 다음 모델/세션을 위한 continuation contract, artifact map, baseline checkpoint |
| `/tk:review` output | 파일 산출물이 아닌 chat compliance review. TigerKit 준수룰 위반 finding 또는 `NO_FINDINGS` |
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

직접 사용자 인터뷰는 local text로 저장할 수 있습니다. 원문과 파생 해석을 분리합니다.

API 검증 source도 source-reference-only 정책으로 기록합니다. backend 내용은 복사하지 않고, `backend repo state reference` set만 남깁니다.

- backend repo 이름
- branch policy: 조회 시점의 최신 `develop`
- 조회 시점 HEAD commit
- open PR 목록 또는 관련 PR
- endpoint/schema/source path
- 관련 API docs/ticket/issue reference

```md
# TigerKit 요구사항 인덱스

## 외부 소스 참조

- PRD 참조: https://...
- Figma 참조: https://...
- GitHub Issue 참조: https://...
- Source Code 경로: src/...
- Commit hash: abc1234

## 사용자 인터뷰 요구사항

### 원문

> 사용자 원문에 가까운 내용

### 파생 해석

- 명시적으로 파생 해석임을 표시

## 모호성

- 확인되지 않은 점과 확인이 필요한 source
```

## gap.md

`gap.md`는 TigerKit의 중심 기록입니다.

각 gap은 아래 비교를 명시합니다.

```text
특정 SOT reference
vs
특정 code baseline
```

baseline 기준:

- feature branch
- clean working tree
- HEAD commit hash

각 gap 형식:

```md
## GAP-001 — 짧은 제목

유형: 불일치 | 누락 | 모호성 | drift | 확인 불가
상태: 열림 | 해결됨 | 확인 필요

### 비교한 SOT

- Source: PRD
- 참조: https://...
- 섹션: ...

### 비교한 코드

- Baseline: abc1234
- 확인한 파일:
  - src/...

### 증거

SOT:
> exact excerpt 또는 pointer

Code:
> exact excerpt 또는 pointer

### 발견 사항

관찰된 차이.

### 해석

증거에서 파생한 해석. 없으면 생략 가능.

### 필요한 해결 기준

확인 또는 변경 기준. 실행 대기열 아님.
```

## reflect.md

`reflect.md`는 session-wide reconstruction입니다. 현재 대화 context를 primary source로 사용하고, artifact와 git evidence는 보조 근거로만 사용합니다.

권장 구조:

```md
# TigerKit 회고

## 검토한 세션 증거

- 현재 대화 context: primary source
- 명시적 사용자 확인
- .tigerkit/branches/{escaped-branch}/requirements.md: 보조 근거
- .tigerkit/branches/{escaped-branch}/gap.md: 보조 근거
- .tigerkit/branches/{escaped-branch}/handoff.md: 있으면 보조 근거
- Diff 또는 commit: 보조 근거
- 확인 불가: context에 남아 있지 않은 내용

## 지속 학습 후보

- 근거가 있는 future-facing learning

## 일회성 correction

- 이번 session에만 해당하는 correction

## 격상 후보

### CLAUDE.md

- repo instruction 또는 TigerKit managed section 후보
- managed section이 없으면 약한 후보가 아니라 실제 반영을 강하게 추천할 고우선 후보

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
# TigerKit 인계

## 현재 목표

## 작성 시점 context

- Branch:
- HEAD:
- Working tree:
- Last verification:

## TigerKit 산출물 지도

### 요구사항 인덱스

- 경로:
- 상태:
- 관련 항목:

### Gap 기록

- 경로:
- 상태:
- 열린 gap:
- 해결된 gap:

### 회고

- 경로:
- 상태:
- 격상 후보:

## 결정 사항

## 증거

## 해석

## 확인되지 않은 사항

## 모호성

## 열린 질문

## 다음 안전 조치

## 하지 말 것

## 먼저 읽을 핵심 파일
```

## `target repo CLAUDE.md`

TigerKit은 현재 작업 대상 repo의 active `CLAUDE.md`를 plugin repo `CLAUDE.md`와 구분되는 작업 규칙 배포 위치로 다룹니다.

`/tk:prep`와 `/tk:reflect`는 아래를 확인할 수 있습니다.

- active `CLAUDE.md` 존재 여부
- managed section 존재 여부
- 현재 plugin이 권장하는 규칙 포함 여부

누락되었거나 오래되어 현재 권장 규칙과 맞지 않으면 사용자에게 업데이트 여부를 묻습니다. 사용자 승인 전에는 수정하지 않습니다.

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

- architecture 개요
- feature boundary
- data flow
- UI convention
- API integration pattern
- stable constraint
- non-goal
- repo-specific design decision

## reuse-map.md

`reuse-map.md`는 기존 code 재사용을 돕는 leverage map입니다.

`reuse-map.md`는 cache-0 discovery aid이며 source of truth가 아닙니다.

- 항목이 있으면 먼저 검토할 reuse candidate로 다룹니다.
- 항목이 없다는 사실은 reusable module이 없다는 evidence가 아닙니다.
- 항목이 없다는 사실은 새 구현 생성 허가가 아닙니다.
- 새 component/hook/util/mapper/API client/layout primitive/UI pattern을 만들기 전에는 repo-wide exploration pass가 필요합니다.

구체 reference를 선호합니다.

```md
## 컴포넌트

### Button

경로:
- src/components/Button.tsx

사용 조건:
- standard button UI가 필요할 때.

확인한 variant:
- `primary`
- `secondary`
- `ghost`

사용 예시:
- src/features/example/ExampleForm.tsx
```

inspect하지 않은 capability, prop, behavior를 기록하지 않습니다.

## 분류 규칙

```text
결정 = 사용자 또는 SOT가 확정
증거 = 직접 관찰
해석 = evidence에서 추론
확인되지 않음 = 아직 확인하지 않음
모호성 = 확인했지만 source가 결론을 지지하지 않거나 source끼리 충돌
```

모호하지 않은 항목을 모호성으로 승격하지 않습니다. 아직 확인하지 않은 항목은 `확인되지 않음`으로 둡니다.
