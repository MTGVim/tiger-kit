(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('comparison-data').textContent);
  const status = document.getElementById('status');
  const storageKey = `tigerkit-blind:${data.study}`;
  const tuple = (item, card) => `${item}/${card.candidate}/${card.fingerprint}`;
  const current = new Map(data.items.flatMap(item => item.cards.filter(card => !card.failed).map(card => [tuple(item.id, card), {item: item.id, ...card}])));
  const validKey = key => /^[a-f0-9]{32}\/[a-f0-9]{32}\/[a-f0-9]{64}$/.test(key);
  const cleanEntry = value => ({score: value.score, note: value.note, favorite: value.favorite});
  const uniqueFavorites = entries => {const seen = new Set(); return Object.entries(entries).every(([key, value]) => {if (!value.favorite) return true; const item=key.split('/')[0]; if (seen.has(item)) return false; seen.add(item); return true;});};
  const hasRatings = entries => Object.values(entries).some(value => value.score !== null || value.note || value.favorite);
  const blank = () => ({schema: 1, study: data.study, evaluator: globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random()}`, revealed: false, entries: {}});
  let state = blank();
  let showing = false;
  const validEntry = value => value && (value.score === null || Number.isInteger(value.score) && value.score >= 1 && value.score <= 5) && typeof value.note === 'string' && typeof value.favorite === 'boolean';
  let storageReadable = true;
  try {
    const raw = localStorage.getItem(storageKey);
    if (raw) {
      const saved = JSON.parse(raw);
      if (saved.schema !== 1 || saved.study !== data.study || typeof saved.evaluator !== 'string' || !saved.evaluator || typeof saved.revealed !== 'boolean' || !saved.entries || typeof saved.entries !== 'object' || Array.isArray(saved.entries) || (!Object.entries(saved.entries).every(([key, value]) => validKey(key) && validEntry(value)) || !uniqueFavorites(saved.entries))) throw new Error('invalid saved state');
      state = {...saved, entries: Object.fromEntries(Object.entries(saved.entries).map(([key, value]) => [key, cleanEntry(value)]))};
    }
  } catch {
    storageReadable = false;
    status.textContent = '저장된 평가를 읽을 수 없습니다. 기존 저장값은 보존하며 JSON 가져오기 또는 내보내기를 사용해 주세요.';
  }
  const save = () => {
    if (!storageReadable) {status.textContent = '브라우저 저장을 사용할 수 없습니다. 평가 JSON을 내보내 주세요.'; return;}
    try {localStorage.setItem(storageKey, JSON.stringify(state)); status.textContent = '평가를 이 브라우저에 저장했습니다.';}
    catch {status.textContent = '브라우저 저장이 차단되거나 용량이 부족합니다. 평가 JSON을 내보내 주세요.';}
  };
  const entry = key => state.entries[key] || {score: null, note: '', favorite: false};
  const candidateNames = () => JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(answerCode), x => x.charCodeAt(0)))).candidates;
  const renderSummary = () => {
    const box = document.getElementById('summary');
    box.replaceChildren(); box.hidden = !showing;
    if (!showing) return;
    const names = candidateNames();
    const table = document.createElement('table');
    const caption = table.createCaption(); caption.textContent = '후보별 평균 · 미평가와 생성 실패는 평균에서 제외합니다.';
    const head = table.createTHead().insertRow();
    for (const title of ['후보', '평균', '평가 수', '미평가', '실패']) {const th = document.createElement('th'); th.scope = 'col'; th.textContent = title; head.append(th);}
    const body = table.createTBody();
    for (const [token, name] of Object.entries(names)) {
      const cards = data.items.flatMap(item => item.cards.filter(card => card.candidate === token).map(card => ({...card, key: tuple(item.id, card)})));
      const values = cards.filter(card => !card.failed).map(card => entry(card.key).score).filter(value => value !== null);
      const row = body.insertRow();
      for (const value of [name.name, values.length ? (values.reduce((a,b) => a+b,0) / values.length).toFixed(2) : '미평가', values.length, cards.filter(c => !c.failed).length - values.length, cards.filter(c => c.failed).length]) row.insertCell().textContent = value;
    }
    box.append(table);
  };
  function restoreControls() {
    for (const node of document.querySelectorAll('.sample')) {
      const key = `${node.dataset.item}/${node.dataset.candidate}/${node.dataset.fingerprint}`;
      const score = node.querySelector('[data-score]');
      if (!score) continue;
      const value = entry(key);
      score.value = value.score === null ? '' : String(value.score);
      node.querySelector('[data-note]').value = value.note;
      const favorite = node.querySelector('[data-favorite]');
      if (favorite) favorite.checked = value.favorite;
    }
  }
  for (const node of document.querySelectorAll('.sample')) {
    const key = `${node.dataset.item}/${node.dataset.candidate}/${node.dataset.fingerprint}`;
    if (!current.has(key)) continue;
    node.querySelector('.rating-controls').hidden = false;
    node.addEventListener('input', event => {
      const value = {...entry(key)};
      if (event.target.matches('[data-score]')) value.score = event.target.value === '' ? null : Number(event.target.value);
      if (event.target.matches('[data-note]')) value.note = event.target.value;
      if (event.target.matches('[data-favorite]')) {
        value.favorite = event.target.checked;
        // Clear old/removed favorites too, so re-adding a candidate cannot create two winners.
        if (value.favorite) for (const [oldKey, oldValue] of Object.entries(state.entries)) if (oldKey.startsWith(`${node.dataset.item}/`)) oldValue.favorite = false;
      }
      state.entries[key] = value;
      save(); restoreControls(); renderSummary();
    });
  }
  restoreControls();
  document.getElementById('toolbar').hidden = false;
  document.getElementById('reveal').addEventListener('click', () => {
    showing = !showing;
    if (showing) {state.revealed = true; save();}
    const names = showing ? candidateNames() : null;
    for (const node of document.querySelectorAll('.sample')) node.querySelector('.identity').textContent = showing ? names[node.dataset.candidate].name : '';
    const button = document.getElementById('reveal');
    button.setAttribute('aria-pressed', String(showing)); button.textContent = showing ? '결과 가리기' : '결과 공개';
    renderSummary();
  });
  const ratingPayload = () => ({schema: 1, study: data.study, version: data.version, evaluator: state.evaluator, revealed: state.revealed,
      archive: state.entries,
      ratings: Array.from(current, ([key, card]) => ({item: card.item, candidate: card.candidate, fingerprint: card.fingerprint, ...cleanEntry(entry(key))}))});
  document.getElementById('copy').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(ratingPayload(), null, 2));
      status.textContent = '평가 JSON을 복사했습니다. 대화에 붙여 넣어 주세요.';
    } catch {
      status.textContent = '평가를 복사하지 못했습니다. 평가 JSON 내보내기를 사용해 주세요. 기존 평가는 유지됩니다.';
    }
  });
  document.getElementById('export').addEventListener('click', () => {
    const blob = new Blob([JSON.stringify(ratingPayload(), null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob); const a = document.createElement('a');
    a.href = url; a.download = 'blind-ratings.json'; document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    status.textContent = '현재 버전의 평가 JSON을 내보냈습니다.';
  });
  const input = document.getElementById('import-file');
  document.getElementById('import').addEventListener('click', () => input.click());
  input.addEventListener('change', async () => {
    try {
      const file = input.files[0]; if (!file) return;
      const payload = JSON.parse(await file.text());
      if (payload.schema !== 1 || payload.study !== data.study || typeof payload.version !== 'string' || typeof payload.evaluator !== 'string' || !payload.evaluator || typeof payload.revealed !== 'boolean' || !Array.isArray(payload.ratings)) throw new Error('invalid import');
      if (hasRatings(state.entries) && state.evaluator !== payload.evaluator) throw new Error('different evaluator');
      const archive = payload.archive === undefined ? {} : payload.archive;
      if (!archive || typeof archive !== 'object' || Array.isArray(archive) || !Object.entries(archive).every(([key, value]) => validKey(key) && validEntry(value))) throw new Error('invalid archive');
      const seen = new Set(), favorites = new Set(), imported = Object.fromEntries(Object.entries(archive).map(([key, value]) => [key, cleanEntry(value)]));
      let skipped = 0;
      for (const row of payload.ratings) {
        if (!row || !validEntry(row) || typeof row.item !== 'string' || typeof row.candidate !== 'string' || typeof row.fingerprint !== 'string') throw new Error('invalid rating');
        const key = tuple(row.item, row);
        if (seen.has(key)) throw new Error('duplicate rating'); seen.add(key);
        if (!validKey(key)) throw new Error('invalid rating identity');
        if (!current.has(key)) skipped++;
        if (row.favorite) {if (favorites.has(row.item)) throw new Error('duplicate favorite'); favorites.add(row.item);}
        imported[key] = {score: row.score, note: row.note, favorite: row.favorite};
      }
      if (!uniqueFavorites(imported)) throw new Error('duplicate archived favorite');
      // Keep removed/changed outputs in the backup; only exact current fingerprints render.
      // Import is single-evaluator, never a multi-rater merge.
      const favoriteItems = new Set(Object.entries(imported).filter(([,v]) => v.favorite).map(([key]) => key.split('/')[0]));
      for (const [key, value] of Object.entries(state.entries)) if (favoriteItems.has(key.split('/')[0])) value.favorite = false;
      state.entries = {...state.entries, ...imported}; state.evaluator = payload.evaluator;
      state.revealed ||= payload.revealed;
      save(); restoreControls(); renderSummary();
      status.textContent += ` 평가 ${Object.keys(imported).length}개를 보존했습니다. 현재 비교에 없는 출력 ${skipped}개는 백업에만 유지됩니다.`;
    } catch (error) {status.textContent = error.message === 'different evaluator' ? '다른 평가자의 결과를 기존 평가와 합칠 수 없습니다. 비어 있는 별도 브라우저 프로필에서 가져와 주세요.' : '평가 JSON을 가져오지 못했습니다. 같은 비교의 올바른 파일인지 확인해 주세요. 기존 평가는 유지됩니다.';}
    finally {input.value = '';}
  });
})();
