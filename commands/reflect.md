---
description: 세션 결과에서 재사용 가능한 learning을 분류하고 repo-local/user-global guidance 기본 반영 또는 명시적 skill materialize를 수행할 수 있습니다.
argument-hint: '"[candidate_id|scope]" [--apply=false|true] [--target <repo-local|repo-shared|user-global|skill|hook|command|agent|discard|repo|user|all>] [--desc "<freeform description>"] [--dry-run]'
---

이 명령은 TigerKit `/tk:reflect` contract를 따릅니다.

사용자에게는 한글로 답합니다. 코드, path, URL, ticket, commit, hash, identifier, error, contract field name은 원문 그대로 둘 수 있습니다.

목표: `/tk:reflect`는 세션 내용, 실제 변경 결과, 성공/실패, 사용자 피드백에서 재사용 가능한 learning과 improvement를 추출하고, 안전한 promotion router로서 가장 적절한 durable promotion surface로 분류합니다. `repo-local`과 `user-global` guidance는 기본 apply(opt-out)로 반영할 수 있고, `skill` target은 명시적 apply일 때 실제 skill artifact로 materialize할 수 있습니다. `hook/command/agent`는 계속 제안-only 입니다.

canonical skill:

```text
skills/reflect/SKILL.md
```

```text
reflect = session result + feedback -> classify learning -> default repo-local/user-global apply or proposal -> emit compact summary + ledger
```

## Core boundary

- Active command surface는 `/tk:gap`, `/tk:route`, `/tk:reflect`, `/tk:grill`, `/tk:prototype`, `/tk:arch-review`, `/tk:merge-conflict`, `/tk:handoff`, `/tk:to-prd`, `/tk:to-issues`, `/tk:ui-diff`입니다.
- `/tk:reflect`는 Claude Code auto memory를 쓰거나, mirror하거나, backup하지 않습니다.
- `/tk:reflect`는 source code, repo-shared guidance, hook settings, command source, agent source, plugin manifest를 수정하지 않습니다.
- `skill` source materialization은 `--target skill --apply=true`일 때만 허용됩니다.
- `hook/command/agent` source materialization은 후속 수동 작업이 맡습니다.
- 기존 `SessionStart` decline marker와 `PROFILE.md`는 legacy/inactive state로만 취급하고 자동 삭제하거나 자동 이관하지 않습니다.

## When to use

- 의미 있는 작업이 끝났을 때
- 시행착오에서 다음 세션에도 유효한 규칙이 생겼을 때
- repo/user guidance, skill, hook, command, agent, discard 중 어디에 둘지 분류할 가치가 있을 때
- local guidance는 바로 반영하고, durable skill 후보는 제안만 하고 싶을 때

모든 candidate가 no-op이면 기본 출력은 `Reflect: 반영할 변경 없음.` 한 줄입니다.

## Canonical target enum

Canonical target은 정확히 아래 8개입니다.

```text
repo-local, repo-shared, user-global, skill, hook, command, agent, discard
```

| Target | Action boundary | Use when |
|---|---|---|
| `repo-local` | default apply 또는 explicit apply일 때 eligibility를 통과한 `<git-root>/CLAUDE.local.md`만 write 가능 | 현재 repo에서 한 사용자에게만 필요한 private/local guidance |
| `repo-shared` | suggest-only | 팀 공유 repo rule 후보 |
| `user-global` | default apply 또는 explicit apply일 때 host-native user-global guidance surface에 write 가능 | 모든 repo에 걸친 사용자 guidance 후보 |
| `skill` | explicit apply일 때만 source 생성 가능 | 반복 가능한 procedural routine 후보 |
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

`--target repo`는 eligible `repo-local` 후보만 direct write할 수 있습니다. `--target user`는 eligible `user-global` 후보만 direct write할 수 있습니다. `--target all`은 eligible `repo-local`과 eligible `user-global` 후보만 direct write할 수 있습니다. 다른 effective target은 모두 `suggest_only`, `preview_only`, 또는 `discard`로 남깁니다.

## Apply policy

기본 동작은 repo-local + user-global apply enabled 입니다.

- option 없음: repo-local 또는 user-global candidate가 있고 eligibility를 통과하면 apply를 시도합니다.
- `--apply=false`: 파일을 쓰지 않고 preview만 출력합니다.
- `--apply=true`: 명시적 apply 표기용입니다.
- `repo-local`과 `user-global`만 기본 apply 대상입니다.
- `skill`은 `--target skill --apply=true`일 때만 source write 후보가 됩니다.
- `repo-shared`, `hook`, `command`, `agent`는 direct source write 하지 않습니다.
- target `discard`는 action `discard`이고 path/write가 없습니다.

## User-global write targets

Claude Code 계열처럼 `CLAUDE.md` user/global surface를 가진 host에서는 아래를 user-global direct write target으로 볼 수 있습니다.

```text
~/.claude/CLAUDE.md
~/.claude/rules/<rule-name>/CLAUDE.md
```

선택 원칙:

1. 여러 repo에 공통으로 적용되는 일반 규칙이면 `~/.claude/CLAUDE.md`
2. 특정 주제/경로/작업군으로 분리하는 편이 낫다면 `~/.claude/rules/<rule-name>/CLAUDE.md`
3. host가 `CLAUDE.md` 계열 파일을 직접 다루지 않으면 host-native user-global guidance surface로 해석합니다.
4. host-native writable surface를 확인할 수 없으면 그 candidate는 `suggest_only`로 남기고 이유를 출력합니다.

## User-global write contract

`user-global` apply는 host가 writable guidance surface를 정확히 resolve할 수 있을 때만 수행합니다.

1. host-native writable target path 또는 equivalent handle을 먼저 확정합니다.
2. exact target을 확정하지 못하면 `suggest_only` 또는 `candidate_not_eligible`입니다.
3. exact `apply_plan`은 repo-local과 같은 수준으로 current invocation 기준 `target_path`, `base_state`, `base_sha256`, `result_sha256`, `planned_result_bytes_sha256`, `unified_diff`를 기록합니다.
4. host가 일반 filesystem path를 제공하면 same-directory temp file + atomic replace를 우선합니다.
5. host가 path 대신 native write primitive를 제공하면 그 primitive로 쓰되, post-write readback 또는 equivalent verification을 수행해야 합니다.
6. verification 실패는 `apply_verification_failed`, 복구 실패는 `rollback_failed`로 보고합니다.

## Reason code vocabulary

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

## Repo-local write eligibility

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

Reject된 후보는 write하지 않고 `suggest_only` 또는 `preview_only`로 보고합니다. `not_ignored`는 `.gitignore`, `.git/info/exclude`, global exclude 후보 문구를 제안할 수 있지만, 해당 ignore 파일을 자동 수정하면 안 됩니다. Eligible 후보가 없으면 `no_eligible_candidates`를 출력하고 어떤 candidate도 Applied로 보고하지 않습니다.

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

- `candidate_id`는 current invocation ledger 안에서 유일합니다.
- `status: confirmed`는 routing evidence sufficiency를 뜻하며 durable write approval이 아닙니다.
- `duplicate_status`는 관찰 가능한 evidence가 있을 때만 `confirmed`입니다. 관찰하지 못했으면 `unknown`입니다.
- `discard` target은 action `discard`, path `NONE`, write 없음입니다.
- branch-specific one-off 또는 workaround discard는 `reason_code: session_local`을 쓸 수 있습니다. `session-local` status은 쓰지 않습니다.
- `deprecated` 후보는 write set에 들어갈 수 없습니다.

## Ledger contract

`/tk:reflect`는 compact human summary와 별도로 machine-readable ledger를 남깁니다.

권장 path:

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml
```

ledger는 최소한 아래를 포함합니다.

```yaml
schemaVersion: tigerkit.reflect-ledger/v1
invocation_id: <id>
requested_target: <raw target>
effective_targets: [repo-local, user-global, skill]
ledger_path: <absolute path>
summary:
  - <compact bullet>
candidates:
  - candidate_id: R1
    status: confirmed
    duplicate_status: unknown
    action: apply
    target: repo-local
    path: <git-root>/CLAUDE.local.md
    evidence: <direct observed evidence>
    reason: <routing reason>
apply_plan: <optional exact plan object>
```

## Apply plan contract

repo-local 또는 user-global write는 exact apply plan 없이 수행하지 않습니다. exact `apply_plan`은 **ledger에만** 기록합니다.

```yaml
apply_plan:
  invocation_id: <current invocation id>
  target_path: <resolved writable target path>
  path_operand: <repo-local이면 CLAUDE.local.md, 아니면 host-native operand or NONE>
  candidate_ids: [R1]
  apply_set: [R1]
  base_state: present | absent
  base_sha256: <sha256 or NONE>
  result_sha256: <sha256>
  planned_result_bytes_sha256: <sha256>
  unified_diff: |
    --- a/<target>
    +++ b/<target>
    ...
```

Rules:

- apply plan은 current invocation에만 유효합니다.
- apply set은 정확하고 immutable입니다.
- 여러 eligible 후보는 exact target별 planned result bytes로 합치고 all-or-nothing으로 처리합니다.
- write 직전 base state와 base hash를 다시 확인합니다.
- write 후 실제 bytes를 읽어 `result_sha256`과 비교합니다.
- verification 실패는 `apply_verification_failed`로 보고하고 rollback을 시도합니다.

## Output

기본 projection은 compact합니다.

- stdout은 `요약 + ledger path + 다음 행동` 구조를 따릅니다.
- exact `apply_plan`, full candidate detail, diff raw는 ledger를 source of truth로 삼습니다.
- empty target section, default empty list, standalone `NONE` line은 의미 보존에 필요할 때만 출력합니다.
- 모든 candidate가 no-op이면 출력은 정확히 `Reflect: 반영할 변경 없음.` 한 줄입니다.

```text
Reflect 완료
Requested target: <raw requested target or default>
Effective targets: <canonical target list>
[Deprecation: <deprecation line when legacy selector used>]
Summary:
- <what changed or what was proposed>
Ledger: <absolute ledger path>
[Changed paths:
- <path>]
[## 다음 행동
- <next step>]
```

## Skill materialize mode

- `reflect`는 `skill/hook/command/agent` 후보를 제안할 수 있습니다.
- `skill`만 explicit apply로 source 생성 가능합니다.
- `candidate_id`는 same-session + same-ledger에서만 유효합니다.
- write target은 agent가 지원하는 user skill surface입니다. Claude Code 계열이면 `~/.claude/skills/<name>/SKILL.md`가 예시입니다.
- 이름 확정 전 write 금지
- `hook|command|agent`는 여전히 제안-only 입니다.

## 금지

- repo shared `CLAUDE.md` 직접 수정
- host-native writable surface를 확인하지 못한 `user-global` direct write
- `PROFILE.md` 생성/수정/promotion output
- explicit apply 없는 skill source 생성/수정/복제
- hook settings, command source, agent source, plugin manifest 자동 수정
- `automation`, `hookify`, `hook / hookify`를 target 이름으로 사용
- source code 수정
- Claude Code auto memory 쓰기, mirror, backup
- branch-specific one-off를 durable rule로 승격
- rejected/low-confidence/민감 정보 저장
