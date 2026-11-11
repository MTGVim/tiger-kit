<a id="confusion-and-badge-review-2026-11-11"></a>
# 이해 실패 신호와 배지 검토 (2026-11-11)

`mattpocock/skills@4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`의
`skills/productivity/wait-what/SKILL.md`, `docs/productivity/wait-what.md`와 teach의
`SKILL.md`·`LEARNING-RECORD-FORMAT.md`를 확인했습니다. `keep`: 이해 실패 신호에 설명을 다시 구성하고
실제 답변과 단순 노출을 구분합니다. `adapt`: 이미 공유한 사례·용어로 돌아가고 필수 조건을 보존하며,
혼란이 이어질 때 막힌 문장을 묻습니다. `omit`: 고정 영어 규격, 필수 glossary, 강제 수업·기록과 숙달 추론입니다.
호출 증가와 학습 효과는 미검증입니다.

`tt-a1i/archify@7e45f36c66de1254d5ad6ba1d878f6499ea269fd`의
`archify/explainer/render.mjs`·`inline.mjs`, `archify/references/explainer-authoring.md`와
`test/explainer-inline.test.mjs`를 정적으로 확인했습니다. `keep`: 사실의 범위·예외와 배지의 의미 색조입니다.
`adapt`: `.assessment.good/caution/bad`를 포함한 배지 선언을 검토 텍스트에 보존하고 셀의 열 속성과 대조합니다.
`omit`: 색조의 자동 정확성 판정, upstream 렌더러 코드 복제와 정적 추출을 실제 색 검증으로 취급하는 주장입니다.
upstream 검증 코드는 읽었지만 실행하지 않았으며 기존 렌더러 최소 버전 계약은 변경하지 않습니다.

<a id="outcome-led-teaching-reassessment-2026-10-18"></a>
# 학습 성과 중심 수업 재평가 (2026-10-18)

`mattpocock/skills`의 `49dd158d1076134a641b33efb035946536778336`에서
[teach](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/teach/SKILL.md)와
[설계 이유 및 보고된 한계](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/docs/productivity/teach.md)를 검토했습니다.
구현과 설계 이유를 검사했습니다. 고정한 트리에서 별도로 실행할 수 있는 upstream teach 평가를
찾지 못했으며 학습 효과를 재현하지 않았습니다.

- `keep`: mission, 신뢰할 수 있는 출처, 범위가 좁고 유용한 역량, 연습 전 필요한 지식, 즉각적인 피드백과 실제 학습 근거에 따른 다음 단위 선택을 유지합니다.
- `adapt`: 선수 지식, 설명, 풀이 사례, 조건을 바꾼 적용과 이유를 설명하는 재시도 피드백을 연결합니다. 기존 과정 조사, 오프라인 자산, 상태 식별 정보와 레거시 이어가기를 보존합니다. 집중 수업에는 과정 골격이 필요하지 않습니다.
- `omit`: 보편적인 페이지 길이, 패널 수, 등장인물이나 대화 형식, 정확한 퀴즈 답변 길이, 자동 열기, 커뮤니티 배정이나 scheduler를 제외합니다. 산출물에 대한 호평은 숙달을 입증하지 않습니다. 메커니즘을 드러내는 경우 데이터 시각화를 계속 사용할 수 있습니다.

<a id="teach-longitudinal-learning-state-upgrade-2026-10-08"></a>
# Teach: 장기 학습 상태 개선 (2026-10-08)

출처는 검사한 Matt Pocock의 `mattpocock/skills`, `skills/productivity/teach/SKILL.md`,
`MISSION-FORMAT.md`와 `LEARNING-RECORD-FORMAT.md`입니다.
mission 우선 수업, 근거에 따라 작성하는 학습 기록, 인출, 적응형 다음 수업, 신뢰할 수 있는 자원과
빠른 참조를 유지합니다. 기존 오프라인 HTML 과정 자산과 식별 정보가 입증된 비공개 workspace
또는 명시적인 추적 대상 workspace에 맞게 적응합니다. 레거시 `.tigerkit/study`는 자동 이전 없이
보존합니다. 보편적인 루트 골격, 활동 일지, 숙달 가정, 새 scheduler와 자동 외부 발행을 제외합니다.

<a id="distillation-provenance"></a>
# 증류 출처

2026-09-19에 Matt Pocock skills revision
`c55ee46073ed923f86ce59a5eb3b6d895095d1b7`의
[teach](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/productivity/teach/SKILL.md)와
[research](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/research/SKILL.md)를 검토했습니다.
두 구현과 본문에 포함된 설계 이유를 모두 읽었습니다. 별도의 upstream 동작 평가는 검증하지
않았습니다. 이는 독립적인 증류이며 복사한 코드나 workspace framework가 아닙니다.

- **keep:** 실용적인 학습 목표, 신뢰할 수 있는 출처, 수준에 맞는 예시, 인출, 실제 답변에 기반한 피드백과 재사용 가능한 용어를 유지합니다.
- **adapt:** 범위가 정해진 과정은 curriculum, 출처와 장을 유지하고, 인터뷰는 주제별 학습자 profile도 유지합니다. 이전 기록에는 주제, 목표와 출처 확인이 필요합니다.
- **adapt:** 조사를 권고 보고서가 아니라 선수 지식을 고려한 과정으로 전환합니다. 렌더링은 수업 설계를 따르며 자동 출력은 `.tigerkit/study/`가 담당합니다.
- **omit:** 이 snapshot에서는 필수 mission 인터뷰를 제외합니다. 아래의 범위를 한정한 재평가를 참조합니다. 루트 수준 workspace 골격, 자동 브라우저 실행, 기본 백그라운드 배정과 경직된 HTML·퀴즈 형식을 제외합니다.

`tk-research`는 의사결정 지원을, `tk-explain`은 알려진 개념의 시각화를 담당합니다.
`tk-retro`는 세션 학습을 분석하지만 스킬을 작성하지 않습니다. 어느 것도 생소한 주제 조사에 이어
수업과 관찰한 인출 피드백까지 제공하는 작업을 포괄하지 않습니다. 저장소 평가는 이 구분과
사용할 수 없는 출처를 다룹니다.

<a id="course-mission-alignment-416"></a>
## 과정 mission 정렬 (#416)

2026-10-05에 `mattpocock/skills` revision
`24fe0ef7737efae15c87225755e9f6f5965e4888`의
`skills/productivity/teach/SKILL.md` (The Mission)와 `MISSION-FORMAT.md`를 검토했습니다.
현재 구현과 mission을 수업 선택에 연결하는 설계 이유를 모두 읽었습니다. 별도의 upstream 동작
평가와 학습 효과는 검증되지 않은 상태입니다. 이 재평가는 이전의 필수 인터뷰 제외만 대체합니다.

- `keep`: 역량 중심 목표, 명시적인 제약·제외 사항과 mission에 연결된 수업을 유지합니다.
- `adapt`: 장 간 의존성이 있는 새 과정에 기본 mission 정렬 라운드를 적용합니다. 현재의 명시적인 답변으로 이를 충족하며, 고정 질문서나 추가 확인이 뒤따르지 않습니다. 기존 주제별 curriculum·profile에 mission과 선언한 지식 대 입증한 지식을 출처와 함께 저장한 뒤 선수 지식과 점검에 연결합니다.
- `omit`: 명시적으로 짧은 설명이나 인터뷰 생략을 요청했거나, 집중 설명이거나, 식별 정보를 검증한 이어가기인 경우 필수 인터뷰를 제외합니다. 생략했을 때 합의를 만들어 내지 않습니다. 루트 workspace 골격, 자동 열기, 백그라운드 배정과 경직된 수업 형식에 대한 기존 제외를 유지합니다.

<a id="course-redesign-375"></a>
## 과정 재설계 (#375)

`lowwwbank/anything-to-course`의 `f11bbf21572a9864759929946c2c3da6857e1744`를 검토했습니다.
`SKILL.md`, `references/course-blueprint.md`, `references/practice-design.md`와
`references/quality-rubrics.md`가 구현, 설계 이유와 작성자 품질 기준을 제공합니다.
별도로 실행할 수 있는 동작 평가는 찾지 못했고, 학습 성과 효과는 재현하지 않았습니다.

- **keep:** 역량 기반 curriculum, 의존성 순서, 첫 사용 시 정의, 인출, 전이와 시도에서 분리한 피드백을 유지합니다.
- **adapt:** 점차 줄이는 도움, 누적 체크포인트와 간격을 둔 인출을 고정된 모듈·질문 수가 아니라 실제 과정 범위에 맞춥니다. 범위를 한정한 사전 탐색과 학습자 소유 질문으로 심층 조사 단계를 선택합니다. 인터뷰 profile은 `.tigerkit/` 아래에서 주제별로 유지합니다.
- **omit:** 필수 예제 수업 승인, 고정 복습 간격, 자동 개인지도 초대, 전역 진행 상태와 과정 골격 전체 도입을 제외합니다.

`MisterBrookT/vividoc`의 `32c7cf963e90c06b00143330f2ad5c6e2366b549`에서
`docs/method.md`, `prompts/executor_prompt.py`의 텍스트·상호작용 단계와 `docs/eval.md`를 검토했습니다.
평가 설계는 콘텐츠 품질과 렌더링·상호작용 정확성을 분리합니다. upstream benchmark 결과와
런타임 실행은 검증되지 않았으며 TigerKit 성능의 근거가 아닙니다.

- **keep:** 콘텐츠 중심 시각적 상호작용과 분리된 콘텐츠·렌더링 검증을 유지합니다.
- **adapt:** 정본 `tk-explain` HTML 참조를 통해 장 anchor와 키보드로 접근 가능한 정답 공개가 있는 오프라인 HTML 산출물 하나로 적응하고, 각 설치 패키지에 동기화합니다.
- **omit:** 제공자 pipeline, 스타일 planner, 고정 지식 단위 수, 서버·런타임과 외부 renderer 의존성을 제외합니다. upstream 코드나 템플릿은 가져와 포함하지 않습니다.

기존 `tk-grill`의 질문 frontier는 선수 지식을 고려한 범위 설정에만 활용합니다. 별도의 공유 이해
관문과 제품 의사결정 workflow는 가져오지 않습니다. `tk-explain`의 초점은 유지합니다.
`tk-explain` 변경 모드는 HTML 관례를 공유하면서 정확한 비교 근거를 유지합니다.

<a id="finite-corpus-coverage-380"></a>
## 유한 자료 집합의 포괄 범위 (#380)

`Lum1104/video-to-skill`의 `5e9f97e89855a8a0ea998ba85e179fbc1765d4b7`에서
`docs/ambitious-startups-v1-v2-product-audit.md`와 `docs/generated-skill-v2.md`를 검토했습니다.
산출물 감사는 출처 보존과 지침 품질을 분리합니다. 현재 설계는 명시적인 처리 결과와 이유를
요구합니다. upstream 런타임·평가 실행은 재현하지 않았습니다.

- **keep:** 중요한 출처 누락은 드러나야 하고 완결성 주장은 근거 범위에 한정되어야 한다는 원칙을 유지합니다.
- **adapt:** 사용자가 지정한 유한 집합에 대해서만 기존 `sources.md`에 출처별 처리 결과를 기록합니다. 개방형 조사 경로와 유용한 부분 수업을 유지합니다.
- **omit:** 의미 단위 대장, 근거 데이터베이스, compiler, ID, manifest와 포괄 범위 지표를 제외합니다.

TigerKit fixture는 사용할 수 없음, 부분 제공, 의도적 누락, 전체 자료 집합과 개방형 사례를
독립적으로 다룹니다. upstream 구현이나 fixture를 복사하지 않습니다.

<a id="executable-exercise-discrimination-386"></a>
## 실행 가능한 연습의 판별력 (#386)

`matlab/agent-skills-playground`의 `7b14a7756bf2765a31840699bc27c8d7240083ac`에서
`demos/course-generation/skills/matlab-create-course-activity/references/matlab-validation-rules.md`,
`demos/assessment-generation-for-matlab-grader/evals/README.md` (EV-G3, G4, G7, G9)와
병합된 PR #26 (`3fc3d57a1568d0dcf8f9b59b5186accdb075e779`)을 검토했습니다.
구현, PR 설계 이유와 시나리오 기준을 검사했습니다. upstream MATLAB 실행은 검증되지 않았습니다.

- **keep:** 참조 풀이가 통과하는 것만으로 의도한 성과의 판별력이 입증되지는 않는다는 원칙을 유지합니다.
- **adapt:** 이미 사용 가능한 안전한 런타임이 있다는 조건 아래, 실제 참조 풀이 통과와 더불어 정상 실행되지만 그럴듯하게 틀린 풀이가 하나 이상 실패하는지 확인하도록 적응합니다. 약한 점검을 보완하고, 관찰한 실패에 피드백을 연결하며, 실행 불가를 정직하게 유지하고 기존 일시적 임시 공간을 사용합니다.
- **omit:** MATLAB MCP 요건, 고정된 두 mutant, grader profile, 강사 관문, 줄 잠금, 평가 대장, 런타임 설치와 지속 검증 보고서를 제외합니다.

집중된 Python fixture는 독립적으로 작성했습니다. upstream 코드나 fixture는 복사하지 않습니다.

<a id="shared-writing-and-html-provenance"></a>
# 공통 글쓰기와 HTML 출처

<a id="optional-revisit-reference-artifacts-425"></a>
## 선택적인 재방문용 참조 산출물 (#425)

2026-10-07에 `mattpocock/skills@6fd947921b935b7e1e69293a200400f0fdd5c15f`의
`skills/productivity/teach/SKILL.md`를 수업·참조 구분과 그 이유까지 검토했습니다.
별도의 upstream 동작 평가와 학습 효과는 검증되지 않은 상태입니다.
이미 가르친 자료를 빠르게 찾아보는 유용한 보조 자료를 유지합니다. 선택적인 과정 내부
`reference/` 단위, 링크, 필수 주의사항과 출처를 기존 주제 식별 정보, 이어가기와 HTML 계약에
맞게 적응합니다. 장별 할당량, 빈 골격, 루트 workspace framework, flashcard, 알림, 숙달 추론과
새 렌더링 의존성을 제외합니다. 출처의 원래 MIT 고지는 이 패키지의 `LICENSE.txt`에 이미 포함되어 있습니다.

upstream 증류를 위한 유지보수 기록이며 스킬의 읽기 경로에 포함되지 않습니다.

## clear-writing.md

- `docwriter-org/plain-writing-skill`, `f0d3630983ac7a82aa580f1c1509d72df739ee12`: 관련 배경, 구체적인 주어, 일관된 설명과 용어를 참고합니다. 규칙 3과 15는 한국어의 내용 없는 강조와 가운뎃점 요건에도 활용합니다. 무관한 서식 금지를 가져오지 않고 뒷받침되는 구체적 내용과 보호 literal에 맞게 적응합니다.
- `hjongc/humanizer-kr`, `a1a7069a32f669afe4b10e35e9522ff504a13263`: 독자·격식 수준 적합성, 맥락에 맞는 편집, 절제된 주장과 내부 자연스러움 검토를 참고합니다.
- `snflkd/fluent-korean`, `ce8683f0eba8cddb91de4dcd151425ff73e60498`: 한국어 문장 성분, 조사·어미, 정확한 어휘와 literal 표현 경계를 참고합니다. 이유와 예시를 포함한 선택적 적응이며 upstream 전역 출력 스타일을 대체하지 않습니다.

- `evergreentree97/K-Humanizer`, `324435d561ba48d53de6b7d3fb3dd72cf77030dc`: 관계를 만들어 내지 않으면서 유용한 문단 연결을 보존합니다.
- `epoko77-ai/im-not-ai`, `9747f036cdc28a1a8aea4dc71fef1f7846eb96f7`: 맥락에 맞는 강도, 밀도에 따른 선택적 편집, 새로운 문체 결함 방지와 실증 근거가 가정한 패턴에 모순될 때의 보수적 교정을 참고합니다. taxonomy, 저자 판정과 수치 임계값은 가져오지 않습니다.

- `conorbronsdon/avoid-ai-writing`, `c4783463cf019a8943364c1ef5f80e0a4c8bff94`: 후보에서 정당한 수정으로 이어지는 범위, 영향받지 않는 구절의 보존과 유효한 수정 없음 결과를 참고합니다. detector, taxonomy, 검토 횟수 예산이나 공개 감사 이력은 가져오지 않습니다.

- `conorbronsdon/avoid-ai-writing`, `5dd2e4ab72b9e0b7e125e5cb592af87033da4fda` (`9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43`와 비교): 기계적 보존과 의미적 보존의 분리, 동등한 숫자 표기와 정직한 불완전 검증을 참고합니다. 내부 두 단계와 최종 결과 하나를 유지하고 이 안전장치만 적응합니다. upstream validator, detector, 인계 묶음, 복구 예산과 공개 검증 보고서는 제외합니다.

문체 예시의 사실 경계에는 `addyosmani/clarity`,
`e27ceeff60368cf6966b4ea00a5b9b36418ee9a0`의 `SKILL.md`, `references/edit.md`와
`evals/cases.json` (`voice_sample_controls_style_not_facts`)도 참고합니다. 진실 보존을 유지하고,
표현에만 예시를 쓰도록 적응하며, 공동 집필, detector와 공개 검토 보고서는 제외합니다.
프로젝트 친숙도는 기존 독자·맥락 계약을 독립적으로 확장한 것이며, 검증된 upstream 프로젝트
친숙도 규칙이 있다는 주장이 아닙니다.

원래 MIT 고지는 호출 패키지의 `LICENSE.txt`에 있습니다.

평가 강도와 확실성의 구분에는 `dotoricode/korean-humanizer`, `4fc566b7d7ded76887f7a85c0886e44796e5e38c`의 `references/ko-ai-signals.md`와 네이티브 스킬 QA를 참고합니다. 양보 표현 보존에는 `conorbronsdon/avoid-ai-writing`, `bdeb726580634868b254972d8eab1a9340d9db16`의 `FALSE_CONCESSION`, PR #359와 그 fixture를 참고합니다. 의미 보존과 과잉 교정 금지 사례를 적응하고 detector 정규식, taxonomy, 출력 템플릿과 런타임 도구는 제외합니다.

주장과 근거의 결합에는 `AIScientists-Dev/academic-humanizer`,
`94b88b23703bed7df507acae7d6d5876209a0cdf`도 참고합니다. 근거 추가, 학술 taxonomy와 투고처 규칙은 제외합니다.

의미 있는 양태 표현에는 `epoko77-ai/im-not-ai`,
`92b2936956d65d62ff4b19b75cccad8e3429bf43`도 참고합니다. A-10/G-2와 그 교정 이력은 반복되더라도
주장 강도를 보존해야 하는 이유가 됩니다. 장르 전반에 의미 동등성을 적용하고, 특정 도메인만의
예외, 고정 반복 임계값, 유보 표현 사전, 표식 수와 런타임 복원은 제외합니다.

재작성 전용 범위에는 `dotoricode/korean-humanizer`, `93580567d4c965024e5b9eb1fb96ace3e7b45907`의 `SKILL.md`, PR #6과 패키지 스킬 QA를 참고합니다. 명시적으로 요청받은 조언은 보존하면서 편집 전용 경계를 적응합니다. 고정 출력 구획과 배포·런타임 도구는 제외합니다.

## html-output.md

동적 그림 출처 (2026-10-05)는 `nicobailon/visual-explainer`의
`5846f5aef34a23c8fea389d2f23ce56224cbf840`, `plugins/visual-explainer/SKILL.md`,
해당 패키지의 `references/diagrams.md` (Live figure)와 `templates/page.html`입니다.
가벼운 상호작용과 읽을 수 있는 정적 상태를 유지합니다. 공유 순수 모델 계산, 작은 조작부,
검증된 기본값과 단순화 모델 공개를 적응합니다. upstream 템플릿, 외부 의존성, 강제적인 그림 우선
배치와 자동 열기는 제외합니다. 별도의 upstream 동작 평가와 런타임 효과는 검증되지 않았습니다.
호출 패키지의 `LICENSE.txt`가 MIT 고지를 보존합니다.

## interactive-examples.md

출처는 동작에 참고합니다. 그 런타임·문체 지침은 의존성이나 권한이 아닙니다.

- `Unclecheng-li/AI_Animation`, `skills/flowchart/SKILL.md`, revision `22ce6df3754c3d914caee78e59b24903191f01bc`: 사용자 제어 단계 진행과 일시정지·초기화를 갖춘 재생을 유지합니다. 움직임을 설명용 전환과 일시정지된 초기 상태에 맞게 적응합니다. 필수 연속 애니메이션, 장면·줄 할당량, CDN 글꼴과 고정 시각 스타일은 제외합니다.
- `CopilotKit/OpenGenerativeUI`, `apps/agent/skills/advanced-visualization/SKILL.md`, revision `457e60cdf7f63fb78004486e1dc7ba753194696d`, 8~9부: 직접 조작, 스스로 설명하는 시각 자료와 색상에만 의존하지 않는 단서를 유지합니다. 콘텐츠에 따른 시각 자료 선택을 완전한 초기화와 눈에 보이는 인과적 차이를 갖춘 오프라인 설명에 맞게 적응합니다. sandbox·도구 계약, 호스트 bridge, 외부 라이브러리와 widget 전용 내레이션 규칙은 제외합니다.

출처의 메커니즘과 설계 이유를 검사했습니다. 로컬 산출물 비교는 예시 수준의 근거를 제공하며
일반적인 upstream 성능 주장은 아닙니다. 전체 호스트 런타임과 영상 backend 효과는 이 계약 범위 밖입니다.


<a id="lesson-files-and-response-adaptation-2026-10-25"></a>
## 수업 파일과 응답 적응 (2026-10-25)

`mattpocock/skills@5beb35b040e3de97e54fa9e386d7e42d15c295c2`의
`skills/productivity/teach/SKILL.md`, `LEARNING-RECORD-FORMAT.md`와
`docs/productivity/teach.md`를 검토했습니다. 동작은 오래된 사용 일화가 아니라 현재 출처가 소유합니다.

- **keep:** mission에 연결된 범위가 정해진 HTML 수업 하나, 신뢰할 수 있는 자원과 필요한 경우에만 남기는 기록을 유지합니다.
- **adapt:** 새 주제의 번호가 붙은 수업 파일, 가벼운 모음 index와 재사용한 표현을 TigerKit의 기존 독립적인 오프라인 HTML 계약에 맞게 적응합니다. 명시적인 전체 다중 장 요청과 식별 정보가 일치하는 레거시 저장 위치를 이전하지 않고 보존합니다.
- **omit:** 필수 별도 저장소, 자동 브라우저 열기, 강제 참조 출력, 정확히 같은 답변 길이, 전역 메모와 자동 커뮤니티 라우팅은 제외합니다.

`SebastianElvis/hammer@c5b86153b15621649560cee247659840738aadae`의
`skills/teach/SKILL.md`, `references/evaluation-rubric.md`, `references/refusal-rules.md`,
`evals/README.md`, `evals/tasks/refusal/just-tell-me.json`과
`evals/graders/code/no_answer_leak.sh`를 검토했습니다.

- **keep:** 올바른 추론, 부분적인 이해와 잘못된 모델을 통해 도달한 정답을 구분하고 실제 근거로 다음 도움을 선택하는 원칙을 유지합니다.
- **adapt:** 관찰한 근거가 다음 단위를 바꿀 때만 범위가 좁은 피드백, 반례·재시도와 필요한 경우에만 남기는 기록을 적용합니다. 추론이 없으면 불확실성을 보존합니다.
- **omit:** 고정 거절 단계, 보이지 않은 추론의 추정, 자신감을 오개념의 증거로 취급하기, 전역 profile, 일일 로그와 런타임·평가 기반 시설을 제외합니다.

이 revision의 upstream harness에는 거절 작업 하나가 있고 사람이 보정한 judge 레이블은 없습니다.
그 token 유출 점검은 이해, 전이나 TigerKit 학습 효과를 입증하지 않습니다. upstream harness는
실행하지 않았습니다. TigerKit 동작 시나리오는 독립적으로 작성했습니다. 실제 수업 진행 점검은
구현 근거이며 통제된 학습 비교가 아닙니다. Matt Pocock의 MIT 고지는 이미 있었으며 Hammer의
MIT 고지는 `LICENSE.txt`에 포함되어 있습니다.

<a id="content-only-document-assembly-2026-10-25"></a>
## 콘텐츠만으로 문서 조립하기 (2026-10-25)

현재 `nicobailon/visual-explainer@5f378868e0ea745a6284b51e710c390f0c76f72c`의
`plugins/visual-explainer/SKILL.md`, `templates/page.html`과 `eval/README.md`, 그리고
`mattpocock/skills@5beb35b040e3de97e54fa9e386d7e42d15c295c2`의
`skills/productivity/teach/SKILL.md`에서 자산과 범위를 한정한 수업 부분을 검토했습니다.
구현과 내장된 설계 이유는 로컬 자산 삽입, 재사용과 작은 소스 수정을 지향합니다.
visual-explainer 평가는 정확성과 토큰 사용량을 분리합니다. upstream 런타임과 전체 소요 시간은
재현하지 않았습니다.

- **keep:** 공유 표현의 로컬 삽입, 재사용 가능한 의미적 구성 요소와 소스 수정을 유지합니다.
- **adapt:** 기존 오프라인 HTML, 설정, 내보내기와 브라우저 검증 계약 아래 독립적으로 작성한 stdlib builder와 shell을 적응합니다. 새 일반 설명·수업 문서에만 기본으로 사용합니다. 유지한 generator와 특수 인터페이스는 소유권을 유지합니다.
- **omit:** 원본 kit·코드·템플릿, 외부 글꼴·CDN, 자동 브라우저 열기, 그림 우선·문장 할당량, 추가 Markdown, 소비자 런타임과 렌더링 점검 면제를 제외합니다.

TigerKit에서 부족했던 것은 실행 가능한 shell 조립이었습니다. 이미 CSS/JS와 탐색 마크업 지침을
제공했지만 agent가 여전히 그 마크업과 인라인 자산을 구성해야 했습니다. 작성하는 마크업 감소는
관찰 가능한 메커니즘이며 전체 속도 주장이 아닙니다. 현재 사용자 요청은 한 단계 HTML과
콘텐츠·검증 품질을 명시적으로 보존합니다.

<a id="independent-artifact-review-and-recognitionaction-coverage-2026-10-26"></a>
## 독립 산출물 검토와 식별·행동 포괄 범위 (2026-10-26)

현재 `mattpocock/skills@5beb35b040e3de97e54fa9e386d7e42d15c295c2`의
`skills/productivity/teach/SKILL.md`는 맥락에 유지하고 main 식별 정보를 다시 확인했으며,
`obra/superpowers@2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`의
`skills/requesting-code-review/SKILL.md`와 `code-reviewer.md`도 검토했습니다.
후자의 구현과 설계 이유는 새 검토자 맥락, 검사한 근거, 심각도와 진행 전 교정을 사용합니다.
별도의 upstream 콘텐츠 검토 평가는 확인하지 못했습니다. tests/README.md 조회는 사용할 수
없었고 upstream 런타임·학습 효과는 재현하지 않았습니다.

- **keep:** 범위를 한정한 수업 목표, 완전한 풀이 자료와 근거 기반 독립 검토를 유지합니다.
- **adapt:** 현재의 명시적인 사용자 workflow를 읽기 전용 반대 관점 콘텐츠 검토자 한 명, 현재 산출물 식별 정보, 목표를 막는 누락, 보완·재검토와 정직한 실행 불가 보고에 맞게 적응합니다. 식별에 필요한 입력, 공간상의 행위자·경로와 공개 전의 정확한 질문 상태를 가르칩니다.
- **omit:** 코드 리뷰·병합 판정, Git 범위 템플릿, 검토자 맥락으로 쓰는 작성자 평가, orchestration 런타임, 새 스킬, 연쇄 검토자, 문체 할당량과 숙달 추론을 제외합니다.

이전의 인과 설명, 공간 배치 포괄 범위, 검증자 사전 점검과 인라인 참조는 이미 존재하며 유지합니다.
설명·수업 제작의 브라우저 점검에는 이제 명시적인 사용자 범위가 필요합니다. 별도로 요청한 점검은
기존 제공자·근거·안전 계약을 유지합니다. 다른 HTML 담당자는 범위가 정해진 UI 점검을 유지합니다.
출처 점검과 콘텐츠 검토는 계속 필수입니다. 지침과 fixture는 독립적으로 작성했으며 원본 코드나
템플릿을 복사하지 않습니다.

<a id="lesson-presentation-2026-10-27"></a>
## 수업 표현 (2026-10-27)

이 이슈의 고정된 조사 근거는 Code Hike `code-hike/codehike@cd81d8af1c503b699cbf0458d504e4578bcb9c74`의
`apps/web/content/docs/layouts/scrollycoding.mdx`와 TutorialKit
`stackblitz/tutorialkit@80cb118647a45cc0dcef1f8018ebc0eef845c8eb`의
`packages/react/src/Panels/EditorPanel.tsx`입니다. 설명과 예시를 가까이 두고 연습, 힌트, 풀이와
재시도를 구분하는 원칙을 유지합니다. 네이티브 오프라인 HTML과 작은 로컬 개선에 맞게 적응하며,
원본 코드, 편집기, 런타임, 서버, 진행 추적과 채점은 제외합니다. 그 런타임과 학습 성과는 이 구현에서
재현하거나 입증하지 않았습니다.
