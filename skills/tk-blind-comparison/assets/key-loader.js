(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('comparison-data').textContent);
  const input = document.getElementById('key-file');
  const status = document.getElementById('status');
  let pendingReveal = null;
  const notice = message => {status.hidden = false; status.textContent = message;};
  const accept = key => {
    const expected = data.items.flatMap(item => item.cards.map(card => [item.id, card.candidate, card.fingerprint, card.failed]));
    if (!key || key.schema !== 1 || key.study !== data.study || key.version !== data.version || !Array.isArray(key.outputs) || key.outputs.length !== expected.length || !key.candidates || typeof key.candidates !== 'object') throw Error('invalid key');
    if (data.mode === 'versus' && key.comparison?.revision !== data.revision) throw Error('stale revision');
    const actual = new Set(key.outputs.map(row => JSON.stringify([row.item, row.candidate, row.fingerprint, row.failed])));
    if (actual.size !== expected.length || !expected.every(row => actual.has(JSON.stringify(row)) && typeof key.candidates[row[1]]?.name === 'string' && key.candidates[row[1]].name.trim())) throw Error('stale key');
    const bytes = new TextEncoder().encode(JSON.stringify({candidates: key.candidates}));
    let binary = ''; for (const byte of bytes) binary += String.fromCharCode(byte);
    answerCode = btoa(binary);
    document.getElementById('reveal').disabled = false;
  };
  const request = callback => {
    if (answerCode) {callback(); return;}
    if (typeof embeddedAnswerKeyCode === 'string' && embeddedAnswerKeyCode) {
      try {
        const bytes = Uint8Array.from(atob(embeddedAnswerKeyCode), c => c.charCodeAt(0));
        accept(JSON.parse(new TextDecoder().decode(bytes)));
        callback();
      } catch {notice('내장 정답표를 검증하지 못했습니다. 같은 비교의 정답표를 관리 메뉴에서 선택해 주세요.');}
      return;
    }
    pendingReveal = callback;
    notice('정답표는 표본과 기법을 연결하는 파일이며, 다른 평가자에게 미리 노출되지 않도록 분리했습니다. 이 비교의 answer-key.json을 골라 주세요.');
    input.click();
  };
  // Both embedded and explicitly selected keys use the same roster/revision validation.
  globalThis.tigerkitAnswerKey = {request};
  document.getElementById('load-key').addEventListener('click', () => {pendingReveal = null; input.click();});
  input.addEventListener('cancel', () => {pendingReveal = null;});
  input.addEventListener('change', async () => {
    const callback = pendingReveal; pendingReveal = null;
    try {
      const file = input.files[0]; if (!file) return;
      accept(JSON.parse(await file.text()));
      notice('일치하는 정답표를 읽었습니다. 결과 공개를 누르기 전까지 이름은 가립니다.');
      if (callback) callback();
    } catch {notice('정답표를 읽지 못했습니다. 같은 비교·버전·내용의 파일인지 확인해 주세요. 기존 기록은 유지됩니다.');}
    finally {input.value = '';}
  });
})();
