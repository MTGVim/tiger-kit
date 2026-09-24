# Clear Writing

These criteria govern explanatory prose and its refinement. The calling skill owns the task, evidence acquisition, output format, and mutation boundaries. Apply relevant criteria without exposing a checklist or imposing a fixed number of paragraphs, examples, scenes, or words.

## Hard Invariants

Apply these within the calling skill's authorized editing scope, before and after contextual style edits. Frequency, density, or a low-severity label never relax them. Protected literals remain exact unless explicitly in scope.

### Meaning Before Polish

A reader should identify the subject, what happens, why, under what conditions, and what remains unknown. Introduce prerequisites this audience needs before relying on them. The final text must carry the context needed for its purpose without relying on the authoring conversation; definitions already present in the document need no repetition. Use concrete actors, stable terms, and actual causal or temporal relationships. When supplied context identifies a department or position, name it instead of an ambiguous umbrella such as `현업`; preserve each actor's distinct responsibility. If the actor or cause is unknown, keep it unknown rather than guessing a department or position. Connect each main point with supporting facts or explanation. Keep useful headings, sequences, comparisons, and domain examples; avoid slogans and decorative structure.

The calling skill determines which facts may be added. Rewriting preserves supplied facts and may restore supplied context; explaining may introduce supported general knowledge and clearly labeled illustrative examples. Neither may invent project history, measurements, decisions, causes, or evidence. Distinguish hypotheses, proposals, observed results, and completed actions. Keep numbers, negation, conditions, alternatives, decision owners, and certainty intact. Do not improve apparent clarity by deleting a limitation or adding a benefit. When rewriting, preserve supported causal, contrastive, temporal, conditional, and conclusion relationships without strengthening, weakening, or inventing them through connectors, reordering, or new assertions. Mere adjacency is not evidence of a relationship.

Preserve meaningful modality in either direction: possibility, capability, permission, obligation, recommendation, and the strength of a claim or hedge are part of its meaning. A different hedge can still strengthen or weaken a claim; a recommendation must not become a requirement, nor a requirement optional advice. Repetition does not authorize either change. When equivalence is uncertain, retain the original modality and improve surrounding word order or sentence boundaries instead. Equivalent capability wording may change when the same actor, action, conditions, and strength remain intact; this is a semantic check, not a protected-word list. Compare each revised claim with its source, including meaning carried by endings and scope, rather than counting hedge markers.

Preserve the binding of each explicit citation, figure/table reference, number, result or measurement to the claim it supports, not just its literal text. When reordering, move evidence with its claim and retain its original scope; proximity to a different sentence never reassigns support. If the source scope is ambiguous, keep that uncertainty rather than broadening support. Ordinary prose without evidence pointers gains no new citation requirement or invented authority.

After polishing, compare each claim-evidence binding and the text with its source or supported explanation outline. Restore background or qualifications lost through shortening. Use existing technical terms, defining unfamiliar ones when needed. Keep code, commands, identifiers, links, quotations, and mandatory attribution exact. Do not treat AI-style removal as authorship concealment or AI-authorship detection.

### Korean Sentence Clarity

Apply this section only to Korean prose. Respect explicit user style requirements and the reader relationship; casual chat is not a writing sample. A supplied sample guides voice within those requirements. Keep formal endings consistent when the genre needs them, varying sentence structure rather than mechanically alternating registers.

Retain sentence components, particles, and endings needed to express the relationship. Replace noun piles and vague possessives with an explicit subject and verb. Concrete Sino-Korean and established technical vocabulary are useful when accurate; do not replace them just to use simpler words. Use customary translations or transliterations when clearer, and retain original terms otherwise. These rules do not translate code, comments, logs, commands, or commit messages.

```text
Before: 정책 변경 영향 검토 후 반영 예정.
After: 정책 변경이 미치는 영향을 검토한 뒤 변경 사항을 반영할 예정입니다.
```

Complete sentences are for prose. Headings, table cells, diagram labels, and buttons may use concise phrases when the relationship is clear from the layout. Do not turn every visual label into a paragraph. A label such as `캐시 조회` can accompany a sentence explaining what is looked up and why.

```text
Before: 그러면 경고가 붙습니다.
Context: 저장하려는 파일이 다른 작업에서 이미 사용 중이면 해당 파일에 경고 표지를 표시한다.
After: 저장하려는 파일이 다른 작업에서 이미 사용 중이면, 해당 파일에 경고 표지가 표시됩니다.
```

Examples show relationships, not permission to infer absent details. If the actor or cause is unknown, keep it unknown. Passive sentences or `할 수 있습니다` can be precise for a capability or an unknown actor. Preserve distinct roles instead of treating administrator, customer, and operator as interchangeable synonyms.

### Required Prose Notation

In ordinary explanatory prose, always replace an em dash (`—`) with a conjunction, colon, parentheses, or separate sentences that retain the relationship. Always replace a section sign such as `§3` with `section 3`, `3절`, or the actual section title, retaining the reference's target and precision. Even one occurrence requires correction; low severity or sparse use is not an exception. Preserve code, commands, URLs, direct quotations, official names, and notation required by the document's format or an explicit user request. Correct the prose relationship, not characters inside protected literals.

In Korean prose, always replace middle-dot (`·`) noun stacking with an explicit relationship: commas for enumeration, `및` or `과/와` for conjunction, and a slash for an established pair such as `조회/취소`. Even one occurrence requires correction; sparse use is no exception. Apply the protected-literal exceptions above, including official names and format-required notation, and preserve verified UI labels. Do not mechanically substitute a slash when the relationship is unclear; retain the uncertainty or ask for the missing context.

In Korean prose, always correct empty modifiers such as `주요`, `핵심`, `가장 중요한`, and `다양한` when they assert importance or scale without identifying the subjects or providing support. This includes modifiers already in the source, even a single occurrence. Put supplied concrete examples or the stated basis first; if neither is available, remove only the empty emphasis without inventing examples or broadening a limited subset into all items. Preserve a source-supported importance claim with its supporting reason, as well as protected literals and established technical terms. These are contextual judgments with mandatory correction, not a word blacklist.

```text
Before: 주요 운영 화면의 언어별 입력 구조를 전환했습니다.
Context: 대상은 목록, 상세, 등록 화면입니다.
After: 목록, 상세, 등록 화면의 언어별 입력 구조를 전환했습니다.
```

For generated item markers in headings, lists, choices, tables, diagrams, and summaries, use ASCII `(1) Item`, `1. Item`, or `- Item`, with a space after the marker. Replace Unicode circled/enclosed numbers, single-character parenthesized numbers, and keycap emoji used as editable item markers; terminal renderers can overlap them with adjacent text. Keep the item order and reference targets intact. Protected literals and verified UI labels remain exact; use plain markers in the surrounding explanation.

## Contextual Patterns

Only after the hard invariants are satisfied, assess expression in its actual genre and local context. These are editing decisions, not authorship signals or runtime scores:

- **Strong artifact:** correct an unnatural construction immediately when it has no useful contextual function and correction preserves meaning.
- **Repetition-sensitive expression:** preserve one or two natural uses; when a repeated connector or construction dominates a paragraph or document, revise only enough occurrences to restore readable rhythm.
- **Weak signal:** edit only when it combines with other patterns or makes the overall rhythm mechanical. An isolated occurrence needs no correction.

When fixing an expression, check that the replacement does not introduce another contextual defect: translationese, stock phrasing, vague abstraction, unnecessary modifiers, or mechanical connectors. Judge the revised passage in context, not by a word blacklist. In expression refinement, a pattern match is only a candidate: edit a span only after confirming a contextual problem and authority within the current request, treating a requested register change as a valid reason. Keep unaffected passages unchanged rather than varying them for style alone, and return the source unchanged when no justified edit or requested structural transformation remains; the hard invariants above still apply. Normal expressions such as `~를 통해`, `~것이다`, passive voice, and capability wording are not banned words. When empirical evidence weakens a presumed style rule, narrow its application rather than adding prohibitions; observations from one genre or model do not establish a universal defect. Never change possibility into certainty to reduce repetition.

Remove unsupported praise, vague authority, generic optimism, fake candor, and ceremonial padding when they add no meaning. Keep politeness and necessary uncertainty. Replace abstract or metaphor-swapped vocabulary with literal actions when clearer; retain established idioms and useful domain terminology.

```text
Before: 또한 해당 이슈는 초기 설정 과정에서 발생할 수 있는 부분이므로 이용에 참고 부탁드립니다.
After: 이 문제는 처음 설정할 때 발생할 수 있습니다.
Unsupported additions: 자주 발생합니다. 오류 화면을 보내 주세요.
```

Keep source-provided actions and deadlines explicit; do not invent support procedures to make a notice more actionable. Describe current behavior in product documentation, but preserve change history in release notes and migration guidance. Reduce overloaded parentheses, decorative emphasis, and repetitive short slogans only where they impair clarity, without removing useful structure.

## Sources

- `docwriter-org/plain-writing-skill`, `f0d3630983ac7a82aa580f1c1509d72df739ee12`: relevant background, concrete subjects, coherent explanation, consistent terminology. Rules 3 and 15 also inform the Korean empty-emphasis and middle-dot requirements; adapt them to supported specifics and protected literals, without importing unrelated formatting bans.
- `hjongc/humanizer-kr`, `a1a7069a32f669afe4b10e35e9522ff504a13263`: reader/register fit, contextual editing, restrained claims, internal naturalness review.
- `snflkd/fluent-korean`, `ce8683f0eba8cddb91de4dcd151425ff73e60498`: Korean sentence components, particles/endings, accurate vocabulary, literal-expression boundaries. This is a selective adaptation with rationale and examples, not a replacement for the upstream global output style.

- `evergreentree97/K-Humanizer`, `324435d561ba48d53de6b7d3fb3dd72cf77030dc`: preserve useful paragraph links without inventing relationships.
- `epoko77-ai/im-not-ai`, `9747f036cdc28a1a8aea4dc71fef1f7846eb96f7`: contextual strength, selective density-based editing, avoiding newly introduced style defects, and conservative correction when empirical evidence contradicts a presumed pattern. Taxonomy, authorship judgments, and numeric thresholds are not imported.

- `conorbronsdon/avoid-ai-writing`, `c4783463cf019a8943364c1ef5f80e0a4c8bff94`: candidate-to-justified-edit scope, preservation of unaffected passages, and valid zero-edit outcomes; no detector, taxonomy, pass budget, or public audit trail is imported.

Original MIT notices are in the calling package's `LICENSE.txt`.

Claim-evidence binding also draws on `AIScientists-Dev/academic-humanizer`,
`94b88b23703bed7df507acae7d6d5876209a0cdf`; evidence addition, academic taxonomy and venue rules are omitted.

Meaningful modality also draws on `epoko77-ai/im-not-ai`,
`92b2936956d65d62ff4b19b75cccad8e3429bf43`: A-10/G-2 and their correction history motivate preserving claim strength even under repetition. Apply semantic equivalence across genres; omit domain-only exceptions, fixed repetition thresholds, hedge dictionaries, marker counts, and runtime restoration.
