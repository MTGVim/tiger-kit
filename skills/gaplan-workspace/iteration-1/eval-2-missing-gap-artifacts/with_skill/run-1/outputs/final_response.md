갭 분석 산출물이 없어 `/tigap:gaplan`을 진행할 수 없습니다.

`/tigap:gaplan`은 먼저 아래 파일을 읽어야 합니다.

```text
.gap/{branch_name}/normalized/source-packet.md
.gap/{branch_name}/analysis/gap-report.md
```

현재는 gap report가 없으므로 작업 목록을 만들면 요구사항과 구현 갭을 추측하게 됩니다. 먼저 다음 명령으로 갭 분석을 실행해 주세요.

```text
/tigap:gap
```

원천 자료가 아직 없다면 자료를 제공하거나, 자료 추출 지시를 주거나, 인터뷰 방식으로 요구사항을 정리한 뒤 갭 분석부터 진행해야 합니다.