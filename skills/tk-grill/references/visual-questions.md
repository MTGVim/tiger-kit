# Visual question aid

Read only when spatial alternatives can change an unresolved user-owned choice. Keep the numbered plain-chat question, a short description of every option and the recommendation complete without opening a file. Add the complete absolute HTML link in that question; users can answer by number or paste the copied selections.

After Artifact Paths checks, create one external-resource-free HTML file in `.tigerkit/tmp/<calling-skill>/<run-id>/questions.html`. Inline this package's `assets/html-theme.css` and `assets/html-theme.js` unchanged,
using their `ht-*` components and tokens; add only question-specific wireframe styles.
Set `<html data-default-theme="system">`. Put the title in `.ht-topbar-title` and a
`.ht-theme-control[data-ht-theme-control]` fieldset inside `.ht-topbar`. Initially hide the fieldset;
the shared script reveals it. Give it labeled `system`, `light`, and `dark` radio choices using
`.ht-theme-buttons` and `.ht-theme-option`, each `input[name="ht-theme"]` immediately followed by
a nonempty `span`. Place the script after the markup. Verify all three choices and storage-refusal
behavior before delivery. Show comparable low-fidelity wireframes, option numbers, pros/cons and the recommended option. Offer single-option and side-by-side views when useful, with keyboard-accessible controls and no focus outlines on passive scroll targets. Match the same viewport/content across options; do not add decorative imagery or implementation code. Reuse this file for later visual rounds in the same run; do not generate files for nonvisual questions, a plan recap or a resolved choice.

Let the user pick an option in place on each option card, plus inline choices for any
nonvisual question in the same round. Keep a fixed answer bar that shows progress in words
(for example `2/5 selected · remaining Q3, Q4, Q5`) and a copy button that copies only the
picked answers in the round's reply format, with an optional note. Never fill unanswered
questions with recommendations or treat copying as approval; identify remaining questions.
Persist picks to `localStorage` under a run- and round-scoped key, wrapping every access in
try/catch; copy must work when storage is refused. If clipboard access fails, expose the
same text for manual copying. Do not watch a saved file from the session.

If writing or viewing the HTML is unavailable, finish the text round and disclose only the missing visual aid. A missing repository does not justify initializing Git or using an external temporary path. Preserve source/config/Seed and approval boundaries apart from the canonical minimal ignore setup. This aid is not a product prototype or approval to implement it.
