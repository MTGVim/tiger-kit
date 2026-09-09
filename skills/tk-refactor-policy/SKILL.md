---
name: tk-refactor-policy
description: "[user] 저장소의 복잡한 boolean 비즈니스 규칙과 조건 분기를 읽기 전용으로 찾아, 현재 유지부터 predicate·Specification·Decision Table·Rules Engine까지 최소 충분한 구조 개선안을 제안합니다. 일반 코드 리뷰나 자동 리팩터링에는 사용하지 않습니다."
disable-model-invocation: true
argument-hint: "<repository scope | path | module | business rule>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# Business Policy Refactoring

Start only through an explicit `/tk-refactor-policy`, `$tk-refactor-policy`, or host skill
selection. Never invoke automatically from `tk-review`, `tk-prep`, `tk-audit`, a generic
refactoring request, or the mere presence of complex conditionals.

This skill is read-only. Inspect the requested repository scope and propose refactoring
candidates, but do not edit source, tests, configuration, Git state, issues, PRs, ledgers,
or durable artifacts. Do not dispatch another skill. If the user later wants an accepted
candidate implemented, `tk-prep` may own that separate execution request.

## Target

Look for logic whose primary purpose is to decide a business policy, eligibility,
permission, availability, approval, visibility, pricing rule, state transition guard, or
similar outcome from multiple facts. Boolean-returning code is a strong signal, not a
requirement.

Distinguish business policy from ordinary control flow. Loops, error handling, resource
cleanup, orchestration order, parsing, one-off guards, framework lifecycle branches, and
straightforward validation should normally stay ordinary code unless the domain meaning is
the actual source of complexity.

Read only enough call sites, types, tests, domain context, and neighboring rules to answer:

- what business statement the code represents;
- whether callers need only `true/false` or also a reason, priority, or matched rule;
- whether conditions are reused independently;
- whether combinations are sparse, tabular, ordered, or stateful;
- how often policy changes and who owns those changes;
- what existing repository abstraction already expresses similar rules.

Prefer repository precedent over introducing a new local vocabulary.

## Minimal abstraction ladder

Choose the least powerful structure that materially improves readability, change safety,
and testability. Consider candidates in this order and stop when one is sufficient:

1. keep the current code;
2. extract clearly named predicates;
3. compose predicates with small `all` / `any` / `not` helpers;
4. use a Specification-style object only when named reusable rule composition needs richer
   domain identity or behavior;
5. use a Decision Table when combinations are naturally tabular and policy rows are easier
   to review than branching control flow;
6. use a Rules Engine or Policy-as-Code only when policy volume, independent runtime change,
   external ownership, or auditability genuinely requires it.

Do not create a custom DSL merely to remove `if` statements. Do not replace readable early
returns with combinators when the result becomes harder to debug. Do not introduce a shared
abstraction until at least two real policies need the same semantics and the common shape is
supported by repository evidence.

## Semantics and explainability

A structural refactor must preserve behavior. Identify the existing tests or observable
invariants that would prove equivalence before recommending implementation. If coverage is
insufficient, name the smallest characterization tests needed before changing structure.
Do not recommend breaking working code just to manufacture a failing test for a
behavior-preserving refactor.

When callers or operators need to know why a decision failed or which rule matched, do not
hide that information behind an opaque boolean combinator. Prefer an explicit decision
result, reason code, matched specification, or another repository-consistent diagnostic
shape. Short-circuit order is behavior when predicates have cost, side effects, or priority;
preserve or explicitly model it instead of assuming pure commutativity.

## Candidate quality

A candidate is worthwhile only when the proposed structure improves at least one material
maintenance property without creating a larger abstraction tax. Check whether it:

- makes the business statement easier to understand from code;
- reduces the edit surface for adding or removing a rule;
- enables focused tests of individual rules and their composition;
- reduces duplicated policy meaning;
- preserves useful failure explanations and debugging paths;
- matches the repository's abstraction level and ownership boundaries.

No candidate is a valid result. Do not produce a refactoring quota.

## Output

Lead with the recommendation, not the procedure. For each worthwhile candidate, report:

```text
<path:line> · <business policy>
Current: <why the current shape is costly or error-prone>
Recommendation: <keep | named predicates | predicate combinator | specification | decision table | rules engine/policy-as-code>
Why: <material benefit and why a simpler option is insufficient>
Verification: <existing invariant/tests or characterization tests needed before implementation>
```

Add `Caution:` only when explainability, ordering, side effects, policy ownership, or another
constraint could make the obvious declarative rewrite unsafe. Keep low-value style cleanup
out of the result.

Close with whether a repository-wide abstraction is justified or whether each candidate
should remain local. If implementation is requested in the same prompt, state that this
skill has completed the read-only policy analysis and present the accepted candidate as an
optional input to a separately selected implementation owner; do not mutate or auto-route.
