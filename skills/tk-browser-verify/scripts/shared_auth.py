#!/usr/bin/env python3
"""Local, worktree-shared *development* authentication handoff.

Only non-secret metadata is written to stdout. Tokens live in a protected file
beneath Git's common directory, never in source, arguments, logs or receipts.
This is not a background worker or an OAuth refresh implementation.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
try:
    import fcntl
except ImportError:  # Never silently fall back to an unverified Windows ACL backend.
    fcntl = None
import hashlib
import json
import os
import re
from pathlib import Path
import secrets
import stat
import subprocess
import sys
import time
from urllib.parse import urlsplit

VERSION = 1
LEASE_SECONDS = 600
POLL_SECONDS = 2


class UnsafeAuth(RuntimeError):
    pass


def now() -> datetime:
    return datetime.now(timezone.utc)


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_time(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("Timestamp must contain a timezone")
    return dt.astimezone(timezone.utc)


def _private_dir(path: Path) -> None:
    if path.is_symlink():
        raise UnsafeAuth("Symlinked credential directory")
    if not path.exists():
        path.mkdir(mode=0o700)
    st = path.lstat()
    if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.getuid() or stat.S_IMODE(st.st_mode) != 0o700:
        raise UnsafeAuth("Credential directory is not private (requires 0700 and current owner)")


def _private_file(path: Path) -> None:
    st = path.lstat()
    if not stat.S_ISREG(st.st_mode) or st.st_uid != os.getuid() or st.st_nlink != 1:
        raise UnsafeAuth("Credential file ownership or link count is unsafe")
    if stat.S_IMODE(st.st_mode) != 0o600:
        raise UnsafeAuth("Credential file must have mode 0600")


def _read(path: Path) -> dict:
    if not path.exists() and not path.is_symlink():
        return {}
    _private_file(path)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    try:
        st = os.fstat(fd)
        original = path.lstat()
        if (st.st_ino, st.st_dev) != (original.st_ino, original.st_dev):
            raise UnsafeAuth("Credential file changed during read")
        with os.fdopen(fd, "r", encoding="utf-8") as handle:
            fd = -1
            data = json.load(handle)
    finally:
        if fd >= 0:
            os.close(fd)
    if not isinstance(data, dict) or data.get("version") not in (None, VERSION):
        raise UnsafeAuth("Invalid credential record")
    return data


def _write(path: Path, data: dict) -> None:
    if path.exists() or path.is_symlink():
        _private_file(path)
    tmp = path.parent / (".tmp-" + secrets.token_hex(12))
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, separators=(",", ":"))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def _origin(value: str) -> str:
    parts = urlsplit(value)
    if parts.scheme not in ("https", "http") or not parts.hostname or parts.username or parts.password:
        raise UnsafeAuth("Use an exact authentication origin, without credentials")
    if parts.path not in ("", "/") or parts.query or parts.fragment:
        raise UnsafeAuth("Authentication authority must be an origin, not an URL with path/query")
    if parts.scheme == "http" and parts.hostname not in ("localhost", "127.0.0.1", "::1"):
        raise UnsafeAuth("Non-loopback authentication authority must use HTTPS")
    return parts.scheme + "://" + parts.netloc.lower()


def location(repo: str, authority: str, environment: str, role: str, profile: str) -> Path:
    if os.name != "posix" or fcntl is None:
        raise UnsafeAuth("No validated private-file ACL backend on this host")
    if not all(x and x.strip() and "\0" not in x for x in (environment, role, profile)):
        raise UnsafeAuth("Environment, role and non-secret profile identity are required")
    if environment.strip().casefold() in ("production", "prod", "live"):
        raise UnsafeAuth("Production credentials are not eligible for this development cache")
    cwd = Path(repo).resolve(strict=True)
    cp = subprocess.run(
        ["git", "-C", str(cwd), "rev-parse", "--path-format=absolute", "--git-common-dir"],
        check=True, capture_output=True, text=True,
    )
    common = Path(cp.stdout.strip())
    if not common.is_dir() or common.is_symlink():
        raise UnsafeAuth("Git common directory is unavailable or symlinked")
    signature = json.dumps(
        [_origin(authority), environment.strip(), role.strip(), profile.strip()],
        ensure_ascii=False, separators=(",", ":"),
    )
    key = hashlib.sha256(signature.encode()).hexdigest()
    home = common / "tigerkit-auth"
    _private_dir(home)
    path = home / key
    _private_dir(path)
    return path


@contextmanager
def locked(path: Path):
    lock = path / ".lock"
    fd = os.open(lock, os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        _private_file(lock)
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def state(home: Path) -> dict:
    record = _read(home / "token.json")
    pending = _read(home / "pending.json")
    info = {
        "status": "missing",
        "revision": record.get("revision"),
        "updated_at": record.get("updated_at"),
        "expires_at": record.get("expires_at"),
    }
    if record.get("token") and not record.get("invalidated"):
        try:
            expires = parse_time(record["expires_at"]) if record.get("expires_at") else None
            info["status"] = "expired" if expires and expires <= now() else ("ready" if expires else "needs-verification")
        except (TypeError, ValueError):
            raise UnsafeAuth("Invalid expiration metadata")
    if pending.get("claim_id") and parse_time(pending["lease_until"]) > now():
        info["status"] = "pending" if info["status"] in ("missing", "expired") else info["status"]
        info["pending_until"] = pending["lease_until"]
    return info


def _result(**fields) -> None:
    print(json.dumps(fields, ensure_ascii=False, sort_keys=True))


def _secret_input(path_text: str, repo: str) -> str:
    root = Path(repo).resolve(strict=True)
    base = root / ".tigerkit" / "secret-input"
    path = Path(path_text).absolute()
    if path.name != "input.json" or path.is_symlink():
        raise UnsafeAuth("Expected regular run-owned secret input.json")
    try:
        path.relative_to(base)
    except ValueError as exc:
        raise UnsafeAuth("Input must be within worktree .tigerkit/secret-input") from exc
    if (root / ".tigerkit").is_symlink() or base.is_symlink():
        raise UnsafeAuth("Symlinked input ancestors are not allowed")
    if not path.parent.parent.samefile(base):
        raise UnsafeAuth("Invalid input directory")
    _private_dir(path.parent)
    _private_file(path)
    data = _read(path)
    if set(data) != {"token"} or not isinstance(data.get("token"), str) or not data["token"].strip():
        raise UnsafeAuth("Input token is absent or invalid")
    return data["token"]



def prepare_input(repo: str, run_id: str) -> dict:
    """Create/reuse a private input file; return only actual paths and blank template."""
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", run_id):
        raise UnsafeAuth("Invalid run identifier")
    root = Path(repo).resolve(strict=True)
    top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"],
                         check=True, capture_output=True, text=True).stdout.strip()
    if root != Path(top).resolve():
        raise UnsafeAuth("--repo must be the actual worktree root")
    tracked = subprocess.run(["git", "-C", str(root), "ls-files", "--",
                              ".tigerkit", ".tigerkit/"], check=True,
                             capture_output=True, text=True).stdout
    ignored = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", "--",
                              ".tigerkit/"], check=False).returncode
    if tracked or ignored != 0:
        raise UnsafeAuth("Ignored and untracked .tigerkit/ must be established first")
    base = root / ".tigerkit"
    if base.is_symlink():
        raise UnsafeAuth("Symlinked artifact root")
    if not base.exists():
        base.mkdir(mode=0o700)
    if not base.is_dir():
        raise UnsafeAuth("Artifact root is not a directory")
    secret = base / "secret-input"
    _private_dir(secret)
    folder = secret / ("tk-browser-verify-" + run_id)
    _private_dir(folder)
    path = folder / "input.json"
    if path.exists() or path.is_symlink():
        _private_file(path)
    else:
        _write(path, {"token": ""})
    return {
        "status": "input-pending",
        "relative_path": str(path.relative_to(root)),
        "absolute_path": str(path),
        "template": {"token": ""},
        "fields": ["token"],
    }


def execute(args: argparse.Namespace) -> int:
    home = location(args.repo, args.authority, args.environment, args.role, args.profile)
    if args.action == "await-input":
        end = time.monotonic() + args.seconds
        while time.monotonic() < end:
            with locked(home):
                pending = _read(home / "pending.json")
                if pending.get("claim_id") != args.claim_id or parse_time(pending["lease_until"]) <= now():
                    raise UnsafeAuth("Refresh claim expired or replaced")
                try:
                    _secret_input(args.input, args.repo)
                except json.JSONDecodeError:
                    pass  # A partially saved JSON file is still pending.
                except UnsafeAuth as exc:
                    if str(exc) != "Input token is absent or invalid":
                        raise  # Permissions and ownership failures must never be masked.
                else:
                    _result(status="ready")
                    return 0
            time.sleep(min(POLL_SECONDS, max(0, end - time.monotonic())))
        _result(status="pending")
        return 2
    if args.action == "wait":
        end = time.monotonic() + args.seconds
        while time.monotonic() < end:
            with locked(home):
                info = state(home)
            if info["revision"] != args.since and info["status"] in ("ready", "needs-verification"):
                _result(**info, token_path=str(home / "token.json"))
                return 0
            time.sleep(min(POLL_SECONDS, max(0, end - time.monotonic())))
        _result(status="timeout")
        return 2
    with locked(home):
        info = state(home)
        if args.action == "inspect":
            _result(**info, token_path=str(home / "token.json") if info["status"] in ("ready", "needs-verification") else None)
        elif args.action == "claim":
            if info["status"] in ("ready", "needs-verification", "pending"):
                _result(**info)
            else:
                claim_id = secrets.token_hex(16)
                _write(home / "pending.json", {"version": VERSION, "claim_id": claim_id, "lease_until": iso(now() + timedelta(seconds=LEASE_SECONDS))})
                _result(status="claimed", claim_id=claim_id, lease_seconds=LEASE_SECONDS)
        elif args.action == "prepare-input":
            pending = _read(home / "pending.json")
            if pending.get("claim_id") != args.claim_id or parse_time(pending["lease_until"]) <= now():
                raise UnsafeAuth("Refresh claim is no longer owned by this run")
            _result(**prepare_input(args.repo, args.run_id))
        elif args.action == "renew":
            pending = _read(home / "pending.json")
            if pending.get("claim_id") != args.claim_id or parse_time(pending["lease_until"]) <= now():
                raise UnsafeAuth("Refresh claim is no longer owned by this run")
            pending["lease_until"] = iso(now() + timedelta(seconds=LEASE_SECONDS))
            _write(home / "pending.json", pending)
            _result(status="renewed", lease_until=pending["lease_until"])
        elif args.action == "commit":
            pending = _read(home / "pending.json")
            if pending.get("claim_id") != args.claim_id or parse_time(pending["lease_until"]) <= now():
                raise UnsafeAuth("Credential claim expired or was replaced")
            expires = iso(parse_time(args.expires_at)) if args.expires_at else None
            token = _secret_input(args.input, args.repo)
            revision = secrets.token_hex(16)
            _write(home / "token.json", {
                "version": VERSION, "token": token, "revision": revision,
                "updated_at": iso(now()), "expires_at": expires,
            })
            (home / "pending.json").unlink()
            _result(status="stored", revision=revision, expires_at=expires)
        elif args.action == "release":
            pending = _read(home / "pending.json")
            if pending.get("claim_id") != args.claim_id:
                raise UnsafeAuth("Refresh claim belongs to another run")
            (home / "pending.json").unlink()
            _result(status="released")
        elif args.action == "invalidate":
            record = _read(home / "token.json")
            if record.get("revision") != args.revision:
                _result(status="superseded")
            else:
                record["invalidated"] = True
                record.pop("token", None)
                _write(home / "token.json", record)
                _result(status="invalidated")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=("inspect", "claim", "prepare-input", "await-input", "renew", "commit", "release", "wait", "invalidate"))
    p.add_argument("--repo", default=".")
    p.add_argument("--authority", required=True, help="Exact trusted auth origin, not a development-server port")
    p.add_argument("--environment", required=True)
    p.add_argument("--role", required=True)
    p.add_argument("--profile", required=True, help="Non-secret account/profile label")
    p.add_argument("--claim-id")
    p.add_argument("--run-id")
    p.add_argument("--input")
    p.add_argument("--expires-at", help="UTC RFC3339 expiry from a verified source, otherwise omit")
    p.add_argument("--revision")
    p.add_argument("--since", default="")
    p.add_argument("--seconds", type=int, default=60)
    args = p.parse_args()
    if args.action in ("prepare-input", "await-input", "renew", "commit", "release") and not args.claim_id:
        p.error("--claim-id is required")
    if args.action == "prepare-input" and not args.run_id:
        p.error("--run-id is required")
    if args.action in ("commit", "await-input") and not args.input:
        p.error("--input is required")
    if args.action == "invalidate" and not args.revision:
        p.error("--revision is required")
    if args.action in ("wait", "await-input") and not 0 < args.seconds <= 180:
        p.error("--seconds must be within 1..180")
    try:
        return execute(args)
    except (UnsafeAuth, ValueError, KeyError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        # No untrusted exception text: it may include user paths or credentials.
        print(json.dumps({"status": "blocked", "reason": type(exc).__name__}))
        return 3


if __name__ == "__main__":
    sys.exit(main())
