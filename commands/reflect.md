---
description: 세션 결과에서 재사용 가능한 learning을 preview-first promotion result로 분류합니다.
argument-hint: "[scope] [--apply=true|false] [--target <repo-local|repo-shared|user-global|skill|hook|command|agent|discard|repo|user|all>]"
---

이 명령은 TigerKit `/tk:reflect` contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:reflect`는 세션 내용, 실제 변경 결과, 성공/실패, 사용자 피드백에서 재사용 가능한 learning과 improvement를 추출하고, 안전한 promotion router로서 가장 적절한 durable promotion surface로 분류합니다.

```text
reflect = session result + feedback -> classify learning -> preview promotion result -> optional eligible repo-local apply
```

## Core boundary

- Active command surface는 `/tk:gap`, `/tk:loop-spec`, `/tk:execute`, `/tk:reflect`입니다.
- `/tk:reflect`는 execution ID 또는 receipt path가 있으면 persisted execution receipt를 transcript보다 우선 소비합니다.
- `/tk:reflect`는 Claude Code auto memory를 쓰거나, mirror하거나, backup하지 않습니다.
- `/tk:reflect`는 source code, hook settings, command source, agent source, skill source, plugin manifest를 수정하지 않습니다.
- 기존 `SessionStart` decline marker와 `PROFILE.md`는 legacy/inactive state로만 취급하고 자동 삭제하거나 자동 이관하지 않습니다.

## When to use

- 의미 있는 작업이 끝났을 때
- `/tk:execute` execution ID 또는 receipt path를 회고할 때
- 시행착오에서 다음 세션에도 유효한 규칙이 생겼을 때
- repo/user guidance, skill, hook, command, agent, discard 중 어디에 둘지 분류할 가치가 있을 때

모든 candidate가 no-op이면 기본 출력은 `Reflect: 반영할 변경 없음.` 한 줄입니다.

## Canonical target enum

Canonical target은 정확히 아래 8개입니다.

```text
repo-local, repo-shared, user-global, skill, hook, command, agent, discard
```

| Target | Action boundary | Use when |
|---|---|---|
| `repo-local` | `--apply=true`일 때 eligibility를 통과한 `<git-root>/CLAUDE.local.md`만 write 가능 | 현재 repo에서 한 사용자에게만 필요한 private/local guidance |
| `repo-shared` | suggest-only | 팀 공유 repo rule 후보 |
| `user-global` | suggest-only | 모든 repo에 걸친 사용자 guidance 후보 |
| `skill` | suggest-only | 반복 가능한 procedural routine 후보 |
| `hook` | suggest-only | lifecycle 자동화 또는 검사 후보 |
| `command` | suggest-only | 사용자가 직접 호출하는 slash workflow 후보 |
| `agent` | suggest-only | 독립 역할/전문성이 필요한 sub-agent 후보 |
| `discard` | discard only | branch-specific one-off, 저신뢰, 민감 정보, 중복, 이미 코드/문서에 충분한 내용 |

금지 target 이름:

- `PROFILE.md`
- `automation`
- `hookify`
- `hook / hookify`

관련 후보는 의도에 따라 `hook`, `command`, `agent` 중 하나로 분류합니다.

## Legacy selector semantics

`--target`의 legacy selector는 deprecation line을 출력하고 canonical target으로 확장합니다.

| Legacy selector | Effective targets | Deprecation line |
|---|---|---|
| `repo` | `repo-local`, `repo-shared` | `Deprecated target selector: repo expands to repo-local, repo-shared.` |
| `user` | `user-global` | `Deprecated target selector: user expands to user-global.` |
| `all` | `repo-local`, `repo-shared`, `user-global`, `skill`, `hook`, `command`, `agent`, `discard` | 없음 |

`--target repo --apply=true`와 `--target all --apply=true`는 eligible `repo-local` 후보만 write set에 포함할 수 있습니다. 다른 effective target은 모두 `suggest_only`, `preview_only`, 또는 `discard`로 남깁니다.

## Apply policy

기본값은 preview-only입니다.

- `--dry-run`, option 없음, 또는 `--apply=false`: 파일을 쓰지 않고 preview만 출력합니다.
- `--apply=true`: current invocation에서 생성한 exact apply plan에 포함된 eligible `repo-local` 후보만 all-or-nothing으로 적용할 수 있습니다.
- write target은 `<git-root>/CLAUDE.local.md` 하나뿐입니다.
- repo shared `CLAUDE.md`, user-global guidance, skill, hook, command, agent는 자동 수정하지 않습니다.
- target `discard`는 action `discard`이고 path/write가 없습니다.

### Reason code vocabulary

Reflect receipt의 reject/failure reason은 아래 vocabulary를 사용합니다.

```text
not_git_worktree
git_root_resolution_error
path_outside_repo
symlink_target
tracked_local_file
tracked_check_error
not_ignored
ignore_check_error
candidate_not_eligible
stale_apply_plan
apply_verification_failed
rollback_failed
no_eligible_candidates
```

### Repo-local write eligibility

`repo-local` apply는 아래를 모두 통과해야 합니다.

1. invocation 시작 시점의 fixed cwd를 `invocation_cwd`로 기록합니다.
2. `git -C <invocation_cwd> rev-parse --is-inside-work-tree`를 argument vector로 실행합니다. exit 0이 아니면 `not_git_worktree`입니다.
3. `git -C <invocation_cwd> rev-parse --show-toplevel`을 argument vector로 실행합니다. 실패하면 `git_root_resolution_error`입니다.
4. 이후 모든 Git 검사는 `git -C <git-root>`로 실행합니다.
5. path operand는 root-relative literal `CLAUDE.local.md`만 사용합니다.
6. `<git-root>/CLAUDE.local.md`를 normalized absolute path로 계산하고, 그 결과가 `<git-root>` 안에 남아 있지 않으면 `path_outside_repo`입니다.
7. target path는 `lstat`으로 검사합니다. symlink이면 symlink target을 따라가지 않고 `symlink_target`으로 reject합니다.
8. `git -C <git-root> ls-files --error-unmatch -- CLAUDE.local.md`를 실행합니다. exit 0은 tracked file이므로 `tracked_local_file`로 reject합니다. exit 1은 untracked이므로 계속합니다. 다른 exit status는 `tracked_check_error`입니다.
9. `git -C <git-root> check-ignore -q --no-index -- CLAUDE.local.md`를 실행합니다. exit 0은 ignored이므로 계속합니다. exit 1은 `not_ignored`입니다. exit 128 또는 그 외 status는 `ignore_check_error`입니다.
10. executable code가 command를 실행할 때 shell string concatenation을 쓰지 말고 argument vector를 사용합니다.

Reject된 후보는 write하지 않고 `suggest_only` 또는 `preview_only`로 보고합니다. `not_ignored`는 `.gitignore`, `.git/info/exclude`, global exclude 후보 문구를 제안할 수 있지만, 해당 ignore 파일을 자동 수정하면 안 됩니다. Eligible 후보가 없으면 `no_eligible_candidates`를 출력하고 어떤 candidate도 `Applied`로 보고하지 않습니다.

## Candidate contract

각 후보는 최소한 아래 field를 출력합니다.

```yaml
candidate_id: R1
status: candidate | confirmed | deprecated
duplicate_status: confirmed | unknown
action: preview_only | apply | suggest_only | discard
target: repo-local | repo-shared | user-global | skill | hook | command | agent | discard
path: <path or NONE>
evidence: <direct observed evidence>
reason: <routing reason>
```

- `candidate_id`는 current invocation 안에서만 유일합니다.
- `status: confirmed`는 routing evidence sufficiency를 뜻하며 durable write approval이 아닙니다.
- `duplicate_status`는 관찰 가능한 evidence가 있을 때만 `confirmed`입니다. 관찰하지 못했으면 `unknown`입니다.
- `discard` target은 action `discard`, path `NONE`, write 없음입니다.
- branch-specific one-off 또는 workaround discard는 `reason_code: session_local`을 쓸 수 있습니다. `session-local` status은 쓰지 않습니다.
- `deprecated` 후보는 write set에 들어갈 수 없습니다.

## Apply plan contract

`--apply=true`로 write가 가능한 경우에도 먼저 exact apply plan을 출력합니다.

```yaml
apply_plan:
  invocation_id: <current invocation id>
  target_path: <git-root>/CLAUDE.local.md
  path_operand: CLAUDE.local.md
  candidate_ids: [R1]
  apply_set: [R1]
  base_state: present | absent
  base_sha256: <sha256 or NONE>
  result_sha256: <sha256>
  planned_result_bytes_sha256: <sha256>
  unified_diff: |
    --- a/CLAUDE.local.md
    +++ b/CLAUDE.local.md
    ...
```

Rules:

- apply plan은 current invocation에만 유효합니다. 이전 invocation의 plan은 `stale_apply_plan`으로 reject합니다.
- apply set은 정확하고 immutable입니다.
- planned result bytes, `planned_result_bytes_sha256`, `result_sha256`, exact unified diff가 있어야 합니다.
- generic edit, broad rewrite, unscoped append/rewrite path는 금지합니다.
- 여러 eligible 후보는 하나의 `CLAUDE.local.md` result bytes로 합치고 all-or-nothing으로 처리합니다.
- write 직전 base state와 base hash를 다시 확인합니다. plan의 `base_state`/`base_sha256`와 다르면 `stale_apply_plan`으로 전체 apply를 중단하고 write하지 않습니다.
- write는 target과 같은 directory에 temporary file을 만들고 fsync 후 atomic replace로 수행합니다.
- write 후 실제 bytes를 읽어 `result_sha256`과 비교합니다.
- post-write verification 실패는 `apply_verification_failed`로 보고합니다. 이때 failed result bytes/hash를 capture하고 어떤 candidate도 Applied로 보고하지 않습니다.
- rollback precheck로 target이 verification 실패 직후 bytes와 같은지 확인합니다. 외부 변경이 있으면 rollback하지 않고 `rollback_failed`를 보고합니다.
- rollback은 원래 bytes가 있으면 원래 bytes로 atomic restore하고, 원래 파일이 없었으면 안전할 때만 original absence로 되돌립니다.
- rollback이 성공하면 `Changed paths: NONE`입니다.
- rollback이 실패했거나 외부 변경 때문에 중단되면 `reason_code: rollback_failed`와 changed path를 출력합니다.

## Output

```text
Reflect 완료
Requested target: <raw requested target or default>
Effective targets: <canonical target list>
Deprecation: <deprecation line or NONE>

## Promotion 결과
| candidate_id | status | duplicate_status | target | action | path | reason |
|---|---|---|---|---|---|---|

## Changed paths
- <path written by this command, or NONE>

## Apply plan
<apply_plan or NONE>

## Repo-local 후보
n. <candidate or NONE>

## Repo-shared 후보
n. <candidate or NONE>

## User-global 후보
n. <candidate or NONE>

## Skill 후보
n. <candidate or NONE>

## Hook 후보
n. <candidate or NONE>
- rationale: <why this check helps>
- trigger: <when it would run>
- action: <what it would do>
- why suggest-only: <why user review is required before install/activation>

## Command 후보
n. <candidate or NONE>
- intent: <user-facing outcome>
- arguments: <args/options/input shape>
- when better than skill: <why slash command surface fits better>

## Agent 후보
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

### Rollback receipt examples

Rollback success:

```text
Apply result: failed
reason_code: apply_verification_failed
rollback: succeeded
Changed paths: NONE
Applied candidates: NONE
```

Rollback failure:

```text
Apply result: failed
reason_code: rollback_failed
rollback: failed
Changed paths:
- <git-root>/CLAUDE.local.md
Applied candidates: NONE
Required action: inspect target manually before rerun
```

## 금지

- default mode에서 파일 쓰기
- repo shared `CLAUDE.md` 직접 수정
- user-global guidance 직접 수정
- `PROFILE.md` 생성/수정/promotion output
- skill source 생성/수정/복제
- hook settings, command source, agent source, plugin manifest 자동 수정
- `automation`, `hookify`, `hook / hookify`를 target 이름으로 사용
- source code 수정
- Claude Code auto memory 쓰기, mirror, backup
- branch-specific one-off를 durable rule로 승격
- rejected/low-confidence/민감 정보 저장
