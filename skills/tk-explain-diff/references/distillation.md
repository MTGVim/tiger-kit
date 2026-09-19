# Distillation Provenance

Reviewed 2026-09-19. Geoffrey Litt's [explain-diff Gist](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524/126e7fe9eecaafadfe1ac8bb183d135812b608f2)
revision `126e7fe9eecaafadfe1ac8bb183d135812b608f2` supplies the educational ordering.
The discussion was read for quiz clues (Butanium, fm1randa), surrounding-code/flow analysis
(yudhiesh-oc), renderer reuse (ankitg12), and injection boundaries (ehsan-ami).
The [ankitg12 derivative](https://gist.github.com/ankitg12/8e808d387799de4e9839bc393f8e6405)
was inspected at the 2026-09-19 snapshot, including its `render.py`; no upstream code is copied.
A fixed derivative revision and automated upstream behavior evals remain unverified.

- **keep:** background, intuition, logical walkthrough and understanding checks; these differ
  from a review verdict or a file-by-file diff summary.
- **adapt:** bind claims to immutable source snapshots and version-qualified lines; explain in
  runtime order and separate inferred intent from facts. Keep retrieved material passive.
- **adapt:** content-first rendering and answer-clue checks, with free-response/transfer preferred.
- **omit:** mandatory HTML styling, global temporary output, fixed five-question MCQs, automatic
  browser opening and any bundled upstream renderer. Markdown is sufficient unless otherwise requested.

TigerKit's `tk-explain` covers concept visuals, not old/new source reconstruction.
`tk-review` owns defects and approval, not teaching. Local success and pressure cases in the
repository eval catalog test the new boundary; upstream discussion is rationale, not proof
that TigerKit's implementation passes those cases.
