# 고지

TigerKit에는 `mattpocock/skills`에서 파생한 동작이 포함되어 있습니다(원본 스냅샷은
커밋 `391a2701dd948f94f56a39f7533f8eea9a859c87`에서 확인됨).

현재 적용된 스킬:

- `grilling`
- `to-spec`
- `to-tickets`
- `implement`

제거된 적용 스킬에서 병합한 동작:

- `tdd` → `implement`
- `diagnosing-bugs` → `implement` 버그 조사 및 계약 계획
- `code-review` → `implement` 내장 검토

과거에 제거된 적용 작업 흐름:

- `grill-me`
- `grill-with-docs`
- `domain-modeling`

현재 적용 스킬의 관계 메타데이터: `relationship: adapted`. 해당 스킬이 계속
배포되는 경우 TigerKit은 상위 원본 스킬 이름에 `tk-` 접두사를 유지하고, 동작은 현재
TigerKit 사양에 맞게 다시 작성합니다.

`tk-grill`은 `mattpocock/skills` 스냅샷
`6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`의
`skills/productivity/grilling/SKILL.md`에서 의사결정 `tree`, 선행 조건을 반영한
`frontier`, 한 차례의 독립 질문 묶음, 사실과 사용자 소유 결정의 분리, 추천 및
`shared understanding` 확인을 적용했습니다. TigerKit은 의무적인 하위 에이전트
`runtime`, `grill-me`/`grill-with-docs` `wrapper`, 자동 구현 전이와 영구 상태를 적용하지
않습니다. 아래 `mattpocock/skills` MIT 라이선스가 이 적용에도 적용됩니다.

`tk-prep`, `tk-pr-respond`, 공유 테스트/SDD와 `tk-audit`의 조건부 엔지니어링 규율은
`mattpocock/skills` 스냅샷 `5b15a47f2d7150f545fbcacbfe381787fc0230dc`에서 다음 원천을 검토해
TigerKit의 기존 소유자와 비공개 참조에 재서술했습니다.

- `skills/engineering/diagnosing-bugs/SKILL.md`
- `skills/engineering/tdd/SKILL.md`
- `skills/engineering/to-tickets/SKILL.md`
- `skills/engineering/codebase-design/SKILL.md`
- `skills/engineering/codebase-design/DEEPENING.md`
- `skills/engineering/codebase-design/DESIGN-IT-TWICE.md`
- `skills/engineering/improve-codebase-architecture/SKILL.md`
- `skills/engineering/domain-modeling/SKILL.md`

적용 범위는 난해하거나 간헐적이거나 성능에 관련된 버그의 `red-capable feedback loop`, 한 행동 단위의
`vertical-first testing`, `expand → migrate batch(es) → contract`, 되돌리기 어려운 모호성의
대안 비교, 관련 저장소 소유 맥락 소비와 근거 기반 `hotspot/locality/deletion-test` 관점입니다. TigerKit은
상위 원본의 의무적인 하위 에이전트 `fan-out`, 아키텍처 용어 강제, 공개 작업 흐름,
`CONTEXT.md`/ADR 생성·관리 수명 주기를 적용하지 않으며 기존 승인/`Seed`/비밀/원격 권한을
유지합니다. 아래 `mattpocock/skills` MIT 라이선스가 이 증류에도 적용됩니다.

`tk-merge-conflict`는 TigerKit 고유 스킬로 유지됩니다(`origin: tigerkit`,
`relationship: native`). 검증된 원본 메타데이터에는 이것이 `mattpocock/skills`의
`resolving-merge-conflicts`를 적용한 것이라고 확인할 근거가 없습니다.

`tk-skill-diagnose`는 `mizchi/skills`의 경험적 `Agent Skill` 평가 방법론을 적용했습니다.
원본 스냅샷은
`7a0d72866a0bb3e9ac3e2768c328b09ba2bc40c4`입니다.

- `meta/empirical-prompt-tuning/SKILL.md`
- `meta/waxa-eval/`

TigerKit은 반복 0의 설명/본문 일관성, 고정 중앙값·대조군·보류군 시나리오, 새 실행자,
양방향 단계 추적, 구조화된 `Issue / Cause / General Fix Rule` 피드백, 한 주제 후보
실험, 수렴 및 실행별 실패 장부를 추려냈습니다. 이 적용은 TigerKit 전용 실패 평면,
호스트/출처 게이트, 작성자 소유권, 로컬 전용 진단 출력, 자원/정확성 우선순위 및
익명화된 상위 원본 이슈 초안을 추가합니다. 상위 원본 표시 문장을 복사하거나
`Darwin` 방식의 광범위한 최적화를 대체하지 않습니다. 관계 메타데이터:
`relationship: adapted`.

`tk-prep`과 `tk-pr-respond`의 공유 SDD/TDD 절차는 `obra/superpowers` v6.3.0의
다음 행동을 TigerKit의 적응형 준비, 패키지 로컬 참조, 최소 복구 경계로 적용했습니다.
원본 스냅샷은 `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`입니다.

- `skills/subagent-driven-development/`
- `skills/test-driven-development/`
- `skills/using-superpowers/references/codex-tools.md`

적용 범위는 행동 우선 RED/GREEN, 좋은 테스트와 변이 규율, 정확한 작업/수정 범위, 말단 역할,
5회 수정 차단기, 증거 우선 검토, Codex `model`+`reasoning_effort` 짝입니다. TigerKit은 원본의
공개 스킬, 실행 체계, 작업공간 계층을 복사하지 않고, `tk-prep`/`tk-pr-respond`의 자체 완결 패키지와
기존 원격 권한 경계를 유지합니다. 관계 메타데이터: `origin: tigerkit`, `relationship: adapted`.

2026-09-14에 현재 기본 브랜치의 위 스냅샷과 미병합
[PR #2297](https://github.com/obra/superpowers/pull/2297)의
`525a1265afd6b2dd9efbc90a04df5e205743ff40`을 비교했습니다. 원본 구현과 PR의 중단 후
복구 설계·압박 평가 보고를 확인했으며, 원본의 작업 공간 평가
`docs/superpowers/specs/2026-07-06-sdd-plan-scoped-workspace-eval-results.md`와
`tests/claude-code/test-sdd-workspace.sh`도 검토했습니다. PR의 평가 실행 원본과 다중 세션
재현은 `unverified`이며, 해당 PR에는 스킬 변경만 있습니다.

- `keep`: 정확한 작업 식별자, 기존 변경 범위, 검증·리뷰 의무와 불명확한 결과의 차단을 유지합니다.
- `adapt`: TigerKit #363에서 확인된 저장 누락을 보완하여, 선택적 복구 장부가 활성화된 경우에만
  위임 전에 전체 `BASE`와 작업 공간·위임 식별자를 보존하고 입증된 기존 작업은 검증·리뷰부터 재개합니다.
- `omit`: 필수 장부, 추가 작업 공간·보고서, 누적 이벤트 기록과 커밋 유무만으로 재위임을 결정하는 규칙은
  도입하지 않습니다. 빈 범위도 미커밋 변경과 이전 자식의 종료 근거를 함께 확인합니다.

`obra/superpowers` 상위 원본 라이선스:

```text
MIT License

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

`mattpocock/skills` 상위 원본 라이선스:

```text
MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

`tk-audit`는 원본 스냅샷
`03369ee6d7cafbfcecc4346539b05b3dc0a603bb`의 `shadcn/improve`를 적용했습니다.

- `skills/improve/SKILL.md`
- `skills/improve/references/plan-template.md`
- `skills/improve/references/audit-playbook.md`

TigerKit은 상위 원본의 수석 조언자/읽기 전용 경계, 증거 우선 감사 범주,
저비용 실행자 인계 품질 및 MIT 저작자 표시를 유지하면서 소유 장부를
`.tigerkit/audit.md`로 바꾸고 `AUD-*` 발견 ID를 사용하며 후보를 TigerKit의
기존 사양·티켓·드라이브 소유자에게 전달합니다. 관계 메타데이터:
`origin: shadcn/improve`, `relationship: adapted`.

`shadcn/improve` 상위 원본 라이선스:

```text
MIT License

Copyright (c) 2026 shadcn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

`tk-eli5`는 `anthropics/claude-plugins-community`의 `eli5` v1.0.0을
원본 스냅샷 `863e70dc7cff21a2facc749e40a7ecd1a5d19833`에서 적용했습니다.

- `eli5/skills/eli5/SKILL.md`
- `eli5/README.md`
- `eli5/.claude-plugin/plugin.json`

TigerKit은 큰 그림·적은 글의 `HTML artifact`와 `/eli5 <topic>` 동작을 유지하면서
`offline self-contained output`, 충돌 없는 `path`, 접근성, `skill` 경계, 검증과 AI 작성자
표시를 추가했습니다. 관계 메타데이터: `origin: anthropics/claude-plugins-community`,
`relationship: adapted`, `upstream-skill: eli5`.

`eli5` `manifest`는 MIT를 표시하며 최초 `package commit`
`0d92c175da762e154c3000ccbc2da8464def3373`의 라이선스는 다음과 같습니다.

```text
MIT License

Copyright (c) 2026 Thariq Shihipar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

`tk-adhd`는 `ayghri/i-have-adhd`의 고정 커밋
`24d22f783e57cb73c957848b588c6f651b6f9cd8`에서
`skills/i-have-adhd/SKILL.md`, `README.md`, `evals/rubric.md`, `LICENSE`를 확인하여 증류했습니다.

- `keep`: 확인된 진행 상태와 다음 행동을 쉽게 찾게 하고 완료한 일을 구체적으로 표시합니다.
- `adapt`: 세션 전체 출력 스타일을 현재 작업의 짧은 현황 안내로 좁히고, 사용자가 상황을 파악하도록 안내 후 턴을 종료합니다. 다음 행동은 재개 이후의 제안으로만 표시합니다.
- `omit`: 상시 모드, 의학적 일반화, 근거 없는 시간 추정, 매번 사용자에게 다음 명령을 넘기는 예시, 설치 훅과 별도 실행 체계는 가져오지 않습니다.

원본 평가는 정확성·자율 수행·실행 가능성·안전·간결성을 구분합니다. 해당 평가 기준은 확인했지만
원본 실행 결과의 재현은 `unverified`입니다. TigerKit의 새 평가는 세션별 근거 구분, 기존 작업 승인에도 현황 안내 후 종료하기,
접근하지 않은 세션 상태를 지어내지 않는 경계에 맞췄습니다. 적용 부분의 MIT 고지는 설치 패키지의
`skills/tk-adhd/LICENSE.txt`에 포함합니다.

2026-09-15에 `ayghri/i-have-adhd`의 최신 커밋
`4092de07ce3ed88389d77c0d623b7af89b40ac0e`에서 원본 스킬, README와 평가 기준을 다시 확인했습니다.
기존 `keep | adapt | omit` 판단을 유지하며, `tk-status`를 `tk-adhd`로 이름 변경했습니다.
복수 세션을 비교할 때 세션별 카드를 출력하도록 명확히 하고 사용자 언어에 맞춰 항목명을 표시합니다.
최신 원본 평가 결과의 재현은 `unverified`입니다.

## 설명 재작성과 한국어 윤문

`tk-plain-writing`은 `docwriter-org/plain-writing-skill`의 고정 커밋
`f0d3630983ac7a82aa580f1c1509d72df739ee12`에서 `skills/plain-writing/SKILL.md`,
`README.md`, `evals/README.md`, `LICENSE`를 확인하여 증류했습니다.

- `keep`: 짧은 배경 복원, 결론 우선, 실제 순서와 인과 관계, 구체적 주체, 일관된 용어를 유지합니다.
- `adapt`: 모든 응답의 기본 문체가 아니라 앞선 설명이나 지정 문서를 재작성하는 독립 호출로 제한합니다.
  이미 제공된 맥락에서 배경을 복원하고, 없는 사실을 보완하지 않으며, 결정 주체와 조건을 보존합니다.
- `omit`: 사전 등재 여부, 절 개수, 목록 길이, 구두점 종류의 일괄 제한과 원본 평가 실행 환경은 가져오지 않습니다.

원본 평가 문서는 동일 입력의 무스킬 결과와 스킬 결과를 규칙별로 비교하며, 67개 작업 중 65개에서
스킬이 우세했다고 보고합니다. 이는 원본의 자체 보고이며 TigerKit의 한국어 이해도 향상이나 원본 동등성을
입증하지 않습니다. 원본 실행 결과의 재현과 무스킬 대비 실측은 `unverified`입니다.

`tk-humanizer-kr`는 `hjongc/humanizer-kr`의 고정 커밋
`a1a7069a32f669afe4b10e35e9522ff504a13263`에서 `skills/humanizer-kr/SKILL.md`,
두 `references` 문서, `README.md`, `tests/test_audit_korean_text.py`,
`examples/evals/output-sample-loop.ko.md`, `LICENSE`를 확인하여 증류했습니다.

- `keep`: 독자와 장르별 말투, 단어 금지 대신 문맥 판단, 사실과 전문 용어 보존, 한 번의 내부 재검토를 유지합니다.
- `adapt`: 사용자가 지정한 문체를 우선하고, 기본 결과는 윤문 본문 하나로 제한합니다. 검토와 복수 시안은
  요청했을 때만 제공합니다. 원본 예시에 나타난 발생 가능성의 빈도 강화와 새 지원 절차 추가를 경계 평가로 다룹니다.
- `omit`: 선택적 정규식 검사 스크립트, 복수 플러그인 배포물, 상시 출처 조사, 기본 감사 보고서는 가져오지 않습니다.

원본 검사는 표현 패턴과 공개 예시의 정적 품질 신호를 다룹니다. 사실 보존을 입증하는 의미 평가나
TigerKit과 원본의 동등성 비교로 간주하지 않습니다. 원본 검사 실행과 무스킬 대비 실측은 `unverified`입니다.

TigerKit 평가는 배경 누락, 전체 문서의 조건 보존, 결정 권한, 불확실성, 정확한 문자열,
문서 속 지시문의 비실행, 이미 자연스러운 글의 과도한 수정 방지, 세 스킬의 호출 경계를 다룹니다.
`tk-adhd`의 현황 안내 후 종료 계약은 그대로 유지하며, 셋을 자동 연쇄 실행하지 않습니다.
각 설치 패키지의 `LICENSE.txt`에 원본 저작권과 MIT 고지를 포함합니다.


## 글 정제 통합과 배경지식 중심 시각 설명

`tk-plain-writing`과 `tk-humanizer-kr`를 `tk-rewrite`로 통합하고, `tk-eli5`를 `tk-explain`으로 개편합니다.
위의 고정 원본과 라이선스 기록은 유지합니다. 앞 절의 독립 호출 설명은 최초 도입 시점의 이력이며,
현재 실행 계약은 새 스킬 본문이 소유합니다.

`snflkd/fluent-korean`의 고정 커밋 `ce8683f0eba8cddb91de4dcd151425ff73e60498`에서
`plugins/fluent-korean/output-styles/fluent-korean.md`, `README.md`, `LICENSE`를 확인했습니다.

- `keep`: 의미를 담는 문장 성분, 조사와 어미, 정확한 한자어와 전문 용어, 코드·주석·인용의 보존을 유지합니다.
- `adapt`: 한국어 문장 검수 기준을 공통 `clear-writing.md`에 선별하여 반영하고, 취지와 한국어 전후 예시를 함께 둡니다.
  설명 문장은 완성하되 제목·표·그림의 짧은 라벨에는 같은 문장 형식을 강제하지 않습니다.
- `omit`: 전역 출력 스타일 설치, 호스트 설정, 다른 에이전트의 실행 방식은 가져오지 않습니다.
  `tigeryoo-ai-setup`의 외부 `fluent-korean` 설정을 변경하거나 의존하지 않습니다.

`anthropics/claude-plugins-community`의 최신 고정 커밋 `a727be1c7bd6064419b6f60d71993a19198adc17`에서
`eli5/skills/eli5/SKILL.md`와 `eli5/README.md`를 다시 확인했습니다.

- `keep`: 시각적인 HTML 설명 자료를 유지하고, 오프라인 실행·접근성·정확성·출처 표시는 계속 검증합니다.
- `adapt`: 성인 독자에게 필요한 배경지식을 먼저 소개하고 실제 구성 요소와 동작을 시각화합니다.
  비유는 요청되거나 도움이 될 때만 보조적으로 사용하고, 그림과 글의 용어·관계를 일치시킵니다.
- `omit`: 아동 수준의 기본 독자 가정, 비유 의무, 장면 수와 단어 수 목표는 제거합니다.

공통 정제 기준의 정본은 `skills/tk-rewrite/references/clear-writing.md`이며 `tk-explain`에는 동일한 사본을
포함합니다. 두 패키지의 `LICENSE.txt`는 정제 원본 세 곳의 MIT 고지를 모두 보존하며,
`tk-explain`은 기존 시각 설명 원본 고지도 함께 포함합니다. 동기화와 설치 후 파일 일치는 릴리즈 검증 대상입니다.
기존 재작성 평가와 경계 검증은 삭제하지 않고 통합 이관합니다. 설명 평가는 비유나 분량 대신 선행 개념,
실제 동작, 그림과 글의 일치, 한국어 설명과 간결한 라벨의 공존을 확인하도록 변경합니다.

원본 자체 결과의 재현이나 전체 모델·호스트에서의 동등성은 여전히 `unverified`입니다.


## tk-rewrite: 강도·밀도 판단의 선택적 증류 (#366)

`epoko77-ai/im-not-ai`의 고정 커밋 `9747f036cdc28a1a8aea4dc71fef1f7846eb96f7`에서
`skills/humanize-korean/references/ai-tell-taxonomy.md`의 심각도 기준과 A-2/A-10,
`empirical-validation.md`의 기각·모델/과업 편향·한계, `design-notes.md`의 설계 근거와 테스트 시나리오,
`tests/test_content_anchor_contract.py`, `LICENSE`를 확인했습니다.

- `keep`: 자연스러운 단발 표현과 의미·조건·가능성을 보존합니다.
- `adapt`: 강한 부자연스러움, 반복·밀집, 다른 패턴과의 중첩을 구별하는 판단만 공통 정제 기준에 반영합니다.
  실증이 기존 통념을 약화하면 적용 범위를 좁힙니다. TigerKit의 의미·표기 절대 규칙은 이 판단보다 우선합니다.
- `omit`: 전체 분류 체계, `S1/S2/S3` 점수, 고정 횟수 임계, AI 작성 판정, 별도 런타임·다중 호출·장부는 가져오지 않습니다.
  원본 실증의 수치와 모델·장르 전반의 재현성은 자체 재검증하지 않았으므로 `unverified`입니다.

기존 `clear-writing.md`와 `tk-rewrite` 평가를 감사했습니다. 엠대시와 절 기호은 기존 선호 문구를
단발도 교정하는 절대 규칙으로 강화했습니다. 의미 보존(사실·수치·부정·조건·대안·결정권자·상태·불확실성),
정확한 리터럴과 필수 출처 보존은 기존 계약을 유지합니다. 한국어 본문의 필수 문장 성분·조사·종결어미도
기존 사용자 의도에 따라 유지하며, 제목·표·그림 라벨과 코드의 기존 예외를 보존합니다.
접속사, 피동, 가능형, 한자어, 괄호, 비유, 강조는 자연스러운 용례가 있어 추가 금칙어로 승격하지 않습니다.

정본을 소비하는 `tk-explain`에도 동일 참조를 동기화합니다. 원본은 MIT이며 두 설치 패키지의
`LICENSE.txt`에 `Copyright (c) 2026 epoko77-ai`와 원본 허가·면책 문구를 보존합니다.

## tk-learn: 기계적 검증 우선 판단 (#368)

`mattpocock/skills`의 최신 고정 커밋 `959a8e9f1edc3adbe2f7e3054bb6fbefa6696260`에서
`skills/in-progress/retro/SKILL.md`, `LICENSE`와 병합된 PR #1083의 설계 근거를 확인했습니다.

- `keep`: 반복 가능한 객관적 조건과 맥락 판단을 구분하고 기존 검사 명령과 담당 도구를 먼저 확인합니다.
- `adapt`: 기존 승격 관문에서 적합한 저장소 검사 도구의 최소 확장을 우선 제안합니다.
  스킬 승격 중단은 저장소 수정 권한을 부여하지 않으며 비용과 오탐에 따라 판단 경로를 유지합니다.
- `omit`: 자동 검사 부재 자체의 결함 판정, 무조건적인 검사 도입, 전체 회고 절차와 전역 규칙 작성은 가져오지 않습니다.

원본 PR은 자동 행동 평가가 없다고 명시합니다. 원본 행동 재현성은 `unverified`이며 TigerKit의
기계적 조건, 기존 도구, 맥락 판단, 취약한 검사, 사건 부재 경계는 별도 행동 평가로 검증합니다.
원본 MIT 고지는 `skills/tk-learn/LICENSE.txt`에 포함합니다.

## tk-rewrite: 관계와 문체 결함의 역주입 방지 (#369)

`evergreentree97/K-Humanizer`의 최신 고정 커밋 `324435d561ba48d53de6b7d3fb3dd72cf77030dc`에서
`skills/k-humanizer/SKILL.md`의 문단 연결·자체 검수, `references/evaluation.md`,
`evals/fixtures/golden_set.v0.jsonl`의 인과 미확인 사례와 `LICENSE`를 확인했습니다.
`epoko77-ai/im-not-ai`는 기존 고정 커밋 `9747f036cdc28a1a8aea4dc71fef1f7846eb96f7`이 최신입니다.
`skills/humanize-korean/references/ai-tell-taxonomy.md`의 `C-11`·`D` 역주입 근거와
`tests/test_strip_injected_commas.py`의 신규 표현·원문 보존 대조군을 확인했습니다.

- `keep`: 원문에 명시된 관계, 정상적인 연결어, 의미·표기 절대 규칙과 문맥에 따른 강도·밀도 판단을 유지합니다.
- `adapt`: 없는 관계를 새로 만들거나 다른 문체 결함을 추가하지 않는 검수를 공통 정제 기준과 행동 평가에 반영합니다.
- `omit`: 원본 전체 분류, 쉼표 개수 제한, 접속사 금칙어, 변경 비율 예산, 별도 후처리와 AI 작성 판정은 가져오지 않습니다.

원본 모델 평가의 수치와 재현성은 자체 재검증하지 않았으므로 `unverified`입니다.
`K-Humanizer`의 MIT 고지는 `tk-rewrite`와 공통 참조를 소비하는 `tk-explain`의 `LICENSE.txt`에
추가하며, 기존 `im-not-ai` MIT 고지는 보존합니다.

## `SDD`: 사용자 상호작용의 `root` 소유권 (#370)

`obra/superpowers`의 최신 고정 커밋 `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`에서
`SDD` 본문과 `implementer-prompt.md`, `2026-07-30-codex-efficiency-fixes-design.md`,
`tests/claude-code/test-subagent-driven-development.sh` 및 `integration` 테스트를 먼저 확인했습니다.
기존 `controller/leaf` 경계는 유지하며, 이 문서들에 없는 사용자 상호작용 소유권만 보완합니다.

이어서 `openai/codex`의 병합된 [PR #46066](https://github.com/openai/codex/pull/46066),
고정 커밋 `40584fad87aa2cd63e03db4784ccfd5b50a59bed`에서
`codex-rs/codex-mcp/src/elicitation.rs`와 관련 `elicitation/connection-manager` 테스트,
`codex-rs/core/tests/suite/mcp_subagent_elicitation.rs`, 인증 테스트와 `handoff` `snapshot`을 확인했습니다.
확인 당시 `elicitation.rs`와 `core/src/mcp_tool_call.rs`의 최신 변경은 이 `PR`이며,
`PR` `timeline`과 해당 `PR` 번호 검색에서는 후속 수정이 확인되지 않았습니다.

- `keep`: 기존 `controller/leaf` 역할, 승인 범위, 자동 `permission` 처리와 제한된 구현 판단을 유지합니다.
- `adapt`: 실제 사용자 입력만 `root`에서 처리하도록 하고 기존 `child` `return`에 `blocker`, 비밀이 없는 근거,
  `mutation` 상태와 재개 조건을 포함합니다. 빈 `form`의 인증 요청도 같은 경계를 적용하며,
  해결 확인 뒤 기존 `Unit`과 복구 식별자를 유지하여 남은 작업을 재개합니다.
- `omit`: `Codex`의 런타임·이벤트·연결 관리 구현, 새 스킬·장부·상태 체계는 가져오지 않습니다.
  코드를 복사하지 않고 행동 경계만 `TigerKit`의 `shared` `SDD` 계약과 평가에 적용합니다.

`Upstream` 테스트를 직접 실행하거나 외부 원시 평가 결과를 재현하지 않았으므로 해당 성과는 `unverified`입니다.
