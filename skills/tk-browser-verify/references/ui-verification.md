# Proactive UI verification

Before a browser tool or verification server call, apply only rows relevant to
the current work. This routes around tool-specific traps; it does not define
the `Pass | Fail | Blocked | Unverifiable` contract.

Guard creates no N/A receipt for unused rows. Verdict combines this checklist
with the complete `SKILL.md` contract. Treat provider behavior as real only
when confirmed for the current tool and version.

| Condition | Trap to check | Detail |
|---|---|---|
| Always | P1 target: interact only with the exact control | [behavior](behavior.md) |
| Always | P3 use trusted pointer/keyboard input as interaction evidence | [behavior](behavior.md) |
| Always | P8 clean up only run-owned page/context/browser/PID | [session lifecycle](session-lifecycle.md) |
| Visual success claim | P1 evidence: inspect screenshot plus required computed state | [visual](visual.md) |
| CDP attachment | P2 verify endpoint, process, port, and isolated profile | [environment](environment.md), [session lifecycle](session-lifecycle.md) |
| Component/primitive migration | P4 compare all baseline style axes and full-width consumers | [visual](visual.md), [design](design.md) |
| API-gated state/native dialog | P5 use exact response mock and preinstalled dialog handler | [behavior](behavior.md), [safety](safety.md) |
| Screenshot saving | P6 write under tool workspace and clean repo residue | [environment](environment.md) |
| Breakpoint/hover | P7 measure actual `innerWidth` and trusted hover state | [visual](visual.md) |
| Animation/transition | P9 prepare event timeline before trigger | [behavior](behavior.md) |
| Clearing a populated field | P10 reobserve an empty value before save | [behavior](behavior.md) |
| Verification server | Confirm runner-specific auto-open suppression | [environment](environment.md) |

User-facing progress and receipt prose follows the user's language.
