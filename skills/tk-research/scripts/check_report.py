#!/usr/bin/env python3
"""Check the structural contract for an offline tk-research report."""

import argparse
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote


SHORT_REPORT_MAX_SECTIONS = 3
TEMPLATE_PATH = Path(__file__).resolve().parents[1] / "assets" / "report.html"
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}
AI_AUTHORSHIP = re.compile(
    r"본\s*보고서는\s*AI가\s*작성했습니다\.?"
    r"|This report (?:was (?:written|generated|created) with AI"
    r"|(?:is|was) AI-generated)\.?"
    r"|AI assistance was used to (?:write|prepare|create) this report\.?",
    re.IGNORECASE,
)
UNSAFE_SCHEME = re.compile(r"^\s*(?:javascript|vbscript|data|file):", re.IGNORECASE)
CSS_IMPORT = re.compile(r"@import\b", re.IGNORECASE)
CSS_URL = re.compile(r"url\(\s*([\"']?)(.*?)\1\s*\)", re.IGNORECASE | re.DOTALL)
CSS_IMAGE_SET = re.compile(r"(?:-webkit-)?image-set\s*\(", re.IGNORECASE)
CSS_ESCAPE = re.compile(r"\\([0-9a-fA-F]{1,6})\s?|\\([^\r\n0-9a-fA-F])")
SVG_URL_ATTRIBUTES = {
    "clip-path", "color-profile", "cursor", "fill", "filter", "marker",
    "marker-end", "marker-mid", "marker-start", "mask", "stroke",
}
NETWORK_SCRIPT = re.compile(
    r"\b(?:fetch|XMLHttpRequest|WebSocket|EventSource|sendBeacon)\b|"
    r"\bimport\s*\(",
    re.IGNORECASE,
)


class Element:
    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.parent = parent
        self.children = []

    def descendants(self):
        for child in self.children:
            if isinstance(child, Element):
                yield child
                yield from child.descendants()

    def text_content(self):
        return "".join(
            child.text_content() if isinstance(child, Element) else child
            for child in self.children
        )


class ReportParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Element("#document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        element = Element(tag.lower(), {
            name.lower(): value or "" for name, value in attrs
        }, parent=self.stack[-1])
        self.stack[-1].children.append(element)
        if tag.lower() not in VOID_ELEMENTS:
            self.stack.append(element)

    def handle_startendtag(self, tag, attrs):
        element = Element(tag.lower(), {
            name.lower(): value or "" for name, value in attrs
        }, parent=self.stack[-1])
        self.stack[-1].children.append(element)

    def handle_endtag(self, tag):
        tag = tag.lower()
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def class_tokens(element):
    return set(element.attrs.get("class", "").split())


def fragment_id(href):
    return unquote(href[1:]) if href.startswith("#") else None


def has_unsafe_scheme(value):
    normalized = re.sub(r"[\x00-\x20]+", "", value)
    return bool(UNSAFE_SCHEME.match(normalized))


def decode_css_escapes(css):
    def replace(match):
        if match.group(1):
            codepoint = int(match.group(1), 16)
            return chr(codepoint) if 0 < codepoint <= 0x10FFFF else "\ufffd"
        return match.group(2)

    return CSS_ESCAPE.sub(replace, css)


def inline_code_blocks(source, tags):
    parser = ReportParser()
    parser.feed(source)
    parser.close()
    return [
        (element.tag, tuple(sorted(element.attrs.items())), element.text_content())
        for element in parser.root.descendants()
        if element.tag in tags
    ]


def check_report(source, template_source):
    parser = ReportParser()
    parser.feed(source)
    parser.close()
    elements = list(parser.root.descendants())
    errors = []
    warnings = []

    template_styles = inline_code_blocks(template_source, {"style"})
    report_styles = inline_code_blocks(source, {"style"})
    template_scripts = inline_code_blocks(template_source, {"script"})
    report_scripts = inline_code_blocks(source, {"script"})
    if report_styles[:len(template_styles)] != template_styles:
        errors.append("the complete offline template styles must be preserved before optional inline styles")
    if report_scripts != template_scripts:
        errors.append("runtime inline scripts must match the offline template exactly")

    titles = [element for element in elements if element.tag == "title"]
    if len(titles) != 1 or not titles[0].text_content().strip():
        errors.append("report must have exactly one non-empty title")
    html_roots = [element for element in elements if element.tag == "html"]
    if len(html_roots) != 1:
        errors.append("report must have exactly one html root")
    else:
        root_attrs = html_roots[0].attrs
        default_theme = root_attrs.get("data-default-theme")
        if default_theme not in {"system", "light", "dark"}:
            errors.append("html root needs a valid data-default-theme")
        if default_theme in {"light", "dark"} and root_attrs.get("data-theme") != default_theme:
            errors.append("explicit light/dark default must also set data-theme for first paint")
        if default_theme == "system" and "data-theme" in root_attrs:
            errors.append("system default must omit data-theme")

    ids_by_value = defaultdict(list)
    for element in elements:
        identifier = element.attrs.get("id")
        if identifier is not None:
            ids_by_value[identifier].append(element)

    for identifier, matches in ids_by_value.items():
        if len(matches) > 1:
            errors.append(f"duplicate id {identifier!r} appears {len(matches)} times")

    if any("data-html-mode" in element.attrs for element in elements):
        errors.append("reports must use one continuous document without presentation modes")
    if any("ht-mode-control" in class_tokens(element) for element in elements) or any(
        element.attrs.get("name") == "ht-mode" for element in elements
    ):
        errors.append("reports must not include a document mode selector")
    theme_controls = [
        element for element in elements
        if element.tag == "fieldset" and "ht-theme-control" in class_tokens(element)
    ]
    theme_inputs = [
        element for element in elements
        if element.tag == "input" and element.attrs.get("name") == "ht-theme"
    ]
    if len(theme_controls) != 1 or "data-ht-theme-control" not in theme_controls[0].attrs:
        errors.append("report must retain one functional shared theme control")
    if [element.attrs.get("value") for element in theme_inputs] != ["system", "light", "dark"]:
        errors.append("theme control must offer system, light, and dark in order")
    theme_options = [element for element in elements if "ht-theme-option" in class_tokens(element)]
    for option in theme_options:
        children = [child for child in option.children if isinstance(child, Element)]
        valid = (
            option.tag == "label" and len(children) == 2
            and children[0] in theme_inputs
            and children[0].attrs.get("type") == "radio"
            and children[1].tag == "span" and children[1].text_content().strip()
            and len(theme_controls) == 1 and option in list(theme_controls[0].descendants())
        )
        if not valid:
            errors.append("each ht-theme-option needs a radio input immediately followed by a non-empty span")
    if len(theme_options) != 3 or any(
        input_element.parent not in theme_options for input_element in theme_inputs
    ):
        errors.append("all theme inputs must use ht-theme-option labels with input + span")
    for element in elements:
        if element.tag == "details":
            children = [child for child in element.children if isinstance(child, Element) or child.strip()]
            if not children or not isinstance(children[0], Element) or children[0].tag != "summary":
                errors.append("every details element must start with a summary")

    for element in elements:
        href_attributes = [
            name for name in element.attrs
            if name == "href" or name.endswith(":href")
        ]
        for attribute in href_attributes + ["src"]:
            value = element.attrs.get(attribute, "")
            if value and has_unsafe_scheme(value):
                errors.append(
                    f"unsafe URL scheme in {element.tag}[{attribute}={value!r}]"
                )
            if attribute in href_attributes and value.startswith("#"):
                target_id = fragment_id(value)
                matches = ids_by_value.get(target_id, [])
                if not target_id or len(matches) != 1:
                    errors.append(
                        f"fragment link {value!r} resolves to {len(matches)} IDs"
                    )
            elif attribute in href_attributes and value and element.tag != "a":
                errors.append(
                    f"runtime non-link resource href is not allowed on <{element.tag}>"
                )

        rel_tokens = set(element.attrs.get("rel", "").lower().split())
        resource_attributes = {
            "src", "srcset", "poster", "background", "manifest", "ping"
        } & element.attrs.keys()
        if resource_attributes:
            errors.append(
                f"runtime network resource attributes are not allowed on <{element.tag}>"
            )
        if element.tag == "link" and "stylesheet" in rel_tokens and "href" in element.attrs:
            errors.append("runtime network stylesheet links are not allowed")
        if element.tag in {"iframe", "object", "embed"} or "srcdoc" in element.attrs:
            errors.append("embedded runtime content is not allowed")
        if element.tag == "object" and "data" in element.attrs:
            errors.append("runtime network object data is not allowed")
        if element.tag == "meta" and element.attrs.get("http-equiv", "").lower() == "refresh":
            errors.append("runtime meta refresh is not allowed")
        if element.tag == "form" or "action" in element.attrs or "formaction" in element.attrs:
            errors.append("runtime form network submissions are not allowed")
        if any(name.startswith("on") for name in element.attrs):
            errors.append("runtime inline event handlers are not allowed")

        css = element.attrs.get("style", "")
        if element.tag == "style":
            css += element.text_content()
        css = decode_css_escapes(css)
        if CSS_IMPORT.search(css) or CSS_IMAGE_SET.search(css) or any(
            target.strip() and not target.strip().startswith("#")
            for _, target in CSS_URL.findall(css)
        ):
            errors.append("runtime network CSS references are not allowed")
        for name in SVG_URL_ATTRIBUTES & element.attrs.keys():
            svg_value = decode_css_escapes(element.attrs[name])
            if any(
                target.strip() and not target.strip().startswith("#")
                for _, target in CSS_URL.findall(svg_value)
            ):
                errors.append(
                    f"runtime network SVG reference is not allowed in {element.tag}[{name}]"
                )
        if element.tag == "script" and NETWORK_SCRIPT.search(element.text_content()):
            errors.append("runtime network JavaScript APIs are not allowed")

    sections = [element for element in elements if element.tag == "section"]
    navigators = [
        element for element in elements if "ht-doc-nav" in class_tokens(element)
    ]
    controls = [
        element for element in elements if "ht-doc-controls" in class_tokens(element)
    ]
    overview = next(
        (section for section in sections if section.attrs.get("id") == "overview"),
        None,
    )
    if overview is None or len(overview.text_content().strip()) < 20:
        errors.append("the report needs a substantive conclusion in #overview")

    if bool(navigators) != bool(controls):
        errors.append("document navigation must include both .ht-doc-nav and .ht-doc-controls")
    elif len(navigators) > 1 or len(controls) > 1:
        errors.append("document navigation must contain one .ht-doc-nav and one .ht-doc-controls")
    elif len(sections) > SHORT_REPORT_MAX_SECTIONS and not navigators:
        errors.append(
            "document navigation is required for reports with more than "
            f"{SHORT_REPORT_MAX_SECTIONS} sections"
        )
    elif navigators and controls:
        if any(not element.attrs.get("id") for element in sections):
            errors.append("every section needs an id when document navigation is present")
        section_ids = {
            element.attrs["id"] for element in sections if element.attrs.get("id")
        }
        toc_ids = {
            fragment_id(element.attrs["href"])
            for element in navigators[0].descendants()
            if element.tag == "a" and element.attrs.get("href", "").startswith("#")
        }
        missing_toc_ids = section_ids - toc_ids
        if missing_toc_ids:
            errors.append(
                ".ht-doc-nav table of contents is missing section links: "
                + ", ".join(sorted(missing_toc_ids))
            )

        for link in navigators[0].descendants():
            if link.tag != "a" or not link.attrs.get("href", "").startswith("#"):
                continue
            matches = ids_by_value.get(fragment_id(link.attrs["href"]), [])
            if len(matches) != 1:
                continue  # The fragment check already reports invalid targets.
            target = matches[0]
            heading = target if re.fullmatch(r"h[1-6]", target.tag) else next(
                (child for child in target.children
                 if isinstance(child, Element) and re.fullmatch(r"h[1-6]", child.tag)), None,
            )
            heading_text = " ".join(heading.text_content().split()) if heading else ""
            if not heading_text or heading_text not in " ".join(link.text_content().split()):
                errors.append(f"TOC link {link.attrs['href']!r} must contain its target heading's full text")

        movement_ids = {
            fragment_id(element.attrs["href"])
            for element in controls[0].descendants()
            if element.tag == "a" and element.attrs.get("href", "").startswith("#")
        }
        missing_movement_ids = {"document-top", "document-bottom"} - movement_ids
        if missing_movement_ids:
            errors.append(
                ".ht-doc-controls must link to both top and bottom "
                "(#document-top and #document-bottom)"
            )

    references = {
        element.attrs["id"]: element for element in elements
        if element.tag == "li" and element.attrs.get("id", "").startswith("ref-")
    }
    citations = [
        element for element in elements
        if element.tag == "sup" and element.attrs.get("id", "").startswith("cite-")
    ]
    citation_targets = defaultdict(set)
    for citation in citations:
        citation_id = citation.attrs["id"]
        citation_links = [
            element for element in citation.descendants()
            if element.tag == "a" and element.attrs.get("href", "").startswith("#")
        ]
        target_ids = [fragment_id(link.attrs["href"]) for link in citation_links]
        if len(target_ids) != 1:
            errors.append(
                f"citation #{citation_id} must link to exactly one reference entry"
            )
            continue
        target_id = target_ids[0]
        matches = ids_by_value.get(target_id, [])
        if (
            not target_id.startswith("ref-")
            or len(matches) != 1
            or matches[0].tag != "li"
            or target_id not in references
        ):
            errors.append(
                f"citation #{citation_id} must point to an existing li[id^=\"ref-\"]"
            )
            continue
        citation_targets[target_id].add(citation_id)

    for reference_id, reference in references.items():
        has_source_url = any(
            element.tag == "a" and re.match(r"^https?://", element.attrs.get("href", ""), re.I)
            for element in [reference, *reference.descendants()]
        )
        def looks_like_local_path(value):
            value = value.strip()
            return bool(value) and (
                value.startswith((".", "/", "~"))
                or "/" in value
                or "\\" in value
                or re.fullmatch(r"[\w.-]+\.[A-Za-z0-9]{1,8}", value) is not None
            )

        has_local_path = any(
            element.tag == "code" and looks_like_local_path(element.text_content())
            for element in [reference, *reference.descendants()]
        )
        has_no_link_note = "링크 없음" in re.sub(r"\s+", " ", reference.text_content())
        if not (has_source_url or has_local_path or has_no_link_note):
            warnings.append(
                f'reference #{reference_id} has no source URL, local path, or explicit "링크 없음" note'
            )
        backlink_ids = {
            fragment_id(element.attrs["href"])
            for element in reference.descendants()
            if element.tag == "a"
            and element.attrs.get("href", "").startswith("#cite-")
        }
        expected_ids = citation_targets.get(reference_id, set())
        if not expected_ids:
            errors.append(f"reference #{reference_id} has no citation")
        missing = expected_ids - backlink_ids
        unexpected = backlink_ids - expected_ids
        if missing or unexpected:
            details = []
            if missing:
                details.append("missing " + ", ".join(sorted(missing)))
            if unexpected:
                details.append("unexpected " + ", ".join(sorted(unexpected)))
            errors.append(
                f"reference #{reference_id} backlink mismatch: {'; '.join(details)}"
            )

    if not any(
        element.tag == "footer" and AI_AUTHORSHIP.search(element.text_content())
        for element in elements
    ):
        errors.append("AI-authorship footer is missing")

    return errors, warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="path to the generated report HTML")
    args = parser.parse_args(argv)

    try:
        source = args.report.read_text(encoding="utf-8")
    except OSError as error:
        print(f"FAIL {args.report}: cannot read report ({error})", file=sys.stderr)
        return 2

    try:
        template_source = TEMPLATE_PATH.read_text(encoding="utf-8")
    except OSError as error:
        print(f"FAIL {TEMPLATE_PATH}: cannot read offline template ({error})", file=sys.stderr)
        return 2

    errors, warnings = check_report(source, template_source)
    if errors:
        for error in errors:
            print(f"FAIL {args.report}: {error}", file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"WARN {args.report}: {warning}", file=sys.stderr)
    print(f"PASS {args.report}: report structure, navigation, citations, footer and safe links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
