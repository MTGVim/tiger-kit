#!/usr/bin/env python3
"""Render report content into the package's checked offline HTML shell."""

import argparse
import html
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import urlparse

from package_html import package


PACKAGE = Path(__file__).resolve().parents[1]
TEMPLATE = PACKAGE / "assets" / "report.html"
SECTION_START = "<!-- tigerkit:generated-sections:start -->"
SECTION_END = "<!-- tigerkit:generated-sections:end -->"
TOC_START = "<!-- tigerkit:generated-toc:start -->"
TOC_END = "<!-- tigerkit:generated-toc:end -->"
EXTRA_CSS = re.compile(
    r"<!-- tigerkit:extra-css -->.*?<!-- /tigerkit:extra-css -->", re.DOTALL
)
ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")
REF_PATTERN = re.compile(r"^ref-[a-z0-9]+(?:-[a-z0-9]+)*$")
CITE_PATTERN = re.compile(r"^cite-[a-z0-9]+(?:-[a-z0-9]+)*$")


class InputError(ValueError):
    pass


def required_text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{field} must be a non-empty string")
    return value.strip()


def escape(value):
    return html.escape(value, quote=True)


def validate_payload(payload):
    if not isinstance(payload, dict):
        raise InputError("report content must be a JSON object")
    title = required_text(payload.get("title"), "title")
    topbar_title = required_text(payload.get("topbar_title", title), "topbar_title")
    meta = required_text(payload.get("meta"), "meta")
    extra_css = payload.get("extra_css", "")
    if not isinstance(extra_css, str):
        raise InputError("extra_css must be a string")
    if re.search(r"</\s*style", extra_css, re.IGNORECASE):
        raise InputError("extra_css must not close its style element")

    sections = payload.get("sections")
    if not isinstance(sections, list) or not sections:
        raise InputError("sections must be a non-empty array")
    normalized_sections = []
    section_ids = set()
    for index, item in enumerate(sections, 1):
        if not isinstance(item, dict):
            raise InputError(f"sections[{index - 1}] must be an object")
        identifier = required_text(item.get("id"), f"sections[{index - 1}].id")
        if not ID_PATTERN.fullmatch(identifier) or identifier == "sources":
            raise InputError(f"invalid or reserved section id: {identifier!r}")
        if identifier in section_ids:
            raise InputError(f"duplicate section id: {identifier}")
        section_ids.add(identifier)
        section_title = required_text(item.get("title"), f"sections[{index - 1}].title")
        content = required_text(item.get("html"), f"sections[{index - 1}].html")
        normalized_sections.append((identifier, section_title, content))
    if "overview" not in section_ids:
        raise InputError("sections must include id 'overview'")
    if "verification" not in section_ids:
        raise InputError("sections must include id 'verification'")

    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        raise InputError("sources must be a non-empty array")
    normalized_sources = []
    source_ids = set()
    cite_ids = set()
    for index, item in enumerate(sources, 1):
        if not isinstance(item, dict):
            raise InputError(f"sources[{index - 1}] must be an object")
        identifier = required_text(item.get("id"), f"sources[{index - 1}].id")
        if not REF_PATTERN.fullmatch(identifier) or identifier in section_ids:
            raise InputError(f"invalid or duplicate reference id: {identifier!r}")
        if identifier in source_ids:
            raise InputError(f"duplicate reference id: {identifier}")
        source_ids.add(identifier)
        source_title = required_text(item.get("title"), f"sources[{index - 1}].title")
        url = item.get("url", "")
        local_path = item.get("local_path", "")
        date = item.get("date", "")
        revision = item.get("revision", "")
        unavailable = item.get("link_unavailable", False)
        citations = item.get("citations")
        for name, value in (("url", url), ("local_path", local_path), ("date", date), ("revision", revision)):
            if not isinstance(value, str):
                raise InputError(f"sources[{index - 1}].{name} must be a string")
        if url:
            parsed = urlparse(url)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                raise InputError(f"source URL must be HTTP(S): {url!r}")
        if not isinstance(unavailable, bool):
            raise InputError(f"sources[{index - 1}].link_unavailable must be boolean")
        if not isinstance(citations, list) or not citations:
            raise InputError(f"sources[{index - 1}].citations must be a non-empty array")
        normalized_citations = []
        for citation in citations:
            citation_id = required_text(citation, f"sources[{index - 1}].citations[]")
            if not CITE_PATTERN.fullmatch(citation_id):
                raise InputError(f"invalid citation id: {citation_id!r}")
            if citation_id in cite_ids:
                raise InputError(f"citation id appears more than once: {citation_id}")
            cite_ids.add(citation_id)
            normalized_citations.append(citation_id)
        normalized_sources.append({
            "id": identifier,
            "title": source_title,
            "url": url,
            "local_path": local_path.strip(),
            "date": date.strip(),
            "revision": revision.strip(),
            "link_unavailable": unavailable,
            "citations": normalized_citations,
        })
    return {
        "title": title,
        "topbar_title": topbar_title,
        "meta": meta,
        "extra_css": extra_css,
        "sections": normalized_sections,
        "sources": normalized_sources,
    }


def render_sections(sections, sources):
    rendered = []
    toc = []
    for identifier, title, content in sections:
        rendered.append(
            f'<section id="{escape(identifier)}"><h2>{escape(title)}</h2>\n{content}\n</section>'
        )
        toc.append(f'<li><a href="#{escape(identifier)}">{escape(title)}</a></li>')

    source_entries = []
    for source in sources:
        title = escape(source["title"])
        if source["url"]:
            title = f'<a href="{escape(source["url"])}">{title}</a>'
        details = []
        if source["local_path"]:
            details.append(f'<code>{escape(source["local_path"])}</code>')
        if source["date"]:
            details.append(escape(source["date"]))
        if source["revision"]:
            details.append(f'revision {escape(source["revision"])}')
        if source["link_unavailable"]:
            details.append("링크 없음")
        suffix = " · ".join(details)
        backlinks = " ".join(
            f'<a href="#{escape(citation_id)}" aria-label="인용 {index}의 위치로 복귀">↩ {index}</a>'
            for index, citation_id in enumerate(source["citations"], 1)
        )
        source_entries.append(
            f'<li id="{escape(source["id"])}">{title}'
            f'{f" · {suffix}" if suffix else ""} {backlinks}</li>'
        )
    rendered.append(
        '<section id="sources"><h2>참고문헌</h2>\n<ol>\n'
        + "\n".join(source_entries)
        + "\n</ol></section>"
    )
    toc.append('<li><a href="#sources">참고문헌</a></li>')
    return "\n".join(rendered), "\n".join(toc)


def resolve_theme(explicit):
    config_home_value = os.environ.get("XDG_CONFIG_HOME")
    config_home = Path(config_home_value) if config_home_value else Path.home() / ".config"
    settings_path = config_home / "tigerkit" / "settings.json"
    warnings = []
    theme = "system"
    if not settings_path.exists():
        try:
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            settings_path.write_text('{"html":{"theme":"system"}}\n', encoding="utf-8")
            warnings.append(f"created default HTML theme settings at {settings_path}")
        except OSError as error:
            warnings.append(f"could not create default HTML theme settings ({error}); using system")
    else:
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
            if not isinstance(settings, dict):
                warnings.append(f"invalid HTML theme settings shape in {settings_path}; using system")
                settings = {}
            html_settings = settings.get("html")
            if "html" in settings and not isinstance(html_settings, dict):
                warnings.append(f"invalid HTML theme settings shape in {settings_path}; using system")
                html_settings = {}
            configured = html_settings.get("theme") if isinstance(html_settings, dict) else None
            if isinstance(configured, str) and configured in {"system", "light", "dark"}:
                theme = configured
            elif configured is not None and (not isinstance(configured, str) or configured.strip()):
                warnings.append(f"invalid HTML theme in {settings_path}; using system")
        except (OSError, json.JSONDecodeError, AttributeError, TypeError) as error:
            warnings.append(f"could not read HTML theme settings ({error}); using system")
    return explicit or theme, warnings


def render(template, payload, theme):
    sections_html, toc_html = render_sections(payload["sections"], payload["sources"])
    if template.count(SECTION_START) != 1 or template.count(SECTION_END) != 1:
        raise InputError("template generated-section markers are missing or duplicated")
    replacements = {
        "{{REPORT_TITLE}}": escape(payload["title"]),
        "{{REPORT_TOPBAR_TITLE}}": escape(payload["topbar_title"]),
        "{{REPORT_META}}": escape(payload["meta"]),
    }
    output = re.sub(
        r"\{\{REPORT_(?:TITLE|TOPBAR_TITLE|META)\}\}",
        lambda match: replacements[match.group(0)],
        template,
    )
    start = output.index(SECTION_START) + len(SECTION_START)
    end = output.index(SECTION_END)
    if end < start:
        raise InputError("template generated-section markers are out of order")
    output = output[:start] + "\n" + sections_html + "\n" + output[end:]
    if output.count(TOC_START) != 1 or output.count(TOC_END) != 1:
        raise InputError("template generated-TOC markers are missing or duplicated")
    toc_start = output.index(TOC_START) + len(TOC_START)
    toc_end = output.index(TOC_END)
    if toc_end < toc_start:
        raise InputError("template generated-TOC markers are out of order")
    output = output[:toc_start] + "\n" + toc_html + "\n" + output[toc_end:]
    css = f'<style>\n{payload["extra_css"]}\n</style>' if payload["extra_css"].strip() else ""
    output, css_matches = EXTRA_CSS.subn(
        lambda match: match.group(0).replace("{{REPORT_EXTRA_CSS}}", css), output, count=1
    )
    if css_matches != 1:
        raise InputError("template extra-CSS marker is missing or duplicated")
    root = re.search(r"<html\b([^>]*)>", output, re.IGNORECASE)
    if root is None or 'data-default-theme="system"' not in root.group(1):
        raise InputError("template must declare system theme as its placeholder")
    attributes = root.group(1).replace('data-default-theme="system"', f'data-default-theme="{theme}"')
    attributes = re.sub(r'\s+data-theme="(?:light|dark)"', "", attributes)
    if theme in {"light", "dark"}:
        attributes += f' data-theme="{theme}"'
    output = output[:root.start(1)] + attributes + output[root.end(1):]
    return output


def atomic_write(path, contents):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            temp_name = handle.name
            handle.write(contents)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="JSON report content file")
    parser.add_argument("--output", required=True, type=Path, help="destination HTML file")
    parser.add_argument("--theme", choices=("system", "light", "dark"), help="explicit theme override")
    args = parser.parse_args(argv)
    try:
        input_path = args.input.resolve()
        output_path = args.output.resolve()
        if output_path in {input_path, TEMPLATE.resolve()}:
            raise InputError("output must not overwrite the JSON input or the offline template")
        payload = validate_payload(json.loads(input_path.read_text(encoding="utf-8")))
        theme, warnings = resolve_theme(args.theme)
        source = TEMPLATE.read_text(encoding="utf-8")
        output = render(source, payload, theme)
        atomic_write(output_path, output)
        download_name = output_path.name if output_path.name.isascii() else 'document.html'
        package(output_path.parent, [output_path.name], download_name)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"FAIL {args.output}: {error}", file=sys.stderr)
        return 1
    for warning in warnings:
        print(f"WARN {warning}", file=sys.stderr)
    print(f"WROTE {args.output} (theme={theme})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
