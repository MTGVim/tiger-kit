/* report.js: 테마 버튼, 좁은 화면의 목차 메뉴, 목차의 현재 절 표시, 막대의 제목 표시만 한다. 외부 요청 없음. */
(function () {
  // 테마: studio 가 먼저 붙었으면 건드리지 않는다. 저장 키와 마크업은 studio 와 같다.
  function theme() {
    if (window.__tigerkitTheme) return;
    var root = document.documentElement, key = 'archify-theme';
    var control = document.querySelector('[data-ht-theme-control]');
    if (!control) return;
    var box = control.querySelector('.ht-theme-buttons');
    var labels = { system: '시스템', light: '밝게', dark: '어둡게' };
    box.textContent = '';
    ['system', 'light', 'dark'].forEach(function (v) {
      var label = document.createElement('label'); label.className = 'ht-theme-option';
      var input = document.createElement('input'); input.type = 'radio'; input.name = 'ht-theme'; input.value = v; input.setAttribute('aria-label', labels[v]);
      var span = document.createElement('span'); span.textContent = labels[v];
      label.appendChild(input); label.appendChild(span); box.appendChild(label);
    });
    var inputs = [].slice.call(box.querySelectorAll('input'));
    function apply(v) {
      if (['system', 'light', 'dark'].indexOf(v) < 0) v = 'system';
      if (v === 'system') root.removeAttribute('data-theme'); else root.setAttribute('data-theme', v);
      inputs.forEach(function (i) { i.checked = i.value === v; });
    }
    var saved = 'system';
    try { var s = localStorage.getItem(key); if (s === 'auto') s = 'system'; if (s) saved = s; } catch (e) {}
    window.__tigerkitTheme = { apply: apply, key: key };
    apply(saved);
    inputs.forEach(function (i) {
      i.addEventListener('change', function () { apply(i.value); try { localStorage.setItem(key, i.value); } catch (e) {} });
    });
    control.hidden = false;
  }
  function toc() {
    var links = [].slice.call(document.querySelectorAll('.toc a'));
    if (!('IntersectionObserver' in window) || !links.length) return;
    var secs = links.map(function (a) { return document.getElementById(a.hash.slice(1)); });
    function set(id) {
      links.forEach(function (a) { if (a.hash === '#' + id) a.setAttribute('aria-current', 'location'); else a.removeAttribute('aria-current'); });
    }
    secs = secs.filter(Boolean);
    if (!secs.length) return;
    var vis = {};
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { vis[e.target.id] = e.isIntersecting; });
      for (var i = 0; i < secs.length; i++) if (vis[secs[i].id]) { set(secs[i].id); return; }
    }, { rootMargin: '-10% 0px -70% 0px' });
    secs.forEach(function (s) { io.observe(s); });
    set(secs[0].id);
  }
  // 좁은 화면: 목차는 <details> 드롭다운. 넓은 화면은 summary 가 숨겨지므로 항상 펼쳐 둔다(경계는 CSS 한 곳).
  function menu() {
    var d = document.querySelector('.rp-bar .toc details'); if (!d) return;
    var s = d.querySelector('summary');
    function wide() { return getComputedStyle(s).display === 'none'; }
    function sync() { s.setAttribute('aria-expanded', d.open); }
    function close(focus) { if (!wide() && d.open) { d.open = false; if (focus) s.focus(); } }
    var was = wide(); d.open = was; sync();
    d.addEventListener('toggle', sync);
    window.addEventListener('resize', function () { var w = wide(); if (w !== was) { was = w; d.open = w; } });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(true); });
    document.addEventListener('click', function (e) { if (!d.contains(e.target) || e.target.closest('a')) close(false); });
  }
  // 본문 제목이 막대 위로 지나가면 표시한다.
  function title() {
    var t = document.querySelector('.rp-title'), h = document.querySelector('.page > header h1');
    if (!t || !h || !('IntersectionObserver' in window)) return;
    var bar = document.querySelector('.rp-tools');
    var top = bar ? Math.round(bar.getBoundingClientRect().height) : 0;
    new IntersectionObserver(function (es) {
      var e = es[0], gone = !e.isIntersecting && e.boundingClientRect.top < top;
      if (gone) t.setAttribute('data-shown', ''); else t.removeAttribute('data-shown');
    }, { rootMargin: '-' + top + 'px 0px 0px 0px' }).observe(h);
  }
  function start() { theme(); menu(); toc(); title(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true }); else start();
})();

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
(function () {
  function fontSize() {
    if (document.querySelector('[data-ht-font-size]')) return;
    var theme = document.querySelector('.rp-tools [data-ht-theme-control]');
    if (!theme) return;
    var label = document.createElement('label'); label.className = 'ht-font-control';
    label.appendChild(document.createTextNode('글자 크기 '));
    var select = document.createElement('select'); select.setAttribute('data-ht-font-size', '');
    [75, 100, 125, 150].forEach(function (n) { var option = document.createElement('option'); option.value = String(n); option.textContent = n + '%'; if (n === 100) option.selected = true; select.appendChild(option); });
    select.addEventListener('change', function () { document.documentElement.style.setProperty('--ht-font-scale', String(Number(select.value) / 100)); });
    label.appendChild(select); theme.parentNode.insertBefore(label, theme);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fontSize, {once:true}); else fontSize();
})();
