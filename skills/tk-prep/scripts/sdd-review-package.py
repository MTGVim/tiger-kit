#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


def git(*args: str) -> str:
    env = os.environ.copy()
    env["GIT_PAGER"] = "cat"
    completed = subprocess.run(
        ["git", *args],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "git command failed"
        raise ValueError(detail)
    return completed.stdout


def resolve_commit(ref: str) -> str:
    return git("rev-parse", "--verify", f"{ref}^{{commit}}").strip()


def build_package(base: str, head: str) -> str:
    base_sha = resolve_commit(base)
    head_sha = resolve_commit(head)
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", base_sha, head_sha],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise ValueError(f"BASE is not an ancestor of HEAD: {base_sha}..{head_sha}")

    commits = git("log", "--oneline", "--no-decorate", f"{base_sha}..{head_sha}").rstrip()
    stat = git("diff", "--stat", "--no-ext-diff", f"{base_sha}..{head_sha}").rstrip()
    diff = git("diff", "--no-ext-diff", "-U10", f"{base_sha}..{head_sha}").rstrip()
    return (
        "# TigerKit SDD Review Package\n"
        f"Base: {base_sha}\n"
        f"Head: {head_sha}\n\n"
        "## Commits\n"
        f"{commits or '(none)'}\n\n"
        "## Files changed\n"
        f"{stat or '(none)'}\n\n"
        "## Diff\n"
        f"{diff or '(none)'}\n"
    )


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(content, encoding="utf-8")
    temp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Write an exact BASE..HEAD review package for TigerKit SDD.")
    parser.add_argument("base")
    parser.add_argument("head")
    parser.add_argument("output")
    args = parser.parse_args()
    try:
        atomic_write(Path(args.output), build_package(args.base, args.head))
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
