# Reflect File Policy

`/tk:reflect`는 세션 learning을 안전한 대상에만 반영한다.

## Target policy

| Target | Policy | Notes |
|---|---|---|
| repo `CLAUDE.local.md` | auto apply | repo-local private guidance |
| repo `CLAUDE.md` | suggest only | shared repo rule이므로 자동 수정 금지 |
| user `PROFILE.md` | auto apply | user-level preference/profile |
| user `CLAUDE.md` | auto apply | user-level guidance |
| user skills | auto apply | reusable routine skill 후보 |

## Repo shared rule boundary

리포 내부 자동 생성/수정은 `CLAUDE.local.md`만 허용한다. Shared `CLAUDE.md`는 항상 diff proposal로만 제시한다.

## Candidate states

- `candidate`: 근거는 있으나 적용 전.
- `confirmed`: 사용자 또는 source evidence로 확정.
- `session-local`: 이번 세션에만 유효.
- `deprecated`: 더 이상 적용하지 않음.

## Merge and conflict

- 중복 규칙은 병합한다.
- 충돌 규칙은 적용 조건을 분리한다.
- branch-specific one-off는 durable rule로 승격하지 않는다.
- 민감하거나 불필요한 사용자 정보는 저장하지 않는다.

## Output requirement

Reflect receipt는 아래를 분리한다.

- repo 후보
- user 후보
- 충돌 / 적용 조건
- 다음 행동
