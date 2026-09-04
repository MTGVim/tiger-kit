# Domain Context

Use this reference for semantic repository work before the task has already recognized a domain term.

Before interpreting repository behavior, requirements, ownership, impact, or domain meaning, or writing implementation, review, or publication prose that depends on them, check for repository-owned context and load only the relevant context when present. Purely mechanical Git, ref, or formatting work does not need it.

1. If root `CONTEXT-MAP.md` exists, read only the mapped context relevant to the task.
2. Otherwise read root `CONTEXT.md` only when it exists.
3. Respect an established repository glossary convention instead of creating a duplicate artifact.
4. Preserve canonical spelling, language, acronyms, and casing. Never substitute an `_Avoid_` term.
5. Keep verified rendered UI literals separate: quoted UI text follows runtime/render-path evidence; domain prose follows the glossary.
6. If fresher code or runtime evidence conflicts with the glossary, surface the conflict instead of silently choosing.
7. If no glossary exists, continue quietly without setup prompts or automatic creation.

Do not read unrelated child contexts or copy glossary content into task artifacts unless the task needs that term.
