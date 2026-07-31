#!/usr/bin/env python3
from __future__ import annotations

import argparse


def build_report(name: str, count: int) -> dict[str, object]:
    return {"name": name, "count": count}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="alpha")
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()
    report = build_report(args.name, args.count)
    print(f"name={report['name']} count={report['count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
