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

## tk-roadmap 증류 출처

`phuryn/pm-skills`의 `outcome-roadmap`, `opportunity-solution-tree`, `prioritize-features`를
커밋 `8607e3b077817f89bf4a9b623246219734ac3be0`에서 확인하여 성과 중심 기획과 대안 비교를 증류했습니다.
`mattpocock/skills`의 `wayfinder`는 커밋 `c55ee46073ed923f86ce59a5eb3b6d895095d1b7`에서 확인하여
미정 사항과 제외 범위를 구분하는 원칙만 보완했습니다. 관계는 `adapted`입니다.
세부 `keep | adapt | omit` 판단은 [출처 기록](skills/tk-roadmap/references/sources.md)에 있으며,
원본 MIT 저작권·라이선스 전문은 설치 패키지의 [고지 파일](skills/tk-roadmap/UPSTREAM-LICENSES.txt)에 포함합니다.

## tk-rewrite: 편집 정당성과 요청 범위 (#372)

`conorbronsdon/avoid-ai-writing`의 최신 고정 커밋 `c4783463cf019a8943364c1ef5f80e0a4c8bff94`에서
`SKILL.md`의 `Editing contract`와 `Output format`, `evals/rewrite/output-contract-scenarios.md`의
`Clean no-op` 사례, `PROOF.md`의 검증 한계와 `LICENSE`를 확인했습니다.

- `keep`: 의미·관계·조건·역할·불확실성과 보호된 리터럴, 기존 표기 절대 규칙을 유지합니다.
- `adapt`: 패턴 후보를 문맥상 문제로 확인한 뒤 요청 범위 안에서만 편집하는 계약을 표현 정제에 적용합니다.
  수정할 이유가 없는 부분은 유지하며, 근거가 전혀 없으면 원문을 반환합니다. 구조 변경은 독자 이해라는 목적에 따라 허용합니다.
- `omit`: 전체 분류 체계, 탐지기, 런타임, 반복 횟수 제한, 공개 감사 기록과 AI 작성 판정은 가져오지 않습니다.

원본의 평가 수치와 모델별 재현성은 자체 재검증하지 않았으므로 `unverified`입니다.
원본 MIT 고지를 `tk-rewrite`와 공유 참조를 소비하는 `tk-explain`, `tk-explain-diff`, `tk-study`의
`LICENSE.txt`에 보존합니다. TigerKit의 기존 두 단계 처리와 최종 본문 하나만 반환하는 형식은 유지합니다.

## `SDD`: 검증된 자식 상호작용 경로 (#373)

우선 `obra/superpowers`의 최신 고정 커밋 `5bf4e78011075bcfc0dc295f0724994cd123ee71`에서
`subagent-driven-development/SKILL.md`, `implementer-prompt.md`,
`2026-07-30-codex-efficiency-fixes-design.md`와 관련 설명·통합 테스트를 확인했습니다.
기존 부모의 위임·리뷰 소유권은 유지하고, 자식의 사용자 입력 경로는 다음 호스트 근거로 좁힙니다.

`openai/codex`의 병합된 [PR #46877](https://github.com/openai/codex/pull/46877),
고정 커밋 `c45ea25ffb72d5f7324489d824d0c677283aa0b4`에서 `elicitation.rs`, `mcp_tool_call.rs`,
`connection_manager_tests.rs`, `mcp_subagent_elicitation.rs`, `mcp_auth_elicitation.rs`의 구현과 테스트를
확인했습니다. 정확한 대기 요청으로 응답을 전달하는 경로, 취소된 요청 제거, 연결 재사용 시 승인 정책 갱신,
자식의 양식·인증 수락/거절과 재개, 기존 `request_user_input` 승인 경로의 `root-only` 제한을 대조했습니다.
확인 당시 두 구현 파일의 최신 내용은 병합 커밋과 같았고, 해당 PR 토론과 번호 검색,
`elicitation` 커밋 검색에서는 후속 변경을 확인하지 못했습니다. 원본 테스트를 직접 실행하지는 않았으므로
호스트별 실행 재현성은 `unverified`입니다.

- `keep`: 사용자 의도·범위·완료 기준과 새 권한은 부모가 소유하며, 기존 승인·발행·복구·비밀 처리 경계를 유지합니다.
- `adapt`: 현재 호스트 근거가 자식 지원, 정확한 요청·응답 연결, 동일 정책, 동일 자식 재개와 승인 범위를
  모두 입증할 때만 제한된 상호작용을 자식에서 처리합니다. 불명확하면 #370의 부모 전달 경로를 사용합니다.
- `omit`: 원본 런타임 코드, 제공자별 지원 목록, 새 상호작용 장부·상태 체계·스킬·승인 단계는 가져오지 않습니다.

원본 코드를 복사하지 않고 행동 경계만 기존 공유 참조와 평가에 독자적으로 반영합니다.

## 주장·근거 연결과 학습 과정 증류 (#374, #375)

`AIScientists-Dev/academic-humanizer`의 `94b88b23703bed7df507acae7d6d5876209a0cdf`에서
`SKILL.md`의 의미 보존과 주장·근거 절, `LICENSE`를 확인했습니다.

- `keep`: 기존 의미·조건·역할·불확실성·보호된 리터럴을 보존합니다.
- `adapt`: 수치·인용·그림·표 참조와 해당 주장의 연결 및 적용 범위를 재배열 후에도 보존합니다.
- `omit`: 근거 추가, 학술 분류, 투고 형식, 탐지 회피와 근거 없는 주장을 임의로 완화하는 절차는 가져오지 않습니다.

`lowwwbank/anything-to-course`의 `f11bbf21572a9864759929946c2c3da6857e1744`에서
능력 중심 커리큘럼과 선수 순서, 인출·전이 연습을 증류했습니다.
`MisterBrookT/vividoc`의 `32c7cf963e90c06b00143330f2ad5c6e2366b549`에서는
내용과 상호작용 설계, 내용 검증과 렌더링 검증의 분리를 참고했습니다.
읽은 구현·설계·평가와 `keep | adapt | omit` 판단은
[학습 과정 출처](skills/tk-study/references/distillation.md)에 기록했습니다.
원본의 실행 성능이나 학습 효과는 자체 재현하지 않았으므로 `unverified`입니다.
원본 코드·템플릿·런타임은 복사하지 않았으며, 참고한 MIT 고지를 해당 설치 패키지에 보존합니다.

## tk-rewrite: 의미가 있는 서법과 강도 보존 (#377)

`epoko77-ai/im-not-ai`의 고정 커밋 `92b2936956d65d62ff4b19b75cccad8e3429bf43`에서
`ai-tell-taxonomy.md`의 A-10/G-2, 수정 커밋 `0aedd76a1e6a1bc2b5f5f99e340988bf860fb685`의
설계 근거와 `tests/test_restore_modality.py`의 단정 전환 및 의미 보존 대조군을 확인했습니다.

- `keep`: 가능성과 의무를 사실로 바꾸지 않는 기존 의미 보존 원칙을 유지합니다.
- `adapt`: 완곡 표현끼리의 교체도 강도를 바꿀 수 있다는 교훈을 모든 장르에 적용합니다.
  강화와 약화, 의무와 권고의 상호 변환을 막고 동등한 기능 표현의 변경은 허용합니다.
- `omit`: 특정 분야만의 예외, 반복 횟수 기준, 완곡어 사전과 표지 개수 검사, 복원기 및 후보 장부는 가져오지 않습니다.

원본의 안과 블로그 55편 중 40편 복원 보고와 모델별 실증 수치는 자체 재현하지 않았으므로
`unverified`입니다. 기존 MIT 고지는 유지합니다. 세부 근거와 평가 범위는
[변경 기록](evals/changes/issue-377.md)에 남깁니다.

## 재작성의 순위와 동시성 보존 (#378)

`blader/humanizer`의 고정 커밋 `9862685f575c65a8247f90369951df1b3416e3d6`에서
`SKILL.md`의 초안 대조 절, `README.md`의 3.0.0 릴리즈 기록과
`c8e187205b574391165032c567c32407998cc8d1`의 #212 수정 이력을 확인했습니다.
[#212](https://github.com/blader/humanizer/issues/212)의 실패 보고와 유지보수자 답변도 확인했습니다.
현재 `scripts/validate-package.py`는 패키지 구조 검사이며, 이 의미 손실을 실행하는 회귀 테스트는
확인하지 못했습니다. 원본 모델 실행 재현성은 `unverified`입니다.

- `keep`: 의미 보존과 공허한 강조 교정, 기존 관계 역주입 방지 및 서법 보존 계약을 유지합니다.
- `adapt`: 실제 순위, 비교 범위, 동시성과 배타성을 양방향으로 대조합니다. 순위 이유가 없다는 사실과
  순위 주장 자체가 없다는 사실을 구분하며, 문구 대신 의미 관계를 보존합니다.
- `omit`: 원본 예시, 문구, 패턴 분류, 특정 강조어 보호 목록과 탐지 절차는 복제하지 않습니다.

구체 문장과 테스트 구조를 복사하지 않고 독자적인 의미 계약과 회귀 평가 6개를 추가했습니다.

## 위임 시 권한 비확장 (#379)

우선 `obra/superpowers`의 `5bf4e78011075bcfc0dc295f0724994cd123ee71`에서
SDD 본문과 구현자 프롬프트, `2026-06-09-sdd-task-scoped-review-dispatch-design.md`,
`tests/claude-code/test-subagent-driven-development.sh`를 확인했습니다.
부모가 위임과 리뷰를 소유하는 구조는 유지합니다. 해당 범위에서는 실효 권한 상속을 입증하는
계약이나 회귀 검증을 확인하지 못했으며, 설명 키워드 검사는 실제 접근 통제의 증거로 삼지 않습니다.

다음 PR의 현재 상태, 고정된 `diff`의 구현과 테스트를 대조했습니다.

| 출처 | 확인한 `revision` | 상태 및 근거 |
| --- | --- | --- |
| [`Continue` #13313](https://github.com/continuedev/continue/pull/13313) | `3a7b0702e0012b2194b158c8c43f7ce3977d1a48` | 미병합입니다. `allow-all` 치환 제거와 부모 정책 유지 및 승인 콜백 전달 테스트를 확인했습니다. |
| [`Claude Code` #96434](https://github.com/anthropics/claude-code/pull/96434) | `3bd80115aa290ba13aeea62a0d2eac61a26657df` | 미병합 `draft`입니다. `diff` 필터링, `deny/ask` 재적용, `shell` 우회 차단과 관련 테스트를 확인했습니다. |
| [Codex #47630](https://github.com/openai/codex/pull/47630) | `851d9e95f153c0f2fc4122adcaf68c5cd2df9464` | 병합되었습니다. 동작 대상 환경의 권한을 선택하고 환경 전환 및 없는 환경을 검사합니다. |
| [Codex #47830](https://github.com/openai/codex/pull/47830) | `61e23bc6a1e9e5fc8ed6aefb3575c9d1fd077c22` | 병합되었습니다. #47630의 동기 검토 경계를 비동기 점수와 캐시에도 연결하고 환경 및 거부 경로 불일치를 검사합니다. |
| [Codex #44617](https://github.com/openai/codex/pull/44617) | `663eb5fbdda690ca4471d92b3f9a29db43c5ba22` | 병합되었습니다. 추가 권한을 요구하는 미평가 동작의 캐시 승인 재사용을 차단하고 일반 동작 대조군을 검사합니다. |

- `keep`: #370/#373의 사용자 결정, 승인, 발행, 파괴적 작업 및 독립 리뷰 경계를 유지합니다.
- `adapt`: 같은 대상 환경에서 부모와 같거나 좁은 실효 권한만 위임합니다. 간접 읽기와 전달 자료도
  접근 제한을 따르며, 환경이나 권한이 바뀌면 기존 승인을 확대 적용하지 않습니다.
- `omit`: 호스트 구현 코드, 제공자별 정책표, 권한 엔진, 새 승인 절차와 영속 장부는 가져오지 않습니다.

원본 테스트는 직접 실행하지 않았으므로 호스트별 재현성은 `unverified`입니다. 미병합 제안은
배포된 보장으로 취급하지 않습니다. #47830의 후속 결합은 확인했으나 그 밖의 전체 후속 이력은
검증하지 않았습니다. 실제 위임에서는 현재 호스트 근거가 필요합니다. 공통 리뷰 계약을 정본으로
사용하고 SDD가 이를 참조하며, 기존 동기화 검사와 회귀 평가 13개로 해당 경계를 보호합니다.

## 2026-09-28: `Seed` 결정 밀도와 윤문 회귀 보호

`obra/superpowers`의 `8ca22dba9a94f28898bbce59f2537ff4d87c747d`에서
`skills/writing-plans/SKILL.md`를 확인했습니다. 병합된 PR #2333
(`71069323964d12f2dca6a1c52066165f4e43ade0`)의 실패 재현, 변형 비교와 `downstream`
실행 결과를 읽었습니다. 해당 평가를 여기서 재실행하지는 않았습니다.
결정과 인터페이스를 남기는 원칙 및 비례 검사를 기존 `Seed/SDD` 계약에 맞게 증류했습니다.
상위 `plan` 형식, 별도 `reviewer`, 고정 예산과 `runtime`은 가져오지 않았습니다.

`devswha/patina`의 `fb3bd7e9c671436c1d2bd7a78eeace4882a9ee8d`에서
`docs/research/2026-ko-overcorrection-flattening.md`, 한국어 구조 `fingerprint` 구현/단위 테스트와
`tests/unit/over-editing-guard.test.js`, 현재 배포된
`src/cli/overcorrection-advisory.js`를 확인했습니다. 원문 대비 불필요한 평탄화와
사용자가 요청한 문체 변경을 구분하는 원칙만 기존 `clear-writing`에 적용했습니다.
종결형 `classifier`, 임계값, `fixture`와 실행 코드는 복제하지 않았습니다. TigerKit 평가는
이슈의 사례와 독립 입력으로 작성했으며 `upstream`의 측정 결과를 TigerKit 성능으로 주장하지 않습니다.

`Lum1104/video-to-skill`의 `5e9f97e89855a8a0ea998ba85e179fbc1765d4b7`에서
제품 감사 및 `docs/generated-skill-v2.md`를 읽고 지정 출처 누락 방지를 기존 `sources.md`에
적용했습니다. 세부 `keep/adapt/omit` 판단은 `tk-study`의 `distillation` 참조에 기록했습니다.
새 코드, `fixture`, `semantic` `ledger`나 `manifest`를 복제하지 않았습니다.

## 문자열 식별 충돌과 재작성 문맥 (#383, #384, #385)

`obra/superpowers`의 최신 `main` 고정 커밋
`8ca22dba9a94f28898bbce59f2537ff4d87c747d`와 미병합
[PR #2414](https://github.com/obra/superpowers/pull/2414)의 최종 후보
`cb2479b488b5a6a35c8d8ac17174dbdae1bce43f`를 비교했습니다.
`writing-plans`의 검토 초점과 작업 리뷰어 지침, 세 커밋의 축약 이력,
PR 본문의 압박 평가 방법과 결과를 확인했습니다. 원시 실행 자료는 공개 본문에 없고
요청 시 제공된다고 되어 있어 재현성과 모델별 성능 수치는 `unverified`입니다.

- `keep`: 기존 행동 중심 테스트, 회귀 검증과 리뷰의 위험 검토 절차를 유지합니다.
- `adapt`: 문자열에서 식별과 소유권을 판정할 때 서로 다른 유효 엔티티를 직접 구성해
  오판을 추적하도록 테스트 참조와 리뷰 참조에 반영했습니다. 접두사 판정은 전체 문자열이
  동일하지 않아도 소유권을 혼동할 수 있으므로 실제 판정식을 검증합니다.
- `omit`: 새 식별 체계, 별도 리뷰 단계, 원본 계획 서식과 모델별 분기를 가져오지 않습니다.

`blader/humanizer`의 최신 고정 커밋
`225a6f39ac85f76ee48dbad772ea4abe4ed6c9d8`에서 `SKILL.md`의 26번 패턴,
`88ee4b5`의 도입 및 `d4b8127`의 재구성 이력과 예시를 확인했습니다.
별도의 실행 가능한 답장 회귀 평가는 발견하지 못했습니다.

- `keep`: 독립 문서의 자체 맥락 복원과 사실 및 불확실성 보존을 유지합니다.
- `adapt`: 명시적인 답장에서는 연결된 스레드의 독자가 이미 아는 배경만 생략합니다.
  새 변경 범위, 예외, 검증 결과와 결정 이유는 보존합니다.
- `omit`: 원본 예시와 문구, 분류 체계, 고정 답장 길이와 별도 실행 절차는 복제하지 않습니다.

`conorbronsdon/avoid-ai-writing`의 최신 고정 커밋
`7cd166c32e91573734f6ed37f4aa4d9e23b18400`에서 `f400c8f`의 도입과 후속 변경,
`detector/patterns.js`의 반복 판정, `detector/patterns.test.js`의 떨어진 교정 표현 및
인접한 반복 사례를 확인했습니다.

- `keep`: 강도와 밀도를 구분하고 절대 규칙을 밀도로 완화하지 않는 기존 계약을 유지합니다.
- `adapt`: 독립적인 정상 표현의 횟수를 합산하지 않고 관련 문맥이나 실제 공통 패턴을
  판정합니다. 문서 전체의 반복 구조도 검토하며 강한 단일 문제는 그대로 수정합니다.
- `omit`: 탐지 코드, 원본 문장, 테스트 구조, 문장 수나 횟수의 고정 임계값은 복제하지 않습니다.

새 평가는 이슈의 요구와 독립 입력으로 작성했습니다. 기존 MIT 고지는 유지합니다.
상위 원본의 보고된 성공률을 TigerKit의 검증 결과로 취급하지 않습니다.

## 조건부 지시와 출력 중복 정리

`obra/superpowers`의 `8ca22dba9a94f28898bbce59f2537ff4d87c747d`에서
`writing-skills`의 설명문의 호출 조건, 토큰 효율과 조건부 참조 근거를 확인했습니다.
원본의 보고된 모델 평가 수치는 재현하지 않았고 TigerKit의 측정으로 사용하지 않습니다.

- `keep`: 행동·경계 비교, 설치 패키지 자급성, 승인·증거·복구 중단 경계을 유지합니다.
- `adapt`: 읽기 조건을 식별할 수 있는 파일 저장, UI 조사, 브라우저 결과 반환, SDD 상호작용·복구·전송 세부를 패키지 로컬 참조로 나눕니다. 설명문은 호출 조건에 집중하고 단순 답변·학습 결과의 중복 상태를 줄입니다.
- `omit`: 원본의 고정 길이 목표, 전용 스킬 프레임워크, 도구·모델 설정과 예제를 복제하지 않습니다.

기존 버전과 같은 입력을 쓰는 독립 정책 시뮬레이션과 설치·참조 검사를 사용합니다.
시뮬레이션은 실제 브라우저 실행이나 여러 호스트에서의 모델 성능 검증을 대신하지 않습니다.

## #386–#390 탐색과 질문 계약의 증류

`tk-discover`는 `mattpocock/skills`의 `d81f3a183412e71a5b1e84ca21bc1a35eea03a60`에서
목적, 구체적인 질문과 불확실성, 의존성과 점진적 갱신을 증류했습니다.
`EveryInc/compound-engineering-plugin`의 `7b867109526165def0cc2a31b7c348b7308ae2c8`에서
조사 근거와 계획 인계 경계를 비교했습니다. 상류 실행 체계나 코드를 복사하지 않았으며 원본 MIT
고지는 새 패키지의 `UPSTREAM-LICENSES.txt`에 보존했습니다. 판단은 패키지의 `references/sources.md`에 있습니다.

일반 질문은 같은 `Matt Pocock` 고정 버전의 `grilling`과 기존 `tk-grill`에서 현재 독립적으로 답할 수 있는
질문을 함께 묻는 방식과 표시 형식을 증류했습니다. 공통 정본은 `tk-grill/references/questions.md`이고
설치 패키지에는 동일한 사본을 포함합니다. 전체 인터뷰나 확인 관문을 다른 스킬에 이식하지 않았습니다.

`tk-study`의 실행 연습문제 검증은 `matlab/agent-skills-playground`의
`7b14a7756bf2765a31840699bc27c8d7240083ac`에서 정답 통과와 그럴듯한 오답 실패를 확인하는
방식만 증류했습니다. MATLAB 실행 환경, 코드나 사례는 복제하지 않았습니다.
재작성 평가의 신뢰성 검토는 `anthropics/skills`의 `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4`를
참고했으며 평가 담당자 문서만 보완했습니다. 상류 문구, 코드나 평가 구조는 복제하지 않았습니다.
`forjd/better-writing`의 `d77d4c074f8a1a51045a2f089d763fb5b78c1875`에서 인간 문장 대조와 결말
의미 변화 검토를 확인했으나 기존 검증과 중복되어 `corpus`, 사례, 규칙을 새로 가져오지 않았습니다.

## 질문 관문과 익명 초안 우선 변경

사용자가 제공한 재현 흐름과 명시적인 재사용 계약을 근거로 공용 질문 블록에 최소 형식을 넣고
`tk-prep`의 질문·승인 지점에 참조 읽기를 연결했습니다. `mattpocock/skills`의 기존 고정 버전
`d81f3a183412e71a5b1e84ca21bc1a35eea03a60`에서 현재 질문 범위와 표시 형식을 다시 확인했습니다.
`keep`: 사실 조사, 독립 질문 묶음과 기존 승인 유지. `adapt`: 설치 본문의 최소 형식과 마지막 질문
블록 및 별도 승인 `Q`. `omit`: 인터뷰 반복 실행과 자동 하위 에이전트 지시. 이번 누락 보강과
익명화·임시 초안 우선 계약은 사용자 요청에 따른 TigerKit 변경이며 상류의 검증된 개선이라고 주장하지 않습니다.

## #393 실행 식별 정보와 #394 탐색 근거

`ayghri/i-have-adhd`의 `e9fee1addbb11073131d4663fe673a4df38d3938` 구현·회귀 테스트 변경과
최신 `839872f9d1cd634fed642b4589ce7226199cc15f`의 `scripts/run_evals.py`를 비교했습니다.
누락 수치의 보존은 `keep`, 실제 모델·좁은 관측 설정 및 정확한 실행 집합 비교는 `adapt`,
상류 채점·모델 선택·실행 체계는 `omit`입니다. 코드는 복사하지 않고 기존 평가기를 확장했습니다.
두 모델 모두 미상인 비교는 상류보다 엄격하게 `Unverifiable`로 처리합니다.

`Data-System-School/agent-skills`의 `a117418ab3596c59d641cab4cb89bdbe560fb277`에서
`investigate-codebase` 본문, ORIENT/IMPACT 참조, `DuckDB`/`vLLM` 사례의 근거와 한계를 확인했습니다.
읽기 전용 경계는 `keep`, 버전에 연결된 최소 경로와 보존 계약은 `adapt`,
별도 원장·고정 개수·검토 판정·추가 보고서는 `omit`입니다. 상류가 보고한 실행 수치는 재현하지 않았으며
TigerKit 검증 결과로 사용하지 않습니다. 패키지에 원본 MIT 고지를 포함했습니다.

## #395 의미 보존, #396 평가 격리와 #397 PR 복구 설명

`conorbronsdon/avoid-ai-writing`의 `9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43` 사례와
현재 `5dd2e4ab72b9e0b7e125e5cb592af87033da4fda`의 `preservation-verifier` 계약을 비교했습니다.
기존 두 단계 재작성과 최종 본문은 `keep`, 기계 검사와 의미 비교의 분리, 동등한 숫자 표기 및
미완료 검증의 정직한 보고는 `adapt`, 탐지기, 검증 실행 체계, 인계 봉투와 공개 감사 보고는
`omit`입니다. 기존 소비 패키지의 MIT 고지를 유지하며 상류 모델의 성능은 재현하지 않았습니다.

`ayghri/i-have-adhd@839872f9d1cd634fed642b4589ce7226199cc15f`의 평가 실행 및 테스트,
`OpenAI` 공식 CLI, 설정과 전역 지침 문서 및
`openai/codex@799324821d36a822923cee7814d3b80f7ec3cf99`의 CLI 옵션, 실행 구현과
설정 로더 테스트를 확인했습니다. 인증 경로 재사용과 프로젝트 사본은 `keep`, 실제 버전 및 옵션
지원 관측과 격리 미입증 시 비교 차단은 `adapt`, 인증 복사, 모델 선택과 설정 전체 덤프는
`omit`입니다. `--ignore-user-config`는 사용자 설정 파일의 제외를 위한 옵션이며 전체 행동 격리를
입증하지 않습니다. 현재 기본 Codex 어댑터의 상대 비교는 `Unverifiable`입니다. 실제 CLI 실행은
당시 환경에 바이너리가 없어 미검증이었으며 제어된 회귀 테스트를 실제 모델 실행으로 보고하지 않습니다.

`2026-10-02`에는 `edonadei/caliper@c2f222b5161afdb3bc986572236cfe0b34ab6881`의
`caliper/harness/codex.py`, 격리 작업 디렉터리 및 계정 연결 제외 ADR, 관련 테스트를 비교했습니다.
시도별 `fresh HOME`과 작업 디렉터리와 계정 앱·플러그인 제외 원칙은 검토 대상으로 `keep`, 최소 인증과
설정 재구성 및 모델에 실제로 활성화된 기능 관측은 미입증 상태로 `adapt` 후보에 남겼으며, 사용자 설정 전체 복제와
런타임 의존성 도입은 `omit`입니다. 실제 `codex-cli 0.159.2`로 실행한 `fresh HOME` 개념 검증은 45초 동안
모델 응답을 얻지 못했습니다. 별도의 네이티브 앱 서버에서 후보와 제거 환경의 스킬 목록을 확인했으며,
대상 스킬 하나만 목록에서 달랐고 공통 내장 스킬 5개, 앱·플러그인·훅 비활성 설정과 빈 MCP 설정을
관측했습니다. 이 결과는 발견 가능한 목록과 설정에 한정되며 실제 모델 활성화를 증명하지 않습니다.
실행 소유 인증 사본과 임시 HOME을 정리했으며 정본 어댑터와 `Unverifiable` 제한은 유지합니다. 파일 배치나 옵션 지원만으로 `true ablation`이 검증되었다고 주장하지 않습니다.

글쓰기에서는 `dotoricode/korean-humanizer@4fc566b7d7ded76887f7a85c0886e44796e5e38c`의
의미 보존 지침과 `native-skill` QA 및 `conorbronsdon/avoid-ai-writing@bdeb726580634868b254972d8eab1a9340d9db16`의
`FALSE_CONCESSION` 수정과 회귀 `fixture`를 확인했습니다. 기존 의미 보존과 과장 금지는 `keep`, 평가 강도와
확신 강도의 분리 및 정상 양보 보존은 `adapt`, `detector`와 정규식·분류 체계·출력 양식 이식은 `omit`입니다.
공유 `clear-writing` 소비 패키지에도 MIT 고지와 동일한 계약을 반영했습니다.

PR 재실행에서는 `EveryInc/compound-engineering-plugin@7fe624d36a5a12253165ebf6400acf20624ae7c5`의
`ce-resolve-pr-feedback/references/resume.md`, `caller-publication` 계획과 `pending/reply` 테스트를 확인했습니다.
최신 원격 상태와 피드백별 제출된 답글 근거는 `keep`, 기존 수정 커밋의 `ancestry` 및 답글과 스레드 해결을
각각 확인하는 복구는 `adapt`, 별도 JSON `handoff`와 장부, `checkpoint helper` 및 `return-to-caller` 모드는 `omit`입니다.

`mattpocock/skills@d81f3a183412e71a5b1e84ca21bc1a35eea03a60`의
`skills/engineering/pr/SKILL.md`와 MIT 고지를 확인했습니다. 저장소 템플릿, 검증 및 발행 권한은
`keep`, 구체적인 복구 가능성과 영향 범위 설명은 `adapt`, 필수 `Merge Danger` 템플릿과 장식적인
라벨은 `omit`입니다. 기존 템플릿에 내용을 반영하고 템플릿이 없을 때에만 유용한 설명을 추가합니다.
원본 MIT 고지는 설치 패키지의 `skills/tk-pr-open/LICENSE.txt`에 포함했습니다.

## tk-rewrite: 교정 요청의 범위 보존 (#417)

`dotoricode/korean-humanizer@93580567d4c965024e5b9eb1fb96ace3e7b45907`의 `SKILL.md`,
[PR #6](https://github.com/dotoricode/korean-humanizer/pull/6) 변경과 공개 QA 및
`eval/model-runs/package-skill-2026-10-02.json`을 확인했습니다.
원문과 요청 범위 보존은 `keep`, 교정만 요청받았을 때 수신자나 전달 상황, 운영 조언과
예상 반응을 추가하지 않으며 명시적으로 요청한 조언은 별도로 허용하는 경계는 `adapt`,
고정 출력 섹션, 카탈로그, ZIP 배포 및 모델 실행 체계는 `omit`입니다.
공개 실행 기록은 상류가 관찰한 작은 표본이며 TigerKit의 성능 근거로 사용하지 않습니다.
원본 MIT 고지는 기존 공유 참조 소비 패키지의 `LICENSE.txt`에 유지합니다.

## PR 응답의 임시 인덱스 격리

2026-10-01 기준 Git 공식 문서와 `git/git` `v2.56.0`의
[`git-hash-object.adoc`](https://github.com/git/git/blob/v2.56.0/Documentation/git-hash-object.adoc)
및 [`commit-tree.c`](https://github.com/git/git/blob/v2.56.0/builtin/commit-tree.c)를 확인했습니다.
태그 객체는 `2478544319491bbd2a42cc57a83e3d2f4730a280`이며, 확인한 파일 객체는 각각
`ef4719ae41c700f5dde933a69ae6c8cf8c5fd3bf`, `30535db131eaa6a3309e6e4383d17dbd8ce4fb57`입니다.
[`GIT_INDEX_FILE`](https://git-scm.com/docs/git),
[`read-tree`](https://git-scm.com/docs/git-read-tree),
[`update-index`](https://git-scm.com/docs/git-update-index),
[`write-tree`](https://git-scm.com/docs/git-write-tree),
[`commit-tree`](https://git-scm.com/docs/git-commit-tree),
[`push`](https://git-scm.com/docs/git-push)의 계약을 참조했습니다. 코드나 도우미는 복사하지 않았습니다.

`keep`: 임시 인덱스에 승인된 `tree`를 채우고 `blob`/`tree`/단일 부모 `commit`을 만드는 Git `plumbing` 순서를 유지합니다.
`adapt`: 일반 비실행 텍스트에만 적용하고, 부모 상태 보존, 정확한 경로의 포매터, `hook`·서명 의무,
독립 범위 검토와 현재 `head` CI를 요구합니다. `omit`: 별도 도우미, 동작 변경·로컬 테스트·`rebase` 경로 확장,
`worktree` 소실 원인에 대한 추정을 제외합니다. 소실 사례와 기존 성공 횟수는 사용자 보고이며 이 작업에서
회수 주체를 검증하지 않았습니다. 검증 시나리오는 `evals/skills/tk-pr-respond/evals.json`과
`evals/skills/tk-pr-sweep/evals.json`에 추가했습니다.

## #398 지속 연구와 근거 검증 증류

`tk-discover`의 공개 담당자는 `tk-autoresearch`로 승격했습니다. 과거 `tk-discover`의 출처 이력은 삭제하지 않고 새 패키지 `references/sources.md`에 고정 커밋 기반 계보로 이관했습니다.

`tk-autoresearch`는 다음 원본을 2026-10-01에 고정 커밋으로 비교했습니다.

- `Orchestra-Research/AI-Research-SKILLs` `773a52944ba4747a18bd4ae9ade53fff041adcbc`: 세션을 넘어 유지되는 연구 결과, 내부 실험 반복과 외부 종합 반복, 정체 시 연구 방향 전환을 적용했습니다. 필수 `/loop`, `never stop`, 논문 작성 수명 주기와 실행 체계는 제외했습니다.
- `uditgoenka/autoresearch` `050e30dc4ba0974b03f2873111b9901ec3211390`: 검증 뒤 유지 또는 폐기, 기계적으로 판정 가능한 경우의 명시적 완료 기준, 정체 감지를 연구의 반증 기준·정보 가치·수렴 경계로 적용했습니다. 배포·출시 실행 체계는 제외했습니다.
- `Companion-Inc/feynman` `4d62d07a7e8eb1fba1b02d6547e6425e456715eb`: 범위가 제한된 실험과 의미 있는 진행·실패·검증·차단 요인을 남기는 연구 일지 원칙을 적용했습니다. 원본 실행 체계와 일반 작업 공간 체계는 제외했습니다.
- `bryanshake/autoresearch` `0fa9a9336fc84a6b069111adb03ca21fabb5394b` (Apache-2.0): 소규모 사전 실험 뒤 확대 또는 중단, 부정 결과 보존, 독립 비판·정보를 가린 검토와 종료 판정 설계를 비교 자료로 사용했습니다. 조정 실행기, 실행 체계, 대기열 구현, 제공자 설정과 지시문·코드는 복제하지 않았습니다.

`tk-research`는 `rohankgeorge/the-researcher` `1184d246c290a4ff772ea669ac6b9f9914d3f7da`에서 1차 출처 추적, 출처 접근 가능성과 주장 충실도의 분리, 모순·검증 불가·철회 결과 보존을 증류했습니다. 원본의 지속 연구 기록과 심층 조사 플랫폼 분기 체계는 가져오지 않았습니다.

각 적용·비적용 판단, 검토한 파일, 검증 한계와 반영 위치는 각 패키지 `references/sources.md`가 정본입니다. 원본 라이선스는 해당 `UPSTREAM-LICENSES.txt`에 보존합니다. 원본 시연·평가의 성능을 TigerKit에서 재현했다고 주장하지 않습니다.

## #409-#411 자동연구 평가 무결성과 파생 근거

2026-10-02에 다음 최신 기본 브랜치의 고정 커밋과 라이선스를 확인했습니다.

- `RUC-NLPIR/Arbor` `7cdaf1fa6d779b3d5e340052357bf3fe55dfed93` (Apache-2.0): 평가 기준 보호, 탐색용 근거와 채택용 근거의 조건부 분리, 선택적인 파생 근거 링크와 상위 방향의 교훈 보존을 증류했습니다. 전체 트리 실행 체계와 병합 동작은 가져오지 않았습니다.
- `Gyubin/autoresearch` `1e2830d9f35853d7eee580b7333a3c91e6259c0d` (Apache-2.0): 예산상 보류와 실제 반증의 분리, 중요한 확률적 결과의 독립 재현 원칙을 증류했습니다. 고정 후보·반복 개수와 별도 실행 체계는 제외했습니다.
- `Muuuun/luxas` `9f77cefe7f47b05b1334ec8778e642deef13da82` (MIT): 객관적인 계약과 원래 근거를 중심으로 독립 검증 입력을 구성하는 원칙을 증류했습니다. 에이전트 구성과 코드·지시문은 복제하지 않았습니다.

`karpathy/autoresearch`는 해당 커밋에 라이선스 파일이 없고, `SakanaAI/AI-Scientist-v2`는 별도 조건이 있는 사용자 정의 라이선스이므로 증류 원본으로 편입하지 않았습니다. 비교 위치·적용·제외 판단과 검증 한계는 `skills/tk-autoresearch/references/sources.md`에 기록했습니다. 채택한 원본의 라이선스는 패키지 `UPSTREAM-LICENSES.txt`에 보존합니다.

## 병렬 리뷰의 공유 실행 자원

2026-10-01에 `obra/superpowers` 최신 `main`의 고정 커밋
`8ca22dba9a94f28898bbce59f2537ff4d87c747d`에서 `requesting-code-review/SKILL.md`,
`requesting-code-review/code-reviewer.md`, `verification-before-completion/SKILL.md`,
`subagent-driven-development/SKILL.md`와
`docs/superpowers/specs/2026-06-09-sdd-task-scoped-review-dispatch-design.md`를 확인했습니다.
이 설계 문서는 동일 코드의 테스트 중복 실행을 줄이고, 기존 근거가 답하지 못하는 구체적인 의문에만
집중 검사를 실행하는 원칙과 원본 평가 결과를 보고합니다. 원본 평가 실행 결과의 재현은 `unverified`입니다.

- `keep`: `context`가 분리된 독립 리뷰와 정확한 대상의 테스트 근거를 먼저 읽는 원칙을 유지합니다.
- `adapt`: `tk-review` 정본과 `tk-prep`·`tk-pr-respond` 생성 사본에서 모든 `leaf`에 테스트·빌드·실행 근거를
  전달하고 공유 실행은 `controller`가 직렬로 조율하도록 합니다. 대기 보고는 실제 프로세스 상태를 확인하고,
  멈춘 리뷰 소유 프로세스만 정리합니다. `CPU` 0%만으로 중단을 판정하지 않습니다.
- `omit`: 호스트별 잠금 도구, 실행 체계와 `Jest` 정지 원인에 대한 추정은 가져오지 않습니다.

19분 정지와 빌드 동시 실행 사례는 사용자 제공 근거이며 이 작업에서 실제 프로젝트의 `Jest` 증상을
재현하지 않았습니다. `tk-prep/references/testing.md`의 기존 근거 우선 원칙을 공유 리뷰 계약에 적용합니다.

## 런타임 검증 라우팅과 익명 초안 최소화

2026-10-02에 `obra/superpowers` 최신 `main`의 고정 커밋
`8ca22dba9a94f28898bbce59f2537ff4d87c747d`에서 `skills/writing-skills/SKILL.md`와
`skills/writing-skills/testing-skills-with-subagents.md`를 확인했습니다. 조건에 따른 분기,
누락된 산출물 계약과 실제 행동 비교 원칙을 검토했습니다. 원본 평가의 재실행은 `unverified`입니다.

- `keep`: 기존 브라우저 검증의 `baseline`·`after`·재개 계약과 비밀값 배제, 공개 업스트림·스킬 식별자 보존을 유지합니다.
- `adapt`: 실제 AC를 기준으로 기존 `tk-app-verify` 계약에 연결하고, 익명 초안은 재현·수정 판단에 필요한 사실만 남깁니다. 필요성 판단은 호출자 예시에도 적용하며 필수 버전·플랫폼 조건은 보존합니다. 수정 전후 독립 입력의 계획·초안을 비교합니다.
- `omit`: 원본 실행 체계와 `provider`별 조작 절차를 복제하지 않습니다. 익명화 최소화 규칙은 사용자 제공 사례와 TigerKit의 기존 초안 계약에서 도출했으며 외부 원본에 같은 규칙이 있다고 주장하지 않습니다.

실제 데스크톱 앱에서 발생한 사례는 사용자 제공 근거입니다. 이번 검증은 `verifier` 계획과 익명 초안 행동을 대상으로 하며 실제 앱의 캡처 실행을 재현했다고 주장하지 않습니다.

## 비활성 앱 실행과 소유 대상 초안

2026-10-02에 `trycua/cua` 최신 `main`의 고정 커밋
`8d4e7a08618611453794035f7ff6187f99f0c1e9`에서
`libs/cua-driver/rust/Skills/cua-driver/MACOS.md`,
`libs/cua-driver/rust/crates/platform-macos/src/tools/launch_app.rs`,
`libs/cua-driver/rust/crates/cua-driver-e2e/tests/installed_app_launch_macos_test.rs`를 확인했습니다.
비활성 실행 도구, 자체 활성화 억제 결과와 실행 후 포커스 확인을 비교했습니다.
`obra/superpowers@8ca22dba9a94f28898bbce59f2537ff4d87c747d`의 스킬 작성·독립 행동 비교 원칙도 재확인했습니다.

- `keep`: 제공자의 버전에 맞는 실행 계약과 실행 후 독립 포커스 확인, 기존 스킬의 소유권·정확한 적용 승인 경계를 유지합니다.
- `adapt`: `tk-app-verify`는 실행과 입력 능력을 분리하고 비활성 실행을 먼저 조사합니다. 원래 후보를 보존하는 격리 래퍼·고유 식별자·등록 조회·실행 소유 정리 절차는 사용자 제공 사례를 조건부 지식으로 적용합니다. `tk-learn`은 소유하지 않은 설치본을 초안으로 끝내며 저장소가 확인되면 기존 산출물 검사를 거쳐 저장소 내부 임시 초안을 사용합니다.
- `omit`: 제공자의 실행 구현과 운영 체계를 복제하지 않습니다. 특정 위치에서의 래퍼 등록 성공을 모든 버전·플랫폼의 보장으로 일반화하지 않으며, 사용자 계정의 기여·발행 선택지를 자동 제안하지 않습니다.

이번 검증은 독립 실행자의 계획·실제 초안 저장 행동과 저장소 검사에 한정합니다. 실제 `macOS` 앱 실행과 원본의 네이티브 테스트 재실행은 `unverified`입니다.

## #407 제한된 CLI 진단과 실행 자원 정리

앞서 기록한 `edonadei/caliper@c2f222b5161afdb3bc986572236cfe0b34ab6881`의 격리 원칙을
기존 어댑터와 분리된 `scripts/probe_codex_isolation.py` 진단에 적용했습니다. 실행별 HOME과
작업 폴더 및 계정 연결 도구 배제의 필요성은 `keep`, 최소 인증 발견과 모델에 전달되는 스킬 목록의
관측을 구분하는 제한된 진단은 `adapt`, 설정 전체 복제와 격리 성공의 포괄적 선언은 `omit`입니다.

진단 도구는 실제 CLI를 제한 시간 내에 호출하고 비밀 값이나 원시 출력 대신 상태만 반환합니다.
선택적 인증 파일은 비갱신 `login status`에만 참조하며 프롬프트 진단에는 전달하지 않습니다.
`codex-cli 0.159.2`에서 최소 인증 발견은 확인했지만 이 진단의 `debug prompt-input`은
시간 초과되어 두 평가군의 스킬 목록을 관측하지 못했습니다. 이는 앞서 기록한 앱 서버 목록 관측과
다른 검증 경로이며, 어느 결과도 실제 스킬 활성화나 작업 성공 및 플러그인, 앱, MCP 전체 격리를
입증하지 않습니다. #407은 사용자 판단에 따라 `not_planned`로 닫혔으며, 이 진단은 완료 조건 충족을
뜻하지 않습니다. 기본 어댑터의 `Unverifiable` 제한을 유지합니다.

POSIX에서는 실행 소유 프로세스 그룹을 종료해 시간 초과, 중단 및 정상 종료 뒤의 자식 프로세스를
정리합니다. 지원하지 않거나 정리가 불확실한 환경에서는 정리 결과를 성공으로 보고하지 않습니다.
관련 회귀 테스트는 종료 신호를 무시하는 자식 프로세스와 세 종료 경로를 검사합니다.

## tk-learn 초안의 설명 언어와 정확한 교체 문장

2026-10-02 사용자 제공 사례와 기존 초안 절·품질 참조를 비교했습니다.
`obra/superpowers@8ca22dba9a94f28898bbce59f2537ff4d87c747d`의
`skills/writing-skills/SKILL.md`와 `skills/writing-skills/testing-skills-with-subagents.md`에서
최소 교정과 수정 전후 독립 행동 비교 근거를 재확인했습니다.

- `keep`: 기존 사용자 언어 원칙과 정확한 교체 문장·식별자·코드, 외부 설치본의 초안 경계를 유지합니다.
- `adapt`: 초안을 작성하는 절에 설명 언어와 대상 언어를 구분하는 규칙을 두고 원문 유지 이유를 해당 부분 옆에 알립니다.
- `omit`: 새 언어 판별 도구나 실행 체계를 추가하지 않습니다. 이 언어 규칙은 사용자 사례와 TigerKit의 기존 계약에서 도출했으며 업스트림의 동일 규칙으로 주장하지 않습니다.

한국어 요청·영어 대상과 영어 요청·한국어 대상의 대화 전용 초안을 독립 실행자로 비교했습니다.
기존 결과도 설명 언어와 정확한 리터럴은 보존했지만 대상 언어 유지 안내가 없었습니다.
후보는 언어 유지 안내까지 제공했고 미실행 검증과 외부 설치본의 초안 경계를 유지했습니다.
사용자가 보고한 초안 전체의 영어 작성 실패와 원본 평가 재실행은 이번 비교에서 재현하지 않았습니다.

## 새 추상화의 이름 정렬과 지속 연구 프로젝트 운영

2026-10-02에 `obra/superpowers` 최신 `main`의 고정 커밋
`8ca22dba9a94f28898bbce59f2537ff4d87c747d`에서 SDD 절차와
`skills/subagent-driven-development/implementer-prompt.md`의 명확한 이름·기존 패턴·`self-review`
계약을 확인했습니다. `Andrew Moffat`의
[AI가 만든 변경의 인지 부담을 줄이는 방법](https://amoffat.github.io/blog/cognitive-load.html)를
읽고 사용자 이슈 #412와 비교했습니다. 글은 설계 참고이며 원문이나 프롬프트를 복제하지 않습니다.

- `keep`: 기존 `self-review`, 승인 범위, 외부 계약과 제품/도메인 결정의 질문 경계를 유지합니다.
- `adapt`: 의미 있는 새 추상화에 기존 저장소 어휘를 우선하며 실제 새 개념은 정확하고 평범한 이름으로 둡니다.
- `omit`: 모든 지역 변수 검사, 상시 이름 승인, 무조건적인 전체 문자열 치환와 별도 스킬은 도입하지 않습니다.

자동연구의 기존 `Orchestra` `773a529`, `uditgoenka` `050e30d`, `bryanshake` `0fa9a93` 고정 리비전은
최신 기본 브랜치와 같음을 확인하고 관련 연속성·중단·복구 설계를 다시 읽었습니다.
구체적인 출처와 `keep | adapt | omit` 판단은 `tk-autoresearch/references/sources.md`에 남겼습니다.
첨부한 사용자 운영 제안을 기존 상태 모델에 적용하여 대기만 남았을 때의 재생성, 후보 소진과
후보 없음 증명의 구분, 부분 인계 목록, 확인 가능한 재개 조건, 지시를 덧붙인 재개와
새 세션의 로컬 우선 진행을 보강합니다. 연구 식별자·상태 경로와 권한 경계는 유지합니다.

원본 런타임이나 실제 운영 로그 접근은 재현하지 않으며, 정책 시나리오의 독립 실행과 저장소의
결정론적 릴리즈 게이트를 구분해 검증합니다.

## #413~#416: 끌기, 문체 샘플, 상호작용 상태와 학습 미션

2026-10-05에 다음 원본의 구현과 설계 근거를 고정된 커밋에서 확인했습니다.

- `trycua/cua@61ec8ac1d80df191bccd7fc9e9275123a809b2f7`: `drag.rs`의 구현, 명세, 거절 테스트와 `MACOS.md` 및 포인터 문서를 확인했습니다. 독립 사후 조건과 승인 경계는 `keep`, `macOS` 창 대상 끌기의 전경 전용 분류는 `adapt`, 전체 화면 입력과 자동 권한 확대는 `omit`입니다. 공유 제공자 지식 정본과 데스크톱 검증 사본을 함께 갱신합니다. 기존 앱 실행 출처는 유지합니다.
- `addyosmani/clarity@e27ceeff60368cf6966b4ea00a5b9b36418ee9a0`: 본문, 편집 참조와 문체 샘플 평가를 확인했습니다. 사실 보존은 `keep`, 문체 예시에서 사실, 경험, 주장, 인용이 유입되지 않는 경계는 `adapt`, 공동 집필, 탐지기, 공개 감사 보고서는 `omit`입니다. 기술 지식과 프로젝트 친숙도 구분은 기존 독자 문맥 계약 및 명시된 개선 요구를 근거로 독립 작성했습니다.
- `nicobailon/visual-explainer@5846f5aef34a23c8fea389d2f23ce56224cbf840`: 본문, `references/diagrams.md`의 상호작용형 그림과 페이지 틀을 확인했습니다. 가벼운 상호작용과 정적 설명은 `keep`, 하나의 계산 상태, 필요한 제어값, 검증된 기본 상태, 단순화 표시는 `adapt`, 외부 자산, 실행 체계, 자동 열기는 `omit`입니다. 원본 코드와 틀을 복제하지 않았습니다.
- `mattpocock/skills@24fe0ef7737efae15c87225755e9f6f5965e4888`: `teach/SKILL.md`와 `MISSION-FORMAT.md`를 다시 확인했습니다. 실제 수행 능력 중심 목표는 `keep`, 새 코스의 미션 정렬 및 기존 주제 폴더의 기록은 `adapt`, 짧은 학습이나 명시적 인터뷰 생략 및 검증된 계속 학습의 강제 인터뷰와 루트 작업 공간 및 자동 열기는 `omit`입니다. 질문 개수나 별도 확인 승인을 추가하지 않았습니다.

`Yila-AI/awesome-research-skills@0609e85b6dbfdae8a48ba66c332d340265d7b3e5`의 문체 참조와
`scarletkc/agents@eb55005652d5708f369bde008cc48c71159f9e95`의 글쓰기 본문, 참조, 평가도 대조했습니다.
앞 자료와 중복된 사실 경계는 MIT 원본만으로 충분했고, 뒤 자료에서는 프로젝트 친숙도 양방향 계약의
직접 원본을 확인하지 못했습니다. 두 Apache-2.0 원본은 `omit`이며 문구, 코드, 평가를 반영하지 않았습니다.

선택한 MIT 원본의 저작권과 라이선스 전문을 해당 설치 패키지의 `LICENSE.txt`에 보존했습니다.
상류 네이티브 테스트, 학습 효과, 호스트 전반의 성공률은 재현하지 않았습니다.
기존 정책과 후보의 독립 재생은 대부분 양쪽 모두 성공했으며, 이를 실패율 개선 근거로 사용하지 않습니다.
