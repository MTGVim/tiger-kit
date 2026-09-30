"""Validate package-local copies of the provider/evidence contract."""
from __future__ import annotations

import importlib.util
from pathlib import Path

REFERENCES = ("verification.md", "provider-selection.md", "providers.json", "provider-knowledge.md", "publication-evidence.md")
SCRIPT = "verify_preferences.py"


def verification_errors(root: Path) -> list[str]:
    source = root / "skills/tk-browser-verify"
    target = root / "skills/tk-app-verify"
    errors = []
    for directory, names in (("references", REFERENCES), ("scripts", (SCRIPT,))):
        for name in names:
            left, right = source / directory / name, target / directory / name
            if not left.is_file() or not right.is_file() or left.read_bytes() != right.read_bytes():
                errors.append(f"tk-app-verify: shared verification {directory}/{name} missing or drifted")
    path = source / "scripts" / SCRIPT
    if path.is_file():
        try:
            spec = importlib.util.spec_from_file_location("verify_preferences_validation", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            providers = module.registry(source / "references/providers.json")
            for row in providers.values():
                note = row["notes"].split("#", 1)[0]
                if Path(note).name != note or not (source / "references" / note).is_file():
                    errors.append(f"provider {row['id']}: missing package-local integration knowledge")
                detection, safety = row["detection"], row["safety"]
                if not all(detection.get(k) for k in ("surface", "hosts", "platforms")):
                    errors.append(f"provider {row['id']}: incomplete detection metadata")
                if not all(safety.get(k) for k in ("input_modes", "profile_boundary", "focus")):
                    errors.append(f"provider {row['id']}: incomplete safety metadata")
        except (ValueError, OSError, ImportError, TypeError) as exc:
            errors.append(f"verification provider registry: {exc}")
    return errors


def sync_verification(root: Path) -> None:
    source = root / "skills/tk-browser-verify"
    target = root / "skills/tk-app-verify"
    for directory, names in (("references", REFERENCES), ("scripts", (SCRIPT,))):
        for name in names:
            destination = target / directory / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((source / directory / name).read_bytes())
