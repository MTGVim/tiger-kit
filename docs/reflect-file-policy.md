# Reflect File Policy

`/tk:reflect`는 promotion router로서 세션 learning을 안전한 promotion surface로 분류하고 허용된 대상에만 반영한다.

## Promotion taxonomy

| Target | Policy | Notes |
|---|---|---|
| repo `CLAUDE.local.md` | auto apply | repo-local private guidance |
| repo `CLAUDE.md` proposal | suggest only | shared repo rule 후보이므로 자동 수정 금지 |
| user `PROFILE.md` | auto apply | user role, preference, collaboration profile |
| user `CLAUDE.md` | auto apply | user-level guidance |
| user skills | auto apply | canonical source는 `.claude/tigerkit/`가 아닌 user skill surface가 소유 |
| hook / hookify proposal | suggest only | 자동화/검사 후보, 제안만 |
| command proposal | suggest only | slash command 후보, 제안만 |
| agent proposal | suggest only | sub-agent 후보, 제안만 |
| discard | never store | branch-specific one-off, 저신뢰, 민감 정보, 중복 |

## Repo shared rule boundary

리포 내부 자동 생성/수정은 `CLAUDE.local.md`만 허용한다. Shared `CLAUDE.md`는 항상 diff proposal로만 제시한다.

## Source and automation boundary

- `/tk:reflect`는 source code를 수정하지 않는다.
- hook / hookify, command, agent 변경은 suggest-only다.
- hook / hookify, command, agent proposal은 설치됨/활성화됨으로 표현하지 않는다.
- user skill source를 `.claude/tigerkit/`에 생성하거나 복제하지 않는다.
- hook 설치, command 생성, agent 생성, plugin manifest 수정, runtime generation을 수행하지 않는다.

## Optional helper docs

선택형 promotion helper guidance는 `.tigerkit/docs/reflect-promotion-helpers.md`에 둔다. 이 문서는 hook / hookify, command, agent proposal을 더 일관되게 쓰기 위한 참고 자료이며 `/tk:reflect` runtime behavior, auto-apply policy, 또는 plugin command surface의 권위 source가 아니다.

문서에 hookify 예시나 promotion receipt 예시가 있어도 hook 설치, settings 수정, command 생성, agent 생성, runtime generation이 발생한 것으로 표현하지 않는다.

## Proposal quality requirement

Proposal 후보는 hook / hookify, command, agent section으로 분리한다. Generic proposal bucket에 섞지 않는다.

### Hook / hookify proposal

각 후보는 아래 필드를 가진다.

- rationale: 어떤 반복 문제나 누락을 줄이는지
- trigger: 언제 실행되어야 하는지
- action: 어떤 검사, 안내, 차단, 기록을 수행할지
- why suggest-only: 왜 지금 설치/활성화하지 않고 사용자 검토가 필요한지

Negative boundary: hook 파일 생성, settings 자동 수정, 설치됨/활성화됨 표현, source code 수정, destructive action 자동화 금지.

### Command proposal

각 후보는 아래 필드를 가진다.

- intent: 사용자가 얻는 결과와 command 목적
- arguments: 필요한 인자, option, 입력 형태
- when better than skill: 사용자가 명시적으로 호출해야 하거나, 출력 계약/receipt가 고정되어야 하거나, plugin command surface가 필요한 이유

Negative boundary: command 파일 생성, plugin manifest 수정, runtime generation, 기존 command surface 변경을 적용된 것으로 표현 금지.

### Agent proposal

각 후보는 아래 필드를 가진다.

- role boundary: agent가 맡는 역할과 맡지 않는 역할
- responsibility: 입력, 산출물, 검증 책임
- when better than command: 독립 조사, 병렬 작업, 전문 판단, 긴 context 격리가 command보다 나은 이유

Negative boundary: agent 파일 생성, 자동 dispatch 설정, orchestration runtime 생성, command로 충분한 작업을 agent로 과대 승격 금지.

## Candidate states

- `candidate`: 근거는 있으나 적용 전.
- `confirmed`: 사용자 또는 source evidence로 확정.
- `session-local`: 이번 세션에만 유효.
- `deprecated`: 더 이상 적용하지 않음.
- `discard`: 저장하지 않음.

## Merge and conflict

- 중복 규칙은 병합한다.
- 충돌 규칙은 적용 조건을 분리한다.
- branch-specific one-off는 durable rule로 승격하지 않고 `discard`로 분류한다.
- 민감하거나 불필요한 사용자 정보는 저장하지 않는다.

## Output requirement

Reflect receipt는 아래를 분리한다.

- repo 후보
- user 후보
- hook / hookify proposal 후보: rationale, trigger, action, why suggest-only 포함
- command proposal 후보: intent, arguments, when better than skill 포함
- agent proposal 후보: role boundary, responsibility, when better than command 포함
- discard와 이유
- 충돌 / 적용 조건
- 다음 행동
- 파일을 쓴 경우 changed path 전체. 파일을 쓰지 않은 경우 `NONE`
