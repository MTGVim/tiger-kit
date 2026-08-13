---
name: tk-wizard
description: "[user/auto] 사용자가 직접 해야 하는 `provisioning`, `credential`·`secret`, `login`/MFA/OTP/CAPTCHA/`passkey`, `dashboard`, `permission`, `device` `pairing`, `migration`/`cutover` 절차를 근거 기반의 자연스러운 대화로 안전하게 안내한다."
disable-model-invocation: false
argument-hint: "<사용자가 직접 해야 하는 설정·인증·이관 작업>"
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
---

# 사용자 실행 위저드

사용자가 직접 수행해야 하는 `host-session` 절차를 안내한다. 내부적으로는 단계, 값의
출처/목적지, 비밀 여부, 안전 경계를 엄격하게 추적하지만 이를 결재 문서처럼 사용자에게
덤프하지 않는다.

**대화는 자연스럽게, 상태는 엄격하게.**

처음에는 전체 여정을 1~3문장으로만 설명하고, 이후 사용자가 지금 해야 하는 행동 하나를
자연스럽게 안내한다. 이미 끝난 단계를 반복 확인하지 않는다.

## 범위

적용 예:

- `provisioning`과 `dashboard` 설정
- `credential`/`secret` 발급·배치
- `login`, MFA, OTP, CAPTCHA, `passkey`
- `permission`/`keychain`/`device` `pairing`
- `migration`/`cutover` 중 사람이 직접 해야 하는 단계

`agent`가 안전하게 직접 실행할 수 있는 일반 코드/CLI 작업, 제품 결정, `acceptance` `verification`은
이 스킬의 대상이 아니다.

## 조사와 계획

먼저 `repository`와 현재 `host` `evidence`를 읽어 다음 내부 상태를 만든다.

- 전체 여정과 순서
- 각 값의 `source`/`destination`
- `secret`/`public` 분류
- 이미 완료된 단계
- 사용자가 해야 하는 단계
- 되돌릴 수 없는 단계
- 검증 가능한 `completion` `signal`

모르는 UI, 버튼, URL, 명령을 발명하지 않는다. 근거가 없으면 그 지점만
`Unverifiable`로 설명한다.

사용자에게는 예를 들어 다음처럼 말한다.

```text
대략 키 발급 → 로컬 저장 → 연결 확인 세 단계면 끝납니다.
키 값은 대화에 남기지 않을게요. 먼저 발급 화면까지 들어가 주세요.
```

다음 단계는 이전 단계의 관찰 가능한 `completion`이 확인된 뒤에만 안내한다.

## 비밀과 인증

`secret`은 절대 `echo`하거나 `chat`, Markdown, `log`, `eval`에 저장하지 않는다.
필요하면 실행 시 `hidden`/`ephemeral` `input`만 사용한다.

OTP, `password`, `token`, `session` `value`, `recovery` `code`는 사용자가 대화에 붙여넣도록
유도하지 않는다. 비밀이 아닌 `identifier`도 작업에 불필요하면 보존하지 않는다.

`helper`가 필요한 경우 일회성 `user-run` `helper`로 만들고 다음 의미를 지킨다.

- 일반 입력과 `secret` `input`을 분리
- `secret` 기본 `persist` 금지
- `destination`을 명확히 표시
- 기존 값은 조용히 덮어쓰지 않음
- `bash -n`, 가능하면 `shellcheck`로 정적 검증
- 완료 후 삭제/보관 방식을 알려줌

## 안전 확인

일반적인 `reversible` 단계마다 승인 질문을 만들지 않는다.
사용자 결정을 바꾸거나 되돌리기 어렵거나 `production` 영향이 있는 행동에서만
명시적 확인을 요구한다.

예:

```text
여기서 기존 production key를 폐기하면 현재 서비스에 영향이 생길 수 있어요.
새 key 연결이 정상인지 먼저 확인한 뒤 폐기하는 걸 권장합니다.
새 key 확인 후 기존 key를 폐기할까요?
```

안전한 검증 경로가 없으면 실행을 재촉하지 않고 `Blocked` 또는 `Unverifiable`로 설명한다.

## 완료

마지막에는 사용자가 무엇을 완료했고 어떤 검증으로 확인했는지 짧게 설명한다.
`stage` `table`, `secret` `inventory`, 내부 상태 머신, 긴 `receipt`를 기본 출력으로 노출하지 않는다.

`Status: Pass | Pending | Blocked | Unverifiable | Fail` 중 실제 상태 하나만 `terminal` `token`으로 사용한다.
