<a id="research-source-dispositions"></a>
# 조사 출처별 처리 판단

아래는 도입 당시의 출처·적응 결정 이력입니다. 과거 HTML 기본값을 현행 의무로 사용하지 않습니다. 현재 출력·완료 계약은 `SKILL.md`가 소유하며 기본은 대화, HTML·시각자료는 요청한 산출물 분기입니다.

2026-10-01에 `rohankgeorge/the-researcher`의 `1184d246c290a4ff772ea669ac6b9f9914d3f7da`(MIT)를 검토했습니다. README, LICENSE와 네 개의 `plugins/researcher/skills/` 패키지인 `deep-research-prompt-builder`, `primary-source-chaser`, `research-log`, `research-verification`을 확인했습니다.

- `keep/adapt`: 결정에 관련된 이차 주장을 접근 가능한 일차 권위 출처로 추적합니다. 출처 접근 가능성과 주장 충실도를 분리합니다. 가져온 내용과 중요한 주장·출처 쌍을 대조하여 검증합니다. 모순, 검증 불가 상태와 정정을 조용히 삭제하지 않고 보존합니다.
- `omit`: 필수 컨설턴트식 프롬프트 작성, 모든 한정된 조사 요청에 대한 지속 주장 원장, 플랫폼별 심층 조사 라우팅과 upstream plugin/toolchain 런타임을 제외합니다.
- TigerKit 반영 위치는 `references/evidence.md`와 `SKILL.md`의 한정된 완료 계약입니다.
- 검증: 고정된 revision에서 출처 텍스트를 확인했습니다. upstream 워크플로의 효과는 독립적으로 재현하지 않았으며 검증되지 않은 상태입니다.


<a id="autoresearch-source-dispositions"></a>
# Autoresearch 출처별 처리 판단

이 문서는 `tk-research`의 정본 출처 색인입니다. 향후 upstream 조사에서는 하드코딩된 목록 대신 이 패키지, 최상위 `NOTICE.md`, 패키지 라이선스와 메타데이터에서 증류 출처를 도출해야 합니다.

<a id="inherited-discovery-lineage"></a>
## 이어받은 탐색 계보

삭제된 공개 담당 스킬 `tk-discover`의 계보는 초기화하지 않고 여기서 이어갑니다.
- `Data-System-School/agent-skills`의 `a117418ab3596c59d641cab4cb89bdbe560fb277`: 읽기 전용 탐색과 미해결 동적 주장을 유지합니다. revision·스냅샷 식별, 의도와 런타임의 대조 및 최소 수직 단면을 조정하여 적용합니다. 모드 orchestration, 목록, 근거 원장, DAG와 자동 worker는 제외합니다.
- `DiUS/agent-toolkit`의 `6dc62cc0beadc92e7617ee8e8a916da369bfa65c`, `skills/codebase-discovery/SKILL.md`: 최신성과 의도 대조가 얇은 단면 모델에 영향을 주었습니다. 등록부, 온보딩 워크플로와 재현하지 않은 런타임 효과는 계속 제외되거나 검증되지 않은 상태로 남습니다.
- `mattpocock/skills`의 `d81f3a183412e71a5b1e84ca21bc1a35eea03a60`, wayfinder/grilling 출처: 목적지, 명확한 항목과 불명확한 영역의 구분, 의존성과 탐색 범위를 유지합니다. 필수 subagent, tracker 워크플로와 전역 상태는 제외합니다.
- `EveryInc/compound-engineering-plugin`의 `7b867109526165def0cc2a31b7c348b7308ae2c8`, 관련 `ce-plan` 조사·계획·인계 출처: 근거 기반 판단과 인계 경계를 유지합니다. 제공자·런타임 orchestration은 제외합니다.

<a id="autoresearch-expansion-reviewed-2026-10-01"></a>
## 2026-10-01에 검토한 Autoresearch 확장

### Orchestra-Research/AI-Research-SKILLs
- 저장소는 `https://github.com/Orchestra-Research/AI-Research-SKILLs`이며 MIT이고, `773a52944ba4747a18bd4ae9ade53fff041adcbc`로 고정했습니다.
- `0-autoresearch-skill/SKILL.md`, `references/agent-continuity.md`, README와 LICENSE를 확인했습니다.
- 지속 발견 사항, 내부 실험과 외부 종합의 구분, 정체 시 방향 전환과 부정적 결과를 통한 진척을 조정하여 적용합니다. `/loop`는 선택적인 사용자 소유 외부 scheduler로 조정하여 적용하며, 외부 질의 간격은 최소 한 시간을 권장하고 변경 없는 재개에는 `NO-DELTA`를 적용합니다. 필수·자체 소유 heartbeat, `never stop`, 논문 완성, 프로젝트 scaffolding과 런타임 orchestration은 제외합니다. upstream 데모는 재현하지 않았습니다.

### uditgoenka/autoresearch
- 저장소는 `https://github.com/uditgoenka/autoresearch`이며 MIT이고, `050e30dc4ba0974b03f2873111b9901ec3211390`으로 고정했습니다.
- `.claude/skills/autoresearch/SKILL.md`, `CONTEXT.md`, `guide/getting-started.md`, `docs/system-architecture.md`, README와 LICENSE를 확인했습니다.
- 유지·폐기 전 검증, 기계적으로 가능한 경우 명시적인 성공 조건, 방어 조건 검증, 정체·진척 없음과 한정된 반복을 조정하여 적용합니다. 범용 ship/deploy orchestration, 고정 반복 횟수, shell 런타임과 필수 지표 감소는 제외합니다. upstream 성능 주장은 재현하지 않았습니다.

### Companion-Inc/feynman
- 저장소는 `https://github.com/Companion-Inc/feynman`이며 MIT이고, `4d62d07a7e8eb1fba1b02d6547e6425e456715eb`로 고정했습니다.
- `skills/autoresearch/SKILL.md`, `AGENTS.md`, release note와 LICENSE를 확인했습니다.
- 한정된 실험 근거와 의미 있는 진척, 실패, 검증 및 차단 요인을 위한 실험 노트 원칙을 조정하여 적용합니다. Feynman 런타임·subagent, 일반 출력 계층, 필수 세션별 파일과 논문 도구는 제외합니다. 런타임 효과는 검증되지 않았습니다.

### bryanshake/autoresearch
- 저장소는 `https://github.com/bryanshake/autoresearch`이며 Apache-2.0이고, `0fa9a9336fc84a6b069111adb03ca21fabb5394b`로 고정했습니다.
- README, `ARCHITECTURE.md`, 프로젝트 레이아웃 문서와 LICENSE를 확인했습니다.
- 설계 참조로만 사용했습니다. 확대·중단 전 시험 실행, 부정적 결과 보존, 복구 가능한 작업 단위, 비평·블라인드 리뷰와 종료 확인이 TigerKit 압박 사례에 영향을 주었습니다. coordinator·런타임, queue 구현, 제공자 설정, 광범위한 권한과 scaffolding은 제외합니다. upstream 코드나 프롬프트 텍스트는 복사하지 않습니다. 다중 에이전트 결과는 재현하지 않았습니다.

<a id="frontier-and-batch-revision-reviewed-2026-10-02"></a>
## 2026-10-02에 검토한 탐색 범위와 묶음 개정

위 세 증류 출처의 revision을 최신 기본 branch commit과 다시 대조했고 여전히 최신이었습니다. 이 개정 전에 Orchestra의 `0-autoresearch-skill/SKILL.md`와 `references/agent-continuity.md`, uditgoenka의 `.claude/skills/autoresearch/SKILL.md`, bryanshake의 `ARCHITECTURE.md`를 다시 읽었습니다. 증류 출처의 데모, 런타임 결과와 경험적 평가 주장은 여전히 검증되지 않았습니다.

- `adapt`: Orchestra의 외부 종합과 정체 시 방향 전환을 프로젝트 수렴 전 필수 탐색 범위 재생성과, 결합된 실험·검증·종합에 걸친 방향 수준 묶음으로 조정했습니다. 일곱 후보 출처 범주와 후보 개수 할당량 없음은 사용자의 명시적인 재사용 워크플로 제안에서 왔습니다. upstream 요구를 인용한 것이 아니라 TigerKit이 조정한 사항입니다.
- `adapt`: Orchestra의 실제 시간 기준 연속성을 실제로 `/loop`를 지원하는 호스트에서 사용자 소유 scheduler를 안내하는 방식으로 조정했습니다. 스킬은 스스로 일정을 잡거나 다시 호출하지 않습니다. 한 시간 권고는 upstream 기본값이 아니라 TigerKit 부하 제어 안내입니다.
- `keep`: uditgoenka의 정체·진척 없음 방어 조건을 변경 없는 재개의 `NO-DELTA`로 유지합니다. `omit`: 고정 반복 횟수와 shell orchestration은 제외합니다.
- `adapt`: bryanshake의 근거에 연결된 종료 확인을 재생성 후 수렴으로 조정하며, 이용할 수 없는 필수 근거는 `BLOCKED`로 유지합니다. `omit`: coordinator·런타임과 queue는 제외합니다.
- `adapt`: 사용자의 안전한 현재 worktree 지정을 기존 단일 홈 지속성 계약으로 조정합니다. 다른 연결 worktree 없이 새 researchId를 포함합니다. `keep`: 소유권, 깨끗한 checkout, 기본·제품 branch와 무관한 작업 보호를 유지합니다.

<a id="evaluation-and-lineage-revision-reviewed-2026-10-02"></a>
## 2026-10-02에 검토한 평가와 계보 개정

이 개정 전에 다음 기본 branch revision을 새로 가져왔습니다. 이는 동작·설계 비교이며, 재현한 런타임 성능이나 복사한 구현이 아닙니다.

- `RUC-NLPIR/Arbor`, Apache-2.0, `7cdaf1fa6d779b3d5e340052357bf3fe55dfed93`:
  `docs/how-it-works.md`, `docs/preparing-a-benchmark.md`,
  `skills/arbor-agent-orchestrator/SKILL.md`, `skills/arbor-agent-merge-eval/SKILL.md`,
  `skills/arbor-agent-ideate/SKILL.md`, `tests/test_executor_tamper.py`와 LICENSE를 확인했습니다.
  `adapt`: 보호된 evaluator·지표·데이터 경계, 가능한 경우 개발과 독립 승인의 구분, 선택적 기원 링크와 형제 아이디어 생성에서 활용하는 근거 기반 부모 교훈을 조정하여 적용합니다.
  `keep`: TigerKit의 일반 조사 범위, 단일 홈과 정보 가치 수렴을 유지합니다.
  `omit`: Idea Tree 런타임, 필수 노드 schema·깊이, 실행자 구조, 대시보드와 merge 임계값을 제외합니다.
- `Gyubin/autoresearch`, Apache-2.0, `1e2830d9f35853d7eee580b7333a3c91e6259c0d`:
  README의 평가·halving·assurance 설계, `tests/test_phase4.py`의 가지치기 사례, LICENSE와 NOTICE를 확인했습니다.
  `adapt`: 예산에 따른 가지치기를 과학적 부정 근거와 구분합니다. 실행하지 않은 후보는 실패 통찰이나 확신도 감점 없이 보존합니다. 해당 출처의 smoke 평가된 endpoint 중복 제거가 TigerKit의 미실행 후보를 시험된 endpoint로 만들지는 않습니다. `adapt`: 결정에 중요한 잡음 있는 근거에는 비용을 고려한 독립 복제와 보호된 승인 신호가 적절합니다.
  `omit`: successive halving, 고정 K·seed, pairwise panel, 원장, sandbox와 통계 런타임을 제외합니다.
- `Muuuun/luxas`, MIT, `9f77cefe7f47b05b1334ec8778e642deef13da82`:
  README의 블라인드 구현·테스트 분리와 자기 순환 실패 예시 및 LICENSE를 확인했습니다.
  `adapt`: 독립 검증자 입력에서 불필요한 제안자 결론은 보류하고 객관적 계약과 일차 산출물을 강조합니다. `omit`: 에이전트 구조, 고정 재시도 상한과 논문 워크플로를 제외합니다.
  보고된 실제 실패와 다중 에이전트 효과는 재현하지 않았습니다.
- `karpathy/autoresearch`, `228791fb499afffb54b46200aca536f79142f117`:
  고정된 `prepare.py`와 편집 가능한 `train.py` 예시를 위해 `program.md`를 확인했습니다. 이 revision에는 LICENSE/NOTICE 파일이 없었습니다. 출처 텍스트·코드는 포함하지 않으며 증류 출처가 아닙니다.
  위 보호 평가 규칙은 Apache-2.0 Arbor/Gyubin이 독립적으로 뒷받침합니다.
- `SakanaAI/AI-Scientist-v2`, `96bd51617cfdbb494a9fc283af00fe090edfae48`:
  LICENSE를 확인했으며, MIT/Apache-2.0이 아니라 사용자 정의 AI Scientist Source Code License v1.0입니다.
  증류 출처가 아니며 구현이나 프롬프트 텍스트는 포함하지 않습니다. Arbor/Gyubin은 이 런타임이나 라이선스 조건을 가져오지 않고도 계보와 복제 원칙을 제공합니다.

설치된 동작은 SKILL.md, `experiments.md`, `state.md`와 `persistence.md`가 소유합니다.
과거 압박 시나리오는 Git 이력에 있습니다. 저장소 eval framework는 폐기되었습니다.
증류 출처의 테스트는 설계 근거로 읽었으며 실행하거나 TigerKit 검증이라고 주장하지 않았습니다. 원본 증류 출처 라이선스는 아래에 보존되어 있습니다.
사용자의 loop 호출 정정으로 패키지는 모델 호출이 활성화된 `hybrid`로 바뀝니다. 선택에는 구체적인 지속 조사·재개 요청이 필요하며 선택 자체는 권한을 부여하지 않습니다.

<a id="continuing-project-revision-reviewed-2026-10-02"></a>
## 2026-10-02에 검토한 지속 프로젝트 개정

새로운 기본 branch 확인에서도 Orchestra `773a529`, uditgoenka `050e30d`, bryanshake `0fa9a93`이 계속 일치했습니다. 이 개정 전에 Orchestra의 agent-continuity 참조, uditgoenka의 autoresearch SKILL.md와 bryanshake의 ARCHITECTURE.md를 다시 읽었습니다.

- `adapt`: 외부 종합·정체 시 방향 전환을 대기, 차단이나 낮은 가치의 항목만 남았을 때 같은 묶음에서 재생성하는 방식으로 조정했습니다. 마지막 실행 가능한 후보를 소진하면 후보가 있던 결과는 무효가 됩니다. 변경 없는 후보 없음 증명은 재개·근거 확인 후 계속 재사용할 수 있습니다.
- `adapt`: 복구 가능한 작업을 기존 정본 상태 안의 인계 후보와 확인 가능한 재개 조건으로 조정했습니다. 선택된 인계는 조사 탐색 범위를 보존합니다. 관찰한 운영 결과는 근거가 되며 구현 권한이 되지는 않습니다.
- `keep`: 의미 있는 진척 없음 결과, 단일 조사 홈, 안정적인 researchId·상태 경로와 현재 세션 권한 경계를 유지합니다.
- `omit`: 필수 heartbeat, 끝없는 불필요한 작업, queue·coordinator와 자동 제품 구현을 제외합니다. 증류 출처 런타임 시연은 여전히 검증되지 않았습니다.

용어, 지시를 반영한 재개, 부분 인계, 기록된 사용자 전제·질문과 새 세션의 로컬 우선 권한 확인은 사용자의 명시적인 재사용 운영 제안에서 왔습니다. 새로운 증류 출처 텍스트나 코드는 포함하지 않습니다.

<a id="cost-aware-measurement-order-2026-10-07"></a>
## 비용을 고려한 측정 순서(2026-10-07)

`EveryInc/compound-engineering-plugin@142dbabc23c86884f2e353502eb20a5fdd2a6d3d`의
`skills/ce-optimize/references/measurement.md`(변경 전 기준과 탐색의 구분 논거),
`scripts/decide.mjs`와 `tests/skills/ce-optimize-decide.test.ts`(smoke 거부, 명확한 열세, 경계선에서의 상향 확인과 유지 전 확인)를 참고했습니다. 테스트는 읽었지만 다시 실행하지 않았습니다.

- `keep`: 여기서 이미 소유하는 보호 evaluator, 비교 가능한 변경 전 기준과 승인 경계를 유지합니다.
- `adapt`: 저렴한 탐색, 선택적인 근거 강화와 `KEEP` 전의 더 강한 확인을 `experiments.md`에 조정하여 적용합니다. 측정 강도는 여전히 비용·잡음·효과·결정에 따라 달라집니다.
- `omit`: 고정 표본 수·무익성 계수, 증류 출처 스크립트, orchestration, worktree, 실험 로그 schema와 대시보드를 제외합니다. 새 런타임이나 지속 정책은 가져오지 않습니다.

<a id="unified-owner-and-human-projection-2026-10-07"></a>
## 담당 통합과 사람이 읽는 표현(2026-10-07)

한정된 조사와 지속 조사의 담당을 `tk-research`로 합칩니다. 과거 탐색 계보와 모든 유효한 실험·탐색 범위·부정적 결과 계약을 유지합니다. 가벼운 근거 수집은 지속 저장·worktree 의례 없이 시작합니다. 지속 로컬 상태는 조건부이며 공유는 명시적입니다. 이는 사용자의 명시적인 재사용 워크플로이며 증류 출처의 성능 주장이 아닙니다.

새로 고정한 revision은 계속 Orchestra `773a52944ba4747a18bd4ae9ade53fff041adcbc`, researcher
`1184d246c290a4ff772ea669ac6b9f9914d3f7da`, EveryInc
`142dbabc23c86884f2e353502eb20a5fdd2a6d3d`입니다. Orchestra의 진척 보고·연속성 참조와 norm-heterogeneity 데모 설명을 읽었습니다. 중요한 결과 보고는 조정하여 적용하고, 강제 heartbeat와 자동 UI 열기는 제외합니다. 데모의 과학적 결과는 재현하지 않았습니다. EveryInc의 `ce-ideate/references/html-rendering.md`에 있는 탐색·자체 완결 불변 조건과 출력 HTML 계획을 읽었습니다. 기본 의미적 절, 고정·간결한 목차, hash와 details는 조정하여 적용하고, CDN 글꼴, 필수 HTML 전용 권한과 증류 출처 orchestration은 제외합니다. 증류 출처의 스타일·팔레트는 복사하지 않습니다. 공통 글쓰기와 HTML 동작은 계속 `tk-rewrite`와 `tk-explain`이 담당하며 릴리즈 체크리스트에 따라 복사하고 확인합니다.
MDN `nav`/`details`와 W3C bypass-blocks는 기본 탐색·접근성 의미를 설명하며 조사 효과를 설명하지 않습니다. 비교 로컬 eval은 동률과 비용·재개·부정적 결과의 한계를 보존합니다.

설치된 담당 문서는 `SKILL.md`입니다. 지속 동작은 조건에 따라 `persistent-research.md`,
`experiments.md`, `state.md`와 `persistence.md`가 담당합니다. 위 과거 증류 출처 결정은 출처 기록이며 현재 운영 권한이 아닙니다. 원본 라이선스 텍스트는 [upstream 라이선스](../UPSTREAM-LICENSES.txt)에 있습니다.

<a id="shared-clear-writing"></a>
## 공통 명확한 글쓰기

`../../tk-writing/references/clear-writing.md`는 `tk-writing`이 소유하는 단일 참조 계약입니다. 이전 `tk-rewrite` 계보는 `tk-explain/references/sources.md`에 기록되어 있습니다. 원본 MIT 고지는 이 패키지의 `LICENSE.txt`에 유지됩니다. 참조를 읽어도 별도 글쓰기 워크플로 실행 권한이나 출력 상태 소유권은 부여되지 않습니다.

<a id="html-quality-extension-2026-10-07"></a>
## HTML 품질 확장(2026-10-07)

제공된 반복 산출물 제안과 TigerKit 기준 `56c8a50603bd1649465a74b2e8af373a0e51a8a9`는 명시적인 재사용 의도와 확인 가능한 계약·템플릿 공백을 제공합니다. 오프라인 읽기와 hash 탐색은 유지하고, 중립적인 QA 테마 구조와 프로젝트 전체 표현은 조정하여 적용하며, 도메인별 스크립트와 원시 세션 세부 정보는 제외합니다. 보고된 독점 `dataviz` 묶음은 참조용일 뿐입니다. 문구, 코드, 팔레트나 검증 스크립트는 포함하지 않습니다. 배포·라이선스와 upstream 동작은 여기서 독립적으로 검증하지 않았습니다. 일반 차트 규칙과 중립 토큰은 독립적으로 작성했습니다. 런타임·제공자 관찰은 조건부이며 호환성 주장이 아닙니다.

<a id="archify-only-document-routing-2026-10-28"></a>
## archify 전용 문서 라우팅(2026-10-28)

새로 확인한 출처는 여전히 `tt-a1i/archify@d6059331abbddb49bca380ff46dca8ce33158b04`(3.2.0)로 해석됩니다. 기존 문서 경로를 제거하기 전에 release manifest, SKILL.md, explainer 작성·viewer-runtime 계약, explainer 렌더러와 CLI·패키징 테스트를 확인했습니다. 기본 안내 단계, 노드·경로 탐색, 출처 연결과 오프라인 finalize 관문을 유지합니다. 설명과 조사 출력 모두에 `tk-writing`의 공통 렌더러·장면 도우미를 사용합니다. 자동 설치, 포함된 외부 런타임과 사용자 정의 스크립트 주입은 제외합니다. 임의의 매개변수 기반 시뮬레이션은 이 버전의 explainer 문법에 포함되지 않습니다. 정적 그림이 이를 구현한다고 주장하지 말고 요청한 동작을 미충족으로 보존합니다. 특수 QA·gallery·prototype·질문 인터페이스와 기존 사용자 산출물은 각 담당자가 유지합니다. 이전 공통 shell 출처는 이력을 기록하며, 새로운 설명·보고서 렌더링 경로가 아닙니다.

## 보고서의 내용 형태별 경로 재검토 (2026-11-09)

사용자의 비교표와 권고 목록 사례에 따라 위 archify 전용 결정을 재검토했습니다.
최신으로 고정한 `tt-a1i/archify@11b0d6031853bdae89eed57e7979aabbf0034097`의
`archify/references/explainer-authoring.md`, `archify/explainer/validate.mjs`와
`test/explainer-validation.test.mjs`를 읽었습니다. 정보 형태에 따른 표와 도해의 구분,
raw HTML과 안전하지 않은 링크 거부 및 출처 참조 검증을 확인했습니다.

- `keep`: 요청한 HTML만 제작, 연구 근거와 프로젝트 전체 포함 범위, 원고에서 수정, 원본 보존과 피드백 후처리입니다.
- `adapt`: `tk-writing`의 내용 형태별 선택과 미위임 HTML의 제작 전 제안, 일반 문서 빌더 및 정적 기준을 보고서에도 적용합니다.
  일반 HTML과 선택한 archify의 검사 결과를 구별하며 기존 보고서 전용 생성기와 검사기를 공통 경로로 복원하지 않습니다.
- `omit`: 모든 조사 페이지의 archify 강제, 원고나 출처를 생략한 임의 HTML, 렌더러 설치나 업데이트와 실패 뒤 조용한 전환입니다.

형태 선택은 TigerKit 사용자 교정입니다. upstream 테스트는 읽었으며 실행하지 않았고 모델 효과는 `unverified`입니다.

## 설치본과 upstream의 revision 구분 (2026-11-11)

최신 HEAD가 같은 `rohankgeorge/the-researcher@1184d246c290a4ff772ea669ac6b9f9914d3f7da`임을 조회하고
README와 `plugins/researcher/skills/research-verification/SKILL.md`의 실제 출처 확인·최신 상태 대조를 읽었습니다.

- `keep`: 주장과 읽은 출처의 연결, 최신성 확인과 접근 불가의 `Unverifiable` 처리를 유지합니다.
- `adapt`: 사용자 피드백 24에 따라 플러그인 버전 표기가 같아도 설치 메타데이터 commit과 upstream HEAD를 먼저 대조하여 두 동작의 근거를 분리합니다. 구체적인 commit 대조는 TigerKit 보강입니다.
- `omit`: 자동 설치·갱신, 필수 주장 원장과 upstream 검증 런타임은 추가하지 않습니다. 출처 텍스트를 읽었으며 upstream 실행 효과는 `unverified`입니다.
