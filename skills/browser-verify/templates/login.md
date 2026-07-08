# login.md

기본 login 절차를 적습니다.

## selectors

- username: <input selector>
- password: <input selector>
- submit: <button selector>
- post_login_ready: <selector or text that proves login succeeded>
- optional_modal_close: <selector or NONE>

## flow

1. 로그인 페이지로 이동합니다.
2. username / password를 채웁니다.
3. submit을 클릭합니다.
4. post_login_ready가 보일 때까지 기다립니다.

## notes

- 2FA / captcha / SSO가 있으면 우회 불가 단계를 적습니다.
- baseline/local의 selector 차이가 크면 차이를 적습니다.

## session reuse

2FA(OTP / SSO) 환경에서 1회 수동 로그인 후 세션을 재사용하는 설정입니다. 엔진의 Auth session reuse 규칙을 따릅니다.

- session_reuse: <yes | no>
- session_profile_dir: <~/.tigerkit/repos/<repo-key>/browser-verify/browser-profile or NONE>
- manual_login_steps: <OTP / SSO 등 최초 1회 사용자 개입이 필요한 단계>
- expiry_signal: <세션 만료 판별 신호. 예: 로그인 페이지 redirect, 401 응답>
