요청하신 대로 바로 작업 목록을 만들 수 없습니다.

`/tigap:gaplan`은 먼저 기존 갭 산출물을 읽어야 하는데, 현재 입력 파일이 제공되지 않았고 필요한 산출물도 확인되지 않았습니다.

필수 입력:

```text
.gap/{branch_name}/normalized/source-packet.md
.gap/{branch_name}/analysis/gap-report.md
```

따라서 지금 단계에서는 작업 목록이나 `.gap` 산출물을 생성하지 않고 중단합니다.

다음 중 하나를 먼저 진행해 주세요.

1. `/tigap:gap`을 실행해 원천 자료 정규화와 갭 보고서를 생성합니다.
2. 이미 만든 `source-packet.md`와 `gap-report.md`가 있다면 해당 `.gap/{branch_name}/` 산출물 위치를 알려주세요.
3. 원천 자료가 아직 없다면 최소한의 자료 수집부터 진행할 수 있도록 요구사항이나 참고 자료를 제공해 주세요.