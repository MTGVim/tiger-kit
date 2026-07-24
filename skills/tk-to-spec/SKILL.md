---
name: tk-to-spec
description: "[user/auto] 확인된 결정과 근거를 독립 구현 명세로 작성할 때 사용합니다. 명확한 spec artifact 요청에 적용하고, 티켓 분해·인터뷰·원격 issue·구현 요청에는 적용하지 않습니다."
argument-hint: "<대화, 소스 또는 요청> [--output <경로>|--print-only]"
metadata:
  tigerkit:
    kind: hybrid
    origin: mattpocock/skills
    upstream-skill: to-spec
    relationship: adapted
---

# 명세 작성

명시 호출 또는 구현 명세 artifact를 요구하는 명확한 자연어 요청에 사용하세요. 티켓 분해, 인터뷰, 원격 issue 생성, 구현 요청 또는 active `tk-drive` phase에는 자동으로 활성화하지 마세요.

소스 우선순위: 사용자가 지정한 소스, 현재 결정, 티켓/문서, 관련 코드, 기존 `.tigerkit/spec.md` 순입니다. 인터뷰를 시작하거나, 티켓을 생성하거나, 게시하거나, 구현하지 마세요.

## Workflow

1. `소스 수집`: 입력은 우선순위가 정해진 소스와 기존 명세이고, 출력은 읽은 경로·주장·접근 상태입니다.
2. `source map`: 입력은 소스와 주장이고, 출력은 각 주장의 출처 위치와 `verified | unverified` 상태입니다.
3. `분리·ID`: 입력은 source map이고, 출력은 사실·결정·가정·미해결 충돌 목록과 안정적인 requirement/acceptance ID입니다.
4. `Ready gate`: 입력은 목록과 필수 요소이고, 출력은 `Ready | Draft | Blocked | Unverifiable` 판정 및 누락 근거입니다.
5. `write/print·verify`: 입력은 gate 판정과 출력 모드이고, 출력은 실제 경로 또는 print-only 결과와 재검증된 필수 요소·source map·ID입니다.
6. `receipt`: 입력은 작성/출력 및 검증 결과이고, 출력은 경로·상태·source map·미검증·충돌·검증을 연결한 receipt입니다.

사용자가 지정한 경로에 쓰거나, 출력 전용이면 결과만 출력하고, 그 외에는 `.tigerkit/spec.md`에 작성하세요. 기존 명세가 같은 작업을 다룬다면 유효한 결정을 유지하고, 그렇지 않으면 아카이브 없이 교체하세요. `.tigerkit/`에 출력할 때는 필요할 때만 상위 디렉터리를 만들고, 가능하면 같은 디렉터리의 임시 파일에 쓴 뒤 이름을 바꾸며, 절대 `.gitignore`를 수정하지 말고, 임시 경로가 무시되지 않으면 짧게 경고하세요.

## Failure paths

파일 출력 전 기존 대상 상태를 보존하세요.

| Trigger | Gate/status | Recovery |
|---|---|---|
| 필수 요소 누락 또는 미확정 가정 | `Draft` | 확인된 내용과 누락 항목을 분리하고 `Ready`로 쓰지 않음 |
| confirmed source 간 충돌 또는 사용자 결정 필요 | `Blocked` | 충돌 source 위치와 필요한 결정 하나를 기록하고 write하지 않음 |
| 필수 source 접근 실패 또는 UI literal exact 대조 불가 | `Unverifiable` | 읽지 못한 경로·오류·영향 R/AC를 기록하고 write하지 않음 |
| write/rename 실패 | `Fail` | 손상되지 않은 기존 대상을 유지하고 이번 실행의 변경만 정확히 복원·재검증 |
| post-write gate·source map·R/AC ID 불일치 | `Fail | Unverifiable` | `Ready`·완료로 보고하지 않고 추가 write를 중단해 실패 경로와 실제 상태를 receipt에 기록 |

Write/rename 후 파일을 다시 읽어 gate 판정·source map·requirement/acceptance ID가 작성안과 일치하는지 확인하세요.

## 계약

사용한 소스와 주장을 연결한 `source map`을 만들고 사실, 결정, 가정, 미해결 충돌을 분리하세요. 요구사항에는 `R1`, `R2`처럼 문서 내 고유한 ID를, 인수 기준에는 `AC1`, `AC2`처럼 고유한 ID를 부여하세요. 같은 작업의 기존 명세를 갱신할 때 의미가 유지된 항목의 ID를 재번호하지 말고, 사용자 source에 ID가 있으면 그대로 보존하세요. 삭제된 ID를 다른 의미에 재사용하지 마세요.

버그 source는 `symptom`, `current behavior`, `expected behavior`, `reproduction`, 관찰 evidence, 환경과 regression seam의 존재 여부를 분리하세요. 재현되지 않은 원인이나 해결책을 결정으로 쓰지 말고 `unverified` 가설로 남기며, 재현 명령·fixture 또는 seam이 없으면 그 부재를 검증 계획에 명시하세요.

`Ready`는 문제, 목표, 범위(포함/제외), 요구사항, 인수 기준, 검증, source traceability, verifiability가 있고 미해결 충돌이 없을 때만 사용하세요. 하나라도 없으면 `Draft`, `Blocked` 또는 `Unverifiable`로 남기세요. receipt에는 경로, 상태, `증거/source map`, requirement/acceptance ID, `미검증`, `미해결 충돌`, `검증`을 포함하세요.

### 🔴 HARD GATE · source UI writing

사용자가 제공한 source에 UI writing이 있으면 `source map`에서 별도 inventory로 고정하세요. Label, button name, heading, guide/help copy, table·column name, placeholder, validation/error, status text마다 source 위치와 명세의 destination requirement/acceptance ID를 연결하고 원문을 exact literal로 기록하세요.

사용자가 해당 문구의 변경을 명시적으로 결정하지 않은 한 spelling, 대소문자, 띄어쓰기, 문장부호, 기호, 숫자, 의미 있는 줄바꿈을 그대로 유지하세요. 번역, 의역, 축약, 교정, typo 수정, normalization을 요구사항으로 만들지 마세요. 이미지·스크린샷의 문구를 정확히 판독할 수 없거나 source끼리 literal이 충돌하면 추정하지 말고 `Blocked` 또는 `Unverifiable`로 남기세요.

write/print 후 inventory와 명세의 모든 UI literal을 다시 exact 대조하세요. 승인되지 않은 drift 또는 대조 evidence 부재가 하나라도 있으면 `Ready`로 판정하지 말고 수정·재검증 전에는 downstream 티켓이나 구현 입력으로 넘기지 마세요. 명시적으로 승인된 문구 변경만 source map에 `authorized change`로 표시하세요.

## 🔴 CHECKPOINT · 🛑 STOP Ready 판정 경계

파일에 쓰기 전 필수 요소, 미해결 충돌, UI writing inventory를 확인하세요. 누락·미확정 가정이면 `Draft`, 사용자 결정이 필요한 source 충돌이면 `Blocked`, 필수 source에 접근할 수 없거나 UI literal을 exact 대조할 수 없으면 `Unverifiable`로 남기고 `Ready`로 저장하지 마세요.

## DO NOT / ANTI-PATTERNS

- source map 없이 사실·결정·가정을 섞거나 미해결 충돌을 임의로 선택하지 마세요.
- 제공된 source의 UI writing을 승인 없이 번역·의역·교정·normalization하거나 exact 대조 없이 `Ready`로 만들지 마세요.
- 기존 requirement/acceptance ID를 이유 없이 재번호하거나 삭제된 ID를 다른 의미로 재사용하지 마세요.
- 필수 요소가 빠진 문서를 `Ready`로 표시하거나 구현 완료로 표현하지 마세요.
- 인터뷰, 티켓 생성, 구현, 원격 게시를 이 스킬의 출력에 섞지 마세요. 명세와 티켓을 함께 요청받았더라도 이 명세가 `Ready`가 아니면 downstream 티켓 작성으로 진행하지 마세요.
