# Source dispositions

## Pinned evidence

Primary: [phuryn/pm-skills](https://github.com/phuryn/pm-skills/tree/8607e3b077817f89bf4a9b623246219734ac3be0).
Read implementations and embedded rationale at:

- `pm-execution/skills/outcome-roadmap/SKILL.md`
- `pm-product-discovery/skills/opportunity-solution-tree/SKILL.md`
- `pm-product-discovery/skills/prioritize-features/SKILL.md`

Supplement: [mattpocock/skills wayfinder](https://github.com/mattpocock/skills/blob/c55ee46073ed923f86ce59a5eb3b6d895095d1b7/skills/engineering/wayfinder/SKILL.md).
Upstream behavioral evaluation of these exact procedures is unverified; repository
structural tests do not establish interview quality. TigerKit provides its own behavior cases.

| Disposition | Element | TigerKit decision |
| --- | --- | --- |
| keep | Outcomes rather than feature inventories | Each milestone needs a beneficiary-relevant result and completion evidence. |
| adapt | Outcome/opportunity/solution/experiment separation | Use relevant alternatives and bounded investigations, without mandatory tree depth or counts. |
| adapt | Impact, effort, risk, strategic alignment | Include authority, capacity, dependencies and operating burden; use qualitative judgments when numbers lack evidence. |
| adapt | Wayfinder unspecified versus excluded scope | Preserve conditional later stages separately from excluded work. |
| omit | Quarterly windows, fixed solution/top-five counts | No deadline and sparse evidence are valid; do not manufacture precision. |
| omit | Tracker maps, assignment, research dispatch, runtime | Roadmap creation does not execute work or publish issues. |

## Existing owners and distinct gap

`tk-grill` exhaustively tests decisions and confirms shared understanding without an
artifact. `tk-research` compares external approaches. `tk-prep` prepares and performs
approved repository implementation. This skill owns an optional, user-selected planning
interview and roadmap, including nontechnical work with no repository. It is not a
mandatory upstream phase or a shared-state runner.

The one-topic interview, empty invocation, valid unknown answers, and separate operations
are explicit user-requested adaptations. The source example is not a universal domain rule.
Licenses are distributed in [upstream licenses](../UPSTREAM-LICENSES.txt).
