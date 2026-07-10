# TigerKit operator-environment follow-ons

이 문서는 repo 밖 operator-environment 후속 과제를 current backlog에서 잃어버리지 않기 위한 tracking artifact입니다.

## Scope

아래 항목은 repo-local command contract와 별개로 운영 환경에서 따로 검토합니다.

1. superpowers SessionStart matcher의 `compact` 재주입 override 조사
2. plugin routing audit (owner-eval 관점)
3. `shoehorn` migration 검토
4. reference drawer
   - `simplify-ignore`
   - `sdd-cache validator`

## Rules

- 이 문서는 repo-local implementation proof가 아닙니다.
- operator-environment 항목은 repo command surface와 분리해 추적합니다.
- repo release gate를 불필요하게 막지 않되, follow-up이 유실되지 않게 유지합니다.

## Current status

- compact reinjection override: pending investigation
- routing audit: pending
- shoehorn migration: pending
- reference drawer: recorded only
