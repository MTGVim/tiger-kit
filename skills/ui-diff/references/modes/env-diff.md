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

## Notes

- 스크린샷은 보조 증거일 뿐이고, 핵심 결론은 computed evidence를 기준으로 둡니다.
- QA root가 landing이면 직접 login path로 진입할 수 있습니다.
