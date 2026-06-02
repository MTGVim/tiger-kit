---
description: 기준자료(basis)와 대상 artifact를 비교해 gap analysis 또는 PR-ready basis-target gap comment를 생성합니다.
argument-hint: "[basis] [target] [mode=analysis|review|both]"
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 경로, URL, ticket, commit, hash, identifier, error message는 원문 그대로 둘 수 있습니다.

목표: `/tk:gap`은 basis와 target을 비교해 누락, 불일치, 검증 불가, 저장소 규칙 위반, 범위 밖 항목을 찾습니다.

명령 표면:
- plugin slash invocation은 `/tk:gap`입니다.
- 자연어 요청도 같은 프로토콜을 따릅니다.

예시:
- `/tk:gap spec <url> scope="3.3.1 2-1~5"`
- `/tk:gap figma <url> vs pr #123`
- `/tk:gap jira PROJ-123 vs pr #456 mode=review`
- `/tk:gap pr #456 mode=review`
- `/tk:gap spec <url> vs current implementation mode=analysis`

## Basis / Spec reference 정의

basis는 현재 비교에 쓰는 기준자료이며 Spec reference를 포함할 수 있습니다. 절대적 진실로 가정하지 않습니다.

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

basis끼리 충돌하면 Status를 `conflicting_sources`로 둡니다.
증거가 부족해 판정할 수 없으면 Status를 `cannot_verify`로 둡니다.
접근할 수 없는 외부 URL, 이미지, Figma/design link, screenshot URL, local path는 Status를 `blocked_external`로 둡니다.

## Target Freshness Preflight

`target`이 `current implementation`, 현재 작업 트리, 현재 branch, local checkout을 뜻하면 gap 분석 전에 target freshness를 확인합니다.

규칙:
- Git repository이면 integration branch tip을 식별합니다. 기본 후보는 `origin/main`이며, repository default branch가 다르면 그 remote tracking branch를 사용합니다.
- 가능하면 remote metadata를 먼저 갱신하거나 현재 `origin/<default-branch>`가 최신인지 확인합니다. 확인할 수 없으면 base freshness를 `cannot_verify` 근거로 보고합니다.
- 현재 `HEAD`가 integration branch tip보다 behind이면, 요청 scope 또는 target evidence로 읽을 파일들이 `HEAD..integration` 사이에서 바뀌었는지 확인합니다.
- behind이고 대상 영역 파일이 영향권이면 stale checkout을 target으로 삼아 `needs_fix`를 재보고하지 않습니다. 비교 target을 integration branch tip 형상으로 전환하고, Summary Table의 `Target` 또는 `Key Next Action`에 base 상태와 전환 사실을 명시합니다.
- behind이지만 대상 영역 파일이 영향권이 아니면 기존 target으로 비교할 수 있습니다. 이때도 Summary Table 또는 첫 finding에 checkout freshness 상태를 짧게 남깁니다.
- 사용자가 특정 commit, branch, PR diff, working tree 상태를 명시적으로 target으로 고정하면 임의로 전환하지 않습니다. 대신 stale 여부를 evidence로 보고합니다.

## Ambiguity Handling

아래 조건 중 하나라도 있으면 조용히 결정하지 않습니다.

1. requirements document와 code가 충돌합니다.
2. 서로 다른 pattern의 유사 구현이 2개 이상 있습니다.
3. Spec reference 또는 source basis에 접근할 수 없습니다.
4. reuse-map에 entry가 없고 repo-wide exploration이 아직 충분하지 않습니다.
5. UI/UX intent를 copy나 screenshot만으로 확인할 수 없습니다.
6. API response, DTO, permission, state transition이 불명확합니다.
7. 변경 범위가 common module에 영향을 줄 수 있습니다.

절차:
- 먼저 code, docs, similar implementation, repo rules, reuse-map을 더 탐색합니다.
- 탐색 후에도 불명확하면 질문을 만듭니다.
- 질문에는 recommendation과 evidence를 함께 적습니다.
- 질문은 `implementation-blocking`과 `reference-only`로 구분합니다.
- `mode=analysis`에서는 별도 Open Questions 섹션을 만들지 않고 Findings table의 `Finding` 또는 `Ask`에 질문 구분을 적습니다.
- `mode=review`에서는 confirmed defect처럼 쓰지 말고 `Ask:`에 질문 구분, recommendation, evidence를 포함합니다.

## Mode 선택

mode는 기능 분기가 아니라 출력 profile입니다.

규칙:
- 명시적 `mode=`가 있으면 그것이 우선입니다.
- `mode=`가 없으면 요청 뉘앙스에서 출력 profile 하나만 추론합니다.
- PR, diff, review, comment, `붙일 수 있게`가 중심이면 `mode=review`입니다.
- analysis, missing, spec vs implementation, current implementation이 중심이면 `mode=analysis`입니다.
- 둘 다 명시적으로 원하면 `mode=both`입니다.
- 애매하면 기본값은 `mode=analysis`입니다. 이때 `## Summary Table`의 Key Next Action에 mode를 analysis로 선택했다는 짧은 note를 포함합니다.

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
- 공백, 줄바꿈, 구두점, 조사, 접두/접미 표현 차이도 보이는 결과가 다르면 Type `mismatch`입니다.
- 의미가 비슷해도 문자열이 다르면 exactness 위반입니다.
- basis가 variation 허용을 명시한 경우에만 예외를 인정합니다.
- 핵심 action, destructive action, approval, legal/compliance, 결제/정산, 권한, 상태 해석을 바꾸는 copy 차이는 Severity `critical` 또는 `major`입니다.
- 일반 입력 라벨, 안내 문구, empty/loading/error text, 표 헤더, 포맷 차이는 영향도에 따라 Severity `major` 또는 `minor`입니다.
- confirmed exact-match 위반은 Status `needs_fix`를 유지합니다. 영향도만 불확실하면 위험도에 따라 Severity `minor` 또는 `major`를 사용하고, mismatch 자체가 basis/target evidence 부족으로 확인되지 않을 때만 Status `cannot_verify`를 사용합니다.

## Taxonomy

아래 값만 사용합니다.

Type:
- `missing`: basis에 있는 요구, UI, 동작, 검증, 접근성, 산출물이 target에 없음
- `mismatch`: basis와 target이 서로 다름
- `convention`: repo convention, `.claude/rules/*`, reuse/component/API 규칙 위반
- `unverifiable`: 근거 부족, 접근 불가, 재현 불가로 확인할 수 없음
- `out_of_scope`: 현재 요청 scope 밖임

Severity:
- `critical`: 핵심 업무 흐름, 데이터 손실, 보안/권한, 결제/정산, 법무/승인, destructive action에 직접 영향
- `major`: 요구 충족, 사용자 이해, 운영 품질, 회귀 위험에 의미 있는 영향
- `minor`: 국소적 copy, 보조 UI, 낮은 위험의 convention 또는 후속 확인 항목

Status:
- `needs_fix`: basis와 target을 비교한 결과 수정이 필요함
- `cannot_verify`: 증거가 부족하거나 재현할 수 없어 판정할 수 없음
- `conflicting_sources`: basis끼리 충돌함
- `blocked_external`: 외부 근거에 접근할 수 없어 사용자 제공 자료가 필요함
- `out_of_scope`: 현재 요청 범위 밖임

Type은 finding의 성격, Severity는 영향도, Status는 처리 상태입니다. Judgment를 별도 출력 축으로 만들지 않습니다.

## Finding IDs

finding ID는 `G<number>` 하나만 사용합니다.

형식:

    G<number>

규칙:
- `G1`, `G2`처럼 한 응답 안에서 순서대로 부여합니다.
- 사용자가 대화에서 지칭하는 canonical handle입니다.
- `mode=analysis`, `mode=review`, `mode=both`에서 같은 finding에는 같은 `G<number>`를 사용합니다.
- 별도 slug-style stable ID(`gap-<scope-slug>-<finding-slug>`)를 만들지 않습니다.
- `GAP-001` 같은 rule ID 또는 순번 기반 stable ID를 finding ID로 사용하지 않습니다.
- scope label은 섹션 번호만 쓰지 않습니다. 사람이 읽을 수 있는 title, menu, page, component, row 이름을 포함합니다.
- 좋은 scope label 예: `§3.2 Summary Row`, `Settings > Billing Page`, `Login Modal Confirm Button`.
- 나쁜 scope label 예: `§3.2`, `3.2`, `row 4`.

## 출력 형식

### mode=analysis

출력은 summary-first compact analysis로 생성합니다. H2는 아래 세 개만 사용합니다.

    ## Summary Table

    | Target | Counts | Next |
    |---|---|---|
    | current implementation | total 3 / fix 2 / verify 1 / blocked 0 | G1, G2를 먼저 반영해 주세요. |

    ## Findings

    | ID / Scope | Class | Evidence | Finding | Ask |
    |---|---|---|---|---|
    | G1 / §3.2 Summary Row | missing/major/needs_fix | spec §3.2 requires `Total`; target has no row in `src/...` | `Total` row missing | Add row per spec |

    ## Bottom Recap
    - Needs fix: 2
    - Cannot verify: 1
    - Key next action: needs_fix 2건을 먼저 반영해 주세요.

규칙:
- Summary Table은 반드시 `Target`, `Counts`, `Next` 세 열 table이어야 하며 긴 Findings에 앞서 전체 결과 count와 핵심 next action을 보여줍니다.
- Findings table은 `ID / Scope`, `Class`, `Evidence`, `Finding`, `Ask` 다섯 열의 단일 table입니다. 별도 Scope, Summary, Open Questions, Recommended Next Actions 섹션을 만들지 않습니다.
- `Class`는 `<type>/<severity>/<status>` 형식입니다.
- `Evidence`는 basis fragment와 target fragment를 한 문장 또는 세미콜론 구분 fragment로 합칩니다.
- `Finding`은 gap을 설명하는 짧은 한 문장입니다.
- `Ask`는 짧은 imperative action입니다.
- Bottom Recap은 긴 Findings 뒤에서도 사용자가 결론을 다시 볼 수 있도록 Summary Table의 핵심 count와 next action을 반복합니다.
- open question, 추가 증거 요청, 범위 밖 항목도 필요하면 같은 table의 `Class`, `Evidence`, `Ask`로 표현합니다.
- `ID / Scope`의 scope는 반드시 사람이 읽을 수 있는 title, menu, page, component, row 이름을 포함합니다.

### mode=review

출력은 PR에 바로 붙일 수 있는 basis-target gap comment만 생성합니다.
설명문, 서론, 분석 본문을 덧붙이지 않습니다.

    [major] G1 | mismatch | needs_fix
    Scope: §3.2 Summary Row
    Basis: spec §3.2의 button label은 `저장`입니다.
    Evidence: `src/...`의 버튼 텍스트가 `확인`입니다.
    Why: visible copy는 exact match 기준입니다.
    Ask: 문구를 `저장`으로 변경해 주세요.

규칙:
- 첫 줄은 `[severity] G<number> | type | status` 형식입니다.
- 첫 줄에는 Severity, `G<number>`, Type, Status가 모두 있어야 합니다.
- `Stable:` line은 쓰지 않습니다.
- 본문은 `Scope:`, `Basis:`, `Evidence:`, `Why:`, `Ask:` 순서를 지킵니다.
- `Scope:`는 반드시 사람이 읽을 수 있는 title, menu, page, component, row 이름을 포함합니다.
- speculative finding은 confirmed defect처럼 쓰지 말고 Status를 `cannot_verify`, `conflicting_sources`, `blocked_external`, `out_of_scope` 중 맞는 값으로 둡니다.

### mode=both

순서:
1. `mode=analysis` 형식
2. `mode=review` basis-target gap comment 묶음

규칙:
- analysis table과 basis-target gap comment는 같은 finding에 같은 `G<number>` ID를 사용합니다.
- basis-target gap comment는 analysis에서 Status `needs_fix`인 항목을 우선 작성합니다.
- `cannot_verify`, `conflicting_sources`, `blocked_external`, `out_of_scope` 항목을 basis-target gap comment로 포함해야 한다면 confirmed defect가 아니라 확인 요청으로 작성합니다.

## Evidence Rule

중요 판단은 아래 구분을 유지합니다.

    Evidence = directly observed
    Interpretation = inferred from evidence
    Decision = confirmed by user or basis
    Suggestion = proposed, not confirmed

규칙:
- Basis와 Target Evidence를 분리합니다.
- Evidence에는 직접 관측한 path, URL, ticket, screenshot, source line, diff, commit, 사용자 발화만 적습니다.
- Interpretation은 evidence에서 추론한 의미입니다.
- Decision은 basis 또는 사용자가 확인한 내용입니다.
- Suggestion은 제안이며 확정된 요구처럼 쓰지 않습니다.

## Repo Rules

저장소 규칙 확인 시 관련 `.claude/rules/*`를 repo convention basis로 사용합니다.
rule ID가 있으면 Basis 또는 Finding에 함께 적습니다.
명시된 규칙이 있는데 구현이 어기면 Type `convention`, Status `needs_fix`로 분류합니다.

## 판단 원칙

- basis와 target을 실제로 확인한 증거만 사용합니다.
- basis를 절대적 진실처럼 단정하지 않습니다.
- basis 충돌을 조용히 합치지 않습니다.
- 근거가 부족하면 Type `unverifiable`, Status `cannot_verify`를 사용합니다.
- 접근 불가 외부 근거 때문에 확인할 수 없으면 Type `unverifiable`, Status `blocked_external`을 사용하고 필요한 자료를 `Ask`에 적습니다.
- basis끼리 충돌하면 Status `conflicting_sources`를 사용합니다.
- 범위 밖 항목은 Type `out_of_scope`, Status `out_of_scope`로 둡니다.
- 접근성, 테스트, 컴포넌트 재사용, API 필드, 동작 차이는 별도 Type을 만들지 않고 위 taxonomy로 매핑합니다.
- ambiguity는 terminal blocked로 끝내지 말고 추가 탐색 후 `cannot_verify`, `conflicting_sources`, `blocked_external` 중 맞는 Status로 라우팅합니다.
- 남은 질문은 recommendation과 evidence를 포함해 `implementation-blocking` 또는 `reference-only`로 구분합니다.

## 절차

1. basis와 target을 식별합니다.
2. target이 current implementation 계열이면 Target Freshness Preflight를 실행합니다.
3. 요청에서 mode output profile을 결정합니다.
4. 관련 basis와 target evidence를 읽습니다.
5. UI copy exactness, 요구사항 충족, 규칙 준수, 접근성, 테스트 공백을 확인합니다.
6. 각 finding에 `G<number>` ID, Scope, Type, Severity, Status를 부여합니다.
7. `mode=analysis`, `mode=review`, `mode=both` 중 하나의 형식으로 답합니다.

## 금지

- basis를 절대적 진실처럼 단정
- 충돌하는 basis를 임의로 합성
- 근거 없는 추정으로 충족 판정
- Judgment를 출력 축으로 추가
- `GAP-001` 같은 repo rule ID를 finding ID로 사용
- 사람에게 의미 없는 section number만 Scope로 사용
- review mode에서 PR에 붙일 수 없는 장황한 설명 추가
- 사용자 응답을 영어 위주로 작성
