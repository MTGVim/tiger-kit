# Selected Narration Alignment

`tk-tts` owns local synthesis, model/runtime pins, installation/cache and audio inspection.
Invoke it after the creator has selected TTS; pass resolved parent voice/engine decisions and
pronunciation-corrected script without asking again. Resolve voice per field from current
explicit request, repository personal preference, user settings, team settings, then sohee.
A voice preference never selects narration itself. Use ordinary returned WAV paths and measured
durations; do not import sibling Python or install a second engine in tk-video. Supplied
sufficient original narration can be reused. Keep captions faithful to original UI literals.

Retain human_action: listen with actual sample paths and terms/numbers/endings to check until
heard. Decode and non-silence are not pronunciation proof. Do not add ASR, automatic engine
fallback or browser speech as an exported-audio route. No-narration MP4/GIF remains usable
without tk-tts or inference dependencies. Installation/download authority stays with tk-tts.

## Fit narration to scenes

For `explainer`, attach frame `audio_path`; measured speech determines presentation holds.
For `evidence`, retain actual timestamps. When an authorized non-mutating scenario is too short,
synthesize each scene first and measure the trimmed WAV. Give the capture owner minimum scene
holds of measured duration plus a small pause; recapture the same scenario and receive its actual
scene starts, final end and final-state facts. Mark deliberate narration-paced waits explicitly;
they are not application latency evidence. Do not stretch old captures or rerun mutating flows.
If safe recapture is unavailable, keep captions and disclose omitted/undelivered narration; do not
silently claim that an explicitly selected voice was delivered.

Pass `scenes: [{start_ms, audio_path}]` in the evidence manifest, using observed scene boundaries,
or an already prepared whole track with `--audio`. The assembler places scene WAVs and silence
without shell-authored filter graphs; clips cannot overlap the next scene or movie end. Never mix
scene audio with a full track, truncate speech or guess duration from character count.

For narrated evidence, plan sentence-level beats with start/end and `cue_targets` in the
capture handoff. At each beat start clear previous marks and show only the targets named in
that sentence. Match explicit quantities to all corresponding targets; state separate group
counts and distinguish groups with colors and labels. Preserve UI labels verbatim, separate
from narration. For disappearance, mark the target before the action and show a hidden/deleted
badge at its prior location only after runtime confirms the state. Verify counts and target
visibility at the beat end; record the evidence and any unresolved mismatch.

When selected, put short callouts beside the cue at that beat, using measured source-frame
coordinates and observed times from the capture handoff. Add facts the narration omits (item
names or the condition/result relationship); avoid repeating the caption sentence. Keep callouts
clear of targets. Pass all simultaneously named rectangles together for zoom planning, including
groups in different parts of the screen; never start a zoom before the targets actually appear.
See [assembly](assembly.md) for optional presentation fields and collision checks.

## Teaching handoff

For continuous `animation`, keep the measured render timeline. Reuse `scenes` offsets or a full
WAV only when no embedded audio exists; ambiguous mixed audio fails instead of silently replacing
the render's sound. Prepare screen/caption literals separately from pronunciation-corrected
spoken text, preserving numeric values and technical identity. A script review is not listening.
If speech exceeds a scene, re-author/rerender that scene; never stretch the video or truncate audio.

When a teaching caller supplies a sequence, retain its accepted scene point, observed start
state, action/change, deciding visual and explanation. Reuse its already-refined script and
settled audio choice. Missing causal steps return to the teaching author before assembly; a
contact sheet, codec check or subtitle coverage does not validate the explanation. Browser Web
Speech API playback does not provide a file track: a narrated movie requires supplied or
synthesized file audio under the parent's resolved choice. Do not silently synthesize it.
