# Browser 안전성

safe environment와 명시적 authority가 없으면 payment, external communication,
irreversible deletion, production-data mutation, account change, permission
change 또는 동등한 side effect를 일으키지 않습니다. approved UI state에는
sending, saving, paying보다 exact repository-evidenced response mock을
우선합니다.

Headless-only는 절대 규칙입니다. Interactive authentication에도 visible-browser
exception은 없습니다. ordinary chat에서 secret을 요청하거나 secret-bearing
value/command를 prompts, output, ledgers, logs, screenshots, HAR, console
capture, receipts에 넣지 않습니다. 사용 가능한 ephemeral secret-input channel만
사용하고 non-sensitive auth-mode fact만 기록합니다.

screenshots/video와 network/HAR/console inventory를 분리합니다. Authorization,
cookies, tokens, credentials, sensitive bodies가 있으면 capture는 sensitive입니다.
verified redaction과 original 및 moved-path residue 부재를 확인한 뒤에만
사용합니다. 그렇지 않으면 owned capture를 안전하게 삭제하고 `Unverifiable` 을
반환합니다.

user screenshot, fixture, profile 또는 ownership을 알 수 없는 artifact를 절대
move/delete하지 않습니다. evidence handling을 위해 `.gitignore` 를 절대
수정하지 않습니다.
