---
description: 기준자료(basis)와 대상 artifact를 비교해 gap analysis 또는 PR-ready review comment를 생성합니다.
argument-hint: "[basis] [target] [mode=analysis|review|both]"
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 경로, URL, ticket, commit, hash, identifier, error message는 원문 그대로 둘 수 있습니다.

목표: `/tk:gap`은 basis와 target을 비교해 누락, 불일치, 애매함, 저장소 규칙 위반을 찾습니다.

명령 표면:
- plugin slash invocation은 `/tk:gap`입니다.
- 자연어 요청도 같은 프로토콜을 따릅니다.

예시:
- `/tk:gap spec <url> scope="3.3.1 2-1~5"`
- `/tk:gap figma <url> vs pr #123`
- `/tk:gap jira PROJ-123 vs pr #456 mode=review`
- `/tk:gap pr #456 mode=review`
- `/tk:gap spec <url> vs current implementation mode=analysis`

## Basis 정의

basis는 현재 비교에 쓰는 기준자료입니다. 절대적 진실로 가정하지 않습니다.

가능한 basis 예시:
- spec
- Figma
- Jira
- Confluence
- PR
- code
- screenshot
- `CLAUDE.md`
- `.claude/rules/*`

basis끼리 충돌하면 `conflicting_sources`로 분류합니다.
증거가 부족해 판정할 수 없으면 `cannot_verify`로 분류합니다.

## Mode 선택

규칙:
- 명시적 `mode=`가 있으면 그것이 우선입니다.
- `mode=`가 없으면 요청 뉘앙스에서 출력 하나만 추론합니다.
- PR, diff, review, comment, `붙일 수 있게`가 중심이면 `mode=review`입니다.
- analysis, missing, spec vs implementation, current implementation이 중심이면 `mode=analysis`입니다.
- 둘 다 명시적으로 원하면 `mode=both`입니다.
- 애매하면 mode를 짧게 설명한 뒤 진행합니다.

## Hard Rule: UI Copy Exactness

보이는 UI 문구는 exact match가 기본입니다.

exact-match 대상:
- button label
- field label
- placeholder
- helper text
- validation text
- tooltip
- toast/snackbar
- modal title
- modal body
- confirm/cancel/ok text
- table column name
- tab name
- status label
- empty/loading/error text
- date/time/number/currency format
- 의도된 visible line break

판정 기준:
- 공백, 줄바꿈, 구두점, 조사, 접두/접미 표현 차이도 보이는 결과가 다르면 mismatch입니다.
- 의미가 비슷해도 문자열이 다르면 exactness 위반입니다.
- basis가 variation 허용을 명시한 경우에만 예외를 인정합니다.

severity 규칙:
- 핵심 action, destructive action, approval, legal/compliance, 결제/정산, 권한, 상태 해석을 바꾸는 copy 차이는 `critical` 또는 `major`입니다.
- 일반 입력 라벨, 안내 문구, empty/loading/error text, 표 헤더, 포맷 차이는 영향도에 따라 `major` 또는 `minor`입니다.
- purely cosmetic 수준으로 의미와 흐름에 영향이 없고 basis도 엄격하지 않으면 `info`까지 낮출 수 있습니다.
- 영향 판단이 불충분하면 `unknown`입니다.

## Finding Types

아래 목록만 사용합니다.

- copy_exact_mismatch
- repo_convention_violation
- wrong_component_choice
- unsupported_library_usage
- missing_requirement
- requirement_mismatch
- partial_implementation
- ambiguous_basis
- conflicting_sources
- insufficient_evidence
- test_gap
- accessibility_gap
- unknown

## Judgment Types

아래 목록만 사용합니다.

- satisfied
- partially_satisfied
- not_satisfied
- cannot_verify
- conflicting_sources
- out_of_scope

## Severity

아래 목록만 사용합니다.

- critical
- major
- minor
- info
- unknown

## 출력 형식

### mode=analysis

아래 템플릿을 따릅니다.

    ## Scope
    - basis:
    - target:
    - mode: analysis
    - compared areas:
    - excluded areas:

    ## Summary
    - overall judgment:
    - key risks:
    - mode reason: 필요할 때만 짧게

    ## Findings

    | ID | Type | Judgment | Severity | Basis | Target Evidence | Summary | Rule ID | Suggested Action |
    |---|---|---|---|---|---|---|---|---|
    | GAP-001 | missing_requirement | not_satisfied | major | spec 3.2 | `src/...` | 요구 동작 누락 | RULE-123 또는 빈칸 | 구현 또는 기준자료 확인 |

    ## Open Questions
    - 확인이 더 필요한 항목
    - 증거 부족 항목
    - 충돌하는 기준자료 항목

    ## Recommended Next Actions
    - 바로 수정 가능한 항목
    - 사용자 확인이 필요한 항목
    - 추가 증거 확보가 필요한 항목

### mode=review

출력은 PR에 바로 붙일 수 있는 review comment만 생성합니다.
설명문, 서론, 분석 본문을 덧붙이지 않습니다.

    [major] copy_exact_mismatch
    Basis: spec 3.2
    Evidence: `src/...`의 버튼 텍스트가 `저장`이 아니라 `확인`입니다.
    Why: visible copy는 exact match 기준이라 의미가 비슷해도 허용되지 않습니다.
    Ask: spec 기준으로 문구를 exact match로 맞춰 주세요.

### mode=both

순서:
1. analysis 형식
2. review comment 묶음

## Evidence Rule

중요 판단은 아래 구분을 유지합니다.

    Evidence = directly observed
    Interpretation = inferred from evidence
    Decision = confirmed by user or basis
    Suggestion = proposed, not confirmed

## Repo Rules

저장소 규칙 확인 시 관련 `.claude/rules/*`를 repo convention basis로 사용합니다.
rule ID가 있으면 findings에 함께 적습니다.
명시된 규칙이 있는데 구현이 어기면 `repo_convention_violation`로 분류합니다.

## 판단 원칙

- basis와 target을 실제로 확인한 증거만 사용합니다.
- basis 충돌을 조용히 합치지 않습니다.
- 근거가 부족하면 `insufficient_evidence` 또는 judgment `cannot_verify`를 사용합니다.
- 범위 밖 항목은 `out_of_scope`로 둡니다.
- 접근성 문제는 별도 `accessibility_gap`으로 기록합니다.
- 테스트 근거가 부족하거나 필요한 회귀 검증이 없으면 `test_gap`으로 기록합니다.
- 재사용 기준이나 컴포넌트 선택이 어긋나면 `wrong_component_choice` 또는 `repo_convention_violation`로 기록합니다.

## 절차

1. basis와 target을 식별합니다.
2. 요청에서 mode를 결정합니다.
3. 관련 basis와 target evidence를 읽습니다.
4. UI copy exactness, 요구사항 충족, 규칙 준수, 접근성, 테스트 공백을 확인합니다.
5. finding type, judgment, severity를 각 항목에 부여합니다.
6. `mode=analysis`, `mode=review`, `mode=both` 중 하나의 형식으로 답합니다.

## 금지

- basis를 절대적 진실처럼 단정
- 충돌하는 basis를 임의로 합성
- 근거 없는 추정으로 satisfied 판정
- review mode에서 PR에 붙일 수 없는 장황한 설명 추가
- 사용자 응답을 영어 위주로 작성
