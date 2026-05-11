---
description: repo knowledge layer의 중복, 모순, 낡은 지침, 누락된 경계를 audit하고 작은 patch 후보를 제안합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 인용한 원문, 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: `CLAUDE.md`, `AGENTS.md`, `.claude/rules`, command docs, README/docs 같은 existing knowledge layer를 읽고 bloat, contradiction, staleness, missing boundary 문제를 찾아 작은 patch 후보를 제안합니다.

기본 출력은 `Improve Report`입니다. 명시적으로 승인받지 않는 한 파일을 수정하지 않습니다.
`Improve Report` 안의 finding ID(`IMP-001` 같은 식별자)는 각 finding마다 고정하고 `Findings`와 `Proposed Patches`에서 같은 값을 반복해 승인 대상을 쉽게 고를 수 있게 유지합니다.

## Agent routing

넓은 knowledge layer 탐색은 Claude Code 내장 `Explore`를 사용할 수 있습니다. 모순, bloat, YAGNI, workflow risk 판단은 `tk-ru`를 사용할 수 있습니다. API workflow 문서나 `mock_api_contract` 설명의 drift는 `tk-sif-muna` 관찰을 참고할 수 있습니다. 승인된 cleanup patch, docs hygiene, 낡은 지침 정리는 `tk-elyvilon`을 사용할 수 있습니다.

agent를 사용해도 이 명령은 audit/report만 수행합니다. 승인 없는 patch 적용, automatic broad rewrite, self-modifying workflow, hook, queue, history scan, automatic apply를 구현하거나 실행하지 않습니다.
