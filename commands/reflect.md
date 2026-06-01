---
description: 사용자 피드백, gap/review 결과, 반복 실수에서 durable repo rule 후보를 추출하고 CLAUDE.md 또는 .claude/rules/* 변경을 제안합니다.
argument-hint: "[scope] [apply=true]"
---

사용자 응답은 한글로 유지합니다. 코드, path, URL, ticket, commit, hash, identifier, error는 원문 그대로 둘 수 있습니다.

목표: `/tk:reflect`는 generic retrospective가 아닙니다. Claude project memory와 repo rule을 큐레이션하는 명령입니다.

```text
reflect = durable rule extraction + scoped rule proposal
```

## 관리 대상

- `CLAUDE.md`
- `.claude/rules/**/*.md`
- `.claude/skills/*/SKILL.md` audit/proposal only
- `.claude/handoffs/current.md` current-state handoff only

## 분류 대상

| 대상 | 언제 분류하나 |
| --- | --- |
| `CLAUDE.md` | 저장소 전반에 항상 적용되어야 하는 상위 작업 규칙, 협업 규칙, evidence rule, approval gate, 금지사항처럼 global rule일 때 |
| `.claude/rules/*` | 특정 경로, 도메인, 파일군, 워크플로우에만 적용되는 path-scoped rule일 때 |
| `.claude/skills/*/SKILL.md` | skill contract, prompt, trigger, output shape의 audit/proposal이 필요할 때. 직접 수정 대상이 아니라 감사와 제안만 한다 |
| `.claude/handoffs/current.md` | durable rule이 아니라 현재 상태, 진행 맥락, 남은 확인사항을 다음 세션에 넘겨야 할 때 |
| local/private memory | 사용자 개인 선호, 로컬 환경 습관, 특정 머신 맥락처럼 repo에 커밋하면 안 되는 정보일 때 |
| no action | one-off correction, 이미 해결된 단발성 메모, 근거 부족, 중복, 기존 규칙과 충돌하지만 아직 결론이 없는 경우 |

## 책임

- user feedback, repeated mistakes, gap results, PR review results에서 durable rule candidate를 추출합니다.
- global rule과 path-scoped rule을 구분합니다.
- 적절한 `.claude/rules/...` target file path를 제안합니다.
- target root에 `CLAUDE.md`가 없고 일반 작업 트리라면 scoped rule 제안과 별개로 root instruction bootstrap 후보를 제시합니다.
- 기존 rule과 충돌하는지 확인합니다.
- 중복 rule은 merge/update 대상으로 정리합니다.
- vague advice를 검증 가능한 rule로 다시 씁니다.
- 무엇이 `CLAUDE.md`에 가야 하는지와 `.claude/rules/*`에 가야 하는지를 구분합니다.

## 적용 게이트

- 기본값은 파일을 수정하지 않고 proposed patch만 출력합니다.
- `apply=true`가 있거나 사용자가 `적용해`, `반영해`, `승인`처럼 명시 승인한 경우에만 파일을 수정합니다.
- 충돌이 있으면 적용하지 않고 conflict를 먼저 보고합니다.

## Rule quality bar

- specific
- verifiable
- scoped
- short
- non-duplicative
- non-conflicting
- not based only on legacy code unless explicitly confirmed

모든 rule은 ID를 사용합니다.

예시 ID:
- `COPY-001`
- `LIB-001`
- `FORM-001`
- `MODAL-001`
- `GAP-001`
- `REVIEW-001`

## `CLAUDE.md`에 들어갈 것과 넣지 않을 것

`CLAUDE.md`에 들어갈 것:
- 저장소 전체에 적용되는 global instruction
- evidence, approval, safety, branch, review 같은 공통 규칙
- 여러 디렉터리와 워크플로우를 가로지르는 상위 규칙
- path-specific file로 쪼개면 오히려 찾기 어려워지는 핵심 운영 규칙

`CLAUDE.md`에 넣지 않을 것:
- 특정 디렉터리, 기능, 파일군에만 적용되는 세부 규칙
- 일회성 incident 메모
- 현재 세션 전용 handoff
- 개인 로컬 환경 선호
- skill implementation detail
- inspect되지 않은 legacy code 관성만으로 만든 규칙

경계가 애매하면 먼저 scoped rule을 우선 검토하고, 정말 전역 규칙일 때만 `CLAUDE.md`를 제안합니다.

## 절차

1. 현재 대화와 산출물에서 feedback, gap, review, repeated mistake evidence를 모읍니다.
2. Evidence와 Interpretation을 분리합니다.
3. one-off correction과 durable rule candidate를 구분합니다.
4. global rule인지 path-scoped rule인지 분류합니다.
5. target root에 `CLAUDE.md`가 있는지와 현재 작업 트리가 일반 작업 트리인지 확인합니다.
6. root instruction file이 없고 일반 작업 트리라면 scoped rule과 별개로 `CLAUDE.md` bootstrap 후보를 분류에 포함합니다.
7. 기존 `CLAUDE.md`, `.claude/rules/**/*.md`, 관련 skill/handoff와 충돌 또는 중복 여부를 점검합니다.
8. vague advice를 테스트 가능한 문장으로 재작성합니다.
9. 기본값에서는 patch proposal만 출력합니다.
10. `apply=true` 또는 사용자 승인 시에만 안전한 대상 파일을 수정합니다.
11. conflict가 남아 있으면 적용을 중단하고 conflict부터 보고합니다.

## 출력 템플릿

아래 섹션을 이 순서로 사용합니다. `### Session Decision Recap`은 optional이지만, 사용자가 decision path나 세션 맥락 추적을 필요로 한 경우에는 durable rule 0건이어도 출력할 수 있습니다.

### Reflect Result
- 무엇을 durable rule candidate로 추출했는지 요약합니다.
- global rule인지 scoped rule인지 표시합니다.
- apply 여부를 표시합니다.

### Session Decision Recap
- optional 섹션입니다.
- Evidence → Interpretation → Decision 흐름을 사람 친화적으로 1회 요약합니다.
- recap은 durable rule 자체가 아니라 추적성 receipt입니다.
- 사용자 원문 quote를 불필요하게 반복하지 않습니다.

### Classification
- 각 candidate를 어느 대상으로 분류했는지 적습니다.
- `CLAUDE.md` bootstrap 후보와 scoped rule 후보를 별도 항목으로 분리합니다.
- 필요하면 target path 예시를 함께 적습니다.

### Reason
- 왜 그 분류가 맞는지 evidence 기반으로 설명합니다.
- user feedback, gap, review, repeated mistake 중 어디서 왔는지 밝힙니다.

### Proposed Patch
- 기본 동작입니다.
- 실제 파일 수정 대신 diff 또는 삽입안 형태로 제안합니다.
- `apply=true`가 없으면 반드시 이 섹션에 머뭅니다.

### Conflicts
- 기존 rule과 충돌, 중복, 우선순위 불명확성을 적습니다.
- conflict가 있으면 적용하지 않습니다.

### Follow-up Audit
- `.claude/skills/*/SKILL.md`는 audit/proposal only인지 확인합니다.
- `.claude/handoffs/current.md`는 current-state only인지 확인합니다.
- 추가로 검토할 rule file 또는 merge 대상이 있으면 적습니다.

## 금지

- generic retrospective처럼 감상문을 쓰기
- `Session Decision Recap`을 durable rule이나 적용 승인처럼 취급하기
- apply 승인 없이 파일 수정하기
- conflict가 있는데도 적용하기
- root instruction file이 없는데 scoped rule만 제안하고 bootstrap 후보를 누락하기
- user feedback 없는 추측 규칙 만들기
- repeated evidence 없이 one-off correction을 durable rule로 승격하기
- global rule인데 scoped file에 숨기기
- scoped rule인데 `CLAUDE.md`에 과도하게 넣기
- `.claude/skills/*/SKILL.md`를 일반 rule 저장소처럼 취급하기
- `.claude/handoffs/current.md`에 durable rule을 저장하기
- legacy code만 보고 확정 규칙처럼 일반화하기

## 간단 예시

```text
Reflect Result
- REVIEW-001 추출, scoped rule, apply=false

Classification
- `.claude/rules/review/frontend.md` 제안

Reason
- 최근 PR review에서 동일한 누락이 3회 반복됨
- user feedback이 특정 frontend form 경로에만 한정됨

Proposed Patch
+ REVIEW-001: forms under `src/features/**` must declare loading/error/empty state explicitly.

Conflicts
- 기존 `FORM-001`과 일부 겹침. merge 후 단일 rule로 정리 필요

Follow-up Audit
- `.claude/skills/frontend-review/SKILL.md`는 rule 반영 대상이 아니라 audit/proposal only
- `.claude/handoffs/current.md`에는 이번 reflect 결과 요약만 남길 수 있음
```