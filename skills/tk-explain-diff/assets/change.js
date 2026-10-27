(() => {
  document.querySelectorAll('[data-change-flow]').forEach(flow => {
    const steps = [...flow.querySelectorAll('[data-change-step]')];
    const controls = flow.querySelector('[data-change-flow-controls]');
    if (!steps.length || !controls) return;
    let index = 0;
    const buttons = [...controls.querySelectorAll('button')];
    const show = () => {
      steps.forEach((step, i) => step.setAttribute('data-active', String(i === index)));
      buttons[0].disabled = index === 0; buttons[1].disabled = index === steps.length - 1;
    };
    buttons[0].addEventListener('click', () => { index = Math.max(0, index - 1); show(); });
    buttons[1].addEventListener('click', () => { index = Math.min(steps.length - 1, index + 1); show(); });
    buttons[2].addEventListener('click', () => { index = 0; show(); });
    controls.hidden = false; show();
  });
  document.addEventListener('click', event => {
    const link = event.target.closest?.('a[href^="#"]');
    if (!link) return;
    let target; try { target = document.getElementById(decodeURIComponent(link.hash.slice(1))); } catch { return; }
    for (let parent = target?.parentElement; parent; parent = parent.parentElement) {
      if (parent.tagName === 'DETAILS') parent.open = true;
    }
  });
})();
