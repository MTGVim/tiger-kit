# env-diff

env-diff는 QA/runtime와 local/runtime를 같은 화면, 같은 context, 같은 viewport에서 비교하는 primary mode입니다.

## Baseline / target

- baseline: QA 또는 배포 runtime
- target: local runtime

## Core checks

- viewport alignment
- overlay/dialog presence
- bounding rect delta
- padding/margin/width/height
- color/opacity/background
- scroll-lock / centering side effect

## Procedure

1. local dev 서버를 확인하거나 기동합니다. profile `env.md`의 local_dev_cmd, tailwind bootstrap, local_url을 기준으로 맞춥니다.
2. baseline_url과 target_url 두 탭을 같은 viewport로 엽니다. driver는 MCP 또는 cdp-direct를 사용합니다.
3. 탭을 식별합니다. baseline은 qa_url 도메인, target은 local_url 기준으로 구분합니다.
4. 로그인합니다. 기법은 엔진의 driver-agnostic 규칙을 따르고, 셀렉터와 자격 정보는 profile `login.md`와 `login.local.md`에서 읽습니다. 필요한 컨텍스트 전환도 profile 기준으로 처리합니다.
5. 대상 화면으로 진입합니다. 화면 정의는 profile `screens/<name>.md`를 따르고, 클릭은 실제 마우스 이벤트 기준으로 수행합니다.
6. 양쪽 탭에서 측정합니다. prop diff를 만들고 다른 값만 보고합니다.
7. 필요하면 스크린샷을 추가해 위치와 육안 차이를 보조 증거로 남깁니다.

## Notes

- 스크린샷은 보조 증거일 뿐이고, 핵심 결론은 computed evidence를 기준으로 둡니다.
- QA root가 landing이면 직접 login path로 진입할 수 있습니다.
