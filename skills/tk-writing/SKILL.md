---
name: tk-writing
description: "[user/auto] 글쓰기·설명·HTML 문서 구성 및 표현 기준을 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

# Shared Writing and Presentation

Read only references whose conditions below hold; return criteria and gaps to the caller,
which retains scope, approvals and completion. References invoke no workflow and grant no
installation, mutation, secret, Git or publication authority.

Resolve owners in the current installed skill collection (`dependencies.json`), not memory,
another installation, hardcoded homes or a source-checkout fallback. A missing/mismatched
owner or resource blocks the affected action: guide to `tk-setup-skills`, never silently install.
Resource links here resolve from `tk-writing`; `<tk-writing>` in commands is its current installed
package path. It owns the shared HTML assets and assembly, code highlighting, export and Chrome
capture helpers, not a runtime workflow. Call only the selected helper after caller-owned approval
and path checks; keep inputs, outputs, scratch and cleanup outside the installed package.

## Conditional references

- [chart design](references/chart-design.md): data needs a chart or chart representation must be chosen.
- [chat delivery](references/delivery.md): returning user-facing results, artifact links or multi-attribute chat comparisons.
- [clear writing](references/clear-writing.md): authoring prose rather than preserving exact supplied text.
- [diataxis](references/diataxis.md): choosing tutorial, how-to, explanation or reference framing.
- [explanation techniques](references/explanation-techniques.md): planning a teaching explanation or its representations.
- [html assembly](references/html-assembly.md): the selected output uses the shared-reader HTML assembly path.
- [html components](references/html-components.md): a selected HTML interface needs a supported component.
- [html figures](references/html-figures.md): the selected HTML needs explanatory figures.
- [html output](references/html-output.md): an HTML artifact is the selected deliverable.
- [html reader](references/html-reader.md): assembling a shared-reader lesson or change document.
- [html render](references/html-render.md): building, packaging or checking selected HTML output.
- [interactive examples](references/interactive-examples.md): the user explicitly requests a live interactive example.
- [media preferences](references/media-preferences.md): a visual or media format/preference needs to be resolved.
- [reader formatting](references/reader-formatting.md): formatting authored prose for an explanation document.
- [renderer contract](references/renderer-contract.md): choosing a supported explanation renderer without changing existing learning materials.
- [scene figures](references/scene-figures.md): a physical or spatial relationship needs a scene figure.
- [visual grammar](references/visual-grammar.md): choosing the figure grammar for a relationship or explanation.
