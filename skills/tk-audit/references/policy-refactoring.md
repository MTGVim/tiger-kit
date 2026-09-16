# Business policy lens

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

## Audit integration

Use the owning audit's `AUD-*` finding contract, including evidence, impact, effort, fix risk, confidence,
verification baseline and next route. Put the chosen minimal structure and why simpler options are insufficient
in the fix sketch. Include explainability, evaluation order, side effects and characterization tests when relevant.
A sound policy with no material maintenance problem yields no finding, not a style or abstraction quota.
Keep recommendations local unless multiple policies justify a repository-wide abstraction. This lens grants no
implementation or automatic dispatch authority and creates no separate report, ID system or durable lifecycle.
