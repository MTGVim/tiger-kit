---
name: tk-learn
description: "[user] 제공된 경험이나 자료로 재사용 가능한 저장소 또는 사용자 스킬을 만듭니다. 사용자가 명시적으로 호출할 때만 사용합니다."
disable-model-invocation: true
argument-hint: "<대화, 메모, 경로, URL, 워크플로 또는 reflect 후보>"
metadata:
  tigerkit:
    kind: user-invoked
    origin: tigerkit
    relationship: native
---

# 학습

사용자가 이 스킬을 명시적으로 호출할 때만 사용합니다. 자동으로 활성화하거나 다른 사용자 호출형 스킬을 호출하지 마세요.

현재 대화 내용, 메모, 파일/디렉터리, URL, 워크플로 또는 reflect 후보를 받습니다. `repo skill` 또는 `user skill`을 만드세요. 규칙 생성은 범위 밖입니다.

## Workflow

다음 gate를 순서대로 통과시키세요.

1. `evidence`: 입력은 대화·자료·후보 경로이고, 출력은 독립 사례/워크플로, 출처, `verified | unverified`가 연결된 재사용 증거입니다.
2. `dedupe`: 입력은 증거와 기존 repo/user skill 목록이고, 출력은 중복·기본 기능 여부와 `merge | no-op | continue` 판정입니다.
3. `trigger proposal`: 입력은 중복 검토 결과이고, 출력은 대상, 이름, invocation kind, positive/negative trigger입니다.
4. `draft`: 입력은 승인 전 제안과 [스킬 품질](references/skill-quality.md) 기준이고, 출력은 최소 SKILL.md와 example/eval 초안입니다.
5. `approval checkpoint`: 입력은 evidence threshold, 중복 판정, 대상·이름·trigger·초안이고, 출력은 사용자의 명시적 승인 또는 `pending | no-op | Blocked`입니다.
6. `write/report`: 입력은 승인된 적용 범위이고, 출력은 실제 생성 경로 또는 `reported | applied | pending` receipt입니다.

증거 threshold를 충족하지 못하거나 중복·기본 기능·불명확한 trigger이면 skill을 만들지 말고 `no-op` 이유를 보고하세요. 대상/적용 의도가 불분명하면 `.tigerkit/skill-drafts/<skill-name>/` 아래 초안도 사용자 승인 전에는 `pending`으로만 두세요. 초안의 경우 상위 디렉터리는 필요할 때 만들고, 가능하면 원자적으로 교체하며, 자동으로 보관하거나 `.gitignore`를 편집하지 말고, 스크래치가 무시되지 않으면 경고하세요.

## Failure paths

- If 사례가 2개 미만이거나 artifact가 없으면 threshold 미달 근거를 보고하고 `no-op`으로 종료합니다.
- If 필수 출처가 없거나 핵심 사실이 `unverified`면 draft에 넣지 말고 `Unverifiable` 또는 `Blocked`로 종료합니다.
- If 기존 skill 목록을 읽을 수 없으면 dedupe하지 않고 `Unverifiable`로 종료하며, 중복·기본 rule이면 `merge | no-op`으로 종료합니다.
- If positive/negative trigger가 구별되지 않거나 승인이 없으면 draft/write하지 않고 `no-op | pending`으로 종료합니다.
- If write 또는 후속 검증이 실패하면 `applied`로 보고하지 말고 실제 경로·미검증 항목과 함께 `Fail | Blocked`를 보고합니다.

## CHECKPOINT / STOP

증거 threshold, 중복 검색, 대상·이름·trigger를 receipt로 제시한 뒤 사용자의 명시적 승인 전에는 어떤 skill 경로에도 쓰지 마세요. 승인이나 필수 증거가 없으면 `pending`, `no-op` 또는 `Blocked`로 멈추세요.

receipt에 `reported | applied | pending`, evidence threshold 판정, 출처, 미검증 항목, 생성 경로를 구분해 보고하세요. `applied`는 명시적 승인 후 실제로 쓴 경우에만 사용하세요. 사용자 중단은 `aborted`, 필수 증거/대상 충돌은 `Blocked`입니다.

스킬 이름/종류/대상, 생성한 경로, 검증, 남은 우려 사항을 보고하세요.

## DO NOT / ANTI-PATTERNS

- 일회성 사례, 원시 credential·log·screenshot을 재사용 증거로 승격하지 마세요.
- 기존 skill과 동등한 후보를 중복 생성하거나 불명확한 trigger를 발명하지 마세요.
- 승인 전 canonical skill 경로에 쓰거나 자동으로 다른 user-invoked skill을 호출하지 마세요.
