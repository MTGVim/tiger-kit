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

기존의 네 영역, 즉 저장소 규칙, 저장소 스킬, 사용자 규칙, 사용자 스킬을 검사하세요. 실제로 존재하는 호스트 네이티브 경로를 사용하세요. [탐색](references/discovery.md)에 후보가 나열되어 있습니다. 누락된 파일을 만들거나 레거시 전역 TigerKit 상태를 검사/마이그레이션하지 마세요.

중복, 모순, 구식, 끊어진 참조, no-op, 과도하게 긴 내용, 잘못된 범위/종류, 트리거 충돌, 죽은 스킬, 오래된 예시 또는 누락된 출처로 분류하세요. `keep | tighten | merge | split | move | convert | deprecate | delete | fix` 중 하나를 제안하세요.

기본은 보고만 수행합니다. 명시적인 요청이 있을 때만 적용하세요. 적용 시 원본을 다시 읽고, 삭제 전에 참조를 검색하고, 관리되거나 자동 생성된 콘텐츠의 소유권 표기를 보존하며, 광범위한 저장소/사용자 변경을 조용히 섞지 마세요. 편집 후 링크, 중복, frontmatter를 다시 확인하세요. 지식을 지어내거나 회고/학습을 대신하지 마세요.

발견 사항, 제안 작업, 적용 내용, 검증을 출력하고 빈 섹션은 생략하세요.
