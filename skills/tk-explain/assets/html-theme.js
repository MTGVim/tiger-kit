(() => {
  const start = () => {
    const download = document.querySelector('[data-ht-download]');
    if (!download) return;
    const share = document.querySelector('[data-ht-share]');
    const status = document.querySelector('[data-ht-export-status]');
    const payload = document.querySelector('template[data-ht-export]');
    const encoder = new TextEncoder();
    const decode = value => Uint8Array.from(atob(value), char => char.charCodeAt(0));
    const message = text => { if (status) { status.textContent = text; status.hidden = !text; } };
    let blob, filename;
    try {
      if (!payload) throw Error('missing export');
      const encoded = payload.content.textContent.trim();
      const manifest = JSON.parse(new TextDecoder().decode(decode(encoded)));
      filename = manifest.name;
      const entries = manifest.files.map(file => {
        let bytes = decode(file.base64);
        if (file.html) {
          const marker = document.createElement('template');
          marker.setAttribute('data-ht-export', '');
          marker.setAttribute('data-entry', file.path);
          marker.innerHTML = encoded;
          const text = new TextDecoder().decode(bytes).replace(/<\/body\s*>/i, match => marker.outerHTML + match);
          bytes = encoder.encode(text);
        }
        return {name: encoder.encode(file.path), bytes};
      });
      if (entries.length === 1) {
        blob = new Blob([entries[0].bytes], {type: 'text/html;charset=utf-8'});
      } else {
        // ZIP STORE: no compression dependency or runtime network, UTF-8 paths.
        const parts = [], directory = [];
        let offset = 0, directorySize = 0;
        const header = size => new DataView(new ArrayBuffer(size));
        for (const {name, bytes} of entries) {
          let crc = 0xffffffff;
          for (const byte of bytes) {
            crc ^= byte;
            for (let bit = 0; bit < 8; bit++) crc = (crc >>> 1) ^ ((crc & 1) ? 0xedb88320 : 0);
          }
          crc = (crc ^ 0xffffffff) >>> 0;
          const local = header(30), central = header(46);
          local.setUint32(0, 0x04034b50, true); local.setUint16(4, 20, true);
          local.setUint16(6, 0x800, true); local.setUint16(12, 33, true);
          local.setUint32(14, crc, true); local.setUint32(18, bytes.length, true);
          local.setUint32(22, bytes.length, true); local.setUint16(26, name.length, true);
          central.setUint32(0, 0x02014b50, true); central.setUint16(4, 20, true);
          central.setUint16(6, 20, true); central.setUint16(8, 0x800, true);
          central.setUint16(14, 33, true); central.setUint32(16, crc, true);
          central.setUint32(20, bytes.length, true); central.setUint32(24, bytes.length, true);
          central.setUint16(28, name.length, true); central.setUint32(42, offset, true);
          parts.push(local.buffer, name, bytes); directory.push(central.buffer, name);
          offset += 30 + name.length + bytes.length; directorySize += 46 + name.length;
        }
        const end = header(22);
        end.setUint32(0, 0x06054b50, true); end.setUint16(8, entries.length, true);
        end.setUint16(10, entries.length, true); end.setUint32(12, directorySize, true);
        end.setUint32(16, offset, true);
        blob = new Blob([...parts, ...directory, end.buffer], {type: 'application/zip'});
      }
    } catch {
      message('다운로드 자료를 준비하지 못했습니다. 생성한 원본 파일을 확인해 주세요.');
      return;
    }
    download.title = download.getAttribute('aria-label') === '다운로드' ? filename : download.title;
    download.hidden = false;
    download.addEventListener('click', () => {
      let url;
      try {
        url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url; link.download = filename;
        document.body.append(link); link.click(); link.remove();
        message('');
      } catch { message('다운로드하지 못했습니다. 브라우저의 다운로드 설정을 확인해 주세요.'); }
      finally { if (url) setTimeout(() => URL.revokeObjectURL(url), 30000); }
    });
    const nav = globalThis.navigator;
    if (share && globalThis.isSecureContext && nav?.share && nav?.canShare && typeof File !== 'undefined') {
      const file = new File([blob], filename, {type: blob.type});
      let supported = false;
      try { supported = nav.canShare({files: [file]}); } catch {}
      if (supported) {
        share.hidden = false;
        share.addEventListener('click', async () => {
          try { await nav.share({files: [file], title: document.title}); message(''); }
          catch (error) { if (error.name !== 'AbortError') message('공유하지 못했습니다. 다운로드 버튼으로 파일을 저장해 주세요.'); }
        });
      }
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once: true});
  else start();
})();

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
  const theme = document.querySelector('[data-ht-theme-control]');
  if (!theme) return;
  const root = document.documentElement;
  const key = 'tigerkit-html-font-size';
  const sizes = ['50', '75', '100', '125', '150', '175', '200'];
  const group = document.createElement('div');
  group.className = 'ht-reader-controls';
  const label = document.createElement('label');
  label.className = 'ht-font-control';
  const caption = document.createElement('span');
  caption.className = 'ht-visually-hidden';
  caption.textContent = '글자 크기';
  const select = document.createElement('select');
  select.setAttribute('data-ht-font-size', '');
  select.setAttribute('aria-label', '글자 크기');
  select.title = '글자 크기';
  for (const size of sizes) {
    const option = document.createElement('option');
    option.value = size;
    option.textContent = `${size}%`;
    select.append(option);
  }
  const apply = value => {
    select.value = sizes.includes(value) ? value : '100';
    root.style.setProperty('--ht-font-scale', String(Number(select.value) / 100));
  };
  let saved = '100';
  try { const value = localStorage.getItem(key); if (sizes.includes(value)) saved = value; } catch {}
  apply(saved);
  select.addEventListener('change', () => {
    apply(select.value);
    try { localStorage.setItem(key, select.value); } catch {}
  });
  label.append(caption, select);
  theme.before(group);
  group.append(label, theme);
})();

(() => {
  const nav = document.querySelector('.ht-doc-nav');
  if (!nav) return;
  const toc = nav.querySelector('.ht-doc-toc');
  const summary = toc?.querySelector('summary');
  const narrowNavigation = globalThis.matchMedia?.('(max-width: 960px)');
  const syncNavigationMode = () => { if (toc && narrowNavigation) toc.open = !narrowNavigation.matches; };
  syncNavigationMode();
  narrowNavigation?.addEventListener('change', syncNavigationMode);
  const links = [...nav.querySelectorAll('.ht-doc-toc-panel a[href^="#"]')];
  const targetFor = hash => {
    try { return document.getElementById(decodeURIComponent(hash.slice(1))); } catch { return null; }
  };
  const sections = links.map(link => targetFor(link.hash)).filter(Boolean);
  const close = (returnFocus = false) => {
    if (!toc?.open || !narrowNavigation?.matches) return;
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

(() => {
  const start = () => {
    (document.querySelectorAll?.('pre.ht-code') || []).forEach((block, index) => {
      if (block.previousElementSibling?.classList.contains('ht-code-toolbar')) return;
      const toolbar = document.createElement('div');
      toolbar.className = 'ht-code-toolbar';
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = '줄바꿈';
      button.setAttribute('aria-label', `코드 블록 ${index + 1} 줄바꿈`);
      button.setAttribute('aria-pressed', 'false');
      button.addEventListener('click', () => {
        const wrap = block.toggleAttribute('data-wrap');
        button.setAttribute('aria-pressed', String(wrap));
      });
      toolbar.append(button);
      block.before(toolbar);
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once: true});
  else start();
})();
