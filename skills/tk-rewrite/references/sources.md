<a id="provenance"></a>
# 출처

upstream 증류의 유지보수 기록이며, 스킬 읽기 경로에는 포함되지 않습니다.

## clear-writing.md

- `docwriter-org/plain-writing-skill`, `f0d3630983ac7a82aa580f1c1509d72df739ee12`: 관련 배경, 구체적인 주어, 일관된 설명과 용어를 참고했습니다. 규칙 3과 15도 한국어의 실질 내용 없는 강조와 가운뎃점 요구에 영향을 주었습니다. 무관한 형식 금지를 가져오지 않고, 뒷받침되는 구체적 내용과 보호 리터럴에 맞게 조정합니다.
- `hjongc/humanizer-kr`, `a1a7069a32f669afe4b10e35e9522ff504a13263`: 독자·격식 적합성, 맥락적 편집, 절제된 주장과 내부 자연스러움 검토를 참고했습니다.
- `snflkd/fluent-korean`, `ce8683f0eba8cddb91de4dcd151425ff73e60498`: 한국어 문장 성분, 조사·어미, 정확한 어휘와 리터럴 표현 경계를 참고했습니다. 이는 논거와 예시를 갖춘 선택적 조정이며, upstream 전역 출력 스타일을 대체하지 않습니다.

- `evergreentree97/K-Humanizer`, `324435d561ba48d53de6b7d3fb3dd72cf77030dc`: 관계를 만들어 내지 않으면서 유용한 문단 연결을 보존합니다.
- `epoko77-ai/im-not-ai`, `9747f036cdc28a1a8aea4dc71fef1f7846eb96f7`: 맥락에 맞는 강도, 밀도에 따른 선택적 편집, 새로운 스타일 결함 방지와 경험적 근거가 가정한 패턴에 반할 때의 보수적 수정을 참고했습니다. 분류 체계, 저자 판정과 수치 임계값은 가져오지 않습니다.

- `conorbronsdon/avoid-ai-writing`, `c4783463cf019a8943364c1ef5f80e0a4c8bff94`: 후보에서 정당한 편집으로 이어지는 범위, 영향받지 않은 구절 보존과 유효한 무수정 결과를 참고했습니다. 탐지기, 분류 체계, 통과 예산이나 공개 감사 기록은 가져오지 않습니다.

- `conorbronsdon/avoid-ai-writing`, `5dd2e4ab72b9e0b7e125e5cb592af87033da4fda`(`9b8d030ce5c846af9520a4f6e5eb7d3b8d80ff43`과 비교): 기계적 보존과 의미 보존의 분리, 동등한 수치 표기와 불완전한 검증의 정직한 보고를 참고했습니다. 내부 두 차례 검토와 최종 결과 하나를 유지하고, 이 방어 조건만 조정합니다. upstream validator, detector, handoff envelope, 수정 예산과 공개 검증 보고서는 제외합니다.

스타일 예시의 사실 경계는 `addyosmani/clarity`,
`e27ceeff60368cf6966b4ea00a5b9b36418ee9a0`의 `SKILL.md`, `references/edit.md`와
`evals/cases.json`(`voice_sample_controls_style_not_facts`)도 참고합니다. 사실 보존은 유지하고, 표현에만 예시를 사용하도록 조정하며, 공동 집필, 탐지기와 공개 리뷰 보고서는 제외합니다.
프로젝트 친숙도는 기존 독자·맥락 계약을 독립적으로 확장한 것이며, 검증된 upstream 프로젝트 친숙도 규칙이라는 주장이 아닙니다.

원본 MIT 고지는 호출 패키지의 `LICENSE.txt`에 있습니다.

최종 한국어 교정 검토는 사용자의 2026-10-19 잘못된 활용 피드백에서 독립적으로 작성한 유지보수 확장입니다. 맥락적 수정과 보호 리터럴은 유지하고, 새로 발생한 오류를 잡기 위해 최종 재독을 적용하며, 단어 금지 목록과 자동 치환은 제외합니다. 저장소의 쌍대 eval은 `검증을 거칠습니다`를 유효한 형용사 `표면이 거칠습니다` 및 미래 표현 `거칠 예정입니다`와 구별합니다.

평가 강도와 확실성의 구분은 `dotoricode/korean-humanizer`, `4fc566b7d7ded76887f7a85c0886e44796e5e38c`(`references/ko-ai-signals.md`와 기본 스킬 QA)를 참고합니다. 양보 의미 보존은 `conorbronsdon/avoid-ai-writing`, `bdeb726580634868b254972d8eab1a9340d9db16`(`FALSE_CONCESSION`, PR #359와 fixture)를 참고합니다. 의미 보존과 과도하게 교정해서는 안 되는 사례를 조정하여 적용하고, detector regex, 분류 체계, 출력 템플릿과 런타임 도구는 제외합니다.

주장과 근거의 연결은 `AIScientists-Dev/academic-humanizer`,
`94b88b23703bed7df507acae7d6d5876209a0cdf`도 참고합니다. 근거 추가, 학술 분류 체계와 학술지·학회 규칙은 제외합니다.

의미 있는 양태 표현은 `epoko77-ai/im-not-ai`,
`92b2936956d65d62ff4b19b75cccad8e3429bf43`도 참고합니다. A-10/G-2와 수정 이력은 반복되는 경우에도 주장 강도를 보존하는 근거가 됩니다. 장르 전반에 의미 동등성을 적용하고, 특정 도메인만의 예외, 고정 반복 임계값, 유보 표현 사전, 표지 개수와 런타임 복원은 제외합니다.

재작성 전용 범위는 `dotoricode/korean-humanizer`, `93580567d4c965024e5b9eb1fb96ace3e7b45907`(`SKILL.md`, PR #6와 패키지 스킬 QA)를 참고합니다. 명시적으로 요청한 조언을 보존하면서 편집 전용 경계를 조정하여 적용하고, 고정 출력 절과 배포·런타임 도구는 제외합니다.

<a id="literal-versus-rhetorical-expression-regression-2026-10-07"></a>
## 리터럴 표현과 수사적 표현의 회귀(2026-10-07)

`conorbronsdon/avoid-ai-writing@1f187c049c1cac4d70fa555b4e3c0a413e25f2ee`를
현재 `main@0469c977d65a2c264c198bfb59eb4c699cb4584c`과 대조하여 검증했습니다.
commit 논거, `references/patterns.md`, `detector/patterns.js`와
`detector/patterns.test.js`의 true-positive/false-positive fixture를 확인했습니다. 테스트는 읽었지만 다시 실행하지 않았습니다. `keep`: 기존 맥락적 편집과 유효한 무수정 결과를 유지합니다. `adapt`: 쌍을 이루는 리터럴·수사적 회귀 사례를 저장소 eval에만 적용합니다. `omit`: detector regex, 단어 목록, 심각도·밀도 분류 체계와 런타임을 제외합니다. `../../tk-writing/references/clear-writing.md`는 변경하지 않습니다.

- `toss/frontend-fundamentals`, `161d3d6a0d6d372eacd75036de567511643f6265`, `fundamentals/code-quality/code/examples/magic-number-readability.md`: 구체적 예시, 누락된 독자 맥락과 그에 따른 개선을 유지합니다. 추상적 구분 전에 행위자·행동·결과를 배치하도록 그 순서를 조정합니다. 고정 절, 이모지와 사이트 런타임은 제외합니다.
- `reactjs/ko.react.dev`, `89f79e9e971e9ad424ea5ebabdf8d5fa66c87375`, `src/content/learn/state-as-a-snapshot.md`와 `wiki/best-practices-for-translation.md`: 예상·실제 동작의 순차 설명과 자연스러운 한국어를 유지합니다. 산문·그림 전반에서 행위자를 일관되게 유지하고 바뀐 조건을 드러내도록 조정합니다. 일괄 격식·문장부호 교체와 교육 런타임은 제외합니다.
- `dotoricode/korean-humanizer`, `90a651b647d209c163ff8f4b979667d1d2ea7244`, `SKILL.md`(의미 보존과 맥락적 문장 재구성): 문장 수준 재구성, 명사 연쇄 수정과 조건·가능성을 유지합니다. 기존 의미 검토와 인과 설명에 맞게 조정하고, 해당 출력 템플릿, 단어 치환과 전체 워크플로는 제외합니다. 이 revision들은 2026-10-25에 upstream HEAD로 재확인했습니다. upstream 모델 eval 효과와 조건이 일치하는 새로운 모델의 개선은 여전히 검증되지 않았습니다. 출처 확인은 실행 근거가 아닙니다.
