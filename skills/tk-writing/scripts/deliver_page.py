#!/usr/bin/env python3
"""Prepare and verify a one-page report delivery without modifying the source.

Usage: python3 deliver_page.py source.html delivery.html
The delivery must be new. A failed delivery is removed, while source is preserved.
"""
import argparse
from pathlib import Path
import subprocess
import sys

from check_page import Document


def deliver(source: Path, output: Path, owner_skill=None, source_path=None) -> None:
    source = source.resolve(strict=True)
    output = output.absolute()
    if output.exists():
        raise ValueError("delivery already exists; choose a new output path")
    if source == output:
        raise ValueError("delivery must differ from source")
    if not output.parent.is_dir() or output.parent.is_symlink():
        raise ValueError("delivery parent must be an existing regular directory")
    if output.suffix.lower() != ".html":
        raise ValueError("delivery output must be .html")
    scripts = Path(__file__).resolve().parent

    def run(script, *args):
        subprocess.run([sys.executable, str(scripts / script), *map(str, args)], check=True)

    try:
        context_args = []
        if owner_skill is not None:
            context_args.extend(["--owner-skill", owner_skill])
        if source_path is not None:
            context_args.extend(["--source-path", source_path])
        run("add_feedback_studio.py", "--input", source, "--output", output, *context_args)
        doc = Document()
        doc.feed(output.read_text(encoding="utf-8"))
        if doc.download:
            run("package_html.py", "--root", output.parent, "--name", output.name, output.name)
            run("package_html.py", "--root", output.parent, "--name", output.name, "--check", output.name)
        run("check_page.py", output, "--profile", "report", "--require-feedback-studio")
    except (subprocess.CalledProcessError, OSError):
        if output.exists() and output.is_file() and not output.is_symlink():
            output.unlink()
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("delivery", type=Path)
    parser.add_argument("--owner-skill", help="originating tk-* workflow for feedback")
    parser.add_argument("--source-path", type=Path, help="editable manuscript forwarded to feedback studio")
    args = parser.parse_args()
    try:
        deliver(args.source, args.delivery, args.owner_skill, args.source_path)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"delivery failed: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
