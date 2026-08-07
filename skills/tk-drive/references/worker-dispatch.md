# Fresh-worker dispatch

Drive는 각 role을 효율적으로 완료할 것으로 예상되는 최소 capability tier를
선택한다.

| Tier | Use when |
| --- | --- |
| `cheapest` | Mechanical하고 범위가 좁으며 evidence가 완전한 작은 local change |
| `standard` | 일반적인 multi-file integration, normal debugging, nontrivial implementation |
| `strongest` | Design-heavy, 원인 불명, broad-reasoning, security/data-sensitive 또는 high-complexity work |
| `host-default` | Host가 spawn마다 tier를 선택할 수 없음 |

Tier 선택을 user decision으로 노출하거나 provider/model name을 저장하지 않는다.
가능하면 host의 per-spawn tier/effort control을 사용한다. 그렇지 않으면
fresh-worker execution을 유지하고 `host-default`를 기록한다. User 또는
repository mapping layer를 만들지 않는다.

Escalate하기 전에 missing context를 보충한다. Demonstrated reasoning 또는
complexity failure 뒤에만, 항상 한 tier 높은 fresh worker로 escalate한다.
Approved bounded corrective round를 넘으면 중단한다. 무기한 retry하지 않는다.

각 worker brief에는 unit 하나, exact R/AC, 관련 source path, scope/exclusion,
verification obligation, 현재 Git ownership fact만 담는다. 관련 없는 source,
verbose history, child receipt, secret 또는 다른 workflow를 nest할 권한은
포함하지 않는다.
