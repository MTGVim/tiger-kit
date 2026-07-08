# env.md

현재 repo의 browser-verify profile에서 runtime endpoint, viewport, 실행 컨텍스트를 적습니다.

## local runtime

- local_url: <http://127.0.0.1:3000>
- local_dev_cmd: <yarn dev>
- local_ready_signal: <ready on http://127.0.0.1:3000>
- local_notes: <tailwind bootstrap / mock server / seed step>

## baseline runtime

- baseline_url: <https://qa.example.com>
- baseline_notes: <qa / staging / prod-like>

## viewport

- width: 1440
- height: 900
- device_scale_factor: 1

## auth / context

- requires_login: yes
- default_user_role: <admin | member | guest>
- seed_or_fixture: <account or fixture name>
- context_notes: <feature flag / locale / org selector>

## test mutation context

behavior-verify가 실제 mutation(저장 / 삭제 등)을 실행해도 되는 범위입니다. 비어 있으면 mutation 유발 상호작용은 차단되고 해당 항목은 unverifiable로 보고됩니다.

- mutation_allowed: <yes | no>
- test_account: <mutation 허용 계정 식별자 or NONE>
- test_scope: <테스트 조직 / 매장 / 프로젝트 등 데이터 범위 식별자 or NONE>
- irreversible_notes: <외부 발송·결제 등 테스트 컨텍스트 안에서도 절대 실행하면 안 되는 항목>
