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
