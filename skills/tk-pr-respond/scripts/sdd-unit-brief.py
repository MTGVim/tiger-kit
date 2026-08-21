#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

UNIT_HEADING = re.compile(r"^### Unit ([1-9][0-9]*): (\S(?:.*\S)?)$")


def outside_fence_lines(lines: list[str]) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    fence: str | None = None
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        marker = "```" if stripped.startswith("```") else "~~~" if stripped.startswith("~~~") else None
        if marker:
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None:
            result.append((index, line))
    return result


def extract(seed_text: str, unit_number: int) -> str:
    lines = seed_text.splitlines()
    outside = outside_fence_lines(lines)
    outside_values = [line for _, line in outside]
    if outside_values.count("<!-- tigerkit:seed -->") != 1:
        raise ValueError("Seed must contain exactly one outside-fence TigerKit ownership marker")
    if outside_values.count("Status: Ready") != 1:
        raise ValueError("Seed must contain exactly one outside-fence 'Status: Ready'")

    execution_rows = [index for index, line in outside if line == "## Execution"]
    if len(execution_rows) != 1:
        raise ValueError("Seed must contain exactly one outside-fence '## Execution' heading")
    start = execution_rows[0]

    end = len(lines)
    for index, line in outside:
        if index > start and line.startswith("## "):
            end = index
            break

    execution_outside = [(index, line) for index, line in outside if start < index < end]
    shape_rows = [index for index, line in execution_outside if line == "Execution shape: SDD"]
    if len(shape_rows) != 1:
        raise ValueError("Execution section must contain exactly one 'Execution shape: SDD'")

    global_rows = [index for index, line in execution_outside if line == "### Global constraints"]
    if len(global_rows) != 1:
        raise ValueError("Execution section must contain exactly one '### Global constraints'")
    global_start = global_rows[0]

    units: list[tuple[int, int, str]] = []
    for index, line in execution_outside:
        match = UNIT_HEADING.fullmatch(line)
        if match:
            units.append((int(match.group(1)), index, match.group(2)))

    if not units:
        raise ValueError("Execution section must contain at least one Unit")
    numbers = [number for number, _, _ in units]
    if numbers != list(range(1, len(units) + 1)):
        raise ValueError("Unit numbers must start at 1 and be unique and sequential")
    if global_start >= units[0][1]:
        raise ValueError("Global constraints must appear before Unit 1")

    by_number = {number: (index, name) for number, index, name in units}
    if unit_number not in by_number:
        raise ValueError(f"Unit {unit_number} does not exist")

    unit_start, _ = by_number[unit_number]
    following = [index for number, index, _ in units if number > unit_number]
    unit_end = min(following) if following else end

    global_end = units[0][1]
    global_block = "\n".join(lines[global_start:global_end]).rstrip()
    unit_block = "\n".join(lines[unit_start:unit_end]).rstrip()
    return f"# TigerKit SDD Unit Brief\nUnit: {unit_number}\n\n{global_block}\n\n{unit_block}\n"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(content, encoding="utf-8")
    temp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract one canonical SDD Unit brief from a Ready TigerKit Seed.")
    parser.add_argument("seed")
    parser.add_argument("unit", type=int)
    parser.add_argument("output")
    args = parser.parse_args()

    if args.unit < 1:
        parser.error("unit must be a positive integer")
    seed = Path(args.seed)
    if not seed.is_file():
        parser.error(f"Seed not found: {seed}")

    try:
        brief = extract(seed.read_text(encoding="utf-8"), args.unit)
        atomic_write(Path(args.output), brief)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
