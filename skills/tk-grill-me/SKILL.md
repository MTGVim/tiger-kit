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

명시적 `/tk-grill-me` 또는 `$tk-grill-me` 호출, 정확한 활성
`tk-drive` 결정 handoff, 또는 같은 대화에서 이 스킬의 `pending` 질문에
대한 사용자 답변에서 사용한다. 일반적인 모호성, 산출물 존재,
일반적인 후속 진행, 무관한 답변에서는 자동 활성화하지 않는다.

하나의 근거 우선 결정 절차를 소유한다. 독립 실행과 활성-drive 호출자는
절차, 안전 경계, 완료 기준을 공유하고 결과 라우팅만 다르다.

## 계약

명시적인 답변 없이는 사용자 결정을 절대 confirm하지 않는다. 침묵, 단순한
진행, 사실 근거, 유사한 과거 답변은 consent가 아니다.

호출 모드가 표시 방식을 제어한다:

- `standalone`: 사용자에게 하나의 pending question 또는 최종 결정 결과를 표시한다.
- `active drive`: 같은 결정 상태를 내부적으로 반환하여 `tk-drive` 가
  다음 applicable procedure를 직접 계속하게 한다. terminal 결과, receipt,
  `Pass`, 또는 호출자가 지정한 중단 표면을 렌더링하지 않는다.

읽기 전용이다. 소스, Drive R/AC, 단위, ADRs, commits를 절대 쓰지 않으며,
`tk-drive`, 새 작업자, 인접 워크플로 소유자를 절대 호출하지 않는다.

## 절차

1. `입력 읽기`: task identity, caller mode, 소스, 현재 근거,
   confirmed decisions, unresolved user-owned decisions, pending question을 바인딩한다.
2. `사실 조사`: 소스 위치가 명시된
   `verified | inferred | unavailable` 사실을 생성한다.
3. `공백 식별`: Scope, Constraints, Outputs, Verification 전반에서
   사실과 decisions를 비교한다.
4. `순위 지정`: 안전한 진행을 막는 blocker, 범위 또는 되돌릴 수 없는 영향,
   검증 blocker, downstream 재작업 순으로 가장 영향이 큰 미해결
   결정을 선택한다.
5. `ask`: `🙋 grill-me · 응답 필요` 를 출력한 뒤, 정확히 하나의 `Question`,
   `Recommendation`, `Evidence` 를 그 순서로 반환하고 `pending` 에서 멈춘다.
6. `반영`: 명시적 답변을 일치하는 `Decision`, `Constraint`, `Out of scope`,
   `Output`, 또는 `Verification` entry로 보존한다.
7. `반복 또는 종료`: 이미 답한 질문은 반복하지 않는다. 네 축이 모두 정리되면,
   명시적 승인을 위해 합의된 목표 문장 하나를 제시한다.
8. `확정`: 그 문장을 명시적으로 승인한 뒤에만 `confirmed` 를 반환한다.

독립 실행의 질문 turn에서는 아래 packet만 사용자에게 표시합니다. `Evidence` 는
소스 위치가 명시된 사실만 담고, 없으면 `unavailable` 로 둡니다. 활성 drive에서는 이
packet을 표시하지 않고 같은 상태를 호출자에게 직접 반환합니다.

```text
🙋 grill-me · 응답 필요
Question: <정확히 하나의 user-owned decision>
Recommendation: <safe default 또는 none>
Evidence: <source와 verified | inferred | unavailable fact>
Native status: pending
```

## 모호성 장부

장부는 대화 안에서만 유지한다:

- `Scope`: 포함하고 제외한 동작;
- `Constraints`: 기술·운영·비즈니스 제약 또는 명시적으로 없음;
- `Outputs`: 필요한 동작, 산출물, 결과;
- `Verification`: acceptance criteria와 completion 근거.

미해결 항목, 확정된 결정, 검증되지 않은 가정을 분리한다.
장부는 turn별 덤프 템플릿가 아니다. Question turn에는 새로 생기거나
변경된 근거, 선택된 미해결 항목, 질문 하나만 포함한다.

## 사실과 사용자 판단

- 정확한 저장소 또는 런타임 근거가 뒷받침하는 현재 사실만 자동 confirm하고; 소스를 cite한다.
- 코드 패턴 결론에 판단이 필요하면 `inferred` 로 표시한다.
- 사실과 선택이 섞인 질문을 묻기 전에 현재 사실을 먼저 조사한다.
- 목표, 범위, 우선순위, 비즈니스 규칙, 성공 기준, 새로운 동작에 대해서는 항상 질문한다.
- 필요한 근거에 접근할 수 없으면 `Unverifiable` 을 반환한다. 단, 독립적인 결정이 여전히 안전하면 예외다.
- 확정된 출처가 충돌하면 양쪽을 보존하고 하나의 결정 질문을 묻는다; 묵묵히 선택하지 않는다.

## 답변 보존과 종결

자유 형식 답변의 의미를 보존한다. 말하지 않은 내용은 assumption으로 남긴다. 요약이
의미를 바꾸거나, confirmed 근거와 충돌하거나, material ambiguity를 만들 때만
clarification을 요청한다.

`done` 과 model confidence만으로는 장부를 닫지 않는다. 네 축을 모두 확인하고,
unresolved 상태에서는 다음 가장 영향이 큰 질문을 묻고, 최종 합의 목표 문장에
대한 명시적 승인을 요구한다.

독립 실행 확정 결과에는 비어 있지 않은 `## Decisions`,
`## Assumptions`, `## Remaining risks` 만 사용한다. phase/status 출처는
붙이지 않는다. 하나의 결정에는 한 줄에서 세 줄을 사용하고, 복합 집합에는
읽기 쉬운 두 줄에서 일곱 개의 row 또는 bullet을 사용한다. 여덟 개 이상이면 소유하는
소스 또는 spec reference와 함께 상위 다섯 개에서 일곱 개만 유지한다.

Native status는 `confirmed | pending | aborted | Blocked | Unverifiable` 이다.
Standalone은 이를 `Pass | Pending | Blocked | Blocked | Unverifiable` 로 매핑한다.
Active drive는 user-facing status block 없이 native status를 직접 소비한다.

## 금지 사항 / 반패턴

- 같은 결정 절차를 다른 스킬로 분리하지 않는다.
- 사용자를 대신해 결정하거나 독립된 결정을 묶지 않는다.
- 산출물을 변경하거나 downstream phase 소유자를 호출하지 않는다.
- 활성-drive 라우팅이 receipt 또는 terminal 중단이 되게 하지 않는다.
