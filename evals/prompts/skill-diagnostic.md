After producing the normal deliverable, append exactly one diagnostic record.
Do not change or replace the normal deliverable.

Do not guess an expected answer. Report only what happened while following the
target skill. Empty issue and fill-in arrays are valid.

For every trace field, choose exactly one state: `ok`, `stuck`, or `skipped`.
The example uses `ok`; replace it only when that phase actually became stuck or
was skipped.

<!-- TIGERKIT_DIAGNOSTIC_START -->
```json
{
  "trace": {
    "understanding": "ok",
    "planning": "ok",
    "execution": "ok",
    "formatting": "ok"
  },
  "unclear_points": [
    {
      "issue": "observed event",
      "cause": "instruction-level cause",
      "general_fix_rule": "class-level prevention rule"
    }
  ],
  "discretionary_fill_ins": [],
  "retries": 0
}
```
<!-- TIGERKIT_DIAGNOSTIC_END -->
