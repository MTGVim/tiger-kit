# TigerKit 운영 사용법

이 문서는 `.tigerkit/docs/` 아래 TigerKit 운영 문서 중 사용 가이드입니다. 산출물 위치는 `.tigerkit/docs/artifact-layout.md`, receipt 규칙은 `.tigerkit/docs/output-contract.md`를 기준으로 봅니다.

## 언어

명령은 사용자에게 한글로 답하고 작업 산출물도 한글로 작성합니다. URL, 코드, 명령어, 경로, 식별자, commit hash는 원문 그대로 유지할 수 있습니다.

## 핵심 모델

```text
TigerKit = source-of-truth index + reproducible gap record + decision gate + compliance review + session reflection + operational handoff
```

TigerKit은 LLM의 장기 절차 기억에 실행 순서나 진행 상태를 맡기지 않습니다.

기본 흐름:

```text
/tk:prep
/tk:gap
/tk:handoff-write
```

조건부 명령:

- `/tk:checkpoint`: high-impact ambiguity, inaccessible SOT, SOT conflict, user decision, external dependency, broad refactor risk가 있을 때 Decision Gate로 사용합니다.
- `/tk:review`: TigerKit command/docs/evals/artifact/implementation 변경에서 source-loss, reuse exploration, baseline, Decision Gate, handoff/reflect contract 위반을 검토할 때 사용합니다.
- `/tk:reflect`: project policy나 repeated user preference를 durable하게 남길 필요가 있을 때 사용합니다.

이전 세션의 `handoff.md`가 있고 현재 feature branch가 확인되면 이어받는 세션은 `/tk:handoff-read`로 시작합니다. detached HEAD나 `main`, `master`, `develop`이면 먼저 feature branch 전환을 안내합니다.

## Branch-local artifacts

TigerKit working material은 branch별로 격리합니다.

```text
.tigerkit/
  branches/
    feature__example/
      requirements.md
      gap.md
      reflect.md
      handoff.md
```

`{escaped-branch}`는 현재 git branch name을 collision-safe하게 path-safe 변환한 값입니다. ASCII letter, digit, `.`, `_`, `-`는 그대로 두고 다른 byte는 `~HH` uppercase hex로 encode합니다. 예: `feature/foo` → `feature~2Ffoo`, `feature__foo` → `feature__foo`.

Root-level `.tigerkit/requirements.md`, `.tigerkit/gap.md`, `.tigerkit/reflect.md`는 deprecated artifact입니다. active write target이 아니라 migration candidate로 다룹니다.

TigerKit branch-local artifacts are not written on detached HEAD or protected branches (`main`, `master`, `develop`). Switch to a feature branch before running write commands.

## Command Surface

| Command | 역할 |
| --- | --- |
| `/tk:prep` | source-of-truth reference와 직접 사용자 인터뷰를 branch-local requirements index에 기록 |
| `/tk:gap` | branch-local indexed SOT reference와 clean HEAD baseline을 비교해 evidence-based gap을 기록 |
| `/tk:checkpoint` | ambiguity, user decision, unverifiable source, conflict, self-resolvable item을 분리하는 Decision Gate |
| `/tk:review` | TigerKit 준수룰 위반을 적대적으로 검토하는 artifact-free compliance review |
| `/tk:reflect` | session을 재구성해 branch-local reflection을 기록하고 durable artifact 격상 후보 제안 |
| `/tk:handoff-write` | 다음 모델/세션을 위한 branch-local continuation contract 작성 |
| `/tk:handoff-read` | handoff와 artifact map을 읽고 현재 repo 상태와 stale risk 확인 |

## 운영 사용 기준

- external source, ticket, Figma, issue, API docs를 먼저 묶어야 하면 `/tk:prep`
- indexed SOT와 현재 clean HEAD baseline을 비교해 누락이나 불일치를 기록하려면 `/tk:gap`
- 계속 진행 전 ambiguity, user decision, access 문제를 분리해야 하면 `/tk:checkpoint`
- TigerKit command, docs, evals, artifact, implementation 변경을 준수 관점에서 점검하려면 `/tk:review`
- session 정리, durable 반영 후보, handoff 전 상태 정리가 필요하면 `/tk:reflect`
- 다음 세션으로 넘길 작업 맥락을 남기려면 `/tk:handoff-write`
- 기존 handoff를 이어받아 stale 여부를 확인하려면 `/tk:handoff-read`

## Command notes

### `/tk:prep`
- 외부 source는 reference와 access status만 기록합니다.
- 직접 사용자 인터뷰만 local text로 보존합니다.
- local artifact 위치와 책임은 `.tigerkit/docs/artifact-layout.md`를 봅니다.

### `/tk:gap`
- branch-local `requirements.md`에 index된 SOT와 clean HEAD baseline을 비교해 `gap.md`에 기록합니다.
- 접근 불가 SOT가 있으면 partial coverage와 fallback 필요를 함께 남깁니다.

### `/tk:checkpoint`
- 확인이 더 필요한 항목과 바로 진행 가능한 항목을 나눌 때 사용합니다.

### `/tk:review`
- TigerKit contract 위반이 있으면 finding, 없으면 `NO_FINDINGS`를 반환합니다.

### `/tk:reflect`
- branch-local reflection을 기록하고 durable artifact 반영 후보를 surfaced 합니다.

### `/tk:handoff-write`, `/tk:handoff-read`
- handoff는 다음 세션용 continuation contract입니다.
- handoff-read는 현재 repo 상태와 artifact freshness를 먼저 확인합니다.

## 운영 범위 메모

세부 정책, 우선순위 규칙, 검증 원칙은 `CLAUDE.md`를 기준으로 봅니다.
