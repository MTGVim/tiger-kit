#!/usr/bin/env python3
"""Compile one explicit explanatory scene into a standalone CSS-animated SVG."""
from __future__ import annotations

import argparse
from html import escape
import json
import math
import os
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def number(value, *, positive=False):
    if (not isinstance(value, (int, float)) or isinstance(value, bool)
            or not math.isfinite(value) or value < 0 or positive and value == 0):
        raise ValueError("expected a finite non-negative number")
    return float(value)


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,39}", value):
        raise ValueError("invalid scene identifier")
    return value


def label(value, limit=100):
    if not isinstance(value, str) or not value.strip() or len(value) > limit or any(ord(c) < 32 for c in value):
        raise ValueError("invalid or oversized scene label")
    return value


def fmt(value):
    return f"{value:.5f}".rstrip("0").rstrip(".") or "0"


def build(spec):
    if not isinstance(spec, dict) or set(spec) != {"title", "description", "width", "height", "loop", "nodes", "edges", "events"}:
        raise ValueError("scene requires title, description, width, height, loop, nodes, edges and events")
    title, description = label(spec["title"]), label(spec["description"], 600)
    width, height, loop = (number(spec[key], positive=True) for key in ("width", "height", "loop"))
    if not 600 <= width <= 1600 or not 320 <= height <= 1600 or not 2 <= loop <= 120:
        raise ValueError("scene dimensions or loop exceed authoring bounds")
    for key, maximum in (("nodes", 9), ("edges", 12), ("events", 8)):
        if not isinstance(spec[key], list) or not 1 <= len(spec[key]) <= maximum:
            raise ValueError(f"split the story: invalid {key} count")
    # Reserve fixed readable rows for the complete static event sequence.
    legend_y = height - 32 * len(spec["events"]) - 24
    nodes, boxes, node_boxes, static, edges, schedule, motion, css = {}, [], {}, [], {}, {}, [], []
    if len(title) * 24 > width - 64:
        raise ValueError("shorten the title or widen the scene")
    static.append(f'<text x="32" y="40" font-size="24" font-weight="700">{escape(title)}</text>')
    for node in spec["nodes"]:
        if not isinstance(node, dict) or set(node) != {"id", "label", "x", "y", "width", "height"}:
            raise ValueError("invalid node fields")
        key, text = identifier(node["id"]), label(node["label"], 40)
        if key in nodes:
            raise ValueError("duplicate node identifier")
        x, y, w, h = (number(node[k]) for k in ("x", "y", "width", "height"))
        if (x < 24 or y < 72 or x + w > width - 24 or y + h > legend_y - 24
                or h < 48 or w < len(text) * 18 + 24):
            raise ValueError("node is outside the scene or its label needs more space")
        if any(x < bx + bw + 12 and x + w + 12 > bx and y < by + bh + 12 and y + h + 12 > by for bx, by, bw, bh in boxes):
            raise ValueError("nodes overlap or lack separation")
        boxes.append((x, y, w, h)); nodes[key] = text
        node_boxes[key] = (x, y, w, h)
        static.append(f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" rx="8" fill="#edf4f1" stroke="#41685a"/>')
        static.append(f'<text x="{fmt(x+w/2)}" y="{fmt(y+h/2+6)}" text-anchor="middle" font-size="18">{escape(text)}</text>')
    for edge in spec["edges"]:
        if not isinstance(edge, dict) or set(edge) != {"id", "from", "to", "points"}:
            raise ValueError("invalid edge fields")
        key = identifier(edge["id"])
        if key in edges or edge["from"] not in nodes or edge["to"] not in nodes:
            raise ValueError("duplicate edge or unknown node")
        if not isinstance(edge["points"], list) or not 2 <= len(edge["points"]) <= 8:
            raise ValueError("edge needs two to eight orthogonal points")
        points = []
        for point in edge["points"]:
            if not isinstance(point, list) or len(point) != 2:
                raise ValueError("invalid edge point")
            x, y = map(number, point)
            if not 16 <= x <= width - 16 or not 64 <= y <= legend_y - 16:
                raise ValueError("edge point outside drawing area")
            points.append((x, y))
        for point, node_id in ((points[0], edge["from"]), (points[-1], edge["to"])):
            px, py = point; nx, ny, nw, nh = node_boxes[node_id]
            if not ((px in (nx, nx+nw) and ny <= py <= ny+nh)
                    or (py in (ny, ny+nh) and nx <= px <= nx+nw)):
                raise ValueError("connector endpoint must touch its named node boundary")
        lengths = [math.hypot(b[0]-a[0], b[1]-a[1]) for a,b in zip(points,points[1:])]
        if any(not length or a[0] != b[0] and a[1] != b[1] for a,b,length in zip(points,points[1:],lengths)):
            raise ValueError("connectors must have nonzero orthogonal segments")
        (px, py), (x, y) = points[-2:]
        dx, dy = (x-px)/lengths[-1], (y-py)/lengths[-1]
        arrow = [(x,y),(x-9*dx+5*dy,y-9*dy-5*dx),(x-9*dx-5*dy,y-9*dy+5*dx)]
        static.insert(0, '<polyline points="'+" ".join(f"{fmt(x)},{fmt(y)}" for x,y in points)+'" fill="none" stroke="#55746a" stroke-width="2"/>')
        static.insert(1, '<polygon points="'+" ".join(f"{fmt(x)},{fmt(y)}" for x,y in arrow)+'" fill="#55746a"/>')
        edges[key] = (edge, points, lengths)
    for index, event in enumerate(spec["events"]):
        if (not isinstance(event, dict) or set(event) - {"id", "edge", "label", "at", "after", "gap", "travel"}
                or not {"id", "edge", "label", "travel"} <= set(event) or ("at" in event) == ("after" in event)):
            raise ValueError("event needs exactly one timing source: at or after")
        key, text = identifier(event["id"]), label(event["label"], 70)
        if key in schedule or event["edge"] not in edges:
            raise ValueError("duplicate event or unknown edge")
        if "after" in event:
            if event["after"] not in schedule:
                raise ValueError("after must refer to an earlier event; cycles are invalid")
            start = schedule[event["after"]]["end"] + number(event.get("gap", 0.25))
        else:
            start = number(event["at"])
        travel = number(event["travel"], positive=True); end = start + travel
        if end + 0.12 > loop * 0.9:
            raise ValueError("event leaves no rest gap before the loop repeats")
        edge, points, lengths = edges[event["edge"]]
        caption = f"{index+1}. {nodes[edge['from']]} → {nodes[edge['to']]}: {text} ({fmt(start)}–{fmt(end)}s)"
        if len(caption) * 18 > width - 64:
            raise ValueError("shorten the event label or widen the static sequence")
        static.append(f'<text x="32" y="{fmt(legend_y+index*32+20)}" font-size="18">{escape(caption)}</text>')
        x0,y0 = points[0]; distance = sum(lengths); elapsed = 0
        stops = [f"0%,{fmt(start/loop*100)}%{{opacity:0;transform:translate(0px,0px)}}",
                 f"{fmt((start+min(0.04,travel/4))/loop*100)}%{{opacity:1}}"]
        for (x,y), length in zip(points[1:],lengths):
            elapsed += length
            at = start + travel * elapsed / distance
            stops.append(f"{fmt(at/loop*100)}%{{opacity:1;transform:translate({fmt(x-x0)}px,{fmt(y-y0)}px)}}")
        stops.append(f"{fmt((end+0.1)/loop*100)}%,100%{{opacity:0;transform:translate({fmt(points[-1][0]-x0)}px,{fmt(points[-1][1]-y0)}px)}}")
        css.append(f"@keyframes event-{key}{{"+"".join(stops)+"}")
        motion.append(f'<circle class="packet" cx="{fmt(x0)}" cy="{fmt(y0)}" r="5" fill="#147c53" style="animation-name:event-{key}"/>')
        schedule[key] = {"start": start, "end": end, "edge": event["edge"]}
    styles = (f"text{{font-family:system-ui,sans-serif;fill:#173c2e}}.packet{{opacity:0;animation-duration:{fmt(loop)}s;animation-timing-function:linear;animation-iteration-count:infinite}}"
              + "".join(css) + "@media(prefers-reduced-motion:reduce){.packet{display:none;animation:none}}")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(width)}" height="{fmt(height)}" viewBox="0 0 {fmt(width)} {fmt(height)}" role="img" aria-labelledby="title description">'
           f'<title id="title">{escape(title)}</title><desc id="description">{escape(description)}</desc><style>{styles}</style>'
           f'<rect width="100%" height="100%" fill="#fff"/>'+"".join(static+motion)+"</svg>\n")
    ET.fromstring(svg)
    return svg, schedule


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check", action="store_true", help="compare an existing SVG with its validated scene")
    args = parser.parse_args()
    try:
        with args.spec.open("r", encoding="utf-8") as stream:
            raw = stream.read(512_001)
        if len(raw) > 512_000:
            raise ValueError("scene is oversized")
        svg, schedule = build(json.loads(raw))
        if args.check:
            with args.output.open("r", encoding="utf-8") as stream:
                if stream.read(len(svg)+1) != svg:
                    raise ValueError("SVG differs from its validated scene; regenerate it")
        else:
            if args.output.parent.absolute() != args.output.parent.resolve():
                raise ValueError("output parent must not traverse symlinks")
            fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as stream:
                    stream.write(svg)
            except Exception:
                args.output.unlink()
                raise
        print(json.dumps({"status": "Pass", "schedule": schedule, "runtime_verified": False}))
        return 0
    except (OSError, ValueError, TypeError, KeyError, ET.ParseError) as exc:
        parser.exit(1, f"{type(exc).__name__}: invalid scene or unavailable safe output\n")


if __name__ == "__main__":
    raise SystemExit(main())
