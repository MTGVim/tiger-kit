# 같은 소스의 평가 편차 측정

`scripts/run_skill_evals.py --calibrate-noise`는 유지보수자가 명시적으로 선택하는 `A/A` 모드입니다.
동일한 커밋의 두 격리 소스를 같은 호스트·모델·설정·평가 계약으로 실행합니다. 기본 `A/B` 실행,
반복 횟수, 판정과 `--diagnose`는 바뀌지 않습니다. `tk-grooming`이 이 모드를 자동 실행하지 않습니다.

먼저 `--dry-run`으로 실제 선택 범위와 호출 예산을 확인합니다. `--runs`는 이 모드에서 사례별
쌍의 수이며, 각 호스트·사례에서 `A`→`B`, `B`→`A` 순서로 번갈아 실행합니다. 작은 시범 실행에서는
한 호스트와 한 사례를 선택합니다. 사례 필터가 없으면 선택 스킬과 전체 카탈로그도 실행하므로
계획에 표시된 호출 예산을 확인해야 합니다.

```bash
python3 scripts/run_skill_evals.py \
  --baseline <frozen-sha> --candidate <same-frozen-sha> \
  --host codex --skill tk-browser-verify \
  --case tk-browser-verify:behavior:browser-contact-sheet-cannot-prove-pass \
  --runs 2 --calibrate-noise --dry-run
```

실제 실행에는 기존과 같이 `--adapter-command`와 `--grader-command`를 지정합니다.
`--diagnose`는 프롬프트 계약이 다르므로 별도 실행합니다. 고정된 대규모 표본 의무는 없으며,
작은 표본으로 유의성이나 안정적인 노이즈 하한을 입증했다고 주장하지 않습니다.

기존 `summary.json`의 선택적 `noise_calibration`과 두 `records` 파일에 결과를 저장합니다.
각 레코드에는 `arm`, `pair`/`position`, 프롬프트 해시, 관측된 모델·설정·출처, `assertion` 결과,
`terminal` `status`, `events`와 가능한 `token`/`time`/`tool`/`cost` 값을 남깁니다. 원시 로그나 사용자
개인정보를 추가 저장하지 않습니다. 요약의 `assertion_passed`는 평가 `assertion`을 통과한
횟수이며 실제 과업 완료나 `phase` 준수와 동일하다고 해석하지 않습니다. 그 구분은 기존
개별 `assertion`과 `events` 및 독립된 과업 검증 증거에서 확인합니다.

각 호스트·사례·`arm`의 관측 범위와 총량, 누락 수를 별도로 보고합니다. 누락된 비용을 0으로
추정하거나 서로 다른 사례·모델의 분산을 하나로 합치지 않습니다. 미완료 실행은 제거하지
않고 `Unverifiable`로 남깁니다. 어느 `arm`에서든 보호된 `safety`/`authority` `assertion`이 실패하면
보정 결과는 `Fail`이며, 이후 실행 중단이나 출처 누락으로도 이 실패를 완화하지 않습니다.

두 체크아웃은 실행 전에 `commit`/`tree`와 추적 파일의 내용·실행 비트 해시가 일치해야 합니다.
각 일회성 실행 소스도 이 고정 입력과 대조합니다. `adapter`/`grader` 명령 및 직접 참조한 파일의
해시는 실제 실행 디렉터리에서 실행 전후에 비교합니다. 행위자가 상대 경로의 채점기를
바꾸면 변조된 `judge`만 실행하지 않고 독립적인 기계 검사는 계속 수행합니다. 채점하지 못한
`judge`는 `passed: null`로 남기며 실제로 관측한 보호 위반과 구분합니다. 채점기가 실행 중 자신을
바꾼 경우에도 보정 근거에서 제외하며, 이미 확인한 보호 위반은 계속 `Fail`입니다. 외부 명령이 불러오는 모든 전이 의존성이나 설정까지 자동으로
증명하지는 못하므로 해당 환경의 변경 여부도 통제해야 합니다.

사용자 정의 `adapter`의 선택적 `execution_source`는 **호스트에서 독립적으로 관측한** 실제
선택 소스를 반환해야 합니다. 필드는 `commit`, `tree`, `files_sha256`, `checkout_id`와
`selector_status: observed`입니다. `scripts/eval_source.py`의 `source_snapshot`과
`checkout_id`로 표현 형식을 맞출 수 있지만, 요청한 `checkout`을 그대로 되풀이한 값이나
모델의 자기 보고는 선택 증명이 아닙니다. 실제 호스트의 완료된 실행 메타데이터와 연결해야 합니다.
`runner`가 관측한 `expected_source`와 일치하지 않거나 호스트의 격리·`fixture` 로딩 증거가
없으면 `Unverifiable`입니다. 기본 `adapter`는 설치 소스를 `installed`로만 관측하므로
실제 선택 증명이 추가되기 전까지 `A/A` 개선 근거로 사용할 수 없습니다.

모든 결과의 `change_verdict`는 `not-applicable`입니다. 이 모드는 무변경 편차의 기술 통계만
제공합니다. 이후 `A/B`와 조건이 같을 때만 비교 자료로 참고하고, 관측 편차 안의 차이를 개선
입증으로 설명하지 않습니다. 이 보정은 기존 `A/B` 결과를 자동 승격하거나 실패를 면제하지 않습니다.
