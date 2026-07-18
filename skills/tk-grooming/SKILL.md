---
name: tk-grooming
description: "[user] 기존 저장소 및 사용자 규칙이나 스킬을 감사하고 선택적으로 수정합니다. 사용자가 명시적으로 호출할 때만 사용합니다."
disable-model-invocation: true
argument-hint: "[범위] [--apply]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# 정리

사용자가 이 스킬을 명시적으로 호출할 때만 사용합니다. 자동으로 활성화하지 마세요.

## Workflow

1. `범위 확정`: 입력은 요청 범위와 `--apply` 여부, 출력은 대상 경로와 허용 변경 범위입니다.
2. `discovery`: 실제 존재하는 native 경로만 읽고, 출력은 네 영역의 후보 경로 목록입니다.
3. `evidence`: 각 후보를 읽어 영역별 관찰 사실·경로·검증 상태를 출력합니다.
4. `분류/제안`: 입력 evidence를 `keep | tighten | merge | split | move | convert | deprecate | delete | fix` 중 하나로 분류합니다.
5. `🔴 CHECKPOINT · 🛑 STOP`: 범위·evidence·제안·허용 apply를 receipt로 요약하고 확인 전에는 변경하지 않습니다.
6. `apply/report`: report-only면 제안과 receipt만 출력하고, apply면 승인된 receipt와 다시 읽은 원본 상태를 입력으로 확인된 범위만 수정합니다.
7. `재검증`: apply 후 링크·중복·frontmatter를 다시 검사하고 결과·미검증·미해결 항목을 receipt로 출력합니다.

기존의 네 영역, 즉 저장소 규칙, 저장소 스킬, 사용자 규칙, 사용자 스킬을 검사하세요. 실제로 존재하는 호스트 네이티브 경로를 사용하세요. [탐색](references/discovery.md)에 후보가 나열되어 있습니다. 누락된 파일을 만들거나 레거시 전역 TigerKit 상태를 검사/마이그레이션하지 마세요.

중복, 모순, 구식, 끊어진 참조, no-op, 과도하게 긴 내용, 잘못된 범위/종류, 트리거 충돌, 죽은 스킬, 오래된 예시 또는 누락된 출처로 분류하세요. `keep | tighten | merge | split | move | convert | deprecate | delete | fix` 중 하나를 제안하세요.

기본은 보고만 수행합니다. 명시적인 요청이 있을 때만 적용하세요. 적용 시 원본을 다시 읽고, 삭제 전에 참조를 검색하고, 관리되거나 자동 생성된 콘텐츠의 소유권 표기를 보존하며, 광범위한 저장소/사용자 변경을 조용히 섞지 마세요. 지식을 지어내거나 회고/학습을 대신하지 마세요.

## Failure paths

- If a required path is missing or unreadable → mark only that area `Unverifiable`, keep unrelated areas read-only, and report the path and required access.
- If scope or apply permission conflicts → make no change and return `Partial/Blocked` with the single decision needed.
- If a delete/move target still has references → do not delete or move it; change the proposal to `keep` or `tighten` and cite the references.
- If an apply target differs from its checkpoint evidence → do not change it; return `Partial/Blocked` with the new evidence and require a fresh proposal.
- If post-apply validation fails → stop and do not claim `Complete`; restore and revalidate only when this run's changes can be reversed exactly, otherwise stop further mutation and report the failed check, affected files, and observed state.

## 계약

각 영역의 실제 경로와 내용을 증거로 남기고 필수 증거가 없으면 해당 영역을 `Unverifiable`로 표시하세요. 하나라도 차단되면 전체를 완료로 보고하지 말고 `Complete | Partial/Blocked | Unverifiable`로 구분하세요. 적용 후 링크, 중복, frontmatter와 같은 네 영역을 재검증하세요. receipt에는 `증거(영역별)`, `미검증`, `미해결 항목`, `제안 작업`, `적용 내용`, `적용 후 재검증`을 포함하며, 기존 `발견 사항`, `제안 작업`, `적용 내용`, `검증` 섹션에 연결하세요.

## CHECKPOINT / STOP

감사 결과와 허용 범위를 receipt로 요약하기 전에는 `--apply` 변경을 시작하지 마세요. 범위가 불명확하거나 삭제·이동의 참조 근거가 없으면 적용하지 말고 `Partial/Blocked` 또는 `Unverifiable`로 멈추세요.

## DO NOT / ANTI-PATTERNS

- `--apply` 없이 파일을 수정하거나, 삭제·이동 전에 참조를 확인하지 마세요.
- 사용자가 지정하지 않은 저장소·사용자 파일을 조용히 섞어 바꾸지 마세요.
- 레거시 전역 TigerKit 상태를 탐색하거나 마이그레이션하지 마세요.
