# TigerKit 운영 산출물 구조

이 문서는 TigerKit v8.0 산출물 배치와 책임을 설명합니다. 사용 흐름은 `.tigerkit/docs/usage.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

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
        gap/
          WF-YYYYMMDD-HHmmss-RAND.md
          current.md
          GAP-YYYYMMDD-HHmmss-RAND.md
        launch/
          LCH-YYYYMMDD-HHmmss-RAND.md
          current.md
        reflect/
          RFL-YYYYMMDD-HHmmss-RAND.md
          current.md
        runs/
          gap/
            GAP-YYYYMMDD-HHmmss-RAND/
              report.md
              run.json
              maintainer-proof/        # only with --maintainer-proof or --review --maintainer-proof
                input-manifest.json
                contracts.json
                candidates.json
                judge-result.json
                baseline-snapshot.json
                proof.json
        handoffs/
          current.md
          YYYY-MM-DD-task-name.md
        cache/
        branch-state.json
  handoffs/
    current.md  # optional pointer to branch-local handoff

.tigerkit/
  docs/
    usage.md
    artifact-layout.md
    output-contract.md
    gap-baselines.json
```

## Workspace fallback storage

Git이 없는 plain workspace도 같은 generated state root를 사용합니다. 이때 `<branch-key>` 자리에 workspace fallback `scope_key`를 사용합니다.

```text
.claude/tigerkit/branches/workspace-<basename-slug>--<hash>/
```

MVP에서는 path compatibility를 위해 `branches/` 아래에 저장하지만 receipt에는 `Scope Kind: workspace`를 반드시 표시합니다.

## 파일 책임

| 파일 | 역할 | 저장 성격 |
| --- | --- | --- |
| `.claude/tigerkit/global-index.json` | branch-key 목록, 마지막 접근 정보, current branch 최신 handoff pointer. 저장 또는 apply를 수행한 `/tk:gap`, `/tk:reflect` 실행 시 `lastUsedAt`을 갱신합니다. `/tk:handoff` 실행 시 branch entry의 `latestHandoffPath`와 `lastHandoffAt`을 갱신합니다. entry가 없으면 현재 branch 정보로 생성할 수 있습니다. `--no-save`, `--dry-run`, `--apply=false`처럼 저장하지 않는 실행은 recency를 갱신하지 않습니다. 손상되어도 branch-local index에서 복구 가능해야 합니다. | generated |
| `.claude/tigerkit/branches/<branch-key>/branch-state.json` | 현재 branch scope의 최신 gap workflow/review, launch, reflect, handoff pointer. | branch-local |
| `.claude/tigerkit/branches/<branch-key>/specs/index.json` | legacy Spec Patch index와 item supersede mapping. v8 MVP command가 새로 생성하지 않으며 `/tk:gap` source material discovery에만 사용할 수 있습니다. | legacy branch-local |
| `.claude/tigerkit/branches/<branch-key>/specs/SP-*.md` | legacy branch-local Spec Patch. PRD나 Design Guide의 영구 대체물이 아니며 `/tk:gap` source material 후보입니다. | legacy branch-local |
| `.claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md` | `/tk:gap`이 `GAP_READY`일 때 만드는 sealed launch workflow archive입니다. | branch-local |
| `.claude/tigerkit/branches/<branch-key>/gap/current.md` | 최신 sealed launch workflow copy입니다. hash seal의 authoritative source는 archive workflow 파일입니다. | branch-local pointer |
| `.claude/tigerkit/branches/<branch-key>/gap/<GAP-ID>.md` | `/tk:gap`이 `GAP_BLOCKED`일 때 만드는 blocked report입니다. workflow block을 포함하지 않습니다. | branch-local |
| `.claude/tigerkit/branches/<branch-key>/launch/<LCH-ID>.md` | `/tk:launch` 실행 또는 abort report입니다. | branch-local execution |
| `.claude/tigerkit/branches/<branch-key>/launch/current.md` | launch status, task/gate 결과, abort code, commit decision을 보존하는 최소 run record입니다. | branch-local execution |
| `.claude/tigerkit/branches/<branch-key>/reflect/<RFL-ID>.md` | `/tk:reflect` generated report archive입니다. `tigerkit-reflect-report` block을 포함합니다. durable apply가 아닙니다. | branch-local generated |
| `.claude/tigerkit/branches/<branch-key>/reflect/current.md` | 최신 reflect report copy입니다. | branch-local pointer |
| `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/report.md` | `/tk:gap --review` 사용자가 읽는 compatibility gap report 본문입니다. Actionable Findings, Clarification Needed, next action 중심입니다. | branch-local |
| `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/run.json` | `/tk:gap --review` 후속 대화와 기계 처리를 위한 최소 run record입니다. user-facing short Ref와 canonical ID mapping을 보존합니다. | branch-local |
| `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/maintainer-proof/` | `--maintainer-proof`가 명시된 경우에만 생성하는 self-eval/performance proof, gate/debug metadata, baseline snapshot 영역입니다. | branch-local maintainer-only |
| `.claude/tigerkit/branches/<branch-key>/handoffs/current.md` | `/tk:handoff`가 생성하는 canonical continuation 문서. 최신 경로는 `global-index.json`과 `branch-state.json`에 pointer로 기록합니다. 현재 작업을 방해하면 안 되는 follow-up은 `Pending Backlog` 섹션에 source/evidence/priority/blocked-by/next action과 함께 보관할 수 있습니다. | branch-local continuation |
| `.claude/tigerkit/branches/<branch-key>/handoffs/YYYY-MM-DD-task-name.md` | `archive=true` 또는 명시적 archive 요청 때만 생성하는 branch-local continuation archive. | branch-local continuation |
| `.claude/handoffs/current.md` | optional convenience pointer. canonical handoff를 대체하지 않습니다. | pointer |
| `.claude/rules/**/*.md` | repo convention basis이자 `/tk:reflect apply=true`의 scoped durable apply target입니다. | durable rule |
| `CLAUDE.md` | repo instruction과 durable project guidance이자 `/tk:reflect apply=true`의 global durable apply target입니다. | durable rule |
| `.tigerkit/docs/*.md` | TigerKit usage, artifact, output contract documentation. | docs |
| `.tigerkit/docs/gap-baselines.json` | `--maintainer-proof`에서만 쓰는 `/tk:gap` proof baseline registry. 기본 사용자 경로의 산출물이나 사용자-facing report 요구사항이 아닙니다. | docs |

## 기본 `/tk:gap` artifact

기본 `/tk:gap`은 v8 sealed workflow builder입니다. launch 가능 여부에 따라 아래 중 하나를 씁니다.

```text
.claude/tigerkit/branches/<branch-key>/gap/<WF-ID>.md       # GAP_READY archive
.claude/tigerkit/branches/<branch-key>/gap/current.md       # latest GAP_READY copy
.claude/tigerkit/branches/<branch-key>/gap/<GAP-ID>.md      # GAP_BLOCKED report
```

`GAP_READY` archive는 사람용 report와 정확히 하나의 `tigerkit-gap-status` block, 정확히 하나의 `tigerkit-launch-workflow` block을 포함합니다. `GAP_BLOCKED` report는 `tigerkit-gap-status` block만 포함하고 `tigerkit-launch-workflow` block을 포함하지 않습니다.

`/tk:gap --review` compatibility mode만 v7 review layout을 씁니다.

```text
.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/
  report.md
  run.json
```

`--maintainer-proof`가 있을 때만 `runs/gap/<GAP-ID>/maintainer-proof/` 아래 proof/debug artifact를 추가할 수 있습니다.

기본 gap workflow/report는 아래 self-eval/proof/debug metadata를 요구하지 않습니다.

```text
input-manifest.json
contracts.json
candidates.json
judge-result.json
baseline-snapshot.json
proof.json
```

기본 gap workflow/report와 `/tk:gap --review` compatibility run은 아래 self-eval/proof/debug metadata를 요구하지 않습니다.

- `qualityGates`
- `heuristicProof`
- `performance`
- `baselinePredicateScore`
- `currentPredicateScore`
- `analysisDepth` proof
- `riskScore`
- `sideEffectConfidence`
- `verificationEscalation`
- `dispatchPlan` dump
- `dispatchSkips` dump
- `targetSurfaceCoverageGate` proof
- `dispatchCompletenessGate` proof
- `claimFreshnessGate`
- artifact inventory dump

확인하지 못한 target/producer/plan surface가 사용자 결정을 막으면 proof dump가 아니라 `Clarification Needed` 또는 `Not Accepted Summary`로 표현합니다.

## `/tk:next` artifact policy

`/tk:next`는 steering replacement continuation run마다 generated receipt를 남깁니다. 기본 위치는 아래와 같습니다.

```text
.claude/tigerkit/branches/<branch-key>/next/
  NXT-YYYYMMDD-HHmmss-RAND.md
  current.md
```

Plain workspace fallback도 `branches/<scope-key>/next/` layout을 사용하고 receipt에 `Scope Kind: workspace`를 표시합니다. next receipt는 branch/workspace-local generated working memory이며 durable repo rule이나 source of truth가 아닙니다.

## Maintainer-only artifacts

`--maintainer-proof`가 명시된 gap run만 기본 artifact에 더해 maintainer-only proof artifact를 생성할 수 있습니다.

```text
.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/
  report.md
  run.json
  maintainer-proof/
    input-manifest.json
    contracts.json
    candidates.json
    judge-result.json
    baseline-snapshot.json
    proof.json
```

`maintainer-proof/` 아래 파일은 일반 사용자 output surface가 아닙니다. TigerKit 자체 성능개선, regression 검증, self-eval proof, baseline refresh, detailed gate/debug 확인에만 씁니다. 기본 stdout과 기본 `report.md`에는 maintainer proof artifact 목록, gate dump, proof ratio, baseline snapshot 내용을 노출하지 않습니다.

Maintainer proof artifact에만 아래를 기록할 수 있습니다.

- `qualityGates`
- `analysisDepth`, `depthReasons`, `riskScore`, `sideEffectConfidence`
- `verificationEscalation`, `compatibilityFlags`
- `dispatchPlan`, `dispatchSkips`
- `candidateIntakeGate`, `evidencePrecisionGate`
- `targetSurfaceCoverageGate`, `dispatchCompletenessGate`
- `baselineAutoRefreshGate`, `claimFreshnessGate`
- `performance`
- `heuristicProof`
- cumulative/iteration baseline
- false-positive/false-negative/speed/analysis-depth improvement claim proof

`run.json`에는 `maintainerProofEnabled: true`와 `maintainerProofPath`만 추가하면 충분합니다. 기본 사용자 receipt에는 maintainer proof artifact list를 출력하지 않습니다.

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

- `branch-state.json`
- `global-index.json`
- `run.json`
- `maintainer-proof/judge-result.json`
- `maintainer-proof/candidates.json`
- `maintainer-proof/contracts.json`
- `maintainer-proof/proof.json`

절차:

1. `target.tmp.<pid>.<rand>` 파일에 씁니다.
2. 가능하면 fsync합니다.
3. rename으로 target을 교체합니다.
4. 실패 시 tmp 파일을 삭제합니다.

## Branch lock

동일 branch scope에서 `gap`, `launch`, `reflect`, `handoff`가 동시에 같은 branch-local state를 갱신할 수 있으므로 lock을 사용합니다.

```text
.claude/tigerkit/branches/<branch-key>/.lock
```

30분 미만 lock은 active로 보고 중단합니다. 30분 이상 lock은 stale warning 후 제거할 수 있습니다. `TIGERKIT_FORCE_LOCK=1`이면 override할 수 있습니다.
