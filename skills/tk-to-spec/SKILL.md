---
name: tk-to-spec
description: "[user] 현재 결정과 근거를 종합해 구현 명세를 작성합니다. 사용자가 명시적으로 호출한 경우에만 사용합니다."
disable-model-invocation: true
argument-hint: "<대화, 소스 또는 요청> [--output <경로>|--print-only]"
metadata:
  tigerkit:
    kind: user-invoked
    origin: mattpocock/skills
    upstream-skill: to-spec
    relationship: adapted
---

# 명세 작성

사용자가 이 스킬을 명시적으로 호출한 경우에만 사용하세요. 자동으로 활성화하지 마세요.

소스 우선순위: 사용자가 지정한 소스, 현재 결정, 티켓/문서, 관련 코드, 기존 `.tigerkit/spec.md` 순입니다. 인터뷰를 시작하거나, 티켓을 생성하거나, 게시하거나, 구현하지 마세요.

Workflow: `소스 수집 → source map → 사실·결정·가정·충돌 분리 → Ready gate → write/print receipt`.

사용자가 지정한 경로에 쓰거나, 출력 전용이면 결과만 출력하고, 그 외에는 `.tigerkit/spec.md`에 작성하세요. 기존 명세가 같은 작업을 다룬다면 유효한 결정을 유지하고, 그렇지 않으면 아카이브 없이 교체하세요. `.tigerkit/`에 출력할 때는 필요할 때만 상위 디렉터리를 만들고, 가능하면 같은 디렉터리의 임시 파일에 쓴 뒤 이름을 바꾸며, 절대 `.gitignore`를 수정하지 말고, 임시 경로가 무시되지 않으면 짧게 경고하세요.

## 계약

사용한 소스와 주장을 연결한 `source map`을 만들고 사실, 결정, 가정, 미해결 충돌을 분리하세요. `Ready`는 문제, 목표, 범위(포함/제외), 요구사항, 인수 기준, 검증, source traceability, verifiability가 있고 미해결 충돌이 없을 때만 사용하세요. 하나라도 없으면 `Draft`, `Blocked` 또는 `Unverifiable`로 남기세요. receipt에는 경로, 상태, `증거/source map`, `미검증`, `미해결 충돌`, `검증`을 포함하세요.

## CHECKPOINT / STOP

파일에 쓰기 전 필수 요소와 미해결 충돌을 확인하세요. 누락·미확정 가정이면 `Draft`, 사용자 결정이 필요한 source 충돌이면 `Blocked`, 필수 source에 접근할 수 없으면 `Unverifiable`로 남기고 `Ready`로 저장하지 마세요.

## DO NOT / ANTI-PATTERNS

- source map 없이 사실·결정·가정을 섞거나 미해결 충돌을 임의로 선택하지 마세요.
- 필수 요소가 빠진 문서를 `Ready`로 표시하거나 구현 완료로 표현하지 마세요.
- 인터뷰, 티켓 생성, 구현, 원격 게시를 이 스킬의 출력에 섞지 마세요.
