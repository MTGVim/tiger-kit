# TigerKit 운영 Output Contract

이 문서는 TigerKit command의 출력 계약을 정의합니다.

## 공통 원칙

- 사용자-facing label은 한글로 씁니다.
- 코드, path, URL, identifier, status code, field name은 원문을 유지할 수 있습니다.
- Evidence, Interpretation, Decision, Suggestion을 구분합니다.
- 검증하지 않은 success를 선언하지 않습니다.
- command가 파일을 쓰면 path를 출력합니다.

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

```text
Reflect 완료
적용 대상:
- repo CLAUDE.local.md: <applied|not_applicable>
- repo CLAUDE.md: suggest_only:<count>
- user PROFILE.md: <applied|not_applicable>
- user CLAUDE.md: <applied|not_applicable>
- user skills: <applied|not_applicable>

## Repo 후보
n. <candidate or NONE>

## User 후보
n. <candidate or NONE>

## 충돌 / 적용 조건
- <condition or none>

## 다음 행동
- <next step or 없음>
```

`--dry-run` 또는 `--apply=false`이면 preview만 출력하고 파일을 수정하지 않습니다.

## Deprecated output surfaces

아래 status/output surfaces는 새 TigerKit active flow에서 생성하지 않습니다.

- AFK receipt
- Patron decision ledger
- setup receipt
- grill question receipt
- launch workflow receipt
- handoff receipt
