(() => {
  const select = document.getElementById('ht-theme');
  if (!select) return;
  const root = document.documentElement;
  const key = 'tigerkit-html-theme';
  const valid = value => ['system', 'light', 'dark'].includes(value);
  const apply = value => {
    if (value === 'system') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', value);
    select.value = value;
  };
  let saved = 'system';
  try { const value = localStorage.getItem(key); if (valid(value)) saved = value; } catch {}
  apply(saved);
  select.addEventListener('change', () => {
    const value = valid(select.value) ? select.value : 'system';
    apply(value);
    try { localStorage.setItem(key, value); } catch {}
  });
  select.parentElement.hidden = false;
})();
