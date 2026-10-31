# QA Sheet Data and Rendering

Read for the default HTML sheet or an explicitly requested HTML sheet. Copy the bundled template, replace the
`script#qa-data` JSON, then use the bundled helper to regenerate its static reading
inventory from that data. The final file needs no external assets or runtime generator.

## Authoring and inspection contract

Use this map without searching the template implementation. Keep its runtime renderer,
styles and control wiring unchanged. These selectors inspect the generated sheet, not the
product being checked; a match alone does not prove a passing runtime result.

| Purpose | Contract or selector |
| --- | --- |
| Editable data | Replace only the JSON text in `script#qa-data` using a serializer and the escaping rule below. |
| Browser tab title | Set JSON `title`; runtime sets `document.title` and `#title` from it. The static HTML `<title>` may also match that plain-text title with HTML escaping; do not edit renderer code. |
| No-JS inventory | Regenerate `noscript#qa-static` with `scripts/render_static_inventory.py`; do not hand-edit it. |
| Rendered heading and inventory | `#title`, `#main`; compare rendered text and row coverage with the final JSON. |
| Editable checks | `#main li.check input[type="checkbox"]:not(:disabled)`; generated `data-id` values own persistence identity. |
| Automated checks | `#main input[data-auto="true"]`; require checked and disabled state, including after reset. |
| Unverified automatic criteria | `#main li.verification-gap`; require visible direction text and no checkbox. |
| Filter and reset | `#onlyOpen`, `#reset`; inspect behavior as required below. |
| Notes and save status | `#notes`, `#saved`; reload to test restoration rather than trusting a status label. |
| Count and storage failure | `#count`, `#storage-warning`; verify counts against data and warning behavior when storage is denied. |

Reuse these selectors as lookup points, not a new mandatory checklist; the existing self-check
below owns required scenarios. A selector mismatch requires inspecting the installed template
version rather than inventing a replacement contract.

## Data

```json
{
  "title": "Task QA",
  "storageKey": "task-topic",
  "head": "abc123",
  "environment": {"label": "Local QA", "baseUrl": "http://localhost:3000"},
  "legend": ["Scope, evidence rules and unresolved screens"],
  "groups": [
    {
      "title": "Area",
      "items": [
        {
          "title": "Observed screen hierarchy or known route",
          "provenance": "observed",
          "url": "http://localhost:3000/orders",
          "notes": ["Shared pattern or missing connection"],
          "checks": [
            {
              "criterionId": "UI-001",
              "text": "Observed trigger and expected behavior",
              "provenance": "observed",
              "verification": "auto-verified",
              "evidence": {"ref": "browser-run-123", "head": "abc123"},
              "indent": 0
            },
            {
              "criterionId": "UI-002",
              "text": "Only the unexercised branch remains",
              "provenance": "observed",
              "verification": "partial",
              "evidence": {"ref": ".tigerkit/evidence/tk-browser-verify/run-123", "head": "abc123"},
              "indent": 1
            },
            {"text": "Source-only trigger and expected behavior", "provenance": "code-only", "indent": 1},
            {"text": "Subheading", "heading": true}
          ]
        },
        {"title": "A screen check without children", "provenance": "code-only"}
      ]
    }
  ]
}
```

New sheets require a nonblank top-level `head` for the candidate whose impact inventory they
represent. The renderer accepts a missing `head` only for older sheets; a browser verifier
must treat that lineage as unknown and reconcile it before runtime. Require nonblank `title`,
`storageKey`, group/item titles and check texts. Require a
nonempty `groups` array and nonempty `items`; optional `legend`/`notes` are string arrays.
`checks` absent or empty makes the item itself a check. `heading: true` creates no checkbox;
require at least one real check per item. `indent` is an integer from 0 to 3.

`provenance` is `observed | code-only`; missing values default to `code-only`.
A child is observed only if both its parent and the child are explicitly observed.
An unsupported ancestor prevents the full check from becoming an observed navigation claim.
Use backticks only for exact observed UI labels; source-only labels use plain text even
when the source contains an exact string. Known routes may appear
in code formatting as technical literals; disclose their status separately from navigation.
List user-provided text and missing click connections explicitly in notes/legend/limitations.

Every new check row has a stable `criterionId`: keep the impact-inventory/browser-verifier ID unchanged, or assign `QA-001`, `QA-002`, ... after splitting entry points when none was supplied. Preserve those IDs when regenerating the same task; IDs must be unique across the sheet. The renderer accepts omitted IDs only for older sheets. A `verification-gap` row must have an ID so a no-argument verifier run can target and return it. The renderer displays it beside the row. Its generated checkbox ID remains separate and content-bound.

When consuming a verifier row map, copy `evidence_ref` to `evidence.ref` and `head` unchanged. Map `Pass` and `covered-by:<criterion_id>` to `auto-verified` only with the mapped evidence on that row ID; retain the equivalence rationale for `covered-by`. Keep `Fail` as `failed` on the same criterion. An authorized `out-of-scope` or `not-executed` row without a proven manual blocker becomes `verification-gap`; a proven blocker becomes `manual` with `reason` mapped to `manualReason`, `search_scope` to `searchScope`, and the concrete `unblock`.

`verification` is `manual | verification-gap | auto-verified | partial | failed`; missing values default to `manual` for older sheets. Use `verification-gap` for an unexecuted row that is within established authority and has no recorded execution, no recorded `searchScope`, and no verified capability gap. This state has no automated evidence and is displayed separately without an editable checkbox. It is not a human task.
It applies to a standalone item or a non-heading child check and is independent from
`provenance`. Items that contain child checks do not carry their own verification state.
`auto-verified`, `partial`, and `failed` rows require an `evidence` object with nonblank `ref`
and `head`: `ref` is the run ID or evidence path, and `head` is the commit head that
evidence was bound to. Manual rows omit `evidence`. For every newly authored human-only `manual` row,
set `manualReason` to `unauthorized-or-irreversible`, `data-unavailable-after-search`, or
`verified-capability-gap`, and set `unblock` to its concrete next step. The latter two
reasons require a nonblank `searchScope` describing the recorded search or attempted
capability check. Missing/irreversible write authority is the only reason to exclude a write
before an attempt. If a user explicitly asks for a human checklist, a gap may instead be an
editable `manual` row with `automatable: true`; this is an explicit checklist exception and
does not claim a human-only blocker. For backwards compatibility, the renderer
accepts older manual rows with no `manualReason`, but new skill output must provide one.
A manual row that was demoted because a
later diff affected its screen may instead carry `previousEvidence` with the same `ref` and
`head` shape. Never-exercised manual rows omit both fields, and `previousEvidence` never
promotes a row to automatic verification.

Set a verifier `Fail` row to `failed` without splitting it into a passed part and a manual
remainder. Preserve the verifier evidence in `evidence`; the row remains in the editable manual
list so a person can record a follow-up check, while the `failed` result and its evidence remain
visible. A manual checkbox does not rewrite the verifier result.

Use `auto-verified` only for run-owned automated runtime evidence that exercised the same
screen, entry path, trigger and expected result. Normally that evidence is on the current head.
When the target head moves, inspect the diff from the evidence head to the current head. Treat a
row as affected only when the diff touches that screen's render path or request path. If those
paths are unchanged, the old evidence may remain `auto-verified`; keep its original head and
report the path-based carry-forward rationale. If the row is affected, prefer recapturing it on
the current head while the runtime session remains available. Otherwise demote it to `manual`
and move the old run to `previousEvidence`. Evidence from another screen or entry path is
`partial`; rewrite that row so its text describes only the unexercised part. Unit tests alone
do not promote a screen check. A data-changing check may be `auto-verified` when its exact
mutation was explicitly authorized and actually executed, and run-owned runtime evidence bound to
the current head proves the same screen, entry path, trigger, operation, and expected saved result
through an independent reread. Request-body capture without backend submission can auto-verify only
the payload-construction check, never a saved-result check. Preserve evidence `ref` and `head`; the
label records verification evidence and is not product acceptance. If authority or current-head
evidence is missing, keep the data-changing result `manual`.

The HTML renderer places `auto-verified` rows in a collapsed `Automated` group as checked,
disabled controls with their evidence reference. `verification-gap` rows appear in a separate
visible `자동 검증 필요` section without checkboxes, with a direction to run
`/tk-browser-verify` without arguments and then regenerate the sheet. `partial`, `failed`, and
`manual` rows remain editable in the manual list; `partial` and `failed` rows show current
evidence, while head-demoted manual rows show `previousEvidence` with an explicit previous-head
label. A `failed` row stays on that same criterion; a manual checkbox records follow-up work
without changing the failed result.

## Screen links

`environment` is optional; when supplied require nonblank `label` and an absolute HTTP(S)
`baseUrl` without URL credentials. Optional item `url` is an absolute HTTP(S) landing URL
in that environment's origin; links require `environment`. The template shows the named
environment and a separate `화면 열기` link without toggling the checklist. Links open a new
tab with `noopener noreferrer` and no referrer. Keep links outside quoted UI text.

Prefer a supported detail/section URL when the actual target ID and route/query/fragment
are verified. If the ID is unavailable, use the known list URL and describe record selection
as a manual check. Reuse the exact supported landing URL; do not invent an ID, fragment,
host/port, or hash-router path. Unknown environment or landing route means omit the link
and report the limitation. A link derived from known route/base evidence does not prove
a clicked navigation connection. Preserve `code-only` status for unobserved labels.
The producer must exclude secret-bearing/signed URLs and sensitive personal data;
structural URL validation alone cannot establish publication safety.

Serialize JSON with a real serializer, then replace every `<` with the JSON escape
`\u003c` before embedding. This prevents `</script>` and HTML comment sequences from
terminating the data block; HTML escaping JSON or manual string interpolation is unsafe.
Verify parsing of the final embedded block and absence of sample task/area/trigger content.

## Identity and persistence

The check ID encodes the full JSON-serialized tuple of environment base URL, landing URL, group
title, item title and child check text (or null for a standalone item). Tuple boundaries
distinguish delimiter-containing labels and standalone/child checks. Changed environments
or record links cannot reuse a previous check's completion. Full tuple encoding avoids
short-hash aliases across regenerations. Identical tuples are rejected visibly before rendering; disambiguate genuinely separate
checks with accurate contextual text rather than order-dependent IDs. Reordering identical
content preserves IDs; changed text creates a new ID. Explain that limitation when rewriting
an existing sheet. Reuse `storageKey` only for the same task and environment; a new task,
environment or independently tested revision uses a new key for notes/filter as well.

Storage keys serialize `["tk-qa-sheet", storageKey, role, 1]` as JSON, with role `checks`,
`notes`, or `onlyOpen`. Keeping task and role as separate tuple fields prevents one task's
name from aliasing another task's note/check key. Theme is intentionally outside task
identity: the canonical shared theme control stores the raw `system | light | dark` value
under `tigerkit-html-theme`, independent of `storageKey`. This lets the reader's explicit
browser preference carry to other TigerKit HTML outputs that share the same browser/localStorage
origin. The generated default comes separately from the shared user `settings.json` contract in
`../../tk-writing/references/html-output.md`; a stored reader preference overrides that default at runtime. Do not
promise cross-file persistence for `file:` URLs or across browsers because storage scoping is
browser-defined there. Missing, invalid or unreadable theme storage starts in `system`;
changing theme can still update the current page if a write is refused, but a reload may
return to `system`. Check reset never clears the theme preference.

Reads/writes tolerate unavailable storage and malformed stored data. Auto-verified rows are
not persisted as user completion: the renderer clears any old stored completion for an item
while it is auto-verified, so a later demotion to manual cannot resurrect a stale manual
check. Failed writes display a warning without preventing in-memory interaction. Notes save after
400 ms and flush on page exit. Reset confirms before clearing checks and preserves notes.
Storage is local to the browser/profile and file/origin; moving the file or changing browser
may lose access to existing state. Do not promise cross-file or multi-user persistence.

## Self-check

After filling `qa-data`, run the package's `scripts/render_static_inventory.py` on the generated
file. It replaces only `noscript#qa-static` from that same JSON, escaping prose and preserving
the runtime renderer. Regenerate it whenever data changes; never maintain a second inventory.
With JavaScript disabled, verify the final groups/items/checks are readable and controls are
not presented as functional. Persistence remains a JavaScript-only capability, disclosed in
the static view. Compare static coverage with the final JSON, not the bundled example.

Use `tk-browser-verify` with the exact generated file, no auth/server, a disposable
headless profile, and all mandatory [HTML output](../../tk-writing/references/html-output.md) render checks, plus any
requested layout criteria. Every short sheet still needs desktop/mobile and light/dark coverage
with numerical readability checks and inspected/missing-check reporting. Verify the visible
segmented theme radios are ordered `system / light / dark`: `system` leaves `data-theme` unset and
follows emulated light/dark OS preference, while manual light/dark choices override it and
restore after reload when storage is available. Confirm check reset preserves the theme and
storage refusal leaves the sheet readable with `system` as the next-load fallback. When at
least two editable rows exist, verify that two rows plus a note survive reload. With fewer
than two editable rows, verify note persistence and `auto-verified` immutability instead, and
report the editable-row check as `not applicable`. IDs must be unique, counts accurate, code-only
status visible, reset must retain the note, auto-verified rows must stay checked after reset
without becoming editable, partial/manual rows must remain in the manual list, and
`verification-gap` rows must appear outside it without checkboxes. The gap direction must be
visible in both interactive and no-JS views. Verify
evidence references and the collapsed Automated grouping from the final data, not just the
bundled sample. Preserve actual
failure/limitation evidence; remove only the run-owned profile. Storage-denied environments
render normally but cannot satisfy persistence acceptance.
