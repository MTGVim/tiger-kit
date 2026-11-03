/* Shared list-item editor. Callers own persistence, timestamps and list rendering. */
(() => {
  if (window.TigerKitFeedback) return;
  let activeEditor = null;
  function bindSubmitKey(textarea, action) {
    let pending = false, cancelled = false;
    textarea.addEventListener('compositionend', () => {
      if (pending) { pending = false; setTimeout(() => { if (!cancelled && textarea.isConnected) action(); }, 0); }
    });
    textarea.addEventListener('keydown', event => {
      if (event.key !== 'Enter' || !(event.metaKey || event.ctrlKey)) return;
      event.preventDefault(); event.stopImmediatePropagation();
      if (event.isComposing || event.keyCode === 229) { pending = true; textarea.blur(); }
      else if (!cancelled) action();
    }, true);
    return () => { cancelled = true; pending = false; };
  }
  function edit({host, textElement, trigger, item, commit, notify}) {
    if (activeEditor?.isConnected) { notify('수정 중인 피드백을 먼저 저장하거나 취소하세요.'); return; }
    if (host.querySelector('[data-feedback-editor]')) return;
    const box = document.createElement('div'); box.dataset.feedbackEditor = '';
    activeEditor = box;
    const area = document.createElement('textarea'); area.value = item.text;
    area.setAttribute('aria-label', '피드백 수정');
    area.style.cssText = 'width:100%;min-height:70px;box-sizing:border-box;font:inherit;color:inherit;background:transparent';
    const row = document.createElement('div'); row.style.cssText = 'display:flex;gap:6px;justify-content:flex-end;flex-wrap:wrap';
    const save = document.createElement('button'), cancel = document.createElement('button');
    save.type = cancel.type = 'button'; save.textContent = '저장'; cancel.textContent = '취소';
    const hint = document.createElement('small'); hint.textContent = '⌘/Ctrl+Enter 저장 · Esc 취소';
    let cancelPending = () => {};
    const done = () => { cancelPending(); activeEditor = null; box.remove(); textElement.hidden = false; trigger.disabled = false; trigger.focus(); };
    const submit = () => {
      if (!box.isConnected) return;
      const value = area.value.trim();
      if (!value) { notify('지우려면 삭제를 누르세요.'); area.focus(); return; }
      cancelPending(); activeEditor = null; item.text = value; item.edited_at = new Date().toISOString(); commit();
    };
    cancelPending = bindSubmitKey(area, submit);
    area.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !event.isComposing && event.keyCode !== 229) {
        event.preventDefault(); event.stopPropagation(); done();
      }
    });
    save.addEventListener('click', submit); cancel.addEventListener('click', done);
    row.append(hint, cancel, save); box.append(area, row);
    textElement.hidden = true; trigger.disabled = true; host.append(box); area.focus();
  }
  window.TigerKitFeedback = {bindSubmitKey, edit};
})();
