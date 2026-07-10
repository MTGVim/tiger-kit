# TigerKit workflow matrix

이 문서는 TigerKit navigation surface가 superpowers 구현 surface와 어떻게 이어지는지 설명하는 사람용 안내입니다.

## Boundary

- `/tk:help` = 어느 command를 먼저 열어야 하는지 찾는 navigation surface
- `/tk:route` = 어떤 구현 전략이 맞는지 고르는 strategy surface
- `/tk:next` = 지금 다음 command 1개만 고르는 conductor surface

## Superpowers connection

| TigerKit question | Recommended surface |
| --- | --- |
| SoT가 없거나 unfamiliar area라 discovery가 먼저 필요하다 | `/tk:gap` (blindspot 포함) |
| 구현 route를 고르고 싶다 | `/tk:route` |
| direct implementation이 맞다 | superpowers direct execution flow |
| 역할 분리 구현이 맞다 | superpowers subagent-driven flow |
| goal decomposition이 더 중요하다 | superpowers goal-driven flow |
| 다음 command를 하나만 추천받고 싶다 | `/tk:next` |
| merge 전 이해도 확인이 필요하다 | `/tk:quiz` |

## Notes

- 이 문서는 사람용 matrix입니다. command selection의 machine-readable source는 `docs/help-map.json`입니다.
- `/tk:help`는 이 문서를 읽을 수 있지만, command list 자체를 수동 hardcode하지 않습니다.
