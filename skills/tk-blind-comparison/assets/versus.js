(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('comparison-data').textContent);
  const node = id => document.getElementById(id);
  const status = node('status');
  const roster = data.items.map(item => ({id:item.id, cards:item.cards.map(({candidate,fingerprint,failed}) => ({candidate,fingerprint,failed}))}));
  const storageKey = `tigerkit-versus:${data.study}:${data.revision}`;
  // Bound untrusted replay work, not media size. The UI preserves the last valid transcript at the limit.
  const MAX_EVENTS = 100000;
  const roundName = count => {const size = 2 ** Math.ceil(Math.log2(count)); return size === 2 ? '결승' : `${size}강`;};
  const replay = (item, events) => {
    if (!Array.isArray(events) || events.length > MAX_EVENTS) throw Error('invalid events');
    let survivors = item.cards.filter(card => !card.failed).map(card => card.candidate);
    let round = 1, cursor = 0, next = [], done = false;
    const seen = new Set(), reached = new Map();
    const incomparable = survivors.length < 2;
    const canCoWin = () => !done && !incomparable && round > 1 && cursor === 0 && survivors.every(id => seen.has(id));
    for (const event of events) {
      if (done || incomparable) throw Error('finished comparison');
      if (event === 'co-winners') {
        if (!canCoWin()) throw Error('early co-winners');
        done = true; continue;
      }
      const pair = survivors.slice(cursor,cursor+2);
      if (!['left','right','both'].includes(event) || pair.length === 1 && event !== 'left') throw Error('invalid choice');
      pair.forEach(id => {seen.add(id); reached.set(id, roundName(survivors.length));});
      next.push(...(event === 'both' ? pair : [pair[event === 'left' ? 0 : 1]]));
      cursor += pair.length;
      if (cursor === survivors.length) {
        survivors = next; next = []; cursor = 0;
        if (survivors.length === 1) done = true; else round++;
      }
    }
    if (done) for (const id of survivors) reached.set(id, survivors.length > 1 ? '공동 우승' : '우승');
    return {survivors, round, cursor, done, incomparable, reached, canCoWin:canCoWin(), pair:done || incomparable ? [] : survivors.slice(cursor,cursor+2)};
  };
  const blank = () => ({schema:1, mode:'versus', study:data.study, version:data.version, revision:data.revision,
    evaluator:globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random()}`, revealed:false, active:0,
    items:roster.map(item => ({...item, events:[]}))});
  const validate = payload => {
    if (!payload || payload.schema !== 1 || payload.mode !== 'versus' || payload.study !== data.study || payload.version !== data.version || payload.revision !== data.revision || typeof payload.evaluator !== 'string' || !payload.evaluator.trim() || typeof payload.revealed !== 'boolean' || !Number.isInteger(payload.active) || payload.active < 0 || payload.active >= roster.length || !Array.isArray(payload.items) || payload.items.length !== roster.length) throw Error('invalid comparison');
    const items = roster.map((item,index) => {
      const imported = payload.items[index];
      if (!imported || imported.id !== item.id || !Array.isArray(imported.cards) || imported.cards.length !== item.cards.length || !imported.cards.every((card,i) => card && Object.keys(card).length === 3 && card.candidate === item.cards[i].candidate && card.fingerprint === item.cards[i].fingerprint && card.failed === item.cards[i].failed)) throw Error('changed outputs');
      replay(item,imported.events);
      return {...item, events:[...imported.events]};
    });
    return {schema:1,mode:'versus',study:data.study,version:data.version,revision:data.revision,evaluator:payload.evaluator,revealed:payload.revealed,active:payload.active,items};
  };
  let state = blank(), storageReadable = true, showing = false;
  let notice = '';
  try {const raw = localStorage.getItem(storageKey); if (raw) state = validate(JSON.parse(raw));}
  catch {storageReadable = false; notice = '저장된 대결을 읽을 수 없습니다. 기존 저장값은 보존하며 JSON 내보내기를 사용해 주세요.';}
  const save = () => {
    if (!storageReadable) {notice = '브라우저 저장을 사용할 수 없습니다. 선택 JSON을 내보내 주세요.';return;}
    try {localStorage.setItem(storageKey,JSON.stringify(state));notice = '';}
    catch {notice = '브라우저 저장이 차단되거나 용량이 부족합니다. 선택 JSON을 내보내 주세요.';}
  };
  const names = () => JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(answerCode), c=>c.charCodeAt(0)))).candidates;
  const escape = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const renderResults = (item, current) => {
    const summary = node('summary'); summary.hidden = !showing;
    if (!showing) {summary.innerHTML = ''; return;}
    const publicItem = data.items[state.active], identity = names();
    const rows = publicItem.cards.map(card => {
      const stage = card.failed ? '생성 실패' : current.incomparable ? '비교 불가' : current.reached.get(card.candidate) || '미대결';
      return `<tr><th scope="row">${escape(card.label)}</th><td>${escape(identity[card.candidate].name)}</td><td>${escape(stage)}</td></tr>`;
    }).join('');
    summary.innerHTML = `<h2>${escape(publicItem.title || '비교 결과')}</h2><table><caption>선택 기록으로 재생한 도달 라운드</caption><thead><tr><th scope="col">표본</th><th scope="col">기법</th><th scope="col">도달 라운드</th></tr></thead><tbody>${rows}</tbody></table>`;
  };
  const previews = new Map();
  for (const sample of document.querySelectorAll('.sample')) {
    const content = sample.querySelector('.sample-content');
    if (!content?.dataset.htmlSrc) continue;
    const toggle = content.querySelector('.toggle-preview');
    const preview = {content, fallback:content.querySelector('.sample-fallback'), toggle,
      fallbackLabel:toggle.textContent, frame:null, active:false, useFallback:false};
    previews.set(sample, preview);
    toggle.hidden = false;
    toggle.addEventListener('click', () => {preview.useFallback = !preview.useFallback; updatePreview(preview);});
  }
  const updatePreview = preview => {
    const showFrame = preview.active && !preview.useFallback;
    if (!showFrame && preview.frame) {preview.frame.remove(); preview.frame = null;}
    if (showFrame && !preview.frame) {
      const frame = document.createElement('iframe');
      frame.title = '익명 설명 문서';
      frame.setAttribute('sandbox', 'allow-scripts allow-popups');
      frame.setAttribute('referrerpolicy', 'no-referrer');
      frame.src = preview.content.dataset.htmlSrc;
      preview.content.prepend(frame); preview.frame = frame;
    }
    preview.fallback.hidden = showFrame;
    preview.toggle.hidden = !preview.active;
    preview.toggle.textContent = preview.useFallback ? 'HTML로 보기' : preview.fallbackLabel;
  };
  const render = () => {
    const focused = document.activeElement;
    const item = state.items[state.active], current = replay(item,item.events);
    const activeIds = new Set(current.done ? current.survivors : current.incomparable ? item.cards.map(c=>c.candidate) : current.pair);
    document.querySelectorAll('section').forEach((section,index) => {section.hidden = index !== state.active || showing;});
    // Return the primary buttons before moving them into the current pair's card footers.
    node('versus-controls').append(node('choose-left'), node('choose-right'));
    for (const sample of document.querySelectorAll('.sample')) {
      const hidden = showing || sample.dataset.item !== item.id || !activeIds.has(sample.dataset.candidate);
      if (hidden && !sample.hidden) for (const media of sample.querySelectorAll('audio, video')) media.pause();
      sample.hidden = hidden;
      sample.setAttribute('tabindex','0');
      const preview = previews.get(sample);
      if (preview) {preview.active = !hidden && (current.pair.includes(sample.dataset.candidate) || current.done && current.survivors.length === 1); updatePreview(preview);}
      const side = current.pair.indexOf(sample.dataset.candidate);
      if (!hidden && side >= 0 && current.pair.length === 2) {
        sample.querySelector('.sample-choice').append(node(side === 0 ? 'choose-left' : 'choose-right'));
      }
      sample.querySelector('.identity').textContent = showing ? names()[sample.dataset.candidate].name : '';
    }
    node('choose-left').hidden = node('choose-right').hidden = current.pair.length !== 2;
    node('choose-left').disabled = current.done || current.incomparable;
    node('choose-right').disabled = current.pair.length !== 2;
    node('choose-both').disabled = current.pair.length !== 2;
    node('choose-both').hidden = showing || current.pair.length !== 2;
    node('bye').hidden = showing || current.pair.length !== 1;
    node('versus-completion').hidden = !current.done;
    node('winner-message').textContent = current.survivors.length > 1 ? '공동 우승입니다. 결과 보기를 눌러 기법과 도달 라운드를 확인해 주세요.' : '우승이 정해졌습니다. 결과 보기를 눌러 기법과 도달 라운드를 확인해 주세요.';
    node('result-reveal').textContent = showing ? '결과 가리기' : '결과 보기';
    node('co-winners').disabled = !current.canCoWin;
    node('undo').disabled = !item.events.length;
    node('previous-item').disabled = state.active === 0;
    node('next-item').disabled = state.active === roster.length-1;
    const failures = item.cards.filter(c=>c.failed).length;
    const size = 2 ** Math.ceil(Math.log2(current.survivors.length));
    const roundTitle = size === 2 ? '결승' : `${size}강`;
    const match = Math.floor(current.cursor / 2) + 1, total = Math.ceil(current.survivors.length / 2);
    const result = current.incomparable ? '비교 불가 · 성공 표본이 2개 미만입니다.' : current.done ?
      (current.survivors.length > 1 ? '공동 우승' : '우승') :
      `${roundTitle}${size === 2 ? '' : ` · ${match}/${total}`}${current.pair.length === 1 ? ' · 부전승' : ''}`;
    node('versus-progress').textContent = `${roster.length > 1 ? `항목 ${state.active+1}/${roster.length} · ` : ''}${result}${failures ? ` · 생성 실패 ${failures}개` : ''}`;
    for (const mark of document.querySelectorAll('.versus-mark')) mark.hidden = current.pair.length !== 2;
    if (focused && ['choose-left','choose-right'].includes(focused.id)) {
      (current.pair.length === 1 ? node('bye') : current.done ? node('undo') : focused).focus();
    }
    renderResults(item, current);
    status.textContent = notice; status.hidden = !notice;
    node('reveal').setAttribute('aria-pressed',String(showing)); node('reveal').textContent = showing ? '결과 가리기' : '결과 공개';
  };
  const choose = event => {
    const item=state.items[state.active], current=replay(item,item.events);
    if (event === 'co-winners' && (!current.canCoWin || !confirm('남은 후보를 모두 확인했습니다. 남은 후보 전부를 공동 1위로 확정할까요?'))) return;
    try {replay(item,[...item.events,event]);}
    catch {notice='선택을 적용하지 못했습니다. 현재 기록을 내보내 주세요.';render();return;}
    item.events.push(event);save();render();
  };
  for(const [id,event] of [['choose-left','left'],['choose-right','right'],['choose-both','both'],['co-winners','co-winners']]) node(id).addEventListener('click',()=>choose(event));
  node('bye').addEventListener('click',()=>choose('left'));
  node('result-copy').addEventListener('click',()=>node('copy').click());
  node('result-reveal').addEventListener('click',()=>node('reveal').click());
  node('undo').addEventListener('click',()=>{state.items[state.active].events.pop();save();render();});
  for(const [id,offset] of [['previous-item',-1],['next-item',1]]) node(id).addEventListener('click',()=>{const next=state.active+offset;if(next>=0 && next<roster.length){state.active=next;save();render();}});
  node('copy').addEventListener('click',async()=>{
    status.hidden=false;
    try{await navigator.clipboard.writeText(JSON.stringify(state,null,2));status.textContent='선택 JSON을 복사했습니다. 대화에 붙여 넣어 주세요.';}
    catch{status.textContent='선택을 복사하지 못했습니다. 선택 JSON 내보내기를 사용해 주세요. 기존 기록은 유지됩니다.';}
  });
  node('export').addEventListener('click',()=>{
    const url=URL.createObjectURL(new Blob([JSON.stringify(state,null,2)],{type:'application/json'})), link=document.createElement('a');
    link.href=url;link.download='blind-versus.json';document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  const input=node('import-file');
  node('import').addEventListener('click',()=>input.click());
  input.addEventListener('change',async()=>{
    status.hidden=false;
    try{
      const file=input.files[0];if(!file)return;
      const imported=validate(JSON.parse(await file.text()));
      if(state.items.some(item=>item.events.length) && imported.evaluator !== state.evaluator) throw Error('different evaluator');
      imported.revealed ||= state.revealed;state=imported;showing=false;save();render();
    }catch{status.textContent='선택 JSON을 가져오지 못했습니다. 같은 비교·버전·내용·평가자의 파일인지 확인해 주세요. 기존 기록은 유지됩니다.';}
    finally{input.value='';}
  });
  const toggleReveal = () => {
    if (!answerCode) return;
    if(!showing && !state.revealed && state.items.some(item=>!replay(item,item.events).done) && !confirm('아직 끝나지 않은 항목이 있습니다. 지금 후보 이름을 공개할까요?')) return;
    showing=!showing;if(showing){state.revealed=true;save();}render();
  };
  node('reveal').addEventListener('click',()=>{
    if (showing) {toggleReveal(); return;}
    if (globalThis.tigerkitAnswerKey) globalThis.tigerkitAnswerKey.request(toggleReveal);
    else if (answerCode) toggleReveal();
    else {status.hidden=false;status.textContent='결과를 보려면 이 비교의 정답표를 선택해 주세요.';}
  });
  node('toolbar').hidden=false;node('versus-controls').hidden=false;
  render();
})();
