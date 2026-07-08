# figma-diff

figma-diff는 design node/spec과 local runtime를 비교하는 secondary mode입니다.

## Baseline / target

- baseline: design node / exported design spec
- target: local runtime element

## Validation focus

- typography: `fontWeight`, `fontSize`, `lineHeight`
- geometry: `width`, `height`, `padding`, `gap`, `borderRadius`, `borderWidth`
- color: `backgroundColor`, `color`, `borderColor`, `borderWidth`, `opacity`

## Match gate

- typography / geometry가 design spec과 맞아도 color 축(`backgroundColor`, `color`, `borderColor`, `borderWidth`)을 확인하기 전에는 `match`, `identical`, `일치` 같은 결론을 내리지 않습니다.
- color 축은 computed value 기준으로 확인하고, background / text / border 중 어떤 color 필드를 확인했는지 결과에 남깁니다.
- 다른 값만 보고하되 color-only regression은 생략하지 않습니다.

## Notes

- node selection과 runtime element mapping은 반자동일 수 있습니다.
- design source가 incomplete하면 exact parity 대신 explicit ambiguity를 남깁니다.
- 최종 요약에는 최소한 `color-axis checked` 여부를 포함합니다.
