# 브라우저 안전성

안전한 환경과 명시적 권한이 없으면 payment, 외부 communication,
되돌릴 수 없는 삭제, production-data mutation, account change, permission
change 또는 동등한 side effect를 일으키지 않습니다. approved UI 상태에는
sending, saving, paying보다 정확한 repository 근거 기반 response mock을
우선합니다.

Headless-only는 절대 규칙입니다. Interactive authentication에도 visible-browser
exception은 없습니다. 일반적인 chat에서 secret을 요청하거나 secret-bearing
value/명령을 prompts, 출력, 장부, logs, screenshots, HAR, console
캡처, receipts에 넣지 않습니다. 사용 가능한 임시 secret 입력 channel만
사용하고 non-sensitive auth-mode 사실만 기록합니다.

screenshots/video와 network/HAR/console inventory를 분리합니다. Authorization,
cookies, tokens, credentials, sensitive bodies가 있으면 캡처는 sensitive입니다.
검증된 redaction과 원본 및 이동 경로에 잔여물이 없음을 확인한 뒤에만
사용합니다. 그렇지 않으면 소유한 캡처를 안전하게 삭제하고 `Unverifiable` 을
반환합니다.

user screenshot, fixture, profile 또는 소유권을 알 수 없는 산출물을 절대
move/delete하지 않습니다. 근거 처리를 위해 `.gitignore` 를 절대
수정하지 않습니다.
