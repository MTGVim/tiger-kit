---
description: 현재 task state의 ambiguity, user decision, unverifiable source, conflict, self-resolvable item을 점검해 계속 진행해도 되는지 판단하는 Decision Gate입니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. URL, 파일 경로, commit hash, ticket id, 코드 식별자, 오류 메시지는 원문 그대로 유지할 수 있습니다.

목표: `/tk:checkpoint`는 구현 명령이 아니라 Decision Gate입니다. 현재 task state를 점검해 계속 진행 가능한지, 어떤 assumption을 기록해야 하는지, 무엇을 사용자 결정으로 멈춰야 하는지 분리합니다.

```text
checkpoint = ambiguity / access / verification / decision gate
```

## 입력으로 확인할 수 있는 자료

필요한 범위에서 아래를 확인합니다.

1. 현재 사용자 요청과 대화 context
2. `.tigerkit/branches/{escaped-branch}/requirements.md`, if present
3. `.tigerkit/branches/{escaped-branch}/gap.md`, if present
4. `.tigerkit/branches/{escaped-branch}/handoff.md`, if present
5. `CLAUDE.md` / project policy
6. `DESIGN.md`, if present
7. `reuse-map.md`, if present
8. 관련 code path, type, schema, API, source file

source에 접근할 수 없으면 내용을 추측하지 않습니다.

## classification rules

각 uncertainty나 gap item은 아래 중 하나 이상으로 분류합니다.

| Category | Meaning |
|---|---|
| `blocking_question` | 사용자 답변 전에는 진행하면 안 됩니다. |
| `user_decision_required` | policy, interpretation, token, scope, behavior를 사용자가 선택해야 합니다. |
| `assumption` | 계속 진행 가능하지만 assumption을 명시적으로 기록해야 합니다. |
| `not_verifiable` | 필요한 source를 현재 inspect할 수 없습니다. |
| `sot_conflict` | 둘 이상의 Source-of-Truth가 충돌합니다. |
| `needs_code_verification` | code, type, schema, data inspection이 필요합니다. |
| `self_resolvable` | 사용자 입력 없이 안전하게 해결할 수 있습니다. |
| `external_dependency` | backend, API, infrastructure, external owner 변경이 필요합니다. |
| `large_or_risky_refactor` | 해결 가능하지만 넓거나 위험해 승인 없이 자동 적용하면 안 됩니다. |
| `safe_default` | 낮은 위험의 default가 있고 그 default를 명시할 수 있습니다. |

Severity와 resolvability를 섞지 않습니다. 낮은 severity도 사용자 결정이 필요할 수 있고, 높은 severity도 local self-resolvable일 수 있습니다.

## final status

마지막에는 반드시 아래 중 하나를 정확히 출력합니다.

| Status | Meaning |
|---|---|
| `CLEAR` | 의미 있는 ambiguity나 blocker가 없습니다. 계속 진행할 수 있습니다. |
| `PROCEED_WITH_ASSUMPTIONS` | 계속 진행할 수 있지만 assumption을 명시적으로 기록해야 합니다. |
| `PAUSE_FOR_USER_DECISION` | 사용자 결정 전에는 계속 진행하면 안 됩니다. |
| `BLOCKED_BY_ACCESS` | 필요한 SOT, document, image, file, API 접근이 없습니다. |
| `NEED_VERIFICATION` | code, type, data, source verification이 필요합니다. |

## SOT accessibility rule

SOT reference는 접근 가능하고 inspect되기 전까지 fully auditable로 다루지 않습니다.

문서, 이미지, URL, local file path에 접근할 수 없으면:

- 내용을 추론하지 않습니다.
- dependent item을 `Match`로 표시하지 않습니다.
- `not_verifiable` 또는 `BLOCKED_BY_ACCESS`로 표시합니다.
- 접근 가능한 file, image, local path, export, pasted content를 요청합니다.
- unresolved reference를 Not Verifiable Items에 기록합니다.

## dependency policy rule

Generic TigerKit 문서와 명령은 특정 dependency, package, framework, component library, vendor를 전역 deprecated로 hard-code하지 않습니다.

Project SOT가 어떤 dependency를 banned, deprecated, avoided, required로 지정한 경우에만 해당 project policy 기준으로 audit합니다.

예시에는 `LegacyComponent`, `DeprecatedPackage`, `ProjectPreferredComponent`, `ProjectPolicyDependency` 같은 neutral placeholder를 사용합니다.

## checkpoint trigger

아래 high-impact ambiguity가 있으면 checkpoint를 실행하거나 report 안에서 checkpoint 필요성을 안내합니다.

- SOT asset이 있지만 접근할 수 없음
- design과 requirements 충돌
- user policy와 existing code 충돌
- dependency/component 선택이 project-specific policy에 의존
- visible copy decision에 source 충돌
- schema/type/data field 불확실
- fix가 backend/API behavior에 의존
- fix가 broad refactoring 필요
- agent가 assumption을 implementation으로 바꾸려 함
- gap classification이 inspect하지 않은 source에 의존

trivial copy나 local one-line fix처럼 SOT가 명확하고 safe action이 분명하면 checkpoint를 남발하지 않습니다.

## required output format

```md
# Checkpoint

## 1. Current Status

Briefly describe what has been reviewed and what task is currently being performed.

## 2. Blocking Questions

| ID | Question | Source | Why it matters | Consequence if wrong | Pause? |
|---|---|---|---|---|---|

## 3. User Decisions Needed

| ID | Decision | Options | Current assumption | Recommended handling | Pause? |
|---|---|---|---|---|---|

## 4. Assumptions Being Made

| ID | Assumption | Source | Risk | Consequence if wrong |
|---|---|---|---|---|

## 5. Not Verifiable Items

| ID | Item | Reason | Needed input | Current handling |
|---|---|---|---|---|

## 6. SOT / Policy Conflicts

| ID | Conflict | Sources | Current priority rule | Needs user decision? |
|---|---|---|---|---|

## 7. Self-resolvable Items

| ID | Item | Why self-resolvable | Safe action |
|---|---|---|---|

## 8. Items Not Safe to Auto-resolve

| ID | Item | Reason | Required next input |
|---|---|---|---|

## 9. Continue / Pause Judgment

Final status: `CLEAR | PROCEED_WITH_ASSUMPTIONS | PAUSE_FOR_USER_DECISION | BLOCKED_BY_ACCESS | NEED_VERIFICATION`

One concise explanation.
```

## 금지

- 구현, commit, push, PR 생성, merge, deploy
- uncertainty를 guessed requirement로 변환
- inaccessible SOT 내용을 추측
- dependent item을 evidence 없이 `Match`로 표시
- 모든 사소한 low-risk detail마다 사용자 질문
- 존재하지 않는 TigerKit command를 real command처럼 언급
- `/tk:reflect`를 default next command로 추천
- generic TigerKit 문서에 repo-specific dependency example 추가
- 특정 dependency를 전역 deprecated로 hard-code
