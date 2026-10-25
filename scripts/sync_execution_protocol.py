#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from html.parser import HTMLParser

try:
    from .verification_policy import verification_errors, sync_verification
    from .question_policy import question_errors, sync_questions
    from .artifact_policy import sync_artifact_guards, validate_artifact_guards
    from .check_runtime_guard import UI_EVIDENCE_CONSUMERS, UI_EVIDENCE_REFERENCE, validate_runtime_guard
except ImportError:
    from verification_policy import verification_errors, sync_verification
    from question_policy import question_errors, sync_questions
    from artifact_policy import sync_artifact_guards, validate_artifact_guards
    from check_runtime_guard import UI_EVIDENCE_CONSUMERS, UI_EVIDENCE_REFERENCE, validate_runtime_guard
from pathlib import Path
try:
    from .narration_policy import errors as narration_errors, sync as sync_narration
except ImportError:
    from narration_policy import errors as narration_errors, sync as sync_narration

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills/tk-prep/references"
TARGET = ROOT / "skills/tk-pr-respond/references"
FILES = ("testing.md", "sdd.md", "sdd-interaction.md", "sdd-recovery.md", "sdd-transport.md", "diagnosis.md", "test-doubles.md")
REVIEW_SOURCE = ROOT / "skills/tk-review/references"
REVIEW_TARGETS = (
    ROOT / "skills/tk-prep/references",
    ROOT / "skills/tk-pr-respond/references",
)
REVIEW_FILES = (
    "review-protocol.md",
    "finding-quality.md",
    "typescript.md",
    "react.md",
    "security.md",
)
EXTERNAL_CONTRACT_SOURCE = ROOT / "skills/tk-prep/references/external-contracts.md"
EXTERNAL_CONTRACT_TARGET = ROOT / "skills/tk-wizard/references/external-contracts.md"
CLEAR_WRITING_SOURCE = ROOT / "skills/tk-rewrite/references/clear-writing.md"
CLEAR_WRITING_TARGET = ROOT / "skills/tk-explain/references/clear-writing.md"
PR_VISUAL_SOURCE = ROOT / "skills/tk-pr-open/references/github-visuals.md"
PR_VISUAL_TARGETS = (
    ROOT / "skills/tk-pr-respond/references/github-visuals.md",
    ROOT / "skills/tk-pr-sweep/references/github-visuals.md",
)
REBASE_READINESS_SOURCE = ROOT / "skills/tk-pr-rebase/references/rebase-readiness.md"
REBASE_READINESS_TARGETS = (
    ROOT / "skills/tk-pr-respond/references/rebase-readiness.md",
    ROOT / "skills/tk-pr-sweep/references/rebase-readiness.md",
)
DOMAIN_CONTEXT_TARGETS = (
    ROOT / "skills/tk-ask-repo/references/domain-context.md",
    ROOT / "skills/tk-audit/references/domain-context.md",
    ROOT / "skills/tk-pr-open/references/domain-context.md",
    ROOT / "skills/tk-pr-respond/references/domain-context.md",
    ROOT / "skills/tk-review/references/domain-context.md",
)

HTML_CONSUMERS = ("tk-explain", "tk-explain-diff", "tk-teach", "tk-research", "tk-qa-sheet", "tk-prototype", "tk-blind-comparison")
QUESTION_HTML_CONSUMERS = ("tk-prep", "tk-grill", "tk-roadmap")
HTML_THEME_CONSUMERS = HTML_CONSUMERS + QUESTION_HTML_CONSUMERS
VISUAL_CONSUMERS = ("tk-explain", "tk-explain-diff", "tk-teach", "tk-research")
HTML_ASSETS = ("html-theme.css", "html-theme.js")
CHART_FILES = ("references/chart-design.md", "assets/chart-examples.html", "references/html-figures.md")
HTML_TEMPLATES = ("skills/tk-research/assets/report.html", "skills/tk-qa-sheet/assets/qa-sheet-template.html")
FEEDBACK_MARKER = "<!-- tigerkit:skill-feedback -->"
FEEDBACK_END = "<!-- /tigerkit:skill-feedback -->"
FEEDBACK_BLOCK = FEEDBACK_MARKER + """
## Skill Feedback

For a reusable incident, retain minimal non-secret evidence in the current conversation
and suggest `tk-retro`; do not write it to persistent memory unless the user asks.
Invocation, feedback artifacts, installed-skill edits and publication require separate
authorization through the owning workflow; this pointer grants none.
""" + FEEDBACK_END + "\n"


def feedback_errors(root: Path) -> list[str]:
    return [f"{path.relative_to(root)}: skill feedback guard must match exactly once"
            for path in sorted((root / "skills").glob("tk-*/SKILL.md"))
            if path.read_text(encoding="utf-8").count(FEEDBACK_MARKER) != 1
            or path.read_text(encoding="utf-8").count(FEEDBACK_END) != 1
            or path.read_text(encoding="utf-8").count(FEEDBACK_BLOCK) != 1]


def sync_feedback(root: Path) -> None:
    for path in sorted((root / "skills").glob("tk-*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if FEEDBACK_MARKER in text:
            if text.count(FEEDBACK_MARKER) != 1 or text.count(FEEDBACK_END) != 1:
                raise ValueError(f"{path}: malformed skill feedback guard")
            start = text.index(FEEDBACK_MARKER)
            end = text.index(FEEDBACK_END, start) + len(FEEDBACK_END)
            if text[end:end + 1] == "\n":
                end += 1
            text = text[:start] + FEEDBACK_BLOCK + text[end:]
        else:
            text = text.rstrip() + "\n\n" + FEEDBACK_BLOCK
        if text != path.read_text(encoding="utf-8"):
            path.write_text(text, encoding="utf-8")


def research_verification_errors(text: str) -> list[str]:
    """Protect the report template's separately labeled verification outcomes."""
    class Summary(HTMLParser):
        def __init__(self):
            super().__init__()
            self.active = False
            self.items = []
            self.item = None
            self.emphasis = False

        def handle_starttag(self, tag, attrs):
            if tag == 'section' and dict(attrs).get('id') == 'verification':
                self.active = True
            if not self.active:
                return
            if tag == 'li':
                self.item = {'label': '', 'body': '', 'label_finished': False}
                self.items.append(self.item)
            if tag == 'strong':
                self.emphasis = True

        def handle_data(self, value):
            if self.active and self.item is not None:
                is_label = self.emphasis and not self.item['label_finished']
                self.item['label' if is_label else 'body'] += value

        def handle_endtag(self, tag):
            if tag == 'strong':
                self.emphasis = False
                if self.item is not None:
                    self.item['label_finished'] = True
            if tag == 'li':
                self.item = None
            if tag == 'section':
                self.active = False

    parser = Summary()
    parser.feed(text)
    labels = [item['label'].strip() for item in parser.items]
    if labels != ['정적 검증:', '화면 검증:'] or any(
        not item['label'].strip() or not item['body'].strip() for item in parser.items
    ):
        return ['research report template: static and screen verification need separate items with bold labels and outcomes']
    return []


def html_policy_errors(root: Path) -> list[str]:
    errors = []
    source = root / "skills/tk-explain"
    for name in VISUAL_CONSUMERS:
        canonical = source / "references/visual-grammar.md"
        target = root / "skills" / name / "references/visual-grammar.md"
        if not canonical.is_file() or not target.is_file() or target.read_bytes() != canonical.read_bytes():
            errors.append(f"{target.relative_to(root)}: shared visual grammar drift")
    for name in HTML_CONSUMERS:
        for relative in ("references/html-output.md", "scripts/package_html.py", "scripts/highlight_code.py", *CHART_FILES):
            canonical = source / relative
            target = root / "skills" / name / relative
            if not canonical.is_file() or not target.is_file() or target.read_bytes() != canonical.read_bytes():
                errors.append(f"{target.relative_to(root)}: shared HTML contract/asset drift")
        for relative in ("references/explanation-techniques.md", "references/html-render.md"):
            canonical = source / relative
            target = root / "skills" / name / relative
            if not canonical.is_file() or not target.is_file() or target.read_bytes() != canonical.read_bytes():
                errors.append(f"{target.relative_to(root)}: shared explanation routing drift")
        clear_target = root / "skills" / name / "references/clear-writing.md"
        if not CLEAR_WRITING_SOURCE.is_file() or not clear_target.is_file() or clear_target.read_bytes() != CLEAR_WRITING_SOURCE.read_bytes():
            errors.append(f"{clear_target.relative_to(root)}: shared clear-writing drift")
    for name in HTML_THEME_CONSUMERS:
        for asset in HTML_ASSETS:
            canonical = source / "assets" / asset
            target = root / "skills" / name / "assets" / asset
            if not canonical.is_file() or not target.is_file() or target.read_bytes() != canonical.read_bytes():
                errors.append(f"{target.relative_to(root)}: shared HTML theme asset drift")
    for relative in HTML_TEMPLATES:
        target = root / relative
        text = target.read_text(encoding="utf-8") if target.is_file() else ""
        for asset in HTML_ASSETS:
            canonical = source / "assets" / asset
            start, end = f"/* tigerkit:{asset} */", f"/* /tigerkit:{asset} */"
            if text.count(start) != 1 or text.count(end) != 1 or not canonical.is_file():
                errors.append(f"{relative}: missing canonical {asset} block")
            elif text.split(start, 1)[1].split(end, 1)[0] != "\n" + canonical.read_text(encoding="utf-8"):
                errors.append(f"{relative}: inline {asset} drift")
        if relative == 'skills/tk-research/assets/report.html':
            errors.extend(research_verification_errors(text))
    return errors


OUTPUT_NOTATION_MARKER = "<!-- tigerkit:output-notation -->"
OUTPUT_NOTATION_END = "<!-- /tigerkit:output-notation -->"
OUTPUT_NOTATION_BLOCK = OUTPUT_NOTATION_MARKER + """
## Output Notation

Use ASCII numbering (`1. Item`, `(1) Item`) and `- Item`, not enclosed/keycap numerals.
Show complete absolute clickable file paths, including examples, without ellipses.
Preserve exact code, commands, identifiers, URLs, quotations and verified UI labels
unless their edit is authorized.

For chat comparisons with multiple shared attributes, use narrow GFM pipe tables
(about four columns, header, short cells); otherwise use lists. No box-drawing,
fenced or empty tables. Owner-specific previews take precedence; publication bodies
and file artifacts retain their own table formats.

In rendered Markdown prose, use hyphens for ranges and escape literal tildes as `\\~`;
preserve exact code, quotations and identifiers.

For authorized temporary input files, follow Artifact Paths before creation and
consumption; a prefilled template is not completed input. This grants no write authority.
""" + OUTPUT_NOTATION_END + "\n"


def output_notation_errors(skills_root: Path) -> list[str]:
    errors = []
    for path in sorted(skills_root.glob("tk-*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if text.count(OUTPUT_NOTATION_MARKER) != 1 or text.count(OUTPUT_NOTATION_END) != 1 or OUTPUT_NOTATION_BLOCK not in text:
            errors.append(f"{path.parent.name}: sync the exact output notation block with scripts/sync_execution_protocol.py")
    return errors


RESULT_SUMMARY_MARKER = "<!-- tigerkit:result-summary -->"
RESULT_SUMMARY_END = "<!-- /tigerkit:result-summary -->"
RESULT_SUMMARY_BLOCK = RESULT_SUMMARY_MARKER + """
## Reader-facing Result Summary

Return a brief result with the outcome, actual verification, material limitations
and direct deliverable links. Distinguish plans/skipped checks from executed work;
retain outstanding manual checks and real cleanup, blocker or human-action details.
Never claim unverified completion or cleanup. Preserve the owner's required artifact,
publication preview, approval boundary, machine return, exact status/footer and final
question block; keep nested returns compact and omit empty sections.
""" + RESULT_SUMMARY_END + "\n"


def result_summary_errors(skills_root: Path) -> list[str]:
    errors = []
    for path in sorted(skills_root.glob("tk-*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if text.count(RESULT_SUMMARY_MARKER) != 1 or text.count(RESULT_SUMMARY_END) != 1 or RESULT_SUMMARY_BLOCK not in text:
            errors.append(f"{path.parent.name}: sync the exact result summary block with scripts/sync_execution_protocol.py")
    return errors



SUMMARY_BODY_MARKER = "<!-- tigerkit:summary-body -->"
SUMMARY_BODY_END = "<!-- /tigerkit:summary-body -->"
SUMMARY_BODY_BLOCK = SUMMARY_BODY_MARKER + """
### Summary body verification

Prepare summary bodies as literal text in a file or structured tool argument, avoiding shell expansion.
After every post/update and when checking a child's publication, fresh-read the exact comment body.
Require exact substrings for the full `<!-- tigerkit:pr-summary:<HEAD_SHA> -->` marker, every intended
`<!-- tigerkit:pr-rereview:<HEAD_SHA>:<LOGIN> -->` marker and `@<LOGIN>` mention against the approved
reviewer set, not just markers found in the body. Missing or mismatched evidence is `Unverifiable`;
the publication owner must repair that same comment and reread it before completion, preserving one summary per head.
""" + SUMMARY_BODY_END + "\n"
SUMMARY_BODY_ANCHORS = {
    "tk-pr-respond": "Do not claim publication complete unless",
    "tk-pr-sweep": "## Completion response",
}


def summary_body_errors(skills_root: Path) -> list[str]:
    errors = []
    for name in SUMMARY_BODY_ANCHORS:
        path = skills_root / name / "SKILL.md"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        if (text.count(SUMMARY_BODY_MARKER) != 1 or text.count(SUMMARY_BODY_END) != 1
                or SUMMARY_BODY_BLOCK not in text):
            errors.append(f"{name}: sync the exact summary body block with scripts/sync_execution_protocol.py")
    return errors


def sync_summary_body(skills_root: Path) -> None:
    for name, anchor in SUMMARY_BODY_ANCHORS.items():
        sync_marked_block(skills_root / name / "SKILL.md", SUMMARY_BODY_MARKER,
                          SUMMARY_BODY_END, SUMMARY_BODY_BLOCK, anchor)


def sync_marked_block(path: Path, marker: str, end_marker: str, block: str, anchor: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text or end_marker in text:
        if text.count(marker) != 1 or text.count(end_marker) != 1:
            raise ValueError(f"{path}: malformed marked block")
        start = text.index(marker)
        end = text.index(end_marker, start) + len(end_marker)
        if text[end:end + 1] == "\n":
            end += 1
        text = text[:start] + block + text[end:]
    else:
        index = text.find(anchor)
        if index == -1:
            text = text.rstrip() + "\n\n" + block
        else:
            text = text[:index] + block + "\n" + text[index:]
    if text != path.read_text(encoding="utf-8"):
        path.write_text(text, encoding="utf-8")


def sync_result_summary(skills_root: Path) -> None:
    for path in sorted(skills_root.glob("tk-*/SKILL.md")):
        sync_marked_block(path, RESULT_SUMMARY_MARKER, RESULT_SUMMARY_END, RESULT_SUMMARY_BLOCK,
                          OUTPUT_NOTATION_MARKER)


def sync_output_notation(skills_root: Path) -> None:
    for path in sorted(skills_root.glob("tk-*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if OUTPUT_NOTATION_MARKER in text:
            start = text.index(OUTPUT_NOTATION_MARKER)
            end = text.find(OUTPUT_NOTATION_END, start + len(OUTPUT_NOTATION_MARKER))
            if end == -1 or text.count(OUTPUT_NOTATION_MARKER) != 1 or text.count(OUTPUT_NOTATION_END) != 1:
                raise ValueError(f"{path}: malformed output notation block; repair its delimiters before syncing")
            end += len(OUTPUT_NOTATION_END)
            if text[end:end + 1] == "\n":
                end += 1
            text = text[:start] + OUTPUT_NOTATION_BLOCK + text[end:]
        else:
            text = text.rstrip() + "\n\n" + OUTPUT_NOTATION_BLOCK
        if text != path.read_text(encoding="utf-8"):
            path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    pairs = [(SOURCE / name, TARGET / name) for name in FILES]
    pairs.extend((SOURCE / "domain-context.md", target) for target in DOMAIN_CONTEXT_TARGETS)
    pairs.extend(
        (REVIEW_SOURCE / name, target / name)
        for target in REVIEW_TARGETS
        for name in REVIEW_FILES
    )
    visual_questions = ROOT / "skills/tk-grill/references/visual-questions.md"
    if visual_questions.is_file():
        pairs.extend((visual_questions, ROOT / "skills" / name / "references/visual-questions.md")
                     for name in ("tk-prep", "tk-roadmap") if (ROOT / "skills" / name).is_dir())
    pairs.append((EXTERNAL_CONTRACT_SOURCE, EXTERNAL_CONTRACT_TARGET))
    pairs.extend((PR_VISUAL_SOURCE, target) for target in PR_VISUAL_TARGETS)
    pairs.extend((REBASE_READINESS_SOURCE, target) for target in REBASE_READINESS_TARGETS)
    context = ROOT / "skills/tk-audit/references/repository-context.md"
    if context.is_file():
        pairs.extend((context, ROOT / "skills" / name / "references/repository-context.md")
                     for name in ("tk-prep", "tk-research"))
    for name in HTML_CONSUMERS:
        if (ROOT / "skills" / name).is_dir():
            pairs.append((CLEAR_WRITING_SOURCE, ROOT / "skills" / name / "references/clear-writing.md"))
            if name != "tk-explain":
                pairs.append((ROOT / "skills/tk-explain/references/html-output.md", ROOT / "skills" / name / "references/html-output.md"))
                for relative in ("references/explanation-techniques.md", "references/html-render.md"):
                    pairs.append((ROOT / "skills/tk-explain" / relative, ROOT / "skills" / name / relative))
                for relative in (*CHART_FILES, "scripts/package_html.py", "scripts/highlight_code.py"):
                    pairs.append((ROOT / "skills/tk-explain" / relative, ROOT / "skills" / name / relative))
    for name in HTML_THEME_CONSUMERS:
        if (ROOT / "skills" / name).is_dir():
            for asset in HTML_ASSETS:
                source = ROOT / "skills/tk-explain/assets" / asset
                if source.is_file():
                    pairs.append((source, ROOT / "skills" / name / "assets" / asset))
    for name in VISUAL_CONSUMERS:
        source = ROOT / "skills/tk-explain/references/visual-grammar.md"
        if name != "tk-explain" and source.is_file():
            pairs.append((source, ROOT / "skills" / name / "references/visual-grammar.md"))
    for name in UI_EVIDENCE_CONSUMERS:
        path = ROOT / "skills" / name / "references/ui-evidence.md"
        if not args.check:
            path.parent.mkdir(exist_ok=True)
            path.write_text(UI_EVIDENCE_REFERENCE, encoding="utf-8")
    if not args.check:
        sync_narration(ROOT)
        sync_verification(ROOT)
        sync_artifact_guards(ROOT)
        sync_questions(ROOT)
        sync_feedback(ROOT)
        sync_result_summary(ROOT / "skills")
        sync_summary_body(ROOT / "skills")
    drift = [
        (source, target)
        for source, target in pairs
        if not target.is_file() or target.read_bytes() != source.read_bytes()
    ]
    if args.check:
        notation_errors = output_notation_errors(ROOT / "skills") + result_summary_errors(ROOT / "skills") + validate_artifact_guards(ROOT) + validate_runtime_guard(ROOT) + question_errors(ROOT) + verification_errors(ROOT) + feedback_errors(ROOT)
        notation_errors.extend(summary_body_errors(ROOT / "skills"))
        notation_errors.extend(html_policy_errors(ROOT))
        notation_errors.extend(narration_errors(ROOT))
        if notation_errors:
            print("\n".join(notation_errors))
        if drift:
            print(
                "Out-of-sync shared reference copies: "
                + ", ".join(str(target.relative_to(ROOT)) for _, target in drift)
            )
            return 1
        if notation_errors:
            return 1
        print("Shared reference copies are synchronized.")
        return 0
    sync_output_notation(ROOT / "skills")
    for source, target in drift:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    for relative in HTML_TEMPLATES:
        path = ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for asset in HTML_ASSETS:
            source = ROOT / "skills/tk-explain/assets" / asset
            start, end = f"/* tigerkit:{asset} */", f"/* /tigerkit:{asset} */"
            if source.is_file() and text.count(start) == 1 and text.count(end) == 1:
                before, rest = text.split(start, 1)
                _, after = rest.split(end, 1)
                text = before + start + "\n" + source.read_text(encoding="utf-8") + end + after
        if text != path.read_text(encoding="utf-8"):
            path.write_text(text, encoding="utf-8")
    print(
        "Synchronized: "
        + (", ".join(str(target.relative_to(ROOT)) for _, target in drift) if drift else "no changes")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
