#!/usr/bin/env python3
"""Emit only the final document, audience/purpose and questions for a fresh reader."""
import argparse
import json
from pathlib import Path


def reader_packet(case):
    source = case["reader_input"]
    return {key: source[key] for key in ("document", "purpose", "questions")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixtures", type=Path)
    parser.add_argument("case_id")
    args = parser.parse_args()
    cases = json.loads(args.fixtures.read_text(encoding="utf-8"))["cases"]
    matches = [case for case in cases if case["id"] == args.case_id]
    if len(matches) != 1:
        parser.error("case_id must identify exactly one case")
    print(json.dumps(reader_packet(matches[0]), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
