# TigerKit 운영 사용법

이 문서는 TigerKit v7.2.7 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash, contract field name은 원문 그대로 유지할 수 있습니다.

사용자 대화에 보이는 안내, 추천, 요약, next action은 계약용어와 변수명을 제외하고 한글로 씁니다.

## 핵심 모델

```text
TigerKit = branch-scoped spec + gap + durable reflection + continuation handoff + generalized meta-feedback
```

TigerKit은 branch-local working memory와 durable repo insight를 분리합니다.

- `spec`, `gap` 산출물은 현재 브랜치의 working memory입니다.
- 해당 산출물은 repo-wide durable knowledge가 아닙니다.
- repo에 영구적으로 남길 insight는 `reflect`만 추출하고 `CLAUDE.md` 또는 `.claude/rules/**/*.md`에 반영합니다.
- 다음 세션을 위한 사람이 읽는 continuation은 `handoff`가 담당합니다.
- TigerKit command/skill 자체 개선 피드백은 `meta-feedback`이 담당합니다.

## Command Surface

Plugin namespace는 `/tk:*`입니다. 해당 workflow를 명시한 자연어 요청은 대응하는 `/tk:*` command contract로 처리합니다.

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:spec` | 즉석 지시, 브레인스토밍, 회의 메모를 gap 분석용 Spec Patch로 저장합니다. | branch-local |
| `/tk:gap` | Product/Design Spec + implementation plan + current implementation을 단일 `/tk:gap` 실행로 비교합니다. | branch-local |
| `/tk:reflect` | branch-local 산출물에서 repo에 남길 insight만 추출하고 반영합니다. | durable insight |
| `/tk:handoff` | 다음 세션이나 다음 작업자가 이어받을 수 있도록 continuation 문서를 작성합니다. | continuation |
| `/tk:meta-feedback` | 현재 세션에서 드러난 TigerKit command/skill 개선안을 프로젝트 자산 유출 없이 일반화합니다. | generalized feedback |

## 사용 예시

```text
/tk:spec "방금 정해졌는데 모바일에서는 CTA를 하단 sticky로 해야 된대. 데스크톱은 기존처럼 우상단 유지."
/tk:gap
/tk:gap --analysis-depth bounded
/tk:gap --analysis-depth expanded
/tk:gap --spec SP-20260602-143012-A7F3
/tk:reflect
/tk:reflect --dry-run
/tk:handoff 현재 작업 이어받을 수 있게 남겨줘
/tk:meta-feedback gap 결과가 느리고 BE 오탐이 난 패턴을 일반화해줘
```

## `/tk:spec`

- raw instruction을 branch-local Spec Patch로 저장합니다.
- 기본 저장 위치는 `.claude/tigerkit/branches/<branch-key>/specs/`입니다.
- 기본 상태는 `active`입니다.
- confirmed item만 `/tk:gap` final finding evidence로 사용될 수 있습니다.
- ambiguous instruction은 confirmed로 세탁하지 않고 `draft`, `assumed`, `unclear`, 또는 clarification 대상으로 둡니다.
- `spec`은 구현 분석을 하지 않고 finding을 만들지 않습니다.
- 기본 stdout은 ID, branch scope, path, item list summary만 출력합니다.
- 전체 본문은 `--print-body`가 있을 때만 출력합니다.

## `/tk:gap`

- 기존 Figma diff tool이 아닙니다.
- Product Spec, Design Spec, Design System Spec, Engineering Constraint, QA Acceptance Criteria, Analytics Contract를 Contract로 normalize해 비교합니다.
- active/confirmed Spec Patch item을 기본 참조합니다.
- 기본 호출은 user-provided references, target hints, Current Implementation 후보, 위험 신호를 먼저 skim한 뒤 단일 `/tk:gap` 실행로 실행합니다.
- `--lite`와 `--strict`는 compatibility flag로만 기록하며 user-facing quality mode가 아닙니다.
- 분석 범위 조절은 내부 `analysisDepth` 휴리스틱 또는 명시 `--analysis-depth <direct|bounded|expanded|exhaustive-capped>`로 표현합니다.
- depth 선택은 hard trigger를 먼저 적용하고 `riskScore`는 tie-breaker로만 사용합니다.
- `direct`는 단일 explicit local surface, ambiguity 없음, API/DTO/state/auth/payment/data mutation/shared component 영향 없음일 때만 사용합니다.
- `bounded`는 single screen/component/command와 주변 1-depth 또는 대표 usage 1-3개를 확인합니다.
- `expanded`는 shared/design-system/API/DTO/state transition, source conflict risk, inaccessible source, 모호한 Product/API/Design decision, divergent similar implementation에 사용합니다.
- `exhaustive-capped`는 P0/P1 후보, auth/permission/payment/data mutation/destructive action, release gate, cross-module impact에 사용합니다.
- `--legacy`, `--deep`, `--no-strict`는 active mode가 아닙니다. v6-era legacy behavior는 미지원 과거 동작이며 `lite`의 별칭이 아닙니다.
- changed files는 primary scope가 아니라 Current Implementation 후보 evidence입니다.
- source/plan이 없으면 관련 agent는 skip하고 이유, evidenceCoveragePreserved, falseNegativeRisk를 artifact에 기록합니다.
- missed P0/P1 방지를 위해 target surface coverage, dispatch completeness, ClaimFreshnessGate를 확인하고 `heuristicProof.falseNegative`에 수치 proof를 남깁니다.
- Product Spec, Design Spec, API contract, source priority, owner decision이 모호하면 user consent 전에는 final finding으로 확정하지 않고 `Clarification Needed` 또는 `SourceConflict`로 둡니다.
- UI 판단이 모호하면 option/evidence/impact/recommendation 표와 오른쪽 border가 정렬된 TUI/ASCII prototype으로 확인합니다.
- subagent는 candidate만 생성합니다.
- candidate의 file:line 또는 module-path evidence는 JudgeMergerAgent queue 진입 전에 현재 target surface에서 read-back으로 재확인합니다.
- JudgeMergerAgent만 final finding을 확정합니다.
- final finding은 P0/P1/P2만 포함합니다.
- P3/nit/duplicate/unverifiable/source_conflict는 final finding이 아닙니다.
- finding이 0개가 될 때까지 반복하지 않습니다.
- run artifact는 `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/` 아래에 저장합니다.
- 기본 stdout은 summary만 출력합니다. 전체 report는 `--print-report`가 있을 때만 출력합니다.
- stdout과 report에는 단일 `/tk:gap` 실행 완료 상태, analysis depth, 확장 이유, 성능 증명, compact tables를 남깁니다.
- 유저향 compact table은 긴 Candidate/Finding ID 대신 run-local short Ref(`G1`, `R1`, `C1`, `Q1`)를 우선 표시하고, canonical ID는 JSON artifact와 report 상세/참조 영역에 보관합니다.

## `/tk:reflect`

- branch-local specs/gap memory에서 durable insight 후보만 추출합니다.
- 기본 동작은 `apply=true`입니다.
- `--dry-run`과 `--apply=false`는 preview-only입니다.
- 기본 apply target은 `CLAUDE.md` 또는 `.claude/rules/**/*.md`입니다.
- `.claude/tigerkit/` 아래에는 durable insight를 저장하지 않습니다.
- source code는 수정하지 않습니다.
- branch-specific one-off decision, 임시 Spec Patch, superseded 결정, P3/nit, rejected finding, low-confidence observation은 durable insight로 만들지 않습니다.

## `/tk:handoff`

- 기존 continuation command입니다. v7.2에서도 active command로 유지합니다.
- 기본 출력 대상은 `.claude/handoffs/current.md`입니다.
- 최신 branch-local Spec Patch와 Gap Run이 있으면 handoff의 relevant files나 validation에 참조할 수 있습니다.
- `archive=true` 또는 명시적 archive 요청이 있을 때만 dated copy를 만듭니다.
- `Reader Guide`와 `Resume Prompt`를 포함합니다.

## `/tk:meta-feedback`

- 기존 TigerKit improvement command입니다. v7.2에서도 active command로 유지합니다.
- 현재 세션 내역에서 TigerKit command/skill 사용 friction과 반복 피드백을 찾습니다.
- gap 속도, BE 오탐, mode 추천 UX, output shape 같은 개선안을 일반화합니다.
- repo 이름, product 이름, 내부 path, URL, ticket, branch, PR 번호, commit hash, 사용자 원문 quote는 출력하지 않습니다.
- repo rule patch는 `/tk:reflect`, basis-target 비교는 `/tk:gap` 대상으로 분리합니다.

## Generated state

`.claude/tigerkit/`은 generated branch-local working memory입니다. git ignore 대상입니다.

주의:

- `.claude/` 전체를 ignore하지 않습니다.
- `.claude/tigerkit/`만 ignore합니다.
- current worktree root 아래에 저장합니다.
- `$GIT_COMMON_DIR`, `.git/worktrees/*`, user home, `/tmp`에 저장하지 않습니다.

## 운영 범위 메모

세부 정책, 우선순위 규칙, 검증 원칙은 `CLAUDE.md`와 `.claude/rules/**/*.md`를 기준으로 봅니다.
