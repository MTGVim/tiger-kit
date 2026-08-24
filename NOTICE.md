# 고지

TigerKit에는 `mattpocock/skills`에서 파생한 동작이 포함되어 있습니다(원본 스냅샷은
커밋 `391a2701dd948f94f56a39f7533f8eea9a859c87`에서 확인됨).

현재 적용된 스킬:

- `grill-me`
- `to-spec`
- `to-tickets`
- `implement`

제거된 적용 스킬에서 병합한 동작:

- `grilling` → `grill-me`
- `tdd` → `implement`
- `diagnosing-bugs` → `implement` 버그 조사 및 계약 계획
- `code-review` → `implement` 내장 검토

과거에 제거된 적용 작업 흐름:

- `grill-with-docs`
- `domain-modeling`

현재 적용 스킬의 관계 메타데이터: `relationship: adapted`. 해당 스킬이 계속
배포되는 경우 TigerKit은 상위 원본 스킬 이름에 `tk-` 접두사를 유지하고, 동작은 현재
TigerKit 사양에 맞게 다시 작성합니다.

`tk-prep`, `tk-pr-respond`, shared testing/SDD와 `tk-audit`의 조건부 engineering 규율은
`mattpocock/skills` 스냅샷 `5b15a47f2d7150f545fbcacbfe381787fc0230dc`에서 다음 원천을 검토해
TigerKit의 기존 owner와 private reference에 재서술했습니다.

- `skills/engineering/diagnosing-bugs/SKILL.md`
- `skills/engineering/tdd/SKILL.md`
- `skills/engineering/to-tickets/SKILL.md`
- `skills/engineering/codebase-design/SKILL.md`
- `skills/engineering/codebase-design/DEEPENING.md`
- `skills/engineering/codebase-design/DESIGN-IT-TWICE.md`
- `skills/engineering/improve-codebase-architecture/SKILL.md`
- `skills/engineering/domain-modeling/SKILL.md`

적용 범위는 hard/flaky/perf bug의 red-capable feedback loop, one-behavior vertical-first testing,
`expand → migrate batch(es) → contract`, hard-to-reverse ambiguity의 alternative comparison,
relevant repo-owned context 소비와 evidence-backed hotspot/locality/deletion-test 관점입니다. TigerKit은
상위 원본의 mandatory subagent fan-out, architecture vocabulary 강제, public workflow,
`CONTEXT.md`/ADR 생성·관리 lifecycle을 적용하지 않으며 기존 approval/Seed/secret/remote authority를
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
