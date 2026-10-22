const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '../skills/tk-blind-comparison/assets/gallery.js'), 'utf8');
const item = 'd'.repeat(32), id = c => c.repeat(32), fingerprint = c => c.repeat(64);
const key = c => `${item}/${id(c)}/${fingerprint(c)}`;
const value = (score = null, note = '', favorite = false) => ({score, note, favorite});
const row = (c, score = null, note = '', favorite = false) => ({item, candidate: id(c), fingerprint: fingerprint(c), ...value(score, note, favorite)});
const payload = (ratings, extra = {}) => ({schema: 1, study: 'study', version: '1', evaluator: 'Alice', revealed: false, ratings, ...extra});
const saved = entries => JSON.stringify({schema: 1, study: 'study', evaluator: 'Alice', revealed: false, entries});

// Run the actual application with only its DOM/storage/download boundary replaced.
function gallery(candidates = ['a', 'b'], raw = null, boundary = {}) {
  const handlers = {}, nodes = {};
  const node = name => nodes[name] ||= {
    textContent: '', hidden: true, value: '',
    addEventListener(event, callback) {handlers[`${name}:${event}`] = callback;},
    replaceChildren() {}, setAttribute() {}, click() {}, remove() {}
  };
  const cards = candidates.map(c => ({candidate: id(c), fingerprint: fingerprint(c), failed: false}));
  node('comparison-data').textContent = JSON.stringify({study: 'study', version: '2', items: [{id: item, cards}]});
  const samples = candidates.map(c => ({
    dataset: {item, candidate: id(c), fingerprint: fingerprint(c)},
    querySelector: selector => node(`${c}:${selector}`),
    addEventListener: (event, callback) => {handlers[`${c}:${event}`] = callback;}
  }));
  let stored = raw, download, copied, writes = 0;
  vm.runInNewContext(source, {
    document: {getElementById: node, querySelectorAll: () => samples, createElement: () => node('download'), body: {append() {}}},
    localStorage: {
      getItem: () => {if (boundary.storageDenied) throw new Error('denied'); return stored;},
      setItem: (_, text) => {if (boundary.storageDenied) throw new Error('denied'); stored = text; writes++;}
    },
    Blob, URL: {createObjectURL: blob => {download = blob; return 'blob:test';}, revokeObjectURL() {}},
    crypto: {randomUUID: () => 'fresh'}, setTimeout() {},
    navigator: boundary.noClipboard ? {} : {clipboard: {writeText: async text => {
      if (boundary.clipboardDenied) throw new Error('denied');
      copied = text;
    }}}
  });
  return {
    async import(input) {
      node('import-file').files = [{text: async () => typeof input === 'string' ? input : JSON.stringify(input)}];
      await handlers['import-file:change']();
    },
    async export() {handlers['export:click'](); return JSON.parse(await download.text());},
    async copy() {await handlers['copy:click'](); return copied === undefined ? undefined : JSON.parse(copied);},
    rate(c, score) {handlers[`${c}:input`]({target: {value: String(score), matches: selector => selector === '[data-score]'}});},
    get status() {return node('status').textContent;},
    get stored() {return stored;},
    get writes() {return writes;}
  };
}

test('copy and export share blind ratings, including archived entries and reveal history', async () => {
  const app = gallery(['a', 'b']);
  await app.import(payload([row('a', 4, '메모'), row('c', 5)], {revealed: true}));
  const copied = await app.copy();
  assert.match(app.status, /복사했습니다/);
  assert.deepEqual(copied, await app.export());
  assert.equal(copied.revealed, true);
  assert.deepEqual(copied.archive[key('c')], value(5));
  assert.equal(copied.ratings[0].candidate, id('a'));
  const receiver = gallery();
  await receiver.import(copied);
  assert.equal((await receiver.export()).ratings[0].score, 4);
});

test('copy remains usable with refused storage, and clipboard failures preserve export', async () => {
  const blockedStorage = gallery(['a', 'b'], null, {storageDenied: true});
  blockedStorage.rate('a', 4);
  assert.equal((await blockedStorage.copy()).ratings[0].score, 4);
  assert.equal(blockedStorage.writes, 0);
  for (const boundary of [{clipboardDenied: true}, {noClipboard: true}]) {
    const app = gallery(['a', 'b'], null, boundary);
    app.rate('b', 3);
    const before = app.stored;
    assert.equal(await app.copy(), undefined);
    assert.match(app.status, /평가 JSON 내보내기/);
    assert.equal(app.stored, before);
    assert.equal((await app.export()).ratings[1].score, 3);
  }
});

test('different evaluators cannot mix existing scores, but an empty gallery accepts an export', async () => {
  const app = gallery(['a', 'b'], saved({[key('a')]: value(5, 'Alice note')}));
  await app.import(payload([row('b', 1)], {evaluator: 'Bob'}));
  assert.match(app.status, /다른 평가자/);
  const result = await app.export();
  assert.equal(result.evaluator, 'Alice');
  assert.deepEqual(result.ratings.map(r => [r.score, r.note]), [[5, 'Alice note'], [null, '']]);
  assert.equal(app.writes, 0);
  const empty = gallery();
  await empty.import(payload([row('b', 1)], {evaluator: 'Bob'}));
  assert.equal((await empty.export()).evaluator, 'Bob');
});

test('removed outputs survive JSON backup and return only with their exact fingerprint', async () => {
  const removed = gallery(['a', 'c']);
  await removed.import(payload([row('a', 2), row('b', 5, 'keep this')]));
  const backup = await removed.export();
  assert.equal(backup.ratings.some(r => r.candidate === id('b')), false);
  assert.deepEqual(backup.archive[key('b')], value(5, 'keep this'));
  const readded = gallery(['c', 'b', 'a']);
  await readded.import(backup);
  const restored = (await readded.export()).ratings.find(r => r.candidate === id('b'));
  assert.equal(restored.score, 5);
  assert.equal(restored.note, 'keep this');
  const changed = gallery(['a', 'b']);
  const stale = payload([row('b', 5)]);
  stale.ratings[0].fingerprint = fingerprint('e');
  await changed.import(stale);
  assert.equal((await changed.export()).ratings.find(r => r.candidate === id('b')).score, null);
});

test('corrupt saved storage is preserved while new ratings remain exportable', async () => {
  for (const raw of ['broken JSON', saved({'invalid-key': value(3)}), saved(true), saved(7), saved({[key('a')]: value(3, '', true), [key('b')]: value(4, '', true)})]) {
    const app = gallery(['a', 'b'], raw);
    assert.match(app.status, /읽을 수 없습니다/);
    app.rate('a', 4);
    assert.equal(app.stored, raw);
    assert.equal(app.writes, 0);
    assert.equal((await app.export()).ratings[0].score, 4);
  }
});

test('malformed imports leave existing ratings and stored bytes untouched', async () => {
  const invalid = [
    'broken JSON', payload([row('b', 6)]), payload([row('b', 2), row('b', 3)]),
    payload([row('b', 2)], {study: 'other'}), payload([], {archive: []}),
    payload([], {archive: false}), payload([], {archive: null}), payload([], {archive: 0}),
    payload([], {archive: {'invalid-key': value(2)}}),
    payload([row('a', 2, '', true), row('b', 3, '', true)]),
    payload([], {archive: {[key('a')]: value(2, '', true), [key('b')]: value(3, '', true)}})
  ];
  for (const input of invalid) {
    const raw = saved({[key('a')]: value(4, 'preserve')});
    const app = gallery(['a', 'b'], raw);
    await app.import(input);
    assert.match(app.status, /가져오지 못했습니다/);
    assert.equal(app.stored, raw);
    assert.equal(app.writes, 0);
    assert.deepEqual((await app.export()).ratings.map(r => [r.score, r.note]), [[4, 'preserve'], [null, '']]);
  }
});

test('archive fields cannot replace the current output identity on export', async () => {
  const app = gallery();
  await app.import(payload([], {archive: {[key('a')]: {...value(4), item: 'wrong', candidate: 'wrong', fingerprint: 'wrong'}}}));
  const result = await app.export();
  assert.deepEqual(result.ratings.map(r => [r.item, r.candidate, r.fingerprint]), [row('a'), row('b')].map(r => [r.item, r.candidate, r.fingerprint]));
});
