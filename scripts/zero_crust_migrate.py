#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_function(text: str, name: str, replacement: str) -> str:
    pattern = re.compile(rf"(?ms)^def {re.escape(name)}\(.*?(?=^def |\Z)")
    updated, count = pattern.subn(replacement.rstrip() + "\n\n", text, count=1)
    if count != 1:
        raise SystemExit(f"expected one function {name}, found {count}")
    return updated


def replace_method(text: str, name: str, replacement: str) -> str:
    pattern = re.compile(rf"(?ms)^    def {re.escape(name)}\(.*?(?=^    def |^class |\Z)")
    updated, count = pattern.subn(replacement.rstrip() + "\n\n", text, count=1)
    if count != 1:
        raise SystemExit(f"expected one method {name}, found {count}")
    return updated


validator_path = ROOT / "scripts/validate_skills.py"
validator = validator_path.read_text(encoding="utf-8")

validator = replace_function(
    validator,
    "validate_user_decision_contract",
    '''def _markdown_section(text: str, heading: str) -> str | None:
    if text.count(heading) != 1:
        return None
    start = text.index(heading) + len(heading)
    match = re.search(r"(?m)^#{1,3} ", text[start:])
    end = start + match.start() if match else len(text)
    return text[start:end].strip()


def validate_user_decision_contract(root: Path) -> list[str]:
    errors: list[str] = []
    heading = "## User decision questions"
    required_tools = ("AskUserQuestion", "request_user_input", "clarify")
    for skill in sorted(EXPECTED_SKILLS - {"tk-adhd"}):
        path = root / "skills" / skill / "SKILL.md"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        section = _markdown_section(text, heading)
        if section is None:
            errors.append(f"{skill}: SKILL.md: add exactly one {heading!r} section")
            continue
        normalized = " ".join(section.split())
        missing: list[str] = []
        if "Question" not in normalized:
            missing.append("Question")
        if "Recommendation" not in normalized:
            missing.append("Recommendation")
        if not any(marker in normalized for marker in ("(Recommended)", "(추천)")):
            missing.append("one recommended marker")
        missing.extend(tool for tool in required_tools if tool not in normalized)
        if "plain text" not in normalized.casefold():
            missing.append("plain-text fallback boundary")
        if not any(status in normalized for status in ("Pending", "Blocked")):
            missing.append("Pending/Blocked preservation")
        if missing:
            errors.append(
                f"{skill}: SKILL.md: incomplete user-decision structure ({', '.join(missing)})"
            )
        if len(section.encode("utf-8")) >= 900:
            errors.append(f"{skill}: SKILL.md: keep user-decision structure below 900 bytes")
        if "option previews, prototype cards" in section:
            errors.append(f"{skill}: SKILL.md: remove question-presentation ceremony")
    return errors''',
)

validator = replace_function(
    validator,
    "validate_response_language_contract",
    '''def validate_response_language_contract(root: Path) -> list[str]:
    errors: list[str] = []
    heading = "### 🔴 HARD GATE · response language"
    for skill in sorted(EXPECTED_SKILLS - {"tk-adhd"}):
        path = root / "skills" / skill / "SKILL.md"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        section = _markdown_section(text, heading)
        if section is None:
            errors.append(f"{skill}: SKILL.md: add exactly one response-language gate")
            continue
        normalized = " ".join(section.casefold().split())
        if len(section.encode("utf-8")) >= 1000:
            errors.append(f"{skill}: SKILL.md: keep response-language gate below 1000 bytes")
        if "language" not in normalized or not any(
            token in normalized for token in ("canonical", "status", "ids", "paths")
        ):
            errors.append(
                f"{skill}: SKILL.md: response-language gate must preserve user language and machine tokens"
            )
    return errors''',
)

validator = replace_function(
    validator,
    "validate_terminal_summary_contract",
    '''def validate_terminal_summary_contract(root: Path) -> list[str]:
    errors: list[str] = []
    terminal_heading = "### 🔴 HARD GATE · terminal user summary"
    language_heading = "### 🔴 HARD GATE · response language"
    forbidden_patterns = (
        re.compile(r"(?m)^## Receipt\\s*$"),
        re.compile(r"(?m)^Outcome:"),
        re.compile(r"`Outcome:\\s*<one user-facing sentence>`"),
    )
    for skill in sorted(EXPECTED_SKILLS - {"tk-adhd"}):
        path = root / "skills" / skill / "SKILL.md"
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        section = _markdown_section(text, terminal_heading)
        if section is None:
            errors.append(f"{skill}: SKILL.md: add exactly one terminal-summary gate")
            continue
        if text.count(language_heading) != 1 or text.index(terminal_heading) > text.index(language_heading):
            errors.append(f"{skill}: SKILL.md: place terminal-summary gate before response-language gate")
        normalized = " ".join(section.casefold().split())
        if len(section.encode("utf-8")) >= 1600:
            errors.append(f"{skill}: SKILL.md: keep terminal-summary gate below 1600 bytes")
        if "terminal user response" not in normalized or "progress" not in normalized:
            errors.append(f"{skill}: SKILL.md: separate progress from terminal user output")
        if any(pattern.search(text) for pattern in forbidden_patterns):
            errors.append(f"{skill}: SKILL.md: remove terminal receipt or Outcome rendering")
    return errors''',
)

validator = replace_function(
    validator,
    "validate_learning_loop_contract",
    '''def validate_learning_loop_contract(root: Path) -> list[str]:
    errors: list[str] = []
    checks = {
        "skills/tk-drive/SKILL.md": (
            (r"at most (?:seven|7)", "bounded prior-art count"),
            (r"prior-art|prior art", "prior-art discovery"),
            (r"raw sessions", "forbidden transient evidence"),
        ),
        "skills/tk-reflect/SKILL.md": (
            (r"Preferred prevention owner", "prevention owner"),
            (r"Host dependency", "host dependency"),
        ),
        "skills/tk-to-spec/SKILL.md": (
            (r"adopted \| already-satisfied \| not-applicable \| conflict", "prior-art disposition"),
            (r"R/AC mapping", "R/AC mapping"),
            (r"conflict.*prevents `Ready`", "conflict gate"),
            (r"omit `## Prior art`", "empty prior-art omission"),
        ),
        "skills/tk-to-tickets/SKILL.md": (
            (r"active.*graph", "active graph handoff"),
            (r"coverage", "source coverage"),
            (r"dependenc", "dependency ownership"),
        ),
    }
    for relative, patterns in checks.items():
        path = root / relative
        text = " ".join(path.read_text(encoding="utf-8").split()) if path.is_file() else ""
        missing = [label for pattern, label in patterns if not re.search(pattern, text, re.I)]
        if missing:
            errors.append(
                f"{relative}: incomplete learning-loop structure ({', '.join(missing)})"
            )
    return errors''',
)

budget_pattern = re.compile(
    r'''(?ms)    normalized_text = " "\.join\(text\.split\(\)\)\n    missing_budget = \[.*?\n    if missing_budget:\n        errors\.append\(.*?\n        \)\n\n'''
)
validator, count = budget_pattern.subn("", validator, count=1)
if count != 1:
    raise SystemExit(f"expected one result-budget validation block, found {count}")

validator = validator.replace(
    '    limit = 250 if kind == "hybrid" else 120',
    '    limit = 160 if kind == "hybrid" else 120',
    1,
)

for relative in (
    "skills/tk-browser-verify/SKILL.md",
    "skills/tk-reflect/SKILL.md",
    "skills/tk-drive/SKILL.md",
):
    block = re.compile(
        rf'''(?ms)        "{re.escape(relative)}": \(.*?\n        \),\n'''
    )
    validator, count = block.subn("", validator, count=1)
    if count != 1:
        raise SystemExit(f"expected one required_text block for {relative}, found {count}")

validator_path.write_text(validator, encoding="utf-8")


test_path = ROOT / "scripts/test_validate_skills.py"
tests = test_path.read_text(encoding="utf-8")

tests = replace_method(
    tests,
    "test_response_language_gate_rejects_one_weakened_skill",
    '''    def test_response_language_gate_rejects_one_weakened_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (source_root / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
                if skill == "tk-ask-repo":
                    text = text.replace(
                        "### 🔴 HARD GATE · response language",
                        "### Response preference",
                        1,
                    )
                target.write_text(text, encoding="utf-8")

            errors = validate_response_language_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])''',
)

tests = replace_method(
    tests,
    "test_terminal_summary_gate_rejects_one_weakened_skill",
    '''    def test_terminal_summary_gate_rejects_one_weakened_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_root = Path(__file__).resolve().parents[1]
            for skill in EXPECTED_SKILLS:
                target = root / "skills" / skill / "SKILL.md"
                target.parent.mkdir(parents=True)
                text = (source_root / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
                if skill == "tk-ask-repo":
                    text = text.replace(
                        "### 🔴 HARD GATE · terminal user summary",
                        "### Output notes",
                        1,
                    )
                target.write_text(text, encoding="utf-8")

            errors = validate_terminal_summary_contract(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("tk-ask-repo", errors[0])''',
)

tests = replace_method(
    tests,
    "test_canonical_skills_embed_native_user_decision_contract",
    '''    def test_canonical_skills_embed_native_user_decision_contract(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_user_decision_contract(root), [])
        for skill in EXPECTED_SKILLS - {"tk-adhd"}:
            text = (root / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            heading = "## User decision questions"
            self.assertEqual(text.count(heading), 1)
            start = text.index(heading) + len(heading)
            match = re.search(r"(?m)^#{1,3} ", text[start:])
            end = start + match.start() if match else len(text)
            self.assertLess(len(text[start:end].encode("utf-8")), 900)''',
)

tests = replace_method(
    tests,
    "test_canonical_skill_outputs_are_decision_first_and_nonduplicative",
    '''    def test_canonical_skill_outputs_are_decision_first_and_nonduplicative(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate_terminal_summary_contract(root), [])
        self.assertEqual(validate_response_language_contract(root), [])
        result_tables = {
            "tk-browser-verify": "Criterion | Result | Evidence",
            "tk-drive": "Ticket | Outcome | Commit",
            "tk-learn": "Candidate | Disposition | Target",
            "tk-merge-conflict": "Path | Intent | Result",
            "tk-prototype": "Criterion | A | B [| C] | Conclusion | Evidence",
            "tk-skill-diagnose": "ID | Incident | Root cause",
            "tk-to-tickets": "Ticket | User-visible slice",
        }
        for skill in EXPECTED_SKILLS:
            text = (root / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("`Outcome: <one user-facing sentence>`", text)
            self.assertNotIn("## Receipt", text)
            if skill in result_tables:
                self.assertIn(result_tables[skill], " ".join(text.split()))''',
)

tests = replace_method(
    tests,
    "test_catalog_result_budget_gate_rejects_one_weakened_skill",
    '''    def test_result_wording_is_not_a_static_abi(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill_dir = Path(directory) / "tk-ask-repo"
            skill_dir.mkdir()
            source = (
                Path(__file__).resolve().parents[1]
                / "skills/tk-ask-repo/SKILL.md"
            ).read_text(encoding="utf-8")
            path = skill_dir / "SKILL.md"
            path.write_text(source.replace("top five to seven", "most relevant items", 1), encoding="utf-8")

            errors, _ = validate_skill(path)

            self.assertFalse(any("bounded result contract missing" in error for error in errors))''',
)

test_path.write_text(tests, encoding="utf-8")

print("zero-crust validator migration applied")
