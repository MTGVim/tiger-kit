---
description: 세션 결과에서 재사용 가능한 learning을 안전한 promotion surface로 분류합니다.
argument-hint: "[scope] [--dry-run] [--apply=true|false] [--target <repo|user>]"
---

이 명령은 TigerKit `/tk:reflect` contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:reflect`는 세션 내용, 실제 변경 결과, 성공/실패, 사용자 피드백에서 재사용 가능한 learning과 improvement를 추출하고, 안전한 promotion router로서 가장 적절한 durable promotion surface로 분류합니다.

```text
reflect = session result + feedback -> classify learning -> promote to the right surface
```

## When to use

- 의미 있는 작업이 끝났을 때
- 시행착오에서 다음 세션에도 유효한 규칙이 생겼을 때
- repo/user guidance, skill, hook, command, agent, discard 중 어디에 둘지 분류할 가치가 있을 때

## Promotion taxonomy

| Target | Policy | Use when |
|---|---|---|
| repo `CLAUDE.local.md` | auto apply | 이 repo에만 필요한 private/local guidance |
| repo `CLAUDE.md` proposal | suggest only | 팀 공유 repo rule 후보 |
| user `PROFILE.md` | auto apply | 사용자 역할, 선호, 협업 방식 |
| user `CLAUDE.md` | auto apply | 모든 repo에 걸친 사용자 guidance |
| user skills | auto apply | 반복 가능한 procedural routine. canonical source는 TigerKit generated state가 아닌 user skill surface가 소유 |
| hook / hookify proposal | suggest only | 반복 실수를 자동으로 막거나 검사할 수 있는 후보 |
| command proposal | suggest only | 새 slash command가 더 나은 사용자-facing workflow 후보 |
| agent proposal | suggest only | 독립 역할/전문성이 필요한 sub-agent 후보 |
| discard | never store | branch-specific one-off, 저신뢰, 민감 정보, 이미 코드/문서에 충분한 내용 |

## Apply policy

중요:

- 리포 내부 자동 생성/수정은 `CLAUDE.local.md`만 허용합니다.
- 리포 공용 `CLAUDE.md`는 자동 수정하지 않습니다.
- `CLAUDE.md` 승격 후보는 diff 형식으로 제안만 합니다.
- source code는 수정하지 않습니다.
- hook / hookify, command, agent 변경은 제안만 합니다.
- user skills auto apply는 user skill surface가 canonical source를 소유할 때만 적용합니다. TigerKit generated state에 skill source를 생성하거나 복제하지 않습니다.
- 제안은 설치됨/활성화됨으로 표현하지 않습니다.
- branch-specific one-off는 durable rule로 승격하지 않고 `discard`로 분류합니다.
- 민감하거나 불필요한 사용자 정보는 저장하지 않습니다.
- 중복 규칙은 병합합니다.
- 충돌 규칙은 적용 조건을 분리합니다.

## Proposal quality

제안 후보는 한 bucket에 섞지 않고 proposal type별로 분리합니다.

### Hook / hookify proposal

Hook / hookify proposal은 반복 실수를 자동으로 막거나 검사할 수 있지만 아직 자동 설치하면 안 되는 후보입니다. 각 후보에는 아래 필드를 포함합니다.

- rationale: 어떤 반복 문제나 누락을 줄이는지
- trigger: 언제 실행되어야 하는지
- action: 어떤 검사, 안내, 차단, 기록을 수행할지
- why suggest-only: 왜 지금 설치/활성화하지 않고 사용자 검토가 필요한지

금지: hook 파일 생성, settings 자동 수정, 설치됨/활성화됨 표현, source code 수정, destructive action 자동화.

### Command proposal

Command proposal은 사용자가 직접 호출하는 slash command가 skill보다 나은 workflow 후보입니다. 각 후보에는 아래 필드를 포함합니다.

- intent: 사용자가 얻는 결과와 command의 목적
- arguments: 필요한 인자, option, 입력 형태
- when better than skill: 사용자가 명시적으로 호출해야 하거나, 출력 계약/receipt가 고정되어야 하거나, plugin command surface로 노출하는 편이 나은 이유

금지: command 파일 생성, plugin manifest 수정, runtime generation, 기존 command surface 변경을 적용된 것으로 표현.

### Agent proposal

Agent proposal은 독립 역할이나 전문성이 필요한 sub-agent 후보입니다. 각 후보에는 아래 필드를 포함합니다.

- role boundary: agent가 맡는 역할과 맡지 않는 역할
- responsibility: 입력, 산출물, 검증 책임
- when better than command: 독립 조사, 병렬 작업, 전문 판단, 긴 context 격리가 command보다 나은 이유

금지: agent 파일 생성, 자동 dispatch 설정, orchestration runtime 생성, command로 충분한 작업을 agent로 과대 승격.

## Candidate status

- `candidate`: 근거는 있으나 아직 적용하지 않음.
- `confirmed`: 사용자 또는 source evidence로 확정됨.
- `session-local`: 이번 세션에만 유효함.
- `deprecated`: 더 이상 맞지 않거나 대체됨.
- `discard`: 저장하지 않음.

## Output

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

`--dry-run` 또는 `--apply=false`는 preview만 출력하고 파일을 수정하지 않습니다. 이 경우 auto-apply 대상 상태값은 `applied` 대신 `preview_only`를 사용합니다.

파일을 쓰는 경우 `Changed paths`에 실제 수정한 path를 모두 출력합니다. 파일을 쓰지 않으면 `NONE`을 출력합니다.

## 금지

- repo shared `CLAUDE.md` 직접 수정
- source code 수정
- hook / hookify, command, agent 변경 자동 적용
- hook / hookify, command, agent proposal을 설치됨/활성화됨으로 표현
- branch-specific one-off를 durable rule로 승격
- rejected/low-confidence/민감 정보 저장
