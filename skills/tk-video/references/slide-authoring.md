# Author explanatory slides

Re-author the explanation for listening and brief viewing; do not crop a document's long panels
into cards. Use one message per narration sentence/beat, splitting dense scenes instead of
shrinking text. Prefer a 1920x1080 canvas with large text (typically at least 40px for primary
copy) and reserve the lower 15-20% for selected captions/player controls. Inspect at actual viewing
size; these are authoring starting points, not proof of readability. Keep material caveats legible.

Follow the resolved `slideTheme`; absent a selected/saved value, recommend light and resolve it in
the first media round. Use that light fallback when authorized to choose defaults. Inside slides,
change only the currently narrated element's highlight, outline or marker. Keep both sides of a
comparison identifiable from the first frame: if the narration says “look at B rather than A”,
show and label A and B before emphasizing B; do not initially blur/fade A into apparent absence.
Default assembler `highlights.zoom` to off for authored slides. Actual captured UI retains its
selected highlight/crop/zoom treatment; an explicit slide zoom is a selected exception.

## Check all authored copy before rendering

Collect every scene's title, body, labels, callouts, source tag, caption and corresponding narration
in one scene-copy list. Read it across scenes before the first render, using these adapted
clear-writing/reader-formatting criteria:

- Use concrete subjects and the reader's vocabulary; preserve facts, conditions, units and caveats.
- Finish explanatory statements and scope notes with a predicate and sentence ending. Meaningful
  short noun labels are allowed; dangling explanatory fragments such as `어떻게 달라지는지`,
  `판단하기 쉬움` or `판단하지 않음` need the missing statement, for example
  `어떻게 달라지는지 보여 줍니다`, `쉽게 판단할 수 있습니다` or `이 자료만으로는 판단하지 않습니다`.
  Choose the correction supported by the source, not a mechanical suffix replacement.
- Keep one register across scenes and match narration in terminology, claim strength and meaning.
  Source/UI literals and deliberately short labels retain their exact form. Narration may verbalize
  notation differently while conveying the same fact; do not force captions to mimic TTS spelling.
- Name comparison subjects explicitly and compare one attribute at a time. Remove redundant badges;
  reserve positive badge tones for supported positive facts.

Record the scene-copy list, checked source/candidate identity and findings/fixes or no-change
result in the inspection evidence. After edits, recheck affected copy and its cross-scene register.
Then render and inspect actual frames for clipping, reading size, safe region, comparison visibility,
source tags and alignment with narration. Retain that result in the same inspection record.
A text check is not factual independent review, decoded-frame inspection or listening approval.
