<!-- tigerkit:`shared-execution-protocol`; `canonical`=skills/tk-prep/references/test-doubles.md -->

# Test-double safeguards

Load this reference only when the actual task uses or proposes a mock, fake, stub, spy,
or another test double. Continue to use [behavior-first testing](testing.md) for the
test's falsifiability and mutation rules.

- A double's existence or a mock-only assertion is not proof of product behavior.
- Understand the real dependency's required side effects before replacing it. When
  practical, mock only the slow or external layer and keep tested local behavior real.
- When arguments, call counts, or call order are the contract, verify them specifically.
- Preserve the real integration response shape; an oversimplified double creates false
  confidence when downstream behavior depends on omitted fields.
- Do not add production cleanup or reset APIs only for tests. Keep test-only cleanup in
  test utilities unless the production component owns that lifecycle.
- If double setup is more complex than the behavior, prefer a real component or a
  narrower integration seam.
