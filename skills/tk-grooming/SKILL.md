---
name: tk-grooming
description: "[user/auto] 기존 repository/user rule 또는 skill의 중복·범위·배치·트리거를 감사할 때 사용합니다. 기본은 report-only이며 literal --apply 또는 현재-turn 승인 전에는 수정하지 않습니다."
argument-hint: "[범위] [--apply]"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: native
---

# 정리

명시 호출 또는 기존 rule/skill을 감사해 달라는 명확한 요청에 사용합니다. 일반 정리나 구현 요청에는 자동으로 활성화하지 마세요. implicit mode는 report-only입니다.

## Workflow

1. `범위 확정`: 입력은 요청 범위와 `--apply` 여부, 출력은 대상 경로와 허용 변경 범위입니다.
2. `discovery`: 실제 존재하는 native 경로만 읽고, 출력은 네 영역의 후보 경로 목록입니다.
3. `evidence`: 각 후보를 읽어 영역별 관찰 사실·경로·검증 상태를 출력합니다.
4. `분류/제안`: repository candidate에는 [배치 rubric](references/repository-placement.md)을 적용하고, 입력 evidence를 `keep | tighten | merge | split | move | convert | deprecate | delete | fix` 중 하나로 분류합니다.
5. `🔴 CHECKPOINT · 🛑 STOP`: 범위·evidence·제안·허용 apply를 receipt로 요약하고 확인 전에는 변경하지 않습니다.
6. `apply/report`: 입력은 checkpoint receipt와 다시 읽은 원본 상태이고, 출력은 아래 mode 전이표가 허용한 제안 또는 수정입니다.
7. `재검증`: apply 후 링크·중복·frontmatter를 다시 검사하고 결과·미검증·미해결 항목을 receipt로 출력합니다.

### Mode 전이

| Mode | Trigger | Allowed mutation | Output |
|---|---|---|---|
| `report-only` | implicit mode, `--apply` 없음, 과거 승인 또는 일반 진행 응답 | 없음 | evidence·분류·제안·receipt |
| `applied` | 최초 요청의 literal `--apply` 또는 checkpoint 뒤 현재 turn의 정확한 범위 승인 | `tighten`, exact target의 기계적 `move`, 참조 없는 `delete`, frontmatter/link `fix`만 | 실제 적용 내용과 재검증 |
| `pending` | Rule→skill `convert`, workflow `split`, semantic skill rewrite | 없음 | exact candidate/target 제안; `tk-learn` 입력 가능, 자동 호출 금지 |
| `Partial/Blocked` | scope/apply 권한 충돌 또는 target이 checkpoint evidence와 달라짐 | 없음 | 새 evidence와 필요한 결정 하나; fresh proposal 필요 |

기존의 네 영역, 즉 저장소 규칙, 저장소 스킬, 사용자 규칙, 사용자 스킬을 검사하세요. 실제로 존재하는 호스트 네이티브 경로를 사용하세요. [탐색](references/discovery.md)에 후보가 나열되어 있습니다. 누락된 파일을 만들거나 레거시 전역 TigerKit 상태를 검사/마이그레이션하지 마세요.

Repository rule/skill은 파일 전체가 아니라 독립적인 normative instruction/workflow 단위로 판정하세요. 기대 kind가 달라지면 `convert`, 둘 다 rule이지만 root와 nested 위치가 다르면 `move`, 한 artifact가 서로 다른 결과 단위를 섞으면 먼저 `split`, 위치와 kind가 맞고 다른 결함이 없으면 `keep`입니다. 필요한 path/count/threshold evidence가 없거나 충돌하면 추정하지 말고 해당 영역을 `Partial/Blocked | Unverifiable`로 두세요.

적용 시 원본을 다시 읽고, 삭제 전에 참조를 검색하고, 관리되거나 자동 생성된 콘텐츠의 소유권 표기를 보존하며, 광범위한 저장소/사용자 변경을 조용히 섞지 마세요. 지식을 지어내거나 회고/학습을 대신하지 마세요.

## Failure paths

- If a required path is missing or unreadable → mark only that area `Unverifiable`, keep unrelated areas read-only, and report the path and required access.
- If scope or apply permission conflicts → make no change and return `Partial/Blocked` with the single decision needed.
- If a delete/move target still has references → do not delete or move it; change the proposal to `keep` or `tighten` and cite the references.
- If an apply target differs from its checkpoint evidence → do not change it; return `Partial/Blocked` with the new evidence and require a fresh proposal.
- If post-apply validation fails → stop and do not claim `Complete`; restore and revalidate only when this run's changes can be reversed exactly, otherwise stop further mutation and report the failed check, affected files, and observed state.

## 계약

각 영역의 실제 경로와 내용을 증거로 남기고 필수 증거가 없으면 해당 영역을 `Unverifiable`로 표시하세요. 하나라도 차단되면 전체를 완료로 보고하지 말고 `Complete | Partial/Blocked | Unverifiable`로 구분하세요. 적용 후 링크, 중복, frontmatter와 같은 네 영역을 재검증하세요. 출력의 단일 소유자는 `발견 사항`(영역별 관찰 증거·미검증·미해결 항목만), `제안 작업`(분류와 제안), `적용 내용`(실제로 바꾼 내용만), `검증`(적용 후 재검증)입니다. `keep | tighten | ... | fix` 분류와 제안 표현을 발견 사항에 섞지 마세요. report-only에서는 빈 적용 내용과 적용 후 검증을 생략할 수 있습니다. Receipt에는 전체 상태, `report-only | applied` 모드와 내용이 있는 섹션의 참조만 기록하고 해당 본문을 반복하지 마세요.

## Output contract

독립적인 normative instruction/workflow 항목을 처음 식별한 순서대로 `GR-01`, `GR-02`, …를 한 번 부여하세요. `발견 사항`, `제안 작업`, 내용이 있을 때의 `적용 내용`·`검증`, Receipt의 섹션 참조와 마지막 Summary는 모두 같은 `GR-##`를 사용합니다. 섹션마다 다시 번호 매기거나 ID 없는 발견·제안·적용·검증 항목을 출력하지 마세요.

응답의 마지막 섹션은 항상 아래 고정 형식의 `## Summary`입니다. 항목마다 정확히 한 행을 두고, `Rule`에는 짧은 이름과 `keep | tighten | merge | split | move | convert | deprecate | delete | fix` 분류를, `한 줄 요약`에는 새 evidence를 추가하지 않는 한 문장을, `적용 타깃`에는 구체적인 경로/skill/user 범위 또는 `미확정 (<이유>)`를 적으세요. 발견·제안·변경·검증 본문을 표에 복사하지 마세요.

| No. | Rule | 한 줄 요약 | 적용 타깃 |
| --- | --- | --- | --- |
| GR-01 | `<짧은 이름> (<분류>)` | `<한 문장>` | `<구체적 타깃 또는 미확정 (이유)>` |

항목이 없거나 전체가 `Unverifiable`이어도 Summary를 생략하지 말고 `| — | 없음 | 감사 항목 없음 | 적용 없음 |` 한 행을 출력하세요.

## CHECKPOINT / STOP

감사 결과와 허용 범위를 receipt로 요약하기 전에는 `--apply` 변경을 시작하지 마세요. 범위가 불명확하거나 삭제·이동의 참조 근거가 없으면 적용하지 말고 `Partial/Blocked` 또는 `Unverifiable`로 멈추세요.

## DO NOT / ANTI-PATTERNS

- `--apply` 없이 파일을 수정하거나, 삭제·이동 전에 참조를 확인하지 마세요.
- 사용자가 지정하지 않은 저장소·사용자 파일을 조용히 섞어 바꾸지 마세요.
- 레거시 전역 TigerKit 상태를 탐색하거나 마이그레이션하지 마세요.
- Rule→skill convert, workflow split 또는 semantic skill rewrite를 직접 적용하거나 `tk-learn`을 자동 호출하지 마세요.
- 항목 ID를 생략·재사용·재번호화하거나 Summary를 생략하지 마세요.
