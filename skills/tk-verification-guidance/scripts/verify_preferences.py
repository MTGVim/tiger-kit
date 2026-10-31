#!/usr/bin/env python3
"""Read/write explicit verification preferences; never launch or route a provider."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

REGISTRY = Path(__file__).resolve().parents[1] / "references/providers.json"
SCOPES = ("browser", "app")
NOTE_FIELDS = ("environment", "condition", "symptom", "workaround")


def usage_url(value: object) -> bool:
    if not isinstance(value, str) or any(c.isspace() for c in value):
        return False
    parsed = urlsplit(value)
    return parsed.scheme == "https" and bool(parsed.hostname) and not parsed.username and not parsed.password


def registry(path: Path = REGISTRY) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1 or not isinstance(data.get("providers"), list):
        raise ValueError("invalid provider registry")
    providers = {}
    for row in data["providers"]:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"] or row["id"] in providers:
            raise ValueError("missing/duplicate provider identity")
        if row.get("scope") not in SCOPES or not usage_url(row.get("docs")):
            raise ValueError("provider needs scope and canonical HTTPS usage URL")
        for key in ("display_name", "notes"):
            if not isinstance(row.get(key), str) or not row[key]:
                raise ValueError(f"provider needs {key}")
        if row.get("recommendation") not in ("recommended", "optional", "reference"):
            raise ValueError("invalid provider recommendation")
        if not isinstance(row.get("detection"), dict) or not isinstance(row.get("safety"), dict):
            raise ValueError("provider needs detection and safety metadata")
        if not isinstance(row.get("capabilities"), list) or not all(isinstance(c, str) and c for c in row["capabilities"]):
            raise ValueError("provider needs capabilities")
        if not all(usage_url(url) for url in row.get("reference_docs", [])):
            raise ValueError("invalid provider reference URL")
        providers[row["id"]] = row
    return providers


def validate_config(data: object, providers: dict) -> dict:
    if not isinstance(data, dict) or data.get("version", 1) != 1:
        raise ValueError("verify config must be a version 1 object")
    for scope in SCOPES:
        if scope not in data:
            continue
        choice = data[scope]
        if not isinstance(choice, dict) or choice.get("selection") != "explicit":
            raise ValueError(f"{scope}: explicit selection required")
        ids = [choice.get("provider")]
        fallbacks = choice.get("fallbacks", [])
        if not isinstance(fallbacks, list):
            raise ValueError(f"{scope}: fallbacks must be a list")
        ids.extend(fallbacks)
        if any(not isinstance(i, str) or i not in providers or providers[i]["scope"] != scope for i in ids):
            raise ValueError(f"{scope}: unknown or wrong-scope provider")
        if len(set(ids)) != len(ids):
            raise ValueError(f"{scope}: duplicate provider/fallback")
    for namespace in ("docsOverrides", "providerNotes"):
        value = data.get(namespace, {})
        if not isinstance(value, dict) or any(key not in providers for key in value):
            raise ValueError(f"invalid {namespace} namespace")
    if not all(usage_url(url) for url in data.get("docsOverrides", {}).values()):
        raise ValueError("docs override must be a credential-free HTTPS URL")
    for notes in data.get("providerNotes", {}).values():
        if not isinstance(notes, list) or len(notes) > 20:
            raise ValueError("provider notes must be a bounded list")
        for note in notes:
            if not isinstance(note, dict) or set(note) != {*NOTE_FIELDS, "verified"} or note["verified"] is not True:
                raise ValueError("only verified structured provider notes are allowed")
            if any(not isinstance(note[k], str) or not 0 < len(note[k]) <= 2000 for k in NOTE_FIELDS):
                raise ValueError("provider note fields must contain 1..2000 characters")
    return data


def config_path(value: str | None) -> Path:
    base = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    return Path(value).expanduser().absolute() if value else Path(base).expanduser().absolute() / "tigerkit/verify.json"


def safe_path(path: Path) -> None:
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("verify config must not traverse symlinks")
    if path.exists() and not path.is_file():
        raise ValueError("verify config must be a regular file")


def read_config(path: Path, providers: dict) -> dict:
    safe_path(path)
    return validate_config(json.loads(path.read_text(encoding="utf-8")), providers) if path.exists() else {}


def update_config(path: Path, providers: dict, mutate) -> dict:
    safe_path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = path.with_name(path.name + ".lock")
    lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    temporary = None
    try:
        data = read_config(path, providers)
        mutate(data)
        data["version"] = 1
        validate_config(data, providers)
        fd, name = tempfile.mkstemp(prefix=".verify-", dir=path.parent)
        temporary = Path(name)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        return data
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        os.close(lock_fd)
        lock.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("show")
    select = commands.add_parser("select")
    select.add_argument("--scope", choices=SCOPES, required=True)
    select.add_argument("--provider", required=True)
    select.add_argument("--fallback", action="append", default=[])
    select.add_argument("--session-only", action="store_true")
    docs = commands.add_parser("docs")
    docs.add_argument("--provider", required=True)
    docs.add_argument("--url", required=True)
    note = commands.add_parser("note")
    note.add_argument("--provider", required=True)
    for field in NOTE_FIELDS:
        note.add_argument("--" + field, required=True)
    note.add_argument("--verified", action="store_true", required=True)
    args = parser.parse_args()
    try:
        providers = registry()
        path = config_path(args.config)
        if args.command == "show":
            data = read_config(path, providers)
        else:
            if args.provider not in providers:
                raise ValueError("unknown provider")
            def mutate(data):
                if args.command == "select":
                    data[args.scope] = {"provider": args.provider, "fallbacks": args.fallback, "selection": "explicit"}
                elif args.command == "docs":
                    data.setdefault("docsOverrides", {})[args.provider] = args.url
                else:
                    entry = {k: getattr(args, k) for k in NOTE_FIELDS} | {"verified": True}
                    notes = data.setdefault("providerNotes", {}).setdefault(args.provider, [])
                    notes[:] = [n for n in notes if (n["environment"], n["condition"]) != (entry["environment"], entry["condition"])]
                    notes.append(entry)
                    del notes[:-20]
            if args.command == "select" and args.session_only:
                data = {}
                mutate(data)
                validate_config(data, providers)
            else:
                data = update_config(path, providers, mutate)
        # Avoid echoing local knowledge or unrelated config into execution logs.
        print(json.dumps({"status": "Pass", "saved": args.command != "show" and not getattr(args, "session_only", False),
                          "preferences": {s: data[s] for s in SCOPES if s in data}}, ensure_ascii=False))
        return 0
    except (ValueError, OSError) as exc:
        reason = str(exc) if isinstance(exc, ValueError) else "preference file access failed: " + type(exc).__name__
        print(json.dumps({"status": "Blocked", "reason": reason, "next_required": "repair config/setup without resetting existing preferences"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
