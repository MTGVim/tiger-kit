# behavior-verify

behavior-verify는 SoT(티켓, PRD, 스펙, 사용자 요청 서술)에 적힌 의도가 local runtime에서 실제로 동작하는지 브라우저에서 검증하는 mode입니다. env-diff가 "같은 화면이 같게 생겼는가"라면, behavior-verify는 "약속된 상호작용이 약속된 결과를 내는가"를 봅니다.

## Baseline / target

- baseline: SoT — 티켓, PRD, 스펙, 사용자 서술. runtime이 아니라 문서/서술입니다.
- target: local runtime
- optional 보조 baseline: 기존 동작의 회귀가 의심되면 같은 상호작용을 QA runtime에서도 실행해 대조할 수 있습니다. 이때 QA 측 mutation도 동일한 Mutation 안전 규칙을 따릅니다.

## SoT ingestion

- 접근 불가 reference(URL, 이미지, 디자인 링크)는 pending으로 기록하고 요구사항을 발명하지 않습니다.
- Evidence(직접 관측) / Interpretation(추론) / Decision(사용자·source 확인) / Suggestion(제안)을 분리합니다.
- SoT에서 관측 가능한 행동 단위 체크리스트를 추출합니다. 각 항목은 아래를 갖습니다.
  - 진입 상태: 어떤 화면 / 어떤 데이터 상태에서 시작하는가
  - 상호작용: 어떤 trusted 입력을 수행하는가
  - 기대 결과: SoT가 약속한 결과는 무엇인가
  - 증거 축: UI 상태 전이 / network 요청 / 응답 후 상태 중 무엇으로 판정하는가
- 브라우저에서 관측 불가능한 항목(서버 내부 처리, 배치, 비동기 후속 작업)은 처음부터 out-of-scope로 표시합니다.
- 체크리스트는 실행 전에 사용자에게 보여 확인받는 것을 기본으로 합니다.

## 판정 contract

- 항목 단위 verdict: `pass` / `fail` / `unverifiable`
- 엔진 `SKILL.md`의 Behavior 판정 규칙을 따릅니다: mutation 판정은 network 증거 필수, 합성 이벤트 관측은 증거 불인정, 3축 구분 기록.
- `unverifiable`에는 사유를 명시합니다: 테스트 컨텍스트 부재 / 상태 도달 불가 / SoT 모호 / 브라우저 관측 범위 밖.
- SoT가 두 가지 이상으로 읽히는 항목은 임의 해석으로 pass / fail을 내리지 않고 ambiguity로 보고합니다.

## 안전 contract

엔진 `SKILL.md`의 Mutation 안전 절을 그대로 따릅니다. mode 차원의 추가 규칙:

- mutation 유발 가능성이 있는 항목은 실행 전에 체크리스트에 표시해 사용자가 실행 범위를 미리 볼 수 있게 합니다.
- 검증 중 예상하지 못한 mutation 요청이 관측되면(의도한 항목 밖의 write) 즉시 중단하고 보고합니다.

## Procedure

1. SoT를 수집하고 행동 단위 체크리스트를 만듭니다. mutation 유발 항목과 비가역 항목을 표시해 사용자에게 확인받습니다.
2. env-diff와 동일한 인프라로 진입합니다: profile `env.md` 기준 dev 서버 확인/기동, `login.md`(+`login.local.md`) 기준 로그인, `screens/<name>.md` 기준 화면 진입.
3. 항목별로 실행합니다.
   - native dialog handler를 먼저 준비합니다.
   - network 관측을 시작합니다 (driver의 request 목록 또는 CDP Network domain).
   - trusted 입력으로 상호작용을 수행합니다.
   - 3축(UI 상태 전이 / network 요청 / 응답 후 상태)을 관측하고 기록합니다.
   - verdict를 내립니다.
4. `fail` 항목은 재현 절차(진입 상태 + 상호작용)와 관측 증거를 함께 남깁니다.
5. 보고합니다.

## Output

항목별 표를 기본으로 합니다.

```text
| # | SoT 항목 | 상호작용 | 기대 결과 | 관측 결과 | network 증거 | verdict |
```

최종 요약에는 아래를 포함합니다.

- mutation 실행 여부와 실행된 테스트 컨텍스트
- mock 사용 여부와 대상 endpoint
- `unverifiable` 항목과 사유
- 예상 밖 mutation 관측 여부 (없으면 없음으로 명시)
- run 산출물 디렉토리 경로와 항목별 스크린샷 파일 목록 (엔진 Evidence artifacts 규칙)
