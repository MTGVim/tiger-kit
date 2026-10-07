# QA Sheet Data and Rendering

Read for the default HTML sheet or an explicitly requested HTML sheet. Copy the bundled template, replace the
`script#qa-data` JSON, then use the bundled helper to regenerate its static reading
inventory from that data. The final file needs no external assets or runtime generator.

## Data

```json
{
  "title": "Task QA",
  "storageKey": "task-topic",
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
              "text": "Observed trigger and expected behavior",
              "provenance": "observed",
              "verification": "auto-verified",
              "evidence": {"ref": "browser-run-123", "head": "abc123"},
              "indent": 0
            },
            {
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

Require nonblank `title`, `storageKey`, group/item titles and check texts. Require a
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

`verification` is `manual | auto-verified | partial`; missing values default to `manual`.
It applies to a standalone item or a non-heading child check and is independent from
`provenance`. Items that contain child checks do not carry their own verification state.
`auto-verified` and `partial` rows require an `evidence` object with nonblank `ref`
and `head`: `ref` is the run ID or evidence path, and `head` is the commit head that
evidence was bound to. Manual rows omit `evidence`.

Use `auto-verified` only for run-owned automated runtime evidence on the current head that
exercised the same screen, entry path, trigger and expected result. Evidence from another
screen or entry path is `partial`; rewrite that row so its text describes only the
unexercised part. Unit tests alone do not promote a screen check, data-changing checks stay
`manual`, and a moved head demotes affected rows to `manual`. The HTML renderer places
`auto-verified` rows in a collapsed `Automated` group as checked, disabled controls with
their evidence reference. `partial` and `manual` rows remain editable in the manual list;
`partial` rows also show their evidence reference. Neither state is product acceptance.

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
name from aliasing another task's note/check key. Reads/writes tolerate unavailable storage and malformed stored data. Auto-verified rows are
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
headless profile, and all mandatory [HTML output](html-output.md) render checks, plus any
requested layout criteria. Every short sheet still needs desktop/mobile and light/dark coverage
with numerical readability checks and inspected/missing-check reporting. Two editable rows plus a note
must survive reload; IDs must be unique, counts accurate, code-only status visible, reset
must retain the note, auto-verified rows must stay checked after reset without becoming
editable, and partial/manual rows must remain in the manual list. Verify evidence references
and the collapsed Automated grouping from the final data, not just the bundled sample. Preserve actual
failure/limitation evidence; remove only the run-owned profile. Storage-denied environments
render normally but cannot satisfy persistence acceptance.
