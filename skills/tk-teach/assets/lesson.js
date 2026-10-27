(() => {
  let focused;
  document.addEventListener('click', event => {
    const focus = event.target.closest?.('a[data-ht-focus]');
    if (focus) {
      const target = document.getElementById(focus.getAttribute('data-ht-focus'));
      if (focused) focused.classList.remove('ht-lesson-focus');
      if (target) { target.classList.add('ht-lesson-focus'); focused = target; }
    }
    const retry = event.target.closest?.('a[data-ht-retry]');
    const practice = retry?.closest('[data-ht-practice]');
    if (practice) {
      practice.querySelectorAll('details[data-ht-hint], details[data-ht-solution]').forEach(detail => { detail.open = false; });
      const added = !practice.hasAttribute('tabindex');
      if (added) practice.setAttribute('tabindex','-1');
      practice.focus({preventScroll:true});
      if (added) practice.addEventListener('blur',()=>practice.removeAttribute('tabindex'),{once:true});
    }
  });
})();
