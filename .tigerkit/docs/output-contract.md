# TigerKit 운영 Output Contract

이 문서는 TigerKit command의 출력 계약을 정의합니다.

## 공통 원칙

- 사용자-facing label은 한글로 씁니다.
- 코드, path, URL, identifier, status code, field name은 원문을 유지할 수 있습니다.
- Evidence, Interpretation, Decision, Suggestion을 구분합니다.
- 검증하지 않은 success를 선언하지 않습니다.
- command가 파일을 쓰면 changed path를 출력합니다.

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
- Impact:
- Priority:
- Suggested fix:

## Ambiguities / Missing Evidence

| Ref | Question | Evidence checked | Impact | Recommendation |
|---|---|---|---|---|

## Not accepted summary

- <optional low-priority or rejected note>

## Recommended Next Steps

1. <next step>
```

Gap values:

- `missing`
- `mismatch`
- `overbuilt`
- `ambiguous`

Priority values:

- `P0`
- `P1`
- `P2`
- `P3`

Findings에는 P0/P1/P2만 둡니다. P3, duplicate, unverifiable, source conflict, missing evidence는 Ambiguities 또는 Not accepted summary에 둡니다.

## `/tk:reflect` Output Contract

`/tk:reflect`는 promotion router로서 세션 learning을 안전한 promotion surface로 분류합니다. Shared repo `CLAUDE.md`, hook / hookify, command, agent는 suggest-only입니다. source code는 수정하지 않습니다. branch-specific one-off는 durable rule로 승격하지 않고 `discard`로 분류합니다. Proposal 후보는 hook / hookify, command, agent section으로 분리하고, 설치됨/활성화됨/자동 적용으로 표현하지 않습니다. User skills auto apply는 user skill surface가 canonical source를 소유할 때만 적용하며 `.claude/tigerkit/`에 skill source를 생성하거나 복제하지 않습니다.

```text
Reflect 완료
Promotion 결과:
- repo CLAUDE.local.md: <applied|preview_only|not_applicable>
- repo CLAUDE.md proposal: suggest_only:<count>
- user PROFILE.md: <applied|preview_only|not_applicable>
- user CLAUDE.md: <applied|preview_only|not_applicable>
- user skills: <applied|preview_only|not_applicable>
- hook / hookify proposal: suggest_only:<count>
- command proposal: suggest_only:<count>
- agent proposal: suggest_only:<count>
- discard: <count>

## Changed paths
- <path written by this command, or NONE>

## Repo 후보
n. <candidate or NONE>

## User 후보
n. <candidate or NONE>

## Hook / Hookify proposal 후보
n. <candidate or NONE>
- rationale: <why this automation/check helps>
- trigger: <when it would run>
- action: <what it would do>
- why suggest-only: <why user review is required before install/activation>

## Command proposal 후보
n. <candidate or NONE>
- intent: <user-facing outcome>
- arguments: <args/options/input shape>
- when better than skill: <why slash command surface fits better>

## Agent proposal 후보
n. <candidate or NONE>
- role boundary: <owned and excluded scope>
- responsibility: <inputs, outputs, verification responsibility>
- when better than command: <why independent agent role fits better>

## Discard
n. <discarded item and reason or NONE>

## 충돌 / 적용 조건
- <condition or none>

## 다음 행동
- <next step or 없음>
```

Promotion targets:

- repo `CLAUDE.local.md`: auto apply
- repo `CLAUDE.md` proposal: suggest only
- user `PROFILE.md`: auto apply
- user `CLAUDE.md`: auto apply
- user skills: auto apply, canonical source owned by user skill surface outside `.claude/tigerkit/`
- hook / hookify proposal: suggest only
- command proposal: suggest only
- agent proposal: suggest only
- discard: never store

`--dry-run` 또는 `--apply=false`이면 preview만 출력하고 파일을 수정하지 않습니다. 이 경우 auto-apply 대상 상태값은 `applied` 대신 `preview_only`를 사용합니다.

파일을 쓰는 경우 `Changed paths`에 실제 수정한 path를 모두 출력합니다. 파일을 쓰지 않으면 `NONE`을 출력합니다.

## Deprecated output surfaces

아래 status/output surfaces는 새 TigerKit active flow에서 생성하지 않습니다.

- AFK receipt
- Patron decision ledger
- setup receipt
- grill question receipt
- launch workflow receipt
- handoff receipt
