---
name: tk-blind-comparison
description: "[user/auto] 후보 이름을 가린 블라인드 비교·청취 갤러리를 요청하면 사용합니다. 취향·품질 후보 중 사람이 판단해야 할 때는 실행 전에 갤러리를 제안만 합니다. 단일 변경 QA, 장단점을 공개하는 설계 질문, 자동 지표 비교에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "<candidate/item/output manifest or exported ratings>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# Blind Comparison

## Shared References

Read branch-triggered criteria from the current installed owners. A missing/mismatched
owner or resource blocks that action: use `tk-setup-skills`, not memory, another installation
or unapproved installs. Reading grants no workflow or mutation authority.

- For a user-owned decision, missing approval or unmet prerequisite, read [question rounds](../tk-questioning/references/questions.md).
- Before a user-facing completion report, artifact-path handoff or multi-attribute chat comparison, read [chat delivery](../tk-writing/references/delivery.md). The task's specific output contract wins.

Own human comparison of existing candidates, never candidate generation or an agent's
quality verdict. When a user requests blind comparison, build it. When merely facing
subjective alternatives, propose a blind gallery and wait for acceptance without choosing
or creating files. Single-change checks belong to `tk-qa-sheet`; disclosed tradeoff questions
to `tk-grill`; candidate creation to `tk-prototype`, `tk-tts` or the relevant producer.

1. Confirm the shared comparison question, candidates, items and equivalent source inputs
   from available evidence. Require at least two candidates; preserve failed outputs.
   Read [manifest and commands](references/manifest.md). Keep originals immutable and
   record content revisions: changed outputs need fresh ratings, unchanged outputs retain them.
   Gallery scoring remains the default. For an explicit head-to-head request read
   [versus comparison](references/versus.md); do not force a single winner from a tie.
2. Before writing, apply Artifact Paths. Use `.tigerkit/tmp/tk-blind-comparison/<run-id>/`
   for HTML, display copies and the separate answer key; use
   `.tigerkit/evidence/tk-blind-comparison/<run-id>/` for returned ratings and summaries.
   Honor an explicit destination. Read [HTML output](../tk-writing/references/html-output.md) and inline
   the package theme assets. Keep the gallery interface rather than adding document navigation.
3. Prepare identity-neutral display copies. Read only the applicable
   [audio](references/audio.md), [images and UI captures](references/images.md),
   [text](references/text.md), or [video](references/video.md) reference. For versus HTML,
   prepare identity-neutral self-contained copies under the manifest preview contract.
   Include optional neutral original/mobile links and public annotations under the manifest contract.
   Strip surface identifiers and metadata without erasing the dimension being compared.
   Record transformations and residual cues visibly. A failed normalization remains a
   failed card with a neutral reason; preserve diagnostic details privately in the answer key.
4. Run the bundled builder with the prepared manifest. Reuse the same study ID and previous
   answer key when adding/removing/reordering candidates; create a new output directory.
   Preserve opaque stable candidate IDs, item IDs and content fingerprints. Use seeded
   per-item shuffles and neutral labels disjoint from candidate names. Candidate identity
   must not appear in filenames, DOM IDs, accessibility names, default text or sorting.
   Choose split delivery when requested or justified by the actual transfer/opening environment,
   not an invented size threshold or unverified browser-failure diagnosis. Read the split contract
   in [manifest and commands](references/manifest.md). Distribute only `comparison.zip`, never its
   enclosing output directory: the separate answer key stays private. Default single-versus
   self-evaluation embeds an encoded minimal key; separate-key single and split delivery require
   a matching selected key. Both versus key paths use the same validator and explicit reveal;
   read the manifest contract. Legacy single gallery keeps its behavior.
   Keep an explicit reveal toggle and the selected delivery
   mode's answer-key boundary; offline blinding prevents casual
   cues, not source inspection. Never claim cryptographic or exam security.
   Keep the comparison topic, item title, shared script and evaluation guide visible within
   the active item's sticky context; bound long context height so scoring stays reachable.
5. Verify the saved local HTML through `tk-browser-verify`: desktop/mobile and both themes,
   media decode, original-size/additional links, escaped annotations, all failure cards, keyboard controls,
   and the selected mode's controls. Verify embedded one-click versus results, separate-key
   guidance/file selection, key validation failures and the full replay-derived result table. Gallery checks include native 1-5 scores, notes and optional favorite;
   reload, candidate addition, JSON import/export, rating copy and clipboard refusal,
   partial-reveal confirmation/cancellation, reveal-only averages and storage refusal.
   Copy uses the same blind-key payload as
   export; if clipboard access fails, retain ratings and offer file export.
   For versus also verify round/VS/card-choice layout, long-image inner scrolling, live HTML
   disclosure/step controls and current-pair-only iframe cleanup, odd byes, repeated both-advance,
   later-round co-winner confirmation/cancellation, undo after completion and cross-item replay.
   Open via `file://` without hosting. Single delivery embeds primary media; split delivery must
   work after extracting the ZIP with all neutral assets, without external requests or missing links. Browser `localStorage` on
   local files varies: show save failures and offer JSON backup/import; file relocation or a
   different browser may require importing the previous export. Report unrun checks honestly.
6. Return the local HTML and answer-key paths, revision/counts, transformations, actual checks
   and remaining human evaluation. Publish only on explicit request. Wait for actual ratings;
   never fabricate scores. Read [results](references/results.md) when copied JSON or a JSON export arrives,
   validate against its matching key, aggregate mode-appropriate counts/means or selection transcripts and item tables, and state evaluator
   count, missing scores, failures and sample limitations. Compare available objective metrics
   against low-scoring items without treating subjective means as statistical proof.

No servers, shared database, live multi-rater collection, statistical tests, automatic winner,
source changes, model installation or synthesis. Existing audio/video comparisons do not authorize
new TTS; ask about TTS only if the user separately requests new narration and its choice is unresolved.

## Artifact Paths

Before authorized artifact writes, checkout/transport/ignore setup or temporary-input consumption,
read [artifact paths](../tk-artifacts/references/artifact-paths.md). Use safe owned nonsymlink paths
and proven Git exclusion for repository scratch; failed checks stop that file branch. Preserve
explicit final destinations and owner-specific defaults. Prefilled input is not completed input.
Cleanup targets only recorded literal resolved absolute run-owned paths, never cwd-relative paths or globs.
