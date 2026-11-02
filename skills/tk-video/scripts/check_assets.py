#!/usr/bin/env python3
"""Read-only integrity check for explicitly selected data/figure assets."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def regular(path: Path) -> Path:
    if any(p.is_symlink() for p in (path, *path.parents)) or not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"expected a nonempty regular nonsymlink file: {path}")
    return path


def check(manifest: Path) -> dict:
    manifest = regular(Path(manifest).absolute())
    root = manifest.parent.resolve()
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("assets"), list) or not data["assets"]:
        raise ValueError("manifest needs a nonempty assets list")
    results, seen = [], set()
    for row in data["assets"]:
        if not isinstance(row, dict):
            raise ValueError("asset must be an object")
        name = row.get("file")
        if not isinstance(name, str) or not name or "\\" in name:
            raise ValueError("asset file must be a relative POSIX path")
        rel = Path(name)
        if rel.is_absolute() or rel.drive or ".." in rel.parts or rel == Path("."):
            raise ValueError("asset file must stay inside the manifest directory")
        if str(rel) in seen:
            raise ValueError(f"duplicate asset: {name}")
        seen.add(str(rel))
        if not isinstance(row.get("kind"), str) or row["kind"] not in {"measured", "reported", "illustration", "generated"}:
            raise ValueError(f"asset needs an explicit kind: {name}")
        if not isinstance(row.get("made_by"), str) or not row["made_by"].strip():
            raise ValueError(f"asset needs a source or generation command: {name}")
        expected = row.get("sha256")
        if not isinstance(expected, str) or re.fullmatch(r"[0-9a-fA-F]{64}", expected) is None:
            raise ValueError(f"asset needs a SHA256 digest: {name}")
        path = root / rel
        # Missing/symlinked inputs fail without reading the target.
        try:
            regular(path)
        except ValueError as exc:
            results.append({"file": name, "status": "unavailable", "error": str(exc)})
            continue
        digest = hashlib.sha256()
        with path.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
        actual = digest.hexdigest()
        results.append({"file": name, "status": "unchanged" if actual == expected.lower() else "changed",
                        "expected_sha256": expected.lower(), "actual_sha256": actual})
    return {"pass": all(row["status"] == "unchanged" for row in results),
            "scope": "listed asset bytes only; source truth and figure meaning are not assessed", "assets": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        result = check(args.manifest)
    except (OSError, ValueError) as exc:
        print(json.dumps({"pass": False, "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
