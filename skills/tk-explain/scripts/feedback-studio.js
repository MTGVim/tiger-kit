/*
  Feedback studio: collect N feedback items on a static explainer page, then copy them in one message,
  and drive videos that add_feedback_studio.py --video put in place of images (speed, poster, missing-file fallback).
  Injected inline by add_feedback_studio.py (no network, no external files; the video is referenced, never embedded). Two modes:
    - archify:  an archify 3.x explainer (has section.panel + .ask-dialog). Adds "목록에 담기" to archify's own
                Ask dialog, so its panel buttons and drag-to-quote keep working; items go to the tray instead of
                being copied one by one. Archify's own single copy button stays.
    - generic:  any other single-file HTML. Adds a drag-to-quote floating button, a small "피드백" button on
                each anchored section, and its own dialog.
  Sections (search "// ==="): CONFIG, STORE, STYLE, ANCHORS, FORMAT, TRAY, DIALOG, ARCHIFY, GENERIC, VIDEO, INIT.
  Coupling note — shortcut: archify mode reads archify 3.2 DOM classes (.panel, .panel-id, .panel-head,
  .ask-dialog, .ask-where, .ask-button, .ask-floating); if archify renames them, the page falls back to generic mode.
*/
(() => {
  'use strict';
  if (window.__feedbackStudio) return; // injected twice

  // === CONFIG ===
  const PAGE_TITLE = (document.querySelector('h1')?.textContent || document.title || '').trim(); // h1 first: archify titles carry a " · Archify" suffix
  const FILE = location.protocol === 'file:' ? decodeURIComponent(location.pathname) : location.href.split('#')[0];
  const STORE_KEY = 'page-feedback:' + FILE;
  const MAC = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
  const isArchify = () => !!(document.querySelector('section.panel .panel-head') && document.querySelector('dialog.ask-dialog footer') && document.querySelector('dialog.ask-dialog textarea') && document.querySelector('dialog.ask-dialog .ask-where'));

  // === STORE: localStorage may be blocked; the page keeps working for the current visit ===
  let items = [];
  try { items = JSON.parse(localStorage.getItem(STORE_KEY) || '[]'); } catch (e) { items = []; }
  if (!Array.isArray(items)) items = [];
  items = items.filter(x => x && typeof x.id_ === 'string' && typeof x.id === 'string' && typeof x.label === 'string' && typeof x.text === 'string');
  function persist() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(items)); }
    catch (e) {
      if (!root.querySelector('.fs-storage-warning')) {
        const warning = el('p', 'fs-storage-warning');
        warning.textContent = '브라우저 저장소를 쓸 수 없어 새로고침하면 사라집니다. 먼저 복사해 두세요.';
        warning.setAttribute('role', 'status'); drawer.append(warning);
      }
    }
  }

  // === STYLE: own tokens; follows html[data-theme] (archify, TigerKit pages) and falls back to the OS preference ===
  const css = `
  .fs-root{--fs-bg:#ffffff;--fs-ink:#0b0b0b;--fs-ink2:#52514e;--fs-line:#dcdbd3;--fs-accent:#2a78d6;--fs-accent-bg:#e8efff;--fs-danger:#c43333;
    font:14px/1.5 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;color:var(--fs-ink)}
  @media (prefers-color-scheme: dark){html:not([data-theme="light"]) .fs-root{--fs-bg:#1d1d1b;--fs-ink:#f2f1ec;--fs-ink2:#c4c3bb;--fs-line:#3a3935;--fs-accent:#6aa5ee;--fs-accent-bg:#1e2c40;--fs-danger:#ef6b6b}}
  html[data-theme="dark"] .fs-root{--fs-bg:#1d1d1b;--fs-ink:#f2f1ec;--fs-ink2:#c4c3bb;--fs-line:#3a3935;--fs-accent:#6aa5ee;--fs-accent-bg:#1e2c40;--fs-danger:#ef6b6b}
  .fs-root button{font:inherit;cursor:pointer;border-radius:8px;border:1px solid var(--fs-line);background:var(--fs-bg);color:var(--fs-ink);padding:5px 10px}
  .fs-root button:focus-visible,.fs-root textarea:focus-visible{outline:2px solid var(--fs-accent);outline-offset:2px}
  .fs-root button.fs-primary{background:var(--fs-accent);border-color:var(--fs-accent);color:#fff}
  .fs-root button.fs-danger{color:var(--fs-danger)}
  .fs-tray-btn{position:fixed;right:16px;bottom:16px;z-index:2147483000;box-shadow:0 4px 16px rgb(0 0 0/.18);border-radius:999px!important;padding:8px 14px!important;background:var(--fs-accent)!important;color:#fff!important;border:0!important}
  .fs-tray-btn[data-empty="true"]{background:var(--fs-bg)!important;color:var(--fs-ink2)!important;border:1px solid var(--fs-line)!important}
  .fs-drawer{position:fixed;right:16px;bottom:64px;z-index:2147483000;width:min(440px,calc(100vw - 32px));max-height:min(70vh,640px);display:flex;flex-direction:column;
    background:var(--fs-bg);border:1px solid var(--fs-line);border-radius:12px;box-shadow:0 10px 32px rgb(0 0 0/.22)}
  .fs-drawer[hidden]{display:none}
  .fs-drawer header,.fs-drawer footer{display:flex;gap:8px;align-items:center;padding:10px 12px;flex-wrap:wrap}
  .fs-drawer header{border-bottom:1px solid var(--fs-line)} .fs-drawer footer{border-top:1px solid var(--fs-line)}
  .fs-drawer h2{font-size:14px;margin:0;flex:1}
  .fs-list{list-style:none;margin:0;padding:4px 12px;overflow:auto}
  .fs-item{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:8px;padding:8px 0;border-top:1px solid var(--fs-line)}
  .fs-item:first-child{border-top:0}
  .fs-item>input,.fs-item>button{align-self:start}
  .fs-where{font-size:12px;color:var(--fs-accent);background:none!important;border:0!important;padding:0!important;text-align:left}
  .fs-quote{font-size:12px;color:var(--fs-ink2);border-left:2px solid var(--fs-line);padding-left:6px;margin:2px 0}
  .fs-text{white-space:pre-wrap;word-break:break-word}
  .fs-empty{color:var(--fs-ink2);padding:12px 0}
  .fs-hint{font-size:12px;color:var(--fs-ink2)}
  .fs-float{position:absolute;z-index:2147483000;border-radius:999px!important;padding:3px 10px!important;font-size:12px!important;background:var(--fs-ink)!important;color:var(--fs-bg)!important;border:0!important;box-shadow:0 4px 14px rgb(0 0 0/.18)}
  .fs-sec-btn{margin-left:8px;font-size:12px!important;padding:1px 8px!important;vertical-align:middle}
  .fs-dialog{width:min(520px,calc(100vw - 32px));padding:0;border-radius:12px;border:1px solid var(--fs-line);background:var(--fs-bg);color:var(--fs-ink)}
  .fs-dialog form{display:flex;flex-direction:column;gap:10px;padding:14px}
  .fs-dialog h2{font-size:15px;margin:0} .fs-dialog .fs-where-line{font-size:12px;color:var(--fs-ink2);margin:2px 0 0}
  .fs-dialog textarea{font:inherit;color:var(--fs-ink);background:var(--fs-bg);border:1px solid var(--fs-line);border-radius:8px;padding:8px;min-height:90px;resize:vertical}
  .fs-dialog footer{display:flex;gap:8px;justify-content:flex-end;align-items:center}
  .fs-toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:2147483001;background:var(--fs-ink);color:var(--fs-bg);padding:8px 14px;border-radius:8px;opacity:0;transition:opacity .2s;pointer-events:none}
  .fs-toast.fs-show{opacity:1}
  .fs-added-btn{margin-right:auto}
  /* video in place of an image: the image right after it stays for poster, print/export and no-JS */
  @media screen{.js .fs-vwrap.interactive,.fs-vwrap{display:block!important;margin:0 0 8px}} /* screen only: archify's print rule must still hide it */
  .fs-vwrap video{width:100%;display:block;border-radius:10px;background:#000}
  .fs-vwrap:not([data-missing]) + img{display:none}
  .fs-vwrap[data-missing] video,.fs-vwrap[data-missing] .fs-speed{display:none}
  .fs-speed{display:flex;gap:4px;align-items:center;margin-top:8px;flex-wrap:wrap}
  .fs-speed .fs-hint{margin-right:2px}
  .fs-root [data-rate]{padding:2px 8px;font-size:13px;font-variant-numeric:tabular-nums}
  .fs-root [data-rate][aria-pressed="true"]{background:var(--fs-accent-bg);border-color:var(--fs-accent);color:var(--fs-accent);font-weight:600}
  .fs-video-missing{color:var(--fs-ink2);margin:8px 0 0}
  @media print{.fs-vwrap + img{display:block!important}
  .fs-root,.fs-dialog::backdrop,.fs-sec-btn{display:none!important}}
  @media (prefers-reduced-motion: reduce){.fs-toast{transition:none}}`;
  const style = document.createElement('style'); style.textContent = css; document.head.append(style);
  const root = document.createElement('div'); root.className = 'fs-root interactive'; document.body.append(root);
  const el = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };
  function toast(msg) { const t = root.querySelector('.fs-toast') || root.appendChild(el('div', 'fs-toast')); t.setAttribute('role', 'status'); t.textContent = msg; t.classList.add('fs-show'); clearTimeout(toast.h); toast.h = setTimeout(() => t.classList.remove('fs-show'), 2200); }

  // === ANCHORS: where a feedback item points. archify: its panels. generic: nearest ancestor with an id ===
  const headText = (h) => { if (!h) return ''; const c = h.cloneNode(true); c.querySelectorAll('.fs-sec-btn,.ask-button').forEach((b) => b.remove()); return c.textContent.trim(); };
  function describe(node) {
    const start = node && node.nodeType === 1 ? node : node?.parentElement;
    if (!start) return { id: '', label: '페이지 전체' };
    const panel = start.closest('section.panel');
    if (panel) {
      if (panel.id === 'answer') return { id: 'answer', label: '결론' };
      const number = panel.querySelector('.panel-id')?.textContent.trim() || '';
      const title = panel.dataset.title || headText(panel.querySelector('h2')) || panel.id;
      return { id: panel.id, label: number ? `패널 ${number} 「${title}」` : `「${title}」` };
    }
    const anchor = start.closest('[data-feedback-anchor],section[id],article[id],figure[id],[id]:is(h1,h2,h3,h4)');
    if (!anchor) return { id: '', label: '페이지 전체' };
    const heading = anchor.matches('h1,h2,h3,h4') ? anchor : anchor.querySelector('h1,h2,h3,h4');
    const title = anchor.dataset.feedbackAnchor || headText(heading) || anchor.id;
    return { id: anchor.id || '', label: `「${title}」` };
  }

  // === FORMAT: one message for N items, ordered as collected ===
  function asMessage(sel) {
    const lines = [`페이지: 「${PAGE_TITLE}」`, `파일: ${FILE}`, `피드백 ${sel.length}건`, ''];
    sel.forEach((it, i) => {
      lines.push(`${i + 1}. 위치: ${it.label}${it.id ? ` (ID: ${it.id})` : ''}`);
      if (it.quote) lines.push(`   인용: 「${it.quote}」`);
      lines.push(`   피드백: ${it.text.replace(/\s*\n\s*/g, ' / ')}`);
    });
    lines.push('');
    lines.push(isArchify()
      ? '각 패널을 Archify 패널 교체(patch explainer)로 고치고, 패널 ID는 유지해 주세요. 지적한 표현이 다른 패널에도 있으면 함께 고쳐 주세요.'
      : '각 위치의 ID와 구조는 유지하고 지적한 부분을 고쳐 주세요. 같은 표현이 다른 곳에도 있으면 함께 고쳐 주세요.');
    return lines.join('\n');
  }
  async function copyText(s) {
    try { await navigator.clipboard.writeText(s); return true; }
    catch (e) {
      const t = document.createElement('textarea'); t.value = s; root.append(t); t.select();
      let ok = false; try { ok = document.execCommand('copy'); } catch (_) { ok = false; }
      t.remove(); return ok;
    }
  }

  // === TRAY: floating counter + drawer with select / jump / delete / copy / clear ===
  const trayBtn = el('button', 'fs-tray-btn'); trayBtn.type = 'button'; trayBtn.setAttribute('aria-expanded', 'false');
  const drawer = el('section', 'fs-drawer'); drawer.hidden = true; drawer.setAttribute('aria-label', '모은 피드백');
  drawer.innerHTML = '<header><h2></h2><label class="fs-hint"><input type="checkbox" class="fs-all" checked> 전체 선택</label></header><ul class="fs-list"></ul><footer><button type="button" class="fs-danger fs-clear">모두 지우기</button><span style="flex:1"></span><button type="button" class="fs-primary fs-copy">선택한 피드백 복사</button></footer><p class="fs-hint" style="margin:0;padding:0 12px 10px">문장을 드래그하거나 각 부분의 버튼으로 피드백을 담은 뒤, 한 번에 복사해 에이전트에게 붙여 넣으세요. 이 브라우저에만 저장됩니다.</p>';
  root.append(drawer, trayBtn);
  trayBtn.addEventListener('click', () => { drawer.hidden = !drawer.hidden; trayBtn.setAttribute('aria-expanded', String(!drawer.hidden)); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !drawer.hidden && !document.querySelector('dialog[open]')) { drawer.hidden = true; trayBtn.setAttribute('aria-expanded', 'false'); } });

  function render() {
    trayBtn.textContent = items.length ? `피드백 ${items.length}건` : '피드백 0건';
    trayBtn.dataset.empty = String(!items.length);
    drawer.querySelector('h2').textContent = `모은 피드백 ${items.length}건`;
    const list = drawer.querySelector('.fs-list'); list.innerHTML = '';
    if (!items.length) list.append(el('li', 'fs-empty', '아직 담은 피드백이 없습니다.'));
    items.forEach((it) => {
      const li = el('li', 'fs-item');
      const cb = document.createElement('input'); cb.type = 'checkbox'; cb.checked = it.checked !== false; cb.setAttribute('aria-label', it.label + ' 선택');
      cb.addEventListener('change', () => { it.checked = cb.checked; persist(); syncAll(); });
      const body = el('div');
      const where = el('button', 'fs-where', it.label + (it.id ? ` · ${it.id}` : '')); where.type = 'button'; where.title = '이 위치로 이동';
      where.addEventListener('click', () => { const t = it.id && document.getElementById(it.id); if (t) t.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' }); });
      body.append(where);
      if (it.quote) body.append(el('div', 'fs-quote', it.quote));
      body.append(el('div', 'fs-text', it.text));
      const del = el('button', 'fs-danger', '삭제'); del.type = 'button';
      del.addEventListener('click', () => { items = items.filter((x) => x.id_ !== it.id_); persist(); render(); });
      li.append(cb, body, del); list.append(li);
    });
    syncAll();
  }
  function syncAll() { drawer.querySelector('.fs-all').checked = items.length > 0 && items.every((x) => x.checked !== false); }
  drawer.querySelector('.fs-all').addEventListener('change', (e) => { items.forEach((x) => { x.checked = e.target.checked; }); persist(); render(); });
  drawer.querySelector('.fs-clear').addEventListener('click', () => {
    if (!items.length) return;
    if (!confirm(`모은 피드백 ${items.length}건을 모두 지울까요? 되돌릴 수 없습니다.`)) return;
    items = []; persist(); render();
  });
  drawer.querySelector('.fs-copy').addEventListener('click', async () => {
    const sel = items.filter((x) => x.checked !== false);
    if (!sel.length) { toast('복사할 피드백을 선택하세요.'); return; }
    toast((await copyText(asMessage(sel))) ? `피드백 ${sel.length}건을 복사했습니다.` : '복사하지 못했습니다. 브라우저 권한을 확인하세요.');
  });
  function add(where, quote, text) {
    text = (text || '').trim();
    if (!text) { toast('피드백 내용을 입력하세요.'); return false; }
    items.push({ id_: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), id: where.id, label: where.label,
                 quote: (quote || '').replace(/\s+/g, ' ').trim().slice(0, 400), text, checked: true, created_at: new Date().toISOString() });
    persist(); render(); toast(`피드백을 담았습니다. 지금 ${items.length}건입니다.`);
    return true;
  }

  // shared: Ctrl/⌘+Enter that waits for IME composition (Korean last syllable) before acting
  function bindSubmitKey(textarea, action) {
    let pending = false;
    textarea.addEventListener('compositionend', () => { if (pending) { pending = false; setTimeout(action, 0); } });
    textarea.addEventListener('keydown', (e) => {
      if (e.key !== 'Enter' || !(e.metaKey || e.ctrlKey)) return;
      e.preventDefault(); e.stopImmediatePropagation();
      if (e.isComposing || e.keyCode === 229) { pending = true; textarea.blur(); } else action();
    }, true);
  }

  // === DIALOG (generic mode): quote + textarea, adds to the tray ===
  function makeDialog() {
    const d = document.createElement('dialog'); d.className = 'fs-dialog';
    d.innerHTML = `<form method="dialog"><div><h2>피드백 담기</h2><p class="fs-where-line"></p></div><blockquote class="fs-quote" hidden></blockquote><textarea aria-label="피드백" placeholder="무엇이 어색하거나 틀렸는지, 어떻게 바꾸면 좋을지 적어 주세요."></textarea><footer><span class="fs-hint">${MAC ? '⌘↵' : 'Ctrl+↵'} 목록에 담기</span><span style="flex:1"></span><button type="button" class="fs-cancel">취소</button><button type="submit" class="fs-primary">목록에 담기</button></footer></form>`;
    root.append(d);
    let ctx = null;
    const area = d.querySelector('textarea');
    const submit = () => { if (ctx && add(ctx.where, ctx.quote, area.value)) d.close(); };
    d.querySelector('form').addEventListener('submit', (e) => { e.preventDefault(); submit(); });
    d.querySelector('.fs-cancel').addEventListener('click', () => d.close());
    bindSubmitKey(area, submit);
    return (where, quote) => {
      ctx = { where, quote };
      d.querySelector('.fs-where-line').textContent = where.label + (where.id ? ` · ${where.id}` : '');
      const q = d.querySelector('.fs-quote'); q.hidden = !quote; q.textContent = quote || '';
      area.value = ''; d.showModal(); area.focus();
    };
  }

  // === ARCHIFY: add "목록에 담기" to archify's Ask dialog and remember which panel opened it ===
  function wireArchify() {
    const dialog = document.querySelector('dialog.ask-dialog');
    const footer = dialog.querySelector('footer');
    const area = dialog.querySelector('textarea');
    let panel = null;
    const panelOfSelection = () => { const s = getSelection(); if (!s || !s.rangeCount) return null; const n = s.getRangeAt(0).commonAncestorContainer; return (n.nodeType === 1 ? n : n.parentElement)?.closest('section.panel') || null; };
    // capture phase: runs before archify's own click handlers open the dialog
    document.addEventListener('click', (e) => {
      const ask = e.target.closest?.('.ask-button'); if (ask) panel = ask.closest('section.panel');
      if (e.target.closest?.('.ask-floating')) panel = panelOfSelection() || panel;
    }, true);
    const addBtn = el('button', 'fs-primary fs-added-btn', '목록에 담기'); addBtn.type = 'button';
    addBtn.style.cssText = 'font:inherit;cursor:pointer;border-radius:8px;padding:5px 10px;border:1px solid #2a78d6;background:#2a78d6;color:#fff';
    footer.prepend(addBtn);
    const collect = () => {
      const quote = dialog.querySelector('blockquote:not([hidden])')?.textContent || '';
      if (add(describe(panel || document.getElementById('answer')), quote, area.value)) dialog.close();
    };
    addBtn.addEventListener('click', collect);
    // on this page ⌘/Ctrl+Enter collects into the list instead of copying a single question
    bindSubmitKey(area, collect);
    const kbd = dialog.querySelector('button[type="submit"] kbd'); if (kbd) kbd.remove();
    const note = dialog.querySelector('.ask-note');
    if (note) note.textContent = `${MAC ? '⌘↵' : 'Ctrl+↵'}로 목록에 담고, 오른쪽 아래에서 여러 건을 한 번에 복사합니다. 이 질문만 바로 복사하려면 오른쪽 버튼을 누르세요.`;
  }

  // === GENERIC: drag-to-quote floating button + a button on each anchored section heading ===
  function wireGeneric() {
    const open = makeDialog();
    const floating = el('button', 'fs-float', '피드백'); floating.type = 'button'; floating.hidden = true; root.append(floating);
    let selected = null;
    document.addEventListener('selectionchange', () => {
      const s = getSelection(); const text = s ? s.toString().replace(/\s+/g, ' ').trim() : '';
      const inside = s && s.rangeCount && root.contains(s.getRangeAt(0).commonAncestorContainer);
      if (!s || !s.rangeCount || text.length < 2 || inside || document.querySelector('dialog.fs-dialog[open]')) { floating.hidden = true; selected = null; return; }
      const box = s.getRangeAt(0).getBoundingClientRect();
      selected = { where: describe(s.getRangeAt(0).commonAncestorContainer), quote: text };
      floating.style.left = `${Math.max(8, Math.min(innerWidth - 90, box.left + box.width / 2 - 30 + scrollX))}px`;
      floating.style.top = `${Math.max(scrollY + 4, box.top + scrollY - 36)}px`;
      floating.hidden = false;
    });
    floating.addEventListener('mousedown', (e) => e.preventDefault()); // keep the selection
    floating.addEventListener('click', () => { if (selected) open(selected.where, selected.quote); floating.hidden = true; });
    document.querySelectorAll('[data-feedback-anchor],section[id],article[id]').forEach((sec) => {
      if (root.contains(sec)) return;
      const h = sec.querySelector('h1,h2,h3'); if (!h || h.querySelector('.fs-sec-btn')) return;
      const b = el('button', 'fs-sec-btn', '피드백'); b.type = 'button'; b.setAttribute('aria-label', `${headText(h)}에 피드백 담기`);
      b.style.cssText = 'font:inherit;cursor:pointer;border-radius:8px;border:1px solid currentColor;background:transparent;color:inherit;opacity:.7';
      b.addEventListener('click', () => open(describe(sec)));
      h.append(b);
    });
  }

  // === VIDEO: each video sits right before the image it replaces; that image is its poster and its fallback ===
  function wireVideo() {
    const RATES = [0.75, 1, 1.25, 1.5, 2], RATE_KEY = 'page-feedback:rate';
    let saved = 1;
    try { const r = Number(localStorage.getItem(RATE_KEY)); if (RATES.includes(r)) saved = r; } catch (e) { /* default 1x */ }
    document.querySelectorAll('[data-fs-video]').forEach((box) => {
      box.hidden = false;
      const v = box.querySelector('video'), btns = [...box.querySelectorAll('[data-rate]')], img = box.nextElementSibling;
      if (img && img.tagName === 'IMG') { v.poster = img.currentSrc || img.src; if (img.alt) v.setAttribute('aria-label', img.alt); }
      const show = () => btns.forEach((b) => b.setAttribute('aria-pressed', String(Number(b.dataset.rate) === v.playbackRate)));
      const set = (r) => {
        document.querySelectorAll('[data-fs-video] video').forEach((x) => { x.playbackRate = r; x.defaultPlaybackRate = r; });
        try { localStorage.setItem(RATE_KEY, String(r)); } catch (e) { /* page-only */ }
      };
      const missing = () => { box.dataset.missing = 'true'; box.querySelector('.fs-video-missing').hidden = false; };
      btns.forEach((b) => b.addEventListener('click', () => set(Number(b.dataset.rate))));
      v.addEventListener('ratechange', show);
      v.addEventListener('error', missing);
      if (v.error) missing(); // the load may have failed before this script ran
      v.playbackRate = saved; v.defaultPlaybackRate = saved;
      show();
    });
  }

  // === INIT: archify builds its Ask dialog in its own script; wait briefly for it before choosing a mode ===
  function start() {
    let tries = 0;
    const pick = () => {
      if (isArchify()) { wireArchify(); render(); return; }
      if (document.querySelector('section.panel .panel-head') && tries++ < 20) { setTimeout(pick, 100); return; }
      wireGeneric(); render();
    };
    pick();
  }
  window.__feedbackStudio = { asMessage, describe, get items() { return items; } }; // for automated checks
  const boot = () => { wireVideo(); start(); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
