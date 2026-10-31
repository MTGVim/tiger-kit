# Media choices and saved defaults

Read before the first video/narration choice, including direct video requests and parent handoffs.
Resolve each optional `evidenceMedia` field independently, highest first: current explicit request
or answered current-run choice > ignored `.tigerkit/repository.json` > user
`${XDG_CONFIG_HOME:-~/.config}/tigerkit/settings.json` > team `tigerkit.config.json` > defaults.
Missing upper fields retain lower values. Inspect existing files without creating them. Preserve
whether each value came from a request, saved field or fallback; a fallback is not an answered choice.

| Field | Type / values | Fallback |
| --- | --- | --- |
| `enabled` | boolean | `false` |
| `format` | `auto`, `gif`, `mp4` | `auto` |
| `narration` | boolean | `false` |
| `voice` | `serena`, `sohee` | `sohee` |
| `captions` | `none`, `band`, `overlay`, `overlay-rounded` | `band` |
| `emphasis` | `in-slide`, `zoom`, `none` | `in-slide` for authored slides; `zoom` for selected capture highlights |
| `callouts` | boolean | `false` |
| `slideTheme` | `light`, `dark` | `light` |

Validate objects and field types/enums before use. A malformed media object makes saved media
preferences unusable for this run: disclose it, preserve its file and use safe fallbacks plus
explicit current-run answers, not a lower-layer opt-in. Do not change unrelated configuration
precedence. `voice` is a legacy Qwen speaker preference, not engine selection or permission to
hide other supported TTS routes. A direct movie request selects this run even if `enabled` is false.
No preference grants installation, capture mutation or publication authority.

## One choice round before production

Reuse explicit parent answers and saved values without re-asking them. For unresolved narration,
follow Narration Choice. For TTS, load `tk-tts` and show every route from its current
`list_options.py` output with device/platform, voices, missing dependencies and actual cache/setup
status; module presence is not verified model readiness. Prior evaluations may explain a
recommendation, never remove an available route. Keep supplied audio and no narration available.
Use the owning skill's ordinary-chat question format, not a host structured-question substitute.

In that same first round, ask about presentation fields with neither an explicit answer nor a
valid saved value: captions, emphasis, callouts and slide theme. Give the fallbacks as recommendations,
not silent decisions. If media itself is still optional, make styling conditional on accepting it;
declining media needs no styling answers. Theme concerns authored slides, not recoloring observed captures; resolve it
once when absent and retain it for any authored cards. Include tutorial cursor/input displays when
applicable. For a GIF with selected narration, resolve voiced MP4 versus caption-only GIF in that
round; never silently disable sound or change format.

When resolving a new unsaved choice and no save offer has already been answered,
on that same media-choice line append `이 선택을 기본값으로 저장할까요?`, naming the user
settings destination and exact proposed fields/values. Show conditional proposed values if answers
are still pending; clarify only an ambiguous save target/value. Selecting this run is not saving
consent. Do not ask another routine save stage. Reuse an accepted/declined offer in the active
conversation and pass its disposition, resolved values and their sources to the child owner.
Do not persist a prompt ledger or hidden opt-in/refusal flag.

## Approved save only

Save only when the user approves the destination and exact fields/values. Validate the current
JSON/version and path ownership again; merge only those approved `evidenceMedia` keys atomically
in that same directory, preserving unrelated keys including `html` and `verificationDataPolicy`.
Reread and verify every approved value before continuing. Concurrent changes require a fresh
merge; malformed/unsupported settings are preserved and reported, not replaced. Refusal or absent
save consent means current-run choices only. This bounded write is the sole settings exception;
team-tracked configuration needs its own explicit mutation/review authority.

## Translate resolved presentation into the manifest

Map `captions` to `caption_style`; `none` explicitly disables subtitle output/coverage only,
never selected narration or its missing/silent-audio checks. Keep source tags visible in rendered
frames when captions are off. Map `callouts: false` to no callout rows; true selects authored,
timed callouts rather than inventing geometry. Pass `slideTheme` to the card author, not ffmpeg.
For authored slides, implement `in-slide` by changing only the currently narrated element; leave
assembler zoom off. For capture-only input, `in-slide` means no assembler enlargement; retain
actual captured cues, never fabricate a slide-style UI state. For captured UI, `zoom` applies only to deliberately selected highlight regions
with the existing coordinate/provenance checks, not automatic motion on every frame. An explicit
zoom request for authored slides must be honored and inspected as a selected exception.
`none` means no emphasis; preserve visible comparisons and source facts in every treatment.
