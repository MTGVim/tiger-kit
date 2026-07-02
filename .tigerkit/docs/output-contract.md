# TigerKit 운영 Output Contract

이 문서는 TigerKit command의 출력 계약을 정의합니다.

## 공통 원칙

- 사용자-facing label은 한글로 씁니다.
- 코드, path, URL, identifier, status code, field name은 원문을 유지할 수 있습니다.
- Evidence, Interpretation, Decision, Suggestion을 구분합니다.
- 검증하지 않은 success를 선언하지 않습니다.
- command가 파일을 쓰면 changed path 또는 ledger path를 출력합니다.
- Active command surface는 `/tk:gap`, `/tk:route`, `/tk:reflect`, `/tk:grill`, `/tk:prototype`, `/tk:arch-review`, `/tk:merge-conflict`, `/tk:handoff`, `/tk:to-prd`, `/tk:to-issues`, `/tk:ui-diff`입니다.
- 기본 projection은 compact합니다. empty section, default empty list, `NONE` line은 의미 보존에 필요할 때만 출력합니다.

## `/tk:gap` Output Contract

`/tk:gap`은 SoT와 Current Implementation의 one-shot gap analysis입니다.

```md
## Gap Summary

| Area | SoT | Current | Gap | Impact | Priority |
|---|---|---|---|---|---|

## Findings

### 1. <finding title>
- SoT:
- Current:
- Evidence:
- Evidence type:
- Impact:
- Priority:
- Suggested fix:
- Route: direct | brainstorm | decision
- Route evidence:

## Ambiguities / Missing Evidence

| Ref | Question | Evidence checked | Impact | Recommendation |
|---|---|---|---|---|

## Not accepted summary

- <optional low-priority or rejected note>

## Recommended Next Steps

1. <next step>
```

Artifact path가 필요하면 repo 밖 `~/.tigerkit/.../gap/` 아래에 둡니다.

## `/tk:route` Output Contract

`/tk:route`는 inline-only decision / brainstorming surface입니다.

```text
Route: <direct|subagent-driven|goal-driven|decision|need-sot>
Confidence: high | medium | low
Why
  - <reason>

Tradeoffs
  - <route>: <pros / cons>

Needs first
  - <missing info or NONE>

First step
  - <one concrete next step>
```

기본적으로 persisted artifact를 만들지 않습니다.

## `/tk:reflect` Output Contract

`/tk:reflect`는 reusable learning을 canonical target으로 분류하고, repo-local/user-global guidance는 기본 apply(opt-out)로 반영할 수 있습니다.

### Apply semantics

- option 생략: 기본 apply
- `--apply=false`: preview-only
- `--apply=true`: 명시적 apply 표기용
- 기본 apply 대상: `repo-local`, `user-global`
- explicit materialize 대상: `skill`
- `user-global` direct write는 writable host-native surface를 exact resolve할 수 있을 때만 허용합니다.

### stdout projection

```text
Reflect 완료
Requested target: <raw requested target or default>
Effective targets: <canonical target list>
Summary:
- <what changed or what was proposed>
Ledger: <absolute ledger path or NONE>
[Changed paths:
- <path>]
[다음 행동
- <next step>]
```

### Ledger contract

reflect는 machine-readable ledger + compact human summary를 남깁니다.

권장 path:

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml
```

ledger는 최소한 아래를 포함합니다.

```yaml
schemaVersion: tigerkit.reflect-ledger/v1
invocation_id: <id>
requested_target: <raw target>
effective_targets: [repo-local, user-global, skill]
summary:
  - <compact bullet>
ledger_path: <absolute path>
candidates:
  - candidate_id: R1
    status: candidate | confirmed | deprecated
    duplicate_status: confirmed | unknown
    action: apply | preview_only | suggest_only | discard
    target: repo-local | repo-shared | user-global | skill | hook | command | agent | discard
    path: <path or NONE>
    evidence: <direct observed evidence>
    reason: <routing reason>
apply_plan: <optional exact plan object>
```

exact `apply_plan`은 stdout이 아니라 ledger에 둡니다. `repo-local`과 `user-global` direct write 모두 `target_path`, `base_state`, `base_sha256`, `result_sha256`, `planned_result_bytes_sha256`, `unified_diff`를 포함해야 합니다.

### skill materialize mode

`/tk:reflect --target skill --apply=true`는 reflect가 제안한 candidate를 실제 artifact로 생성합니다. 1차 범위는 `skill only`입니다.

```text
Reflect 완료 | Reflect 미리보기 | Reflect 중단
Requested target: skill
Apply: explicit
Input: <candidate_id or --desc>
Name:
- suggested: <slug>
- confirmed: <slug or NONE>
Ledger: <reflect ledger path or NONE>
Created:
- <path or NONE>
다음 행동:
- <rename/remove/follow-up>
```

Rules:
- `candidate_id`는 same-session + same-ledger만 유효합니다.
- skill source 생성은 explicit apply일 때만 허용합니다.
- 생성 target은 agent가 지원하는 user skill surface입니다. Claude Code 계열이면 `~/.claude/skills/<name>/SKILL.md`가 예시입니다.
- 이름 확정 전 write 금지
- `--dry-run`은 preview only입니다.
- 상세 preview/diff는 별도 ledger 또는 generated preview file로 둘 수 있습니다.

## `/tk:grill` Output Contract

`/tk:grill`은 계획, 설계, RFC, 개선안을 수렴형 질문으로 압박 검증합니다.

```text
Grill 진행중 | Grill 중단 | Grill 요약
Question:
- <one sharp question or NONE>
Why:
- <why this matters>
Known:
- <confirmed facts>
Decision summary:
- <decisions or NONE>
Assumptions:
- <assumptions or NONE>
Risks:
- <remaining risks or NONE>
Next step:
- <continue questioning | proceed with assumptions | stop>
```

## `/tk:prototype` Output Contract

`/tk:prototype`은 UI 또는 logic/state 가설을 throwaway prototype으로 빠르게 검증합니다.

```text
Prototype 준비 | Prototype 완료 | Prototype 중단
Mode: ui | logic
Goal:
- <what is being tested>
Created:
- <prototype files or NONE>
Confirmed:
- <what the prototype proved>
Still fake:
- <what is mocked or assumed>
Next production step:
- <what to port, delete, or refine>
```

## `/tk:arch-review` Output Contract

`/tk:arch-review`는 boundary, ownership, coupling, repeated pain을 evidence-first로 검토하는 report-only 구조 리뷰입니다.

```text
Arch Review 완료 | Arch Review 중단
Scope:
- <target area>
Strengths:
- <what is already clean>
Hotspots:
- <confirmed architectural hotspots>
Boundary risks:
- <where ownership/coupling leaks>
Evidence:
- <file / behavior / repeated pain evidence>
Suggested direction:
- <smallest safe architectural direction>
First step:
- <one concrete next step>
```

## `/tk:merge-conflict` Output Contract

`/tk:merge-conflict`는 merge/rebase conflict를 상태 확인 → intent 추적 → 검증 순서로 해결합니다.

```text
Merge conflict 분석 | Merge conflict 해결 | Merge conflict 중단
State:
- <merge|rebase|none>
Conflict files:
- <file list or NONE>
Hunks:
- <summary>
Resolution:
- <how each intent was reconciled>
Verification:
- <commands run and result or NONE>
Next step:
- <continue merge/rebase | manual follow-up>
```

## `/tk:handoff` Output Contract

`/tk:handoff`는 다음 세션이나 다른 에이전트가 바로 이어받을 수 있는 repo-local handoff를 만듭니다.

```text
Handoff 완료 | Handoff 미리보기 | Handoff 중단
Goal:
- <one-line goal>
Output:
- <path or NONE>
Includes:
- Goal / Current state / Decisions / Changed files / Commands / Verification / Remaining tasks / Open questions / Risks / Suggested next skills / Do-not-repeat context
Verification:
- <verified / partially verified / unverified>
Next step:
- <what the next agent should do first>
```

## `/tk:to-prd` Output Contract

`/tk:to-prd`는 현재 대화나 요구사항을 draft-only PRD로 정리합니다.

```text
To-PRD 완료 | To-PRD 미리보기 | To-PRD 중단
Goal:
- <what the PRD covers>
Output:
- <path or NONE>
Includes:
- problem / goal / user value / non-goals / requirements / acceptance criteria / risks / open questions
Publish:
- disabled by default
Next step:
- <review draft | convert to issues | revise scope>
```

## `/tk:to-issues` Output Contract

`/tk:to-issues`는 plan/PRD를 independently grabbable vertical-slice issue draft로 분해합니다.

```text
To-Issues 완료 | To-Issues 미리보기 | To-Issues 중단
Source:
- <plan|prd|scope>
Output:
- <path or NONE>
Issue count:
- <N>
Rules applied:
- vertical slice only
- no layer slicing
- draft-only by default
Dependencies:
- <blocked-by summary or NONE>
Publish:
- disabled by default
Next step:
- <review drafts | revise slicing | publish explicitly>
```

## `/tk:ui-diff` Output Contract

`/tk:ui-diff`는 provisioning command가 아니라 direct QA surface입니다.

```text
UI Diff 준비 완료 | UI Diff 중단
Mode: env-diff | figma-diff
Profile path:
- <path or NONE>
Engine skill:
- skills/ui-diff/SKILL.md
다음 행동:
- <run diff / inspect missing profile / provide selectors>
```

Rules:
- current repo의 `<root>/.claude/ui-diff/` profile만 읽습니다.
- profile이 없으면 필요한 파일 경로를 안내하고 중단합니다.
- `login.local.md`는 gitignored local override입니다.
- provisioning artifact나 install/update mode는 없습니다.
