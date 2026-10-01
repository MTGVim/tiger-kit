"""Keep the installed user-question contract self-contained and synchronized."""
import re
from pathlib import Path

MARKER = "<!-- tigerkit:questions -->"
END = "<!-- /tigerkit:questions -->"
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
    for path in sorted((root / "skills").glob("tk-*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        reference = path.parent / "references/questions.md"
        if text.count(MARKER) != 1 or text.count(END) != 1 or BLOCK not in text:
            errors.append(f"{path.parent.name}: question rounds guard must match exactly once")
        if re.search(r"AskUserQuestion|request_user_input|`clarify`|Hermes:\s*clarify", text):
            errors.append(f"{path.parent.name}: question tool policy belongs only in the canonical reference")
        if not reference.is_file() or reference.read_bytes() != source.read_bytes():
            errors.append(f"{path.parent.name}: question rounds reference drift")
    return errors


def sync_questions(root: Path) -> None:
    source = root / "skills/tk-grill/references/questions.md"
    content = source.read_bytes()
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
