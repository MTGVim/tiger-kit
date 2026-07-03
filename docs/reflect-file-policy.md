# Reflect File Policy

`/tk:reflect`는 promotion router로서 세션 learning을 canonical target으로 분류하고, repo-local guidance는 기본 apply(opt-out)로 `<git-root>/CLAUDE.local.md`에 반영할 수 있습니다. `user-global` guidance도 지원 host에서는 기본 apply(opt-out)로 user-level guidance surface에 반영할 수 있습니다. `skill` target은 explicit apply일 때만 source 생성이 가능하고, `hook/command/agent` source는 직접 생성하지 않습니다.

## Default policy

- 기본 동작은 **repo-local + user-global apply enabled** 입니다.
- option 생략은 eligible `repo-local` 또는 `user-global` apply를 시도합니다.
- `--apply=false`는 preview-only opt-out입니다.
- `--apply=true`는 명시적 apply 표기용이며 기본 동작을 바꾸지 않습니다.
- source code, repo shared `CLAUDE.md`, hook settings, command source, agent source, plugin manifest는 수정하지 않습니다.
- skill source 생성은 explicit apply일 때만 허용합니다.

## Canonical promotion targets

Canonical target enum은 정확히 아래 8개입니다.

```text
repo-local, repo-shared, user-global, skill, hook, command, agent, discard
```

| Target | Write policy | Notes |
|---|---|---|
| `repo-local` | eligible default apply 또는 explicit apply일 때만 `<git-root>/CLAUDE.local.md` write 가능 | repo-local private guidance |
| `repo-shared` | suggest-only | shared repo rule 후보 |
| `user-global` | eligible default apply 또는 explicit apply일 때 host-native user-global guidance surface write 가능 | Claude Code 계열이면 `~/.claude/CLAUDE.md` 또는 `~/.claude/rules/<rule-name>/CLAUDE.md` |
| `skill` | explicit apply일 때만 source 생성 가능 | 기본은 제안-only |
| `hook` | suggest-only | lifecycle 자동화 또는 검사 후보 |
| `command` | suggest-only | slash command 후보 |
| `agent` | suggest-only | sub-agent 후보 |
| `discard` | no write | 저장하지 않음 |

`PROFILE.md`, `automation`, `hookify`, `hook / hookify`는 target 이름이 아닙니다. `PROFILE.md`는 reflect target이 아니며 자동 생성하거나 자동 이관하지 않습니다.

## User-global write contract

`user-global` apply는 host가 writable guidance surface를 정확히 resolve할 수 있을 때만 허용합니다.

1. exact target path 또는 equivalent native handle을 먼저 확정합니다.
2. exact target을 확정하지 못하면 `suggest_only` 또는 `candidate_not_eligible`입니다.
3. exact `apply_plan`은 `target_path`, `base_state`, `base_sha256`, `result_sha256`, `planned_result_bytes_sha256`, `unified_diff`를 current invocation 기준으로 기록합니다.
4. 일반 filesystem path가 있으면 same-directory temp file + atomic replace를 우선합니다.
5. path 대신 host-native write primitive만 있으면 write 후 readback 또는 equivalent verification을 수행합니다.
6. verification 실패는 `apply_verification_failed`, 복구 실패는 `rollback_failed`입니다.

## Repo-local write target

유일한 repo-local write target:

```text
<git-root>/CLAUDE.local.md
```

path operand는 root-relative literal `CLAUDE.local.md`만 허용합니다.

## Repo-local eligibility checks

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

1. fixed invocation cwd를 `invocation_cwd`로 기록합니다.
2. `git -C <invocation_cwd> rev-parse --is-inside-work-tree`를 argument vector로 실행합니다.
3. `git -C <invocation_cwd> rev-parse --show-toplevel`로 git root를 구합니다.
4. 이후 모든 Git 검사는 `git -C <git-root>`로 실행합니다.
5. path operand는 `CLAUDE.local.md` literal만 허용합니다.
6. normalized absolute path가 repo 밖으로 나가면 reject합니다.
7. symlink target은 reject합니다.
8. tracked file이면 reject합니다.
9. ignored가 아니면 reject합니다.
10. shell string concatenation 대신 argument vector를 사용합니다.

Reject는 silent skip이 아닙니다. Receipt/ledger에 `reason_code`를 남기고 write하지 않습니다.

## Compact receipt expectation

stdout receipt는 compact하지만 아래 의미를 숨기면 안 됩니다.

- `repo-local`, `user-global` = direct-apply candidate
- `skill` = explicit materialize only
- `repo-shared`, `hook`, `command`, `agent` = suggest-only
- reject/failure = `reason_code` 또는 동등한 reject 이유 노출
- write failure = `Applied candidates: NONE`
- rollback = `succeeded | failed | not_needed`

## Ledger contract

`/tk:reflect`는 compact human summary와 별도로 machine-readable ledger를 남깁니다.

권장 path:

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml
```

ledger는 최소한 아래를 담아야 합니다.

- `schemaVersion`
- `invocation_id`
- `requested_target`
- `effective_targets`
- `ledger_path`
- `candidates[]`
- optional `apply_plan`
- write result / rollback result when relevant

`candidate_id`는 ledger 안에서만 식별됩니다. reflect skill-materialize mode가 candidate를 읽을 때는 chat prose가 아니라 ledger를 source of truth로 삼아야 합니다.

## Apply plan

repo-local 또는 user-global write는 exact apply plan 없이 수행하지 않습니다. 다만 exact `apply_plan`은 기본적으로 **ledger에만** 기록합니다. stdout은 compact summary만 유지합니다.

Apply plan에는 아래가 포함되어야 합니다.

- exact apply set
- `base_state`
- `base_sha256`
- `result_sha256`
- planned result bytes
- `planned_result_bytes_sha256`
- exact unified diff
- target path
- repo-local이면 root-relative `CLAUDE.local.md` operand, 아니면 host-native operand 또는 `NONE`

## All-or-nothing and rollback

여러 eligible 후보는 exact target별 planned result bytes로 합치고 all-or-nothing으로 적용합니다.

Write 후에는 target bytes와 `result_sha256`을 검증합니다. verification 실패는 `apply_verification_failed`로 보고하고 rollback을 시도합니다. rollback success/failure는 ledger에 남깁니다.

## Skill materialize relationship

- `reflect`는 `skill/hook/command/agent` 후보를 제안할 수 있습니다.
- `skill`만 explicit apply로 source 생성 가능합니다.
- write target: agent가 지원하는 user skill surface. Claude Code 계열이면 `~/.claude/skills/<name>/SKILL.md`가 예시입니다.
- `hook|command|agent`는 여전히 source 생성하지 않습니다.
