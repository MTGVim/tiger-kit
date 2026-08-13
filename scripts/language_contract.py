"""Small shared check for generated user-facing Korean prose."""
from __future__ import annotations

import re


LANGUAGE_WORD = re.compile(r"[A-Za-z][A-Za-z0-9_'-]*")
LANGUAGE_EXACT_WORDS = {
    "AC", "API", "Bash", "Blocked", "CLI", "Claude", "Codex", "Conflict",
    "Coverage", "Disposition", "Evidence", "Fail", "Git", "GitHub", "Goal",
    "Hermes", "HTML", "ID", "JSON", "JavaScript", "Lineage", "Markdown", "MCP",
    "NotApplicable", "Orca", "Pass", "Paseo", "Pending", "PR", "Python", "R",
    "Ready", "Receipt", "Scope", "SKILL", "Status", "TigerKit", "TypeScript", "URL",
    "Unverifiable", "Verification", "YAML", "aborted", "applied", "completed",
    "in_progress", "pending", "reported", "unavailable", "unknown", "unverified",
    "false", "true", "hybrid", "native", "user-invoked", "tigerkit",
    "description", "license", "upstream-skill",
}


def _mask_literals(line: str) -> str:
    line = re.sub(r"`[^`]*`", " ", line)
    line = re.sub(r"https?://\S+", " ", line)
    line = re.sub(r"\[(?:user|auto|user/auto)\]", " ", line)
    line = re.sub(
        r"^\s*(?:[-*+]\s+)?(?:name|argument-hint|disable-model-invocation|metadata|kind|origin|relationship|version|tigerkit)\s*:\s*.*$",
        " ",
        line,
    )
    line = re.sub(r"(?<!\w)--[A-Za-z0-9][A-Za-z0-9_-]*", " ", line)
    line = re.sub(r"^\s*(?:[-*+]\s+)?[A-Za-z][A-Za-z0-9_-]*\s*:\s*", "", line)
    return re.sub(r"(?<!\w)(?:[./~]|skills/|\.tigerkit/)[^\s,;:)]+", " ", line)


def _prose_words(line: str) -> set[str]:
    return {
            word
        for word in LANGUAGE_WORD.findall(_mask_literals(line))
        if word not in LANGUAGE_EXACT_WORDS
        and not word.startswith("tk-")
        and not (word.isupper() and len(word) > 1)
        and not any(char.isdigit() for char in word)
        and "_" not in word
    }


def has_korean_prose(text: str) -> bool:
    """Require Hangul and reject unmasked English prose, including mixed lines."""
    has_hangul = False
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not line.strip():
            continue
        if re.search(r"[\uac00-\ud7a3]", line):
            has_hangul = True
        if _prose_words(line):
            return False
    return has_hangul
