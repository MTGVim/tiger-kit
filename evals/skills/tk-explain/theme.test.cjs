const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const code = fs.readFileSync(path.join(__dirname, '../../../skills/tk-explain/assets/html-theme.js'), 'utf8');

function run(saved, denied = false, configured = 'system', packageName = 'tk-explain', savedFont) {
  const code = fs.readFileSync(path.join(__dirname, '../../../skills', packageName, 'assets/html-theme.js'), 'utf8');
  const attributes = new Map(), storage = new Map(), styles = new Map(), created = [];
  const createElement = tag => {
    const element = {tag, children: [], attributes: new Map(), value: '',
      append: (...children) => element.children.push(...children),
      setAttribute: (key, value) => element.attributes.set(key, value),
      addEventListener: (event, fn) => { element[event] = fn; },
    };
    created.push(element);
    return element;
  };
  attributes.set('data-default-theme', configured);
  if (configured === 'light' || configured === 'dark') attributes.set('data-theme', configured);
  if (saved !== undefined) storage.set('tigerkit-html-theme', saved);
  if (savedFont !== undefined) storage.set('tigerkit-html-font-size', savedFont);
  const inputs = ['system', 'light', 'dark'].map(value => {
    const input = {
      value,
      checked: false,
      addEventListener: (_, fn) => { input.change = fn; },
    };
    return input;
  });
  const control = {
    hidden: true,
    querySelectorAll: selector => selector === 'input[name="ht-theme"]' ? inputs : [],
    before: element => { control.beforeElement = element; },
  };
  const root = {
    style: {setProperty: (key, value) => styles.set(key, value)},
    setAttribute: (key, value) => attributes.set(key, value),
    removeAttribute: key => attributes.delete(key),
    getAttribute: key => attributes.has(key) ? attributes.get(key) : null,
  };
  vm.runInNewContext(code, {
    document: {
      documentElement: root,
      createElement,
      querySelector: selector => selector === '[data-ht-theme-control]' ? control : null,
    },
    localStorage: {
      getItem: key => { if (denied) throw Error('denied'); return storage.get(key); },
      setItem: (key, value) => { if (denied) throw Error('denied'); storage.set(key, value); }
    }
  });
  return { attributes, storage, control, inputs, styles, created,
    font: created.find(element => element.tag === 'select') };
}
const input = (result, value) => result.inputs.find(item => item.value === value);
const choose = (result, value) => {
  const target = input(result, value);
  for (const item of result.inputs) item.checked = item === target;
  target.change();
};

test('browser preference wins over the generated default and switching to system persists', () => {
  for (const initial of ['light', 'dark']) {
    const configured = initial === 'light' ? 'dark' : 'light';
    const result = run(initial, false, configured);
    assert.equal(result.attributes.get('data-theme'), initial);
    assert.equal(result.control.hidden, false);
    assert.equal(input(result, initial).checked, true);
    choose(result, configured);
    assert.equal(result.attributes.get('data-theme'), configured);
    assert.equal(result.storage.get('tigerkit-html-theme'), configured);
    choose(result, 'system');
    assert.equal(result.attributes.has('data-theme'), false);
    assert.equal(result.storage.get('tigerkit-html-theme'), 'system');
    assert.equal(input(result, 'system').checked, true);
  }
});

test('generated default applies without saved preference and survives storage refusal', () => {
  for (const configured of ['system', 'light', 'dark']) {
    for (const denied of [false, true]) {
      const result = run(undefined, denied, configured);
      assert.equal(input(result, configured).checked, true);
      if (configured === 'system') assert.equal(result.attributes.has('data-theme'), false);
      else assert.equal(result.attributes.get('data-theme'), configured);
    }
  }
});

test('invalid saved values fall back to the generated default while controls remain usable', () => {
  const result = run('invalid', false, 'dark');
  assert.equal(input(result, 'dark').checked, true);
  assert.equal(result.attributes.get('data-theme'), 'dark');
  choose(result, 'light');
  assert.equal(result.attributes.get('data-theme'), 'light');
  assert.equal(input(result, 'light').checked, true);
});

test('a page without the optional control remains readable', () => {
  assert.doesNotThrow(() => vm.runInNewContext(code, { document: { querySelector: () => null } }));
});


test('question packages switch all themes and tolerate refused storage', () => {
  for (const packageName of ['tk-prep', 'tk-grill', 'tk-roadmap']) {
    for (const denied of [false, true]) {
      const result = run(undefined, denied, 'system', packageName);
      assert.equal(result.control.hidden, false);
      for (const value of ['dark', 'light', 'system']) {
        choose(result, value);
        assert.equal(input(result, value).checked, true);
        if (value === 'system') assert.equal(result.attributes.has('data-theme'), false);
        else assert.equal(result.attributes.get('data-theme'), value);
        if (!denied) assert.equal(result.storage.get('tigerkit-html-theme'), value);
      }
    }
  }
});

const packages = ['tk-explain', 'tk-explain-diff', 'tk-teach', 'tk-research', 'tk-qa-sheet',
  'tk-prototype', 'tk-blind-comparison', 'tk-prep', 'tk-grill', 'tk-roadmap'];
const sizes = ['50', '75', '100', '125', '150', '175', '200'];

test('all HTML consumers expose the font select immediately left of themes, defaulting to 100%', () => {
  for (const packageName of packages) {
    const result = run(undefined, false, 'system', packageName);
    assert.equal(result.font.attributes.get('aria-label'), '글자 크기');
    assert.deepEqual(result.font.children.map(option => option.value), sizes);
    assert.deepEqual(result.font.children.map(option => option.textContent), sizes.map(size => `${size}%`));
    const group = result.control.beforeElement;
    assert.equal(group.className, 'ht-reader-controls');
    assert.equal(group.children[0].className, 'ht-font-control');
    assert.equal(group.children[0].children[1], result.font);
    assert.equal(group.children[1], result.control);
    assert.equal(result.font.value, '100');
    assert.equal(result.styles.get('--ht-font-scale'), '1');
    assert.equal(result.storage.has('tigerkit-html-font-size'), false);
    for (const size of sizes) {
      result.font.value = size;
      result.font.change();
      assert.equal(result.styles.get('--ht-font-scale'), String(Number(size) / 100));
      assert.equal(result.storage.get('tigerkit-html-font-size'), size);
      const reloaded = run('dark', false, 'system', packageName, result.storage.get('tigerkit-html-font-size'));
      assert.equal(reloaded.font.value, size);
      assert.equal(reloaded.styles.get('--ht-font-scale'), String(Number(size) / 100));
      assert.equal(reloaded.attributes.get('data-theme'), 'dark');
    }
  }
});

test('invalid stored font sizes use 100%; rejected storage still permits every size and theme', () => {
  for (const saved of ['', '0', '100%', '125.0', '201', '-50', 'NaN', '150; color:red']) {
    const result = run('light', false, 'dark', 'tk-explain', saved);
    assert.equal(result.font.value, '100');
    assert.equal(result.styles.get('--ht-font-scale'), '1');
  }
  const result = run('dark', true, 'light', 'tk-explain', '200');
  assert.equal(result.font.value, '100');
  for (const size of sizes) {
    result.font.value = size;
    assert.doesNotThrow(() => result.font.change());
    assert.equal(result.styles.get('--ht-font-scale'), String(Number(size) / 100));
    choose(result, 'dark');
    assert.equal(result.attributes.get('data-theme'), 'dark');
  }
  result.font.value = 'invalid';
  result.font.change();
  assert.equal(result.font.value, '100');
  assert.equal(result.styles.get('--ht-font-scale'), '1');
});
