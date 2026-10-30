# Browser Evidence and Results

Read before storing runtime evidence or returning an executed verification phase.

Before the first write under `.tigerkit/evidence/`, verify that
`git ls-files -- .tigerkit/` returns no tracked path and
`git check-ignore -q -- .tigerkit/` succeeds. Record only the matching source class and
pattern from `git check-ignore -v`, redacting an absolute user-level path. Apply [artifact paths](artifact-paths.md)
ignore setup when coverage is missing. If checks still fail, do not write or use an external
fallback; return `Unverifiable`.

Binary evidence may be stored in run-owned `.tigerkit/evidence/tk-browser-verify/<run-id>/`. Baseline comparisons use
`baseline/`, `after/`, and immutable `failed-<attempt>/` subdirectories. The required bounded `README.md` maps each
AC to its screenshot, exact publication-safe `display_route`, replay procedure, and disclosed capture-only or
nondeterministic exclusions; it is an evidence index, not a lifecycle ledger.
Do not place other Markdown files there.
An explicitly requested [contact sheet](contact-sheet.md) may add derived PNGs and tile-to-original
links to this same README. Record generation skips there without changing verification status.
Do not move user fixtures. Use sensitive captures as evidence only after verifying redaction and absence of residue.
If any failure appears, whether deterministic, rare, or flaky, preserve its run-owned screenshot, trace, log, or dump
before a rerun that could overwrite or delete it. Keep baseline comparison failures in a new unique `failed-<attempt>/` path,
not the later `after/` path. A later negative sample does not erase the observed failure.

Require these contract fields in nested and standalone results; keep nested results limited to:

- status
- `contract: <metadata.tigerkit.version>`; the current contract is `1.2.0`
- `scope: full-inventory | explicitly-scoped`; when scoped, identify the user's exact scope
- `coverage: planned <N> / executed <n> / covered-by <c> / out-of-scope <o> / not-executed <m>`; the counts must reconcile to the full discovered inventory
- `human_action: none | <N> (criterion IDs, reason and next action)`; nested returns use `none` when the parent owns all remaining work
- `phase: baseline | after | acceptance`; for a successful pre-edit baseline also return `baseline_capture: Pass`,
  `verification_complete: false`, `run_id`, `replay_procedure`, and the exact `next_required`; include
  `resume_parent: required` when the active parent has approved implementation remaining
- `visual_contract: applied | n/a`; `n/a` requires a reason proving no visual-reference, baseline/after,
  multi-capture, visual/responsive, or render-affecting branch applies
- `capture_only_mutation: <description> | none`, also in the evidence index; include outlines/labels,
  hiding/removal, and runtime mocks, or explicitly `none` when no capture-only mutation occurred
- one fact row per approved criterion with `criterion_id`, `result`, `route`, `entry`, `trigger`, `operation: read | create | update`, `input`, `evidence_kind`, `evidence_ref`, and `head`
- use `result: out-of-scope` for inventory rows omitted only by explicit user scope; keep their IDs and scope reason in the full row map
- use `result: covered-by:<criterion_id>` for covered rows, with the referenced row's `evidence_ref` and `head`; preserve the equivalence rationale in the full row map
- `input: trusted | synthetic(<reason>) | not-run`; product interaction cannot Pass on synthetic input. Synthetic evidence is allowed only when the criterion itself permits a non-interaction probe
- `evidence_kind`: one or more of `blocked-intercept | request+response | reread-runtime | reread-image | visual-pair | trace | accessibility | dom-runtime | none`; use `none` and `evidence_ref: none` when no attempt produced evidence
- for every `create` or `update` row, `Pass` requires `reread-runtime` on the same screen and field. If `reread-image` is used, the inspected image must show the field being judged
- for every unexecuted row: `reason`, `search_scope` (page, filters, data conditions or the exact preflight boundary), and `unblock` (the concrete step that would permit execution)
- non-sensitive auth mode
- absolute evidence directory
- baseline provenance and replay procedure when a visual pair is required
- one ordered row per inspected screenshot with its path, exact origin-free `display_route` or explicit omission,
  criterion, state/region, `capture_method`, effective viewport, role, and comparison result; otherwise the direct trace/a11y/DOM/runtime/request evidence
- the same per-capture method/effective viewport in the evidence index, including reason and effect for exceptions
- per visual capture, `annotation: visible (pixel-checked) | none (remain unchanged) | none (target absent by intent)`
  for the target outline, and `target in frame: yes | no`; an absent target needs its appear/disappear intent and visible surrounding context
- for sensitive screens, the capture plan's sensitive region and pre-capture clip/mask; never retain a full-page/raw original
- limitation
- cleanup fact, including exact run-owned server/browser shutdown, recorded launch PID/handle and confirmed exit and any verified residue; no baseline-to-final-head process hold
- `automated_regression: protected | N/A | exception | unknown` as supplied/verified parent disposition

Use the parent-provided or discovered inventory row ID verbatim as `criterion_id`. For direct calls without IDs, assign `BV-001`, `BV-002`, ... once in inventory order and preserve that mapping across retries and phases. A standalone no-argument or scope-only call discovers and reconciles the full same-task inventory before runtime startup; explicit narrowing records excluded rows as `out-of-scope`. `tk-prep` assigns IDs before handoff. Keep the same ID in the QA sheet's `criterionId`; map `evidence_ref` to the sheet's `evidence.ref`, and copy `head` unchanged. Never create a second criterion for a failed part of one row.

When runtime evidence exists, maintain one bounded run-owned `README.md` as the evidence index and canonical full row map. Include each row's full fields above, detailed facts, capture mapping and any non-executed-row details. A standalone chat result may show only the compact row summary below and substitute the README's complete absolute path for the full map. Do not add other Markdown files to the evidence directory.

For a baseline/after comparison, use one compact row per scene:
`scene | baseline observed value | after observed value | verdict`. Read observed values from
the DOM/runtime at capture time; use exactly that phase's observed-value text as its capture
label, preserving required redaction. Use `match`, `intended change` or `pre-existing issue` only
when supported; report `regression` or `unverifiable` for an unexpected change or missing evidence.
These scene descriptions never replace criterion statuses or turn a pre-existing issue into `Pass`.
Pixel-check labels even when the intent requires no target outline; disclose labels in
`capture_only_mutation`. A capture whose criterion target is out of frame cannot support that
visual criterion, even when DOM evidence exists. For appear/disappear's absent side, prove the
expected absence in the visible surrounding context rather than inventing an off-screen target.

An optional HTML gallery or contact sheet is a derived view and never replaces the required
`README.md` or inspection of originals. Return absolute evidence paths; do not open files,
galleries or pages in the user's own browser or through a desktop opener unless the user
explicitly asks. This does not prevent the run-owned headless capture/replay required by verification.

A successful baseline is intermediate evidence, never acceptance. The verifier must release
its owned server, context and browser before returning phase evidence to the parent. A later
final-head replay uses new run-owned runtime resources and the saved baseline/replay conditions;
the parent must preserve evidence provenance, not PID or live browser handles.

Missing required identity/provenance or return metadata makes the phase `Unverifiable`, even when a screenshot
was inspected. Report the missing fields and collect them before returning phase `Pass`; a limitation note
or `verification_complete: false` does not waive the required evidence contract.

A successful pre-edit baseline proves only that the reference capture exists. Return
`next_required: implement candidate, then start fresh runtime resources and capture after with the saved baseline/replay`; do not use aggregate completion wording.
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

A standalone result, with no active owner task to resume, starts with required `## Verdict` and
exact `Status: <token>`. Preserve the contract, head/environment identity, scope and coverage
counts. Summarize actual verification, material limits, cleanup or residue and outstanding user
actions without empty sections. Keep the complete criterion row map in the evidence README.

For each unexecuted row, put its reason, `search_scope`, and `unblock` in the full map, and include
its ID and next action when the user must act. Preserve any owning contract's exact status footer.
Standalone baseline success remains capture-only with `verification_complete: false`.
Never promote a result to `Pass` without required runtime evidence.

| Status | Meaning |
| --- | --- |
| `Pass` | Current inspected evidence covers every approved browser criterion; if `scope` is `explicitly-scoped`, this is not a full-inventory pass |
| `Fail` | Current runtime evidence violates a criterion |
| `Blocked` | A user-owned safety or target decision is required before execution |
| `Unverifiable` | Required headless auth, environment, or evidence cannot be established |

Do not cause unauthorized payments, external communications, destructive mutations, production-data mutations, or account/permission changes.

