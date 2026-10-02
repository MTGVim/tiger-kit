const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const template = fs.readFileSync(path.join(__dirname, '../../../skills/tk-qa-sheet/assets/qa-sheet-template.html'), 'utf8');
const script = template.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
const sample = JSON.parse(template.match(/id="qa-data">\s*([\s\S]*?)<\/script>/)[1]);

// Run the actual renderer with a small DOM/storage seam; browser layout is checked separately.
function run(data = sample, storage = new Map(), denied = false) {
  const timers = new Map();
  let sequence = 0;
  class Element {
    constructor() {
      this.listeners = {}; this.classes = new Set(); this.style = {}; this.dataset = {};
      this.textContent = ''; this.value = ''; this.hidden = false;
      this.classList = { toggle: (name, on) => on ? this.classes.add(name) : this.classes.delete(name) };
    }
    addEventListener(name, fn) { this.listeners[name] = fn; }
    emit(name) { this.listeners[name]?.(); }
    closest() { return this.row; }
    querySelector() { return this.count; }
    querySelectorAll() { return this.boxes; }
  }
  const ids = Object.fromEntries(['qa-data', 'title', 'environment', 'main', 'count', 'bar', 'reset', 'onlyOpen', 'notes', 'saved', 'storage-warning'].map(id => [id, new Element()]));
  ids['storage-warning'].hidden = true;
  ids['qa-data'].textContent = typeof data === 'string' ? data : JSON.stringify(data);
  const body = new Element(), document = new Element(), window = new Element();
  const layout = new Element(), header = new Element();
  body.insertAdjacentHTML = (_, html) => { body.error = html; };
  let boxes = [], groups = [], html = '';
  Object.defineProperty(ids.main, 'innerHTML', {
    get: () => html,
    set: value => {
      html = value;
      groups = [...value.matchAll(/<section class="group">([\s\S]*?)<\/section>/g)].map(match => {
        const group = new Element(); group.count = new Element();
        group.boxes = [...match[1].matchAll(/data-id="([^"]+)"/g)].map(input => {
          const box = new Element(); box.dataset.id = input[1]; box.row = new Element(); return box;
        });
        return group;
      });
      boxes = groups.flatMap(group => group.boxes);
    }
  });
  document.getElementById = id => ids[id];
  document.querySelectorAll = selector => selector === '.group' ? groups : boxes;
  document.querySelector = selector => selector === 'header' ? header : layout;
  document.body = body;
  vm.runInNewContext(script, {
    document, window, console, URL, confirm: () => true,
    localStorage: {
      getItem: key => { if (denied) throw Error('denied'); return storage.get(key) ?? null; },
      setItem: (key, value) => { if (denied) throw Error('denied'); storage.set(key, value); }
    },
    setTimeout: fn => { timers.set(++sequence, fn); return sequence; },
    clearTimeout: id => timers.delete(id)
  });
  return { ids, boxes, groups, body, layout, header, document, window, html, storage,
    flush: () => { for (const fn of timers.values()) fn(); timers.clear(); } };
}
const clone = value => JSON.parse(JSON.stringify(value));
const toggle = box => { box.checked = !box.checked; box.emit('change'); };
const make = groups => ({ title: 'QA', storageKey: 'qa', groups });

test('two checks, notes and filter survive reload; reset preserves notes', () => {
  const first = run();
  toggle(first.boxes[0]); toggle(first.boxes[3]);
  first.ids.notes.value = 'replay note'; first.ids.notes.emit('input'); first.flush();
  first.ids.onlyOpen.checked = true; first.ids.onlyOpen.emit('change');
  const second = run(sample, first.storage);
  assert.equal(second.ids.count.textContent, '2 / 5');
  assert.deepEqual(second.groups.map(g => g.count.textContent), ['1 / 3', '1 / 2']);
  assert.equal(second.ids.notes.value, 'replay note');
  assert.equal(second.ids.onlyOpen.checked, true);
  second.ids.reset.emit('click');
  const third = run(sample, first.storage);
  assert.equal(third.ids.count.textContent, '0 / 5');
  assert.equal(third.ids.notes.value, 'replay note');
});

test('pending notes flush on pagehide before debounce', () => {
  const first = run(); first.ids.notes.value = 'immediate'; first.ids.notes.emit('input');
  first.window.emit('pagehide');
  assert.equal(run(sample, first.storage).ids.notes.value, 'immediate');
});

test('delimiter-bearing identity is separate and reordering preserves checked content', () => {
  const data = make([{ title: 'A|B', items: [{ title: 'C' }] }, { title: 'A', items: [{ title: 'B|C' }] }]);
  const first = run(data); assert.equal(new Set(first.boxes.map(b => b.dataset.id)).size, 2);
  toggle(first.boxes[0]);
  const reordered = clone(data); reordered.groups.reverse();
  const second = run(reordered, first.storage);
  assert.deepEqual(second.boxes.map(b => b.checked), [false, true]);
});

test('duplicate identities stop rendering instead of sharing state', () => {
  const result = run(make([{ title: 'Area', items: [{ title: 'same' }, { title: 'same' }] }]));
  assert.match(result.body.error, /ID/);
  assert.equal(result.boxes.length, 0);
  assert.equal(result.layout.hidden, true);
});

test('source-only parent and omitted provenance stay source-only', () => {
  const result = run(make([{ title: 'Area', items: [{ title: 'Parent', provenance: 'code-only', checks: [{ text: 'Child', provenance: 'observed' }] }, { title: 'Unknown' }] }]));
  assert.equal((result.html.match(/class="badge"/g) || []).length, 2);
  assert.equal((run().html.match(/class="badge"/g) || []).length, 1);
});

test('malformed data and schema show an error without a partial sheet', () => {
  for (const data of ['{', null, {}, { ...sample, groups: null }, make([{ title: 'Area', items: [{ title: 'Only headings', checks: [{ text: 'Heading', heading: true }] }] }])]) {
    const result = run(data);
    assert.match(result.body.error, /qa-data/);
    assert.equal(result.boxes.length, 0);
    assert.equal(result.header.hidden, true);
  }
});

test('corrupt stored state falls back without executing or promoting invalid values', () => {
  for (const state of ['null', '[]', '"yes"', '{', '{"unknown": 100}']) {
    const key = role => JSON.stringify(['tk-qa-sheet', sample.storageKey, role, 1]);
    const storage = new Map([[key('checks'), state], [key('notes'), '{}'], [key('onlyOpen'), '"true"']]);
    const result = run(sample, storage);
    assert.equal(result.ids.count.textContent, '0 / 5');
    assert.equal(result.ids.notes.value, '');
    assert.equal(result.ids.onlyOpen.checked, false);
  }
});

test('unavailable storage preserves in-memory checks and exposes failed writes', () => {
  const result = run(sample, new Map(), true); toggle(result.boxes[0]);
  assert.equal(result.ids.count.textContent, '1 / 5');
  assert.equal(result.ids['storage-warning'].hidden, false);
  assert.match(result.ids['storage-warning'].textContent, /저장 실패/);
});

test('UI text is escaped before inline code formatting', () => {
  const result = run(make([{ title: 'Area', items: [{ title: '`<img src=x onerror=alert(1)>`' }] }]));
  assert.doesNotMatch(result.html, /<img/);
  assert.match(result.html, /<code>&lt;img/);
});

test('standalone checks retain explanatory notes and evidence limitations', () => {
  const result = run(make([{ title: 'Area', items: [{ title: 'Screen', notes: ['Navigation connection unverified'] }] }]));
  assert.match(result.html, /Navigation connection unverified/);
  assert.equal(result.boxes.length, 1);
});

test('environment-bound screen links render separately with safe tab attributes', () => {
  const data = make([{ title: 'Area', items: [{ title: 'List', url: 'https://qa.example.test/orders?q=a&state=b' }, { title: 'Detail', url: 'https://qa.example.test/orders/123#refund', checks: [{ text: 'Open' }] }] }]);
  data.environment = { label: 'QA', baseUrl: 'https://qa.example.test' };
  const result = run(data);
  assert.match(result.html, /href="https:\/\/qa.example.test\/orders\?q=a&amp;state=b"/);
  assert.match(result.html, /orders\/123#refund/);
  assert.equal((result.html.match(/rel="noopener noreferrer"/g) || []).length, 2);
  assert.equal(result.ids.environment.hidden, false);
  assert.match(result.ids.environment.textContent, /환경: QA/);
  assert.equal(result.boxes.length, 2);
});

test('unsafe, cross-environment and environment-less links stop rendering', () => {
  for (const url of ['javascript:alert(1)', '/orders', 'https://user:secret@qa.example.test/orders', 'https://production.example.test/orders']) {
    const data = make([{ title: 'Area', items: [{ title: 'List', url }] }]);
    data.environment = { label: 'QA', baseUrl: 'https://qa.example.test' };
    assert.match(run(data).body.error, /qa-data/);
  }
  const data = make([{ title: 'Area', items: [{ title: 'List', url: 'https://qa.example.test/orders' }] }]);
  assert.match(run(data).body.error, /qa-data/);
});

test('changing the environment or record cannot inherit completed checks', () => {
  const data = make([{ title: 'Area', items: [{ title: 'Detail', url: 'https://qa.example.test/orders/123' }] }]);
  data.environment = { label: 'QA', baseUrl: 'https://qa.example.test' };
  const first = run(data); toggle(first.boxes[0]);
  data.groups[0].items[0].url = 'https://qa.example.test/orders/456';
  assert.equal(run(data, first.storage).ids.count.textContent, '0 / 1');
  data.environment.baseUrl = 'https://production.example.test';
  data.groups[0].items[0].url = 'https://production.example.test/orders/123';
  assert.equal(run(data, first.storage).ids.count.textContent, '0 / 1');
});

test('historical short-hash collisions cannot transfer completion to changed text', () => {
  const data = make([{ title: 'Area', items: [{ title: 'AĀ' }] }]);
  const first = run(data); toggle(first.boxes[0]);
  data.groups[0].items[0].title = 'B}';
  assert.equal(run(data, first.storage).ids.count.textContent, '0 / 1');
});

test('distinct task keys cannot alias notes and completion storage', () => {
  const firstData = make([{ title: 'Area', items: [{ title: 'Screen' }] }]); firstData.storageKey = 'task';
  const first = run(firstData); first.ids.notes.value = 'keep note'; first.ids.notes.emit('input'); first.flush();
  const secondData = clone(firstData); secondData.storageKey = 'task:notes';
  const second = run(secondData, first.storage); toggle(second.boxes[0]);
  assert.equal(run(firstData, first.storage).ids.notes.value, 'keep note');
  assert.equal(run(secondData, first.storage).ids.count.textContent, '1 / 1');
});
