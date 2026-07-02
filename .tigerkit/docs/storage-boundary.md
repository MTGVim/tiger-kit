# TigerKit storage boundary

이 문서는 TigerKit generated state의 active external layout과 legacy repo-inside layout의 경계를 구분한다.

## Core rule

```text
active generated state = ~/.tigerkit/ file-only state outside the project repository
legacy repo-inside state = .claude/tigerkit/ migration context only
legacy packaging metadata owner = support/execute-support-matrix.json
```

TigerKit generated state는 durable repo guidance, shared team rule, user-global guidance, user skill source, command source, agent source의 canonical home이 아니다. legacy execute boundary packaging metadata는 plugin package 안의 declared component가 소유할 수 있지만, 현재 active public command surface를 정의하지는 않는다.

## Active external state

Active generated state는 project repository 밖 `~/.tigerkit/` 아래에 둔다. `TIGERKIT_STATE_ROOT`가 있으면 그 값을 state root로 사용할 수 있지만, 기본 contract는 `~/.tigerkit/`이다.

```text
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/<GAP-ID>.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/gap/current.md
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/REFLECT-YYYYMMDD-HHmmss-RAND.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/reflect/current.yaml
~/.tigerkit/repos/<repo-key>/branches/<scope-key>/branch-state.json
```

역할:

- `/tk:gap` one-shot report archive
- latest gap report pointer
- `/tk:reflect` machine-readable ledger archive/current pointer
- branch/workspace-local generated index

`repo-key`와 `scope-key` 계산은 `scripts/tigerkit_state.py` helper만 수행한다. Command prompt나 agent가 path-key 알고리즘을 재구현하지 않는다.

## Legacy packaged compatibility metadata

현재 repo는 active public command surface를 `gap/route/reflect/ui-diff/grill/prototype/arch-review/merge-conflict/handoff/to-prd/to-issues`로 둔다. 그와 별도로 execute write-boundary 관련 패키징 메타데이터는 compatibility/preview validation 맥락으로 남을 수 있다.

Capability proof canonical root example:

```text
~/.tigerkit/capabilities/execute-write-boundary/<plugin-version>/<environment-key>/proof.yaml
```

Rules:

- proof schema is `tigerkit.capability-proof/execute-write-boundary-v1`.
- support matrix schema is `tigerkit.execute-support-matrix/v1`.
- `support/execute-support-matrix.json` owns public, preview, unsupported environment set.
- support matrix `boundaryComponents[]` is the canonical ordered package path set.
- proof `componentDigests[]` must exact-match support matrix component path set plus fixed proof owner path set.
- proof `tests[]` must be exactly `CAP-01` through `CAP-10` in order and all `passed`.
- proof `runtimeBinding` must byte-match current helper capture.
- proof `supportMatrixDigest` must match current package support matrix bytes.

## Legacy boundary runtime packaging

Current selected architecture is `hook_gate` preview. Packaged components:

```text
hooks/hooks.json
hooks/execute-write-boundary.py
```

`hooks/execute-write-boundary.py` is inert unless `TIGERKIT_EXECUTE_BOUNDARY_FILE` is present. 이 파일군은 legacy/preview validation metadata 맥락에서만 남을 수 있으며, 현재 active public command surface를 정의하지 않는다.

Hook files are mandatory only for hook architecture. Other architecture components must be declared by support matrix if selected later.

## Legacy SessionStart state

기존 decline marker는 inactive legacy state로만 보존하며 core command/runtime이 읽거나 쓰지 않는다.

```text
~/.tigerkit/local/session-start/worktree-context-declines.json
.claude/tigerkit/local/session-start/worktree-context-declines.json
```

처리 원칙:

- 자동 삭제하지 않는다.
- 자동 이관하지 않는다.
- 새 core command contract의 active generated layout으로 취급하지 않는다.
- 새 core command/runtime은 해당 marker를 읽거나 쓰지 않는다.

## Legacy repo-inside state

`.claude/tigerkit/`는 legacy/migration context다. 새 write path가 아니다.

기존 파일이 있으면 migration context로 언급할 수 있지만, active source of truth로 취급하지 않는다. 새 generated state, gap report, reflect ledger, branch pointer는 `~/.tigerkit/`에 쓴다.

## Not stored here

TigerKit generated state에는 아래를 canonical source로 저장하지 않는다.

- repo `CLAUDE.md`
- repo `CLAUDE.local.md`
- repo shared docs 본문
- user `CLAUDE.md`
- user `PROFILE.md`
- user skill source
- command source
- agent source
- source code
- product artifact
- Claude Code auto memory backup/mirror

## Promotion boundary

`/tk:reflect`는 learning을 분류할 수 있지만, TigerKit generated state가 promotion target 자체를 소유하지 않는다.

| Target | Canonical owner or action |
|---|---|
| `repo-local` | repo `<git-root>/CLAUDE.local.md` |
| `repo-shared` | suggest-only proposal |
| `user-global` | supported host의 user-global guidance surface (`~/.claude/CLAUDE.md`, `~/.claude/rules/<rule-name>/CLAUDE.md`, 또는 host-native equivalent) |
| `skill` | explicit-apply proposal to user skill surface |
| `hook` | suggest-only proposal |
| `command` | suggest-only proposal |
| `agent` | suggest-only proposal |
| `discard` | no storage |

## Git policy

Active `~/.tigerkit/` state는 project repository 밖에 있으므로 repo `.gitignore` 대상이 아니다.

Legacy `.claude/tigerkit/` repo-inside state는 migration context로 남을 수 있으므로 계속 git ignore 대상이다.

```gitignore
.claude/tigerkit/
```

`.claude/` 전체를 ignore 대상으로 확대하지 않는다.

## Review checklist

1. active write path가 project repository 밖 `~/.tigerkit/`인가?
2. repo identity와 branch/workspace scope가 충돌 없이 분리되는가?
3. `.claude/tigerkit/`는 legacy/migration context로만 쓰는가?
4. reflect ledger가 `reflect/REFLECT-...`와 `reflect/current.yaml`에 기록되는가?
5. support matrix가 legacy packaging metadata의 owner로만 남는가?
6. capability proof는 compatibility metadata로만 설명되고 active command surface로 오인되지 않는가?
7. user-global guidance, shared repo rule, skill source, Claude Code auto memory를 복제하지 않는가?

## Bottom line

TigerKit active generated state는 `~/.tigerkit/` 아래의 file-only external state다. 현재 active generated layout은 gap report와 reflect ledger 중심이다. execute write-boundary proof 같은 파일은 compatibility/preview validation metadata로 남을 수 있지만 active public command surface를 뜻하지 않는다.
