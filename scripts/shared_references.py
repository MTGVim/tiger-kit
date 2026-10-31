"""Authoring checks for explicitly declared installed sibling references."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


def reference_only(path: Path) -> bool:
    """Explicit reference/setup roles skip shared workflow boilerplate only.

    Setup must bootstrap without dependencies; role schema is enforced by validate_skills.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return False
    try:
        data = yaml.safe_load(text.split("---", 2)[1])
        return data.get("metadata", {}).get("tigerkit", {}).get("role") in {"reference", "setup"}
    except (IndexError, AttributeError, yaml.YAMLError):
        return False


def link_error(source: Path, target: str, skills_root: Path) -> str | None:
    """Permit local files or declared sibling packages, never escapes or symlinks."""
    parsed = urlsplit(target)
    if parsed.scheme or target.startswith("#") or not parsed.path:
        return None
    relative = unquote(parsed.path)
    root = skills_root.absolute()
    source = source.absolute()
    try:
        caller = source.relative_to(root).parts[0]
    except ValueError:
        return "source outside skills root"
    if Path(relative).is_absolute() or "\\" in relative or parsed.netloc:
        return f"unsafe installed reference {target!r}"
    levels = list(source.parent.relative_to(root).parts)
    for part in Path(relative).parts:
        if part == "..":
            if not levels:
                return f"reference traverses outside skills root: {target!r}"
            levels.pop()
        elif part != ".":
            levels.append(part)
    candidate = source.parent / relative
    resolved = candidate.resolve()
    if not resolved.is_relative_to(root.resolve()):
        return f"reference escapes skills root: {target!r}"
    # Reject even internal symlinks: installations ship ordinary independent files.
    current = root
    lexical = Path(os.path.normpath(candidate))
    try:
        parts = lexical.relative_to(root).parts
    except ValueError:
        return f"reference escapes skills root: {target!r}"
    for part in parts:
        current /= part
        if current.is_symlink():
            return f"symlink installed reference: {target!r}"
    if not parts:
        return f"missing package owner: {target!r}"
    owner = parts[0]
    owner_path = root / owner / "SKILL.md"
    if not re.fullmatch(r"tk-[a-z0-9]+(?:-[a-z0-9]+)*", owner) or not owner_path.is_file() or owner_path.is_symlink():
        return f"unknown installed reference owner: {owner}"
    try:
        data = yaml.safe_load(owner_path.read_text(encoding="utf-8").split("---", 2)[1])
        if not isinstance(data, dict) or data.get("name") != owner:
            return f"installed reference owner identity mismatch: {owner}"
    except (OSError, IndexError, yaml.YAMLError):
        return f"invalid installed reference owner: {owner}"
    if owner != caller:
        declaration = root / caller / "dependencies.json"
        try:
            data = json.loads(declaration.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return f"missing or invalid dependency declaration for {caller}: {owner}"
        if (not isinstance(data, dict) or set(data) != {"version", "requires"}
                or type(data.get("version")) is not int or data["version"] != 1
                or not isinstance(data.get("requires"), list)
                or not all(isinstance(item, str) and re.fullmatch(r"tk-[a-z0-9]+(?:-[a-z0-9]+)*", item)
                           for item in data["requires"])
                or len(data["requires"]) != len(set(data["requires"]))):
            return f"invalid dependency declaration for {caller}: {owner}"
        if owner not in data["requires"]:
            return f"undeclared installed reference owner for {caller}: {owner}"
    if not resolved.is_file():
        return f"broken installed reference {target!r}"
    return None


def reference_errors(root: Path, source: Path, target: str) -> list[str]:
    error = link_error(source, target, root / "skills")
    return [f"{source.relative_to(root)}: {error}"] if error else []


# Stable single-owner authoring contract (not an installation/runtime registry).
SHARED_REFERENCES = {
    "skills/tk-questioning/references/questions.md": [
        "skills/tk-adhd/references/questions.md",
        "skills/tk-app-verify/references/questions.md",
        "skills/tk-ask-repo/references/questions.md",
        "skills/tk-audit/references/questions.md",
        "skills/tk-blind-comparison/references/questions.md",
        "skills/tk-browser-verify/references/questions.md",
        "skills/tk-compound/references/questions.md",
        "skills/tk-domain/references/questions.md",
        "skills/tk-explain/references/questions.md",
        "skills/tk-grill/references/questions.md",
        "skills/tk-grooming/references/questions.md",
        "skills/tk-handoff/references/questions.md",
        "skills/tk-inquiry/references/questions.md",
        "skills/tk-merge-conflict/references/questions.md",
        "skills/tk-pr-media/references/questions.md",
        "skills/tk-pr-open/references/questions.md",
        "skills/tk-pr-rebase/references/questions.md",
        "skills/tk-pr-respond/references/questions.md",
        "skills/tk-pr-sweep/references/questions.md",
        "skills/tk-prep/references/questions.md",
        "skills/tk-prototype/references/questions.md",
        "skills/tk-qa-sheet/references/questions.md",
        "skills/tk-research/references/questions.md",
        "skills/tk-retro/references/questions.md",
        "skills/tk-review/references/questions.md",
        "skills/tk-rewrite/references/questions.md",
        "skills/tk-roadmap/references/questions.md",
        "skills/tk-skill-vet/references/questions.md",
        "skills/tk-tts/references/questions.md",
        "skills/tk-video/references/questions.md",
        "skills/tk-wizard/references/questions.md"
    ],
    "skills/tk-artifacts/references/artifact-paths.md": [
        "skills/tk-app-verify/references/artifact-paths.md",
        "skills/tk-audit/references/artifact-paths.md",
        "skills/tk-blind-comparison/references/artifact-paths.md",
        "skills/tk-browser-verify/references/artifact-paths.md",
        "skills/tk-compound/references/artifact-paths.md",
        "skills/tk-domain/references/artifact-paths.md",
        "skills/tk-explain/references/artifact-paths.md",
        "skills/tk-grill/references/artifact-paths.md",
        "skills/tk-grooming/references/artifact-paths.md",
        "skills/tk-handoff/references/artifact-paths.md",
        "skills/tk-inquiry/references/artifact-paths.md",
        "skills/tk-merge-conflict/references/artifact-paths.md",
        "skills/tk-pr-media/references/artifact-paths.md",
        "skills/tk-pr-open/references/artifact-paths.md",
        "skills/tk-pr-rebase/references/artifact-paths.md",
        "skills/tk-pr-respond/references/artifact-paths.md",
        "skills/tk-pr-sweep/references/artifact-paths.md",
        "skills/tk-prep/references/artifact-paths.md",
        "skills/tk-prototype/references/artifact-paths.md",
        "skills/tk-qa-sheet/references/artifact-paths.md",
        "skills/tk-research/references/artifact-paths.md",
        "skills/tk-retro/references/artifact-paths.md",
        "skills/tk-rewrite/references/artifact-paths.md",
        "skills/tk-roadmap/references/artifact-paths.md",
        "skills/tk-skill-vet/references/artifact-paths.md",
        "skills/tk-tts/references/artifact-paths.md",
        "skills/tk-video/references/artifact-paths.md",
        "skills/tk-wizard/references/artifact-paths.md"
    ],
    "skills/tk-artifacts/references/authentication.md": [
        "skills/tk-app-verify/references/authentication.md",
        "skills/tk-audit/references/authentication.md",
        "skills/tk-blind-comparison/references/authentication.md",
        "skills/tk-browser-verify/references/authentication.md",
        "skills/tk-compound/references/authentication.md",
        "skills/tk-domain/references/authentication.md",
        "skills/tk-explain/references/authentication.md",
        "skills/tk-grill/references/authentication.md",
        "skills/tk-grooming/references/authentication.md",
        "skills/tk-handoff/references/authentication.md",
        "skills/tk-inquiry/references/authentication.md",
        "skills/tk-merge-conflict/references/authentication.md",
        "skills/tk-pr-media/references/authentication.md",
        "skills/tk-pr-open/references/authentication.md",
        "skills/tk-pr-rebase/references/authentication.md",
        "skills/tk-pr-respond/references/authentication.md",
        "skills/tk-pr-sweep/references/authentication.md",
        "skills/tk-prep/references/authentication.md",
        "skills/tk-prototype/references/authentication.md",
        "skills/tk-qa-sheet/references/authentication.md",
        "skills/tk-research/references/authentication.md",
        "skills/tk-retro/references/authentication.md",
        "skills/tk-rewrite/references/authentication.md",
        "skills/tk-roadmap/references/authentication.md",
        "skills/tk-skill-vet/references/authentication.md",
        "skills/tk-tts/references/authentication.md",
        "skills/tk-video/references/authentication.md",
        "skills/tk-wizard/references/authentication.md"
    ],
    "skills/tk-verification-guidance/references/provider-knowledge.md": [
        "skills/tk-app-verify/references/provider-knowledge.md",
        "skills/tk-browser-verify/references/provider-knowledge.md"
    ],
    "skills/tk-verification-guidance/references/provider-selection.md": [
        "skills/tk-app-verify/references/provider-selection.md",
        "skills/tk-browser-verify/references/provider-selection.md"
    ],
    "skills/tk-verification-guidance/references/publication-evidence.md": [
        "skills/tk-app-verify/references/publication-evidence.md",
        "skills/tk-browser-verify/references/publication-evidence.md"
    ],
    "skills/tk-ui-evidence/references/ui-evidence.md": [
        "skills/tk-app-verify/references/ui-evidence.md",
        "skills/tk-ask-repo/references/ui-evidence.md",
        "skills/tk-audit/references/ui-evidence.md",
        "skills/tk-browser-verify/references/ui-evidence.md",
        "skills/tk-handoff/references/ui-evidence.md",
        "skills/tk-pr-open/references/ui-evidence.md",
        "skills/tk-pr-respond/references/ui-evidence.md",
        "skills/tk-pr-sweep/references/ui-evidence.md",
        "skills/tk-prep/references/ui-evidence.md",
        "skills/tk-qa-sheet/references/ui-evidence.md",
        "skills/tk-review/references/ui-evidence.md",
        "skills/tk-wizard/references/ui-evidence.md"
    ],
    "skills/tk-verification-guidance/references/verification.md": [
        "skills/tk-app-verify/references/verification.md",
        "skills/tk-browser-verify/references/verification.md"
    ],
    "skills/tk-repository-guidance/references/domain-context.md": [
        "skills/tk-ask-repo/references/domain-context.md",
        "skills/tk-audit/references/domain-context.md",
        "skills/tk-pr-open/references/domain-context.md",
        "skills/tk-pr-respond/references/domain-context.md",
        "skills/tk-prep/references/domain-context.md",
        "skills/tk-review/references/domain-context.md"
    ],
    "skills/tk-writing/references/media-preferences.md": [
        "skills/tk-audit/references/media-preferences.md",
        "skills/tk-browser-verify/references/media-preferences.md",
        "skills/tk-explain/references/media-preferences.md",
        "skills/tk-prep/references/media-preferences.md",
        "skills/tk-research/references/media-preferences.md",
        "skills/tk-video/references/media-preferences.md"
    ],
    "skills/tk-repository-guidance/references/repository-context.md": [
        "skills/tk-audit/references/repository-context.md",
        "skills/tk-prep/references/repository-context.md",
        "skills/tk-research/references/repository-context.md"
    ],
    "skills/tk-engineering/references/security-boundaries.md": [
        "skills/tk-audit/references/security-boundaries.md",
        "skills/tk-pr-respond/references/security-boundaries.md",
        "skills/tk-prep/references/security-boundaries.md",
        "skills/tk-review/references/security-boundaries.md"
    ],
    "skills/tk-writing/references/chart-design.md": [
        "skills/tk-blind-comparison/references/chart-design.md",
        "skills/tk-explain/references/chart-design.md",
        "skills/tk-prototype/references/chart-design.md",
        "skills/tk-qa-sheet/references/chart-design.md",
        "skills/tk-research/references/chart-design.md"
    ],
    "skills/tk-writing/references/clear-writing.md": [
        "skills/tk-blind-comparison/references/clear-writing.md",
        "skills/tk-explain/references/clear-writing.md",
        "skills/tk-prototype/references/clear-writing.md",
        "skills/tk-qa-sheet/references/clear-writing.md",
        "skills/tk-research/references/clear-writing.md",
        "skills/tk-rewrite/references/clear-writing.md"
    ],
    "skills/tk-writing/references/explanation-techniques.md": [
        "skills/tk-blind-comparison/references/explanation-techniques.md",
        "skills/tk-explain/references/explanation-techniques.md",
        "skills/tk-prototype/references/explanation-techniques.md",
        "skills/tk-qa-sheet/references/explanation-techniques.md",
        "skills/tk-research/references/explanation-techniques.md"
    ],
    "skills/tk-writing/references/html-assembly.md": [
        "skills/tk-blind-comparison/references/html-assembly.md",
        "skills/tk-explain/references/html-assembly.md",
        "skills/tk-prototype/references/html-assembly.md",
        "skills/tk-qa-sheet/references/html-assembly.md",
        "skills/tk-research/references/html-assembly.md"
    ],
    "skills/tk-writing/references/html-components.md": [
        "skills/tk-blind-comparison/references/html-components.md",
        "skills/tk-explain/references/html-components.md",
        "skills/tk-prototype/references/html-components.md",
        "skills/tk-qa-sheet/references/html-components.md",
        "skills/tk-research/references/html-components.md"
    ],
    "skills/tk-writing/references/html-figures.md": [
        "skills/tk-blind-comparison/references/html-figures.md",
        "skills/tk-explain/references/html-figures.md",
        "skills/tk-prototype/references/html-figures.md",
        "skills/tk-qa-sheet/references/html-figures.md",
        "skills/tk-research/references/html-figures.md"
    ],
    "skills/tk-writing/references/html-output.md": [
        "skills/tk-blind-comparison/references/html-output.md",
        "skills/tk-explain/references/html-output.md",
        "skills/tk-prototype/references/html-output.md",
        "skills/tk-qa-sheet/references/html-output.md",
        "skills/tk-research/references/html-output.md"
    ],
    "skills/tk-writing/references/html-reader.md": [
        "skills/tk-blind-comparison/references/html-reader.md",
        "skills/tk-explain/references/html-reader.md",
        "skills/tk-prototype/references/html-reader.md",
        "skills/tk-qa-sheet/references/html-reader.md",
        "skills/tk-research/references/html-reader.md"
    ],
    "skills/tk-writing/references/html-render.md": [
        "skills/tk-blind-comparison/references/html-render.md",
        "skills/tk-explain/references/html-render.md",
        "skills/tk-prototype/references/html-render.md",
        "skills/tk-qa-sheet/references/html-render.md",
        "skills/tk-research/references/html-render.md"
    ],
    "skills/tk-writing/references/reader-formatting.md": [
        "skills/tk-blind-comparison/references/reader-formatting.md",
        "skills/tk-explain/references/reader-formatting.md",
        "skills/tk-prototype/references/reader-formatting.md",
        "skills/tk-qa-sheet/references/reader-formatting.md",
        "skills/tk-research/references/reader-formatting.md"
    ],
    "skills/tk-writing/references/diataxis.md": [
        "skills/tk-explain/references/diataxis.md",
        "skills/tk-research/references/diataxis.md"
    ],
    "skills/tk-writing/references/interactive-examples.md": [
        "skills/tk-explain/references/interactive-examples.md",
        "skills/tk-research/references/interactive-examples.md"
    ],
    "skills/tk-writing/references/renderer-contract.md": [
        "skills/tk-explain/references/renderer-contract.md",
        "skills/tk-research/references/renderer-contract.md"
    ],
    "skills/tk-writing/references/scene-figures.md": [
        "skills/tk-explain/references/scene-figures.md",
        "skills/tk-research/references/scene-figures.md"
    ],
    "skills/tk-writing/references/visual-grammar.md": [
        "skills/tk-explain/references/visual-grammar.md",
        "skills/tk-research/references/visual-grammar.md"
    ],
    "skills/tk-questioning/references/visual-questions.md": [
        "skills/tk-grill/references/visual-questions.md",
        "skills/tk-prep/references/visual-questions.md",
        "skills/tk-roadmap/references/visual-questions.md"
    ],
    "skills/tk-pr-guidance/references/github-visuals.md": [
        "skills/tk-pr-open/references/github-visuals.md",
        "skills/tk-pr-respond/references/github-visuals.md",
        "skills/tk-pr-sweep/references/github-visuals.md"
    ],
    "skills/tk-pr-guidance/references/multi-pr-delivery.md": [
        "skills/tk-pr-open/references/multi-pr-delivery.md",
        "skills/tk-pr-respond/references/multi-pr-delivery.md",
        "skills/tk-prep/references/multi-pr-delivery.md"
    ],
    "skills/tk-pr-guidance/references/rebase-readiness.md": [
        "skills/tk-pr-rebase/references/rebase-readiness.md",
        "skills/tk-pr-respond/references/rebase-readiness.md",
        "skills/tk-pr-sweep/references/rebase-readiness.md"
    ],
    "skills/tk-engineering/references/diagnosis.md": [
        "skills/tk-pr-respond/references/diagnosis.md",
        "skills/tk-prep/references/diagnosis.md"
    ],
    "skills/tk-engineering/references/finding-quality.md": [
        "skills/tk-pr-respond/references/finding-quality.md",
        "skills/tk-prep/references/finding-quality.md",
        "skills/tk-review/references/finding-quality.md"
    ],
    "skills/tk-engineering/references/project-rules.md": [
        "skills/tk-pr-respond/references/project-rules.md",
        "skills/tk-prep/references/project-rules.md",
        "skills/tk-review/references/project-rules.md"
    ],
    "skills/tk-engineering/references/react.md": [
        "skills/tk-pr-respond/references/react.md",
        "skills/tk-prep/references/react.md",
        "skills/tk-review/references/react.md"
    ],
    "skills/tk-engineering/references/review-protocol.md": [
        "skills/tk-pr-respond/references/review-protocol.md",
        "skills/tk-prep/references/review-protocol.md",
        "skills/tk-review/references/review-protocol.md"
    ],
    "skills/tk-engineering/references/sdd-interaction.md": [
        "skills/tk-pr-respond/references/sdd-interaction.md",
        "skills/tk-prep/references/sdd-interaction.md"
    ],
    "skills/tk-engineering/references/sdd-recovery.md": [
        "skills/tk-pr-respond/references/sdd-recovery.md",
        "skills/tk-prep/references/sdd-recovery.md"
    ],
    "skills/tk-engineering/references/sdd-transport.md": [
        "skills/tk-pr-respond/references/sdd-transport.md",
        "skills/tk-prep/references/sdd-transport.md"
    ],
    "skills/tk-engineering/references/sdd.md": [
        "skills/tk-pr-respond/references/sdd.md",
        "skills/tk-prep/references/sdd.md"
    ],
    "skills/tk-engineering/references/security.md": [
        "skills/tk-pr-respond/references/security.md",
        "skills/tk-prep/references/security.md",
        "skills/tk-review/references/security.md"
    ],
    "skills/tk-engineering/references/test-doubles.md": [
        "skills/tk-pr-respond/references/test-doubles.md",
        "skills/tk-prep/references/test-doubles.md"
    ],
    "skills/tk-engineering/references/testing.md": [
        "skills/tk-pr-respond/references/testing.md",
        "skills/tk-prep/references/testing.md"
    ],
    "skills/tk-engineering/references/typescript.md": [
        "skills/tk-pr-respond/references/typescript.md",
        "skills/tk-prep/references/typescript.md",
        "skills/tk-review/references/typescript.md"
    ],
    "skills/tk-repository-guidance/references/external-contracts.md": [
        "skills/tk-prep/references/external-contracts.md",
        "skills/tk-wizard/references/external-contracts.md"
    ],
    "skills/tk-engineering/references/selection-handoff.md": [
        "skills/tk-prep/references/selection-handoff.md",
        "skills/tk-prototype/references/selection-handoff.md"
    ]
}

def validate_shared_references(skills_root: Path) -> list[str]:
    errors = shared_boundary_errors(skills_root)
    root = skills_root.parent
    for target, originals in SHARED_REFERENCES.items():
        path = root / target
        if (not path.is_file() or path.is_symlink()
                or not path.resolve().is_relative_to(skills_root.resolve())
                or any(parent.is_symlink() for parent in path.parents if parent.is_relative_to(skills_root))):
            errors.append(f"{target}: missing regular single-owner reference")
        for original in originals:
            if (root / original).exists() or (root / original).is_symlink():
                errors.append(f"{original}: duplicate shared reference; use {target}")
    return errors


# Exact inline availability/authority guards; repository authoring source only.
CONSUMER_BOUNDARY = '## Shared References\n\nLoad the named skill and criteria. If missing, stop: use `tk-setup-skills`; no memory or unapproved installs. Reading grants no authority.\n'
REFERENCE_ONLY_BOUNDARY = 'Use this reference-only skill when the caller needs one of the criteria below. Read only the\nrequested reference under its stated condition; do not preload the whole collection. Return\nthe relevant criteria and unresolved evidence to the calling workflow. This invocation does\nnot start that workflow or grant installation, file mutation, secret access, Git or publication\nauthority. The caller retains its approval gates, authority, evidence and completion duties.\n\nIf this skill or a requested resource is missing, stop the affected action and guide the user\nto `tk-setup-skills`. Do not substitute remembered guidance or silently install dependencies.\nResolve linked sibling packages in the current host\'s installed skill collection, never from\na hardcoded home directory. Dependencies are declared in `dependencies.json`.\n\nIn moved references, `<package>`, "package-local" and "this package" mean the invoking\nworkflow\'s installed package unless an explicit resource link identifies another owner.\nFollowing a resource link reads that resource only; it does not invoke the owner\'s workflow.\n'
SHARED_BOUNDARY_BLOCKS = (CONSUMER_BOUNDARY, REFERENCE_ONLY_BOUNDARY)


def shared_boundary_errors(skills_root: Path) -> list[str]:
    errors = []
    for path in sorted(skills_root.glob("tk-*/SKILL.md")):
        if path.is_symlink() or path.parent.is_symlink() or not path.resolve().is_relative_to(skills_root.resolve()):
            errors.append(f"{path.parent.name}: unsafe shared boundary path")
            continue
        try:
            text = path.read_text(encoding="utf-8")
            data = yaml.safe_load(text.split("---", 2)[1])
        except (OSError, UnicodeError, IndexError, yaml.YAMLError):
            errors.append(f"{path.parent.name}: unreadable shared boundary metadata")
            continue
        metadata = data.get("metadata", {}) if isinstance(data, dict) else {}
        tigerkit = metadata.get("tigerkit", {}) if isinstance(metadata, dict) else {}
        role = tigerkit.get("role") if isinstance(tigerkit, dict) else None
        if role == "setup":
            continue  # Bootstrap uses its own bounded read-only planner contract.
        expected = REFERENCE_ONLY_BOUNDARY if role == "reference" else CONSUMER_BOUNDARY
        if text.count(expected) != 1:
            errors.append(f"{path.parent.name}: shared availability/authority boundary must match exactly once")
    return errors
