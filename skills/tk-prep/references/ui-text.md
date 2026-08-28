# UI Text Evidence

Read this reference only when the task names or changes a user-visible label, title, tab, option, button, modal, or
instruction.

Record the exact rendered string in quotes, preserving language, case, punctuation, and spacing. Use the first applicable
evidence:

1. current runtime-rendered text for the target environment and locale;
2. a component prop, i18n entry, or option source connected to the render path;
3. a supplied screenshot or reference with provenance;
4. ticket or specification wording;
5. identifier, enum, route, domain term, or i18n key inference, which is not label evidence.

Dynamic or server text that source cannot determine remains unverified. If no visible label exists, record the entry path
ending in an exact visible title. A value such as `BOTTOM` is valid only when the current render path displays it as-is.
Preserve verified literals exactly. Conflicting downstream evidence returns to preparation instead of guessing.
