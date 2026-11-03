<a id="empirical-diagnosis-method"></a>
# 경험적 진단 방법

입력에서 정확히 하나의 대상과 사고를 식별한 뒤에만 이 참조를 읽습니다. 이는 광범위한 최적화가 아니라 인과 진단을 위한 경험적 프롬프트 조정입니다.

<a id="1-static-coherence"></a>
## 1. 정적 일관성

새로운 실행 전에 frontmatter description과 본문을 비교합니다.

- 긍정·부정 트리거를 비교합니다.
- 능력과 출력 약속을 비교합니다.
- 승인, 변경, 실패와 복구 담당자를 비교합니다.

description에만 있는 약속, 본문에만 있는 동작이나 충돌하는 담당자는 가설입니다. 정적 일관성만으로 런타임 원인을 입증하지는 못합니다.

<a id="2-freeze-the-smallest-deciding-set"></a>
## 2. 판단에 필요한 최소 집합 고정

실험 전에 다음을 고정합니다.

```text
Incident: observed prompt and expected/observed result
Control: nearest adjacent behavior that distinguishes the suspected cause
Must preserve: critical behavior, safety, routing, authority, and host boundaries
Metric: actual anchor, labeled proxy, or unavailable
```

첫 사고·대조군 쌍으로 실패 계층을 구별할 수 없을 때만 시나리오를 추가합니다. 일반적인 holdout은 선택 사항이며 기본 의례가 아닙니다.

<a id="3-fresh-execution"></a>
## 3. 새로운 실행

조건이 일치하는 깨끗한 맥락에서 사고를 한 번 실행합니다. 결과가 불안정하거나 지표 임계값에 가깝거나 대조군과의 구별이 모호할 때만 반복합니다. 진단이나 후보를 이미 본 실행자는 새로운 실행자가 아닙니다.

정상 결과물을 우선합니다. adapter가 진단 suffix를 지원할 때만 다음을 수집합니다.

```json
{
  "trace": {
    "understanding": "ok | stuck | skipped",
    "planning": "ok | stuck | skipped",
    "execution": "ok | stuck | skipped",
    "formatting": "ok | stuck | skipped"
  },
  "unclear_points": [
    {
      "issue": "observed event",
      "cause": "candidate cause",
      "general_fix_rule": "class-level prevention rule"
    }
  ],
  "discretionary_fill_ins": [],
  "retries": 0
}
```

실행자에게 예상 답변, 판정 기준이나 변경 전 기준·후보의 판정을 공개하지 않습니다. 잘못된 진단은 평가 계층의 근거이며 검증된 결과물을 자동으로 무효화하지 않습니다.

<a id="4-two-sided-evidence"></a>
## 4. 양면 근거

다음을 결합합니다.

- 결정론적 assertion과 Git·경로·런타임 근거를 결합합니다.
- 선택·로드와 호스트·adapter 이벤트를 결합합니다.
- 단계별 trace와 재량으로 채운 내용을 결합합니다.
- 이용할 수 있으면 실제 토큰, 소요 시간, 도구, 중첩 호출이나 재시도 지표를 결합합니다.

자기 보고는 관찰 하나이며 원인을 입증하기에 충분하지 않습니다. 모든 인과 주장에는 지침, 라우팅, 런타임, 저장소나 평가 기준점이 필요합니다. 사용자에게 보이는 전달 사고에서는 에이전트 맥락을 전달 근거로 사용하기 전에 접근 가능한 현재 세션의 출력 텍스트와 블록·표시 메타데이터를 확인합니다. 접근 한계를 기록합니다. 숨겨진 추론이나 무관한 로그를 읽지 않습니다. 표시 계약이나 보이는 payload 없이 블록 유형만으로 사용자가 무엇을 봤는지 입증할 수는 없습니다.

<a id="5-minimal-experiment"></a>
## 5. 최소 실험

사고·대조군 근거만으로 원인을 직접 입증할 수 없을 때만 실행 소유의 격리 checkout을 사용합니다. 의심하는 원인과 이를 구별할 예상 결과를 먼저 밝힙니다. 근본 원인 주제 하나를 바꾸고 영향받는 최소 시나리오를 실행합니다.

실험은 인과를 확인하거나 기각하며 정본 패치가 아닙니다. 두 번째 실험에는 첫 결과에서 배운 새로운 구체적 원인이 필요합니다. 같은 실패가 반복된 뒤 문구 변경을 쌓지 않습니다.

<a id="6-disposition"></a>
## 6. 처리 방향

- 검증된 스킬 목표에는 간결하고 한정된 예방 제안을 제시합니다.
- 독립적으로 유용한 새 스킬에는 스킬 후보를 제안합니다.
- grader/harness/fixture 결함은 `eval-owner`로 분류합니다.
- loader/adapter/host 결함은 `host-owner`로 분류합니다.
- 독립적으로 검증된 소비자 override·설정은 `local-only`로 분류합니다. 공유 스킬 수정 대신 저장소만 고치는 대안이 아닙니다.
- 재현되지 않았거나 대상이 올바르면 `no-change`로 분류합니다.
- 결정적 근거가 없으면 `unverifiable`로 분류하고, 담당자와 판단할 확인을 포함한 가설 독립적 예방책이나 그러한 예방책이 없는 이유를 함께 제시합니다. 승인된 현재 세션 범위에서 접근할 수 있으면 결정적 근거를 먼저 확보하려고 시도합니다. 원인이 없다는 사실만으로 예방 평가 없이 종료할 수는 없습니다.

스킬 수준 사고에는 개인 에이전트 memory 쓰기나 현재 저장소에만 적용하는 우회책 대신 담당 스킬·문서 변경을 제안합니다. 그 계층을 변경하지 않습니다. 안전하고 유용한 개입을 뒷받침할 수 없으면 이유가 있는 `no-change`를 유지합니다.

담당 SKILL.md의 처리 방향 규칙에 따라 진단을 대화로 반환합니다. 사용자가 상세 초안 파일을 요청한 경우에만 upstream 소유 발견 사항을 산출물 경로·익명화·파일 전달 확인을 거쳐 이슈 초안으로 쓸 수 있습니다. 기본 대화 출력은 파일을 만들거나 파일용 검사를 수행하지 않습니다. 진단 근거는 원시 로그 보존을 승인하지 않습니다.
