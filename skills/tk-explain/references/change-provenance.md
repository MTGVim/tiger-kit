<a id="distillation-provenance"></a>
# 증류 출처 기록

<a id="human-comprehension-and-blast-radius-review"></a>
## 사람의 이해와 영향 범위 검토

2026-10-07에 `joshuawheelock/grill-me@2d0c1c492b2f1c3a3b708d2735fdb9131ecbf060`의
`skills/grill-me/SKILL.md`를 검토했습니다. 현재 구현과 질문 품질 규칙을 읽었습니다.
유지보수자에게 필요한 멘탈 모델 확인을 유지합니다. 동작·제어·데이터 흐름, 상태, 경계,
절충, 컴포넌트 간 영향과 실패 처리 질문을 이 스킬의 기존
단일 산출물 이해 확인에 맞게 조정합니다. 저장소 전체 무작위 표본 추출, 영속적인 퀴즈 상태,
채점 대화와 실행 도우미는 제외합니다.

2026-10-07에
`ysk8hori/delta-typescript-graph-action@6fffe4437c77d8b70fd38052b1a302affa9db43a`의
`README.md`와 제시된 변경 파일 의존성 보기를 검토했습니다. 변경 노드와
검증된 관련 맥락을 함께 제시하면 검토자에게 도움이 된다는 발상을 유지합니다. 이를 TigerKit의 기존
Dependency graph와 Architecture delta 문법에 맞게 조정하며, 삭제나
이동 때문에 단일 오버레이가 모호해지면 base/head 보기를 구분합니다. GitHub Action, Mermaid 런타임, TypeScript 전용
분석, 노드 할당량, 지표와 PR 댓글 발행은 제외합니다.

사람이 주의를 기울여야 할 영역은 AI가 생성한 변경량이 많아져도
사람의 이해를 보존해야 한다는 사용자 요구에서 비롯된 TigerKit 확장입니다. 파일을 AI 작성 여부로 분류하지
않으며, 생성 파일이나 반복 파일을 자동으로 건너뛰어도 안전하다고 취급하지 않습니다. 영속적인 인지
부채 장부, 강제 merge 관문과 편집 차단은 여전히 `tk-explain` 변경 모드의 범위 밖입니다. 이 스킬은
고정된 변경 하나를 설명하며, 지속적인 부채 추적은 TigerKit에 별도 담당자가 추가된다면 그 담당자에게 맡깁니다.

별도의 upstream 런타임 효과와 학습 결과는 재현하지 않았으며 검증되지 않은 상태입니다.
upstream 런타임, 템플릿이나 구현 코드는 복사하지 않습니다.

<a id="preserved-invariants"></a>
## 보존된 불변 조건

2026-10-01에 `Data-System-School/agent-skills`의
`a117418ab3596c59d641cab4cb89bdbe560fb277`에서 `investigate-codebase/SKILL.md`,
`references/analyze-pr-impact.md`와 `examples/investigate-codebase/duckdb/03-impact-pr-19235.md`를 검토했습니다.
이 예시는 최적화기의 불변 조건과 지정되지 않은 순서를 구별하고,
규칙 토글 근거가 실제 base/head 귀속과 어떻게 다른지 명시적으로 한정합니다.
구현, 포함된 설계 근거와 보고된 검사를 읽었습니다. TigerKit은
upstream 런타임 측정을 재현하지 않았습니다.

- `keep`: 고정된 비교 끝점과 출처·런타임·추론의 구분을 유지합니다.
- `adapt`: 동작 변경과 함께 보존된 불변 조건을 식별하고 가르칩니다.
  고정된 근거로 검증하거나 정확한 한계를 유지합니다.
- `omit`: 필수 행렬, 위험 점수, 검토·merge 판정, 추가 보고서와
  upstream 실행 프레임워크는 제외합니다. `tk-review`가 계속 결함을 담당합니다.

보조 출처로 제안된 `Chris-Graffagnino/explain-diff`의
`fec813246040e43108d1c7206b97454ee4c4a201`은 이 변경에 필요하지 않아
제외합니다. 해당 구현·평가 근거는 미검증 상태이며, 도입 근거가 아닙니다.

2026-09-19에 검토했습니다. Geoffrey Litt의 [explain-diff Gist](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524/126e7fe9eecaafadfe1ac8bb183d135812b608f2)
revision `126e7fe9eecaafadfe1ac8bb183d135812b608f2`에서 교육 순서를 참고했습니다.
토론에서 퀴즈 단서(Butanium, fm1randa), 주변 코드·흐름 분석
(yudhiesh-oc), 렌더러 재사용(ankitg12)과 주입 경계(ehsan-ami)를 읽었습니다.
[ankitg12 파생본](https://gist.github.com/ankitg12/8e808d387799de4e9839bc393f8e6405)은
2026-09-19 스냅샷에서 `render.py`를 포함해 확인했습니다. upstream 코드는 복사하지 않습니다.
파생본의 고정 revision과 upstream 자동 동작 평가는 여전히 미검증 상태입니다.

- **유지:** 배경, 직관, 논리적 해설과 이해 확인을 유지합니다. 이는
  검토 판정이나 파일별 diff 요약과 다릅니다.
- **조정:** 주장을 불변 원본 스냅샷과 버전을 명시한 행에 결합합니다. 런타임
  순서로 설명하고 추론한 의도와 사실을 분리합니다. 가져온 자료는 수동적인 데이터로 유지합니다.
- **조정:** 콘텐츠 우선 렌더링과 답 단서 검사를 적용하고, 자유 응답·전이 문제를 우선합니다.
- **제외:** 필수 HTML 스타일, 전역 임시 출력, 고정된 다섯 문항 객관식 퀴즈, 자동
  브라우저 열기와 번들 upstream 렌더러는 제외합니다. TigerKit은 기본적으로 오프라인 HTML 산출물 하나를 사용합니다.
  명시적으로 요청된 다른 형식은 담당 SKILL.md 계약에 따라 존중합니다.

TigerKit의 `tk-explain`은 개념 시각화를 다루며, 이전·이후 원본 재구성을 다루지 않습니다.
`tk-review`는 교육이 아니라 결함과 승인을 담당합니다. 저장소 평가 카탈로그의 로컬 성공·압박 사례는
새 경계를 시험합니다. upstream 토론은 설계 근거이며,
TigerKit 구현이 해당 사례를 통과한다는 증거가 아닙니다.

<a id="shared-writing-and-html-provenance"></a>
# 공통 글쓰기와 HTML 출처 기록

upstream 증류를 위한 유지보수 기록이며, 스킬의 읽기 경로에 포함되지 않습니다.

## clear-writing.md

- `docwriter-org/plain-writing-skill`, `f0d3630983ac7a82aa580f1c1509d72df739ee12`: 관련 배경, 구체적인 주어, 일관된 설명과 용어를 참고합니다. 규칙 3과 15는 한국어의 내용 없는 강조 및 가운뎃점 요구 사항에도 참고했습니다. 관련 없는 서식 금지를 가져오지 않고, 근거 있는 구체성과 보호 대상 리터럴에 맞게 조정합니다.
- `hjongc/humanizer-kr`, `a1a7069a32f669afe4b10e35e9522ff504a13263`: 독자·문체 적합성, 맥락에 맞는 편집, 절제된 주장과 내부 자연스러움 검토를 참고합니다.
- `snflkd/fluent-korean`, `ce8683f0eba8cddb91de4dcd151425ff73e60498`: 한국어 문장 성분, 조사·어미, 정확한 어휘와 리터럴 표현의 경계를 참고합니다. 이는 근거와 예시를 갖춘 선택적 조정이며, upstream의 전역 출력 스타일을 대체하지 않습니다.

- `evergreentree97/K-Humanizer`, `324435d561ba48d53de6b7d3fb3dd72cf77030dc`: 관계를 지어내지 않으면서 유용한 문단 연결을 보존합니다.
- `epoko77-ai/im-not-ai`, `9747f036cdc28a1a8aea4dc71fef1f7846eb96f7`: 맥락에 따른 강도, 밀도에 따른 선택적 편집, 새로운 문체 결함 방지와 경험적 근거가 추정 패턴에 어긋날 때의 보수적 수정을 참고합니다. 분류 체계, 작성자 판정과 수치 임계값은 가져오지 않습니다.

- `conorbronsdon/avoid-ai-writing`, `c4783463cf019a8943364c1ef5f80e0a4c8bff94`: 수정 후보에서 근거 있는 수정까지의 범위, 영향받지 않은 구절의 보존과 수정이 없는 유효한 결과를 참고합니다. 탐지기, 분류 체계, 검토 횟수 예산이나 공개 감사 기록은 가져오지 않습니다.

- `conorbronsdon/avoid-ai-writing`, `5dd2e4ab72b9e0b7e125e5cb592af87033da4fda`(`9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43`과 비교): 기계적 보존과 의미 보존의 분리, 동등한 수치 표기와 미완료 검증의 정직한 보고를 참고합니다. 두 번의 내부 검토와 하나의 최종 결과를 유지하고, 이러한 보호 장치만 조정합니다. upstream 검증기, 탐지기, 인수인계 봉투 형식, 수정 예산과 공개 검증 보고서는 제외합니다.

스타일 예시의 사실적 경계는 `addyosmani/clarity`,
`e27ceeff60368cf6966b4ea00a5b9b36418ee9a0`의 `SKILL.md`, `references/edit.md`와
`evals/cases.json`(`voice_sample_controls_style_not_facts`)도 참고합니다. 진실 보존을 유지하고,
표현에만 예시를 사용하도록 조정하며, 공동 집필, 탐지기와 공개 검토 보고서는 제외합니다.
프로젝트 친숙도는 기존 독자·맥락 계약을 독립적으로 확장한 것이며,
검증된 upstream 프로젝트 친숙도 규칙이 있다는 주장이 아닙니다.

원본 MIT 고지는 호출 패키지의 `LICENSE.txt`에 있습니다.

평가적 강도와 확실성의 구분은 `dotoricode/korean-humanizer`, `4fc566b7d7ded76887f7a85c0886e44796e5e38c`(`references/ko-ai-signals.md`와 기본 스킬 QA)를 참고합니다. 양보 표현 보존은 `conorbronsdon/avoid-ai-writing`, `bdeb726580634868b254972d8eab1a9340d9db16`(`FALSE_CONCESSION`, PR #359와 해당 fixture)을 참고합니다. 의미 보존과 과잉 교정을 금지해야 하는 사례를 조정하고, 탐지기 정규식, 분류 체계, 출력 템플릿과 런타임 도구는 제외합니다.

주장과 근거의 결합은 `AIScientists-Dev/academic-humanizer`,
`94b88b23703bed7df507acae7d6d5876209a0cdf`도 참고합니다. 근거 추가, 학술 분류 체계와 발표 매체 규칙은 제외합니다.

의미 있는 양태 표현은 `epoko77-ai/im-not-ai`,
`92b2936956d65d62ff4b19b75cccad8e3429bf43`도 참고합니다. A-10/G-2와 그 수정 이력은 반복되더라도 주장 강도를 보존해야 한다는 근거가 됩니다. 장르 전반에 의미적 동등성을 적용합니다. 특정 분야에만 해당하는 예외, 고정 반복 임계값, 완곡 표현 사전, 표지 개수와 런타임 복원은 제외합니다.

다시 쓰기에만 한정하는 범위는 `dotoricode/korean-humanizer`, `93580567d4c965024e5b9eb1fb96ace3e7b45907`(`SKILL.md`, PR #6과 패키지 스킬 QA)를 참고합니다. 명시적으로 요청된 조언은 보존하면서 편집 전용 경계를 조정합니다. 고정 출력 절과 배포·런타임 도구는 제외합니다.

## html-output.md

동적 그림 출처 기록(2026-10-05): `nicobailon/visual-explainer`의
`5846f5aef34a23c8fea389d2f23ce56224cbf840`, `plugins/visual-explainer/SKILL.md`,
해당 패키지의 `references/diagrams.md`(Live figure)와 `templates/page.html`입니다.
가벼운 상호작용과 읽을 수 있는 정적 상태를 유지합니다. 공유 순수 모델
계산, 작은 컨트롤, 검증된 기본값과 단순화된 모델의 공개를 조정합니다.
upstream 템플릿, 외부 의존성, 강제적인 그림 우선 표현과
자동 열기는 제외합니다. 별도의 upstream 동작 평가와 런타임 효과는
미검증 상태입니다. 호출 패키지의 `LICENSE.txt`에 MIT 고지를 보존합니다.

## interactive-examples.md

출처는 동작에 참고합니다. 출처의 런타임과 스타일 지침은 의존성이나 권한이 아닙니다.

- `Unclecheng-li/AI_Animation`, `skills/flowchart/SKILL.md`, revision `22ce6df3754c3d914caee78e59b24903191f01bc`: 사용자가 제어하는 단계 진행과 일시정지·초기화를 갖춘 재생을 유지합니다. 움직임은 설명용 전이와 처음에 일시정지된 상태에 맞게 조정합니다. 필수 연속 애니메이션, 장면·행 할당량, CDN 글꼴과 고정 시각 스타일은 제외합니다.
- `CopilotKit/OpenGenerativeUI`, `apps/agent/skills/advanced-visualization/SKILL.md`, revision `457e60cdf7f63fb78004486e1dc7ba753194696d`, 8~9부: 직접 조작, 자체로 이해할 수 있는 시각 요소와 색상에만 의존하지 않는 단서를 유지합니다. 콘텐츠에 따른 시각화 선택을 완전한 초기화와 눈에 보이는 인과 차이가 있는 오프라인 설명에 맞게 조정합니다. sandbox·도구 계약, 호스트 브리지, 외부 라이브러리와 위젯 전용 설명 규칙은 제외합니다.

출처의 메커니즘과 설계 근거를 확인했습니다. 로컬 산출물 비교는 예시 수준의 근거이며, 일반적인 upstream 성능 주장이 아닙니다. 전체 호스트 런타임과 영상 백엔드 효과는 이 계약의 범위 밖입니다.

<a id="content-only-document-assembly-2026-10-25"></a>
## 콘텐츠만 작성하는 문서 조립(2026-10-25)

당시 최신 `nicobailon/visual-explainer@5f378868e0ea745a6284b51e710c390f0c76f72c`의
`plugins/visual-explainer/SKILL.md`, `templates/page.html`과 `eval/README.md`를 검토했습니다. 또한
`mattpocock/skills@5beb35b040e3de97e54fa9e386d7e42d15c295c2`의
`skills/productivity/teach/SKILL.md`(Assets와 범위가 정해진 수업)를 검토했습니다. 구현과
포함된 설계 근거는 로컬 자산 주입, 재사용과 작은 원본 수정을 지향합니다.
visual-explainer 평가는 정확성과 토큰 사용을 구별합니다. upstream 런타임과
종단 간 소요 시간은 재현하지 않았습니다.

- **유지:** 공통 표현의 로컬 삽입, 재사용 가능한 의미 컴포넌트와 원본 수정을 유지합니다.
- **조정:** 기존 오프라인 HTML, 설정, 내보내기와 브라우저 검증 계약 아래에서
  독립적으로 작성한 stdlib 빌더와 셸을 사용하도록 조정합니다. 새로 만드는 일반적인
  설명·수업 문서에만 이를 기본값으로 둡니다. 유지되는 생성기와 특수 인터페이스는 담당자를 유지합니다.
- **제외:** 원본 도구 모음·코드·템플릿, 외부 글꼴·CDN, 자동 브라우저 열기,
  그림 우선·산문 할당량, 추가 Markdown, 소비자 런타임과 렌더링 검사 면제를 제외합니다.

TigerKit에 빠져 있던 것은 실행 가능한 셸 조립이었습니다. 이미 CSS/JS와 탐색
마크업 지침을 제공했지만, 에이전트는 여전히 그 마크업을 구성하고 자산을 인라인으로 넣어야 했습니다.
작성해야 하는 마크업의 감소는 관찰 가능한 메커니즘이며, 종단 간 속도 주장이 아닙니다.
현재 사용자 요청은 한 단계 HTML과 콘텐츠·검증 품질을 명시적으로 보존합니다.

<a id="independent-artifact-review-and-recognitionaction-coverage-2026-10-26"></a>
## 독립 산출물 검토와 인식·행동 범위(2026-10-26)

당시 최신 `mattpocock/skills@5beb35b040e3de97e54fa9e386d7e42d15c295c2`
(`skills/productivity/teach/SKILL.md`를 맥락에 유지하고 주 정체성을 재확인했습니다)와
`obra/superpowers@2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`
(`skills/requesting-code-review/SKILL.md`, `code-reviewer.md`)를 검토했습니다. 후자의 구현과
설계 근거는 진행 전에 새로운 검토자 맥락, 확인한 근거, 심각도와 수정을
사용합니다. 별도의 upstream 콘텐츠 검토 평가는 확인하지 못했습니다. tests/README.md
조회가 불가능했고 upstream 런타임·학습 효과는 재현하지 않았습니다.

- **유지:** 범위가 정해진 교육 목표, 완전한 풀이 자료와 근거 기반 독립 검토를 유지합니다.
- **조정:** 현재의 명시적 사용자 작업 절차를 한 명의 읽기 전용 반대 관점 콘텐츠 검토자,
  현재 산출물의 정체성, 목표를 막는 누락, 수정·재검토와 실행 불가의 정직한 보고에 맞게
  조정합니다. 인식에 필요한 입력, 공간상의 행위자·경로와 답 공개 전의 정확한 질문 상태를 가르칩니다.
- **제외:** 코드 검토·merge 판정, Git 범위 템플릿, 검토자 맥락으로 제공하는 작성자 평가,
  오케스트레이션 런타임, 새 스킬, 연쇄 검토자, 문체 할당량과 숙달 추론은 제외합니다.

기존의 인과 설명문, 공간 배치 범위, 검증기 사전 점검과 인라인 참조는 이미
존재하며 유지합니다. 이제 설명·수업 제작의 브라우저 검사에는 명시적인 사용자 범위가
필요합니다. 별도로 요청된 검사는 기존 제공자·근거·안전 계약을 유지합니다.
다른 HTML 담당자는 범위가 정해진 UI 검사를 유지합니다. 출처 검사와 콘텐츠 검토는 여전히 필수입니다.
지침과 fixture는 독립적으로 작성했으며, 원본 코드·템플릿을 복사하지 않습니다.

<a id="source-bound-change-groups-2026-10-27"></a>
## 출처가 결합된 변경 그룹(2026-10-27)

PR Lens `coldteadotai/pr-lens@132ff8bd7d86a318a06965377f8511a267808a5a`의
`packages/agent-skill/references/graph-document.md`, `packages/schema/src/integrity.ts`,
`packages/agent-skill/manual.md`와 MIT 라이선스가 이 이슈의 고정된 조사 근거입니다.
명시적인 정체성, 변경분, 인접 근거와 연결 대상 없는 참조의 거부를 유지합니다. 이를
출처가 결합된 논리 그룹, 끝점 버전과 작은 순수 검증기에 맞게 조정합니다.
PR Lens의 노드 그룹은 아키텍처 클러스터이며, hunk 그룹화의 증거가 아닙니다. 원본 런타임,
코드, 템플릿, 호스팅, 업로드, 발행과 그래프 배치 엔진은 제외합니다. 이 구현에서는 upstream 런타임 동작과
품질 효과를 재현하지 않았습니다.

변경 해설은 해당 고정 출처의 집중 경로와 원본 링크를 순서가 있는 그룹과
선택적인 사용자 조작 흐름 단계를 갖춘 단일 로컬 문서에 맞게 조정합니다. 호스팅
canvas, 에이전트 브리지, 원본 렌더러와 런타임은 제외합니다. UI는 독립적으로 구현했습니다.
시각적 사용성과 upstream 런타임 효과에는 각각의 근거가 필요하며, 빌드로 이를 암시할 수 없습니다.
