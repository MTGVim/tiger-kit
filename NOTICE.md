# Notices

TigerKit includes adapted behavior from `mattpocock/skills` (source snapshot inspected at commit `391a2701dd948f94f56a39f7533f8eea9a859c87`).

Current adapted skills:

- `grill-me`
- `to-spec`
- `to-tickets`
- `implement`

Behavior merged from removed adapted skills:

- `grilling` → `grill-me`
- `tdd` → `implement`
- `diagnosing-bugs` → `implement` investigation and planning bug contracts
- `code-review` → `implement` built-in review

Removed historical adapted workflows:

- `grill-with-docs`
- `domain-modeling`

Relationship metadata for current adapted skills: `relationship: adapted`. TigerKit preserves upstream skill names with a `tk-` prefix where the skill remains deployed and rewrites behavior to the current TigerKit specification.

`tk-merge-conflict` remains TigerKit-native (`origin: tigerkit`, `relationship: native`). No verified source metadata establishes it as an adaptation of `mattpocock/skills` `resolving-merge-conflicts`.

`tk-skill-diagnose` adapts empirical Agent Skill evaluation methodology from
`mizchi/skills`, source snapshot
`7a0d72866a0bb3e9ac3e2768c328b09ba2bc40c4`:

- `meta/empirical-prompt-tuning/SKILL.md`
- `meta/waxa-eval/`

TigerKit distilled Iteration 0 description/body consistency, frozen
median/control/holdout scenarios, fresh executors, two-sided phase traces,
structured `Issue / Cause / General Fix Rule` feedback, one-theme candidate
experiments, convergence, and run-local failure ledgers. The adaptation adds
TigerKit-specific failure planes, host/provenance gates, writer ownership,
local-only diagnostic output, resource/correctness precedence, and anonymized
upstream issue drafts. It does not copy upstream presentation prose or replace
Darwin-style broad optimization. Relationship metadata:
`relationship: adapted`.

`mattpocock/skills` upstream license:

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

`tk-improve` adapts `shadcn/improve` from source snapshot
`03369ee6d7cafbfcecc4346539b05b3dc0a603bb`:

- `skills/improve/SKILL.md`
- `skills/improve/references/plan-template.md`
- `skills/improve/references/audit-playbook.md`

TigerKit keeps the upstream senior-advisor/read-only boundary, evidence-first
audit categories, cheaper-executor handoff quality, and MIT attribution while
changing the owned artifact to `.tigerkit/improve.md` and routing candidates to
TigerKit's existing spec/ticket/drive owners. Relationship metadata:
`origin: shadcn/improve`, `relationship: adapted`.

`shadcn/improve` upstream license:

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
