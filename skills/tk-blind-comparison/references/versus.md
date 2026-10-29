# Versus comparison

Use only for an explicit head-to-head request. Build with `--mode versus`; choose `single`
or `split` under the [manifest contract](manifest.md). This is a human selection interface,
not a new candidate generator, objective ranking or memory backend. Keep producer identity
and technique-to-sample mappings private even if recommendations and reasons were already
shown. Explain residual style cues. Preference persistence belongs to an explicitly
consented external memory owner, not browser comparison state.

## Interaction and replay

Each item starts in its existing deterministic, seeded opaque-card order. Adjacent surviving
cards form a pair. `왼쪽 진출` or `오른쪽 진출` keeps only that side; `양쪽 진출` keeps both
in the same order. A final odd card is shown alone: acknowledge it with `왼쪽 진출` before
its bye advances. There is no automatic tie breaker, loop that silently reduces ties, or
forced single winner. Repeated both-advance rounds remain pending until a human chooses.

`남은 후보 공동 1위` is available only at the start of a later round after every survivor
has appeared in an acknowledged pair or bye. It requires explicit confirmation and selects
all survivors. After a legitimate round leaves one survivor, that item is complete.
`선택 취소` removes the current item's last event, including final or co-winner selection.
`이전 항목` / `다음 항목` navigate independent transcripts. Both sample cards have bounded,
keyboard-focusable independent scrolling in the remaining viewport height; shared context
remains above them. Guidance is collapsible and progress is not repeated in storage status.
At viewport heights of 560 CSS pixels or less, including zoom/landscape, page scrolling is
an accessibility fallback so controls remain reachable.

Failed outputs stay in the item's failure list, full exported roster and summary counts,
with private diagnostics only in the answer key. They do not enter the bracket. Fewer than
two successful outputs makes an item `incomparable`; it has no winner and accepts no events.
Initial empty events on a comparable item are `pending`, never an inferred winner.

## Export contract

Copy and file export produce the same `blind-versus.json` payload. The existing gallery's
`schema: 1` ratings format is unchanged. A versus payload is distinguished by `mode: "versus"`:

```json
{
  "schema": 1,
  "mode": "versus",
  "study": "opaque-study-digest",
  "version": "1",
  "revision": "comparison-content-digest",
  "evaluator": "browser-evaluator-id",
  "revealed": false,
  "active": 0,
  "items": [
    {
      "id": "opaque-item-token",
      "cards": [
        {"candidate": "opaque-candidate-token", "fingerprint": "content-digest", "failed": false}
      ],
      "events": ["left", "right", "both", "co-winners"]
    }
  ]
}
```

The example shows field shapes, not a valid playable roster/transcript. Real exports include
every item and every card, including failures, in build order. `active` is a zero-based item
index. Events are ordered action literals; a bye accepts only `left`. Do not fabricate events
from a requested outcome. Actual media, candidate names, answer keys and private diagnostics
are excluded. Schema, nonblank evaluator, boolean reveal/failure fields, item/card membership,
order, fingerprints, valid action sequence and completion boundaries are checked before import.
Malformed imports leave current choices and saved bytes unchanged. Recorded exposure is never
reset by undo or an imported `revealed: false`. Existing nonempty choices reject a different
evaluator; imports replace one evaluator's transcript, not merge multiple raters.

`revision` binds study/version, shared title and transformations, item context, seeded roster
order and every output fingerprint. Reuse `--previous-key` for stable opaque identities.
Unlike independent gallery scores, a bracket depends on its entire field: changed content,
context, candidate set/order or version requires fresh choices. Preserve the old export/key
for replay in its exact old build; never silently reuse it against a new revision. Single and
split delivery of the same comparison share a revision.

Reload restores the same revision's choices and active item. Local-file storage remains
browser-dependent. Corrupt/refused storage is not overwritten; live choices remain exportable.
Clipboard failure retains all choices and offers JSON file export. For untrusted replay work,
both browser and summary parser reject more than 100000 events per item without truncating
or discarding the last valid state. This event budget is not a media-size cutoff.

## Summary parser

```bash
python3 <package>/scripts/build_gallery.py summarize blind-versus.json --key <matching-run-directory>/answer-key.json --blind
python3 <package>/scripts/build_gallery.py summarize - --key <matching-run-directory>/answer-key.json --blind
```

The same command recognizes `mode: "versus"`, verifies `key.comparison.revision` and its
full roster, and replays events before producing results. No output directory means stdout
only. `--output <new-evidence-directory>` writes `summary.json` and `summary.md` as before.
The JSON includes `mode`, `revision`, `evaluators: 1`, `revealed`, candidate `wins`, `co_wins`
and `failures`, and per-item `status`, `round`, `events`, `winners`, `winner_names`, `failures`.
Statuses are `complete`, `pending` and `incomparable`. `totals` contains `items`, `complete`,
`pending`, `incomparable`, `failures`, `outputs`; the three item statuses sum to `items`.
A co-win also counts as a win. These counts summarize human actions, not statistical superiority.
Do not compare them as means or pool repeated exports as independent evaluators.
