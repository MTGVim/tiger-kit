# Fresh-worker dispatch

This is the canonical tier-to-capability contract for `tk-drive` and delegated
`tk-pr-respond`/`tk-pr-sweep` workers. Consumer skills refer to this file; they
do not redefine the tier vocabulary.

## Two-axis tier contract

Every requested tier resolves two independent axes. The axes describe
capability, not a provider, model name, or user-configurable setting.

| Tier | Model axis | Effort axis | Use when |
| --- | --- | --- | --- |
| `cheapest` | lowest sufficient | low | Mechanical, narrow local work with complete evidence |
| `standard` | standard sufficient | medium | Ordinary multi-file integration or debugging |
| `strongest` | highest available | high | Design-heavy, unknown-cause, broad-reasoning, security/data-sensitive, or high-complexity work |
| `host-default` | host default | inherit | The host cannot select a tier per spawn |

The requested tier is selected from unit evidence. It is not exposed as a user
decision, and provider/model names are never stored in a receipt or ledger.

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
silently promote, invent a mapping layer, or fall back to controller edits.

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
delegated fresh-worker dispatch required by this skill. A host restriction that
only permits an AgentTool after a user request must not be interpreted as a
reason to reverse the dispatch into direct/controller execution. If the host
still cannot spawn a usable worker, stop with `Blocked`; never edit as a
controller fallback.

Escalate only after missing context is supplied and a demonstrated reasoning or
complexity failure remains. Escalation uses one tier higher and a fresh worker;
it is bounded and never an unlimited retry loop.

Each worker brief contains one unit, exact R/AC, relevant source paths,
scope/exclusion, verification obligation, and current Git ownership facts. Do
not nest unrelated source, verbose history, child receipts, secrets, or another
workflow's authority.
