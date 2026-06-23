# Reflect promotion helper guide

이 문서는 `/tk:reflect` promotion router 결과를 검토할 때 참고할 수 있는 선택형 helper guide다.

## Status

- Optional helper document
- Non-authoritative for runtime behavior
- Not a command, hook, agent, generator, installer, or generated artifact layout
- Not a replacement for `commands/reflect.md`, `.tigerkit/docs/output-contract.md`, `docs/reflect-file-policy.md`, or `.tigerkit/docs/storage-boundary.md`

이 문서의 예시는 후보를 더 잘 읽고 검토하기 위한 설명이다. 예시가 있다고 해서 hook 설치, settings 수정, command 생성, agent 생성, user skill 생성, plugin manifest 수정, runtime generation, Claude Code auto memory write가 발생하지 않는다.

## When this guide helps

이 문서는 다음 상황에서만 참고한다.

- `/tk:reflect` receipt에 `hook`, `command`, `agent` proposal이 나왔고 사용자가 후속 검토를 원할 때
- promotion 후보가 repo-local, repo-shared, user-global, skill, hook, command, agent, discard 중 어디에 가까운지 다시 판단할 때
- TigerKit generated state와 실제 durable target의 역할을 구분해야 할 때
- 제안 문구가 설치됨/활성화됨/자동 적용됨처럼 과장됐는지 점검할 때

## Canonical promotion target quick guide

| Target | Good fit | Boundary |
|---|---|---|
| `repo-local` | 이 repo에만 필요한 local/private guidance | eligible `--apply=true`일 때 `<git-root>/CLAUDE.local.md`만 write 가능 |
| `repo-shared` | 팀이 공유할 repo-wide rule 후보 | suggest-only, 직접 수정 금지 |
| `user-global` | 여러 repo에 적용되는 user-global instruction 또는 rule 후보 | suggest-only, TigerKit이 user memory를 쓰지 않음 |
| `skill` | 반복 가능한 multi-step routine 후보 | suggest-only, TigerKit generated state에 source 생성/복제 금지 |
| `hook` | lifecycle event 기반 warning/check/block 후보 | suggest-only, settings 수정 금지 |
| `command` | 사용자가 명시적으로 호출할 slash workflow 후보 | command 파일 또는 manifest 생성 금지 |
| `agent` | 독립 역할, 병렬 조사, 전문 판단이 필요한 후보 | 자동 dispatch 또는 orchestration runtime 생성 금지 |
| `discard` | branch-specific one-off, 저신뢰, 민감 정보, 중복 | durable surface에 저장하지 않음 |

금지 target 이름:

- `PROFILE.md`
- `automation`
- `hookify`
- `hook / hookify`

## Optional hook guidance

`hook` proposal은 자동 적용 대상이 아니다. 후보는 아래 조건을 모두 만족할 때만 제안으로 남긴다.

1. 반복되는 실수나 누락이 있다.
2. trigger를 tool event, path, command, prompt pattern 같은 표면에서 설명할 수 있다.
3. action이 warning, reminder, check, block 중 무엇인지 분명하다.
4. false positive risk와 사용자 검토 필요성이 적혀 있다.
5. destructive action, credential handling, external side effect를 자동화하지 않는다.

권장 receipt shape:

```text
## Hook 후보
1. <candidate title>
- rationale: <어떤 반복 문제를 줄이는지>
- trigger: <언제 실행되는지>
- action: <무엇을 경고/검사/차단/기록하는지>
- why suggest-only: <왜 설치/활성화 전 사용자 검토가 필요한지>
```

금지 표현:

- hook installed
- hook active
- settings updated
- 자동 적용됨
- 다음부터 반드시 실행됨

허용 표현:

- hook proposal
- suggest-only
- optional follow-up
- user review required before install

## Candidate metadata review

각 candidate는 아래 field를 가져야 한다.

```yaml
candidate_id: R1
status: candidate | confirmed | deprecated
duplicate_status: confirmed | unknown
action: preview_only | apply | suggest_only | discard
target: repo-local | repo-shared | user-global | skill | hook | command | agent | discard
```

`status: confirmed`는 routing evidence sufficiency다. Durable write approval이 아니다. Auto memory나 기존 durable target을 직접 관찰하지 못하면 `duplicate_status: unknown`으로 남긴다. Branch-specific one-off 또는 workaround discard는 `reason_code: session_local`을 쓸 수 있지만 `session-local` status은 쓰지 않는다.

## Promotion receipt and TigerKit generated state

Active TigerKit generated state는 `~/.tigerkit/` 아래에 있다. `.claude/tigerkit/`와 SessionStart decline marker는 legacy/migration context로만 남는다. Execute boundary packaging은 preview/runtime validation 표면으로 존재할 수 있고 execute availability는 support matrix environment gate가 소유한다. 현재 helper guide는 reflect artifact write path를 선언하지 않는다.

Receipt가 기록할 수 있는 것:

- source session summary
- promotion candidate list
- target classification
- preview-only / apply / suggest-only / discard result
- changed paths when files were written
- apply plan and rollback result when relevant
- durable target path 또는 follow-up proposal pointer

Receipt가 canonical source가 되면 안 되는 것:

- repo shared policy 본문
- user-global guidance 본문
- skill canonical source 복제본
- installed hook config
- generated command or agent source
- source code or product artifact
- Claude Code auto memory mirror/backup

즉 receipt는 “무엇이 어디로 가야 하는지”를 보여준다. “그 표면 자체”를 소유하지 않는다.

## Apply safety quick check

Repo-local apply receipt를 검토할 때는 아래 표면을 확인한다.

- `git -C <invocation_cwd> rev-parse --is-inside-work-tree`
- `git -C <invocation_cwd> rev-parse --show-toplevel`
- `git -C <git-root> ls-files --error-unmatch -- CLAUDE.local.md`
- `git -C <git-root> check-ignore -q --no-index -- CLAUDE.local.md`
- `lstat` symlink check
- normalized path inside git root
- argument vector, no shell string concatenation
- same-directory temp file and atomic replace
- failed result bytes/hash capture
- rollback precheck before restore
- restore original bytes or original absence only when safe
- rollback success means `Changed paths: NONE` and `Applied candidates: NONE`

## Review checklist

Reflect promotion 결과를 볼 때는 아래를 확인한다.

1. 후보가 정확히 하나의 canonical target으로 분류됐는가?
2. default가 preview-only인가?
3. `--apply=true` write set이 eligible `repo-local` 후보로만 제한됐는가?
4. shared repo rule, user-global, skill, hook, command, agent 후보가 suggest-only로 남았는가?
5. `PROFILE.md`, `automation`, `hookify`를 target으로 쓰지 않았는가?
6. user skill 후보가 TigerKit generated state source처럼 표현되지 않았는가?
7. hook, command, agent 후보가 설치됨/활성화됨으로 표현되지 않았는가?
8. 파일을 쓴 경우 changed path와 apply plan이 출력됐는가?
9. TigerKit generated state receipt가 canonical durable target처럼 설명되지 않았는가?
10. branch-specific one-off, 저신뢰, 민감 정보, 중복 후보가 discard됐는가?
11. auto memory duplicate evidence를 관찰하지 못한 후보가 `duplicate_status: unknown`으로 남았는가?
12. apply reject/failure가 `not_git_worktree`, `git_root_resolution_error`, `path_outside_repo`, `symlink_target`, `tracked_local_file`, `tracked_check_error`, `not_ignored`, `ignore_check_error`, `candidate_not_eligible`, `stale_apply_plan`, `apply_verification_failed`, `rollback_failed`, `no_eligible_candidates` 중 하나의 `reason_code`를 쓰는가?
13. `not_ignored`가 ignore entry 제안만 하고 `.gitignore`, `.git/info/exclude`, global exclude를 자동 수정하지 않았는가?
14. rollback success가 `Changed paths: NONE`과 `Applied candidates: NONE`을 출력하는가?
15. rollback failure 또는 external change가 `reason_code: rollback_failed`와 changed path를 출력하는가?

## Bottom line

이 문서는 `/tk:reflect` 결과를 읽는 보조 설명서다. TigerKit runtime behavior는 command contract와 output/file policy가 정하고, optional helper docs는 그 contract를 실행하거나 확장하지 않는다.
