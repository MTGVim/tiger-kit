# TigerKit 운영 Output Contract

이 문서는 TigerKit command의 출력 계약을 정의합니다.

## 공통 원칙

- 사용자-facing label은 한글로 씁니다.
- 코드, path, URL, identifier, status code, field name은 원문을 유지할 수 있습니다.
- Evidence, Interpretation, Decision, Suggestion을 구분합니다.
- 검증하지 않은 success를 선언하지 않습니다.
- command가 파일을 쓰면 changed path를 출력합니다.
- Core `tk` plugin은 hook-free이며 active command surface는 `/tk:gap`, `/tk:reflect`, `/tk:loop-spec`입니다.

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
- Evidence type:
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

`Current` evidence는 동일 강도가 아닙니다. 읽은 파일, 실행 결과, rendered output, diff, generated artifact, implementation plan을 구분해서 기록합니다. plan이나 generated artifact만으로 구현 완료를 단정하지 않습니다.

source 간 우선순위가 확인되지 않으면 조용히 병합하지 않고 `ambiguous`로 남깁니다.

## `/tk:reflect` Output Contract

`/tk:reflect`는 promotion router로서 세션 learning을 안전한 promotion surface로 분류합니다. 기본값은 preview-only입니다. 명시적 `--apply=true`가 있어도 write는 eligible `repo-local` candidate의 `<git-root>/CLAUDE.local.md`로 제한합니다.

### Canonical targets

Canonical target enum은 정확히 아래 8개입니다.

```text
repo-local, repo-shared, user-global, skill, hook, command, agent, discard
```

`PROFILE.md`, `automation`, `hookify`, `hook / hookify`는 target 이름이 아닙니다. Existing `PROFILE.md`와 legacy decline marker는 inactive legacy state로만 취급하고 자동 삭제하거나 자동 이관하지 않습니다.

### Legacy selector output

Legacy selector가 요청되면 receipt에 requested target, effective targets, deprecation line을 출력합니다.

```text
Requested target: repo
Effective targets: repo-local, repo-shared
Deprecation: Deprecated target selector: repo expands to repo-local, repo-shared.
```

```text
Requested target: user
Effective targets: user-global
Deprecation: Deprecated target selector: user expands to user-global.
```

`--target repo --apply=true`와 `--target all --apply=true`는 eligible `repo-local`만 apply set에 넣을 수 있습니다.

### Candidate contract

각 candidate는 최소한 아래 field를 출력합니다.

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

- `status: confirmed`는 routing evidence sufficiency이며 durable write approval이 아닙니다.
- `duplicate_status`는 관찰 가능한 evidence가 있을 때만 `confirmed`입니다. 관찰하지 못했으면 `unknown`입니다.
- `target: discard`는 `action: discard`, `path: NONE`, write 없음입니다.
- Branch-specific one-off 또는 workaround discard는 `reason_code: session_local`을 쓸 수 있습니다. `session-local` status은 쓰지 않습니다.
- TigerKit은 Claude Code auto memory를 쓰거나, mirror하거나, backup하지 않습니다.

### Apply plan contract

`--apply=true` write는 current invocation의 exact apply plan을 요구합니다.

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

- Reason code vocabulary는 `not_git_worktree`, `git_root_resolution_error`, `path_outside_repo`, `symlink_target`, `tracked_local_file`, `tracked_check_error`, `not_ignored`, `ignore_check_error`, `candidate_not_eligible`, `stale_apply_plan`, `apply_verification_failed`, `rollback_failed`, `no_eligible_candidates`입니다.
- `git -C <invocation_cwd> rev-parse --is-inside-work-tree`를 argument vector로 실행합니다. exit 0이 아니면 `not_git_worktree`입니다.
- `git -C <invocation_cwd> rev-parse --show-toplevel`을 argument vector로 실행합니다. 실패하면 `git_root_resolution_error`입니다.
- 이후 모든 Git 검사는 `git -C <git-root>`로 실행합니다.
- path operand는 root-relative literal `CLAUDE.local.md`입니다.
- normalized target path가 git root 밖이면 `path_outside_repo`입니다.
- `lstat` 결과 target path가 symlink이면 `symlink_target`입니다.
- `git -C <git-root> ls-files --error-unmatch -- CLAUDE.local.md`는 exit 0이면 `tracked_local_file`, exit 1이면 계속, 다른 status이면 `tracked_check_error`입니다.
- `git -C <git-root> check-ignore -q --no-index -- CLAUDE.local.md`는 exit 0이면 계속, exit 1이면 `not_ignored`, exit 128 또는 그 외 status이면 `ignore_check_error`입니다.
- `not_ignored`는 ignore entry를 제안할 수 있지만 `.gitignore`, `.git/info/exclude`, global exclude를 자동 수정하지 않습니다.
- apply plan은 current invocation에만 유효합니다. 이전 invocation plan은 `stale_apply_plan`입니다.
- planned result bytes, `planned_result_bytes_sha256`, exact unified diff가 있어야 합니다.
- generic edit/rewrite path와 broad rewrite는 금지합니다.
- 여러 후보는 one planned result bytes로 all-or-nothing 적용합니다.
- write 직전 base state/hash를 다시 확인하고 달라졌으면 `stale_apply_plan`으로 중단합니다.
- write는 같은 directory temporary file과 atomic replace를 사용합니다.
- post-write verification을 수행하고 실패하면 `apply_verification_failed`로 failed result bytes/hash를 capture합니다.
- verification 실패 후에는 어떤 candidate도 Applied로 보고하지 않습니다.
- rollback precheck로 external change를 확인합니다. 안전하면 원래 bytes 또는 original absence만 복구합니다.
- rollback succeeded이면 `Changed paths: NONE`입니다. rollback failed/external change이면 `reason_code: rollback_failed`와 changed path를 출력합니다.

### Reflect receipt shape

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

```text
Apply result: failed
reason_code: apply_verification_failed
rollback: succeeded
Changed paths: NONE
Applied candidates: NONE
```

```text
Apply result: failed
reason_code: rollback_failed
rollback: failed
Changed paths:
- <git-root>/CLAUDE.local.md
Applied candidates: NONE
Required action: inspect target manually before rerun
```


## `/tk:loop-spec` Output Contract

`/tk:loop-spec`은 명시적 task를 실행 없는 LoopSpec recommendation으로 컴파일하거나 기존 spec의 schema/context freshness를 검증합니다.

```text
Loop strategy: <motif or not-recommended>
Applicability: recommended | conditional | not-recommended
Readiness: complete | incomplete | manual
Fit score: <0..100>/100
Confidence: high | medium | low
Worktree: <branch or workspace>

Why
  - <reason and provenance>

Blockers
  - <blocker or NONE>

Guards
  - <guard>

Saved
  <~/.tigerkit/.../loop-specs/<spec-id>/spec.yaml or NONE>

Write receipt
  changed: <path or NONE>
  source tree changed: no
```

Validation output:

```text
LoopSpec: <id or path>
Schema: valid | invalid
Context: current | stale | unknown
```

`not-recommended`와 stale context는 정상 domain result입니다. Raw diff content와 secret content는 spec 또는 scanner artifact에 저장하지 않습니다.

## Deprecated output surfaces

아래 status/output surfaces는 새 TigerKit active flow에서 생성하지 않습니다.

- AFK receipt
- Patron decision ledger
- setup receipt
- grill question receipt
- launch workflow receipt
- handoff receipt
- active `SessionStart` hook receipt
- workflow hash
- sealed workflow
- `tigerkit-launch-workflow`
