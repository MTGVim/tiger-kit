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
