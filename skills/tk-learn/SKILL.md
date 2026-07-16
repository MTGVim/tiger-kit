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

## 계약

다음 gate를 순서대로 통과시키세요.

1. 반복 가능한 증거를 수집하세요. 동일한 동작이 서로 독립된 두 사례에서 나타났는지, 또는 재사용을 입증하는 명시적 워크플로와 corroborating artifact가 있는지 적고, 출처와 `verified | unverified`를 연결하세요. 일회성 사례나 원시 자격 증명·로그·screenshot은 승격 근거로 쓰지 마세요.
2. 기존 repo/user skill과 중복을 검색하고, 기본 모델 기능이나 짧은 standing rule로 충분한지 검사하세요. 동등한 skill이 있으면 새 skill 대신 `merge` 또는 `no-op`을 제안하세요.
3. 대상(`repo skill` 또는 `user skill`), 이름, invocation kind, positive/negative trigger를 제안하세요. trigger가 명시되지 않으면 생성하지 마세요.
4. 자체 완결적인 최소 SKILL.md와 최소 example 또는 eval을 제안하세요. [스킬 품질](references/skill-quality.md)을 기준으로 삼고, 필요한 경우에만 기존 skill-local references/scripts를 사용하세요.
5. 사용자가 대상·이름·초안과 적용 범위를 명시적으로 승인하기 전에는 확정하거나 실제 경로에 쓰지 마세요. 침묵, 계속 진행, 과거 유사 답변은 승인으로 취급하지 않습니다.

증거 threshold를 충족하지 못하거나 중복·기본 기능·불명확한 trigger이면 skill을 만들지 말고 `no-op` 이유를 보고하세요. 대상/적용 의도가 불분명하면 `.tigerkit/skill-drafts/<skill-name>/` 아래 초안도 사용자 승인 전에는 `pending`으로만 두세요. 초안의 경우 상위 디렉터리는 필요할 때 만들고, 가능하면 원자적으로 교체하며, 자동으로 보관하거나 `.gitignore`를 편집하지 말고, 스크래치가 무시되지 않으면 경고하세요.

## CHECKPOINT / STOP

증거 threshold, 중복 검색, 대상·이름·trigger를 receipt로 제시한 뒤 사용자의 명시적 승인 전에는 어떤 skill 경로에도 쓰지 마세요. 승인이나 필수 증거가 없으면 `pending`, `no-op` 또는 `Blocked`로 멈추세요.

receipt에 `reported | applied | pending`, evidence threshold 판정, 출처, 미검증 항목, 생성 경로를 구분해 보고하세요. `applied`는 명시적 승인 후 실제로 쓴 경우에만 사용하세요. 사용자 중단은 `aborted`, 필수 증거/대상 충돌은 `Blocked`입니다.

스킬 이름/종류/대상, 생성한 경로, 검증, 남은 우려 사항을 보고하세요.

## DO NOT / ANTI-PATTERNS

- 일회성 사례, 원시 credential·log·screenshot을 재사용 증거로 승격하지 마세요.
- 기존 skill과 동등한 후보를 중복 생성하거나 불명확한 trigger를 발명하지 마세요.
- 승인 전 canonical skill 경로에 쓰거나 자동으로 다른 user-invoked skill을 호출하지 마세요.
