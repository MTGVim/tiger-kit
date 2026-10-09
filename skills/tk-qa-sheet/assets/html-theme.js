(() => {
  const control = document.querySelector('[data-ht-theme-control]');
  if (!control) return;
  const inputs = [...control.querySelectorAll('input[name="ht-theme"]')];
  if (!inputs.length) return;
  const root = document.documentElement;
  const key = 'tigerkit-html-theme';
  const valid = value => ['system', 'light', 'dark'].includes(value);
  const configuredValue = root.getAttribute('data-default-theme');
  const configured = valid(configuredValue) ? configuredValue : 'system';
  const apply = value => {
    if (value === 'system') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', value);
    for (const input of inputs) input.checked = input.value === value;
  };
  let saved = configured;
  try { const value = localStorage.getItem(key); if (valid(value)) saved = value; } catch {}
  apply(saved);
  for (const input of inputs) {
    input.addEventListener('change', () => {
      if (!input.checked) return;
      const value = valid(input.value) ? input.value : 'system';
      apply(value);
      try { localStorage.setItem(key, value); } catch {}
    });
  }
  control.hidden = false;
})();

(() => {
  const nav = document.querySelector('.ht-doc-nav');
  if (!nav) return;
  const toc = nav.querySelector('.ht-doc-toc');
  const summary = toc?.querySelector('summary');
  const links = [...nav.querySelectorAll('.ht-doc-toc-panel a[href^="#"]')];
  const targetFor = hash => {
    try { return document.getElementById(decodeURIComponent(hash.slice(1))); } catch { return null; }
  };
  const sections = links.map(link => targetFor(link.hash)).filter(Boolean);
  const close = (returnFocus = false) => {
    if (!toc?.open) return;
    toc.open = false;
    if (returnFocus) summary?.focus({preventScroll: true});
  };
  nav.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toc?.open) { event.preventDefault(); close(true); }
  });
  document.addEventListener('click', event => { if (!nav.contains(event.target)) close(); });
  nav.addEventListener('focusout', () => {
    requestAnimationFrame(() => { if (!nav.contains(document.activeElement)) close(); });
  });
  // Native anchor navigation owns hashes, history and scrolling; only enhance focus.
  document.addEventListener('click', event => {
    const link = event.target.closest?.('a[href^="#"]');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const target = targetFor(link.hash);
    if (!target) return;
    close();
    const added = !target.hasAttribute('tabindex');
    if (added) target.setAttribute('tabindex', '-1');
    target.focus({preventScroll: true});
    if (added) target.addEventListener('blur', () => target.removeAttribute('tabindex'), {once: true});
  });
  const bar = document.querySelector('.ht-topbar');
  const offset = () => {
    const height = bar && getComputedStyle(bar).position === 'sticky' ? bar.getBoundingClientRect().height : 0;
    document.documentElement.style.setProperty('--ht-anchor-offset', `${height + 16}px`);
  };
  offset();
  if (bar && typeof ResizeObserver !== 'undefined') new ResizeObserver(offset).observe(bar);
  const mark = id => {
    for (const link of links) {
      if (targetFor(link.hash)?.id === id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
  };
  const current = () => {
    const top = bar && getComputedStyle(bar).position === 'sticky' ? Math.max(0, bar.getBoundingClientRect().bottom) : 0;
    // Select the deepest section at the reading edge, not its enclosing area.
    const edge = top + 48;
    let active = null, upcoming = null, nearest = Infinity;
    for (const section of sections) {
      const r = section.getBoundingClientRect();
      if (r.top <= edge && r.bottom > edge) {
        if (!active || active.contains(section)) active = section;
      } else if (r.top > edge && r.top < innerHeight && r.top < nearest) {
        upcoming = section; nearest = r.top;
      }
    }
    active ||= upcoming;
    if (active) mark(active.id);
  };
  const hash = () => { const target = targetFor(location.hash); if (target && sections.includes(target)) mark(target.id); else current(); };
  let pending = false;
  const schedule = () => { if (!pending) { pending = true; requestAnimationFrame(() => { current(); pending = false; }); } };
  addEventListener('hashchange', hash);
  addEventListener('scroll', schedule, {passive: true});
  addEventListener('resize', () => { offset(); schedule(); });
  hash();
})();

(() => {
  const citations = [...(document.querySelectorAll?.('.ht-document sup[id^="cite-"] > a[href^="#ref-"]') || [])];
  if (!citations.length) return;
  const preview = document.createElement('div');
  preview.id = 'ht-citation-preview';
  preview.className = 'ht-citation-preview';
  preview.setAttribute('role', 'tooltip');
  preview.hidden = true;
  document.body.append(preview);
  let active = null;
  const hide = () => {
    if (active) {
      const described = (active.getAttribute('aria-describedby') || '').split(/\s+/).filter(id => id && id !== preview.id);
      if (described.length) active.setAttribute('aria-describedby', described.join(' '));
      else active.removeAttribute('aria-describedby');
    }
    active = null;
    preview.hidden = true;
  };
  const position = () => {
    if (!active || preview.hidden) return;
    const anchor = active.getBoundingClientRect();
    if (anchor.bottom < 0 || anchor.top > innerHeight) { hide(); return; }
    const box = preview.getBoundingClientRect();
    const margin = 12;
    preview.style.left = Math.max(margin, Math.min(anchor.left, innerWidth - box.width - margin)) + 'px';
    const above = anchor.top - box.height - 8;
    const below = Math.min(anchor.bottom + 8, innerHeight - box.height - margin);
    preview.style.top = Math.max(margin, above >= margin ? above : below) + 'px';
  };
  const show = link => {
    let reference;
    try { reference = document.getElementById(decodeURIComponent(link.hash.slice(1))); } catch { return; }
    if (!reference?.matches('li[id]')) return;
    const content = reference.cloneNode(true);
    for (const back of content.querySelectorAll('a[href^="#cite-"]')) back.remove();
    const text = content.textContent.replace(/\s+/g, ' ').trim();
    if (!text) return;
    hide();
    active = link;
    preview.textContent = text;
    preview.hidden = false;
    const described = link.getAttribute('aria-describedby');
    link.setAttribute('aria-describedby', [described, preview.id].filter(Boolean).join(' '));
    position();
  };
  for (const link of citations) {
    link.addEventListener('pointerenter', event => { if (event.pointerType !== 'touch') show(link); });
    link.addEventListener('pointerleave', () => { if (document.activeElement !== link) hide(); });
    link.addEventListener('focus', () => show(link));
    link.addEventListener('blur', hide);
    link.addEventListener('click', hide);
  }
  document.addEventListener('keydown', event => { if (event.key === 'Escape') hide(); });
  addEventListener('hashchange', hide);
  addEventListener('scroll', position, {passive: true});
  addEventListener('resize', position);
})();

