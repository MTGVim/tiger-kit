# TigerKit 운영 Output Contract

이 문서는 TigerKit v7 command의 출력 계약을 정의합니다. 사용 흐름은 `.tigerkit/docs/usage.md`, 산출물 위치는 `.tigerkit/docs/artifact-layout.md`를 기준으로 봅니다.

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

## `/tk:spec` Output Contract

- 목적: raw instruction을 현재 branch-local Spec Patch로 저장합니다.
- 기본 저장 위치: `.claude/tigerkit/branches/<branch-key>/specs/`
- 기본 stdout은 summary만 출력합니다.
- Spec Patch 전체 본문은 `--print-body`가 있을 때만 출력합니다.
- `spec`은 finding을 만들지 않고 구현 분석을 하지 않습니다.

기본 stdout:

```text
Created Spec Patch: <SP-ID>
Branch Scope: <branch-key>
Path: .claude/tigerkit/branches/<branch-key>/specs/<SP-ID>-<slug>.md
Items:
- <ITEM-ID>
```

Spec Patch는 아래 섹션을 포함합니다.

```md
# Spec Patch: <SP-ID>

## Metadata
## Supersedes
## Product Spec Items
## Design Spec Items
## Design System Spec Items
## Engineering Constraints
## QA Acceptance Criteria
## Analytics Contracts
## Clarification Needed
```

## `/tk:gap` Output Contract

- 목적: Product/Design Spec contract와 implementation plan/current implementation을 비교합니다.
- 기본 저장 위치: `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/`
- 기본 mode는 `auto`입니다.
- `--strict`는 CriticalRedTeamAgent를 정확히 1회 실행합니다.
- `--no-strict`는 red-team pass를 실행하지 않습니다.
- auto mode는 risk trigger가 있을 때만 red-team pass를 1회 실행합니다.
- subagent는 final finding을 확정하지 못합니다.
- JudgeMergerAgent만 final accepted finding을 확정합니다.
- final finding에는 P0/P1/P2만 포함합니다.
- P3/nit/duplicate/unverifiable/source_conflict는 final finding으로 출력하지 않습니다.
- finding이 안 나올 때까지 반복하지 않습니다.

기본 stdout:

```text
Gap Review Complete: <GAP-ID>
Branch Scope: <branch-key>
Mode: <auto|strict|no-strict>
Strict Executed: <yes|no>
Report: .claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md

Findings:
- P0: <count>
- P1: <count>
- P2: <count>

Source Conflicts: <count>
Rejected/Downgraded: <count>
```

Run artifact files:

```text
input-manifest.json
contracts.json
candidates.json
judge-result.json
report.md
```

`report.md` shape:

```md
# Tiger Kit Gap Report: <GAP-ID>

## Summary

## Sources Used

## Actionable Findings

## Rejected / Downgraded Observations

## Source Conflicts / Clarification Needed
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

- 목적: 작업 종료 전 branch-local 검증 evidence를 저장합니다.
- 기본 저장 위치: `.claude/tigerkit/branches/<branch-key>/runs/verify/<VFY-ID>/`
- 기본은 저장입니다.
- `--no-save`는 debugging 용도입니다.
- 전체 report는 `--print-report`가 있을 때만 stdout에 함께 출력합니다.

기본 stdout:

```text
Verification Complete: <VFY-ID>
Branch Scope: <branch-key>
Status: <passed|failed|unknown>
Report: .claude/tigerkit/branches/<branch-key>/runs/verify/<VFY-ID>/report.md
```

Verify run files:

```text
checklist.md
evidence.json
report.md
```

기본 checks:

| ID | Title |
| --- | --- |
| CHK-001 | No unresolved P0/P1 gap findings |
| CHK-002 | Source conflicts handled |
| CHK-003 | Required changes completed |
| CHK-004 | Active specs reviewed |
| CHK-005 | Explicit user requests covered |

Check status:

- `passed`
- `failed`
- `skipped`
- `unknown`

최신 gap run이 없으면 gap-dependent checks는 `unknown` 또는 `skipped`로 둡니다. gap run 부재만으로 failed 처리하지 않고 overall status는 `unknown`으로 둡니다.

## `/tk:reflect` Output Contract

- 목적: branch-local working memory에서 durable repo insight만 추출합니다.
- 기본 동작은 `apply=true`입니다.
- `--dry-run`과 `--apply=false`는 preview-only입니다.
- 기본 durable target은 `.claude/tigerkit-reflections.md`입니다.
- `.claude/tigerkit/` 아래에는 durable insight를 저장하지 않습니다.
- source code는 수정하지 않습니다.
- content write는 durable insight target만 수정합니다.
- branch recency bookkeeping으로 `global-index.json`의 `lastUsedAt`은 갱신할 수 있습니다.
- 같은 insight를 중복 반영하지 않습니다.

기본 stdout:

```text
Reflect Complete
Apply: true
Target: .claude/tigerkit-reflections.md

Applied Insights:
- <added> added
- <updated> updated
- <skipped> skipped as duplicate

Summary:
- <one-line insight summary>
```

Dry-run stdout:

```text
Reflect Complete
Apply: false
Target: .claude/tigerkit-reflections.md

Preview Insights:
- <added> would add
- <updated> would update
- <skipped> skipped as duplicate

Summary:
- <one-line preview summary>
```

Reflect excludes:

- branch-specific one-off decision
- temporary Spec Patch itself
- superseded decision
- P3/nit
- rejected finding
- low-confidence observation
- unresolved source conflict

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
