# Fresh-worker dispatch

This is the canonical tier-to-capability contract for `tk-drive` and delegated
`tk-pr-respond`/`tk-pr-sweep` workers. Consumer skills refer to this file; they
do not redefine the tier vocabulary.

## Two-axis tier contract

Every requested tier resolves two independent axes. The axes describe
capability, not a provider, model name, or user-configurable setting.

| Tier | Model axis | Effort axis | Use when |
| --- | --- | --- | --- |
| `cheapest` | lowest sufficient | low | Mechanical work or bounded implementation with a known pattern and complete evidence |
| `standard` | standard sufficient | medium | Multi-file implementation with interacting interfaces, or focused debugging after the cheapest tier cannot prove the fix |
| `strongest` | highest available | high | Design-heavy, unknown-cause, broad-reasoning, security/data-sensitive, or high-complexity work |
| `host-default` | host default | inherit | The host cannot select a tier per spawn |

The requested tier is selected from unit evidence. It is not exposed as a user
decision, and provider/model names are never stored in a receipt or ledger.

Implementation work starts at `cheapest`. File count, urgency, or a preference
for a stronger model is not evidence for promotion. Use `standard` only when
the unit's interfaces or debugging evidence require it, and use `strongest` only
for design, unknown-cause, security/data-sensitive, or demonstrated reasoning
failure. A corrective escalation promotes one tier at most once and remains
bounded.

## Execution strategy

Each unit records one explicit execution strategy: `direct` or `delegated`.

| Strategy | Executor | Allowed when |
| --- | --- | --- |
| `direct` | The current host context temporarily acts as the unit executor; no subagent is spawned. | The user passes `--direct` or approves the displayed plan recommendation `strategy=direct`, and the unit is one bounded standalone `tk-drive` or standalone `tk-pr-respond` implementation. |
| `delegated` | One fresh worker receives the bounded unit brief. | A fresh context, isolation, independent worker, reviewer handoff, design-heavy reasoning, or parent `tk-pr-sweep` route is required. |

For a bounded known-pattern implementation with no isolation obligation,
Prepare recommends `strategy=direct` with `tier=cheapest` in the single
`👍 Recommendation:` approval surface. In `tk-drive` this is the default
recommendation; standalone `tk-pr-respond` uses the same recommendation unless
the unit needs isolation or another delegated-only boundary. Approval of that
displayed plan is the explicit strategy approval; do not ask for a second
direct confirmation. `--direct` preselects the same strategy. If the user
chooses delegated, honor that choice. This is a role handoff, not controller
fallback: while editing, the current context is the unit executor and may touch
only the frozen unit paths. It cannot expand scope, create another unit, change
the approval/ledger owner, or publish remotely. After the candidate is ready,
the owning controller resumes verification and mechanical bookkeeping.

`direct` is never an implicit fallback for an unavailable delegated worker. If
the approved strategy is `delegated`, an unusable worker remains `Blocked`.
`tk-pr-sweep` is delegated-only because its multi-PR isolation and nested-owner
boundaries cannot be replaced by one direct executor.

Direct execution inherits the current host context; it must not claim a lower
model than the host provides. The low-tier preference applies to delegated
workers through the model/effort axes below.

## Host capability contract

Determine capability independently for the `model` and `effort` axes before the
first dispatch. Each axis has exactly one of these states:

| State | Meaning and rule |
| --- | --- |
| `per_call` | The axis can be sent on every spawn. |
| `definition_only` | The axis is effective only through an existing matching host/agent definition. If that definition is absent, treat the axis as `unavailable`; do not invent a roster or create a provider-specific mapping. |
| `unavailable` | The axis cannot be applied. Use `host-default` for model and `inherit` for effort. |

TigerKit does not ship a provider-specific effort-definition roster. A
`definition_only` capability is therefore usable only when the host already
provides the matching definition.

Resolve the axes separately. A host may therefore apply a model per call while
using effort from an existing definition, or apply only effort while the model
uses the host default. Never claim an axis was applied when its capability is
`definition_only` without the backing definition.

## Deterministic collapse

When a host exposes fewer controls than the requested tier, preserve the
requested tier as an internal fact and record the realized collapse. Do not
silently promote, invent a mapping layer, or silently switch execution strategy.

1. If `model` is unavailable, realize model as `host-default` and still apply
   the effort axis when it is available.
2. If `effort` is unavailable, realize effort as `inherit` and still apply the
   model axis when it is available.
3. If both axes are unavailable, realize the dispatch as `host-default`.
4. If only effort is available, `cheapest` and `standard` both realize `low`,
   `strongest` realizes `high`, and `host-default` realizes `inherit`.
5. If no per-spawn tier selection is possible, use `host-default` for the
   dispatch and keep the original tier only as non-user-visible evidence.

The ledger records symbolic facts such as
`requested=strongest; model=host-default; effort=high; collapse=model-unavailable`.
It never records provider/model names, secrets, or a user-facing tier choice.

## Dispatch authorization and failure

`tk-drive` is `user-invoked` and has `disable-model-invocation: true`. An
explicit `/tk-drive` or `$tk-drive` invocation is the user's request for the
skill's approved execution strategy. It also satisfies a host restriction that
only permits an AgentTool after a user request; do not reverse an approved
delegated run into direct execution. If the host cannot spawn a usable worker,
stop with `Blocked` unless `direct` was selected before mutation. Direct mode
must still obey the one-unit scope and verification boundaries above.

Escalate only after missing context is supplied and a demonstrated reasoning or
complexity failure remains. Escalation uses one tier higher and a fresh worker;
it is bounded and never an unlimited retry loop.

Each worker brief contains one unit, exact R/AC, relevant source paths,
scope/exclusion, verification obligation, and current Git ownership facts. Do
not nest unrelated source, verbose history, child receipts, secrets, or another
workflow's authority.
