const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../../../skills/tk-browser-verify/scripts/capture_overlay.js'), 'utf8');

function harness() {
  class Element {
    constructor() { this.children = []; this.style = {}; this.attrs = {}; this.offsetWidth = 120; this.offsetHeight = 50; }
    append(el) { this.children.push(el); el.parent = this; }
    remove() { if (this.parent) this.parent.children = this.parent.children.filter(el => el !== this); }
    setAttribute(k, v) { this.attrs[k] = v; }
    attachShadow() { this.shadow = new Element(); return this.shadow; }
    get firstElementChild() { return this.children[0]; }
    getBoundingClientRect() { return { left: 40, top: 50, width: 200, height: 100 }; }
  }
  const documentElement = new Element(), listeners = new Map(), timers = new Map();
  let time = 0, timerId = 0;
  const target = { closest: () => null };
  const document = { documentElement, activeElement: target, createElement: () => new Element(),
    addEventListener(name, fn, { signal }) {
      listeners.set(name, fn); signal.addEventListener('abort', () => listeners.delete(name), { once: true });
    } };
  const context = vm.createContext({ window: {}, document, innerWidth: 800, innerHeight: 600,
    AbortController, performance: { now: () => time },
    setTimeout(fn) { timers.set(++timerId, fn); return timerId; }, clearTimeout(id) { timers.delete(id); } });
  const inject = () => vm.runInContext(source, context);
  inject();
  const emit = (name, props) => listeners.get(name)?.({ target, ...props });
  const root = () => documentElement.children[0].shadow;
  const byClass = name => root().children.find(el => el.className === name);
  const text = el => (el.textContent || '') + el.children.map(text).join('');
  return { context, documentElement, listeners, timers, target, inject, emit, root, byClass, text,
    advance: ms => { time += ms; }, expire: () => { for (const fn of [...timers.values()]) fn(); } };
}

test('cursor, clicks, grouped keys, repeat count, viewport clamp and highlights', () => {
  const h = harness();
  h.emit('mousemove', { clientX: 790, clientY: 590 });
  assert.equal(h.byClass('cursor').style.left, '790px');
  assert.equal(h.byClass('dock').style.left, '654px');
  assert.equal(h.byClass('dock').style.top, '524px');
  h.emit('mousedown', { clientX: 120, clientY: 200 });
  assert.equal(h.byClass('ring').style.left, '120px');
  h.emit('keydown', { key: 'a' }); h.advance(100); h.emit('keydown', { key: 'b' });
  assert.equal(h.text(h.byClass('dock')), 'ab');
  h.emit('keydown', { key: 'ArrowRight' }); h.emit('keydown', { key: 'ArrowRight' });
  assert.equal(h.text(h.byClass('dock')), 'ab→×2');
  h.context.window.__tigerkitCapture.highlight(h.documentElement);
  assert.equal(h.byClass('highlight').style.width, '212px');
  h.context.window.__tigerkitCapture.clear();
  assert.equal(h.byClass('highlight'), undefined);
  h.expire();
  assert.equal(h.byClass('dock').children.length, 0);
  assert.equal(h.byClass('ring'), undefined);
});

test('sensitive targets mask before DOM insertion and explicit IME display, and teardown is complete', () => {
  const h = harness();
  const sensitive = { closest: () => ({}) };
  h.emit('keydown', { key: 'private', target: sensitive });
  h.context.window.__tigerkitCapture.text('한글 비밀', sensitive);
  assert.equal(h.text(h.byClass('dock')), '●●');
  h.emit('keydown', { key: 'Process', isComposing: true });
  assert.equal(h.text(h.byClass('dock')), '●●');
  h.context.window.__tigerkitCapture.text('공개 설명', h.target);
  assert.ok(h.text(h.byClass('dock')).includes('공개 설명'));
  assert.equal(h.documentElement.children[0].attrs['aria-hidden'], 'true');
  h.inject(); assert.equal(h.documentElement.children.length, 1);
  h.context.window.__tigerkitCapture.remove();
  assert.equal(h.documentElement.children.length, 0);
  assert.equal(h.listeners.size, 0); assert.equal(h.timers.size, 0);
  assert.equal(h.context.window.__tigerkitCapture, undefined);
  h.emit('keydown', { key: 'z' });
  assert.equal(h.documentElement.children.length, 0);
  h.inject(); assert.equal(h.documentElement.children.length, 1);
  h.context.window.__tigerkitCapture.remove();
});

test('retargeted shadow input is masked when opaque and uses the actual target when visible', () => {
  const h = harness();
  const opaque = { tagName: 'PRIVATE-FIELD', closest: () => null };
  h.emit('keydown', { key: 'x', target: opaque });
  assert.equal(h.text(h.byClass('dock')), '●');
  h.emit('keydown', { key: 'y', target: opaque, composedPath: () => [h.target] });
  assert.equal(h.text(h.byClass('dock')), '●y');
  h.context.window.__tigerkitCapture.remove();
});
