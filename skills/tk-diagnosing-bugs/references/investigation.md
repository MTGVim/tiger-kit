# 조사 루프

```text
feedback loop
→ reproduce
→ minimize
→ ranked hypotheses
→ instrument
→ fix
→ regression verification
→ cleanup
```

가설 전에 red-capable feedback loop를 만들고 최소 한 번 실행하세요. 빠르고 반복 가능한 신호를 우선하고 탐색마다 변수 하나만 바꾸세요. 3~5개 가설에 반증 가능한 예측을 붙이고 관찰 결과로 제거하세요.

올바른 public regression seam이 있으면 최소 재현을 test로 고정하고 `red → fix → green → 원래 reproduction` 순서로 확인하세요. seam이 없으면 얕은 test를 만들지 말고 후속 구조 작업으로 기록하세요. 임시 계측과 throwaway artifact는 제거하세요.

충실하게 재현할 수 없다면 추측 patch를 하지 말고 시도한 방법과 부족한 환경 또는 artifact를 보고하세요.
