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

Host adapters report `per_call_model`, `per_call_effort`, and
`provider_override` capabilities separately. Unsupported fields are ignored
with an advisory/fallback, not represented as applied configuration. A user-
required unsupported override is `Blocked`; an inferred optimization falls
back to `direct` and the current model.
