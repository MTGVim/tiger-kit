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

Use this reference-only skill when the caller needs one of the criteria below. Read only the
requested reference under its stated condition; do not preload the whole collection. Return
the relevant criteria and unresolved evidence to the calling workflow. This invocation does
not start that workflow or grant installation, file mutation, secret access, Git or publication
authority. The caller retains its approval gates, authority, evidence and completion duties.

If this skill or a requested resource is missing, stop the affected action and guide the user
to `tk-setup-skills`. Do not substitute remembered guidance or silently install dependencies.
Resolve linked sibling packages in the current host's installed skill collection, never from
a hardcoded home directory. Dependencies are declared in `dependencies.json`.

In moved references, `<package>`, "package-local" and "this package" mean the invoking
workflow's installed package unless an explicit resource link identifies another owner.
Following a resource link reads that resource only; it does not invoke the owner's workflow.

## Conditional references

- [chart design](references/chart-design.md): data needs a chart or chart representation must be chosen.
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
