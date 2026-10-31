"""Test fixture helpers for ordinary installed sibling packages."""
import json
from pathlib import Path


def add_package(root: Path, name: str, *, requires=(), role=None, body="") -> Path:
    path = root / "skills" / name / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata = f"metadata:\n  tigerkit:\n    role: {role}\n" if role else ""
    path.write_text(f"---\nname: {name}\n{metadata}---\n{body}", encoding="utf-8")
    (path.parent / "dependencies.json").write_text(json.dumps({"version": 1, "requires": list(requires)}))
    return path


def add_shared_artifacts(root: Path) -> None:
    from artifact_policy import artifact_reference, AUTHENTICATION_REFERENCE
    path = add_package(root, "tk-artifacts", role="reference", requires=("tk-questioning",))
    refs = path.parent / "references"
    refs.mkdir(exist_ok=True)
    (refs / "artifact-paths.md").write_text(artifact_reference("tk-artifacts").replace(
        "(questions.md#", "(../../tk-questioning/references/questions.md#"))
    (refs / "authentication.md").write_text(AUTHENTICATION_REFERENCE)
