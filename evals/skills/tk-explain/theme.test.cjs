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
  const buttons = ['system', 'light', 'dark'].map(value => {
    const attrs = new Map([['aria-pressed', 'false']]);
    const item = {
      dataset: { themeChoice: value },
      addEventListener: (_, fn) => { item.click = fn; },
      setAttribute: (key, val) => attrs.set(key, val),
      getAttribute: key => attrs.get(key),
    };
    return item;
  });
  const control = {
    hidden: true,
    querySelectorAll: selector => selector === '[data-theme-choice]' ? buttons : [],
  };
  const root = {
    setAttribute: (key, value) => attributes.set(key, value),
    removeAttribute: key => attributes.delete(key),
    getAttribute: key => attributes.has(key) ? attributes.get(key) : null,
  };
  vm.runInNewContext(code, {
    document: {
      documentElement: root,
      querySelector: selector => selector === '[data-ht-theme-control]' ? control : null,
    },
    localStorage: {
      getItem: key => { if (denied) throw Error('denied'); return storage.get(key); },
      setItem: (key, value) => { if (denied) throw Error('denied'); storage.set(key, value); }
    }
  });
  return { attributes, storage, control, buttons };
}
const button = (result, value) => result.buttons.find(item => item.dataset.themeChoice === value);

test('browser preference wins over the generated default and switching to system persists', () => {
  for (const initial of ['light', 'dark']) {
    const configured = initial === 'light' ? 'dark' : 'light';
    const result = run(initial, false, configured);
    assert.equal(result.attributes.get('data-theme'), initial);
    assert.equal(result.control.hidden, false);
    assert.equal(button(result, initial).getAttribute('aria-pressed'), 'true');
    button(result, configured).click();
    assert.equal(result.attributes.get('data-theme'), configured);
    assert.equal(result.storage.get('tigerkit-html-theme'), configured);
    button(result, 'system').click();
    assert.equal(result.attributes.has('data-theme'), false);
    assert.equal(result.storage.get('tigerkit-html-theme'), 'system');
    assert.equal(button(result, 'system').getAttribute('aria-pressed'), 'true');
  }
});

test('generated default applies without saved preference and survives storage refusal', () => {
  for (const configured of ['system', 'light', 'dark']) {
    for (const denied of [false, true]) {
      const result = run(undefined, denied, configured);
      assert.equal(button(result, configured).getAttribute('aria-pressed'), 'true');
      if (configured === 'system') assert.equal(result.attributes.has('data-theme'), false);
      else assert.equal(result.attributes.get('data-theme'), configured);
    }
  }
});

test('invalid saved values fall back to the generated default while controls remain usable', () => {
  const result = run('invalid', false, 'dark');
  assert.equal(button(result, 'dark').getAttribute('aria-pressed'), 'true');
  assert.equal(result.attributes.get('data-theme'), 'dark');
  button(result, 'light').click();
  assert.equal(result.attributes.get('data-theme'), 'light');
  assert.equal(button(result, 'light').getAttribute('aria-pressed'), 'true');
});

test('a page without the optional control remains readable', () => {
  assert.doesNotThrow(() => vm.runInNewContext(code, { document: { querySelector: () => null } }));
});
