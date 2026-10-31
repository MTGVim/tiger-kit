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
import runpy
import secrets
import sys
import zipfile
from pathlib import Path

class SharedOwnerError(ValueError):
    """Safe installation guidance, never private comparison input."""


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
    content = sys.stdin.read() if str(path) == "-" else Path(path).read_text(encoding="utf-8")
    return json.loads(content, object_pairs_hook=pairs,
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


def prepare(manifest, source, previous=None, mode="gallery"):
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
        context = {field: neutral(items[item_id][field], candidates)
                   for field in ("title", "script") if field in items[item_id]}
        order = sorted(candidates)
        salt = json.dumps([seed, item_id, sorted(candidates)], ensure_ascii=False)
        random.Random(hashlib.sha256(salt.encode()).digest()).shuffle(order)
        cards = []
        for slot, candidate in enumerate(order, 1):
            raw = pairs[item_id, candidate]
            kind = raw.get("kind")
            require(kind in {*MIME, "text"} or kind == "html" and mode == "versus", "unsupported output kind")
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
            elif not failed and kind == "html":
                path = (source.parent / text(raw.get("path"))).resolve()
                require(path.is_file() and path.suffix.lower() == ".html", "missing or unsupported prepared HTML")
                data = path.read_bytes()
                require(bool(data), "empty prepared HTML")
                neutral(data.decode("utf-8"), candidates)
                neutral(html.unescape(data.decode("utf-8")), candidates)
                used_inputs.append(path)
                filename = f"item-{i:04d}-slot-{slot:04d}-link-0000.html"
                files.append((filename, data))
                card["html_src"] = filename
                fingerprint_bytes = data
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
                if kind == "image":
                    card["display_file"] = filename
                fingerprint_bytes = data
            else:
                fingerprint_bytes = diagnostic.encode()
            # Optional public evidence changes the rated material; legacy bytes keep their hash.
            extras = {}
            if "annotation" in raw:
                card["annotation"] = neutral(raw["annotation"], candidates)
                extras["annotation"] = card["annotation"]
            links = raw.get("links", [])
            require(isinstance(links, list), "links must be a list")
            link_fingerprints = []
            for index, link in enumerate(links, 1):
                require(isinstance(link, dict), "link must be an object")
                label_text = neutral(link.get("label"), candidates)
                path = (source.parent / text(link.get("path"))).resolve()
                require(path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".html", ".txt", ".pdf"},
                        "missing or unsupported prepared link")
                data = path.read_bytes()
                require(bool(data), "empty prepared link")
                # Textual link contents are inspectable; compressed bytes are not text.
                # Binary metadata, pixels and encoded cues retain the manual identity review.
                if path.suffix.lower() in {".html", ".txt"}:
                    decoded = data.decode("utf-8")
                    neutral(decoded, candidates)
                    neutral(html.unescape(decoded), candidates)
                used_inputs.append(path)
                filename = f"item-{i:04d}-slot-{slot:04d}-link-{index:04d}{path.suffix.lower()}"
                files.append((filename, data))
                card.setdefault("links", []).append({"label": label_text, "href": filename})
                link_fingerprints.append({"label": label_text, "type": path.suffix.lower(), "sha256": hashlib.sha256(data).hexdigest()})
            if link_fingerprints:
                extras["links"] = link_fingerprints
            if extras:
                fingerprint_bytes += b"\0public-evidence\0" + json.dumps(extras, sort_keys=True, ensure_ascii=False).encode()
            fingerprint = hashlib.sha256(kind.encode() + b"\0" + fingerprint_bytes).hexdigest()
            card["fingerprint"] = fingerprint
            record = {"item": item_registry[item_id], "candidate": registry[candidate], "fingerprint": fingerprint,
                      "item_id": item_id, "description": description, "failed": failed,
                      "diagnostic": raw.get("diagnostic", diagnostic)}
            key["outputs"].append(record)
            cards.append(card)
        public["items"].append({"id": item_registry[item_id], "description": description, **context, "cards": cards})
        key["order"][item_registry[item_id]] = [{"candidate": c["candidate"], "label": c["label"]} for c in cards]
    return public, key, files, used_inputs


def safe_json(value):
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def render(public, key, theme, mode="gallery", external_key=False):
    # Shared theme belongs to tk-writing in this installed collection only.
    writing = PACKAGE.parent / 'tk-writing'
    resources = [writing / 'SKILL.md', writing / 'assets/html-theme.css', writing / 'assets/html-theme.js']
    if any(p.is_symlink() for resource in resources for p in (resource, *resource.parents)):
        raise SharedOwnerError('Unsafe tk-writing resource; use tk-setup-skills')
    validator = PACKAGE.parent / 'tk-setup-skills/scripts/skill_dependencies.py'
    if not validator.is_file() or any(p.is_symlink() for p in (validator, *validator.parents)):
        raise SharedOwnerError('tk-setup-skills validator unavailable or unsafe; use tk-setup-skills')
    try:
        metadata = runpy.run_path(str(validator), run_name='tk_setup_metadata')
        metadata['read_package'](PACKAGE.parent, 'tk-setup-skills')
        metadata['read_package'](PACKAGE.parent, 'tk-writing')
    except (OSError, ValueError):
        raise SharedOwnerError('Shared owner validation failed; use tk-setup-skills with an approved Python/PyYAML environment') from None
    sections = []
    for number, item in enumerate(public["items"], 1):
        cards = []
        for slot, card in enumerate(item["cards"], 1):
            content = '<p class="failure">생성 실패</p>'
            if not card["failed"]:
                if card["kind"] == "html":
                    content = '<p>HTML을 표시할 수 없으면 아래 원본 문서 링크를 이용해 주세요.</p>'
                elif card["kind"] == "text":
                    content = '<pre class="sample-text">' + html.escape(card["text"]) + '</pre>'
                elif card["kind"] == "image":
                    content = f'<img src="{card["src"]}" alt="{card["label"]} 비교 이미지">'
                else:
                    tag = card["kind"]
                    content = f'<{tag} controls preload="metadata" src="{card["src"]}" aria-label="{card["label"]} 재생"></{tag}>'
            html_src = card.get("html_src") if mode == "versus" else None
            if mode == "versus" and not card["failed"] and not html_src:
                html_src = next((link["href"] for link in card.get("links", []) if link["href"].endswith(".html")), None)
            if html_src:
                content = '<div class="sample-fallback">' + content + '</div>'
                fallback_label = '캡처로 보기' if card['kind'] == 'image' else '대체 안내 보기'
                content += f'<p class="html-tools"><button type="button" class="toggle-preview" hidden>{fallback_label}</button> <a href="{html_src}" target="_blank" rel="noopener noreferrer">원본 문서</a></p>'
            if card.get("display_file"):
                content += f'<p><a href="{card["display_file"]}" target="_blank" rel="noopener noreferrer">원본 크기로 보기</a></p>'
            if card.get("links"):
                content += '<ul class="display-links">' + ''.join(
                    f'<li><a href="{link["href"]}" target="_blank" rel="noopener noreferrer">{html.escape(link["label"])}</a></li>'
                    for link in card["links"]) + '</ul>'
            if card.get("annotation"):
                content += '<p class="annotation">' + html.escape(card["annotation"]) + '</p>'
            controls = ''
            if not card["failed"]:
                options = '<option value="">미평가</option>' + ''.join(f'<option value="{n}">{n}점</option>' for n in range(1, 6))
                favorite = '<label><input type="checkbox" data-favorite> 가장 나은 후보</label>' if public["favorite"] else ''
                controls = f'<div class="rating-controls" hidden><label>점수 <select data-score>{options}</select></label><label>메모 <textarea data-note rows="2"></textarea></label>{favorite}</div>'
            if mode == "versus":
                preview = f' data-html-src="{html.escape(html_src, quote=True)}"' if html_src else ''
                content = f'<div class="sample-content" tabindex="0" aria-label="{card["label"]} 내용"{preview}>' + content + '</div><div class="sample-choice"></div>'
            cards.append(f'<article class="sample" data-item="{item["id"]}" data-candidate="{card["candidate"]}" data-fingerprint="{card["fingerprint"]}"><h3>{card["label"]}<span class="identity"></span></h3>{content}{controls}</article>')
        title = html.escape(item.get("title", f"항목 {number}"))
        script = '<p class="shared-script">' + html.escape(item["script"]) + '</p>' if "script" in item else ''
        context = (f'<div class="item-context" role="region" aria-labelledby="context-{number:04d}" tabindex="0">'
                   f'<p class="comparison-topic">{html.escape(public["title"])}</p><h2 id="context-{number:04d}">{title}</h2>'
                   f'{script}<p>{html.escape(item["description"])}</p></div>')
        failures = ''
        if mode == "versus":
            failed_cards = [card for card in item["cards"] if card["failed"]]
            failures = ('<details class="versus-failures"><summary>생성 실패 ' + str(len(failed_cards)) + '개</summary><ul>' + ''.join('<li>' + html.escape(card["label"]) + ': 생성 실패</li>' for card in failed_cards) + '</ul></details>') if failed_cards else ''
        if mode == "versus":
            grid = '<div class="versus-stage"><div class="sample-grid">' + ''.join(cards) + '</div><span class="versus-mark" aria-hidden="true">VS</span></div>'
        else:
            grid = '<div class="sample-grid">' + ''.join(cards) + '</div>'
        sections.append(f'<section id="item-{number:04d}">{context}' + grid + failures + '</section>')
    template = (PACKAGE / 'assets/gallery.html').read_text(encoding="utf-8")
    if external_key or mode == "versus":
        template = template.replace('<script>const answerCode = "@@ANSWER@@";</script>', '<script>let answerCode = ""; const embeddedAnswerKeyCode = "@@EMBEDDED_KEY@@";</script><script>@@KEY_JS@@</script>')
        disabled = ' disabled' if external_key and mode != 'versus' else ''
        template = template.replace('<button id="reveal"', '<button id="load-key" type="button">정답표 선택</button><input id="key-file" type="file" accept="application/json,.json" hidden><button id="reveal"' + disabled)
    if mode == "versus":
        template = template.replace('<div id="summary" class="summary-scroll"', '<div id="summary" class="summary-scroll" tabindex="0" role="region" aria-label="비교 결과표"')
        template = template.replace('각 항목의 후보를 비교하고 1-5점과 메모를 남겨 주세요. 라벨은 항목마다 달라집니다.', '두 표본을 비교하고 한쪽 또는 양쪽을 진출시켜 주세요. 스타일로 기법을 짐작할 수 있습니다.')
        template = template.replace('<div id="summary"', '<div id="versus-progress" role="status" aria-live="polite"></div><div id="versus-controls" class="versus-actions" hidden><button id="choose-left" type="button">이 설명 선택</button><button id="choose-right" type="button">이 설명 선택</button><button id="bye" type="button" hidden>다음 라운드로</button><button id="choose-both" type="button">둘 다 진출</button><button id="undo" type="button">되돌리기</button></div><div id="versus-completion" hidden><p id="winner-message"></p><button id="result-copy" type="button">결과 복사</button><button id="result-reveal" type="button">결과 보기</button></div><div id="summary"')
        # Move maintenance tools out of the primary decision surface. Gallery markup stays unchanged.
        toolbar = re.search(r'<div id="toolbar".*?</div>', template, re.S)[0]
        template = template.replace(toolbar, '')
        footer = re.search(r'<footer>.*?</footer>', template, re.S)[0]
        template = template.replace(footer, '')
        help_start = template.index('<main>') + len('<main>')
        help_end = template.index('<p id="status"')
        help_text = template[help_start:help_end]
        navigation = '<div class="gallery-toolbar"><button id="previous-item" type="button">이전 항목</button><button id="next-item" type="button">다음 항목</button><button id="co-winners" type="button">남은 후보 공동 1위</button></div>'
        template = template[:help_start] + '<details class="versus-management"><summary>관리</summary>' + toolbar + navigation + help_text + footer + '</details>' + template[help_end:]
        template = template.replace('</style></head>', (PACKAGE / 'assets/versus.css').read_text(encoding='utf-8') + '\n</style></head>')
        template = template.replace('점수·메모·저장·결과 공개', '대결·저장·결과 공개').replace('평가 복사', '선택 복사').replace('평가 JSON', '선택 JSON')
    theme_attr = f'data-default-theme="{theme}"' + (f' data-theme="{theme}"' if theme != 'system' else '')
    values = {"THEME_ATTR": theme_attr, "TITLE": html.escape(public["title"]),
              "VERSION": html.escape(public["version"]), "COUNT": str(public["candidate_count"]),
              "TRANSFORMS": ''.join('<li>' + html.escape(x) + '</li>' for x in public['transformations']),
              "SECTIONS": ''.join(sections), "DATA": safe_json(public),
              "KEY_JS": (PACKAGE / "assets/key-loader.js").read_text(encoding="utf-8") if external_key or mode == "versus" else "",
              "EMBEDDED_KEY": base64.b64encode(json.dumps({"schema": 1, "study": key["study"], "version": key["version"],
                  "comparison": key.get("comparison"), "candidates": {token: {"name": row["name"]} for token, row in key["candidates"].items()},
                  "outputs": [{field: row[field] for field in ("item", "candidate", "fingerprint", "failed")} for row in key["outputs"]]}, ensure_ascii=False).encode()).decode() if mode == "versus" and not external_key else "",
              "ANSWER": "" if external_key or mode == "versus" else base64.b64encode(json.dumps({"candidates": key["candidates"]}, ensure_ascii=False).encode()).decode(),
              "CSS": (writing / 'assets/html-theme.css').read_text(encoding='utf-8'),
              "THEME_JS": (writing / 'assets/html-theme.js').read_text(encoding='utf-8'),
              "APP_JS": (PACKAGE / ('assets/versus.js' if mode == 'versus' else 'assets/gallery.js')).read_text(encoding='utf-8')}
    return re.sub(r'@@([A-Z_]+)@@', lambda match: values[match[1]], template)


def build(manifest_path, output, previous_key=None, theme="system", mode="gallery", delivery="single", answer_key=None):
    require(mode in {"gallery", "versus"} and delivery in {"single", "split"}, "invalid mode/delivery")
    require(theme in {"system", "light", "dark"}, "invalid theme")
    require(answer_key in {None, "embedded", "separate"}, "invalid answer key delivery")
    require(not (delivery == "split" and answer_key == "embedded"), "split delivery requires a separate answer key")
    external_key = delivery == "split" or answer_key == "separate"
    source = Path(manifest_path).resolve()
    public, key, files, inputs = prepare(read_json(source), source, read_json(previous_key) if previous_key else None, mode)
    if previous_key:
        inputs.append(previous_key)
    if mode == "versus":
        public["mode"] = mode
        roster = [{"id": item["id"], "cards": [{field: card[field] for field in ("candidate", "fingerprint", "failed")} for card in item["cards"]]} for item in public["items"]]
        public["revision"] = hashlib.sha256(json.dumps([public["study"], public["version"], public["title"], public["transformations"], [{k: v for k, v in item.items() if k != "cards"} for item in public["items"]], roster], sort_keys=True).encode()).hexdigest()
        key["comparison"] = {"revision": public["revision"], "items": roster}
    if delivery == "split":
        media_files = {name.rsplit(".", 1)[0]: name for name, _ in files}
        for i, item in enumerate(public["items"], 1):
            for slot, card in enumerate(item["cards"], 1):
                if "src" in card:
                    card["src"] = "assets/" + media_files[f"item-{i:04d}-slot-{slot:04d}"]
                if "display_file" in card:
                    card["display_file"] = "assets/" + card["display_file"]
                if "html_src" in card:
                    card["html_src"] = "assets/" + card["html_src"]
                for link in card.get("links", []):
                    link["href"] = "assets/" + link["href"]
    rendered = render(public, key, theme, mode, external_key)
    dest = destination(output, inputs)
    asset_dir = dest / 'assets' if delivery == "split" else dest
    if delivery == "split":
        asset_dir.mkdir()
    for filename, data in files:
        (asset_dir / filename).write_bytes(data)
    (dest / 'answer-key.json').write_text(json.dumps(key, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    page_name = 'index.html' if delivery == "split" else 'gallery.html'
    (dest / page_name).write_text(rendered, encoding='utf-8')
    if delivery == "split":
        with zipfile.ZipFile(dest / 'comparison.zip', 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            archive.write(dest / page_name, page_name)
            for filename, _ in files:
                archive.write(asset_dir / filename, 'assets/' + filename)
    return public, key


def replay_versus(item, events):
    require(isinstance(events, list) and len(events) <= 100000, "invalid versus events")
    survivors = [card["candidate"] for card in item["cards"] if not card["failed"]]
    incomparable = len(survivors) < 2
    round_number, cursor, next_round, done, seen = 1, 0, [], False, set()
    for event in events:
        require(not done and not incomparable, "events after completion")
        if event == "co-winners":
            require(round_number > 1 and cursor == 0 and all(c in seen for c in survivors), "early co-winners")
            done = True
            continue
        pair = survivors[cursor:cursor + 2]
        require(event in ("left", "right", "both") and (len(pair) == 2 or event == "left"), "invalid versus choice")
        seen.update(pair)
        next_round.extend(pair if event == "both" else [pair[0 if event == "left" else 1]])
        cursor += len(pair)
        if cursor == len(survivors):
            survivors, next_round, cursor = next_round, [], 0
            done = len(survivors) == 1
            if not done:
                round_number += 1
    return {"status": "incomparable" if incomparable else "complete" if done else "pending",
            "round": round_number, "winners": survivors if done else []}


def summarize_versus(payload, key, blind=False):
    require(type(payload.get("schema")) is int, "invalid versus schema")
    comparison = key.get("comparison")
    require(isinstance(comparison, dict) and payload.get("revision") == comparison["revision"], "versus revision mismatch")
    expected = comparison["items"]
    require(type(payload.get("active")) is int and 0 <= payload["active"] < len(expected), "invalid active item")
    imported = payload.get("items")
    require(isinstance(imported, list) and len(imported) == len(expected), "invalid versus items")
    identities = ({token: {"id": token, "name": f"후보 {i:03d}"}
                   for i, token in enumerate(sorted(key["candidates"]), 1)} if blind else key["candidates"])
    outputs = {row["item"]: row["item_id"] for row in key["outputs"]}
    item_rows = []
    counts = {"items": len(expected), "complete": 0, "pending": 0, "incomparable": 0,
              "failures": sum(row["failed"] for row in key["outputs"]), "outputs": len(key["outputs"])}
    wins = {candidate: 0 for candidate in identities}
    co_wins = dict(wins)
    for item, supplied in zip(expected, imported):
        require(isinstance(supplied, dict) and supplied.get("id") == item["id"] and supplied.get("cards") == item["cards"], "unknown/stale versus output")
        require(all(isinstance(card, dict) and set(card) == {"candidate", "fingerprint", "failed"} and type(card.get("failed")) is bool for card in supplied["cards"]), "invalid versus roster")
        result = replay_versus(item, supplied.get("events"))
        counts[result["status"]] += 1
        for winner in result["winners"]:
            wins[winner] += 1
            co_wins[winner] += len(result["winners"]) > 1
        item_rows.append({"item_id": item["id"] if blind else outputs[item["id"]], **result,
                          "winners": [identities[token]["id"] for token in result["winners"]],
                          "winner_names": [identities[token]["name"] for token in result["winners"]],
                          "failures": sum(card["failed"] for card in item["cards"]), "events": supplied["events"]})
    candidates = [{"id": identity["id"], "name": identity["name"], "wins": wins[token], "co_wins": co_wins[token],
                   "failures": sum(row["failed"] for row in key["outputs"] if row["candidate"] == token)} for token, identity in identities.items()]
    return {"schema": 1, "mode": "versus", "study_id": key["study"] if blind else key["study_id"],
            "version": key["version"], "revision": comparison["revision"], "evaluators": 1, "blind": blind,
            "revealed": payload["revealed"], "totals": counts, "candidates": candidates, "items": item_rows,
            "limitations": "평가자는 1명입니다. 선정은 사람의 선택 기록이며, 생성 실패와 비교 불가를 품질 순위로 바꾸지 않습니다."}


def summarize(ratings, key, blind=False):
    require(isinstance(ratings, dict) and ratings.get("schema") == 1, "invalid rating schema")
    require(ratings.get("study") == key["study"] and ratings.get("version") == key["version"], "rating study/revision mismatch")
    text(ratings.get("evaluator"))
    require(type(ratings.get("revealed")) is bool, "invalid reveal state")
    if ratings.get("mode") == "versus":
        return summarize_versus(ratings, key, blind)
    require("mode" not in ratings or ratings["mode"] == "gallery", "invalid comparison mode")
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
    identities = ({token: {'id': token, 'name': f'후보 {i:03d}'}
                   for i, token in enumerate(sorted(key['candidates']), 1)} if blind else key['candidates'])
    for token, identity in identities.items():
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
            item_rows.append({'item_id': output['item'] if blind else output['item_id'], 'candidate_id': identity['id'],
                              'candidate_name': identity['name'], 'failed': output['failed'],
                              **{k: rating[k] for k in ('score', 'note', 'favorite')}})
        candidates.append({'id': identity['id'], 'name': identity['name'], 'mean': sum(values) / len(values) if values else None,
                           'rated': len(values), 'missing': missing, 'failures': failures, 'favorites': wins})
    totals = {field: sum(row[field] for row in candidates) for field in ('rated', 'missing', 'failures')}
    totals['total'] = len(lookup)
    require(totals['rated'] + totals['missing'] + totals['failures'] == totals['total'], 'rating coverage mismatch')
    return {'schema': 1, 'study_id': key['study'] if blind else key['study_id'], 'version': key['version'], 'evaluators': 1,
            'blind': blind, 'totals': totals,
            'revealed': ratings['revealed'], 'candidates': candidates, 'items': item_rows,
            'limitations': '평가자는 1명입니다. 미평가와 생성 실패는 평균에서 제외하며 항목별 표본 수와 평가 범위가 다를 수 있습니다.'}


def markdown(summary):
    def cell(value):
        return html.escape(str(value)).replace('|', '\\|').replace('\n', '<br>').replace('\r', '')
    if summary.get("mode") == "versus":
        lines = ['# 블라인드 대결 결과', '', summary['limitations'], f"결과 공개 이력: {summary['revealed']}",
                 '', '| 항목 | 상태 | 선정 · 공동 1위 | 생성 실패 |', '|---|---|---|---:|']
        for row in summary['items']:
            lines.append('| ' + ' | '.join(cell(value) for value in (row['item_id'], row['status'], ', '.join(row['winner_names']) or '미선정', row['failures'])) + ' |')
        return '\n'.join(lines) + '\n'
    lines = ['# 블라인드 비교 결과', '', '평가자는 1명입니다. 미평가와 생성 실패는 평균에서 제외했습니다. 통계적 우열을 입증하지 않습니다.',
             f'결과 공개 이력: {summary["revealed"]}', '', '| 후보 | 평균 | 평가 수 | 미평가 | 생성 실패 | 최선 선택 |', '|---|---:|---:|---:|---:|---:|']
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
    b.add_argument('--mode', choices=('gallery', 'versus'), default='gallery')
    b.add_argument('--delivery', choices=('single', 'split'), default='single')
    b.add_argument('--answer-key', choices=('embedded', 'separate'), help='single defaults to embedded; split keeps a separate key')
    s = commands.add_parser('summarize')
    s.add_argument('ratings', help='rating JSON path, or - for stdin'); s.add_argument('--key', required=True)
    s.add_argument('--output', help='new directory for summary files; omit to print JSON without saving')
    s.add_argument('--blind', action='store_true', help='keep study, item and candidate identities hidden')
    args = parser.parse_args()
    try:
        if args.command == 'build':
            build(args.manifest, args.output, args.previous_key, args.theme, args.mode, args.delivery, args.answer_key)
        else:
            summary = summarize(read_json(args.ratings), read_json(args.key), blind=args.blind)
            if args.output:
                dest = destination(args.output, [args.key] + ([] if args.ratings == '-' else [args.ratings]))
                (dest / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
                (dest / 'summary.md').write_text(markdown(summary), encoding='utf-8')
            else:
                print(json.dumps(summary, ensure_ascii=False, indent=2))
    except SharedOwnerError as error:
        parser.exit(2, str(error) + '\n')
    except (ValueError, KeyError, TypeError, OSError):
        parser.exit(2, 'Invalid comparison input or unsafe output; preserve inputs and check the manifest contract.\n')


if __name__ == '__main__':
    main()
