# Code and Reference Components

Use only for the components present in the artifact; HTML Output owns the shared shell.

## Code excerpts

Generate static code markup with [the code helper](../scripts/highlight_code.py):
`python3 <package>/scripts/highlight_code.py source.kt --language kotlin --line-start 1`.
Use `.ht-code` with unchanged shared CSS/script.
Color known Kotlin, JavaScript/TypeScript, Python and JSON tokens; mark `diff` additions/deletions.
Leave unknown languages plain. This lexical aid does not validate syntax. Line numbers are CSS
metadata. Compare parsed code `textContent` with the exact source before/after generation and
interaction. Explicitly normalize CR/CRLF/NUL before establishing that baseline: HTML cannot
preserve them. Preserve cited line numbers.

Default to horizontal scrolling. The shared script adds one header with a `data-label` filename
or label (fallback: numbered code label), a copy icon and a `줄바꿈` icon. Both buttons have
accessible names; copy announces success/failure through `aria-live` and preserves the exact
source including trailing newlines. Wrap has `aria-pressed` and hanging indentation; keep no
page-wide preference. Lexical roles include calls, properties/keys, types, literals, punctuation
and JavaScript/TypeScript template interpolation; ambiguous syntax is not parser-validated. Without JS,
retain static colors and scrolling with no inert buttons. Check long/blank lines, diff and unknown
languages, wrap-mode overflow and token contrast >=4.5 against `--code-bg` in both themes.

## Citations and references

For document prose, place numbered superscript citations beside claims where the reader needs
an immediate source, especially disputed, consequential or precisely quoted claims. Collect
verified titles, links and relevant date/revision metadata in a numbered bottom `참고문헌`
section. For other sourced explanation, name the supported section or exact claim in the reference
metadata; use a citation beside the claim whenever section-level binding would be ambiguous.
Keep every external claim traceable; a source list without that binding is insufficient.
Research reports retain their checker-owned requirement that each entry has citation backlinks. Reuse a source number, assigning a unique ID to each citation occurrence.
Use native `<sup id="cite-1-1"><a href="#ref-1" aria-label="참고문헌 1">[1]</a></sup>` with inline references below.
For another occurrence `cite-1-2`, add a second labeled backlink in the same reference entry.
Default each entry to two logical rows: a linked title followed by a muted `.ht-ref-meta`
block with needed institution/version/date, source line range, supported section or claim and
short backlinks for actual citation occurrences. Let long titles and metadata wrap naturally;
never truncate, clamp to two physical lines or use `white-space: nowrap`.
Keep internal inspection/adoption notes in source records and reader-relevant limits beside claims.
An entry with section-level support only needs no fabricated citation or backlink.

```html
<li id="ref-1"><a href="https://example.org/guide">자료 제목</a>
<span class="ht-ref-meta">발행 기관, 2026. 근거: 동작 원리 <a href="#cite-1-1" aria-label="본문 인용으로 복귀">↩</a></span></li>
```
Render each reference item slightly smaller than body text, at `.875em` relative to the body
with `line-height: 1.55`; keep the text readable and allow long titles and URLs to wrap. Keep its
return link visible without letting it dominate the source details. Verify every forward/back target
and claim-source relationship; a bibliography alone is not attribution. Keep code evidence bound to its base/head SHA and `path:line` in the referenced entry;
do not require full diff/source duplication. A supplied explanation target is content, not a
replacement for citations. For document HTML, inline the shared theme script and CSS so that
hovering over a numbered citation, glossary/appendix item or citation backlink, or focusing it
with the keyboard, previews its destination in a bounded, viewport-safe tooltip. Links to `dt`
and `li` targets opt in automatically; use `data-ht-preview` on other same-document links.
Use a one-line title and roughly 200-character summary derived from the target (a term uses
its definition; a backlink uses its surrounding sentence). Essential explanation stays inline. Exclude return links from its displayed
text, preserve existing `aria-describedby` values, and derive text from the rendered reference
rather than injecting external HTML. Escape closes the preview; touching or clicking the native
link still navigates to the full reference, including with JavaScript disabled. On a backlink
return, suppress the outline on the citation superscript alone, without suppressing the visible
keyboard focus of its anchor or other interactive elements. Verify pointer, keyboard, mobile,
no-JavaScript and forward/back navigation. Use independently authored assets: functional UX
inspiration does not authorize copying another site's code, content, branding or visual skin.

The shared script opens external HTTP(S) links in a new tab with `noopener noreferrer`, a
visible marker and an accessible new-tab notice; same-origin links retain native behavior.
Local `file://` documents hide sharing even if the browser advertises file-share support;
download remains available. Other secure contexts still require successful capability detection.

