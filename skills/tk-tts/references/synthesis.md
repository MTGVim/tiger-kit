# Synthesis and Inspection

Preserve source/caption/UI literals and prepare a separate run-owned UTF-8 spoken script.
Before synthesis, resolve numeric spans by meaning: quantities, currency, decimals and counters
versus identifiers, telephone digits and version components. Preserve values, signs, precision,
leading zeros and intended grouping. Expand units or abbreviations only with their context and
case; resolve meaning-changing ambiguity in the affected passage while continuing unambiguous
preparation. Review these spans source-to-spoken and pass the spoken script to the adapter.
Raw-input benchmarks keep the approved text unchanged; a pronunciation-corrected comparison is
a separate declared condition shared by every candidate. Use complete sentences; avoid splitting
short interjections into independent requests without testing.

These are script examples, not verified acoustic outputs or a fixed replacement dictionary.

| Source context | Spoken-script example | Meaning to preserve |
|---|---|---|
| `가격 2,048원` | `가격 이천사십팔 원` | Quantity and currency |
| `인증코드 002048` | `인증코드 공 공 이 공 사 팔` | Leading zeros and individual digits |
| `응답 시간 250ms` | `응답 시간 이백오십 밀리초` | Duration and time unit |
| `MS 계정` | `엠에스 계정` | Abbreviation, not a time unit |
| `0.5GB` | `영 점 오 기가바이트` | Decimal value and byte unit |
| `버전 2.4.0` | `버전 이 점 사 점 영` | Version components and final zero |

Verify claimed pronunciation improvements separately by listening to fresh before/after files
with the same engine, voice and settings; script review alone is not acoustic evidence.

Qwen provides sohee (Korean default) and explicit serena;
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
