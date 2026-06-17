# TigerKit 운영 사용법

이 문서는 TigerKit v8.0 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, 출력 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash, contract field name은 원문 그대로 유지할 수 있습니다.

사용자 대화에 보이는 안내, 추천, 요약, next action은 계약용어와 변수명을 제외하고 한글로 씁니다.

## 핵심 모델

```text
TigerKit = branch-scoped spec + sealed gap workflow + human-approved launch + durable reflection + continuation handoff + generalized meta-feedback
```

TigerKit은 branch-local working memory와 durable repo insight를 분리합니다.

- 사용자 입력, 문서, 스크린샷, 회의 메모, 이전 계획은 source material이며 그 자체로 authority가 아닙니다.
- `spec`, `gap` 산출물은 현재 브랜치의 working memory입니다.
- 해당 산출물은 repo-wide durable knowledge가 아닙니다.
- repo에 영구적으로 남길 insight는 `reflect`만 추출하고 `CLAUDE.md` 또는 `.claude/rules/**/*.md`에 반영합니다.
- 다음 세션을 위한 사람이 읽는 continuation과 pending follow-up queue는 `handoff`가 담당합니다.
- TigerKit command/skill 자체 개선 피드백은 `meta-feedback`이 담당합니다.

## Command Surface

Plugin namespace는 `/tk:*`입니다. TigerKit v8.0 MVP의 공개 실행 표면은 Claude Code plugin command이며, 별도 repo-local skill 파일 없이 `commands/*.md`와 `.claude-plugin/plugin.json`이 `/tk:*` contract를 소유합니다. 해당 workflow를 명시한 자연어 요청은 대응하는 `/tk:*` command contract로 처리합니다.

Hermes Agent, Codex CLI, `npx skills` 기반 command-skill adapter는 v8 MVP에 포함하지 않습니다. Hermes에서 native `/gap`, `/launch`, `/reflect` command를 제공하려면 Hermes plugin(`.hermes/plugins/<name>/plugin.yaml`, `ctx.register_command`)이 필요하므로, 사전조사 후 별도 adapter 작업으로 다룹니다.

| Command | 역할 | 저장 성격 |
| --- | --- | --- |
| `/tk:spec` | 즉석 지시, 브레인스토밍, 회의 메모를 gap 분석용 Spec Patch로 저장합니다. | branch-local |
| `/tk:gap` | source grounding, ambiguity attack, sealed launch workflow 생성을 수행하고 `GAP_READY` 또는 `GAP_BLOCKED`로 끝납니다. | branch-local |
| `/tk:gap --review` | v7 Contract-based Gap Review compatibility mode로 사용자가 고칠 finding과 답할 clarification을 남깁니다. | branch-local |
| `/tk:launch` | sealed workflow만 실행하고 verification, abort receipt, reflect trace를 남깁니다. | branch-local execution |
| `/tk:reflect` | gap+launch trace와 branch-local 산출물에서 repo에 남길 insight만 추출하고 반영합니다. | durable insight |
| `/tk:handoff` | 다음 세션이나 다음 작업자가 이어받을 수 있도록 continuation 문서를 작성합니다. | continuation |
| `/tk:meta-feedback` | 현재 세션에서 드러난 TigerKit command/skill 개선안을 프로젝트 자산 유출 없이 일반화합니다. | generalized feedback |

## 사용 예시

```text
/tk:spec "방금 정해졌는데 모바일에서는 CTA를 하단 sticky로 해야 된대. 데스크톱은 기존처럼 우상단 유지."
/tk:gap
/tk:gap --review
/tk:gap --analysis-depth bounded
/tk:gap --analysis-depth expanded
/tk:gap --spec SP-20260602-143012-A7F3
/tk:gap --maintainer-proof
/tk:launch
/tk:launch --no-worktree
/tk:launch --autopilot
/tk:reflect
/tk:reflect --dry-run
/tk:reflect --no-meta-feedback
/tk:handoff 현재 작업 이어받을 수 있게 남겨줘
/tk:meta-feedback gap 결과가 느리고 BE 오탐이 난 패턴을 일반화해줘
```

## `/tk:spec`

- raw instruction을 branch-local Spec Patch로 저장합니다.
- source material과 authority를 분리합니다. confirmed 또는 명시 scope가 있는 항목만 gap evidence 후보가 됩니다.
- 기본 저장 위치는 `.claude/tigerkit/branches/<branch-key>/specs/`입니다.
- 기본 상태는 `active`입니다.
- confirmed item만 `/tk:gap` final finding evidence로 사용될 수 있습니다.
- ambiguous instruction은 confirmed로 세탁하지 않고 `draft`, `assumed`, `unclear`, `blocked`, 또는 clarification 대상으로 둡니다.
- `spec`은 구현 분석을 하지 않고 finding을 만들지 않습니다.
- 기본 stdout은 ID, branch scope, path, item list summary만 출력합니다.
- 전체 본문은 `--print-body`가 있을 때만 출력합니다.

## `/tk:gap`

- 기본 `/tk:gap`은 v8.0에서 Ground / Attack / Produce workflow command입니다.
- 사용자 의도, URL, ticket, notes, screenshots, repo context, prior specs, conversation decisions를 source material로 intake합니다.
- source material과 authority를 분리하고 confirmed requirement, assumption, rejected assumption, non-goal을 정규화합니다.
- ambiguity attack으로 contradiction, missing decision, hidden dependency, edge case, failure mode, verification gap을 찾습니다.
- launch 가능한 sealed workflow가 있으면 `GAP_READY`로 끝내고 `tigerkit-launch-workflow` block을 생성합니다.
- unresolved decision/conflict/missing source 때문에 launch하면 안 되면 `GAP_BLOCKED`로 끝내고 workflow block을 생성하지 않습니다.
- `/tk:gap --review`는 v7 Contract-based Gap Review compatibility mode입니다.
- `--analysis-depth <direct|bounded|expanded|exhaustive-capped>`는 source discovery depth만 명시하며 품질 gate를 낮추지 않습니다.
- `--maintainer-proof`는 maintainer/self-eval 전용입니다.

### `/tk:gap` 기본 출력 예시

```text
GAP_READY: WF-20260617-143012-A7F3
Branch Scope: main--c0ffee
Workflow: .claude/tigerkit/branches/main--c0ffee/gap/WF-20260617-143012-A7F3.md
Workflow Hash: <sha256>
Tasks: 4
Verification Gates: 4
Autopilot Allowed: false
Commit Policy: preflight_decision_required
다음 행동: /tk:launch
```

```text
GAP_BLOCKED: GAP-20260617-143012-A7F3
Branch Scope: main--c0ffee
Blocked Reasons: 2
Human Decisions: 1
Missing Sources: 1
Report: .claude/tigerkit/branches/main--c0ffee/gap/GAP-20260617-143012-A7F3.md
다음 행동: Q1 확인 후 /tk:gap 재실행
```

### `/tk:gap --review`

`/tk:gap --review`는 기존 v7 review behavior를 유지합니다.

- Product/Design Spec, implementation plan, current implementation을 Contract로 normalize해 비교합니다.
- 기본 산출물은 `report.md`와 `run.json`입니다.
- 기본 stdout은 run 결과, finding/clarification count, report path, run.json path, next action만 출력합니다.
- subagent는 candidate만 생성하고 JudgeMergerAgent만 final finding을 확정합니다.
- final finding은 P0/P1/P2만 포함합니다.
- P3/nit/duplicate/unverifiable/source_conflict는 final finding이 아닙니다.
- `/tk:gap --review` run artifact는 `.claude/tigerkit/branches/<branch-key>/runs/gap/<GAP-ID>/` 아래에 저장합니다. 기본 `/tk:gap` sealed workflow는 `.claude/tigerkit/branches/<branch-key>/gap/` 아래에 저장합니다.
- 유저향 compact table은 run-local short Ref(`G1`, `R1`, `C1`, `Q1`)를 우선 표시합니다.

### `/tk:launch`

- `/tk:launch`는 sealed workflow만 실행합니다.
- workflow 밖 scope 확장, missing requirement 임의 해석, public API/DB/product behavior 재정의, verification 없는 success 선언, out-of-scope diff commit을 금지합니다.
- mid-flight 질문을 하지 않습니다. 새 사용자 결정이 필요하면 `HUMAN_DECISION_REQUIRED`로 abort합니다.
- `/tk:launch --autopilot`은 Phase 1에서 recovery를 수행하지 않고 `AUTOPILOT_DISABLED` 또는 `AUTOPILOT_NOT_IMPLEMENTED_IN_PHASE1`로 abort합니다.
- commit은 preflight receipt에 `user_preapproved_commit=true`와 `approval_source_ref`가 있을 때만 가능합니다.

### Maintainer only: `--maintainer-proof`

`--maintainer-proof`는 TigerKit maintainer가 자체 성능개선, regression 검증, proof artifact 확인을 할 때만 씁니다. 일반 사용자가 gap 결과를 더 좋게 만들기 위해 선택하는 품질 모드가 아닙니다.

이 옵션을 명시한 경우에만 아래가 허용됩니다.

- `maintainer-proof/` artifact 생성
- `input-manifest.json`, `contracts.json`, `candidates.json`, `judge-result.json`, `baseline-snapshot.json`, `proof.json`
- `heuristicProof`, `performance`, baseline/current score
- false-positive/false-negative/speed/analysis-depth improvement claim
- target coverage proof와 dispatch completeness proof
- ClaimFreshnessGate와 BaselineAutoRefreshGate

기본 `/tk:gap`은 성능개선이나 false-positive/false-negative 개선 claim을 하지 않습니다. 사용자에게 중요한 정보는 Actionable Findings, Clarification Needed, next action입니다.

## `/tk:reflect`

- branch-local specs/gap memory에서 durable insight 후보만 추출합니다.
- 기본 동작은 `apply=true`입니다.
- 반영할 durable insight가 없으면 아무 파일도 수정하지 않고 성공할 수 있습니다.
- `--dry-run`과 `--apply=false`는 preview-only입니다.
- 기본 apply target은 `CLAUDE.md` 또는 `.claude/rules/**/*.md`입니다.
- `.claude/tigerkit/` 아래에는 durable insight를 저장하지 않습니다.
- source code는 수정하지 않습니다.
- 후보는 Frequency, Cost, Risk, Stability, Coverage를 모두 통과해야 합니다.
- 기존 `CLAUDE.md`와 `.claude/rules/**/*.md`를 먼저 inventory해 중복 durable guidance를 피합니다.
- 근거가 부족한 후보는 `Needs more evidence`로 남기고 durable rule로 승격하지 않습니다.
- branch-specific one-off decision, 임시 Spec Patch, superseded 결정, P3/nit, rejected finding, low-confidence observation은 durable insight로 만들지 않습니다.
- branch-local specs/gap 산출물이 없으면 산출물 기반 후보는 없는 것으로 처리합니다. 사용자 대화에서 명시적으로 확인된 TigerKit 운영 규칙은 후보가 될 수 있지만, 반복 관측 패턴이나 실행자 해석만으로 durable insight를 만들지 않습니다.
- apply가 저장을 수행하면 `global-index.json`에 current branch entry가 없을 때 새 entry를 만들 수 있습니다.
- reflect 처리 직후 `/tk:meta-feedback`을 proposal-only로 함께 제출합니다.
- `--no-meta-feedback` 또는 `--meta-feedback=false`가 있으면 meta-feedback 제출을 생략합니다.

## `/tk:handoff`

- 기존 continuation command입니다. v8.0에서도 active compatibility command로 유지합니다.
- canonical 출력 대상은 `.claude/tigerkit/branches/<branch-key>/handoffs/current.md`입니다.
- `/tk:handoff`는 `.claude/tigerkit/global-index.json`의 current branch entry에 `latestHandoffPath`를 함께 기록합니다.
- 경로를 지정하지 않은 resume 지시는 `global-index.json`의 `latestHandoffPath`를 1순위로 확인합니다.
- 최신 branch-local Spec Patch와 Gap Run이 있으면 handoff의 relevant files나 validation에 참조할 수 있습니다.
- 현재 작업을 방해하면 안 되는 follow-up은 `Pending Backlog`에 source/evidence/priority/blocked-by/next action과 함께 남길 수 있습니다.
- `archive=true` 또는 명시적 archive 요청이 있을 때만 branch-local dated copy를 만듭니다.
- `.claude/handoffs/current.md`는 optional convenience pointer이며 canonical handoff를 대체하지 않습니다.
- `Reader Guide`와 `Resume Prompt`를 포함합니다.

## `/tk:meta-feedback`

- 기존 TigerKit improvement command입니다. v8.0에서도 active compatibility command로 유지합니다.
- 현재 세션 내역에서 TigerKit command/skill 사용 friction과 반복 피드백을 찾습니다.
- gap 속도, BE 오탐, mode 추천 UX, output shape 같은 개선안을 일반화합니다.
- repo 이름, product 이름, 내부 path, URL, ticket, branch, PR 번호, commit hash, 사용자 원문 quote는 출력하지 않습니다.
- repo rule patch는 `/tk:reflect`, basis-target 비교는 `/tk:gap`, follow-up 보관은 `/tk:handoff` 대상으로 분리합니다.
- agent runtime/config, MCP permission, custom agent 추천은 TigerKit 본체 범위 밖으로 둡니다.

## Generated state

`.claude/tigerkit/`은 generated branch-local working memory입니다. git ignore 대상입니다.

주의:

- `.claude/` 전체를 ignore하지 않습니다.
- `.claude/tigerkit/`만 ignore합니다.
- current worktree root 아래에 저장합니다.
- `$GIT_COMMON_DIR`, `.git/worktrees/*`, user home, `/tmp`에 저장하지 않습니다.

## 운영 범위 메모

세부 정책, 우선순위 규칙, 검증 원칙은 `CLAUDE.md`와 `.claude/rules/**/*.md`를 기준으로 봅니다.
