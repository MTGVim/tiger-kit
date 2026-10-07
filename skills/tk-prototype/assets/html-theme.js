(() => {
  const control = document.querySelector('[data-ht-theme-control]');
  if (!control) return;
  const buttons = [...control.querySelectorAll('[data-theme-choice]')];
  if (!buttons.length) return;
  const root = document.documentElement;
  const key = 'tigerkit-html-theme';
  const valid = value => ['system', 'light', 'dark'].includes(value);
  const configuredValue = root.getAttribute('data-default-theme');
  const configured = valid(configuredValue) ? configuredValue : 'system';
  const apply = value => {
    if (value === 'system') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', value);
    for (const button of buttons) {
      button.setAttribute('aria-pressed', button.dataset.themeChoice === value ? 'true' : 'false');
    }
  };
  let saved = configured;
  try { const value = localStorage.getItem(key); if (valid(value)) saved = value; } catch {}
  apply(saved);
  for (const button of buttons) {
    button.addEventListener('click', () => {
      const value = valid(button.dataset.themeChoice) ? button.dataset.themeChoice : 'system';
      apply(value);
      try { localStorage.setItem(key, value); } catch {}
    });
  }
  control.hidden = false;
})();
