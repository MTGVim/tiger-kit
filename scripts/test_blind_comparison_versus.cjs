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
  const node = name => nodes[name] ||= {hidden:true, disabled:false, textContent:'', value:'', setAttribute() {}, click() {}, remove() {},
    addEventListener: (event, callback) => {handlers[name + ':' + event] = callback;}};
  node('comparison-data').textContent = JSON.stringify(data);
  const samples = data.items.flatMap(item => cards.map(card => ({hidden:false, dataset:{item:item.id, candidate:card.candidate}, setAttribute(){}, querySelector: () => node(item.id + card.candidate + ':identity')})));
  const sections = data.items.map(item => ({hidden:false,querySelectorAll:()=>samples.filter(s=>s.dataset.item===item.id)}));
  let stored = options.raw || null, download, copied, writes = 0;
  const confirms = [];
  vm.runInNewContext(fs.existsSync(sourcePath) ? fs.readFileSync(sourcePath, 'utf8') : '', {
    document:{getElementById:node, querySelectorAll: selector => selector === 'section' ? sections : samples, createElement:()=>node('download'), body:{append(){}}},
    localStorage:{getItem:()=>{if(options.storageDenied) throw Error(); return stored;},setItem:(_, value)=>{if(options.storageDenied) throw Error(); stored=value; writes++;}},
    crypto:{randomUUID:()=>options.evaluator || 'human'}, Blob, URL:{createObjectURL:blob=>{download=blob;return 'blob:test';},revokeObjectURL(){}}, setTimeout(){},
    navigator:{clipboard:{writeText:async value=>{if(options.clipboardDenied) throw Error();copied=value;}}},
    confirm: message=>{confirms.push(message);return options.confirm !== false;}, answerCode:options.answerCode || '',
    atob:value=>Buffer.from(value,'base64').toString('binary'), TextDecoder, Uint8Array
  });
  return {data,cards,samples,nodes,confirms,
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
  assert.match(app.status, /선정/);
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
  assert.match(app.nodes['versus-progress'].textContent,/라운드/);
});
