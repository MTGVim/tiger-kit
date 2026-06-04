# TigerKit 운영 산출물 구조

이 문서는 TigerKit v7.2.11 산출물 배치와 책임을 설명합니다. 사용 흐름은 `.tigerkit/docs/usage.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

TigerKit은 branch-local working memory와 durable insight를 분리합니다.

## 기본 구조

```text
.claude/
  rules/
    **/*.md
  tigerkit/
    global-index.json
    branches/
      <branch-key>/
        specs/
          index.json
          SP-YYYYMMDD-HHmmss-RAND-<slug>.md
        runs/
          gap/
            GAP-YYYYMMDD-HHmmss-RAND/
              input-manifest.json
              contracts.json
              candidates.json
              judge-result.json
              baseline-snapshot.json
              report.md
        cache/
        branch-state.json
  handoffs/
    current.md
    YYYY-MM-DD-task-name.md

.tigerkit/
  docs/
    usage.md
    artifact-layout.md
    output-contract.md
    gap-baselines.json
```

## 파일 책임

| 파일 | 역할 | 저장 성격 |
| --- | --- | --- |
| `.claude/tigerkit/global-index.json` | branch-key 목록과 마지막 접근 정보. 저장 또는 apply를 수행한 `/tk:spec`, `/tk:gap`, `/tk:reflect` 실행 시 `lastUsedAt`을 갱신합니다. `--no-index`, `--no-save`, `--dry-run`, `--apply=false`처럼 저장하지 않는 실행은 recency를 갱신하지 않습니다. 손상되어도 branch-local index에서 복구 가능해야 합니다. | generated |
| `.claude/tigerkit/branches/<branch-key>/branch-state.json` | 현재 branch scope의 마지막 spec/gap run pointer. | branch-local |
| `.claude/tigerkit/branches/<branch-key>/specs/index.json` | 현재 branch scope의 Spec Patch index와 item supersede mapping. | branch-local |
| `.claude/tigerkit/branches/<branch-key>/specs/SP-*.md` | branch-local Spec Patch. PRD나 Design Guide의 영구 대체물이 아닙니다. | branch-local |
| `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/*.json` | gap input, contract, candidate, judge result artifact. 유저향 short Ref와 canonical ID mapping을 `displayRef` 또는 equivalent ref map으로 보존합니다. | branch-local |
| `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/baseline-snapshot.json` | 해당 run이 사용한 cumulative baseline, refreshed `origin/main` iteration baseline, current score, ratio, 다음 반복 승격 후보를 기록합니다. | branch-local |
| `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md` | 저장된 gap report 본문. | branch-local |
| `.claude/handoffs/current.md` | `/tk:handoff`가 생성하는 기본 continuation 문서. | continuation |
| `.claude/handoffs/YYYY-MM-DD-task-name.md` | `archive=true` 또는 명시적 archive 요청 때만 생성하는 continuation archive. | continuation |
| `.claude/rules/**/*.md` | repo convention basis이자 `/tk:reflect apply=true`의 scoped durable apply target입니다. | durable rule |
| `CLAUDE.md` | repo instruction과 durable project guidance이자 `/tk:reflect apply=true`의 global durable apply target입니다. | durable rule |
| `.tigerkit/docs/*.md` | TigerKit usage, artifact, output contract documentation. | docs |
| `.tigerkit/docs/gap-baselines.json` | `/tk:gap` 휴리스틱 proof의 누적 기준, 직전 main 반복 기준, 현재 contract target score registry. 다음 반복은 `origin/main`의 `currentTarget`을 `iterationBaseline`으로 자동 승격해 사용합니다. | docs |

Gap run은 단일 `/tk:gap` 실행에서도 아래 필수 run artifact 이름과 위치를 유지합니다.

```text
input-manifest.json
contracts.json
candidates.json
judge-result.json
baseline-snapshot.json
report.md
```

단일 `/tk:gap` 실행은 metadata와 execution order를 바꾸며, artifact location은 유지하고 기존 required file name에 `baseline-snapshot.json`을 추가합니다. `heuristicProof`, `heuristicProof.baselineProvenance`, `heuristicProof.baselineAutoRefreshGate`, `baselineAutoRefreshGate`, `performance`, `dispatchPlan`, `dispatchSkips`, `candidateIntakeGate`, `targetSurfaceCoverageGate`, `dispatchCompletenessGate`, `claimFreshnessGate`는 `input-manifest.json` 또는 `judge-result.json`에 기록합니다. `baseline-snapshot.json`은 same-run baseline score snapshot과 next iteration promotion candidate를 보관합니다.

## Branch key

Branch key 형식:

```text
<branch-slug>--<short-hash>
```

Normal branch는 `refs/heads/<branchName>`의 sha256 앞 6자리 hex를 사용합니다. Detached HEAD는 아래 형식을 사용합니다.

```text
detached-<shortHeadSha7>--<worktreeRootHash6>
```

## Worktree safety

동일 repository에서 여러 worktree를 사용하는 경우에도 TigerKit state는 반드시 current worktree root 아래에 저장합니다.

금지:

- `$GIT_COMMON_DIR/.claude/tigerkit`
- `.git/worktrees/*`
- user home global path
- `/tmp`

linked worktree는 repository common dir를 공유할 수 있으므로 common dir에 쓰면 산출물이 섞일 수 있습니다.

플러그인 hook은 사용자가 실제로 찾는 artifact path 또는 receipt 경계를 보호할 수 있을 때만 추가합니다. repo 유지보수용 sync/lint 목적이면 hook을 추가하지 않고 검증 절차나 문서 계약으로 둡니다.

## Git ignore

권장 `.gitignore`:

```gitignore
# Tiger Kit branch-local working memory
.claude/tigerkit/
```

주의:

- `.claude/` 전체를 ignore하지 않습니다.
- `.claude/tigerkit/`만 ignore합니다.
- reflect의 durable apply target은 `.claude/tigerkit/` 아래가 아니라 `CLAUDE.md` 또는 `.claude/rules/**/*.md`입니다.

## Atomic write 대상

아래 파일은 atomic write로 갱신합니다.

- `specs/index.json`
- `branch-state.json`
- `global-index.json`
- `judge-result.json`
- `candidates.json`
- `contracts.json`

절차:

1. `target.tmp.<pid>.<rand>` 파일에 씁니다.
2. 가능하면 fsync합니다.
3. rename으로 target을 교체합니다.
4. 실패 시 tmp 파일을 삭제합니다.

## Branch lock

동일 branch scope에서 `spec`, `gap`, `reflect`가 동시에 실행될 수 있으므로 lock을 사용합니다.

```text
.claude/tigerkit/branches/<branch-key>/.lock
```

30분 미만 lock은 active로 보고 중단합니다. 30분 이상 lock은 stale warning 후 제거할 수 있습니다. `TIGERKIT_FORCE_LOCK=1`이면 override할 수 있습니다.
