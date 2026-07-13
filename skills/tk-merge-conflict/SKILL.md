---
name: tk-merge-conflict
description: "[auto] 양쪽의 의도를 보존하고 결과를 검증하면서 진행 중인 merge 또는 rebase 충돌을 해결합니다."
user-invocable: false
metadata:
  tigerkit:
    kind: model-invoked
    origin: tigerkit
    relationship: native
---

# 병합 충돌 규율

진행 중인 병합/리베이스 상태를 확인하고 충돌 파일과 충돌 구간을 나열한 다음 편집하기 전에 양쪽의 의도를 추적하세요. 가능한 경우 양쪽 의도를 모두 보존하세요. 의도를 뒷받침하는 증거 없이 관련 없는 리팩터링, 형식 변경 남발, 대규모 삭제를 하지 마세요.

파괴적인 reset, clean, force-push 작업은 절대 실행하지 마세요. 진행 중인 충돌만 해결하고 이후 관련 검증을 실행하세요. 상태, 충돌 파일, 의도를 보존한 해결 내용, 검증, 남은 수동 후속 작업을 보고하세요.
