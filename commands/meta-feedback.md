---
description: 현재 세션의 TigerKit command/skill friction을 일반화된 개선안으로 정리합니다.
argument-hint: "[target-skill-or-command?] [--out <path>]"
---

이 명령은 기존 TigerKit improvement command이며 v7.1에서도 active command로 유지합니다.

사용자 응답은 한글로 유지합니다. 단, 이 command의 핵심 안전 조건은 출력 자체가 이미 일반화되어 있어야 한다는 점입니다.

목표: `/tk:meta-feedback`은 현재 세션 전체 내역에서 관측된 TigerKit command/skill 사용 friction, 사용자 교정, 반복 실수, output UX 문제, latency 문제, false-positive pattern을 TigerKit 자체 개선안으로 추출합니다. 이 명령은 repo rule을 제안하는 `/tk:reflect`가 아닙니다.

```text
meta-feedback = session-history-based generalized skill improvement proposal + privacy-first redaction receipt
```

## 역할 경계

| 구분 | `/tk:reflect` | `/tk:meta-feedback` |
| --- | --- | --- |
| 대상 | 사용자 repo의 durable insight | TigerKit command/skill 자체 |
| 입력 | branch-local specs/gap/verify memory와 repo context | 현재 세션 내역 전체의 feedback/friction |
| 산출 | repo rule direct-apply contract 개선안 또는 issue draft | 일반화된 TigerKit 개선안 또는 issue draft |
| 표현 | repo context를 제한적으로 유지할 수 있음 | repo context를 반드시 제거 |
| 기본 동작 | apply=true | proposal-only |

`/tk:meta-feedback`은 TigerKit 본체 개선만 다룹니다. agent runtime 설정, MCP permission/config, custom agent 생성, editor/CLI harness 튜닝은 TigerKit command contract 범위 밖으로 두고 필요하면 별도 외부 작업으로 제안만 분리합니다.

## 기본 동작

- 기본값은 파일을 수정하지 않고 일반화된 proposal만 출력합니다.
- `/tk:reflect`가 기본 후속 단계로 제출할 때도 같은 proposal-only 동작과 privacy gate를 유지합니다.
- `--out <path>`가 있을 때만 current worktree root 내부 경로에 파일을 작성할 수 있습니다.
- `--out` 파일 내용도 chat output과 같은 redacted format이어야 합니다.
- worktree root 밖 경로, user home, `/tmp`, hidden control file path에는 쓰지 않습니다.
- 출력하기 전에 privacy gate를 통과해야 합니다.
- 안전하게 일반화할 수 없으면 개선안을 만들지 않고 `cannot_generalize_safely`로 중단합니다.

## v7.1 feedback classes

허용 feedback class:

- `ux`
- `output-format`
- `taxonomy`
- `safety`
- `dispatch`
- `docs`
- `performance`
- `false-positive`

## Generalization Gate

`/tk:meta-feedback`은 emit 전에 모든 proposal을 일반화 게이트에 통과시켜야 합니다. 이 게이트는 privacy gate보다 넓은 품질 게이트이며, 통과하지 못한 proposal은 rewrite하거나 reject합니다.

### Domain-term guard

Proposal 본문에서 host-specific 명사를 탐지하면 그대로 출력하지 않습니다.

탐지 대상:

- project, framework, product, customer, organization 이름
- 파일, 디렉토리, source path, 확장자를 포함한 path fragment
- symbol, class, function, command 구현체 이름 같은 CamelCase 또는 코드 식별자
- feature, page, menu, UI label, domain entity 이름
- URL, ticket, issue, PR, branch, commit, local environment reference

휴리스틱으로 고유명사, path separator, 파일 확장자, CamelCase, snake_case/kebab-case 식별자, issue/PR/hash 형태를 확인합니다. 단, `/tk:*`, `gap`, `launch`, `reflect`, `handoff`, `meta-feedback`, `seal`, `precondition`, `verification_gate`, `abort code`, `privacy gate`, `generalization gate`처럼 TigerKit command contract 자체 어휘는 허용합니다.

### Restate test

각 proposal은 아래 자가검증 질문을 통과해야 합니다.

```text
다른 repo·다른 도메인에서도 그대로 말이 되는가?
```

도메인 명사를 제거했을 때 friction이 사라지면 command-level friction이 아니므로 `/tk:meta-feedback` 대상이 아닙니다. 이 경우 repo/도메인 insight는 `/tk:reflect`로 route하고, command·skill 계약 friction만 추출해 meta-feedback로 남깁니다.

### Routing rule

- repo/도메인 insight → `/tk:reflect` 또는 repo durable rule 후보
- command·skill 계약 friction → `/tk:meta-feedback`
- continuation/follow-up 보관 → `/tk:handoff`
- basis-target 비교 finding → `/tk:gap` 또는 `/tk:gap --review`

한 사실이 두 채널에 걸치면 domain-specific 부분은 제거하거나 `/tk:reflect`로 분리하고, mechanism-level 부분만 `/tk:meta-feedback` proposal로 작성합니다.

### Vocabulary constraint

`/tk:meta-feedback` 산출물은 대상 command/skill의 자체 계약 어휘와 feedback taxonomy만 사용합니다. 외부 repo의 domain vocabulary로 설명해야만 이해되는 proposal은 generalization gate 실패입니다.

예시:

- `/tk:gap`이 작은 ticket에서도 오래 걸리는 performance friction
- BE DTO, permission, persistence 의미를 과추론해 오탐을 내는 false-positive pattern
- `lite`/`strict` 추천 UX 혼동
- 기존 command를 제거해 compatibility가 깨진 command surface feedback
- 사용자 대화에 보이는 안내가 영어라 이해 비용이 커지는 output-format feedback

## Privacy Gate

출력과 저장 산출물에는 아래 항목이 없어야 합니다.

- repo 이름, product 이름, customer 또는 organization 이름
- feature, page, menu, UI label 같은 도메인 고유명
- 내부 path, URL, ticket, branch, PR 번호, commit hash
- 사용자 원문 quote 또는 세션 원문 발화
- code path, 파일명, stack trace 원문
- 특정 프로젝트를 역추적할 수 있는 조합 정보

허용되는 표현은 아래처럼 placeholder 또는 abstract class만 사용합니다.

- `<project>`
- `<skill>`
- `<command>`
- `<domain-term>`
- `<ui-label>`
- `<internal-path>`
- `<reference>`
- `source_type=session_correction`
- `source_type=repeated_friction`
- `source_type=output_shape_feedback`
- `source_type=latency_feedback`
- `source_type=false_positive_feedback`

## Generalization Rules

| 원본 유형 | 출력 대체 표현 |
| --- | --- |
| repo/product/customer 이름 | `<project>` |
| page/menu/title/feature 이름 | `<domain-term>` 또는 `<ui-label>` |
| local path 또는 source path | `<internal-path>` |
| URL, ticket, issue, PR, branch, commit | `<reference>` |
| 사용자 원문 발화 | `source_type=session_correction` |
| 세션의 구체적 시행착오 | `source_type=repeated_friction` |
| gap latency feedback | `source_type=latency_feedback` |
| backend false positive feedback | `source_type=false_positive_feedback` |

## 절차

1. target이 있으면 `<skill>` 또는 `<command>` 수준으로만 식별합니다.
2. 현재 세션 전체 내역에서 TigerKit command/skill 개선과 관련 있는 friction만 고릅니다.
3. repo rule, product requirement, implementation TODO는 제외하거나 `/tk:reflect`, `/tk:gap`, `/tk:handoff` 대상으로 분류합니다.
4. agent runtime/config, MCP permission, custom agent 추천은 TigerKit 본체 개선안에서 제외합니다.
5. 원문 evidence를 직접 출력하지 않고 evidence class만 남깁니다.
6. 모든 고유명, path, URL, ticket, branch, PR, commit, raw quote를 placeholder로 치환합니다.
7. Domain-term guard를 실행하고 host-specific 명사가 남으면 rewrite 또는 reject합니다.
8. Restate test를 실행하고 다른 repo·다른 도메인에서 그대로 말이 되지 않으면 `/tk:reflect`, `/tk:handoff`, `/tk:gap` 계열로 route합니다.
9. 대상 command/skill의 자체 계약 어휘와 feedback taxonomy만 사용했는지 확인합니다.
10. 치환 후에도 특정 프로젝트를 추정할 수 있으면 `cannot_generalize_safely`로 중단합니다.
11. 개선안을 TigerKit command/skill 수준의 generic change로 씁니다.
12. `--out <path>`가 있으면 같은 redacted output만 파일로 작성합니다.

## 출력 템플릿

아래 H2 섹션을 이 순서로 사용합니다.

```md
## Meta Feedback Summary
- Target: <skill-or-command>
- Feedback class: <ux|output-format|taxonomy|safety|dispatch|docs|performance|false-positive>
- Privacy status: generalized

## Generalized Friction
- Situation: <generic situation>
- Problem: <generic problem>
- Impact: <generic impact>

## Proposed Improvement
- Change: <generic skill/command improvement>
- Why: <reason without project-specific evidence>

## Redaction Receipt
- Removed: <repo names|paths|URLs|domain labels|quoted user text>
- Kept: <abstract pattern only>
- Generalization gate: passed
- Restate test: passed
- Unsafe details included: none
```

## 중단 템플릿

안전하게 일반화할 수 없으면 아래 형식을 사용합니다.

```md
## Meta Feedback Summary
- Target: <skill-or-command>
- Feedback class: safety
- Privacy status: cannot_generalize_safely

## Generalized Friction
- Situation: cannot report safely without exposing project-specific details
- Problem: cannot report safely without exposing project-specific details
- Impact: cannot report safely without exposing project-specific details

## Proposed Improvement
- Change: none
- Why: privacy gate failed

## Redaction Receipt
- Removed: attempted project-specific details
- Kept: none
- Unsafe details included: none
```

## 금지

- raw session evidence를 quote하기
- repo 이름, product 이름, domain label, 내부 path를 그대로 쓰기
- URL, issue, PR, ticket, branch, commit을 그대로 쓰기
- 사용자 발화를 원문으로 붙여 넣기
- `/tk:reflect`처럼 repo rule patch를 제안하기
- `/tk:gap`처럼 basis-target gap finding을 만들기
- privacy gate 실패 후에도 일부만 가려서 계속 출력하기
