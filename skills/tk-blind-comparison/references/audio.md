# Audio display copies

Inspect available local tools before conversion. Decode every source; preserve originals.
Use WAV for local playback, not host-dependent FLAC links. For loudness-neutral comparison,
measure integrated loudness and true peak with local ffmpeg `loudnorm` first, then apply the
measured second pass to every clip with a shared target (for example -16 LUFS, -1.5 dBTP),
mono/stereo policy and sample rate. Strip metadata with `-map_metadata -1`. Validate decoded
samples, non-silence, duration and clipping after conversion. Very short/silent clips may
not yield valid loudness measurements: record the limitation rather than fabricating values.

If loudness/dynamics are the variable under test, preserve them and disclose the exception.
Never trim pronunciation/endings, denoise or synthesize replacement speech to improve a candidate.
Review spoken self-identification manually. Put measured settings and any residual voice cues
in neutral transformations, with engine-specific diagnostics only in the answer key.
