"""Keep the installed user-question contract self-contained and synchronized."""
import re
from pathlib import Path

MARKER = "<!-- tigerkit:questions -->"
END = "<!-- /tigerkit:questions -->"
QUESTION_NOTICE = """MIT License

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
"""
BLOCK = MARKER + """
## User Questions

Before sending any user-owned clarification, choice, or approval, read [question rounds](references/questions.md) in this turn. Ask the whole answerable frontier in one plain-chat round; resolve facts first, preserve existing authorization, and skip question ceremony when no decision remains. Do not use question tools for ordinary TigerKit questions.

Minimum shape, even when already familiar:

```text
❓ **Q1 · <short title>**: <question and relevant choices>

➡️ <recommendation and reason, when supported>
```

Separate questions with `---`. Put context before the question block and make it the final substantive block: no plan, promise, or “answer and I will proceed” line afterward, except one short reply-format hint. An approval request is its own numbered `Q`, never buried in the proposal. Defer approval whose scope still depends on an unresolved answer.
""" + END + "\n"


def question_errors(root: Path) -> list[str]:
    source = root / "skills/tk-grill/references/questions.md"
    if not source.is_file():
        return ["missing canonical tk-grill question rounds reference"]
    errors = []
    notice = root / "skills/tk-grill/LICENSE.txt"
    notice_text = QUESTION_NOTICE.strip()
    if not notice.is_file():
        errors.append("missing canonical tk-grill question rounds license notice")
    else:
        if notice_text not in notice.read_text(encoding="utf-8"):
            errors.append("invalid canonical tk-grill question rounds license notice")
    for path in sorted((root / "skills").glob("tk-*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        reference = path.parent / "references/questions.md"
        if text.count(MARKER) != 1 or text.count(END) != 1 or BLOCK not in text:
            errors.append(f"{path.parent.name}: question rounds guard must match exactly once")
        if re.search(r"AskUserQuestion|request_user_input|`clarify`|Hermes:\s*clarify", text):
            errors.append(f"{path.parent.name}: question tool policy belongs only in the canonical reference")
        if not reference.is_file() or reference.read_bytes() != source.read_bytes():
            errors.append(f"{path.parent.name}: question rounds reference drift")
        package_notice = path.parent / "LICENSE.txt"
        if not package_notice.is_file() or notice_text not in package_notice.read_text(encoding="utf-8"):
            errors.append(f"{path.parent.name}: installed question rounds license notice is missing or incomplete")
    return errors


def sync_questions(root: Path) -> None:
    source = root / "skills/tk-grill/references/questions.md"
    content = source.read_bytes()
    notice_text = QUESTION_NOTICE.strip()
    for path in sorted((root / "skills").glob("tk-*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if MARKER in text:
            if text.count(MARKER) != 1 or text.count(END) != 1:
                raise ValueError(f"{path}: malformed question guard")
            start, end = text.index(MARKER), text.index(END) + len(END)
            text = text[:start] + BLOCK + text[end:].lstrip("\n")
        else:
            text = text.rstrip() + "\n\n" + BLOCK
        path.write_text(text, encoding="utf-8")
        reference = path.parent / "references/questions.md"
        reference.parent.mkdir(exist_ok=True)
        reference.write_bytes(content)
        package_notice = path.parent / "LICENSE.txt"
        existing = package_notice.read_text(encoding="utf-8") if package_notice.is_file() else ""
        if notice_text not in existing:
            package_notice.write_text(existing.rstrip() + ("\n\n" if existing else "") + notice_text + "\n", encoding="utf-8")
