# FE 감사·검증 비교 근거

## Unit 1: actor mechanical 판정 보존

`grade_behavior`가 judge 실행 전에 actor 상태에서 mechanical assertion을 평가합니다.
원래 assertion 순서에 따라 결과를 반환하며 judge 결과와 오류 전파를 보존합니다.
grader가 파일을 생성·삭제·덮어쓰거나 Git HEAD를 commit/reset으로 바꾸는 사례를
두 assertion 순서에서 실제 함수의 actor-only oracle과 대조했습니다.

수정 전 focused 검사는 67개 중 10개가 실패하여 exit 1을 반환했습니다. 수정 후에는
68개가 모두 통과하여 exit 0을 반환했고, 독립 검수자가 같은 committed HEAD에서
동일한 결과를 재확인했습니다. judge-only, no-judge, grader 실행 오류와 schema 오류도
회귀로 보호했습니다. 이 변경은 actor mechanical 판정을 미리 계산하며 grader의
checkout 변경 자체나 host isolation을 차단하지 않습니다.

## Unit 2: 미해결 Dependabot backlog

기존 `tk-audit`의 Security/Dependencies 분기에만
[dependency reference](../../skills/tk-audit/references/dependency-audit.md)를 연결했습니다.
GitHub의 [REST alerts 계약](https://docs.github.com/en/rest/dependabot/alerts#list-dependabot-alerts-for-a-repository)과
[pagination 계약](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api)을
근거로 `state=open`, 반환 cursor, manifest instance, 수집 범위와 실패를 보존합니다.
로컬 resolved dependency와 default-branch advisory backlog를 구별하며,
PR merge나 dismissal만으로 fixed를 확정하지 않습니다. 기존 owner의 read-only 판단이
필요한 절차이므로 별도 scanner·provider·runtime을 추가하지 않았습니다.

같은 고정 사례 7개를 fresh-context prior/candidate actor에 주고 조건 이름을 모르는
독립 judge가 action·verdict·boundary를 의미로 판정했습니다. 보호 입력과 oracle은
비교 뒤 수정하지 않았습니다.

| 사례 | 관찰할 행동 | prior | candidate |
| --- | --- | --- | --- |
| A1 | 로컬 검사 뒤 남은 provider 보안 근거에서 open Dependabot backlog와 전체 pagination을 선택합니다. | fail | pass |
| A2 | 빈 첫 페이지의 next cursor를 따르며 전체 zero를 확정하지 않습니다. | pass | pass |
| A3 | 5개와 timeout을 partial/전체 unknown으로 보존하고 로컬 findings를 유지합니다. | pass | pass |
| A4 | 두 manifest 및 direct/transitive 관계와 local/default revision 경계를 유지합니다. | pass | pass |
| A5 | merged version PR과 dismissed/open 상태를 분리하고 연결·수정을 추정하지 않습니다. | pass | pass |
| A6 | 403을 provider 미감사로 남기고 새 credential이나 접근 확대를 하지 않습니다. | pass | pass |
| A7 | perf-only에서는 dependency reference와 provider 수집을 생략합니다. | pass | pass |

A1의 prior는 generic provider 조회를 선택했지만 수집할 정보의 종류를 특정하지 않아
unresolved Dependabot backlog의 완전 수집으로 판정할 수 없었습니다. candidate는
해당 endpoint·open 상태·전체 cursor 수집을 명시했습니다. A5–A7은 별도로 고정한
heldout 사례이며 양쪽 모두 통과했습니다. 기존 21개 canonical eval을 보존하고
[7개 회귀 계약](../skills/tk-audit/evals.json)을 추가했습니다.

## Unit 3: FE 성능 근거의 조건부 no-op

Unit 2와 같은 방식으로 고정한 FE 사례 7개를 fresh-context prior/candidate actor에
주고 조건 이름을 모르는 독립 judge가 action·verdict·boundary를 의미로 판정했습니다.
기존 `tk-browser-verify`와 `tk-prep` 지침은 6개 pass와 1개 unclear였고 candidate는
7개 pass였습니다. 현재 판정을 잘못 내린 prior 사례는 없었습니다. P5–P7은 별도로
고정한 heldout이며 양쪽 모두 pass였습니다. 비교 입력·oracle·응답·assessment는
비교 뒤 변경하지 않았습니다.

| 사례 | 관찰할 행동 | prior | candidate |
| --- | --- | --- | --- |
| P1 | cache를 맞추고 baseline/after 양쪽의 반복 samples와 spread로 비교합니다. | unclear | pass |
| P2 | static scanner hint를 observed hot path로 승격하지 않고 증상과 profiler 근거를 먼저 확보합니다. | pass | pass |
| P3 | 초기-load LCP와 실제 late dropdown interaction 및 관찰 구간을 구별합니다. | pass | pass |
| P4 | matched local 반복 samples의 criterion 충족을 인정하고 해당 조건에 한정합니다. | pass | pass |
| P5 | lab/field·origin/route population·percentile·수집 window가 다른 값을 차감하지 않습니다. | pass | pass |
| P6 | deployment/error/failed request를 분리하고 comparable request/transition 근거를 bundle 가설보다 먼저 확보합니다. | pass | pass |
| P7 | focus-only AC에 무관한 performance trace나 RUM 계정 연결을 추가하지 않습니다. | pass | pass |

P1의 prior도 cold/warm cache와 단일 sample의 한계를 확인하여 개선이나 AC Pass를
선언하지 않았습니다. 다음 계획은 after 반복을 지정했지만 baseline은 기존 단일
측정값이므로, 양쪽 반복 sample 집단과 spread를 확보하는지 확정할 수 없었습니다.
이 unclear는 다음 행동의 완전성에 관한 해석 경계이며 확정된 잘못된 판정이나
production 결함이 아닙니다. candidate는 양쪽의 matching replay와 반복·분산 확인을
명시했지만, 이 차이만으로 기존 owner의 실행 지침이 부족하다고 확정하지 않았습니다.

따라서 `SKILL.md`, references, description과 frontmatter를 모두 유지했습니다.
기존 browser의 criterion별 직접 근거·provenance·불완전 증거 경계와 prep의
증상 자체를 판별하는 loop·한 변수씩 반증하는 진단 절차를 보존합니다. 새로운
performance reference/loader, 일반 threshold, scanner, field collector나 runtime은
추가하지 않았습니다. 이는 승인된 Seed의 조건부 유지 분기이며 Seed deviation은 없습니다.

기존 browser 77개와 prep 146개 records 및 metadata를 보존하고
[browser 회귀 계약 5개](../skills/tk-browser-verify/evals.json)에 P1/P3/P4/P5/P7을,
[prep 회귀 계약 2개](../skills/tk-prep/evals.json)에 P2/P6을 추가했습니다.
각 계약은 제공된 입력에 대한 observable 판단과 다음 행동을 judge로 보호하며
실제 browser/API 실행이나 파일·Git 변경을 요구하지 않습니다. P4는 모든 after
samples가 명시된 local LCP<=2.0s criterion을 충족하는 정상 대조입니다. 양쪽 sample
범위와 수를 보고하고 local criterion Pass를 허용하되, 미제공 visual contract·다른 AC나
전체 verifier의 visual/runtime Pass 및 `verification_complete`로 확대하지 않습니다.
전체 terminal Pass를 강제하는 assertion은 넣지 않았습니다.

## 검증 범위와 한계

Unit 2의 GREEN 근거는 위 의미 비교와 canonical schema·link 검사입니다. 새 canonical
eval은 이후 실행할 observable 회귀 계약이며, 이번에 실제 API와 native skill loading으로
실행한 결과는 아닙니다. Canonical 계약에 포함한 추가 metadata·HTTP404·malformed·disabled
변형도 7개 policy simulation에서 직접 관찰한 결과와 구별합니다. 실제 pagination 수집,
계정 권한, production 효능이나 모델·호스트 전반의 개선율을 입증하지 않습니다.
`validate_skills.py`는 29개 skill에서 오류 0개, 기존 길이 경고 5개로 exit 0을 반환했고,
`validate_skills.py --links-only`도 링크 오류 0개로 exit 0을 반환했습니다.
`git diff --check`는 exit 0이며 reference의 exact readback, 기존 21개 eval·metadata와
고정 비교 입력의 hash 보존을 확인했습니다.
Unit 3은 실제 production 동작 변경이 없는 회귀 계약 추가이므로 production RED를
만들지 않았습니다. 위 비교는 batched fresh-context 정책 시뮬레이션이며 실제
browser measurement, native skill loading, API 수집, production RUM 또는 모델·호스트
격리 효능을 입증하지 않습니다. 7개 신규 canonical 계약을 실제 actor/grader로 실행한
결과도 아닙니다. P6의 sparse/음성 probe 한계와 P4의 전체 visual/runtime 판정 경계처럼
새 계약에 명시한 보호 범위는 고정 응답에서 직접 관찰한 결과와 구별합니다.
Unit 3의 `validate_skills.py`는 29개 skill에서 오류 0개와 기존 길이 경고 5개로
exit 0을 반환했습니다. `validate_skills.py --links-only`는 링크 오류 0개로 exit 0이며
`git diff --check`도 exit 0입니다. BASE의 기존 browser 77개·prep 146개 records와
metadata를 직렬화한 의미 객체가 byte-equivalent임을 확인했습니다. Self-review에서는
7개 계약의 observable 판단·local positive control·판정 범위 및 기존 owner 본문 유지와
Unit 1/Unit 2 설명·AI footer 보존을 대조했습니다.
전체 suite·release gate와 최종 통합 검증은 controller가 별도로 수행합니다.

🤖 본 검증 근거 문서는 AI가 작성했습니다.
