# env.md

현재 repo의 UI diff profile에서 runtime endpoint, viewport, 실행 컨텍스트를 적습니다.

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
