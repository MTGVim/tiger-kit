// Inject only for selected tutorial capture. Remove before assertion screenshots.
(() => {
  if (window.__tigerkitCapture) return;
  const host = document.createElement('div');
  host.setAttribute('aria-hidden', 'true');
  host.style.cssText = 'all:initial;display:block;position:fixed;inset:0;pointer-events:none;z-index:2147483647';
  const root = host.attachShadow({ mode: 'closed' });
  document.documentElement.append(host);
  const style = document.createElement('style');
  style.textContent = `
    :host,*{pointer-events:none!important;box-sizing:border-box}
    .cursor,.ring,.dock,.highlight{position:fixed}
    .cursor{width:28px;height:28px;left:-40px;top:-40px;transform:translate(-4px,-2px)}
    .ring{width:44px;height:44px;border:3px solid #ff2488;border-radius:50%;
      background:#ff248830;animation:tk-ring .7s ease-out forwards}
    .dock{display:flex;flex-direction:column;gap:6px;max-width:calc(100vw - 16px)}
    .keys{display:flex;gap:5px;padding:6px 8px;border-radius:12px;background:#111a;
      overflow:hidden;animation:tk-key 1.8s ease-out forwards}
    .cap{display:inline-flex;align-items:center;justify-content:center;min-width:36px;
      height:38px;padding:0 10px;flex-shrink:0;font:600 19px/1 sans-serif;color:#1f2330;
      background:linear-gradient(#fff,#e9ebf0);border:1px solid #b9bdc8;
      border-bottom-width:4px;border-radius:8px;box-shadow:0 3px 8px #0004}
    .count{align-self:center;color:white;font:700 18px/1 sans-serif}
    .highlight{border:3px solid #ff2488;border-radius:10px;box-shadow:0 0 0 4px #ff248830}
    @keyframes tk-ring{from{transform:translate(-50%,-50%) scale(.3);opacity:.9}
      to{transform:translate(-50%,-50%) scale(1.6);opacity:0}}
    @keyframes tk-key{0%{opacity:0;transform:translateY(8px)}12%,75%{opacity:1}
      100%{opacity:0;transform:translateY(-24px)}}`;
  root.append(style);
  const make = (className, parent = root) => {
    const el = document.createElement('div'); el.className = className; parent.append(el); return el;
  };
  const cursor = make('cursor');
  cursor.innerHTML = '<svg width="28" height="28" viewBox="0 0 24 24"><path d="M4 2l15 11-6.5 1 3.8 7.2-2.6 1.4-3.8-7.3L5 20z" fill="#111" stroke="white" stroke-width="1.5"/></svg>';
  const dock = make('dock');
  const events = new AbortController(), timers = new Set(), highlights = new Set();
  let x = innerWidth / 2, y = innerHeight / 2, last = null;
  const later = (fn, ms) => {
    const id = setTimeout(() => { timers.delete(id); fn(); }, ms); timers.add(id); return id;
  };
  const position = () => {
    const w = dock.offsetWidth, h = dock.offsetHeight;
    dock.style.left = Math.max(8, Math.min(innerWidth - w - 8, x + 28 + w > innerWidth - 8 ? x - w - 16 : x + 28)) + 'px';
    dock.style.top = Math.max(8, Math.min(innerHeight - h - 8, y + 24 + h > innerHeight - 8 ? y - h - 16 : y + 24)) + 'px';
  };
  const secret = target => Boolean(target?.tagName?.includes('-') || target?.closest?.(
    'input[type="password"],[autocomplete~="current-password"],[autocomplete~="new-password"],'
    + '[autocomplete~="one-time-code"],[autocomplete~="cc-number"],[autocomplete~="cc-csc"],[data-tigerkit-sensitive]'));
  const names = { ArrowRight: '→', ArrowLeft: '←', ArrowUp: '↑', ArrowDown: '↓',
    Enter: 'Enter', Escape: 'Esc', Tab: 'Tab', Backspace: '⌫', ' ': 'Space' };
  const show = (text, target, character) => {
    // Mask before constructing DOM, grouping state or labels; retain no secret key value.
    const label = secret(target) ? '●' : text;
    const now = performance.now();
    const grouped = last && now - last.at < 900 && last.target === target;
    if (!(grouped && ((character && last.character) || (!character && !last.character && last.label === label)))) {
      const row = make('keys', dock);
      last = { row, target, character, label, count: 1, at: now };
      while (dock.children.length > 3) dock.firstElementChild.remove();
    } else if (!character) {
      last.count++;
    }
    if (character || last.count === 1) {
      const cap = make('cap', last.row); cap.textContent = label;
      // Bound long input displays without retaining an unlimited transcription.
      while (last.row.children.length > 12) last.row.firstElementChild.remove();
    } else {
      if (!last.badge) last.badge = make('count', last.row);
      last.badge.textContent = '×' + last.count;
    }
    last.row.style.animation = 'none'; void last.row.offsetWidth;
    last.row.style.animation = 'tk-key 1.8s ease-out forwards';
    clearTimeout(last.timer); timers.delete(last.timer);
    const current = last;
    current.timer = later(() => { current.row.remove(); if (last === current) last = null; }, 1850);
    last.at = now; position();
  };
  const on = (name, fn) => document.addEventListener(name, fn, { capture: true, signal: events.signal });
  on('mousemove', e => { x = e.clientX; y = e.clientY; cursor.style.left = x + 'px'; cursor.style.top = y + 'px'; position(); });
  on('mousedown', e => {
    const ring = make('ring'); ring.style.left = e.clientX + 'px'; ring.style.top = e.clientY + 'px';
    later(() => ring.remove(), 800);
  });
  on('keydown', e => {
    if (e.isComposing || e.key === 'Process' || e.key === 'Dead') return;
    show(names[e.key] || e.key, e.composedPath?.()[0] || e.target,
      Array.from(e.key).length === 1 && !names[e.key]);
  });
  const clear = () => { for (const el of highlights) el.remove(); highlights.clear(); };
  window.__tigerkitCapture = {
    // Call only with an approved public literal for insertText/IME; do not read input values.
    text: (text, target = document.activeElement) => show(String(text), target, true),
    highlight: element => {
      const r = element.getBoundingClientRect(), el = make('highlight');
      Object.assign(el.style, { left: r.left - 6 + 'px', top: r.top - 6 + 'px',
        width: r.width + 12 + 'px', height: r.height + 12 + 'px' }); highlights.add(el);
    },
    clear,
    remove: () => {
      events.abort(); for (const id of timers) clearTimeout(id); timers.clear(); clear();
      host.remove(); delete window.__tigerkitCapture;
    },
  };
})();
