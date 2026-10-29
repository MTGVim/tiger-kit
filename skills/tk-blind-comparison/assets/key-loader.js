(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('comparison-data').textContent);
  const input = document.getElementById('key-file');
  const status = document.getElementById('status');
  document.getElementById('load-key').addEventListener('click', () => input.click());
  input.addEventListener('change', async () => {
    status.hidden = false;
    try {
      const file = input.files[0]; if (!file) return;
      const key = JSON.parse(await file.text());
      const expected = data.items.flatMap(item => item.cards.map(card => [item.id, card.candidate, card.fingerprint, card.failed]));
      if (key.schema !== 1 || key.study !== data.study || key.version !== data.version || !Array.isArray(key.outputs) || key.outputs.length !== expected.length || !key.candidates || typeof key.candidates !== 'object') throw Error('invalid key');
      const actual = new Set(key.outputs.map(row => JSON.stringify([row.item, row.candidate, row.fingerprint, row.failed])));
      if (actual.size !== expected.length || !expected.every(row => actual.has(JSON.stringify(row)) && typeof key.candidates[row[1]]?.name === 'string')) throw Error('stale key');
      // The explicitly selected key stays in memory, never in browser storage or exports.
      const bytes = new TextEncoder().encode(JSON.stringify({candidates: key.candidates}));
      let binary = ''; for (const byte of bytes) binary += String.fromCharCode(byte);
      answerCode = btoa(binary);
      document.getElementById('reveal').disabled = false;
      status.textContent = '일치하는 정답표를 읽었습니다. 결과 공개를 누르기 전까지 이름은 가립니다.';
    } catch {
      status.textContent = '정답표를 읽지 못했습니다. 같은 비교·버전·내용의 파일인지 확인해 주세요. 기존 기록은 유지됩니다.';
    } finally {input.value = '';}
  });
})();
