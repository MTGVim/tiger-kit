const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const code = fs.readFileSync(path.join(__dirname, '../../../skills/tk-explain/assets/html-theme.js'), 'utf8');

function run(saved, denied = false) {
  const attributes = new Map(), storage = new Map([['tigerkit-html-theme', saved]]);
  const select = { value: '', parentElement: { hidden: true }, addEventListener: (_, fn) => { select.change = fn; } };
  const root = { setAttribute: (key, value) => attributes.set(key, value), removeAttribute: key => attributes.delete(key) };
  vm.runInNewContext(code, {
    document: { documentElement: root, getElementById: () => select },
    localStorage: {
      getItem: key => { if (denied) throw Error('denied'); return storage.get(key); },
      setItem: (key, value) => { if (denied) throw Error('denied'); storage.set(key, value); }
    }
  });
  return { attributes, storage, select };
}
test('manual light and dark restore, switching to system removes the override', () => {
  for (const initial of ['light', 'dark']) {
    const { attributes, storage, select } = run(initial);
    assert.equal(attributes.get('data-theme'), initial);
    assert.equal(select.parentElement.hidden, false);
    select.value = initial === 'light' ? 'dark' : 'light'; select.change();
    assert.equal(attributes.get('data-theme'), select.value);
    assert.equal(storage.get('tigerkit-html-theme'), select.value);
    select.value = 'system'; select.change();
    assert.equal(attributes.has('data-theme'), false);
    assert.equal(storage.get('tigerkit-html-theme'), 'system');
  }
});
test('storage refusal and invalid saved values keep all choices usable', () => {
  for (const denied of [true, false]) {
    const { attributes, select } = run('invalid', denied);
    assert.equal(select.value, 'system');
    select.value = 'dark'; select.change();
    assert.equal(attributes.get('data-theme'), 'dark');
    select.value = 'invalid'; select.change();
    assert.equal(attributes.has('data-theme'), false);
    assert.equal(select.value, 'system');
  }
});
test('a page without the optional control remains readable', () => {
  assert.doesNotThrow(() => vm.runInNewContext(code, { document: { getElementById: () => null } }));
});
