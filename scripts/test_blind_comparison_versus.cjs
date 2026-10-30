const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
// Keep the model real; only browser-owned DOM/storage/clipboard boundaries are doubled.
const sourcePath = path.join(__dirname, '../skills/tk-blind-comparison/assets/versus.js');
function runtime(count = 5, options = {}) {
  const handlers = {}, nodes = {}, cards = Array.from({length: count}, (_, i) => ({candidate: String(i + 1).repeat(32), fingerprint: String(i + 1).repeat(64), failed: options.failed?.includes(i) || false}));
  const data = {schema:1, mode:'versus', study:'study', version:'1', revision:'revision', items:Array.from({length:options.itemCount || 1},(_,i)=>({id:String.fromCharCode(97+i).repeat(32),cards}))};
  const node = name => nodes[name] ||= {hidden:true, disabled:false, textContent:'', value:'', setAttribute() {}, append() {}, click() {handlers[name + ':click']?.();}, remove() {},
    addEventListener: (event, callback) => {handlers[name + ':' + event] = callback;}};
  node('comparison-data').textContent = JSON.stringify(data);
  const samples = data.items.flatMap(item => cards.map((card,index) => ({
    hidden:false, dataset:{item:item.id, candidate:card.candidate}, setAttribute(){},
    media:options.media ? [{tagName:index % 2 ? 'VIDEO' : 'AUDIO', paused:true, currentTime:7,
      pause(){this.paused=true;}}] : [],
    querySelectorAll(selector){return selector === 'audio, video' ? this.media : [];},
    querySelector: selector => selector === '.sample-content' ? null : node(item.id + card.candidate + ':' + selector)
  })));
  const sections = data.items.map(item => ({hidden:false,querySelectorAll:()=>samples.filter(s=>s.dataset.item===item.id)}));
  let stored = options.raw || null, download, copied, writes = 0;
  const confirms = [];
  const context = {
    document:{getElementById:node, querySelectorAll: selector => selector === 'section' ? sections : selector === '.sample' ? samples : [], createElement:()=>node('download'), body:{append(){}}},
    localStorage:{getItem:()=>{if(options.storageDenied) throw Error(); return stored;},setItem:(_, value)=>{if(options.storageDenied) throw Error(); stored=value; writes++;}},
    crypto:{randomUUID:()=>options.evaluator || 'human'}, Blob, URL:{createObjectURL:blob=>{download=blob;return 'blob:test';},revokeObjectURL(){}}, setTimeout(){},
    navigator:{clipboard:{writeText:async value=>{if(options.clipboardDenied) throw Error();copied=value;}}},
    confirm: message=>{confirms.push(message);return options.confirm !== false;}, answerCode:options.answerCode || '',
    atob:value=>Buffer.from(value,'base64').toString('binary'), btoa:value=>Buffer.from(value,'binary').toString('base64'), TextEncoder, TextDecoder, Uint8Array
  };
  const key={schema:1,study:data.study,version:data.version,comparison:{revision:data.revision},candidates:Object.fromEntries(cards.map((card,i)=>[card.candidate,{name:options.unsafeName && i===0 ? '<img onerror=bad()>' : `Technique ${i+1}`} ])),outputs:data.items.flatMap(item=>item.cards.map(card=>({item:item.id,...card})))};
  if(options.loader){context.embeddedAnswerKeyCode=options.embedded ? Buffer.from(JSON.stringify(options.badKey?{...key,comparison:{revision:'stale'}}:key)).toString('base64') : '';vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(__dirname,'../skills/tk-blind-comparison/assets/key-loader.js'),'utf8'),context);vm.runInContext(fs.readFileSync(sourcePath,'utf8'),context);}
  else vm.runInNewContext(fs.readFileSync(sourcePath,'utf8'),context);
  return {data,cards,samples,nodes,confirms,key,
    async keyFile(value){node('key-file').files=[{text:async()=>JSON.stringify(value)}];await handlers['key-file:change']();},
    cancelKey(){handlers['key-file:cancel']();},
    click(name){assert.equal(typeof handlers[name+':click'], 'function', `missing ${name} action`);handlers[name+':click']();},
    async export(){this.click('export');return JSON.parse(await download.text());},
    async copy(){await handlers['copy:click']();return copied && JSON.parse(copied);},
    async import(value){node('import-file').files=[{text:async()=>typeof value === 'string' ? value : JSON.stringify(value)}]; await handlers['import-file:change']();},
    get stored(){return stored;},get writes(){return writes;},get status(){return node('status').textContent || node('versus-progress').textContent;},
    visible(){return samples.filter(s=>!s.hidden).map(s=>s.dataset.candidate);}
  };
}

test('odd bracket keeps both, exposes each survivor, confirms co-winners only at later round start and undo replays', async () => {
  const app = runtime();
  assert.equal(app.visible().length, 2);
  assert.equal(app.nodes['co-winners'].disabled, true);
  app.click('choose-both'); app.click('choose-both');
  assert.equal(app.visible().length, 1, 'odd bye must be shown, not silently skipped');
  assert.equal(app.nodes['choose-right'].disabled, true);
  app.click('choose-left');
  assert.equal(app.nodes['co-winners'].disabled, false);
  const round2 = await app.export();
  app.click('co-winners');
  const done = await app.export();
  assert.equal(done.items[0].events.at(-1), 'co-winners');
  assert.equal(app.confirms.length, 1);
  assert.match(app.status, /共同|공동/);
  app.click('undo');
  assert.deepEqual((await app.export()).items, round2.items);
  assert.equal(app.nodes['co-winners'].disabled, false);
  const reload = runtime(5, {raw:app.stored});
  assert.deepEqual((await reload.export()).items, round2.items);
  assert.deepEqual(reload.visible(), app.visible());
});

test('repeated both is finite per click, never forces a winner, and single choices finish undoably', async () => {
  const app = runtime(2);
  for(let i=0;i<20;i++) app.click('choose-both');
  assert.equal(app.visible().length, 2);
  assert.equal((await app.export()).items[0].events.length, 20);
  app.click('choose-left');
  const finished = await app.export();
  assert.match(app.status, /우승/);
  app.click('undo');
  assert.equal(app.visible().length, 2);
  assert.equal((await app.export()).items[0].events.length, finished.items[0].events.length-1);
});

test('failures remain in export, zero/one success is incomparable, and storage/clipboard failure retains choices', async () => {
  for(const failed of [[0,1,2],[0,1]]) {
    const app=runtime(3,{failed});
    assert.match(app.status,/비교 불가/);
    assert.equal(app.nodes['choose-left'].disabled,true);
    assert.equal((await app.export()).items[0].cards.filter(c=>c.failed).length,failed.length);
  }
  const app=runtime(3,{failed:[0],storageDenied:true,clipboardDenied:true});
  app.click('choose-both');
  const before=await app.export();
  assert.equal(await app.copy(),undefined);
  assert.match(app.status,/내보내기/);assert.equal(app.nodes.status.hidden,false);
  assert.deepEqual(await app.export(),before);
  assert.equal(app.writes,0);
});

test('malformed/stale/foreign-evaluator imports never mutate current or saved choices', async () => {
  const app=runtime(3); app.click('choose-left'); const valid=await app.export(); const raw=app.stored;
  const variants=['broken', {...valid,study:'other'}, {...valid,version:'2'}, {...valid,revision:'changed'}, {...valid,evaluator:''}, {...valid,evaluator:'other'}, {...valid,revealed:'yes'}];
  const altered=structuredClone(valid); altered.items[0].cards[0].fingerprint='stale'; variants.push(altered);
  const illegal=structuredClone(valid);illegal.items[0].events=['co-winners'];variants.push(illegal);
  const runaway=structuredClone(valid);runaway.items[0].events=Array(100001).fill('both');variants.push(runaway);
  for(const input of variants){await app.import(input); assert.equal(app.nodes.status.hidden,false);assert.deepEqual(await app.export(),valid);assert.equal(app.stored,raw);}
  const receiver=runtime(3,{evaluator:'fresh'}); await receiver.import(valid);
  assert.deepEqual(await receiver.export(),valid);
  assert.deepEqual(await receiver.copy(),valid);
});

test('cancelled co-winner confirmation leaves transcript and storage unchanged', async () => {
  const app=runtime(2,{confirm:false});app.click('choose-both');const before=await app.export(), raw=app.stored;
  app.click('co-winners');assert.equal(app.confirms.length,1);assert.deepEqual(await app.export(),before);assert.equal(app.stored,raw);
});

test('corrupt saved state is not overwritten and later-round partial progress cannot finalize co-winners', async () => {
  const app=runtime(5,{raw:'corrupt'});app.click('choose-both');
  assert.equal(app.stored,'corrupt');assert.equal(app.writes,0);assert.equal((await app.export()).items[0].events.length,1);
  const fresh=runtime(5);fresh.click('choose-both');fresh.click('choose-both');fresh.click('choose-left');fresh.click('choose-left');
  assert.equal(fresh.nodes['co-winners'].disabled,true);
  const before=await fresh.export();fresh.click('co-winners');assert.deepEqual(await fresh.export(),before);assert.equal(fresh.confirms.length,0);
});

test('external answer key validates full output roster before enabling reveal and never persists names', async () => {
  const handlers={},nodes={};
  const node=id=>nodes[id] ||= {disabled:id==='reveal',hidden:true,value:'',textContent:'',addEventListener:(event,callback)=>{handlers[id+':'+event]=callback;},click(){}};
  const item='a'.repeat(32), candidate='b'.repeat(32), fingerprint='c'.repeat(64);
  const data={study:'study',version:'1',items:[{id:item,cards:[{candidate,fingerprint,failed:false}]}]};
  node('comparison-data').textContent=JSON.stringify(data);
  const context={document:{getElementById:node},TextEncoder,answerCode:'',btoa:value=>Buffer.from(value,'binary').toString('base64')};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../skills/tk-blind-comparison/assets/key-loader.js'),'utf8'),context);
  const key={schema:1,study:'study',version:'1',candidates:{[candidate]:{name:'숨긴 기법'}},outputs:[{item,candidate,fingerprint,failed:false}]};
  for(const invalid of ['broken',{...key,study:'other'},{...key,version:'2'},{...key,outputs:[{...key.outputs[0],fingerprint:'changed'}]}]){
    node('key-file').files=[{text:async()=>typeof invalid==='string'?invalid:JSON.stringify(invalid)}];await handlers['key-file:change']();assert.equal(node('reveal').disabled,true);assert.equal(context.answerCode,'');assert.equal(node('status').hidden,false);
  }
  node('key-file').files=[{text:async()=>JSON.stringify(key)}];await handlers['key-file:change']();
  assert.equal(node('reveal').disabled,false);assert.match(node('status').textContent,/공개를 누르기 전/);
  assert.equal(JSON.parse(Buffer.from(context.answerCode,'base64').toString()).candidates[candidate].name,'숨긴 기법');
});


test('items keep independent transcripts, navigation and reload restore active item', async () => {
  const app=runtime(3,{itemCount:2});app.click('choose-left');const first=(await app.export()).items[0];
  app.click('next-item');assert.equal((await app.export()).active,1);assert.equal(app.visible().length,2);
  app.click('choose-both');assert.deepEqual((await app.export()).items[0],first);
  const before=await app.export();const reload=runtime(3,{itemCount:2,raw:app.stored});assert.deepEqual(await reload.export(),before);
  app.click('previous-item');assert.equal((await app.export()).active,0);assert.equal(app.visible().length,1);
});

test('reveal requires a loaded key, partial confirmation and never resets exposure on undo/import', async () => {
  const keyCode=Buffer.from(JSON.stringify({candidates:{['1'.repeat(32)]:{name:'First'},['2'.repeat(32)]:{name:'Second'}}})).toString('base64');
  const locked=runtime(2);locked.click('reveal');assert.equal((await locked.export()).revealed,false);
  const cancelled=runtime(2,{answerCode:keyCode,confirm:false});cancelled.click('reveal');assert.equal(cancelled.confirms.length,1);assert.equal((await cancelled.export()).revealed,false);
  const app=runtime(2,{answerCode:keyCode});app.click('reveal');assert.equal((await app.export()).revealed,true);
  app.click('choose-left');app.click('undo');assert.equal((await app.export()).revealed,true);
  const imported=await app.export();imported.revealed=false;await app.import(imported);assert.equal((await app.export()).revealed,true);
});

test('normal progress is announced once, without repeating it in the storage status', () => {
  const app=runtime(3);
  assert.equal(app.nodes.status.textContent,'');
  assert.match(app.nodes['versus-progress'].textContent,/4강/);
});


test('pair advance pauses hidden audio/video without stopping a still-visible survivor', () => {
  const app=runtime(4,{media:true});
  const first=app.samples[0].media[0], second=app.samples[1].media[0];
  first.paused=false;second.paused=false;
  app.click('choose-both');
  assert.equal(app.samples[0].hidden,true);assert.equal(app.samples[1].hidden,true);
  assert.equal(first.paused,true);assert.equal(second.paused,true);
  assert.equal(first.currentTime,7);assert.equal(second.currentTime,7);
  const final=runtime(2,{media:true});
  const survivor=final.samples[0].media[0], eliminated=final.samples[1].media[0];
  survivor.paused=false;eliminated.paused=false;
  final.click('choose-both');
  assert.equal(survivor.paused,false);assert.equal(eliminated.paused,false);
  final.click('choose-left');
  assert.equal(final.samples[0].hidden,false);assert.equal(survivor.paused,false);
  assert.equal(final.samples[1].hidden,true);assert.equal(eliminated.paused,true);
  assert.equal(survivor.currentTime,7);assert.equal(eliminated.currentTime,7);
});

test('item switch pauses media in the hidden item and does not resume it automatically', () => {
  const app=runtime(2,{media:true,itemCount:2});
  const audio=app.samples[0].media[0],video=app.samples[1].media[0];
  audio.paused=false;video.paused=false;
  app.click('next-item');
  assert.equal(app.samples[0].hidden,true);assert.equal(app.samples[1].hidden,true);
  assert.equal(audio.paused,true);assert.equal(video.paused,true);
  app.click('previous-item');
  assert.equal(app.samples[0].hidden,false);assert.equal(audio.paused,true);assert.equal(video.paused,true);
  assert.equal(audio.currentTime,7);assert.equal(video.currentTime,7);
});


test('fifteen candidates display 16, 8, 4 and final rounds, explicit bye and undoable winner', async () => {
  const app = runtime(15);
  const headings = [];
  for(let i=0;i<16;i++) {
    headings.push(app.nodes['versus-progress'].textContent);
    if(app.nodes['versus-completion'].hidden === false) break;
    if(app.nodes.bye.hidden === false) app.click('bye'); else app.click('choose-left');
  }
  assert.equal(headings[0],'16강 · 1/8');
  for(const title of ['16강 · 8/8 · 부전승','8강 · 1/4','4강 · 1/2','결승','우승']) assert.ok(headings.includes(title),title);
  const final=await app.export(); assert.equal(final.items[0].events.length,15);
  app.click('undo'); assert.equal(app.nodes['versus-progress'].textContent,'결승');
  assert.equal(app.nodes['versus-completion'].hidden,true);
});

test('HTML previews mount only the current pair, keep sandbox restrictions and unload on advance/undo', () => {
  const handlers = {}, nodes = {}, frames = new Set(), previews = [];
  const node = id => nodes[id] ||= {id,hidden:true,disabled:false,textContent:'',setAttribute(){},append(){},
    addEventListener(event, callback){handlers[id+':'+event]=callback;}};
  const cards = Array.from({length:15},(_,i)=>({candidate:`opaque-${i}`,fingerprint:`bytes-${i}`,failed:false}));
  const data={study:'study',version:'1',revision:'revision',items:[{id:'item',cards}]};
  node('comparison-data').textContent=JSON.stringify(data);
  const samples=cards.map((card,i)=>{
    const toggle={textContent:'캡처로 보기',hidden:true,addEventListener(event,callback){this.toggle=callback;}};
    const content={dataset:{htmlSrc:`item-0001-slot-${String(i).padStart(4,'0')}-link-0001.html`},
      querySelector(selector){return selector==='.toggle-preview'?toggle:this.fallback;},fallback:{hidden:false},
      prepend(frame){frames.add(frame);}};
    previews.push(content);
    return {dataset:{item:'item',candidate:card.candidate},hidden:false,setAttribute(){},querySelectorAll(){return [];},
      querySelector(selector){return selector==='.sample-content'?content:selector==='.sample-choice'?{append(){}}:{textContent:''};}};
  });
  vm.runInNewContext(fs.readFileSync(sourcePath,'utf8'),{
    document:{getElementById:node,querySelectorAll(selector){return selector==='.sample'?samples:selector==='section'?[{}]:[];},
      createElement(tag){assert.equal(tag,'iframe');return {attrs:{},setAttribute(k,v){this.attrs[k]=v;},remove(){frames.delete(this);}};}},
    localStorage:{getItem(){return null;},setItem(){}},answerCode:'',crypto:{randomUUID(){return 'human';}}});
  const click = id => handlers[id+':click']();
  assert.equal(frames.size,2);
  for(const frame of frames){assert.equal(frame.attrs.sandbox,'allow-scripts allow-popups');assert.ok(!frame.attrs.sandbox.includes('same-origin'));}
  const first=[...frames];
  click('choose-left'); assert.equal(frames.size,2); assert.ok(first.every(frame=>!frames.has(frame)));
  click('undo'); assert.equal(frames.size,2);assert.ok(first.every(frame=>!frames.has(frame)));
  previews[0].querySelector('.toggle-preview').toggle(); assert.equal(frames.size,1);assert.equal(previews[0].fallback.hidden,false);
  previews[0].querySelector('.toggle-preview').toggle(); assert.equal(frames.size,2);
  for(let i=0;i<7;i++) click('choose-left');
  assert.equal(frames.size,1);assert.equal(node('bye').hidden,false);
  click('bye');assert.equal(frames.size,2);
});


test('one explicit result action validates embedded key and shows all fifteen replayed stages', async () => {
  const app=runtime(15,{loader:true,embedded:true,unsafeName:true});
  assert.equal(app.nodes.summary.innerHTML,'');
  for(let i=0;i<15;i++) app.click(app.nodes.bye.hidden?'choose-left':'bye');
  assert.equal(app.nodes.summary.innerHTML,'');
  app.click('result-reveal');
  const html=app.nodes.summary.innerHTML;
  assert.equal((html.match(/<tr><th scope="row">/g)||[]).length,15);
  for(const [stage,count] of [['16강',7],['8강',4],['4강',2],['결승',1],['우승',1]])
    assert.equal((html.match(new RegExp(`<td>${stage}</td>`,'g'))||[]).length,count,stage);
  assert.ok(html.includes('&lt;img onerror=bad()&gt;'));assert.ok(!html.includes('<img'));
  assert.equal((await app.export()).revealed,true);
  app.click('reveal');assert.equal(app.nodes.summary.innerHTML,'');
  assert.equal((await app.export()).revealed,true);
});

test('separate result action explains key, rejects stale revision, and continues only the pending explicit reveal', async () => {
  const app=runtime(2,{loader:true});app.click('choose-left');const before=await app.export();
  app.click('result-reveal');assert.match(app.nodes.status.textContent,/정답표.*분리/);
  await app.keyFile({...app.key,comparison:{revision:'stale'}});assert.equal((await app.export()).revealed,false);assert.equal(app.nodes.summary.innerHTML,'');
  app.click('result-reveal');app.cancelKey();await app.keyFile(app.key);assert.equal((await app.export()).revealed,false);
  app.click('result-reveal');assert.equal((await app.export()).revealed,true);assert.equal((app.nodes.summary.innerHTML.match(/<tr><th scope="row">/g)||[]).length,2);
  assert.deepEqual((await app.export()).items,before.items);
  const corrupt=runtime(2,{loader:true,embedded:true,badKey:true});corrupt.click('choose-left');corrupt.click('result-reveal');
  assert.equal((await corrupt.export()).revealed,false);assert.match(corrupt.nodes.status.textContent,/검증하지 못했습니다/);
});

test('result stages recompute after co-winner undo without resetting exposure or adding persisted ranking fields', async () => {
  const app=runtime(2,{loader:true,embedded:true});app.click('choose-both');app.click('co-winners');app.click('result-reveal');
  assert.equal((app.nodes.summary.innerHTML.match(/<td>공동 우승<\/td>/g)||[]).length,2);
  app.click('undo');assert.equal((app.nodes.summary.innerHTML.match(/<td>결승<\/td>/g)||[]).length,2);
  const state=await app.export();assert.equal(state.revealed,true);assert.ok(!('ranking' in state));assert.ok(!JSON.stringify(state).includes('Technique'));
});
