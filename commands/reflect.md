---
description: 세션 결과에서 재사용 가능한 learning을 추출해 정리합니다.
argument-hint: "[scope] [--dry-run] [--apply=true|false] [--target <repo|user>]"
---

이 명령은 TigerKit `/tk:reflect` contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:reflect`는 세션 내용, 실제 변경 결과, 성공/실패, 사용자 피드백에서 재사용 가능한 learning과 improvement를 추출합니다.

```text
reflect = session result + feedback -> safe improvement candidates/apply
```

## When to use

- 의미 있는 작업이 끝났을 때
- 시행착오에서 다음 세션에도 유효한 규칙이 생겼을 때
- repo/user guidance로 남길 가치가 있는 패턴을 발견했을 때

## Apply policy

| Target | Policy |
|---|---|
| repo `CLAUDE.local.md` | auto apply |
| repo `CLAUDE.md` | suggest only |
| user `PROFILE.md` | auto apply |
| user `CLAUDE.md` | auto apply |
| user skills | auto apply |

중요:

- 리포 내부 자동 생성/수정은 `CLAUDE.local.md`만 허용합니다.
- 리포 공용 `CLAUDE.md`는 자동 수정하지 않습니다.
- `CLAUDE.md` 승격 후보는 diff 형식으로 제안만 합니다.
- source code는 수정하지 않습니다.
- 민감하거나 불필요한 사용자 정보는 저장하지 않습니다.
- 중복 규칙은 병합합니다.
- 충돌 규칙은 적용 조건을 분리합니다.

## Candidate status

- `candidate`: 근거는 있으나 아직 적용하지 않음.
- `confirmed`: 사용자 또는 source evidence로 확정됨.
- `session-local`: 이번 세션에만 유효함.
- `deprecated`: 더 이상 맞지 않거나 대체됨.

## Output

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

`--dry-run` 또는 `--apply=false`는 preview만 출력하고 파일을 수정하지 않습니다.

## 금지

- repo shared `CLAUDE.md` 직접 수정
- source code 수정
- branch-specific one-off를 durable rule로 승격
- rejected/low-confidence/민감 정보 저장
