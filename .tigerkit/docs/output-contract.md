# TigerKit 운영 Output Contract

이 문서는 TigerKit v7.2 command의 출력 계약을 정의합니다. 사용 흐름은 `.tigerkit/docs/usage.md`, 산출물 위치는 `.tigerkit/docs/artifact-layout.md`를 기준으로 봅니다.

```text
stdout is a receipt. Full spec/gap/verify bodies are saved as branch-local artifacts unless explicit print option is used.
```

## 공통 원칙

기본 응답은 아래 네 가지에 집중합니다.

1. outcome
2. branch scope
3. artifact paths when files are written
4. counts, risks, next action

상세 보고서는 파일에 저장하고, 사용자가 `--print-body` 또는 `--print-report`를 지정한 경우에만 stdout에 함께 출력합니다.

사용자 대화에 보이는 안내, 추천, 요약, next action은 계약용어, path, identifier, field name을 제외하고 한글로 씁니다.

## `/tk:spec` Output Contract

- 목적: raw instruction을 현재 branch-local Spec Patch로 저장합니다.
- 기본 저장 위치: `.claude/tigerkit/branches/<branch-key>/specs/`
- 기본 stdout은 summary만 출력합니다.
- Spec Patch 전체 본문은 `--print-body`가 있을 때만 출력합니다.
- `spec`은 finding을 만들지 않고 구현 분석을 하지 않습니다.

기본 stdout:

```text
Spec Patch 생성: <SP-ID>
Branch Scope: <branch-key>
경로: .claude/tigerkit/branches/<branch-key>/specs/<SP-ID>-<slug>.md
Items:
- <ITEM-ID>
```

## `/tk:gap` Output Contract

- 목적: Product/Design Spec contract와 implementation plan/current implementation을 비교합니다.
- 기본 저장 위치: `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/`
- 기본 호출은 preflight skim 후 실행 preset을 결정하고 자동 실행합니다. stdout에는 실행 preset과 이유를 기본 출력합니다.
- `--lite`는 빠른 contract-based preset입니다. bounded target resolver와 bounded usage lookup을 사용합니다.
- `--strict`는 기본 추천에 가까운 보수적 contract-based preset입니다. expanded discovery와 `CriticalRedTeamAgent` 1회를 사용합니다.
- `lite`는 side-effect confidence >= 90, risk score <= 15, hard strict trigger 없음일 때만 추천합니다.
- 신규 화면/flow, BE/API/DTO, auth/permission/payment/data mutation, shared component, source conflict, inaccessible source, 모호한 Product/API/Design decision은 strict trigger입니다.
- `--legacy`, `--deep`, `--no-strict`는 active mode가 아닙니다. v6-era legacy behavior는 미지원 과거 동작입니다.
- subagent는 final finding을 확정하지 못합니다.
- candidate의 file:line 또는 module-path evidence는 JudgeMergerAgent queue 진입 전에 현재 target surface에서 read-back으로 재확인합니다.
- JudgeMergerAgent만 final accepted finding을 확정합니다.
- final finding에는 P0/P1/P2만 포함합니다.
- P3/nit/duplicate/unverifiable/source_conflict는 final finding으로 출력하지 않습니다.
- Product/API/Design ambiguity는 user consent 전 final finding으로 출력하지 않고 `Clarification Needed` 또는 `SourceConflict`로 기록합니다.
- finding이 안 나올 때까지 반복하지 않습니다.

기본 stdout:

```text
실행 preset: <lite|strict>
이유: <한글 이유>
Discovery depth: <bounded|expanded>
Verification strength: <standard|red-team>
상태: <lite|strict> preset 기준 완료
추천 preset: <lite|strict, 실행 preset과 다를 때만 출력>
추천 이유: <한글 이유, 실행 preset과 다를 때만 출력>

Gap Review 완료: <GAP-ID>
Branch Scope: <branch-key>
Strict 실행: <yes|no>
Report: .claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md

Findings:
- P0: <count>
- P1: <count>
- P2: <count>

Source Conflicts: <count>
Clarification Needed: <count>
Rejected/Downgraded: <count>
Rerun: <none|/tk:gap --lite|/tk:gap --strict + reason>
```

Run artifact files:

```text
input-manifest.json
contracts.json
candidates.json
judge-result.json
report.md
```

`input-manifest.json`과 `judge-result.json`에는 `mode`, `strictExecuted`, `recommendedMode`, `recommendationReasons`, `discoveryDepth`, `verificationStrength`, `dispatchSkips`, `evidencePrecisionGate`, `blockedClarifications`, `rerunTrail`을 기록합니다.

`추천 preset`은 실행 preset과 다를 때만 stdout에 출력합니다. 같은 경우에는 실행 preset과 이유만 출력하면 충분합니다. 더 넓은 discovery 또는 강한 verification이 필요할 때만 `Rerun`에 재실행 안내를 남깁니다.

Clarification table shape:

```md
| ID | Category | Question | Options | Evidence | Impact | Recommendation | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CLAR-... | implementation-blocking | <질문> | A / B | <근거> | <영향> | <추천> | blocked_pending_user |
```

UI clarification prototype은 오른쪽 border 정렬을 맞춥니다.

```text
Option A
┌────────────────────┐
│ 저장               │
└────────────────────┘

Option B
┌────────────────────┐
│ 변경사항 저장      │
└────────────────────┘
```

Accepted finding uses:

- ID: `FND-YYYYMMDD-HHmmss-RAND-NN`
- finalSeverity: `P0`, `P1`, or `P2`
- sourceContracts referencing confirmed, non-superseded contracts
- concrete evidence
- requiredChange engineers can execute without guessing
- confidence `medium` or `high`

Rejected finding uses one of:

- `P3_nit`
- `duplicate`
- `unverifiable`
- `source_conflict`
- `not_user_visible`
- `not_actionable`
- `low_confidence`
- `missing_evidence`
- `superseded_source`

## `/tk:verify-before-stop` Output Contract

- 목적: Stop hook이 자동 확인할 verification evidence를 수동으로 준비하거나 보완합니다.
- command는 manual preparation입니다.
- Stop hook은 automatic guard입니다.
- 기본 저장 위치: `.claude/tigerkit/branches/<branch-key>/runs/verify/<VFY-ID>/`
- 기본은 저장입니다.
- `--no-save`는 debugging 용도입니다.
- 전체 report는 `--print-report`가 있을 때만 stdout에 함께 출력합니다.

기본 stdout:

```text
Verification 완료: <VFY-ID>
Branch Scope: <branch-key>
상태: <passed|failed|unknown>
Report: .claude/tigerkit/branches/<branch-key>/runs/verify/<VFY-ID>/report.md
```

Verify run files:

```text
checklist.md
evidence.json
report.md
```

최신 gap run이 없으면 gap-dependent checks는 `unknown` 또는 `skipped`로 둡니다. gap run 부재만으로 failed 처리하지 않고 overall status는 `unknown`으로 둡니다.

## `/tk:reflect` Output Contract

- 목적: branch-local working memory에서 durable repo insight만 추출합니다.
- 기본 동작은 `apply=true`입니다.
- `--dry-run`과 `--apply=false`는 preview-only입니다.
- 기본 apply target은 `CLAUDE.md` 또는 `.claude/rules/**/*.md`입니다.
- `.claude/tigerkit/` 아래에는 durable insight를 저장하지 않습니다.
- source code는 수정하지 않습니다.
- content write는 `CLAUDE.md` 또는 `.claude/rules/**/*.md`만 수정합니다.
- branch recency bookkeeping으로 `global-index.json`의 `lastUsedAt`은 갱신할 수 있습니다.
- 같은 insight를 중복 반영하지 않습니다.

기본 stdout:

```text
Reflect 완료
Apply: true
적용 대상:
- CLAUDE.md
- .claude/rules/<path>.md

적용 결과:
- <added> added
- <updated> updated
- <skipped> skipped as duplicate

요약:
- <한글 insight summary>
```

Dry-run stdout:

```text
Reflect 완료
Apply: false
예상 대상:
- CLAUDE.md
- .claude/rules/<path>.md

미리보기 결과:
- <added> would add
- <updated> would update
- <skipped> skipped as duplicate

요약:
- <한글 preview summary>
```

Reflect excludes:

- branch-specific one-off decision
- temporary Spec Patch itself
- superseded decision
- P3/nit
- rejected finding
- low-confidence observation
- unresolved source conflict
- 별도 `tigerkit-reflections.md` sidecar 생성

## `/tk:handoff` Output Contract

- 목적: 다음 세션이나 다른 작업자가 이어받을 continuation 문서를 작성합니다.
- 기본 기록 위치: `.claude/handoffs/current.md`
- `archive=true` 또는 사용자 명시 archive 요청이 있을 때만 dated archive를 추가로 만듭니다.
- v7.2에서는 최신 branch-local Spec Patch, Gap Run, Verify Run path를 Relevant Files 또는 Validation에 포함할 수 있습니다.
- handoff는 durable rule 저장소가 아닙니다.

채팅 receipt:

```text
handoff 작성했습니다.
- 기록: .claude/handoffs/current.md
- archive: 없음
- next action: .claude/handoffs/current.md 읽고 Next Actions부터 이어가.
```

필수 section:

```md
# Handoff: <task title>

## Reader Guide
## Mission
## Current State
## Key Decisions
## Relevant Files
## Basis / References
## Completed Work
## Pending Work
## Known Risks / Unknowns
## Failed Attempts / Do Not Repeat
## Validation
## Next Actions
## Resume Prompt
```

## `/tk:meta-feedback` Output Contract

- 목적: 현재 세션에서 관측된 TigerKit command/skill 개선점을 프로젝트 자산 유출 없이 일반화합니다.
- 세션 내역 전체에서 friction, 사용자 교정, 반복 실수, output UX 문제, latency 문제, false-positive pattern을 찾습니다.
- 기본값은 proposal-only입니다.
- `--out <path>`가 있을 때만 current worktree root 내부 지정 경로에 파일을 작성할 수 있습니다.
- worktree root 밖 경로, user home, `/tmp`, hidden control file path에는 쓰지 않습니다.
- raw session evidence, 사용자 원문 quote, repo 이름, product 이름, 도메인 고유명, 내부 path, URL, ticket, branch, PR 번호, commit hash를 출력하지 않습니다.
- repo rule patch는 `/tk:reflect`, basis-target 비교는 `/tk:gap` 대상으로 분리합니다.

필수 section:

```md
## Meta Feedback Summary
- Target: <skill-or-command>
- Feedback class: <ux|output-format|taxonomy|safety|dispatch|docs|performance|false-positive>
- Privacy status: generalized

## Generalized Friction
- Situation: <generic situation>
- Problem: <generic problem>
- Impact: <generic impact>

## Proposed Improvement
- Change: <generic skill/command improvement>
- Why: <reason without project-specific evidence>

## Redaction Receipt
- Removed: <repo names|paths|URLs|domain labels|quoted user text>
- Kept: <abstract pattern only>
- Unsafe details included: none
```

안전하게 일반화할 수 없으면 `Privacy status: cannot_generalize_safely`, `Change: none`, `Why: privacy gate failed`를 사용합니다.

## Evidence Rule

중요 판단은 아래 구분을 유지합니다.

```text
Evidence = directly observed
Interpretation = inferred from evidence
Decision = confirmed by user or source contract
Suggestion = proposed, not confirmed
```

## Storage Rule

`spec`, `gap`, `verify-before-stop` generated artifacts는 current worktree root 아래 `.claude/tigerkit/branches/<branch-key>/`에 저장합니다.

금지:

- `/tmp`
- `$GIT_COMMON_DIR`
- `.git/worktrees/*`
- user home global path
- current worktree root 밖 path

## detail 원칙

- command별 stdout은 필요한 만큼만 작성합니다.
- 다음 행동은 자연어로 짧게 제시합니다.
- 근거가 부족한 항목은 추측하지 않고 `unknown`, rejected, 또는 source conflict로 둡니다.
