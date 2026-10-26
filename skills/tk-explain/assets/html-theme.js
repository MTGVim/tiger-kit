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
    download.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M4 16v4h16v-4"/></svg>';
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
    if (share && globalThis.location?.protocol !== 'file:' && globalThis.isSecureContext && nav?.share && nav?.canShare && typeof File !== 'undefined') {
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
  const citations = [...(document.querySelectorAll?.('.ht-document a[href^="#"]') || [])].filter(link => {
    let target;
    try { target = document.getElementById(decodeURIComponent(link.hash.slice(1))); } catch { return false; }
    return target && (link.hasAttribute('data-ht-preview') || link.closest('[data-ht-backlinks]') || target.matches('dt[id], li[id], sup[id^="cite-"]'));
  });
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
    if (!reference) return;
    const plain = element => {
      const copy = element.cloneNode(true);
      for (const back of copy.querySelectorAll('a[href^="#cite-"], [data-ht-backlinks], .ht-backlink-current, .ht-external-mark')) back.remove();
      return copy.textContent.replace(/\s+/g, ' ').trim();
    };
    const clip = (text, length) => text.length > length ? text.slice(0, length).trimEnd() + '…' : text;
    let title = '', text = '';
    if (reference.matches('dt')) {
      title = plain(reference);
      let next = reference.nextElementSibling;
      while (next?.matches('dt')) next = next.nextElementSibling;
      while (next?.matches('dd')) { text += ' ' + plain(next); next = next.nextElementSibling; }
    } else if (link.closest('[data-ht-backlinks]') || reference.matches('sup[id^="cite-"]')) {
      title = reference.closest('section')?.querySelector('h2,h3,h4,h5,h6')?.textContent || '';
      const context = reference.closest('p,li,td,dd,figcaption,blockquote') || reference;
      text = plain(context);
      if (text.length > 200 && context !== reference) {
        const before = document.createRange();
        before.selectNodeContents(context);
        before.setEndBefore(reference);
        const offset = plain(before.cloneContents()).length;
        const start = Math.max(0, offset - 80);
        text = (start ? '…' : '') + text.slice(start);
      }
    } else {
      const heading = reference.querySelector('h2,h3,h4,h5,h6,a:not([href^="#"])');
      title = heading ? plain(heading) : '';
      text = plain(reference);
      if (title && text.startsWith(title)) text = text.slice(title.length).trim();
    }
    if (!title.trim() && !text.trim()) return;
    hide();
    active = link;
    preview.replaceChildren();
    if (title.trim()) {
      const heading = document.createElement('strong');
      heading.className = 'ht-preview-title';
      heading.textContent = clip(title.trim(), 80);
      preview.append(heading);
    }
    const summary = document.createElement('span');
    summary.textContent = clip(text.trim(), 200);
    preview.append(summary);
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
  // The authored numbers and hrefs work without JS; only the recent origin is transient.
  const root = document.querySelector('.ht-document');
  if (!root) return;
  const groups = [...root.querySelectorAll('[data-ht-backlinks]')];
  if (!groups.length) return;
  const targetOf = link => {
    try { return document.getElementById(decodeURIComponent(link.hash.slice(1))); }
    catch { return null; }
  };
  let marked = null, destination = null, originalLabel = null;
  const clear = () => {
    if (marked) {
      marked.querySelector('.ht-backlink-current')?.remove();
      if (originalLabel === null) marked.removeAttribute('aria-label');
      else marked.setAttribute('aria-label', originalLabel);
    }
    marked = destination = null;
  };
  root.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.hasAttribute('download') || (link.target && link.target !== '_self')) return;
    clear();
    if (link.closest('[data-ht-backlinks]')) return;
    const target = targetOf(link);
    if (!target) return;
    for (const group of groups) {
      if (group.getAttribute('data-ht-backlinks') !== target.id) continue;
      const backlinks = [...group.querySelectorAll('a[href^="#"]')];
      if (backlinks.length < 2) continue;
      const back = backlinks.find(back => {
        const origin = targetOf(back);
        return origin === link || (origin?.matches('sup') && origin.contains(link));
      });
      if (!back) continue;
      marked = back; destination = target;
      originalLabel = back.getAttribute('aria-label');
      const label = originalLabel || back.textContent.trim();
      const marker = document.createElement('span');
      marker.className = 'ht-backlink-current';
      marker.textContent = ' · 읽던 곳';
      back.append(marker);
      back.setAttribute('aria-label', label + ' · 읽던 곳');
      break;
    }
  });
  addEventListener('hashchange', () => {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { clear(); return; }
    if (destination?.id !== id) clear();
  });
  addEventListener('pageshow', event => { if (event.persisted) clear(); });
})();

(() => {
  const start = () => {
    (document.querySelectorAll?.('pre.ht-code') || []).forEach((block, index) => {
      if (block.previousElementSibling?.classList.contains('ht-code-toolbar')) return;
      const toolbar = document.createElement('div');
      toolbar.className = 'ht-code-toolbar';
      const label = document.createElement('span');
      label.className = 'ht-code-label';
      label.textContent = block.getAttribute('data-label') || block.getAttribute('data-language') || `코드 ${index + 1}`;
      const iconButton = (name, paths) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.title = name;
        button.setAttribute('aria-label', name);
        button.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true">${paths}</svg>`;
        return button;
      };
      const copy = iconButton(`코드 블록 ${index + 1} 복사`, '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V4H4v12h4"/>');
      copy.setAttribute('data-ht-copy', '');
      const status = document.createElement('span');
      status.className = 'ht-visually-hidden';
      status.setAttribute('aria-live', 'polite');
      copy.addEventListener('click', async () => {
        const text = (block.querySelector('code') || block).textContent;
        let success = false;
        try { await navigator.clipboard.writeText(text); success = true; } catch {
          // Local files may deny Clipboard API; never trim the source or steal focus.
          const focus = document.activeElement;
          const selection = document.getSelection();
          const ranges = selection ? Array.from({length: selection.rangeCount}, (_, i) => selection.getRangeAt(i).cloneRange()) : [];
          const area = document.createElement('textarea');
          area.value = text;
          area.className = 'ht-visually-hidden';
          document.body.append(area);
          try { area.select(); success = document.execCommand('copy'); } catch {} finally {
            area.remove();
            focus?.focus({preventScroll: true});
            if (selection) { selection.removeAllRanges(); for (const range of ranges) selection.addRange(range); }
          }
        }
        status.textContent = success ? '코드를 복사했습니다.' : '복사하지 못했습니다. 코드를 선택해서 복사해 주세요.';
      });
      const button = iconButton(`코드 블록 ${index + 1} 줄바꿈`, '<path d="M3 5h18M3 10h13a4 4 0 0 1 0 8h-4m3-3-3 3 3 3M3 16h4"/>');
      button.setAttribute('aria-pressed', String(block.hasAttribute('data-wrap')));
      button.addEventListener('click', () => {
        const wrap = block.toggleAttribute('data-wrap');
        button.setAttribute('aria-pressed', String(wrap));
      });
      toolbar.append(label, copy, button, status);
      block.before(toolbar);
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once: true});
  else start();
})();

(() => {
  const root = document.querySelector('.ht-document');
  if (!root) return;
  root.setAttribute('data-ht-anchor-cues', '');
  let active = [], hold, fade;
  const clear = () => {
    clearTimeout(hold); clearTimeout(fade);
    for (const item of active) item.classList.remove('ht-arrival', 'ht-arrival-fade');
    active = [];
  };
  const settled = () => {
    if (!active.length) return;
    clearTimeout(hold); clearTimeout(fade);
    for (const item of active) item.classList.remove('ht-arrival-fade');
    // Every scroll event restarts the quiet period, including nested scrollers.
    hold = setTimeout(() => {
      for (const item of active) item.classList.add('ht-arrival-fade');
      fade = setTimeout(clear, 450);
    }, 1100);
  };
  const show = hash => {
    clear();
    let target;
    try { target = document.getElementById(decodeURIComponent(hash.slice(1))); } catch { return; }
    if (!target || !root.contains(target)) return;
    const heading = target.matches('section,article,main,header,footer') ? target.querySelector('h1,h2,h3,h4,h5,h6') : null;
    // Never frame a whole section (or the whole page).
    if (target === root || target.matches('section,article,main,header,footer') && !heading) return;
    active = [heading || target];
    if (target.matches('dt')) {
      let next = target.nextElementSibling;
      while (next?.matches('dd')) { active.push(next); next = next.nextElementSibling; }
    }
    for (const item of active) item.classList.add('ht-arrival');
    settled();
  };
  document.addEventListener('click', event => {
    const link = event.target.closest?.('a[href^="#"]');
    clear();
    if (link && !event.defaultPrevented && event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey) show(link.hash);
  });
  document.addEventListener('scroll', settled, {passive: true, capture: true});
  addEventListener('hashchange', () => show(location.hash));
  if (location.hash) show(location.hash);

  for (const link of root.querySelectorAll('a[href]')) {
    let url;
    try { url = new URL(link.getAttribute('href'), document.baseURI); } catch { continue; }
    if (!['http:', 'https:'].includes(url.protocol) || url.origin === location.origin) continue;
    link.target = '_blank';
    link.relList.add('noopener', 'noreferrer');
    const mark = document.createElement('span');
    mark.className = 'ht-external-mark';
    mark.innerHTML = '<span aria-hidden="true"> ↗</span><span class="ht-visually-hidden"> (새 탭에서 열림)</span>';
    link.append(mark);
    const label = link.getAttribute('aria-label');
    if (label) link.setAttribute('aria-label', label + ' (새 탭에서 열림)');
  }
})();
