---
name: tk-grill-me
description: "[user/auto] 사용자 소유 결정을 한 번에 하나씩 evidence-first 질문으로 닫는다. 명시적 invocation, 정확한 active tk-drive decision handoff, 또는 이 스킬의 pending question에 대한 답변에서 사용한다. 일반적인 ambiguity, artifact 존재, generic continuation만으로는 자동 시작하지 않는다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: grill-me
    relationship: adapted
---

# 결정 점검

명시적 `/tk-grill-me` 또는 `$tk-grill-me` invocation, 정확한 active
`tk-drive` decision handoff, 또는 같은 conversation에서 이 스킬의 pending question에
대한 사용자 답변에서 사용한다. 일반적인 ambiguity, artifact presence,
generic continuation, unrelated answer에서는 자동 활성화하지 않는다.

하나의 evidence-first decision procedure를 소유한다. standalone과 active-drive caller는
procedure, safety boundary, completion criteria를 공유하고; 결과 routing만 다르다.

## 계약

명시적 answer 없이는 사용자 결정을 절대 confirm하지 않는다. 침묵, 단순한
진행, factual evidence, 유사한 과거 답변은 consent가 아니다.

Caller mode가 presentation을 제어한다:

- `standalone`: 사용자에게 하나의 pending question 또는 최종 decision result를 표시한다.
- `active drive`: 같은 decision state를 내부적으로 반환하여 `tk-drive`가
  다음 applicable procedure를 직접 계속하게 한다. terminal result, receipt,
  `Pass`, 또는 caller-directed stopping surface를 렌더링하지 않는다.

Read-only다. source, Drive R/AC, units, ADRs, commits를 절대 쓰지 않으며,
`tk-drive`, fresh worker, sibling workflow owner를 절대 invoke하지 않는다.

## 절차

1. `read input(입력 읽기)`: task identity, caller mode, source, current evidence,
   confirmed decisions, unresolved user-owned decisions, pending question을 바인딩한다.
2. `investigate facts(사실 조사)`: source-located
   `verified | inferred | unavailable` facts를 생성한다.
3. `identify gaps`: Scope, Constraints, Outputs, Verification 전반에서
   facts와 decisions를 비교한다.
4. `rank`: safe-progress blocker, scope 또는 irreversible effect,
   verification blocker, downstream rework 순으로 가장 영향이 큰 unresolved
   decision을 선택한다.
5. `ask`: `🙋 grill-me · 응답 필요`를 출력한 뒤, 정확히 하나의 `Question`,
   `Recommendation`, `Evidence`를 그 순서로 반환하고 `pending`에서 멈춘다.
6. `incorporate`: 명시적 answer를 일치하는 `Decision`, `Constraint`, `Out of scope`,
   `Output`, 또는 `Verification` entry로 보존한다.
7. `repeat or close`: 이미 답한 질문은 반복하지 않는다. 네 축이 모두 정리되면,
   명시적 승인을 위해 합의된 목표 문장 하나를 제시한다.
8. `confirm`: 그 문장을 명시적으로 승인한 뒤에만 `confirmed`를 반환한다.

standalone의 질문 turn에서는 아래 packet만 user-facing으로 렌더링합니다. `Evidence`는
source-located fact만 담고, 없으면 `unavailable`로 둡니다. active drive에서는 이
packet을 표시하지 않고 같은 state를 caller에게 직접 반환합니다.

```text
🙋 grill-me · 응답 필요
Question: <정확히 하나의 user-owned decision>
Recommendation: <safe default 또는 none>
Evidence: <source와 verified | inferred | unavailable fact>
Native status: pending
```

## 모호성 ledger

ledger는 conversation 안에서만 유지한다:

- `Scope`: 포함하고 제외한 behavior;
- `Constraints`: technical, operational, business constraints 또는 명시적으로 없음;
- `Outputs`: 필요한 behavior, artifacts, results;
- `Verification`: acceptance criteria와 completion evidence.

unresolved items, confirmed decisions, unverified assumptions를 분리한다.
ledger는 per-turn dump template가 아니다. Question turn에는 새로 생기거나
변경된 evidence, selected unresolved item, one question만 포함한다.

## 사실과 사용자 판단

- 정확한 repository 또는 runtime evidence가 뒷받침하는 current facts만 자동 confirm하고; source를 cite한다.
- code-pattern 결론에 judgment가 필요하면 `inferred`로 표시한다.
- mixed fact-and-choice question을 묻기 전에 current facts를 먼저 조사한다.
- goals, scope, priorities, business rules, success criteria, new behavior에 대해서는 항상 질문한다.
- 필요한 evidence에 접근할 수 없으면 `Unverifiable`을 반환한다. 단, 독립적인 decision이 여전히 안전하면 예외다.
- confirmed sources가 충돌하면 양쪽을 보존하고 하나의 decision question을 묻는다; 묵묵히 선택하지 않는다.

## 답변 보존과 종결

free-form answer의 의미를 보존한다. 말하지 않은 내용은 assumption으로 남긴다. summary가
의미를 바꾸거나, confirmed evidence와 충돌하거나, material ambiguity를 만들 때만
clarification을 요청한다.

`done`과 model confidence만으로는 ledger를 닫지 않는다. 네 축을 모두 확인하고,
unresolved 상태에서는 다음 highest-impact question을 묻고, 최종 합의 목표 문장에
대한 명시적 승인을 요구한다.

Standalone confirmed results에는 비어 있지 않은 `## Decisions`,
`## Assumptions`, `## Remaining risks`만 사용한다. phase/status provenance는
붙이지 않는다. 하나의 decision에는 한 줄에서 세 줄을 사용하고, compound set에는
읽기 쉬운 두 줄에서 일곱 rows 또는 bullets를 사용한다. 여덟 개 이상이면 owning
source 또는 spec reference와 함께 상위 다섯 개에서 일곱 개만 유지한다.

Native status: `confirmed | pending | aborted | Blocked | Unverifiable`.
Standalone maps these to `Pass | Pending | Blocked | Blocked | Unverifiable`.
Active drive는 user-facing status block 없이 native status를 직접 소비한다.

## 금지 사항 / 반패턴

- 같은 decision procedure를 다른 skill로 분리하지 않는다.
- 사용자를 대신해 결정하거나 독립된 decisions를 묶지 않는다.
- artifacts를 mutate하거나 downstream phase owners를 invoke하지 않는다.
- active-drive routing이 receipt 또는 terminal stop이 되게 하지 않는다.
