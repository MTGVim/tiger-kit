갭 분석 산출물이 없어 작업 목록을 만들 수 없습니다.

`/tigap:gaplan`은 먼저 다음 파일을 읽어야 합니다.

```text
.gap/{branch_name}/normalized/source-packet.md
.gap/{branch_name}/analysis/gap-report.md
```

현재 gap report가 아직 없으므로, 바로 작업 목록을 생성하지 않고 여기서 중단합니다. 먼저 다음 명령으로 갭 분석 산출물을 만들어 주세요.

```text
/tigap:gap
```

또는 최소한의 원천 자료 수집을 먼저 진행한 뒤 다시 `/tigap:gaplan`을 실행해야 합니다.
