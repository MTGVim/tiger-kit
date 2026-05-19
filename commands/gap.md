---
description: branch-local indexed source-of-truth reference와 reproducible code baseline을 비교해 evidence-based gap을 .tigerkit/branches/{escaped-branch}/gap.md에 기록합니다. 실행 대기열로 변환하지 않습니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. URL, 파일 경로, commit hash, ticket id, 코드 식별자, 오류 메시지는 원문 그대로 유지할 수 있습니다.

목표: `/tk:gap`은 TigerKit의 중심 명령입니다. `.tigerkit/branches/{escaped-branch}/requirements.md`에 인덱싱된 SOT reference와 특정 code baseline을 비교하고, 증거 기반 차이를 `.tigerkit/branches/{escaped-branch}/gap.md`에 기록합니다.

```text
gap = SOT reference vs commit/code comparison
```

## 기본 산출물

- `.tigerkit/branches/{escaped-branch}/gap.md`

입력 source index는 같은 branch-local directory의 `.tigerkit/branches/{escaped-branch}/requirements.md`를 우선 사용합니다.

Root-level `.tigerkit/gap.md`는 deprecated artifact입니다. 발견하면 migration 후보로만 표시하고 사용자 승인 없이 이동하지 않습니다.

## gap record state guidance

`/tk:gap`은 workflow orchestration이나 task queue 안내를 하지 않습니다. receipt에 넣는 상태 표현이 필요하면 비교 기록 관점의 현재 상태만 간단히 말합니다. 이 정보는 read-only state이며 별도 상태 artifact를 만들지 않습니다.

권장 상태 표현:

- `branch_invalid`: gap 기록을 시작할 수 없는 branch 상태
- `source_index_missing`: 비교할 SOT reference index가 부족한 상태
- `baseline_not_reproducible`: clean HEAD working tree 또는 HEAD commit hash가 없는 상태
- `comparison_in_progress`: SOT/code/reuse evidence를 비교 중인 상태
- `gap_recorded`: `.tigerkit/branches/{escaped-branch}/gap.md` 기록이 끝난 상태
- `needs_decision_gate`: gap record는 남겼지만 ambiguity, access, verification, user decision 점검이 더 필요한 상태

receipt에는 최소한 아래를 포함합니다.

- `state`: 현재 gap record 상태
- `blocked`, if applicable
- `reason`, if applicable
- `recorded`, if applicable
- `next safe action`, if applicable

## baseline rule

gap 분석 전에 code baseline을 식별합니다.

필수 baseline:

```text
clean HEAD working tree + HEAD commit hash
```

추가 branch 조건:

- detached HEAD이면 gap 기록을 시작하지 않습니다.
- `main`, `master`, `develop`이면 gap 기록을 시작하지 않습니다.
- feature branch에서 clean HEAD working tree + HEAD commit hash를 baseline으로 사용합니다.

working tree에 staged, unstaged, untracked 변경 중 하나라도 있으면 gap 기록을 시작하지 않습니다.

특히 staged 변경은 reproducible baseline이 아닙니다. 아직 commit hash가 없는 상태이므로 staged diff를 baseline으로 비교하지 않습니다. staged diff를 gap.md에 baseline evidence로 기록하지도 않습니다.

working tree가 clean하지 않으면 gap을 쓰기 전에 반드시 멈춥니다. staged 변경은 먼저 commit할 것을 강하게 권고하고, unstaged 또는 untracked 변경은 commit 또는 정리 후 rerun `/tk:gap`을 권고합니다.

blocked receipt에는 아래를 포함합니다.

- `blocked: working tree not clean`
- staged status
- unstaged status
- untracked status
- 해야 할 일

## SOT priority and conflict rule

SOT conflict는 아래 우선순위를 현재 비교 범위에 명시해서 판단합니다.

| Priority | Source | Applies to |
|---|---|---|
| P0 | Current explicit user instruction in the current session | 현재 요청에 직접 적용되는 최신 사용자 지시 |
| P1 | Binding project policy / architecture decisions / user-confirmed durable feedback | project policy, architecture, durable user-confirmed rule |
| P2 | Design SOT | visible UI, layout, spacing, border, typography, visual states, visible copy |
| P3 | Requirements / PRD / business spec | business logic, validation, permissions, workflow, data semantics, API behavior |
| P4 | Existing code baseline | actual evidence only, not authority over active SOT |
| P5 | Model inference | explicitly marked assumption only |

Conflict rule:

- Current explicit user instruction overrides older derived knowledge when directly applicable.
- Binding project policy overrides existing code.
- Existing code does not justify violating active SOT.
- Visible UI/copy/layout/style conflict에서는 design SOT가 visible target을 명시하면 requirements SOT보다 우선합니다.
- Business logic, validation condition, permission rule, workflow semantics, API behavior, data semantics는 design SOT가 기능 동작을 명시적으로 override하지 않는 한 requirements SOT가 우선합니다.
- Source category만으로 conflict를 해결할 수 없으면 추측하지 않고 `sot_conflict`로 기록합니다.
- 충돌 source를 조용히 합쳐 synthetic requirement를 만들지 않습니다.
- conflict-dependent item은 inspected evidence와 stated priority rule 없이 `Match`로 표시하지 않습니다.

## gap scope

gap 분석은 아래 3개 관점을 함께 다룹니다.

- functional
- design
- reuse

Functional 관점에는 최소한 아래를 포함합니다.

- implementation degree
- loading, error, empty state
- API, data mapping
- validation
- permission, visibility
- edge case

Design 관점에는 최소한 아래를 포함합니다.

- border
- spacing
- color
- typography
- hierarchy
- density
- alignment
- section grouping
- interaction affordance
- existing screens 또는 components와의 similarity
- fixture 표현 차이
- date/time, number, currency, line break 같은 format 차이

Figma 등 design SOT와 비교할 때는 “의미는 비슷하다”는 이유로 fixture나 format 차이를 무시하지 않습니다. copy fixture, label, placeholder, 상태 문구, `yyyy-MM-dd hh:mm:ss` vs `yyyy-MM-dd\nhh:mm:ss` 같은 줄바꿈/format 차이는 중대한 gap 사유로 기록합니다.

Visible UI text는 SOT가 variation을 명시적으로 허용하지 않는 한 exact match가 필요합니다. button label, label, placeholder, validation message, tooltip copy, toast/snackbar message, modal title, modal body copy, confirm/cancel/ok text, table column name, tab name, status label, date/time/number/currency format, 의도된 visible line break는 exact-match audit target입니다. Meaning-similar text도 exact text가 다르면 gap입니다.

Project SOT가 component, pattern, dependency를 required, avoided, banned, deprecated, preferred로 지정하면 기능이 동작해도 policy gap으로 기록합니다. `IMPLEMENTATION_POLICY.md`가 target repo에 있고 접근/inspect 가능하면 binding project policy SOT candidate로 audit합니다. Generic TigerKit 문서는 실제 package/library/vendor 이름을 deprecated example로 쓰지 않고 neutral placeholder만 사용합니다.

현재 구현 증거가 부족하면 문제 화면의 현재 DOM, accessibility tree, screenshot, rendered text, style token evidence 같은 재현 가능한 관찰 자료를 사용자에게 요청하거나 직접 수집한 뒤 비교합니다.

Reuse 관점에는 최소한 아래를 포함합니다.

- existing component, hook, util, mapper, API client 재사용 가능성
- unnecessary new implementation 여부
- unnecessary common module modification 여부
- design-system drift
- nearby screen pattern mismatch

## gap shape

각 gap은 아래 항목을 포함합니다.

- compared SOT
- compared code baseline
- inspected files
- evidence
- finding
- interpretation, if any
- resolution
- required resolution

권장 형식:

```md
## GAP-001 — Tooltip copy 불일치

유형: mismatch
상태: open

### 비교한 SOT

- Source: PRD
- 참조: https://...
- 섹션: Tooltip copy

### 비교한 코드

- Baseline: abc1234
- 확인한 파일:
  - src/...

### 증거

SOT:
> short exact excerpt 또는 pointer

Code:
> short exact excerpt 또는 pointer

### 발견 사항

PRD copy와 구현 tooltip copy가 다릅니다.

### 해석

implementation drift로 보입니다. source ambiguity는 아닙니다.

### 필요한 해결 기준

사용자 확인 또는 code update 필요.
```

## SOT access coverage

`/tk:gap`은 branch-local `requirements.md`의 SOT 접근성 manifest 또는 equivalent metadata를 확인하고, audit coverage를 gap record에 포함합니다.

필수 section:

```md
## SOT Access Coverage

| SOT ID | Source | Access Status | Used in Audit | Result |
|---|---|---|---|---|
| SOT-REQ-001 | ./docs/REQUIREMENTS.md | accessible | yes | audited |
| SOT-IMG-001 | https://.../1.1.1.png | pending_user_input | no | Not verifiable |
```

binding SOT asset이 inaccessible, auth_required, local_missing, pending_user_input, not_verifiable이면 audit이 partial임을 명시합니다.

```text
Audit is partial because 1 binding SOT asset is inaccessible.
```

## Coverage Inventory

`/tk:gap`은 complete처럼 말하기 전에 scoped SOT item 중 무엇을 비교했는지 inventory를 남깁니다. 모든 코드 line을 나열하지 않아도 되지만, audit 범위에 들어온 SOT item은 low-severity UI/copy/policy 항목까지 포함합니다.

```md
## Coverage Inventory

| Item ID | Source | Item Type | Expected / SOT Value | Actual Evidence | Compared? | Result |
|---|---|---|---|---|---|---|
| ITEM-COPY-001 | SOT-DESIGN-001 | button label | `저장` | `src/...`, rendered text `확인` | yes | Gap |
| ITEM-TABLE-001 | SOT-REQ-001 | table column | `상태` | inspected table header | yes | Match |
| ITEM-IMG-001 | SOT-IMG-001 | modal spacing | pending asset | no inspected asset | no | Not verifiable |
```

`Not verifiable`은 `Match`가 아닙니다. 비교하지 못한 item은 coverage gap으로 남기고 필요한 fallback이나 verification을 적습니다.

## Gap Table

권장 summary table:

```md
## Gap Table

| Gap ID | Source Item | Expected | Actual | Gap Type | Severity | Resolvability | Evidence | Required Handling |
|---|---|---|---|---|---|---|---|---|
| GAP-001 | ITEM-COPY-001 | `저장` | `확인` | mismatch | low | selfResolvable | rendered text + source pointer | update exact copy |
```

Severity와 resolvability는 별도 column으로 유지합니다.

접근 불가 binding asset에 의존하는 구현은 `Match`로 표시하지 않습니다. `Not verifiable`, `Coverage gap`, 또는 `pending_user_asset` resolution class로 기록합니다.

예시:

```text
resolution_class: pending_user_asset
selfResolvable: false
requires: user-provided file, local path, screenshot/export, or pasted content
```

## Decision Gate rule

각 gap은 severity와 resolvability를 분리합니다.

```text
Severity != Resolvability
```

필요한 경우 gap record에 아래 필드를 추가합니다.

```text
selfResolvable
requiresUserDecision
externalDependency
notVerifiable
needsVerification
pending_user_asset
largeOrRiskyRefactor
shouldPauseBeforeFix
blocker
safeAutoFixReason
```

분류 기준:

- `selfResolvable`: SOT가 명확하고 local low-risk fix가 가능합니다.
- `requiresUserDecision`: policy, interpretation, token, scope, behavior 선택이 필요합니다.
- `externalDependency`: backend, API, infrastructure, external owner 변경이 필요합니다.
- `notVerifiable`: SOT, document, image, file, API를 현재 inspect할 수 없습니다.
- `needsVerification`: code, type, schema, data source 확인이 필요합니다.
- `pending_user_asset`: binding SOT asset을 inspect할 수 없어 user-provided file, local path, screenshot/export, pasted content가 필요합니다.
- `largeOrRiskyRefactor`: fix 범위가 넓거나 위험해 승인 없이 auto-resolve하지 않습니다.

SOT reference에 접근할 수 없으면 내용을 추론하지 않습니다. dependent item을 `Match`로 표시하지 않고, accessible file, local path, screenshot/export, pasted content를 요청합니다. binding visual SOT는 `./docs/assets/sot/requirements/` 또는 `./docs/assets/sot/design/` 아래 stable local asset reference를 선호합니다.

high-impact ambiguity가 있으면 `/tk:checkpoint`를 실행하거나 report 안에서 checkpoint 필요성을 안내합니다. trivial copy나 local one-line fix처럼 SOT가 명확하고 safe action이 분명하면 checkpoint를 남발하지 않습니다.

`/tk:reflect`는 default next command로 추천하지 않습니다. project policy나 repeated user preference를 durable하게 남길 필요가 있을 때만 자연어로 안내합니다.

## evidence rule

중요 claim은 아래 중 하나에 근거해야 합니다.

- external SOT reference
- direct user interview text
- code path
- commit hash
- observed diff
- explicit user confirmation
- gap record
- derived artifact clearly marked as derived

항상 분리합니다.

```text
Evidence = directly observed
Interpretation = inferred from evidence
Decision = confirmed by user or SOT
Suggestion = proposed, not confirmed
```

## ambiguity rule

source가 결론을 지지하지 않으면 추측하지 않습니다.

1. ambiguity를 gap으로 기록합니다.
2. 필요하면 사용자에게 질문합니다.
3. resolved처럼 구현하거나 decision으로 저장하지 않습니다.

## COMPONENT_REUSE_MAP.md rule

`COMPONENT_REUSE_MAP.md`는 inspected reusable component, hook, utility, API client, adapter, form pattern, validation pattern, UI composition pattern, test helper, avoid/deprecated pattern의 derived map입니다. source of truth가 아닙니다.

- hit이면 review candidate입니다.
- miss는 reusable module이 없다는 evidence가 아닙니다.
- miss만으로 new component, hook, util, mapper, API client, layout primitive, UI pattern 생성을 정당화할 수 없습니다.
- 새 모듈 생성 판단 전에는 반드시 repo-wide exploration pass가 필요합니다.
- `reuse-map.md`가 있으면 legacy alias 또는 migration candidate로만 읽습니다.
- 둘 다 있으면 duplicate reuse maps can diverge 위험을 warning 또는 checkpoint-style ambiguity로 기록합니다.

## repo-wide exploration

repo-wide exploration은 모든 파일을 읽는 뜻이 아닙니다. 현실적인 탐사는 tracked source 전반에서 candidate를 찾고, 찾은 candidate와 callsite를 정밀 inspect하는 것입니다.

필수 포함 항목:

- file inventory
- source root, package, domain structure 확인
- keyword search
- import, export search
- component, hook, util, API, mapper naming search
- candidate file inspection
- callsite inspection
- UI hierarchy, spacing, border, color, density, component reuse pattern 비교

monorepo에서는 scope를 합리적으로 좁힐 수 있습니다. 다만 아래를 반드시 기록합니다.

- included scope
- excluded scope
- exclusion reason
- shared package 포함 여부
- design system 포함 여부
- common module 포함 여부

## 새 모듈 생성 판단

새 모듈 생성이 필요하다고 주장할 때는 아래 형식으로 기록합니다.

```md
### 새 모듈 생성 판단

- 대상: new component | hook | util | mapper | API client | layout primitive | UI pattern
- 필요성 주장:
- explored scope:
- searched keywords:
- inspected candidates:
- COMPONENT_REUSE_MAP.md hit/miss, with `reuse-map.md` only as legacy fallback:
- miss만으로 판단하지 않았는지:
- 기존 재사용 후보를 배제한 근거:
- 새 모듈 대신 가능한 대안:
- 사용자 승인 필요 여부:
```

## 공통 모듈 수정 gate

공통 모듈 수정은 기본 경로가 아닙니다. 아래 같은 경우는 gate를 통과해야 합니다.

- shared util 시그니처 변경
- common hook 동작 변경
- shared mapper field mapping 변경
- API client 기본 에러 처리 변경
- design system token 또는 primitive 수정
- 여러 화면이 쓰는 layout component 수정

공통 모듈을 수정하려면 반드시 아래를 선행합니다.

- repo-wide callsite impact analysis
- 영향 받는 callsite와 사용 패턴 기록
- 변경이 design-system drift 또는 nearby screen mismatch를 만들지 않는지 확인
- 대체로 local composition 또는 caller-level adaptation이 가능한지 검토
- 수정 전 explicit user approval 확보

사용자 승인 전에는 공통 모듈 수정이 필요한 gap을 기록할 수는 있어도, 수정 방향을 confirmed decision처럼 다루지 않습니다.

## Gap: 불충분한 재사용 탐사

```md
## GAP-REUSE-001 — 불충분한 재사용 탐사

유형: process gap
심각도: high
상태: open

### 비교한 SOT

- Source: Figma
- 참조: https://example.com/figma
- 섹션: 주문 상세 우측 요약 카드

### 비교한 코드

- Baseline: abc1234
- 확인한 파일:
  - src/features/order-detail/RightSummaryCard.tsx

### 증거

- 새 `RightSummaryCard`가 추가되었지만, 동일 domain과 nearby screen의 card pattern 탐사 기록이 없습니다.
- `COMPONENT_REUSE_MAP.md` miss만 언급되고 tracked source 전반 keyword, import/export, callsite inspection evidence가 없습니다.
- shared summary/card/layout primitive 후보 inspection 기록이 없습니다.

### 발견 사항

재사용 가능 후보를 충분히 탐사하지 않은 상태에서 새 UI module을 전제로 비교가 진행되었습니다.

### 중요한 이유

불충분한 재사용 탐사는 unnecessary new implementation, design-system drift, nearby screen pattern mismatch를 만들 수 있습니다.

### 필요한 해결 기준

repo-wide exploration을 다시 수행하고, inspected candidates와 callsite evidence를 gap에 추가한 뒤 새 모듈 생성 필요성을 다시 판단합니다.
```

## 절차

1. 현재 branch를 확인합니다.
2. detached HEAD 또는 protected branch이면 branch switch/create를 요청하고 멈춥니다.
3. `.tigerkit/branches/{escaped-branch}/requirements.md`에서 비교할 SOT reference를 확인합니다.
4. working tree 상태와 HEAD commit을 확인해 reproducible baseline인지 판정합니다.
5. staged, unstaged, untracked 변경 중 하나라도 있으면 `blocked: working tree not clean`으로 보고하고 멈춥니다.
6. staged diff를 baseline으로 비교하지 않고 gap evidence로도 기록하지 않습니다.
7. gap scope를 functional, design, reuse 관점으로 잡습니다.
8. repo-wide exploration으로 재사용 후보를 탐사합니다.
9. 관련 code file과 candidate file, callsite를 읽고 inspected files에 기록합니다.
10. design SOT와 rendered UI 비교가 필요하면 현재 DOM, accessibility tree, screenshot, rendered text, style token evidence 중 재현 가능한 자료를 확보하거나 사용자에게 요청합니다.
11. exact excerpt나 pointer 중심으로 evidence를 남깁니다.
12. finding과 interpretation을 분리합니다.
13. required resolution을 해결 기준으로 적습니다.
14. `.tigerkit/branches/{escaped-branch}/gap.md`를 갱신하고 추가 Decision Gate가 필요한지만 안내합니다.

## 금지

- gap을 실행 대기열로 변환
- ambiguity silent resolution
- external source 요약을 official requirement처럼 저장
- `CLAUDE.md`, `DESIGN.md` 또는 `COMPONENT_REUSE_MAP.md` 직접 업데이트
- root-level `.tigerkit/gap.md` 새로 쓰기
- implementation, commit, push, PR 생성, merge, deploy

## 출력

기록 성공 예시:

```text
gap 기록했습니다.
- branch: `feature__example`
- state: `needs_decision_gate`
- baseline: `abc1234`
- inspected files: source 비교에 필요한 파일
- recorded: `GAP-001`, `GAP-002`
- SOT coverage: partial, `SOT-IMG-001` pending_user_input
- 기록: `.tigerkit/branches/feature__example/gap.md`
- next safe action: 접근 불가 binding SOT가 있으면 file, local path, screenshot/export, pasted content를 요청하고, 없으면 gap별 필요한 해결 기준에 따라 진행합니다.
```

blocked 예시:

```text
gap 기록을 시작하지 않았습니다.
- state: `baseline_not_reproducible`
- blocked: working tree not clean
- staged: yes
- unstaged: no
- untracked: yes
- next safe action: staged 변경은 commit하고, 나머지 변경은 정리하거나 함께 commit한 뒤 clean baseline에서 gap 분석을 다시 요청하세요.
```
