# Narration loudness postprocessing

After selected synthesis and validation, normalize a course/video's sentence-clip batch before
handing ordinary WAVs to its owner. Keep engine choice and raw outputs; do not overwrite sources
or normalize the same output repeatedly. Use one consistent batch target, then listen across
adjacent clips for joins, clipping and unexpected emphasis. A normalized waveform does not prove
pronunciation, natural prosody or equal perceived loudness for every utterance.

Run the packaged helper with explicit source paths and a new safe output directory:

```bash
python3 scripts/normalize_audio.py --inputs <raw-01.wav> <raw-02.wav> --output-dir <new-normalized-directory>
```

It requires local FFmpeg and mono PCM16 WAVs, uses two-pass EBU R128 `loudnorm` at -18 LUFS,
-1.5 dBTP and LRA 7, and returns source/output paths, measurements, duration checks and
`human_action: listen`. These are consistent narration defaults, not a universal broadcast
requirement. For video narration, `--target-lufs -23` is an alternative batch target;
measure and listen to the result. Missing FFmpeg is a readiness problem; installation retains its own authority.
Invalid, silent, unsafe or overwritten inputs/targets fail without replacing source files.

Very short or ungated clips can yield nonfinite LUFS measurements. The helper explicitly reports
bounded RMS/peak fallback with at most 20 dB gain and a -1.5 dBFS sample-peak ceiling; it does not claim
that such a clip met a LUFS target. Reauthor/resynthesize an unsuitable fragment when listening
finds a mismatch. Retain complete text and natural sentence endings; segmentation comes from
the author's sentence/phrase boundaries, never guessed timestamps. Consumers update media paths
to the returned normalized files and retain raw sources for recovery. Keep synthesis in this
package and assembly/compression in the consuming owner; no sibling code imports.
