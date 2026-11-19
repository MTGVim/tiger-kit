#!/usr/bin/env python3
"""Check final report/gallery HTML. No installation or remote requests.

Without --browser, checks are static only. --browser requires an already
installed Python Playwright and Chromium. It serves a fixed allowlist through an
owned temporary loopback server and shuts it down before returning. Browser screenshots still require
human/visual inspection; this tool does not declare that inspection complete.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
import mimetypes
import posixpath
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
from pathlib import Path
import re
from urllib.parse import urlsplit, unquote

STUDIO_MARK = 'feedback-studio'


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.toc = 0
        self.ids = set()
        self.errors = []
        self.inert = 0
        self.studio = 0

    def handle_comment(self, data):
        if not self.inert and data.strip() == STUDIO_MARK:
            self.studio += 1

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'template':
            self.inert += 1
        if self.inert:
            return
        if tag == 'h1':
            self.h1 += 1
        if tag == 'nav' and 'toc' in attrs.get('class', '').split():
            self.toc += 1
        if attrs.get('id'):
            if attrs['id'] in self.ids:
                self.errors.append('duplicate id: ' + attrs['id'])
            self.ids.add(attrs['id'])
        if tag in ('img', 'script', 'iframe', 'video', 'audio', 'source', 'link'):
            value = attrs.get('src') or (attrs.get('href') if tag == 'link' else '')
            if value and (urlsplit(value).netloc or urlsplit(value).scheme in ('http', 'https')):
                self.errors.append('automatic remote resource: ' + value)

    def handle_endtag(self, tag):
        if tag == 'template' and self.inert:
            self.inert -= 1


def static_check(text, profile='report', require_studio=False):
    doc = Document()
    doc.feed(text)
    if doc.h1 != 1:
        doc.errors.append(f'expected one h1, found {doc.h1}')
    if profile == 'report' and doc.toc != 1:
        doc.errors.append(f'expected one report TOC, found {doc.toc}')
    if require_studio and doc.studio != 1:
        doc.errors.append(f'expected one real feedback-studio comment, found {doc.studio}')
    return doc.errors


RUNTIME = r'''() => {
  const errors = [], warnings = [];
  if (document.documentElement.scrollWidth > innerWidth + 1)
    errors.push('horizontal overflow');
  const elements = [...document.querySelectorAll('button,input:not([type=hidden]),select,textarea,summary,a[href]')];
  let checked = 0;
  for (const el of elements) {
    if (el.disabled || el.closest('[hidden],[inert]')) continue;
    let target = el;
    // A visually hidden native radio is operated through its visible label.
    if (el.matches('input[type=radio],input[type=checkbox]') && el.closest('label')) target = el.closest('label');
    const closed = target.closest('details:not([open])');
    if (closed && !closed.querySelector('summary')?.contains(target)) continue;
    const r = target.getBoundingClientRect(), s = getComputedStyle(target);
    if (!r.width || !r.height || s.visibility !== 'visible' || s.display === 'none' || r.top < 0 || r.bottom > innerHeight || r.left < 0 || r.right > innerWidth) continue;
    const hit = document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
    if (!hit || !(target === hit || target.contains(hit))) {
      // Opaque sticky chrome intentionally covers scrolling content beneath it.
      // Scroll that control into an unobscured viewport before deciding.
      if (hit && hit.closest('.rp-tools,.rp-bar,.toc') && !target.closest('.rp-bar')) {
        warnings.push('control underneath sticky chrome: '+(el.textContent || el.getAttribute('aria-label') || el.tagName).trim().slice(0,80));
      } else errors.push('covered control: '+(el.textContent || el.getAttribute('aria-label') || el.tagName).trim().slice(0,80));
    }
    checked++;
  }
  // Only validate the export icon after payload preparation has made it visible.
  for (const button of document.querySelectorAll('[data-ht-download]:not([hidden])')) {
    if (getComputedStyle(button).display === 'none') continue;
    const svg = button.querySelector('svg');
    if (!svg) { errors.push('visible download button has no SVG icon'); continue; }
    const rect = svg.getBoundingClientRect(), style = getComputedStyle(svg);
    if (rect.width <= 0 || rect.height <= 0 || style.visibility === 'hidden' || style.stroke === 'none' || style.strokeWidth === '0px')
      errors.push('visible download SVG has no rendered size or stroke');
  }
  const title = document.querySelector('h1');
  if (scrollY === 0 && title && title.getBoundingClientRect().top < 8) warnings.push('title top padding needs visual inspection');
  return {errors,warnings,checked,scrollY,width:innerWidth,height:innerHeight,background:getComputedStyle(document.body).backgroundColor};
}'''


def snapshot_resources(path):
    """Serve only this exact HTML and its declared automatic local assets."""
    root = path.parent.resolve(strict=True)
    resources = {'/entry.html': (path.read_bytes(), 'text/html; charset=utf-8')}
    class Resources(HTMLParser):
        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            value = attrs.get('src') or (attrs.get('href') if tag == 'link' else None)
            if not value:
                return
            url = urlsplit(value)
            if url.scheme or url.netloc or not url.path:
                return
            lexical = root / unquote(url.path)
            current = root
            for part in Path(unquote(url.path)).parts:
                current = current / part
                if current.is_symlink():
                    raise ValueError('browser assets must not use symlinks')
            target = lexical.resolve(strict=True)
            target.relative_to(root)
            key = '/' + target.relative_to(root).as_posix()
            resources[key] = (target.read_bytes(), mimetypes.guess_type(target.name)[0] or 'application/octet-stream')
    Resources().feed(path.read_text(encoding='utf-8'))
    return resources


def serve_snapshot(resources):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            key = posixpath.normpath(unquote(urlsplit(self.path).path))
            if key not in resources:
                self.send_error(404)
                return
            data, mime = resources[key]
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(data)
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f'http://127.0.0.1:{server.server_port}'


def browser_check(path, evidence, executable, widths, dom_only=False):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise RuntimeError('Python Playwright is unavailable; no packages were installed') from error
    evidence.mkdir(parents=True, exist_ok=True)
    results, network = [], []
    resources = snapshot_resources(path)
    if dom_only and len(resources) != 1:
        raise ValueError('--dom-only requires self-contained HTML; external local assets need a real page load')
    server, thread, origin = (None, None, None) if dom_only else serve_snapshot(resources)
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True, executable_path=executable)
            try:
                for width in widths:
                    context = browser.new_context(viewport={'width':width,'height':900}, reduced_motion='reduce')
                    page = context.new_page()
                    page_errors = []
                    page.on('pageerror', lambda e: page_errors.append(str(e)))
                    def intercept(route):
                        url = route.request.url
                        if url.startswith(('http:', 'https:')) and (origin is None or not url.startswith(origin + '/')):
                            network.append(url)
                            route.abort()
                        else:
                            route.continue_()
                    page.route('**/*', intercept)
                    if dom_only:
                        page.set_content(path.read_text(encoding='utf-8'))
                    else:
                        page.goto(origin + '/entry.html')
                    for theme in ('light','dark'):
                        control = page.locator(f'[data-ht-theme-control] input[value="{theme}"]')
                        # Reports must exercise their actual UI; galleries support OS theme.
                        if control.count():
                            control.locator('..').click()
                            if page.locator('html').get_attribute('data-theme') != theme:
                                raise RuntimeError('theme control did not change data-theme')
                        else:
                            page.emulate_media(color_scheme=theme)
                        page.wait_for_timeout(60)
                        for ratio in (0, .25, .5, .75, 1):
                            page.evaluate('(r) => scrollTo(0,(document.documentElement.scrollHeight-innerHeight)*r)', ratio)
                            page.wait_for_timeout(60)
                            row = page.evaluate(RUNTIME)
                            row.update({'theme':theme,'ratio':ratio,'page_errors':page_errors.copy()})
                            results.append(row)
                            if ratio in (0,.5,1) and width in (375,1440):
                                name = f'{path.stem}-{width}-{theme}-{ratio:g}.png'
                                page.screenshot(path=str(evidence/name), full_page=False)
                                row['screenshot'] = name
                    context.close()
            finally:
                browser.close()
    except Exception as error:
        raise RuntimeError('browser verification failed: ' + str(error)) from error
    finally:
        if server is not None:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
    return {'views':results,'blocked_network':sorted(set(network)),
            'visual_inspection':'not performed by this script',
            'delivery_transport':('DOM-only set_content; navigation and origin storage unverified' if dom_only else 'fixed-byte loopback snapshot; file:// policy was not tested')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('html', type=Path)
    parser.add_argument('--profile', choices=('report','gallery'), default='report')
    parser.add_argument('--require-feedback-studio', action='store_true')
    parser.add_argument('--browser', action='store_true')
    parser.add_argument('--dom-only', action='store_true', help='render known self-contained bytes without URL navigation; does not test origin storage or file delivery')
    parser.add_argument('--chromium', default='/usr/bin/chromium', help='existing Chromium executable')
    parser.add_argument('--evidence', type=Path)
    parser.add_argument('--widths', nargs='+', type=int, default=[375,1056,1100,1206,1216,1440])
    args = parser.parse_args()
    try:
        raw = args.html.read_bytes()
        result = {'path':str(args.html),'sha256':hashlib.sha256(raw).hexdigest(),
                  'static_errors':static_check(raw.decode('utf-8'), args.profile,args.require_feedback_studio),
                  'browser':'not run','studio_behavior':'not verified by marker check'}
        if args.browser:
            if args.evidence is None or any(w < 200 for w in args.widths):
                raise ValueError('--browser requires --evidence and widths >= 200')
            result['browser'] = browser_check(args.html,args.evidence,args.chromium,args.widths,args.dom_only)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        failure = bool(result['static_errors'])
        if isinstance(result['browser'], dict):
            failure |= bool(result['browser']['blocked_network']) or any(v['errors'] or v['page_errors'] for v in result['browser']['views'])
        return 1 if failure else 0
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(2,str(error)+'\n')


if __name__ == '__main__':
    raise SystemExit(main())
