# TigerKit 운영 사용법

이 문서는 `.tigerkit/docs/` 아래 TigerKit 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash는 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = basis gap analysis + durable reflection + generalized meta-feedback + safe handoff
```

TigerKit은 요구사항을 재작성하거나 실행 대기열을 관리하지 않습니다. 기준자료와 대상 산출물을 비교하고, 반복되는 피드백을 repo 규칙 후보로 제안하며, 프로젝트 자산을 노출하지 않는 일반화된 TigerKit 개선안을 추출하고, 다음 세션이 안전하게 이어받을 문맥을 남깁니다.

## Command Surface

Plugin namespace는 `/tk:*`입니다. 해당 workflow를 명시한 자연어 요청은 대응하는 `/tk:*` command contract로 처리합니다.

| Command | 역할 |
| --- | --- |
| `/tk:gap` | 기준자료와 대상 산출물을 비교해 gap analysis 또는 PR-ready basis-target gap comment를 만듭니다. |
| `/tk:reflect` | durable feedback, 반복 실수, gap/review 결과에서 `CLAUDE.md`와 `.claude/rules/*` 업데이트 후보를 제안합니다. |
| `/tk:meta-feedback` | TigerKit command/skill 사용 friction을 프로젝트 자산 유출 없이 일반화된 개선안으로 정리합니다. |
| `/tk:handoff` | 다음 세션이 이어받을 수 있도록 `.claude/handoffs/current.md`를 작성합니다. |

## 사용 예시

```text
/tk:gap spec <url> vs current implementation
/tk:gap pr #123 mode=review
/tk:gap figma <url> vs pr #123 mode=both
/tk:reflect gap 결과에서 반복되는 리뷰 포인트를 rules로 제안해줘
/tk:reflect apply=true 이 copy rule을 반영해줘
/tk:meta-feedback gap output UX에서 생긴 friction을 일반화해줘
/tk:meta-feedback gap --out tk-feedback/gap-output-ux.md
/tk:handoff 현재 작업 이어받을 수 있게 남겨줘
/tk:handoff tiger-kit skill refactor archive=true
```

## Command notes

### `/tk:gap`

- 입력된 basis와 target을 직접 확인 가능한 근거로 비교합니다. basis는 Spec reference를 포함할 수 있는 비교 자료이지 절대적 진실이 아닙니다.
- target이 `current implementation` 또는 현재 checkout을 뜻하면 integration branch 대비 stale 여부를 먼저 확인합니다. 현재 `HEAD`가 behind이고 대상 영역 파일이 영향권이면 integration branch tip 형상으로 비교하고, Summary Table 또는 첫 finding에 base 상태를 명시합니다.
- `mode=analysis`는 compact `## Summary Table`, `## Findings`, `## Bottom Recap`만 출력합니다. Summary Table은 `Target`, `Counts`, `Next`로 결과 count와 핵심 next action을 보여주고, Findings는 `ID / Scope`, `Class`, `Evidence`, `Finding`, `Ask`로 압축합니다.
- `mode=review`는 PR-ready basis-target gap comment만 출력합니다. 일반 code review가 아니며 `Stable:` line을 쓰지 않습니다.
- `mode=both`는 analysis 뒤에 basis-target gap comment를 출력하며 같은 finding에 같은 `G<number>` ID를 사용합니다.
- 사용자가 대화에서 지칭하는 기본 ID는 `G1`, `G2` 같은 `G<number>`입니다. 별도 `gap-<scope-slug>-<finding-slug>` stable ID는 만들지 않습니다. `GAP-001` 같은 repo rule ID도 finding ID로 쓰지 않습니다.
- Scope label은 섹션 번호만 쓰지 않고 사람이 읽을 수 있는 title, menu, page, component, row 이름을 포함합니다.
- Type은 `missing`, `mismatch`, `convention`, `unverifiable`, `out_of_scope` 중 하나입니다.
- Severity는 `critical`, `major`, `minor` 중 하나입니다.
- Status는 `needs_fix`, `cannot_verify`, `conflicting_sources`, `blocked_external`, `out_of_scope` 중 하나입니다.
- Judgment는 출력 축으로 사용하지 않습니다.
- 보이는 UI copy는 exact match 기준입니다. 의미상 유사함은 충분하지 않습니다.
- 근거가 부족하면 `cannot_verify`, basis끼리 충돌하면 `conflicting_sources`, 접근 불가 외부 근거는 `blocked_external`로 남기고 추측으로 채우지 않습니다.
- ambiguity가 있으면 code/docs/similar implementation을 먼저 더 확인하고, 남은 질문은 recommendation과 evidence를 포함해 `implementation-blocking` 또는 `reference-only`로 구분합니다.
- Evidence, Interpretation, Decision, Suggestion 구분을 유지합니다.

### `/tk:reflect`

- durable하게 남길 만한 피드백, 반복 실수, gap/review finding을 분류합니다.
- 기본은 제안만 합니다.
- `apply=true` 또는 명시 승인 없이는 파일을 수정하지 않습니다.
- 필요하면 `### Session Decision Recap`으로 Evidence → Interpretation → Decision 흐름을 짧게 요약합니다.
- target root에 `CLAUDE.md`가 없고 일반 작업 트리라면 scoped rule과 별개로 root instruction bootstrap 후보를 제안합니다.

### `/tk:meta-feedback`

- TigerKit command 또는 skill 사용 중 드러난 friction, 사용자 교정, 반복 실수를 TigerKit 자체 개선안으로 정리합니다.
- 출력 자체가 이미 generalize되어야 합니다. repo 이름, product 이름, 도메인 고유명, 내부 path, URL, ticket, branch, PR 번호, commit hash, 사용자 원문 quote를 포함하지 않습니다.
- 기본은 제안만 합니다.
- `--out <path>`가 있을 때만 같은 redacted output을 파일로 작성할 수 있습니다.
- 안전하게 일반화할 수 없으면 `cannot_generalize_safely`로 중단합니다.
- repo rule 제안은 `/tk:reflect`, basis-target 비교는 `/tk:gap` 대상으로 분리합니다.

### `/tk:handoff`

- 기본 출력 대상은 `.claude/handoffs/current.md`입니다.
- `archive=true` 또는 명시 요청이 있을 때만 dated archive copy를 만듭니다.
- handoff에는 Reader Guide와 Resume Prompt를 포함합니다.

## 선택형 Stop hook

TigerKit은 선택 기능으로 Claude Code `Stop` 시점에 실행되는 hook을 제공할 수 있습니다.

```text
hooks/tigerkit-stop-advisor.sh
hooks/hooks.json
```

이 hook은 TigerKit 핵심 command surface(`/tk:gap`, `/tk:reflect`, `/tk:handoff`)를 대체하지 않습니다. 정상 응답 종료 직전에 `verification-manifest-guard`만 실행합니다.

### `verification-manifest-guard`

변경사항이 있는데 변경 파일별 검증 상태 manifest가 없거나 누락되어 있으면 `stderr`와 `exit 2`로 Stop을 막습니다.

검증 manifest는 repo 안에 만들지 않고 아래 임시 경로만 사용합니다.

```text
${TMPDIR:-/tmp}/tiger-kit/{repo-hash}/{branch-hash}/{session-id}/verification.md
```

각 변경 파일은 아래 상태 중 하나와 `method`, `result`, `note`를 가져야 합니다.

- `verified`
- `unverified`
- `not-applicable`

특정 package manager나 test/build/typecheck 명령은 강제하지 않습니다.

### 제한과 비목표

이 hook은 정상 `Stop` 시점만 대상으로 합니다. 아래 상황에서는 안정적으로 실행된다고 기대하지 않습니다.

- `Ctrl+C`
- 터미널 종료
- process kill
- 사용자 인터럽트
- OS/process-level 강제 종료

이 hook은 `.tigerkit` 또는 기타 repo-local state path에 verification state를 쓰지 않습니다. 또한 `/tk:gap`, `/tk:reflect`, `/tk:handoff` 실행을 강제하지 않습니다.

## 운영 범위 메모

세부 정책, 우선순위 규칙, 검증 원칙은 `CLAUDE.md`를 기준으로 봅니다.
