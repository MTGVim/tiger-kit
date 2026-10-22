#!/usr/bin/env python3
"""Build an offline blind gallery and validate/aggregate one evaluator's export."""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import json
import random
import re
import secrets
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
MIME = {"audio": {".wav": "audio/wav", ".mp3": "audio/mpeg"},
        "image": {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"},
        "video": {".mp4": "video/mp4", ".webm": "video/webm"}}


def read_json(path):
    def pairs(rows):
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")))


def require(value, message):
    if not value:
        raise ValueError(message)


def text(value):
    require(isinstance(value, str) and value.strip(), "expected nonempty text")
    return value


def table(rows):
    require(isinstance(rows, list) and rows, "expected nonempty rows")
    result = {}
    for row in rows:
        require(isinstance(row, dict), "expected row object")
        key = text(row.get("id"))
        require(key not in result, "duplicate ID")
        result[key] = row
    return result


def destination(path, inputs):
    p = Path(path).absolute()
    require(p.resolve() == p and not any(x.is_symlink() for x in [p, *p.parents]), "unsafe output path")
    require(not p.exists(), "output must be a new directory")
    require(not any(Path(x).resolve().is_relative_to(p) for x in inputs), "output contains an input")
    p.mkdir(parents=True)
    return p


def neutral(value, candidates):
    text(value)
    # Boundary matching avoids rejecting ordinary single-letter words inside prose.
    for row in candidates.values():
        for name in (row["id"], row["name"]):
            if (len(name) >= 3 and name.casefold() in value.casefold()) or re.search(r"(?<![A-Za-z0-9])" + re.escape(name) + r"(?![A-Za-z0-9])", value, re.I):
                raise ValueError("identity cue in shared labels or display text")
    return value


def prepare(manifest, source, previous=None):
    require(isinstance(manifest, dict), "manifest must be an object")
    study = text(manifest.get("study_id"))
    version = text(manifest.get("version"))
    seed = text(manifest.get("seed"))
    candidates = table(manifest.get("candidates"))
    require(len(candidates) >= 2, "at least two candidates required")
    for row in candidates.values():
        text(row.get("name"))
    items = table(manifest.get("items"))
    title = neutral(manifest.get("title"), candidates)
    neutral(version, candidates)
    transformations = manifest.get("transformations")
    require(isinstance(transformations, list) and transformations, "declare display transformations or explicit unchanged dimensions")
    for value in transformations:
        neutral(value, candidates)
    require(type(manifest.get("favorite", False)) is bool, "favorite must be boolean")
    if previous is not None:
        require(previous.get("schema") == 1 and previous.get("study_id") == study, "previous key belongs to another study")
    registry = dict(previous.get("registry", {})) if previous else {}
    item_registry = dict(previous.get("item_registry", {})) if previous else {}
    for key in candidates:
        registry.setdefault(key, secrets.token_hex(16))
    for key in items:
        item_registry.setdefault(key, secrets.token_hex(16))
    tokens = list(registry.values()) + list(item_registry.values())
    require(all(isinstance(x, str) and re.fullmatch(r"[a-f0-9]{32}", x) for x in tokens)
            and len(tokens) == len(set(tokens)), "invalid previous identity registry")
    outputs = manifest.get("outputs")
    require(isinstance(outputs, list), "outputs must be a list")
    pairs = {}
    for row in outputs:
        require(isinstance(row, dict), "output must be an object")
        pair = (row.get("item_id"), row.get("candidate_id"))
        require(pair[0] in items and pair[1] in candidates and pair not in pairs, "unknown or duplicate output pair")
        pairs[pair] = row
    require(len(pairs) == len(items) * len(candidates), "include every pair, including failed outputs")
    public = {"schema": 1, "study": hashlib.sha256(study.encode()).hexdigest(), "version": version,
              "title": title, "transformations": transformations, "favorite": manifest.get("favorite", False),
              "candidate_count": len(candidates), "items": []}
    key = {"schema": 1, "study_id": study, "study": public["study"], "version": version,
           "seed": seed, "registry": registry, "item_registry": item_registry,
           "candidates": {registry[c]: {"id": c, "name": candidates[c]["name"]} for c in candidates}, "outputs": [], "order": {}}
    files = []
    used_inputs = [source]
    # Sorting IDs here makes dictionary insertion order irrelevant. Display order is seeded.
    for i, item_id in enumerate(sorted(items), 1):
        description = neutral(items[item_id].get("description"), candidates)
        order = sorted(candidates)
        salt = json.dumps([seed, item_id, sorted(candidates)], ensure_ascii=False)
        random.Random(hashlib.sha256(salt.encode()).digest()).shuffle(order)
        cards = []
        for slot, candidate in enumerate(order, 1):
            raw = pairs[item_id, candidate]
            kind = raw.get("kind")
            require(kind in {*MIME, "text"}, "unsupported output kind")
            failed = "error" in raw
            diagnostic = text(raw["error"]) if failed else ""
            for attempt in range(1000):
                label = f"표본 {slot:03d}" if attempt == 0 else chr(0xAC00 + (attempt * 37 + slot) % 11172) + chr(0xAC00 + slot % 11172)
                if not any(n.casefold() in label.casefold() or label.casefold() in n.casefold()
                           for c in candidates.values() for n in (c["id"], c["name"])):
                    break
            else:
                raise ValueError("cannot choose identity-neutral labels")
            card = {"candidate": registry[candidate], "label": label, "kind": kind, "failed": failed}
            content = ""
            if not failed and kind == "text":
                content = neutral(raw.get("text"), candidates)
                card["text"] = content
                fingerprint_bytes = content.encode()
            elif not failed:
                path = (source.parent / text(raw.get("path"))).resolve()
                require(path.is_file() and path.suffix.lower() in MIME[kind], "missing or unsupported prepared media")
                used_inputs.append(path)
                data = path.read_bytes()
                require(bool(data), "empty prepared media")
                content = f"data:{MIME[kind][path.suffix.lower()]};base64," + base64.b64encode(data).decode()
                filename = f"item-{i:04d}-slot-{slot:04d}{path.suffix.lower()}"
                files.append((filename, data))
                card["src"] = content
                fingerprint_bytes = data
            else:
                fingerprint_bytes = diagnostic.encode()
            fingerprint = hashlib.sha256(kind.encode() + b"\0" + fingerprint_bytes).hexdigest()
            card["fingerprint"] = fingerprint
            record = {"item": item_registry[item_id], "candidate": registry[candidate], "fingerprint": fingerprint,
                      "item_id": item_id, "description": description, "failed": failed,
                      "diagnostic": raw.get("diagnostic", diagnostic)}
            key["outputs"].append(record)
            cards.append(card)
        public["items"].append({"id": item_registry[item_id], "description": description, "cards": cards})
        key["order"][item_registry[item_id]] = [{"candidate": c["candidate"], "label": c["label"]} for c in cards]
    return public, key, files, used_inputs


def safe_json(value):
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def render(public, key, theme):
    sections = []
    for number, item in enumerate(public["items"], 1):
        cards = []
        for slot, card in enumerate(item["cards"], 1):
            content = '<p class="failure">생성 실패</p>'
            if not card["failed"]:
                if card["kind"] == "text":
                    content = '<pre class="sample-text">' + html.escape(card["text"]) + '</pre>'
                elif card["kind"] == "image":
                    content = f'<img src="{card["src"]}" alt="{card["label"]} 비교 이미지">'
                else:
                    tag = card["kind"]
                    content = f'<{tag} controls preload="metadata" src="{card["src"]}" aria-label="{card["label"]} 재생"></{tag}>'
            controls = ''
            if not card["failed"]:
                options = '<option value="">미평가</option>' + ''.join(f'<option value="{n}">{n}점</option>' for n in range(1, 6))
                favorite = '<label><input type="checkbox" data-favorite> 가장 나은 후보</label>' if public["favorite"] else ''
                controls = f'<div class="rating-controls" hidden><label>점수 <select data-score>{options}</select></label><label>메모 <textarea data-note rows="2"></textarea></label>{favorite}</div>'
            cards.append(f'<article class="sample" data-item="{item["id"]}" data-candidate="{card["candidate"]}" data-fingerprint="{card["fingerprint"]}"><h3>{card["label"]}<span class="identity"></span></h3>{content}{controls}</article>')
        sections.append(f'<section id="item-{number:04d}"><h2>항목 {number}</h2><p>{html.escape(item["description"])}</p><div class="sample-grid">' + ''.join(cards) + '</div></section>')
    template = (PACKAGE / 'assets/gallery.html').read_text(encoding="utf-8")
    theme_attr = f'data-default-theme="{theme}"' + (f' data-theme="{theme}"' if theme != 'system' else '')
    values = {"THEME_ATTR": theme_attr, "TITLE": html.escape(public["title"]),
              "VERSION": html.escape(public["version"]), "COUNT": str(public["candidate_count"]),
              "TRANSFORMS": ''.join('<li>' + html.escape(x) + '</li>' for x in public['transformations']),
              "SECTIONS": ''.join(sections), "DATA": safe_json(public),
              "ANSWER": base64.b64encode(json.dumps({"candidates": key["candidates"]}, ensure_ascii=False).encode()).decode(),
              "CSS": (PACKAGE / 'assets/html-theme.css').read_text(encoding='utf-8'),
              "THEME_JS": (PACKAGE / 'assets/html-theme.js').read_text(encoding='utf-8'),
              "APP_JS": (PACKAGE / 'assets/gallery.js').read_text(encoding='utf-8')}
    return re.sub(r'@@([A-Z_]+)@@', lambda match: values[match[1]], template)


def build(manifest_path, output, previous_key=None, theme="system"):
    require(theme in {"system", "light", "dark"}, "invalid theme")
    source = Path(manifest_path).resolve()
    public, key, files, inputs = prepare(read_json(source), source, read_json(previous_key) if previous_key else None)
    if previous_key:
        inputs.append(previous_key)
    rendered = render(public, key, theme)
    dest = destination(output, inputs)
    for filename, data in files:
        (dest / filename).write_bytes(data)
    (dest / 'answer-key.json').write_text(json.dumps(key, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (dest / 'gallery.html').write_text(rendered, encoding='utf-8')
    return public, key


def summarize(ratings, key):
    require(isinstance(ratings, dict) and ratings.get("schema") == 1, "invalid rating schema")
    require(ratings.get("study") == key["study"] and ratings.get("version") == key["version"], "rating study/revision mismatch")
    text(ratings.get("evaluator"))
    require(type(ratings.get("revealed")) is bool, "invalid reveal state")
    rows = ratings.get("ratings")
    require(isinstance(rows, list), "ratings must be an array")
    lookup = {(r["item"], r["candidate"], r["fingerprint"]): r for r in key["outputs"]}
    seen = set()
    data = {}
    favorites = set()
    for row in rows:
        require(isinstance(row, dict), "rating must be an object")
        token = (row.get('item'), row.get('candidate'), row.get('fingerprint'))
        require(token in lookup and token not in seen, "unknown/stale/duplicate rating")
        seen.add(token)
        require(not lookup[token]['failed'], "failed output cannot be scored")
        score = row.get('score')
        require(score is None or type(score) is int and 1 <= score <= 5, "score must be null or integer 1-5")
        require(isinstance(row.get('note'), str) and type(row.get('favorite')) is bool, "invalid note/favorite")
        if row['favorite']:
            require(token[0] not in favorites, "multiple favorites for an item")
            favorites.add(token[0])
        data[token] = row
    candidates = []
    item_rows = []
    for token, identity in key['candidates'].items():
        values = []
        failures = missing = wins = 0
        for lookup_token, output in lookup.items():
            if output['candidate'] != token:
                continue
            rating = data.get(lookup_token, {'score': None, 'note': '', 'favorite': False})
            failures += output['failed']
            missing += not output['failed'] and rating['score'] is None
            wins += rating['favorite']
            if rating['score'] is not None:
                values.append(rating['score'])
            item_rows.append({'item_id': output['item_id'], 'candidate_id': identity['id'],
                              'candidate_name': identity['name'], 'failed': output['failed'],
                              **{k: rating[k] for k in ('score', 'note', 'favorite')}})
        candidates.append({'id': identity['id'], 'name': identity['name'], 'mean': sum(values) / len(values) if values else None,
                           'rated': len(values), 'missing': missing, 'failures': failures, 'favorites': wins})
    return {'schema': 1, 'study_id': key['study_id'], 'version': key['version'], 'evaluators': 1,
            'revealed': ratings['revealed'], 'candidates': candidates, 'items': item_rows,
            'limitations': '평가자는 1명입니다. 미평가와 생성 실패는 평균에서 제외하며 항목별 표본 수와 평가 범위가 다를 수 있습니다.'}


def markdown(summary):
    def cell(value):
        return html.escape(str(value)).replace('|', '\\|').replace('\n', '<br>').replace('\r', '')
    lines = ['# 블라인드 비교 결과', '', '평가자는 1명입니다. 미평가와 생성 실패는 평균에서 제외했습니다. 통계적 우열을 입증하지 않습니다.',
             f'정답 공개 이력: {summary["revealed"]}', '', '| 후보 | 평균 | 평가 수 | 미평가 | 생성 실패 | 최선 선택 |', '|---|---:|---:|---:|---:|---:|']
    for row in summary['candidates']:
        lines.append('| ' + ' | '.join(cell(row[k]) for k in ('name', 'mean', 'rated', 'missing', 'failures', 'favorites')) + ' |')
    lines += ['', '| 항목 | 후보 | 점수 | 실패 | 메모 |', '|---|---|---:|---|---|']
    for row in summary['items']:
        lines.append('| ' + ' | '.join(cell(row[k]) for k in ('item_id', 'candidate_name', 'score', 'failed', 'note')) + ' |')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    b = commands.add_parser('build')
    b.add_argument('manifest'); b.add_argument('--output', required=True); b.add_argument('--previous-key')
    b.add_argument('--theme', choices=('system', 'light', 'dark'), default='system')
    s = commands.add_parser('summarize')
    s.add_argument('ratings'); s.add_argument('--key', required=True); s.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'build':
            build(args.manifest, args.output, args.previous_key, args.theme)
        else:
            summary = summarize(read_json(args.ratings), read_json(args.key))
            dest = destination(args.output, [args.ratings, args.key])
            (dest / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            (dest / 'summary.md').write_text(markdown(summary), encoding='utf-8')
    except (ValueError, KeyError, TypeError, OSError):
        parser.exit(2, 'Invalid comparison input or unsafe output; preserve inputs and check the manifest contract.\n')


if __name__ == '__main__':
    main()
