#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil

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
DOMAIN_CONTEXT_TARGETS = (
    ROOT / "skills/tk-ask-repo/references/domain-context.md",
    ROOT / "skills/tk-audit/references/domain-context.md",
    ROOT / "skills/tk-pr-open/references/domain-context.md",
    ROOT / "skills/tk-pr-respond/references/domain-context.md",
    ROOT / "skills/tk-review/references/domain-context.md",
)

HTML_CONSUMERS = ("tk-explain", "tk-explain-diff", "tk-teach", "tk-research", "tk-qa-sheet", "tk-prototype")
VISUAL_CONSUMERS = ("tk-explain", "tk-explain-diff", "tk-teach", "tk-research")
HTML_ASSETS = ("html-theme.css", "html-theme.js")
HTML_TEMPLATES = ("skills/tk-research/assets/report.html", "skills/tk-qa-sheet/assets/qa-sheet-template.html")
FEEDBACK_MARKER = "<!-- tigerkit:skill-feedback -->"
FEEDBACK_END = "<!-- /tigerkit:skill-feedback -->"
FEEDBACK_BLOCK = FEEDBACK_MARKER + """
## Skill Feedback

When a skill run reveals a reusable incident, preserve only minimal non-secret evidence and suggest a `tk-retro` review. Do not silently invoke it, create improvement artifacts, edit installed skills, or publish issues/PRs. Explicit implementation requests belong to the authorized change owner; this pointer grants no mutation authority.
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


def html_policy_errors(root: Path) -> list[str]:
    errors = []
    source = root / "skills/tk-explain"
    for name in VISUAL_CONSUMERS:
        canonical = source / "references/visual-grammar.md"
        target = root / "skills" / name / "references/visual-grammar.md"
        if not canonical.is_file() or not target.is_file() or target.read_bytes() != canonical.read_bytes():
            errors.append(f"{target.relative_to(root)}: shared visual grammar drift")
    for name in HTML_CONSUMERS:
        for relative in ("references/html-output.md", *(f"assets/{asset}" for asset in HTML_ASSETS)):
            canonical = source / relative
            target = root / "skills" / name / relative
            if not canonical.is_file() or not target.is_file() or target.read_bytes() != canonical.read_bytes():
                errors.append(f"{target.relative_to(root)}: shared HTML contract/asset drift")
        clear_target = root / "skills" / name / "references/clear-writing.md"
        if not CLEAR_WRITING_SOURCE.is_file() or not clear_target.is_file() or clear_target.read_bytes() != CLEAR_WRITING_SOURCE.read_bytes():
            errors.append(f"{clear_target.relative_to(root)}: shared clear-writing drift")
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
    return errors


OUTPUT_NOTATION_MARKER = "<!-- tigerkit:output-notation -->"
OUTPUT_NOTATION_END = "<!-- /tigerkit:output-notation -->"
OUTPUT_NOTATION_BLOCK = OUTPUT_NOTATION_MARKER + """
## Output Notation

Use ASCII numbering such as `(1) Item` or `1. Item`, with a space after the marker, in generated headings, lists, choices, tables, diagrams, and summaries. Use `- Item` for unordered items. Do not generate Unicode circled/enclosed numbers, single-character parenthesized numbers, or keycap emoji as item markers; they can overlap adjacent text in terminal renderers. Preserve exact code, commands, URLs, quotations, identifiers, and verified UI labels unless explicitly authorized to edit them; apply this rule to the surrounding explanation instead.

For authorized user-editable temporary input files, follow the owning skill's Artifact Paths input branch before creation and consumption. A prefilled template does not signal completed input; this rule grants no write authority.
""" + OUTPUT_NOTATION_END + "\n"


def output_notation_errors(skills_root: Path) -> list[str]:
    errors = []
    for path in sorted(skills_root.glob("tk-*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if text.count(OUTPUT_NOTATION_MARKER) != 1 or text.count(OUTPUT_NOTATION_END) != 1 or OUTPUT_NOTATION_BLOCK not in text:
            errors.append(f"{path.parent.name}: sync the exact output notation block with scripts/sync_execution_protocol.py")
    return errors


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
    pairs.append((EXTERNAL_CONTRACT_SOURCE, EXTERNAL_CONTRACT_TARGET))
    context = ROOT / "skills/tk-audit/references/repository-context.md"
    if context.is_file():
        pairs.extend((context, ROOT / "skills" / name / "references/repository-context.md")
                     for name in ("tk-prep", "tk-research"))
    for name in HTML_CONSUMERS:
        if (ROOT / "skills" / name).is_dir():
            pairs.append((CLEAR_WRITING_SOURCE, ROOT / "skills" / name / "references/clear-writing.md"))
            if name != "tk-explain":
                pairs.append((ROOT / "skills/tk-explain/references/html-output.md", ROOT / "skills" / name / "references/html-output.md"))
    for name in HTML_CONSUMERS:
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
        sync_verification(ROOT)
        sync_artifact_guards(ROOT)
        sync_questions(ROOT)
        sync_feedback(ROOT)
    drift = [
        (source, target)
        for source, target in pairs
        if not target.is_file() or target.read_bytes() != source.read_bytes()
    ]
    if args.check:
        notation_errors = output_notation_errors(ROOT / "skills") + validate_artifact_guards(ROOT) + validate_runtime_guard(ROOT) + question_errors(ROOT) + verification_errors(ROOT) + feedback_errors(ROOT)
        notation_errors.extend(html_policy_errors(ROOT))
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
