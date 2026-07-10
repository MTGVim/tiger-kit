# env-diff

env-diff는 QA/runtime와 local/runtime를 같은 화면, 같은 context, 같은 viewport에서 비교하는 primary mode입니다.

## Baseline / target

- baseline: QA 또는 배포 runtime
- target: local runtime

## Core checks

- viewport alignment
- overlay/modal presence
- native dialog readiness / occurrence
- bounding rect delta
- typography: `fontWeight`, `fontSize`, `lineHeight`
- geometry: `borderRadius`, `padding`, `width`, `height`, `justifyContent`
- color: `backgroundColor`, `color`, `borderColor`, `borderWidth`, `opacity`
- scroll-lock / centering side effect

## Procedure

1. local dev 서버를 확인하거나 기동합니다. profile `env.md`의 local_dev_cmd, tailwind bootstrap, local_url을 기준으로 맞춥니다.
2. baseline_url과 target_url 두 탭을 같은 viewport로 엽니다. driver는 MCP 또는 cdp-direct를 사용합니다.
3. 탭을 식별합니다. baseline은 qa_url 도메인, target은 local_url 기준으로 구분합니다.
4. 로그인합니다. 기법은 `commands/browser-verify.md`의 driver-agnostic 규칙을 따르고, 셀렉터와 자격 정보는 profile `login.md`와 `login.local.md`에서 읽습니다. 필요한 컨텍스트 전환도 profile 기준으로 처리합니다.
5. 대상 화면으로 진입합니다. 화면 정의는 profile `screens/<name>.md`를 따르고, 클릭은 실제 마우스 이벤트 기준으로 수행합니다.
5.2. trusted 클릭 / 활성화 / submit이 native dialog를 유발할 수 있으면 dialog handler를 먼저 준비합니다.
   - 대상은 `alert`, `confirm`, `beforeunload`입니다.
   - native dialog 대응과 overlay/modal 판별은 별도 경우로 다룹니다.
   - dialog가 뜨면 가능한 한 즉시 `accept` 또는 `dismiss`로 해제합니다.
   - `dialog opened` 같은 중간 상태로 멈춘 뒤 뒤늦게 대응하는 흐름은 피합니다.
5.5. baseline 측정 방식을 먼저 정합니다.
   - baseline 요소가 실제 runtime에 렌더돼 있으면 그 live rendered element를 직접 측정하는 것을 1순위로 둡니다.
   - class 주입 probe는 fallback으로만 사용합니다.
   - fallback probe를 쓸 때는 `variant` class만 따로 넣지 말고, 소비처에서 실제로 붙는 전체 `className`을 그대로 사용합니다.
   - probe 결과는 inline style / cascade / override를 완전히 담지 못하는 low-trust 측정으로 표시합니다.
   - baseline 출처나 타입은 commit message/라벨보다 pre-change source, 예: `git show <base>:<file>`와 그 렌더 근거를 우선 확인합니다.
6. 양쪽 탭에서 측정합니다. prop diff를 만들되 아래 순서를 지킵니다.
   - typography / geometry / color 3축을 모두 확인합니다.
   - typography / geometry가 맞아도 color 축 확인 전에는 `match`, `identical`, `일치` 결론을 내리지 않습니다.
   - color 축은 computed value 기준으로 확인하고, `backgroundColor`, `color`, `borderColor`, `borderWidth` 중 어떤 필드를 확인했는지 결과에 남깁니다.
   - 다른 값만 보고하되 color-only regression은 생략하지 않습니다.
7. 필요하면 스크린샷을 추가해 위치와 육안 차이를 보조 증거로 남깁니다.

## Notes

- 스크린샷은 보조 증거일 뿐이고, 핵심 결론은 computed evidence를 기준으로 둡니다.
- 최종 요약에는 최소한 color-axis checked 여부를 포함합니다.
- fallback probe를 썼다면 최종 요약에 low-trust baseline 측정이었다는 점을 같이 남깁니다.
- native dialog가 개입했다면 어떤 dialog를 `accept`/`dismiss`했는지 최종 요약에 남깁니다.
- QA root가 landing이면 직접 login path로 진입할 수 있습니다.
