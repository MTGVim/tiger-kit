# Model routing

## Axes

Keep implementation ownership and model cost separate:

```text
strategy: direct | delegated
tier: cheap | standard | most_capable
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

## Configuration

`$tk-implement --config --show` reports effective values without writing.
`--repo` selects a repository-local override; without it, the user-level host
context is selected. Precedence is:

```text
repo-local explicit override → user-level host context → inherit current model
```

The only managed block is replaced atomically and never duplicated:

````md
<!-- tigerkit:model-routing:v1 -->
```yaml
cheap:
  model: <host-resolved-cheap-alias>
  effort: low
standard:
  model: <host-resolved-standard-alias>
  effort: medium
most_capable:
  model: inherit
  effort: high
```
<!-- /tigerkit:model-routing:v1 -->
````

`--config --migrate` first shows source location, preserved/removed text, and
the proposed mapping. It may remove only instructions that map exactly to the
managed block. Ambiguous, domain-specific, conflicting, or host-specific
instructions remain untouched and are reported as migration candidates.
`--config --reset` removes only the managed block at the selected scope.

### Host capability contract

Host adapters report `per_call_model`, `per_call_effort`, and
`provider_override` separately. `per_call_effort` is exactly one of:

`per_call | definition_only | unavailable`

| State | `--config --show` consequence |
| --- | --- |
| `per_call` | The adapter sends the tier's effort on every dispatch. |
| `definition_only` | The effort is effective only when its managed definition file exists; the preview must show that file and the block otherwise uses `effort: inherit`. |
| `unavailable` | The host cannot apply the effort; the block uses `effort: inherit` and `--config --show` reports the advisory/fallback. |

`--config --show` reports the state and consequence, not an effort value that
may be inert. A user-required override that the state cannot satisfy is
`Blocked`; an inferred optimization falls back to `direct` and the current
model.

#### Claude Code

Claude Code uses `definition_only` for models whose effort is exposed through
agent-definition frontmatter. Dispatch-time `model` remains a separate knob
and overrides any model in frontmatter, so TigerKit's managed definitions
carry `effort` only and have no model field.

For `--config --migrate`, the preview lists the definition files it would
create, one effort-only file per distinct effort value in the managed block,
alongside the preserved/removed text and proposed mapping. Nothing is written
until the same explicit apply action required for the managed block is
confirmed. `--config --reset` removes only the definitions TigerKit created.

If a tier's model has no effort parameter, including Haiku, the tier is inert:
no definition file is created and its block value is `effort: inherit`. If the
user declines the roster, every tier it would have covered also uses
`effort: inherit`; a concrete effort is written only when a backing definition
file exists.

#### Codex

Codex uses `per_call` effort. Every spawn that emits a tier `model` must emit
the matching `reasoning_effort` in the same call; model-only dispatch is never
valid because it resets effort to the selected model's default rather than
preserving the tier's effort.
