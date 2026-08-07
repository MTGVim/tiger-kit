# Fresh-worker dispatch

Drive selects the least capable tier expected to complete each role efficiently:

| Tier | Use when |
| --- | --- |
| `cheapest` | Mechanical, tightly bounded, complete evidence, small local change |
| `standard` | Ordinary multi-file integration, normal debugging, nontrivial implementation |
| `strongest` | Design-heavy, unknown-cause, broad-reasoning, security/data-sensitive, or high-complexity work |
| `host-default` | The host cannot select a tier per spawn |

Do not expose tier selection as a user decision or persist provider/model names.
Use the host's per-spawn tier/effort control when available. Otherwise preserve
fresh-worker execution and record `host-default`; never create a user or repository
mapping layer.

Supply missing context before escalating. Escalate only after demonstrated
reasoning or complexity failure, always to a fresh worker one tier higher. Stop
after the approved bounded corrective rounds; never retry indefinitely.

Each worker brief contains one unit, its exact R/AC, relevant source paths,
scope/exclusions, verification obligations, and current Git ownership facts. It
does not include unrelated source, verbose history, child receipts, secrets, or
authority to nest another workflow.
