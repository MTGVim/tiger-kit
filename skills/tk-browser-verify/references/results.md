# Browser Evidence and Results

Read before storing runtime evidence or returning an executed verification phase.

Before the first write under `.tigerkit/evidence/`, verify that
`git ls-files -- .tigerkit/` returns no tracked path and
`git check-ignore -q -- .tigerkit/` succeeds. Record only the matching source class and
pattern from `git check-ignore -v`, redacting an absolute user-level path. Apply [artifact paths](artifact-paths.md)
ignore setup when coverage is missing. If checks still fail, do not write or use an external
fallback; return `Unverifiable`.

Binary evidence may be stored in run-owned `.tigerkit/evidence/tk-browser-verify/<run-id>/`. Baseline comparisons use
`baseline/`, `after/`, and immutable `failed-<attempt>/` subdirectories. A bounded `README.md` may map each
AC to its screenshot, exact publication-safe `display_route`, replay procedure, and disclosed capture-only or
nondeterministic exclusions; it is an evidence index, not a lifecycle ledger.
Do not place other Markdown files there.
Do not move user fixtures. Use sensitive captures as evidence only after verifying redaction and absence of residue.
If any failure appears, whether deterministic, rare, or flaky, preserve its run-owned screenshot, trace, log, or dump
before a rerun that could overwrite or delete it. Keep baseline comparison failures in a new unique `failed-<attempt>/` path,
not the later `after/` path. A later negative sample does not erase the observed failure.

Require these contract fields in nested and standalone results; keep nested results limited to:

- status
- `phase: baseline | after | acceptance`; for a successful pre-edit baseline also return `baseline_capture: Pass`,
  `verification_complete: false`, `run_id`, `replay_procedure`, and the exact `next_required`; include
  `resume_parent: required` when the active parent has approved implementation remaining
- `visual_contract: applied | n/a`; `n/a` requires a reason proving no visual-reference, baseline/after,
  multi-capture, visual/responsive, or render-affecting branch applies
- `capture_only_mutation: <description> | none`, also in the evidence index; include outlines/labels,
  hiding/removal, and runtime mocks, or explicitly `none` when no capture-only mutation occurred
- Facts per criterion
- non-sensitive auth mode
- absolute evidence directory
- baseline provenance and replay procedure when a visual pair is required
- one ordered row per inspected screenshot with its path, exact origin-free `display_route` or explicit omission,
  criterion, state/region, `capture_method`, effective viewport, role, and comparison result; otherwise the direct trace/a11y/DOM/runtime/request evidence
- the same per-capture method/effective viewport in the evidence index, including reason and effect for exceptions
- limitation
- cleanup fact
- `automated_regression: protected | N/A | exception | unknown` as supplied/verified parent disposition

Missing required identity/provenance or return metadata makes the phase `Unverifiable`, even when a screenshot
was inspected. Report the missing fields and collect them before returning phase `Pass`; a limitation note
or `verification_complete: false` does not waive the required evidence contract.

A successful pre-edit baseline proves only that the reference capture exists. Return
`next_required: implement candidate, then capture after with the same run/replay`; do not use aggregate completion wording.
For nested results, use the phase fields without a standalone `## Verdict` or user-facing completion summary;
`status: Pass` describes only the requested phase. `resume_parent` is an instruction to the owner, not a scheduler signal.
When the user requested only standalone capture, finish that bounded request without inventing a parent or implementation approval.
Only the matching after comparison or standalone acceptance phase may set `verification_complete: true` when every
criterion is covered. An after result binds the same `run_id`, `baseline_provenance`, and `replay_procedure`. A
baseline-only result cannot satisfy final acceptance or authorize product edits, commits, or publication by itself.

When an inspected image is required for PR publication and its represented criterion is `Pass`, return the
producer-neutral manifest from [publication evidence](publication-evidence.md); do not upload it. Direct
trace, accessibility-tree, DOM/runtime, and request/response evidence remains in the ordinary verifier result and does
not trigger the image uploader. If a parent specifically requires an image that cannot directly prove the criterion, do
not create a ceremonial screenshot; return the image-publication requirement as `Blocked | Unverifiable`. For any
non-`Pass` criterion, preserve owned failure evidence, return its real status, and never emit a `verification_status:
Pass` manifest entry for it.

A standalone result, with no active owner task to resume, starts with `## Verdict` and exact `Status: <token>`, then shows verified facts, required limitations, evidence paths, and the cleanup fact. Standalone baseline success remains capture-only with `verification_complete: false`.
Never promote a result to `Pass` without required runtime evidence.

| Status | Meaning |
| --- | --- |
| `Pass` | Current inspected evidence covers every approved browser criterion |
| `Fail` | Current runtime evidence violates a criterion |
| `Blocked` | A user-owned safety or target decision is required before execution |
| `Unverifiable` | Required headless auth, environment, or evidence cannot be established |

Do not cause unauthorized payments, external communications, destructive mutations, production-data mutations, or account/permission changes.

