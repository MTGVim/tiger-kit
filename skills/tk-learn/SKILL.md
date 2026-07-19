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
4. `draft`: 입력은 승인 전 제안과 [스킬 품질](references/skill-quality.md) 기준이고, 출력은 최소 SKILL.md, trigger train/validation, success/boundary assertion, baseline 계획, portable-core/host-extension 판정입니다.
5. `approval checkpoint`: 입력은 evidence threshold, 중복 판정, 대상·이름·eval·compatibility 초안이고, 출력은 사용자의 명시적 승인 또는 `pending | no-op | Blocked`입니다.
6. `write/verify/report`: 입력은 승인된 적용 범위와 대상의 write 전 존재 여부·내용이고, 출력은 이름·종류·대상, 실제 경로, target-host validation, 남은 우려 사항과 이를 참조하는 `reported | applied | pending` receipt입니다.

증거 threshold를 충족하지 못하거나 중복·기본 기능·불명확한 trigger, success/boundary assertion, baseline 비교 또는 target-host compatibility이면 skill을 만들지 말고 `no-op` 이유를 보고하세요. 대상/적용 의도가 불분명하면 `.tigerkit/skill-drafts/<skill-name>/` 아래 초안도 사용자 승인 전에는 `pending`으로만 두세요. 초안의 경우 상위 디렉터리는 필요할 때 만들고, 가능하면 원자적으로 교체하며, 자동으로 보관하거나 `.gitignore`를 편집하지 말고, 스크래치가 무시되지 않으면 경고하세요.

쓰기 실패 시 기존 대상을 그대로 보존하고 이번 실행이 만든 임시 파일만 정리한 뒤 `pending`으로 보고하세요. 작성 후 frontmatter·link·eval·target-host validation이 실패하면 `applied`로 표시하지 마세요. Write 직전 상태를 정확히 복원하고 재검증할 수 있을 때만 이번 실행의 변경을 되돌리고, 복원 또는 재검증이 불가능하면 실제 경로와 실패 증거를 남긴 채 `Fail | Blocked | Unverifiable`로 멈추세요.

## CHECKPOINT / STOP

증거 threshold, 중복 검색, 대상·이름·trigger validation, behavior assertions, baseline 계획, compatibility 판정을 approval summary로 제시한 뒤 사용자의 명시적 승인 전에는 어떤 skill 경로에도 쓰지 마세요. 승인이나 필수 증거가 없으면 `pending`, `no-op` 또는 `Blocked`로 멈추세요.

Receipt에는 `reported | applied | pending`, evidence threshold 판정, 출처, 미검증 항목과 최종 보고 필드의 참조만 기록하세요. 생성 경로와 검증 본문은 Receipt에 복사하지 마세요. `applied`는 명시적 승인 후 실제로 쓴 경우에만 사용하세요. 사용자 중단은 `aborted`, 필수 증거/대상 충돌은 `Blocked`입니다.

스킬 이름/종류/대상, 생성한 경로, 검증, 남은 우려 사항을 각각 한 번만 보고하고 Receipt는 이 필드들을 참조만 하세요.

## DO NOT / ANTI-PATTERNS

- 일회성 사례, 원시 credential·log·screenshot을 재사용 증거로 승격하지 마세요.
- 기존 skill과 동등한 후보를 중복 생성하거나 불명확한 trigger를 발명하지 마세요.
- 승인 전 canonical skill 경로에 쓰거나 자동으로 다른 user-invoked skill을 호출하지 마세요.
