# Reflect File Policy

`/tk:reflect`는 promotion router로서 세션 learning을 canonical target으로 분류하고, repo-local guidance는 기본 apply(opt-out)로 `<git-root>/CLAUDE.local.md`에 반영할 수 있습니다. `skill/hook/command/agent` source는 직접 생성하지 않으며, durable artifact 생성은 `/tk:forge`가 맡습니다.

## Default policy

- 기본 동작은 **repo-local apply enabled** 입니다.
- option 생략은 repo-local apply를 시도합니다.
- `--apply=false`는 preview-only opt-out입니다.
- `--apply=true`는 명시적 apply 표기용이며 기본 동작을 바꾸지 않습니다.
- source code, repo shared `CLAUDE.md`, user-global guidance, skill source, hook settings, command source, agent source, plugin manifest는 수정하지 않습니다.

## Canonical promotion targets

Canonical target enum은 정확히 아래 8개입니다.

```text
repo-local, repo-shared, user-global, skill, hook, command, agent, discard
```

| Target | Write policy | Notes |
|---|---|---|
| `repo-local` | eligible default apply 또는 explicit apply일 때만 `<git-root>/CLAUDE.local.md` write 가능 | repo-local private guidance |
| `repo-shared` | suggest-only | shared repo rule 후보 |
| `user-global` | suggest-only | 모든 repo에 영향을 주는 user-global instruction 또는 rule 후보 |
| `skill` | suggest-only from reflect | source generation은 forge-owned |
| `hook` | suggest-only | lifecycle 자동화 또는 검사 후보 |
| `command` | suggest-only | slash command 후보 |
| `agent` | suggest-only | sub-agent 후보 |
| `discard` | no write | 저장하지 않음 |

`PROFILE.md`, `automation`, `hookify`, `hook / hookify`는 target 이름이 아닙니다. 기존 `PROFILE.md`는 legacy/inactive state로만 보고 자동 삭제하거나 자동 이관하지 않습니다.

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

`candidate_id`는 ledger 안에서만 식별됩니다. forge가 candidate를 읽을 때는 chat prose가 아니라 ledger를 source of truth로 삼아야 합니다.

## Apply plan

repo-local write는 exact apply plan 없이 수행하지 않습니다. 다만 exact `apply_plan`은 기본적으로 **ledger에만** 기록합니다. stdout은 compact summary만 유지합니다.

Apply plan에는 아래가 포함되어야 합니다.

- exact apply set
- `base_state`
- `base_sha256`
- `result_sha256`
- planned result bytes
- `planned_result_bytes_sha256`
- exact unified diff
- target path와 root-relative `CLAUDE.local.md` operand

## All-or-nothing and rollback

여러 eligible repo-local 후보는 하나의 planned result bytes로 합치고 all-or-nothing으로 적용합니다.

Write 후에는 target bytes와 `result_sha256`을 검증합니다. verification 실패는 `apply_verification_failed`로 보고하고 rollback을 시도합니다. rollback success/failure는 ledger에 남깁니다.

## Forge relationship

- `reflect`는 `skill/hook/command/agent` 후보를 제안할 수 있습니다.
- `reflect`는 그 source를 직접 생성하지 않습니다.
- `/tk:forge`는 직전 same-session ledger의 `candidate_id`를 받아 실제 artifact를 생성합니다.
- 1차 forge 범위는 `skill only`입니다.
