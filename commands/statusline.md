---
description: steer/reflect indicator를 statusline 또는 trailing으로 어디에 표시할지 설정합니다.
---

이 명령은 아래 계약을 직접 따릅니다.

사용자에게는 한글로 답합니다. 코드, 명령어, 파일 경로, 식별자는 원문 그대로 유지할 수 있습니다.

목표: steer/reflect indicator delivery mode를 설정합니다. 기본은 trailing이며, statusline을 쓰면 토큰 사용을 줄일 수 있습니다.

## 지원 형태

```text
/tk:statusline
/tk:statusline install
/tk:statusline remove
/tk:statusline trailing
/tk:statusline trailing on
/tk:statusline trailing off
```

## 의미

- `install`: statusline 표시 활성화
- `remove`: statusline 표시 제거
- `trailing`: 현재 trailing 설정과 예시 보여주기
- `trailing on`: 메시지 맨 아래 trailing badge 표시
- `trailing off`: trailing badge 비활성화

기본 정책:
- trailing이 default
- statusline은 token-saving 옵션

## badge 규칙

- steer only -> `[🛞]`
- reflect pending only -> `[🪞 2]`
- both -> `[🛞 / 🪞 2]`
- none -> 숨김

`🪞` 숫자는 reflect candidate pending count입니다. durable reflect write count가 아닙니다.

## 출력

```text
indicator 설정 확인했습니다.
- default: trailing
- preview: [🛞], [🪞 2], [🛞 / 🪞 2]

다음 추천: /tk:statusline trailing on
```

## 금지

- 본문과 섞여 상태 의미가 흐려지는 긴 설명
- reflect 상태를 durable write 완료처럼 오해시키는 문구