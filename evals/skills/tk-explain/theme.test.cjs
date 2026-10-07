const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const code = fs.readFileSync(path.join(__dirname, '../../../skills/tk-explain/assets/html-theme.js'), 'utf8');

function run(saved, denied = false, configured = 'system') {
  const attributes = new Map(), storage = new Map();
  attributes.set('data-default-theme', configured);
  if (configured === 'light' || configured === 'dark') attributes.set('data-theme', configured);
  if (saved !== undefined) storage.set('tigerkit-html-theme', saved);
  const select = { value: '', parentElement: { hidden: true }, addEventListener: (_, fn) => { select.change = fn; } };
  const root = {
    setAttribute: (key, value) => attributes.set(key, value),
    removeAttribute: key => attributes.delete(key),
    getAttribute: key => attributes.has(key) ? attributes.get(key) : null,
  };
  vm.runInNewContext(code, {
    document: { documentElement: root, getElementById: () => select },
    localStorage: {
      getItem: key => { if (denied) throw Error('denied'); return storage.get(key); },
      setItem: (key, value) => { if (denied) throw Error('denied'); storage.set(key, value); }
    }
  });
  return { attributes, storage, select };
}
test('browser preference wins over the generated default and switching to system persists', () => {
  for (const initial of ['light', 'dark']) {
    const configured = initial === 'light' ? 'dark' : 'light';
    const { attributes, storage, select } = run(initial, false, configured);
    assert.equal(attributes.get('data-theme'), initial);
    assert.equal(select.parentElement.hidden, false);
    select.value = configured; select.change();
    assert.equal(attributes.get('data-theme'), configured);
    assert.equal(storage.get('tigerkit-html-theme'), configured);
    select.value = 'system'; select.change();
    assert.equal(attributes.has('data-theme'), false);
    assert.equal(storage.get('tigerkit-html-theme'), 'system');
  }
});
test('generated default applies without saved preference and survives storage refusal', () => {
  for (const configured of ['system', 'light', 'dark']) {
    for (const denied of [false, true]) {
      const { attributes, select } = run(undefined, denied, configured);
      assert.equal(select.value, configured);
      if (configured === 'system') assert.equal(attributes.has('data-theme'), false);
      else assert.equal(attributes.get('data-theme'), configured);
    }
  }
});
test('invalid saved values fall back to the generated default while controls remain usable', () => {
  const { attributes, select } = run('invalid', false, 'dark');
  assert.equal(select.value, 'dark');
  assert.equal(attributes.get('data-theme'), 'dark');
  select.value = 'light'; select.change();
  assert.equal(attributes.get('data-theme'), 'light');
  select.value = 'invalid'; select.change();
  assert.equal(attributes.has('data-theme'), false);
  assert.equal(select.value, 'system');
});
test('a page without the optional control remains readable', () => {
  assert.doesNotThrow(() => vm.runInNewContext(code, { document: { getElementById: () => null } }));
});
