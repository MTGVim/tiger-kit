# PR 목적 판단, 조건부 보안 검사와 SVG 실험

대상 이슈는 #470, #471, #472입니다. `README: no public change`.
`skills/tk-pr-rebase/references/rebase-readiness.md`,
`skills/tk-audit/references/audit-playbook.md`,
`skills/tk-review/references/security.md`의 내부 판단만 보강합니다.
공개 스킬 이름·호출 방식·카탈로그 설명·HTML 런타임은 바꾸지 않습니다.

## 확인한 상류와 선택

| 상류와 고정 커밋 | 확인한 근거 | 판단 |
| --- | --- | --- |
| [PR 유지보수 상류](https://github.com/EveryInc/compound-engineering-plugin/tree/8fc624947680a39b06a3c4fa9200c91d5ec97fc7) | `skills/ce-babysit-pr/references/intake.md`, `scripts/intake-overlap`, `tests/skill-eval-cell/packs/ce-babysit-pr-stale-intake.md`, PR #1909 | 변형: 목적·관련 `base` 변경·대체 구현과 `Update`/`Rework`/`Close` 판정. 제외: `watcher`, `takeover`, 별도 겹침 검사 런타임, 상류 권한 체계. |
| [브라우저·에이전트 보안 감사 상류](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8) | `skills/security-audit/CLIENT-SIDE.md`, `AI-AND-LLM.md` | 변형: 브라우저·도구의 실제 신뢰 경계와 안전한 반례. 제외: 전체 감사 파이프라인, 검사 범위 장부, 상시 `hunter`/`critic`. |
| [다이어그램 설계 상류](https://github.com/cathrynlavery/diagram-design/tree/97d795138448f6a739a0cebc3d9beb37a42077f1) | `scripts/verify-geometry.py`, `scripts/test-verify-geometry.py` | 유지: 재현 가능한 기하 검사의 접근. 제외: 현 시점의 런타임 도입과 도형 크기·직교 연결선·그리기 순서 가정. |

모두 MIT 라이선스를 확인했습니다. 증류한 PR·보안 참조를 포함하는 각 독립 설치
패키지에 해당 상류 저작권·허가 고지를 보존합니다. 상류의 보고된 행동 평가 결과는
TigerKit에서 실행한 결과로 간주하지 않습니다.

## #470: 목적이 유지되는 PR만 일반 최신화

기존 참조는 최신 기준·작업 커밋와 병합 충돌·뒤처짐을 판단하지만, 삭제한 구조의 복원이나
이미 충족된 목적을 별도로 판정하지 않았습니다. 공통 `readiness`가 짧은 목적·경로 검사를
소유하며, 겹침·상위 디렉터리 삭제/이동·대체 구현 징후가 있을 때 관련 이력만 조사합니다.
`Update`만 기존 최신화 경로로 이어지고 `Rework`와 `Close`는 근거와 필요한 결정을
반환합니다. 판정 자체에 PR 닫기나 발행 권한은 없습니다. 열린 대안은 병합된 대체 구현과
구분하며, 비교를 할 수 없으면 `Unverifiable`로 중단합니다.

`tk-pr-rebase`에 5개, `tk-pr-sweep`과 `tk-pr-respond`에 각 1개의 평가를 추가했습니다.
기존 `lease`·승인·`freshness` 계약과 결정론적 분류는 유지합니다.

## #471: 관련 코드가 있을 때만 보안 참조를 읽기

`tk-audit`가 `security-boundaries.md`의 정본을 소유합니다. `tk-review`와 그 보안 참조를
사용하는 `tk-prep`, `tk-pr-respond`에 기존 동기화 도구가 일반 파일 사본을 배포합니다.
관련 없는 코드에서는 참조를 읽지 않습니다. 누락·`drift`를 만들고 복구하는 설치 사본
회귀 검사도 추가했습니다.

상류 CLIENT-SIDE의 `postMessage`, `worker`/`storage` `identity`, `prototype` `gadget`, DOM/XSS와
AI-AND-LLM의 `handler` `authorization`, `action` `binding`, `retry`/`resume`, `tenant` `cache`,
`schema`/`dispatcher` 항목을 각각 같은 이름의 조건부 조사 항목으로 옮겼습니다.
기존 `source`→`sink`·`guard` 추적, 독립 검증, `Finding` 형식을 복제하지 않았습니다.
감사와 리뷰에 각각 7개의 취약 사례·안전한 반례·외부 정책 미확인 평가를 추가했습니다.
실제 운영 서비스 공격이나 새로운 스캐너 설치는 수행하지 않습니다.

## #472: 기하 검사 도입 보류

현재 공통 HTML 조립·정적 검사는 문서 구조, `anchor`, 오프라인 참조 등을 담당하며
연결선 좌표를 검사하지 않습니다. `visual-grammar.md`와 `html-figures.md`는 내용과
시각 대응을 판단하는 규칙이므로 좌표 검사와 역할이 다릅니다.

검토한 실제 표본은 현재 공통 `chart-examples.html`의 SVG 5개와 과거 TigerKit이 생성한
강의 HTML의 텍스트·선/경로를 포함한 SVG 8개입니다. 후자는 폐기된 `course` 산출물이고
현재 `explain`/`teach` 전체 모집단을 대표하지 않습니다. 상류 검사 결과는 두 파일 모두
0건이었지만 강의 SVG에는 직접 `marker` 속성이 없어 연결선 검사 범위가 특히 제한됩니다.
따라서 새로 포착한 실제 결함이나 전체 산출물의 무결성을 주장하지 않습니다.

재현 명령은 다음과 같습니다. 상류 `checkout`은 네트워크가 없는 별도 인자로 전달하며,
실험은 `revision`과 검사기 바이트가 일치하는지 먼저 확인합니다.

```bash
python3 evals/skills/tk-explain/geometry_probe.py \
  --upstream .tigerkit/tmp/upstream/diagram-design
```

선택적인 `--sample <existing.html>`은 원본을 수정하지 않고 추가 표본을 검사합니다.
실험은 14개 합성 `fixture`에서 아래 관찰을 재현합니다. 성공 종료는 **호환성 실험이
예상대로 재현됐다는 뜻**이며 SVG 품질 통과 판정이 아닙니다.

| 범위 | 관찰 |
| --- | --- |
| 정상 직선, `head-to-tail` 접점, 곡선, 노드 위에 나중에 그린 라벨 | 경고하지 않습니다. |
| 중복 연결선, 테두리와 겹친 선, 가까운 접점, 뒤에서 덮이는 라벨 | 후보 위치·원인을 보고합니다. |
| 해석할 수 없는 경로 | 파서 진단을 반환합니다. |
| 정상 사선 | 직교 규칙 위반으로 오탐합니다. TigerKit은 사선을 일괄 금지하지 않습니다. |
| 서로 다른 SVG의 같은 좌표 | 하나의 좌표계로 비교하여 중복 연결선으로 오탐합니다. |
| `scale` 변환, CSS `marker`, 작은따옴표 속성의 중복 연결선 | 0건이지만 파서가 해당 연결선을 누락한 미검증 상태입니다. |

유의미한 실제 추가 검출 이득을 입증하지 못했고 상류 그대로는 오탐·미검증 문제가 있어,
이슈에서 허용한 도입 보류를 선택합니다. 실험은 저장소 전용이며 설치 패키지·HTML 검사
경로·필수 릴리즈 검사에 연결하지 않습니다. 실제 생성 SVG의 실패 사례가 확보되면,
SVG별 좌표계·도형 의미 식별·미지원 상태를 명시하는 좁은 검사부터 다시 평가합니다.

## 지침 부하와 검증 경계

상시 SKILL 본문을 늘리지 않았습니다. 공통 `readiness`의 목적 검사 블록을 제거하면
삭제된 상위 디렉터리·이미 충족된 목적을 `clean`과 구분하는 기준이 사라집니다.
보안 참조 진입점을 제거하면 새 렌즈가 읽히지 않으며, 각 조건부 항목을 제거하면
동명 평가의 구체적인 반증 기준이 사라집니다. 일반 `source`→`sink`·권한·독립 리뷰 원칙은
기존 소유 문서를 유지했습니다. 이는 문서와 시나리오의 비교이며 독립 모델 `A`/`B` 실행이나
실서비스 취약점 검증을 주장하지 않습니다.
