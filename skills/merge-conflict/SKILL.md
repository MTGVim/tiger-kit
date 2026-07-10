---
name: merge-conflict
description: conflict 해결 트리거입니다.
---

# Merge Conflict

merge/rebase conflict를 단순 문자열 선택이 아니라 양쪽 intent 기준으로 정리하는 skill입니다.

## Goal

- conflict 상태를 먼저 정확히 파악합니다.
- hunk마다 어느 쪽 intent가 살아야 하는지 설명할 수 있게 합니다.
- 가능한 검증을 돌린 뒤 마무리합니다.

## Process

1. 현재 merge/rebase 상태를 확인합니다.
2. 충돌 파일과 hunk를 목록화합니다.
3. ours/theirs가 각각 무엇을 바꾸려던 건지 주변 코드와 최근 변경으로 추적합니다.
4. hunk별 해결 방안을 정합니다.
5. 필요하면 최소 추가 수정을 해서 일관성을 맞춥니다.
6. 가능한 typecheck/test/lint를 실행합니다.
7. merge/rebase 완료 또는 다음 수동 조치를 보고합니다.

## Boundaries

- `git reset --hard` 금지
- `git clean` 금지
- force push 금지
- 의도 확인 없는 대규모 삭제 금지
- conflict 해결 없이 포매팅/리팩터링으로 범위 확대 금지

## Good use cases

- feature branch merge conflict
- rebase conflict
- generated file과 source file이 엮인 충돌
- 양쪽 다 의미 있는 변경이 들어와 단순 ours/theirs 선택이 위험할 때
