# TigerKit 운영 Output Contract

이 문서는 TigerKit command의 출력 계약을 정의합니다.

## 공통 원칙

- 사용자-facing label은 한글로 씁니다.
- 코드, path, URL, identifier, status code, field name은 원문을 유지할 수 있습니다.
- Evidence, Interpretation, Decision, Suggestion을 구분합니다.
- 검증하지 않은 success를 선언하지 않습니다.
- command가 파일을 쓰면 changed path 또는 ledger path를 출력합니다.
- Active command surface는 `/tk:gap`, `/tk:route`, `/tk:reflect`, `/tk:forge`, `/tk:ui-diff`입니다.
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

`/tk:reflect`는 reusable learning을 canonical target으로 분류하고, repo-local guidance는 기본 apply(opt-out)로 반영할 수 있습니다.

### Apply semantics

- option 생략: 기본 apply
- `--apply=false`: preview-only
- `--apply=true`: 명시적 apply 표기용

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
effective_targets: [repo-local, skill]
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

exact `apply_plan`은 stdout이 아니라 ledger에 둡니다.

## `/tk:forge` Output Contract

`/tk:forge`는 reflect가 제안한 candidate를 실제 artifact로 생성합니다. 1차 범위는 `skill only`입니다.

```text
Forge 완료 | Forge 미리보기 | Forge 중단
Input: <candidate_id or --desc>
Target: skill
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
- 생성 전 이름 확정이 필요합니다.
- `--dry-run`은 preview only입니다.
- 상세 preview/diff는 별도 ledger 또는 generated preview file로 둘 수 있습니다.

## `/tk:ui-diff` Output Contract

`/tk:ui-diff`는 provisioning command가 아니라 direct QA surface입니다.

```text
UI Diff 준비 완료 | UI Diff 중단
Mode: env-diff | figma-diff
Profile path:
- <path or NONE>
Engine skill:
- templates/ui-diff/SKILL.md
다음 행동:
- <run diff / inspect missing profile / provide selectors>
```

Rules:
- current repo의 `<root>/.claude/ui-diff/` profile만 읽습니다.
- profile이 없으면 필요한 파일 경로를 안내하고 중단합니다.
- `login.local.md`는 gitignored local override입니다.
- provisioning artifact나 install/update mode는 없습니다.
