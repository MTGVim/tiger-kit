<!-- tigerkit:`shared-execution-protocol`; `canonical`=skills/tk-prep/references/testing.md -->

# Behavior-first testing

Read this document only for work that changes code. Do not create ceremonial tests for
documentation or wording-only changes, or for trivial changes without observable
behavior. The goal is protection for changed behavior, not a numeric adoption rate.

## Readiness

Before approval, inspect the actual repository test surface:

- related test locations and the fastest focused command;
- the observable behavior and exact regression this change must protect;
- whether existing tests can actually fail when that behavior breaks;
- boundaries, errors, and states that need new tests;
- binding integration checks and whether any AC is browser-visible.

Do not treat test presence as sufficient protection. When possible, capture a bug first
with an exact reproduction test.

## `N/A` and engineering exception

- `N/A`: wording-only changes, visual-only judgment, or no useful automated behavior
  test surface, such as a simple pass-through.
- Engineering exception: meaningful behavior exists, but the test foundation is absent
  or unsuitable and no useful test can be built.

For an exception, record the gap, investigation evidence, risk, mitigation, and approval
state. Do not add a fake test or hide behind `N/A` when a real test surface exists.
Browser verification does not replace automated regression tests, although a visual-only
AC may be judged with browser evidence.

## RED → GREEN → REFACTOR

This is the default order for testable features, bug fixes, behavior changes, and
meaningful structural improvements.

1. **RED**: Write the smallest behavior test for the desired behavior.
2. **Confirm RED**: Run it before changing product behavior code and verify that it
   fails for the intended reason.
3. **GREEN**: Write only the minimum implementation that passes the test.
4. **Confirm GREEN**: Verify the same focused command and related existing tests.
5. **REFACTOR**: Clean up duplication, names, and structure only while green, then
   verify again.

Each cycle protects one `observable behavior slice`. Here, `vertical` does not always
mean crossing every UI→API→DB layer; it means the highest `practical seam` that
independently protects one user/product behavior. Do not default to a
`horizontal bulk cycle` that accumulates many tests before implementing them. When an existing
`public/observable seam` is sufficient, do not create a new `seam` or widen a
`production API` solely for `testability`.

If the test fails for the wrong reason, fix it and confirm RED again. If it already
passes, investigate whether it protects the new behavior or the product behavior
already exists. Do not write product code first when a necessary RED is missing.

## Good-test gate

Before writing a test body, answer: “What realistic product-code mutation should make
this test fail?” Verify real components, integration boundaries, output, and side
effects with independently checked expectations whenever possible.

When the actual task uses or proposes a mock, fake, stub, spy, or another test double,
lazy-load [test-double safeguards](test-doubles.md). Do not load them for ordinary tests
that keep their dependencies real.

These do not protect behavior:

- a circular assertion where a product helper computes both expected and actual values;
- tests that search only for raw text, symbol presence/removal, or private structure;
- tests that verify only tool behavior, mocks, or test identifier presence;
- change detectors that react only to intentional constant or message changes;
- test-only helpers added to the product API;
- tests that increase adoption counts without checking results or side effects.

Before completion, imagine these mutations. Protection is incomplete if no test fails
for any applicable mutation:

- a wrong branch, handler, argument, or constant;
- a missing state change or side effect;
- an empty or default return value;
- removed validation or recurrence of the exact bug.

## Evidence contract

When applicable, the implementer report records:

- the RED command, relevant failure, and expected reason;
- the GREEN command and relevant passing result;
- required related suites and check results;
- the rationale when the test judgment is `N/A` or an engineering exception.

Reviewers compare the diff against testing obligations rather than trusting a passing
claim alone. Read existing evidence before rerunning it, and run a focused test only for
a specific unresolved question.

Before any success or completion claim, run the fresh complete command that proves it
at the current candidate and read both its output and exit state. An implementer or
child success report remains untrusted evidence, and a focused or partial check must not
be extrapolated into full completion.
