# Lesson HTML presentation

Use the package-local `lesson` profile for new HTML lessons. Keep the goal and needed background
visible, place explanation and its worked example together, then offer outcome-appropriate
practice, optional hints, a separately revealed explanation and a way to retry. Do not require
a fixed number of steps, code, quizzes or a programming runtime. Honor actual prior knowledge,
explicit Markdown, existing learning-home identity and independent content-review rules.

Author a content fragment with top-level `<section id="..." data-ht-nav-unit>` learning units.
Use `.ht-lesson-workbench`, `.ht-lesson-instruction`, `.ht-lesson-example` and
`.ht-lesson-practice` where applicable. An optional `a[data-ht-focus]` is a native anchor to
its unique example ID. Practice has an ID and `data-ht-practice`; optional hints/solutions are
closed native `details` marked `data-ht-hint` or `data-ht-solution` with first-child summaries.
An optional `a[data-ht-retry]` points to the enclosing practice. It closes only that practice's
reveals and keeps learner text; without JS it remains a native link. Never infer an answer,
progress or mastery from clicks, scrolling or reveal state. Keep answers out of pre-reveal labels,
comments and accessibility text; offline source is not exam security.

```bash
python3 <package>/scripts/check_lesson.py --body <scratch>/lesson-body.html
python3 <package>/scripts/build_html.py --profile lesson --body <scratch>/lesson-body.html --title '<subject>' --output <lesson>.html --theme system
python3 <package>/scripts/package_html.py --root <lesson-directory> --name <lesson>.html <lesson>.html
```

Fix preflight errors before assembly. It checks structure, ID/anchor and focus/reveal/retry
relationships; it does not judge content accuracy, answer clues, learning or mastery. Render code
with the shared highlighter and preserve exact source. The two package examples cover a cache
boundary and a non-code classification rule. Neither is a mandatory template. Keep all essential
content expanded and searchable in one continuous DOM, with mobile reading order matching source.
Preserve native deep links, Find, print, no-JS, reduced motion, theme, font scaling and offline
export. When linking previous or next units, use anchors to units that actually exist; omit a missing
neighbor and keep the entire lesson in the DOM. Use the existing separate content review for
correctness, clues and outcome alignment.

For renderer changes, check profile assembly, broken targets, open solutions, misplaced retries,
keyboard/pointer focus and reveals, narrow/wide layout, themes and export. Record unperformed
screen checks as unverified. Ordinary teaching invocations retain their existing opt-in browser
verification boundary; changing this presentation does not change that boundary.
