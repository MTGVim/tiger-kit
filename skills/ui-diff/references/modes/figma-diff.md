# figma-diff

figma-diff는 design node/spec과 local runtime를 비교하는 secondary mode입니다.

## Baseline / target

- baseline: design node / exported design spec
- target: local runtime element

## Validation focus

- width / height
- padding / gap
- font size / weight / line height
- color / opacity
- radius / border

## Notes

- node selection과 runtime element mapping은 반자동일 수 있습니다.
- design source가 incomplete하면 exact parity 대신 explicit ambiguity를 남깁니다.
