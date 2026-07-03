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
