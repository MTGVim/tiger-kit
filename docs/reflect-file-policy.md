# Reflect File Policy

`/tk:reflect`는 promotion router로서 세션 learning을 preview-first로 분류하고, 명시적 `--apply=true`가 있으며 eligibility를 통과한 repo-local 후보만 `<git-root>/CLAUDE.local.md`에 반영할 수 있다.

## Default policy

- 기본 동작은 preview-only다.
- `--dry-run`, option 없음, `--apply=false`는 파일을 쓰지 않는다.
- `--apply=true`도 eligible `repo-local` apply plan이 있을 때만 파일을 쓸 수 있다.
- source code, repo shared `CLAUDE.md`, user-global guidance, skill source, hook settings, command source, agent source, plugin manifest는 수정하지 않는다.

## Canonical promotion targets

Canonical target enum은 정확히 아래 8개다.

```text
repo-local, repo-shared, user-global, skill, hook, command, agent, discard
```

| Target | Write policy | Notes |
|---|---|---|
| `repo-local` | eligible `--apply=true`일 때만 `<git-root>/CLAUDE.local.md` write 가능 | repo-local private guidance |
| `repo-shared` | suggest-only | shared repo rule 후보 |
| `user-global` | suggest-only | 모든 repo에 영향을 주는 user-global instruction 또는 rule 후보 |
| `skill` | suggest-only | user skill 후보. TigerKit generated state에 source 생성/복제 금지 |
| `hook` | suggest-only | lifecycle 자동화 또는 검사 후보 |
| `command` | suggest-only | slash command 후보 |
| `agent` | suggest-only | sub-agent 후보 |
| `discard` | no write | 저장하지 않음 |

`PROFILE.md`, `automation`, `hookify`, `hook / hookify`는 target 이름이 아니다. 기존 `PROFILE.md`는 legacy/inactive state로만 보고 자동 삭제하거나 자동 이관하지 않는다.

## Legacy selector semantics

| Legacy selector | Canonical expansion | 처리 |
|---|---|---|
| `repo` | `repo-local`, `repo-shared` | deprecation warning 출력 |
| `user` | `user-global` | deprecation warning 출력 |
| `all` | 전체 canonical target | warning 없음 |

`--target repo --apply=true`와 `--target all --apply=true`는 eligible `repo-local` 후보만 write set에 넣을 수 있다. 나머지 target은 `suggest_only`, `preview_only`, 또는 `discard`다.

## Repo-local write target

유일한 repo-local write target:

```text
<git-root>/CLAUDE.local.md
```

path operand는 root-relative literal `CLAUDE.local.md`만 허용한다. 다른 파일명, absolute operand, path traversal, symlink target, repo 밖 resolve path는 reject한다.

## Repo-local eligibility checks

Apply 전 아래를 모두 확인한다.

Reason vocabulary:

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

1. fixed invocation cwd를 `invocation_cwd`로 기록한다.
2. `git -C <invocation_cwd> rev-parse --is-inside-work-tree`를 argument vector로 실행한다. exit 0이 아니면 `not_git_worktree`다.
3. `git -C <invocation_cwd> rev-parse --show-toplevel`을 argument vector로 실행한다. 실패하면 `git_root_resolution_error`다.
4. 이후 모든 Git 검사는 `git -C <git-root>`로 실행한다.
5. path operand는 root-relative literal `CLAUDE.local.md`만 허용한다.
6. `<git-root>/CLAUDE.local.md`를 normalized absolute path로 계산하고, 그 결과가 `<git-root>` 안에 남아 있지 않으면 `path_outside_repo`다.
7. target path는 `lstat`으로 검사한다. symlink이면 symlink target을 따라가지 않고 `symlink_target`으로 reject한다.
8. `git -C <git-root> ls-files --error-unmatch -- CLAUDE.local.md`를 실행한다. exit 0은 `tracked_local_file` reject다. exit 1은 untracked이므로 계속한다. 다른 exit status는 `tracked_check_error`다.
9. `git -C <git-root> check-ignore -q --no-index -- CLAUDE.local.md`를 실행한다. exit 0은 ignored이므로 계속한다. exit 1은 `not_ignored`다. exit 128 또는 그 외 status는 `ignore_check_error`다.
10. executable code가 command를 실행할 때 shell string concatenation을 쓰지 않고 argument vector를 사용한다.

Reject는 silent skip이 아니다. Receipt에 `reason_code`를 남기고 write하지 않는다. `not_ignored`는 ignore entry 제안을 출력할 수 있지만 `.gitignore`, `.git/info/exclude`, global exclude를 자동 수정하지 않는다. Eligible 후보가 없으면 `no_eligible_candidates`를 출력하고 어떤 candidate도 `Applied`로 보고하지 않는다.

## Candidate states and actions

각 candidate는 아래 contract를 따른다.

- `candidate_id`: current invocation 안에서 유일한 ID
- `status`: `candidate | confirmed | deprecated`
- `duplicate_status`: `confirmed | unknown`
- `action`: `preview_only | apply | suggest_only | discard`
- `target`: canonical target enum 중 하나
- `path`: write path 또는 `NONE`

`status: confirmed`는 routing evidence sufficiency이며 durable write approval이 아니다. Claude Code auto memory를 관찰하지 못한 경우 `duplicate_status: unknown`으로 둔다. Branch-specific one-off 또는 workaround discard는 `reason_code: session_local`을 쓸 수 있지만 `session-local` status은 쓰지 않는다. TigerKit은 auto memory를 쓰거나, mirror하거나, backup하지 않는다.

## Apply plan

`--apply=true` write는 current invocation apply plan 없이 수행하지 않는다.

Apply plan은 아래를 포함한다.

- exact apply set
- `base_state`
- `base_sha256`
- `result_sha256`
- planned result bytes
- `planned_result_bytes_sha256`
- exact unified diff
- target path와 root-relative `CLAUDE.local.md` operand

Generic edit, broad rewrite, unscoped append/rewrite는 금지한다. Plan 이후 target 상태가 바뀌면 `stale_apply_plan`으로 전체 apply를 중단한다. 이전 invocation에서 만든 apply plan은 항상 stale이다.

## All-or-nothing and rollback

여러 eligible repo-local 후보는 하나의 planned result bytes로 합치고 all-or-nothing으로 적용한다. 일부 후보만 조용히 적용하지 않는다.

Write 직전 base state/hash를 다시 확인한다. 계획과 다르면 `stale_apply_plan`으로 중단하고 write하지 않는다. Write는 target과 같은 directory에 temporary file을 만들고 fsync 후 atomic replace로 수행한다.

Write 후에는 target bytes와 `result_sha256`을 검증한다. Verification 실패는 `apply_verification_failed`로 보고하고 failed result bytes/hash를 capture한다. 이 경우 no candidate may be reported Applied after verification failure.

rollback precheck로 target이 verification 실패 직후 bytes와 같은지 확인한다. 외부 변경이 있으면 rollback하지 않고 `rollback_failed`를 보고한다. 안전하면 원래 bytes 또는 original absence만 복구한다. Rollback succeeded이면 `Changed paths: NONE`과 `Applied candidates: NONE`이다. Rollback failed 또는 외부 변경이면 `reason_code: rollback_failed`, `Applied candidates: NONE`, changed path를 출력한다.

## Proposal quality requirement

Proposal 후보는 `hook`, `command`, `agent` section으로 분리한다. Generic `automation` bucket이나 `hookify` bucket에 섞지 않는다.

### Hook proposal

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

## Output requirement

Reflect receipt는 compact projection을 기본으로 하면서 아래 의미를 분리한다.

- requested target
- effective targets
- deprecation line where relevant
- candidate table with `candidate_id`, `status`, `duplicate_status`, `target`, `action`, `path`, `reason`
- changed path 전체. 실제 write가 없으면 기본적으로 section을 생략하지만, apply reject/failure 또는 rollback receipt처럼 no-change 증명이 필요한 경우 `Changed paths: NONE`을 명시할 수 있다.
- exact apply plan. plan이 없으면 기본적으로 section을 생략한다.
- repo-local, repo-shared, user-global, skill, hook, command, agent, discard section. 해당 target candidate가 있을 때만 출력한다.
- rollback success/failure when verification fails
- 충돌 / 적용 조건
- 다음 행동

Empty target section, default empty list, standalone `NONE` line은 의미 보존에 필요할 때만 출력한다. 모든 candidate가 no-op이면 출력은 정확히 `Reflect: 반영할 변경 없음.` 한 줄이다.
