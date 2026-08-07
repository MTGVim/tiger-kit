# Model routing

## Axes

Keep implementation ownership, implementor identity, and model cost separate:

```text
strategy: direct | delegated
tier: cheap | standard | most_capable
implementor: host-resolved writable agent/profile
```

`direct` keeps the current agent as implementor. `delegated` transfers one
Ready unit to exactly one autonomous implementor; the controller still owns
diff review, verification, staging, and the commit. A tier names the lowest
sufficient reasoning level, not a provider or a hard-coded model alias.

## Selection

| Evidence | Strategy | Tier |
| --- | --- | --- |
| Ready, bounded, independently transferable unit and host supports per-call routing | delegated | cheap |
| Several files, known repository pattern, ordinary debugging | direct or delegated | standard |
| Design choice, unknown cause, security-critical boundary, or controller-only context | direct | most_capable or inherit |

Failure handling is bounded: context failure strengthens the brief, scope
failure resizes the unit, reasoning failure promotes one tier, and a new user
or design decision returns to the controller. Do not treat every failure as
evidence that the model is too weak.

## Implementor resolution

For `delegated`, resolve the implementor after the strategy and tier are fixed
and before dispatch. A tier is not itself a dispatch target.

1. Query the host's exposed candidate roster. Each candidate must have a stable
   identifier and enough metadata to distinguish writable tools, model,
   effort/profile backing, and read-only status.
2. Discard candidates that cannot modify the unit's files, lack the required
   tools, are explicitly read-only, or are investigation/planning personas
   such as `Explore` or `Plan`. A read-only candidate is never an implementor.
3. Prefer an explicit v2 `agent` mapping when that candidate is still writable
   and satisfies the unit. Otherwise choose the host candidate that matches the
   resolved tier and unit requirements. Use the host's stable roster order as
   the deterministic tie-break; do not invent a provider alias.
4. Record `resolved implementor`, tier, dispatch model/effort, and the
   selection reason in the handoff and configuration evidence before spawn.

If no suitable candidate exists, inferred optimization falls back to `direct`
with the current model and is reported as a fallback. A user-required
implementor/model/effort override that cannot be satisfied is `Blocked`; it is
never silently mapped to a read-only or unrelated candidate.

## Configuration

`$tk-implement --config --show` is read-only. For each tier it reports the
effective source, `resolved implementor`, dispatch `model`, effort state, and
the evidence/reason. It must distinguish an effective route from an inert,
unknown, or fallback route and must not claim that an unsupported effort was
applied.

`--repo` selects a repository-local override; without it, the user-level host
context is selected. Precedence is:

```text
repo-local explicit override → user-level host context → inherit current model
```

The managed block is v2 and is replaced atomically, never duplicated:

````md
<!-- tigerkit:model-routing:v2 -->
```yaml
cheap:
  agent: <host-resolved-writable-agent-or-omit>
  model: <host-resolved-cheap-model-or-inherit>
  effort: <effective-effort-or-inherit>
standard:
  agent: <host-resolved-writable-agent-or-omit>
  model: <host-resolved-standard-model-or-inherit>
  effort: <effective-effort-or-inherit>
most_capable:
  agent: <host-resolved-writable-agent-or-omit>
  model: <host-resolved-most-capable-model-or-inherit>
  effort: <effective-effort-or-inherit>
```
<!-- /tigerkit:model-routing:v2 -->
````

`agent` is optional and identifies the implementor selected from the host
roster. `model` remains a dispatch-time value. A concrete `effort` is allowed
only when the host has an effective backing path; otherwise the value is
`effort: inherit`. Existing v1 text is read during migration and upgraded only
after the normal preview, user choice, and explicit apply gate. `--reset`
removes only TigerKit-owned managed text and definitions at the selected scope.

### Host capability contract

An available host adapter reports `per_call_model`, `per_call_effort`, and
`provider_override` separately. For an available adapter,
`per_call_effort` is exactly one of:

`per_call | definition_only | unavailable`

| State | `--config --show` consequence |
| --- | --- |
| `per_call` | The adapter sends the tier's effort on every dispatch. |
| `definition_only` | Effort is effective only through the selected managed definition file; the preview names that file and the block uses `effort: inherit` without it. |
| `unavailable` | The host cannot apply effort; the block uses `effort: inherit` and the output reports the advisory/fallback. |

An absent or unconfigured adapter reports each capability as `unknown`, not as
a guessed state. Inferred optimization uses safe `direct` + current-model
execution. A required override remains `Blocked`.

## Claude Code

Claude Code exposes a roster of agent types with fixed model, effort, tools,
and instructions. For a delegated unit, select an existing writable roster
entry first, set its identifier in the v2 `agent` field, and keep dispatch-time
`model` separate. `Explore`, `Plan`, and any candidate without the tools and
instructions needed by the Implementor contract are not eligible.

For `--config --migrate`, preview the source location, v1-to-v2 mapping,
resolved roster candidates, preserved/removed text, and any files that would be
created. Then present exactly one decision checkpoint with these choices:

- `Map tiers to existing agent types` — **Recommended**; use suitable writable
  roster entries and create no new definitions for covered tiers.
- `Add effort-only agent definitions` — always show this exact label. If the
  preview proves that a suitable writable roster candidate covers the tier,
  mark this option `unavailable`, explain why, and create no files. Otherwise,
  it becomes actionable only after the preview proves roster coverage is
  absent; create one effort-only file per distinct effort value, with no model
  field, plus the writable tools and Implementor instructions required by the
  contract. These files are TigerKit-owned.
- `Keep effort: inherit without definitions` — create no definition files and
  leave every affected tier at `effort: inherit`.

All three exact labels remain visible at the one checkpoint; an inapplicable
option is marked `unavailable` rather than silently omitted.

`--config --migrate` is a real preview/apply flow, not show-only. Nothing is
written until the user selects one option and confirms the same explicit apply
action required for the managed block. The `--reset` action removes only the definitions TigerKit created and the managed text; it never deletes a host-owned roster entry.

If a model has no effort parameter, including Haiku, its tier is inert: do not
create a definition and use `effort: inherit`. If the user declines the roster
or the roster does not cover a tier, do not write a concrete effort. Report the
resolved implementor and the backing evidence rather than claiming the value
was applied.

## Codex

Codex uses `per_call` effort. Resolve a writable implementor/profile before
spawn using the same candidate, requirement, and fallback rules. Every spawn
that emits a tier `model` must emit the selected implementor plus the matching
`reasoning_effort` in the same call; model-only dispatch is invalid because it
resets effort to the selected model's default.

## Hermes

The installed Hermes CLI exposes `--model`, `--reasoning`, and `--provider` on
`hermes chat`; that CLI capability is verified separately from the repository
adapter. The current TigerKit host adapter invokes only
`hermes chat -q <wrapped prompt> --toolsets terminal,skills` and does **not**
forward those routing flags. Do not claim that CLI support is effective
TigerKit per-call routing.

The adapter may resolve the adapter-local writable implementor identifier
`hermes-chat` when `terminal,skills` and file-write permission are present. It
is not a read-only planning persona or a provider alias. Record the identifier
and the toolset/permission reason before dispatch. Because the current adapter
does not forward `--model`, `--reasoning`, or `--provider`, it reports
`per_call_model: unknown`, `per_call_effort: unknown`, and
`provider_override: unknown` for TigerKit routing. Inferred optimization falls
back to `direct` + current-model execution; a required override is `Blocked`.

The verified CLI flags and generic Hermes tier mapping (`cheap → low`,
`standard → medium`, `most_capable → high`) are adapter implementation inputs,
not current effective behavior. A future adapter change must forward them in
the same invocation and add matching host/eval evidence before changing these
capability states.

## Unconfigured hosts

Any host without an adapter section reports
`per_call_model: unknown`, `per_call_effort: unknown`, and
`provider_override: unknown` from `--config --show`. Do not infer a tier-to-
model or provider mapping from a generic host-context phrase. Use direct/current
execution for an inferred optimization and return `Blocked` when the user
requires an override that cannot be proven effective.
