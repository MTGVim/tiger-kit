# Notices

TigerKit includes adapted behavior from `mattpocock/skills` (source snapshot inspected at commit `391a2701dd948f94f56a39f7533f8eea9a859c87`).

Current adapted skills:

- `grill-me`
- `to-spec`
- `to-tickets`
- `implement`

Behavior merged from removed adapted skills:

- `grilling` → `grill-me`
- `tdd` → `implement`
- `diagnosing-bugs` → `implement` investigation and planning bug contracts
- `code-review` → `implement` built-in review

Removed historical adapted workflows:

- `grill-with-docs`
- `domain-modeling`

Relationship metadata for current adapted skills: `relationship: adapted`. TigerKit preserves upstream skill names with a `tk-` prefix where the skill remains deployed and rewrites behavior to the TigerKit 20 specification.

`tk-merge-conflict` remains TigerKit-native (`origin: tigerkit`, `relationship: native`). No verified source metadata establishes it as an adaptation of `mattpocock/skills` `resolving-merge-conflicts`.

Upstream license:

```text
MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
