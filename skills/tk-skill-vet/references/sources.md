<a id="sources-and-boundaries"></a>
# 출처와 경계

이 패키지를 설계하기 전인 2026-10-30에 불변 revision으로 검사했습니다.

- `Agent-Threat-Rule/agent-threat-rules@28d0a198e843cbccf8b7446db3a798cfd27f5ec1`:
  `rules/skill-compromise/ATR-2026-00128-html-comment-hidden-payload.yaml`,
  `ATR-2026-00129-unicode-smuggling.yaml`, `ATR-2026-00149-skill-exfil-compound.yaml`,
  그리고 악성 인코딩 주석/정상 shell wrapper 벤치마크 예시를 확인했습니다. MIT, ATR Contributors.
- `OSSAfrica/skillguard@12a958cb426aac8163f7dc86e3a22af5fd1412eb`:
  `README.md`, `internal/analyzer/scorer.go`, `injection_test.go`, `regression_test.go`.
  MIT, OSSAfrica. 회귀 사례는 문구와 명령 실행을 구별하고, 일반 다국어 텍스트와 의심스러운 혼합 문자 은폐를 구별합니다.

구체적인 복합 행동 근거와 정상 대조 사례를 유지합니다. 이러한 실패 유형을 전체 패키지와 업데이트 diff에 대한 사람이 읽을 수 있는 정적 검토에 맞게 적용합니다. 정규식/점수 엔진, 임계값, 설치/강제 적용, hook, 클라우드 보고와 벤치마크 정확도 주장은 제외합니다. Upstream의 실험적 규칙 일치는 운영 차단 정책이나 악성의 증거가 아닙니다. 여기의 fixture는 독립적으로 작성했으며 외부 엔진이나 의존성을 포함하지 않습니다. 여러 프로젝트가 SkillGuard라는 이름을 사용하므로 이 출처를 다른 저장소에 귀속하지 않습니다. `LLMSecurity/skillguard`에는 라이선스가 없는 것으로 확인되어 복사한 자료가 없습니다. 원래 MIT 고지는 이 패키지의 `LICENSE.txt`에 보존합니다.

## 입력·해석기 흐름과 정상 대조

`protectskills/MaliciousSkillBench@893afd609be22a2dfac5a2b94bbebb4eeb99515e`의 `README.md`,
`benchmark/taxonomy.md`, `benchmark/protocols.md`, `baselines/README.md`, `scanner_eval/README.md`,
`RESPONSIBLE_USE.md`를 공개 읽기 API로 확인했습니다. 위협 분류와 inert-text 평가 설계만 참고했으며,
원본 악성 샘플·scanner/learned baseline 구현과 실제 탐지 효과는 `unverified`입니다.

- `keep`: 고정 snapshot, 도달 가능한 복합 행동·정상 대조, 실행 금지와 기존 위험도·판정 경계를 유지합니다.
- `adapt`: 입력→명령 해석기와 검증·escaping의 효과, socket→shell→표준 입출력의 결합을 기존 정적 검토 목록에 명시합니다. 상세 흐름과 대조 사례는 독자 작성이며 upstream이 두 규칙을 구현·실증했다고 귀속하지 않습니다.
- `omit`: 악성 원문·코드 복사/실행, scanner·learned model·regex 차단기·상시 eval과 benchmark 수치의 전용은 제외합니다. 새로운 설치 권한이나 무조건 `Reject` 정책은 추가하지 않습니다.
