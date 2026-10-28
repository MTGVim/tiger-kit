# Accuracy review rubric

Read this entire rubric. Review the exact saved artifact, extracted visible text including
image alt text, figures/captures and pinned evidence. Receive the reader's goal, knowledge,
constraints and supplied examples, not the author's intended verdict. Inspect actual content
and any revealed answers; a successful renderer or attractive figure is not correctness.

| Code | Meaning | Check |
| --- | --- | --- |
| H | Hallucination or unsupported claim | Evidence supports the actual assertion and version. |
| B | Behavior or causal error | Calls, conditions, state, invariants and outcomes match sources. |
| O | Omitted prerequisite/condition | The reader can follow the mechanism or first action. |
| N | Name, number or notation error | Terms, units, labels and quantities are grounded. |
| V | Visual/content mismatch | Geometry, arrows, positions and exercise inputs teach the same claim. |
| P | Presentation issue | Readability, contrast or density; distinguish meaning loss from preference. |
| R | Renderer-owned constraint | Fixed chrome, locale fallback or supported-format limitation. |

Use `high` for a materially wrong conclusion/action, `medium` for a misleading step or
important missing condition, `low` for a localized factual error, and `suspect` when evidence
cannot yet decide. Severity never exempts a supported H/B/O/N/V error from correction.
Classify by consequence, not symbol intuition: a wrong author-drawn label is N/V, while
immutable renderer UI is R. Do not count fixed renderer wording as an authored content error.
A P/R limitation that makes required content unreadable still prevents successful delivery;
an incidental untranslated control can be disclosed without inventing a factual defect.

For follow-up pages, judge each learner belief and its reasoning separately. A correct result
with a wrong reason is not mastery; missing reasoning is unobserved. Verify whether the page
corrects the supported common misconception and provides necessary conditions and a new
transfer case. Do not infer learning from reading, agreement or revealing an answer.

Return:

```text
artifact path + SHA-256 / evidence snapshot:
verdict: Pass | Fail | Unverifiable
location | code | severity | taught claim | evidence | reader consequence | minimum correction
renderer-owned limitations:
```

Fix all supported content findings, including low ones. Investigate suspect findings or
retain `Unverifiable`. High/medium/suspect corrections return to the same reviewer for changed
scope, then one whole-artifact check. Verify low corrections against evidence and final bytes.
Preserve unaffected titles, labels and register; review is not a Korean rewriting pass.
Bound repair to three rounds; unresolved findings end as `Fail | Unverifiable`, not silent
acceptance. An unavailable independent reviewer cannot be replaced by author self-approval.
