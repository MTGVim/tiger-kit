#!/usr/bin/env python3
"""결정용 보고서 빌더: Markdown 원고 하나를 오프라인 HTML 한 장으로 만든다.

    build_page.py manuscript.md out.html [--figures DIR] [--css page.css] [--js page.js]
                                           [--lang ko] [--toc-label 목차] [--allow-missing-figures] [--no-download]

원고 문법
  # 제목                      첫 줄. 바로 다음 비어 있지 않은 줄은 부제(날짜, 작성자 등)
  ## 절 제목                  목차 항목이 된다. 제목 끝에 ` ~` 를 붙이면 조용한 절(한계, 부록)
  ## 절 제목 ~~               목차 항목 하나로 표시하며 본문을 접는 조용한 절(부록)
  ### 소제목                  소제목. 아래가 전부 `- 라벨: 내용` 줄이면 카드가 된다
                              카드 블록에는 `- 라벨: 내용` 줄만 둔다. 일반 문단을 섞으면 소제목이 된다
  ### [A1] 제목               카드 제목의 [..] 는 번호 배지. `### ~ 제목` 은 조용한 카드
  > 문단                      결론 콜아웃. 제목 바로 다음이 아니라 첫 `##` 절 안에 둔다
  | 표 |                      표. 구분 줄의 `---:` 는 오른쪽 정렬 숫자 열. 첫 칸이 `~ ` 로 시작하면 조용한 행
  - 항목 / 1. 항목            목록
  :::tiles                    `- 값 | 설명` 줄마다 숫자 타일
  :::decision                 안의 표나 문단을 결정 블록으로 감싼다
  :::note                     조용한 노트
  :::bars                     caption: 지표와 unit: 단위를 먼저 적고 `- 라벨 | 숫자 | quiet(선택)`을 씁니다.
                              비율처럼 기준이 따로 있으면 max: 100 을 더해 막대 길이를 그 기준에 맞춘다
  [[figure:이름]]             --figures 폴더의 이름.html 조각을 그 자리에 넣는다
  `코드` **굵게** [글](https://..)  인라인
"""
import argparse, html, math, os, re, sys, tempfile
from pathlib import Path
from html_controls import theme_assets

HERE = Path(__file__).resolve().parent


def asset(name):
    """같은 폴더에 있으면 그것을, 없으면 설치본의 ../assets 를 쓴다."""
    return str(HERE / name if (HERE / name).is_file() else HERE.parent / 'assets' / name)


def esc(s): return html.escape(str(s), quote=True)


def inline(s):
    # Code spans are protected before prose markup is applied.
    output = []
    for piece in re.split(r'(`[^`]+`)', s):
        if len(piece) >= 2 and piece.startswith('`') and piece.endswith('`'):
            output.append('<code>' + esc(piece[1:-1]) + '</code>')
            continue
        piece = esc(piece)
        piece = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', piece)
        piece = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+|#[\w-]+)\)',
                       r'<a href="\2">\1</a>', piece)
        output.append(piece)
    return ''.join(output)


# ---------- 블록 분해 ----------
FENCES = {'tiles', 'bars', 'decision', 'note'}


def split_blocks(text):
    """빈 줄로 나눈 문단 목록. `:::이름` 은 닫는 `:::` 까지 한 덩어리."""
    out, cur, lines = [], [], text.split('\n')
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.fullmatch(r':::(\w+)\s*', ln)
        if m:
            if cur: out.append(('p', '\n'.join(cur))); cur = []
            if m.group(1) not in FENCES: sys.exit(f'알 수 없는 블록 :::{m.group(1)}')
            j = i + 1
            while j < len(lines) and lines[j].strip() != ':::': j += 1
            if j == len(lines): sys.exit(f':::{m.group(1)} 를 닫는 ::: 가 없다')
            out.append((m.group(1), '\n'.join(lines[i + 1:j]))); i = j + 1; continue
        if ln.strip() == '':
            if cur: out.append(('p', '\n'.join(cur))); cur = []
        else: cur.append(ln)
        i += 1
    if cur: out.append(('p', '\n'.join(cur)))
    return out


def table(b):
    rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in b.splitlines()]
    if len(rows) < 3 or not all(re.fullmatch(r':?-{3,}:?', c) for c in rows[1]):
        sys.exit('표의 둘째 줄이 구분 줄이 아니다: ' + b.splitlines()[0])
    hdr, body, n = rows[0], rows[2:], len(rows[0])
    if len(rows[1]) != n:
        raise ValueError('table header and separator must have the same number of columns')
    num = [c.endswith(':') for c in rows[1]]
    cls = ' class="wide"' if n >= 3 else ''
    o = [f'<div class="scroll" tabindex="0" role="region" aria-label="{esc(hdr[0])} 표"><table{cls}><thead><tr>']
    o += [f'<th scope="col"{" class=num" if num[i] else ""}>{inline(h)}</th>' for i, h in enumerate(hdr)]
    o.append('</tr></thead><tbody>')
    for r in body:
        if len(r) != n: sys.exit(f'열 수가 다르다: {r}')
        quiet = r[0].startswith('~ ')
        if quiet: r[0] = r[0][2:]
        o.append('<tr class="quiet">' if quiet else '<tr>')
        for i, c in enumerate(r):
            if i == 0: o.append(f'<th scope="row">{inline(c)}</th>')
            else: o.append(f'<td{" class=num" if num[i] else ""}>{inline(c)}</td>')
        o.append('</tr>')
    return ''.join(o) + '</tbody></table></div>'


def bullets(b):
    lines = b.splitlines()
    if not lines or any(not line.startswith('- ') for line in lines):
        raise ValueError('every list item must start with "- "')
    return [line[2:] for line in lines]



class Ctx:
    figures = None
    missing_ok = False


def figure(name):
    if not re.fullmatch(r'[\w-]+', name):
        raise ValueError('invalid figure name')
    if Ctx.figures:
        source = Ctx.figures / f'{name}.html'
        if source.is_symlink():
            raise ValueError('figure symlinks are not accepted')
        if source.is_file():
            resolved_root = Ctx.figures.resolve(strict=True)
            if source.resolve(strict=True).parent != resolved_root:
                raise ValueError('figure escapes the selected directory')
            return source.read_text(encoding='utf-8')
    if Ctx.missing_ok:
        return f'<div class="slot" role="note">그림 자리: {esc(name)}</div>'
    raise ValueError(f'figure file not found: {name}.html')


def bars(block):
    """Require a named measure and unit; do not infer them from numeric values."""
    lines = block.splitlines()
    metadata = {}
    while lines and not lines[0].startswith('- '):
        key, separator, value = lines.pop(0).partition(':')
        if not separator or key not in ('caption', 'unit', 'max') or key in metadata or not value.strip():
            raise ValueError('bars take one caption:, one unit: and optional max: before the list')
        metadata[key] = value.strip()
    if not {'caption', 'unit'} <= set(metadata):
        raise ValueError('bars require explicit caption: and unit:')
    items = [[x.strip() for x in item.split('|')] for item in bullets('\n'.join(lines))]
    if any(len(item) not in (2, 3) or not item[0] or
           (len(item) == 3 and item[2] != 'quiet') for item in items):
        raise ValueError('bars use label | nonnegative number | quiet(optional)')
    values = [float(item[1].replace(',', '')) for item in items]
    if any(not math.isfinite(value) or value < 0 for value in values):
        raise ValueError('bar values must be finite and nonnegative')
    maximum = max(values)
    if 'max' in metadata:
        scale = float(metadata['max'].replace(',', ''))
        if not math.isfinite(scale) or scale <= 0 or scale < maximum:
            raise ValueError('bars max: must be a positive number no smaller than every value')
        maximum = scale
    rendered = []
    for item, value in zip(items, values):
        width = value / maximum * 100 if maximum else 0
        cls = ' quiet' if len(item) == 3 else ''
        label = f'{item[0]}: {value:g} {metadata["unit"]}'
        rendered.append(f'<div class="bar{cls}"><span>{esc(label)}</span>'
                        f'<b aria-hidden="true" style="width:{width:.1f}%"></b></div>')
    caption = metadata['caption'] + '. 단위: ' + metadata['unit']
    return ('<figure class="fig bars"><figcaption>' + esc(caption) + '</figcaption>' +
            ''.join(rendered) + '</figure>')


def render(blocks):
    o = []
    for kind, b in blocks:
        if kind == 'tiles':
            items = [[x.strip() for x in t.split('|')] for t in bullets(b)]
            if any(len(item) != 2 or not all(item) for item in items):
                raise ValueError('tiles use nonempty value | description pairs')
            o.append('<ul class="tiles">' + ''.join(f'<li><span class="cap">{inline(c)}</span><span class="big">{inline(v)}</span></li>' for v, c in items) + '</ul>')
        elif kind == 'bars':
            o.append(bars(b))
        elif kind in ('decision', 'note'):
            o.append(f'<div class="{kind}">' + render(split_blocks(b)) + '</div>')
        elif b.startswith('|'): o.append(table(b))
        elif b.startswith('> '): o.append('<div class="callout"><p>' + inline(re.sub(r'(?m)^> ?', '', b).replace('\n', ' ')) + '</p></div>')
        elif b.startswith('- '): o.append('<ul>' + ''.join(f'<li>{inline(t)}</li>' for t in bullets(b)) + '</ul>')
        elif re.match(r'\d+\. ', b): o.append('<ol>' + ''.join(f'<li>{inline(re.sub(r"^\d+\. ", "", l))}</li>' for l in b.splitlines()) + '</ol>')
        elif (m := re.fullmatch(r'\[\[figure:([\w-]+)\]\]', b)): o.append(figure(m.group(1)))
        else: o.append(f'<p>{inline(" ".join(b.splitlines()))}</p>')
    return '\n'.join(o)


def card(h, lines):
    quiet = h.startswith('~ ')
    h = h[2:] if quiet else h
    m = re.match(r'\[([^\]]+)\]\s*(.*)', h)
    badge = f'<span class="badge">{esc(m.group(1))}</span>' if m else ''
    title = m.group(2) if m else h
    dl = ''.join(f'<dt>{esc(a)}</dt><dd>{inline(b)}</dd>' for a, b in lines)
    card_class = "card quiet" if quiet else "card"
    return f'<article class="{card_class}"><h3>{badge}{esc(title)}</h3><dl>{dl}</dl></article>'


def fields(txt):
    ls = [l.strip() for l in txt.strip().splitlines() if l.strip()]
    ms = [re.fullmatch(r'-\s+([^:]+):\s+(.*)', l) for l in ls]
    return [(m.group(1), m.group(2)) for m in ms] if ls and all(ms) else None


def section(i, title, body):
    folded = title.endswith(' ~~')
    quiet = folded or title.endswith(' ~')
    title = title[:-3] if folded else title[:-2] if quiet else title
    sid = f's{i}'
    parts = re.split(r'^### ', body, flags=re.M)
    if folded:
        o = [f'<section id="{sid}" class="is-quiet is-folded" aria-labelledby="{sid}-h"><details class="rp-fold"><summary><h2 id="{sid}-h">{esc(title)}</h2></summary>']
    else:
        o = [f'<section id="{sid}" aria-labelledby="{sid}-h"{" class=is-quiet" if quiet else ""}><h2 id="{sid}-h">{esc(title)}</h2>']
    if parts[0].strip(): o.append(render(split_blocks(parts[0].strip('\n'))))
    run = []

    def flush():
        if run: o.append('<div class="cards">' + ''.join(run) + '</div>'); run.clear()
    for blk in parts[1:]:
        h, _, txt = blk.partition('\n')
        f = fields(txt)
        if f: run.append(card(h.strip(), f)); continue
        if re.match(r'^(?:\[[^\]]+\]\s*|~\s*)', h.strip()) and re.search(r'(?m)^-\s+[^:]+:', txt):
            print('경고: 카드처럼 보이는 ### 블록에 필드 이외의 본문이 있어 일반 소제목으로 처리합니다: ' + h.strip(), file=sys.stderr)
        flush()
        o.append(f'<h3 class="sub">{esc(h.strip())}</h3>' + render(split_blocks(txt.strip('\n'))))
    flush()
    if folded:
        o.append('</details>')
    o.append('</section>')
    return sid, title, '\n'.join(o)


def build(md, a):
    parts = re.split(r'^## ', md, flags=re.M)
    m = re.match(r'# (.+)', parts[0])
    if not m: sys.exit('원고 첫 줄이 `# 제목` 이 아니다')
    title = m.group(1).strip()
    rest = [l for l in parts[0].splitlines()[1:] if l.strip()]
    if len(rest) > 1:
        raise ValueError('제목 다음에는 부제 한 줄만 둘 수 있습니다. 결론 콜아웃(> 문단)과 본문은 첫 ## 절 안에 작성하세요.')
    if len(parts) < 2:
        raise ValueError('보고서에 ## 절이 하나 이상 필요합니다. 결론 콜아웃은 첫 ## 절 안에 두세요.')
    meta = rest[0].strip() if rest else ''
    secs = []
    for i, p in enumerate(parts[1:], 1):
        t, _, body = p.partition('\n')
        if not t.strip():
            raise ValueError('## 절 제목이 비어 있습니다.')
        secs.append(section(i, t.strip(), body.strip('\n')))
    toc = ''.join(f'<li><a href="#{s}">{esc(t)}</a></li>' for s, t, _ in secs)
    css = Path(a.css).read_text(encoding='utf-8')
    js = Path(a.js).read_text(encoding='utf-8')
    download_controls = '' if a.no_download else '<button type="button" data-ht-download aria-label="다운로드" hidden>다운로드</button><span data-ht-export-status role="status" hidden></span>'
    return f'''<!doctype html>
<html lang="{esc(a.lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{esc(title)}</title>
<style>
{css}
</style>
</head>
<body>
<div class="page">
<div class="rp-bar">
<nav class="toc" aria-label="{esc(a.toc_label)}"><details><summary><svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true" focusable="false"><path d="M1 3h12M1 7h12M1 11h12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg><span>{esc(a.toc_label)}</span></summary><ol>{toc}</ol></details></nav>
<div class="rp-tools"><a class="rp-title" href="#top">{esc(title)}</a><fieldset class="ht-theme-control" data-ht-theme-control hidden><legend class="ht-visually-hidden">테마</legend><div class="ht-theme-buttons"></div></fieldset>{download_controls}</div>
</div>
<header id="top"><h1>{esc(title)}</h1>{f'<p class="meta">{esc(meta)}</p>' if meta else ''}</header>
<main>
{chr(10).join(h for _, _, h in secs)}
</main>
</div>
<script>
{js}
</script>
<!-- tk-writing:shared-theme -->
{theme_assets()}</body>
</html>
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('manuscript'); ap.add_argument('output')
    ap.add_argument('--figures'); ap.add_argument('--css', default=asset('page.css'))
    ap.add_argument('--js', default=asset('page.js')); ap.add_argument('--lang', default='ko')
    ap.add_argument('--toc-label', default='목차'); ap.add_argument('--allow-missing-figures', action='store_true')
    ap.add_argument('--no-download', action='store_true', help='omit download button/status and export payload in report delivery')
    a = ap.parse_args()
    Ctx.figures = Path(a.figures) if a.figures else None
    Ctx.missing_ok = a.allow_missing_figures
    try:
        out = build(Path(a.manuscript).read_text(encoding='utf-8'), a)
        destination = Path(a.output)
        if destination.is_symlink():
            raise ValueError('output must not be a symlink')
        # All parsing finishes before replacing an existing output.
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=destination.parent,
                                         prefix='.report-', delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(out)
        try:
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)
    except (ValueError, OSError) as error:
        ap.exit(1, str(error) + '\n')
    print('wrote', a.output, len(out.encode('utf-8')), 'bytes')


if __name__ == '__main__':
    main()
