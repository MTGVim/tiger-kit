# Revisit reference artifacts

Read only when already taught material has clear recurring lookup value. A lesson builds
understanding through motivation, sequence, examples and practice. A reference supports
quick retrieval of an established distinction, decision rule, syntax, algorithm, glossary
or mechanism; it is not a compressed copy of every chapter.

Select only useful units from the course's verified content. Keep the minimum conditions,
versions, assumptions, material limitations and source links needed to avoid misusing them.
Add no new facts solely in a reference; first research and teach them in the course if they
belong in the approved scope. Preserve canonical terminology and claim provenance.

When useful, create a `reference/<slug>.html` file under the current
identity-verified course home (new `.tigerkit/teach/<topic>/`, explicitly selected
workspace, or legacy `.tigerkit/study/<topic>/`) and link it from `index.html` and relevant chapters. Honor an
explicit Markdown-only format with reference Markdown files rather than forcing HTML.
Use no per-chapter quota or minimum count; if there is no recurring lookup value, create
neither files nor an empty reference directory. A continuation reuses only that course's
verified content and preserves unrelated files and learner records.

Use the existing [HTML output](html-output.md) contract for HTML references and
[visual grammar](visual-grammar.md) only when a figure helps. Keep each HTML file offline
and self-contained; its inclusion does not authorize a new renderer or browser launch.
For quick lookup, prefer descriptive headings, concise comparison/rule tables and searchable
terms. Check print readability when the reference is intended as a printable cheat sheet.
Link to the fuller course explanation without depending on it for essential caveats.

Before delivery, verify that reference claims match taught content and `sources.md`,
conditions/limits survive compression, links resolve within the course, and the course's
curriculum, chapters, practice and continuation state remain intact. Apply required HTML
render checks to every generated reference. Reference creation or reading does not prove
learner mastery and does not create reminders, flashcards or a new learning-state system.
