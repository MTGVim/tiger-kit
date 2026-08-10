---
name: tk-wizard
description: "[user/auto] 사용자가 직접 수행해야 하는 provisioning, credential·secret, login/MFA/OTP/CAPTCHA/passkey, dashboard 클릭, permission/keychain, device pairing, migration/cutover 절차를 조사하고 안전한 ephemeral wizard 단계로 정리한다. agent가 실행 가능한 작업, decision/approval, acceptance verification에는 사용하지 않는다."
disable-model-invocation: false
argument-hint: "<host-session 절차>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
---

# 사용자 실행 wizard

사용자가 해야 하는 host-session 절차만 다룬다. 먼저 repository와 host를 조사하고
stage, 값, 출처, 목적지, secret/public을 inventory한 뒤 **stage 목록을 먼저 보여주고
확인**받는다. 모르는 UI·명령은 발명하지 않는다. 각 stage는 stranger가 따라 할 수 있는
한 가지 작업이며, URL을 먼저 열고 정확한 클릭·복사 경로를 쓴다.

## Helper vocabulary

생성하는 shell은 다음 의미의 helper를 사용한다: `stage`(진행/화면 전환), `say`/`step`(설명),
`open_url`(URL 열기), `ask`(일반 입력), `ask_secret`(hidden input), `write_env`(idempotent
`.env` 기록), `set_secret`/`set_var`(CI 저장), `pause`(사용자 대기), `confirm`(명시 승인).
secret은 절대 echo하거나 기본 persist하지 않는다. irreversible action 전에는 `confirm`한다.

기본은 한 번 실행하고 삭제하는 ephemeral user-run이다. agent는 browser/human input flow를
end-to-end 실행하지 않으며, capture-to-destination trace와 안전한 handoff만 출력한다.
생성 shell은 `bash -n` 및 가능하면 `shellcheck`으로 정적 검사하고, 실행 권한과 모든 값의
최종 목적지를 확인한다. host/UI evidence가 없으면 정확히 `Unverifiable` 또는 `Blocked`로
중단한다. credential은 eval이나 출력에 넣지 않는다.

## 절차

1. `.env*`, README, config, workflow와 host capabilities를 읽는다.
2. stage 목록과 각 값의 source/destination/secret 여부를 제시하고 사용자 확인을 받는다.
3. 확인된 stage만 helper로 작성하고, 누락된 evidence는 질문한다.
4. static validation 결과, 실행 명령, 삭제/보관 handoff를 제공한다.

Upstream adapted from Matt Pocock's `wizard` skill, retrieved 2026-08-11:
`https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/wizard/SKILL.md`.
