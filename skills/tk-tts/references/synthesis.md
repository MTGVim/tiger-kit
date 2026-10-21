# Synthesis and Inspection

Write complete pronunciation-corrected sentences to a run-owned UTF-8 text file; avoid splitting
short interjections into independent requests without testing. Keep canonical caption spelling
and technical UI literals separate. Qwen provides sohee (Korean default) and explicit serena;
the 0.6B model ignores instruct. Do not offer unsupported styles or silently upgrade models.
ppaso uses its model voice, not Qwen speaker IDs. Browser speech is never an exported WAV route.

```bash
python -B scripts/qwen3.py --engine mlx --quantization 5 --text-file <script.txt> --output <new.wav> --speaker sohee
python -B scripts/ppaso.py --text-file <script.txt> --output <new.wav>
```

Use a new WAV path after editing text; preserve existing output. Run synthesis in a fresh owned
process with its own deadline and stall limit set before launch. Downloads/setup and smoke are
separate from measurement. Include the longest planned input and use the same sentence/cache
policy as the baseline in a comparison; measure models sequentially. MLX selects Metal GPU,
cache_limit 0 and clears released sentence allocations. No silent CPU/engine fallback.
Keep peak Mac process footprint distinct from RSS and MLX active allocation; unavailable values
remain null. An observed run is not a general memory ceiling. No global watcher/benchmark runner.

Trim measured leading silence, validate consistent sample rate and write finite/non-silent mono
PCM16 WAV. The receipt owns actual duration, trim, revision and human_action: listen. The limited
cache inventory names new top-level entries and scan limits, not proof of ownership or a full
recursive audit. Attribute unexpected entries before cleaning exact run-owned paths. Python -B
prevents bytecode writes; PYTHONDONTWRITEBYTECODE alone is ignored by isolated Python -I.

Very short Qwen utterances can be silent or garbled depending on seed. Silence rejection does
not catch garbling. Do not silently retry another engine/seed or merge sentences as a claimed
fix: those policies need before/after evidence and listening. Return failure and retain the
script and proper-name/number/ending listening checklist. No ASR or automatic download is added.

The consumer chooses breathing gaps/scene alignment from measured WAV duration. Do not bake
course-specific timing or video scene logic into the TTS adapter. A selected voice not delivered
must stay failed/pending, never be relabeled as a finished silent preview.
