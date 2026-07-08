# Browser Verify migration guide

`/tk:browser-verify`는 `/tk:ui-diff`의 cut-over successor입니다. deprecated alias는 유지하지 않고, legacy profile이 남아 있으면 자동 migration 대신 안내 후 중단합니다.

## What changed

- active command: `/tk:ui-diff` → `/tk:browser-verify`
- repo-scoped profile path: `~/.tigerkit/repos/<repo-key>/ui-diff/` → `~/.tigerkit/repos/<repo-key>/browser-verify/`
- helper command: `python3 scripts/tigerkit_state.py browser-verify-paths --repo-root <repo-root>`
- supported modes: `env-diff`, `figma-diff`, `behavior-verify`

## Why TigerKit does not auto-migrate

TigerKit는 legacy profile을 자동 이동하지 않습니다.

이유:
- profile 이동은 credential, login flow, screen catalog 같은 민감/환경 의존 정보를 포함할 수 있습니다.
- rename과 동시에 behavior-verify용 새 field가 추가되어, 무조건 기계적으로 옮기면 잘못된 기본값이 생길 수 있습니다.
- 조용한 새 bootstrap은 기존 operator가 profile을 잃어버렸다고 오해하게 만들 수 있습니다.

그래서 legacy `ui-diff` profile이 감지되면 migration guide를 먼저 보여주고 멈춥니다.

## Migration steps

1. 새 경로를 확인합니다.

```bash
python3 scripts/tigerkit_state.py browser-verify-paths --repo-root <repo-root>
```

2. legacy profile이 있으면 내용을 새 경로로 옮깁니다.

```text
from: ~/.tigerkit/repos/<repo-key>/ui-diff/
to:   ~/.tigerkit/repos/<repo-key>/browser-verify/
```

옮겨야 할 기본 파일:

```text
env.md
login.md
login.local.md
screens/README.md
screens/*.md
```

3. 새 template field를 채웁니다.

- `env.md`
  - `test mutation context`
- `login.md`
  - `session reuse`

4. 다시 실행합니다.

```text
/tk:browser-verify "QA와 로컬 화면 비교"
/tk:browser-verify "이 티켓 기준으로 저장 플로우가 실제로 동작하는지 검증" --mode behavior-verify
```

## Recommended review after migration

- `login.local.md` 경로가 새 `browser-verify` 아래를 가리키는지 확인
- behavior-verify를 쓸 repo라면 `env.md`의 mutation context를 비워두지 말 것
- 2FA/SSO 환경이면 `login.md`의 `session reuse` 필드를 채울 것
- run artifact는 `~/.tigerkit/repos/<repo-key>/browser-verify/runs/` 아래에 쌓이는 기준으로 이해할 것
