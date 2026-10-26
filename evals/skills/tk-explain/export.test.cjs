const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const vm = require('node:vm');
const { execFileSync } = require('node:child_process');
const { File } = require('node:buffer');
const root = path.resolve(__dirname, '../../..');
const code = fs.readFileSync(path.join(root, 'skills/tk-explain/assets/html-theme.js'), 'utf8');
const packager = path.join(root, 'skills/tk-explain/scripts/package_html.py');
const payload = html => html.match(/<template\b[^>]*data-ht-export[^>]*>([A-Za-z0-9+/=]+)<\/template>/)?.[1];

function run(encoded, { supported = false, error, denied = false, secure = true, protocol = 'https:' } = {}) {
  const control = () => ({ hidden: true, title: '', addEventListener(type, fn) { this[type] = fn; }, getAttribute() { return '다운로드'; } });
  const download = control(), share = control(), status = control();
  const timers = [], blobs = [], shared = [];
  let savedName;
  const document = {
    title: '파일 검증',
    querySelector(selector) {
      return { '[data-ht-download]': download, '[data-ht-share]': share, '[data-ht-export-status]': status,
        'template[data-ht-export]': encoded ? { content: { textContent: encoded } } : null }[selector] || null;
    },
    createElement(tag) {
      if (tag === 'template') return { attrs: {}, innerHTML: '', setAttribute(key, value) { this.attrs[key] = value; },
        get outerHTML() { return '<template data-ht-export="" data-entry="' + this.attrs['data-entry'] + '">' + this.innerHTML + '</template>'; } };
      return { click() { savedName = this.download; }, remove() {} };
    },
    body: { append() {} },
  };
  vm.runInNewContext(code, { document, TextEncoder, TextDecoder, Blob, File, Uint8Array, DataView, ArrayBuffer, atob,
    isSecureContext: secure, location: {protocol},
    URL: { createObjectURL(blob) { if (denied) throw Error('blocked'); blobs.push(blob); return 'blob:export'; }, revokeObjectURL(url) { assert.equal(url, 'blob:export'); } },
    setTimeout(fn) { timers.push(fn); },
    navigator: { canShare({ files }) { assert.equal(files.length, 1); return supported; },
      async share(data) { shared.push(data); if (error) throw { name: error }; } },
  });
  return { download, share, status, blobs, shared, timers, get savedName() { return savedName; } };
}

function fixture(files, filename) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'tk-export-'));
  for (const [name, content] of Object.entries(files)) {
    fs.mkdirSync(path.dirname(path.join(dir, name)), { recursive: true });
    fs.writeFileSync(path.join(dir, name), content);
  }
  execFileSync('python3', [packager, '--root', dir, '--name', filename, ...Object.keys(files)]);
  return dir;
}

test('single HTML downloads original source, ignores live form state, and remains exportable', async () => {
  const source = '<!doctype html><html><body><h1>공유 문서</h1><input value="original"></body></html>';
  const dir = fixture({ 'document.html': source }, 'document.html');
  try {
    const generated = fs.readFileSync(path.join(dir, 'document.html'), 'utf8');
    const result = run(payload(generated));
    assert.equal(result.download.hidden, false); assert.equal(result.share.hidden, true);
    result.download.click();
    assert.equal(result.savedName, 'document.html');
    const downloaded = await result.blobs[0].text();
    assert.ok(downloaded.includes('<h1>공유 문서</h1>')); assert.ok(downloaded.includes('value="original"'));
    assert.equal(payload(downloaded), payload(generated));
    result.timers.forEach(fn => fn());
    fs.writeFileSync(path.join(dir, 'document.html'), downloaded);
    execFileSync('python3', [packager, '--root', dir, '--name', 'document.html', 'document.html']);
    assert.equal(payload(fs.readFileSync(path.join(dir, 'document.html'), 'utf8')), payload(generated));
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});

test('ZIP validates CRCs, preserves nested links/assets, excludes unrelated files and reexports after extraction', async () => {
  const files = {
    'index.html': '<html><body><a href="lessons/one.html#part">수업</a></body></html>',
    'lessons/one.html': '<html><body id="part"><a href="../index.html">홈</a><a href="자료.txt">자료</a></body></html>',
    'lessons/자료.txt': '한글 경로와 본문',
  };
  const dir = fixture(files, 'course.zip');
  try {
    fs.writeFileSync(path.join(dir, 'private.txt'), 'must not export');
    const result = run(payload(fs.readFileSync(path.join(dir, 'lessons/one.html'), 'utf8')));
    result.download.click(); assert.equal(result.savedName, 'course.zip');
    const bytes = Buffer.from(await result.blobs[0].arrayBuffer());
    fs.writeFileSync(path.join(dir, 'course.zip'), bytes);
    const extracted = JSON.parse(execFileSync('python3', ['-c',
      'import base64,json,sys,zipfile\nwith zipfile.ZipFile(sys.argv[1]) as z:\n assert z.testzip() is None\n print(json.dumps({n:base64.b64encode(z.read(n)).decode() for n in z.namelist()}))',
      path.join(dir, 'course.zip')], { encoding: 'utf8' }));
    assert.deepEqual(Object.keys(extracted), Object.keys(files));
    assert.equal(Buffer.from(extracted['lessons/자료.txt'], 'base64').toString(), files['lessons/자료.txt']);
    const lesson = Buffer.from(extracted['lessons/one.html'], 'base64').toString();
    assert.ok(lesson.includes('href="../index.html"'));
    const again = run(payload(lesson)); again.download.click();
    assert.deepEqual(Buffer.from(await again.blobs[0].arrayBuffer()), bytes);
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});

test('sharing sends the file only, preserves download, and handles unsupported, cancel and failure', async () => {
  const dir = fixture({ 'one.html': '<html><body>문서</body></html>' }, 'one.html');
  try {
    const encoded = payload(fs.readFileSync(path.join(dir, 'one.html'), 'utf8'));
    for (const error of [undefined, 'AbortError', 'NotAllowedError']) {
      const result = run(encoded, { supported: true, error });
      assert.equal(result.share.hidden, false); await result.share.click();
      assert.equal(result.shared[0].files[0].name, 'one.html'); assert.equal(result.shared[0].url, undefined);
      assert.equal(result.download.hidden, false);
      assert.equal(!!result.status.textContent, error === 'NotAllowedError');
    }
    assert.equal(run(encoded, { supported: true, secure: false }).share.hidden, true);
    const local = run(encoded, { supported: true, protocol: 'file:' });
    assert.equal(local.share.hidden, true); assert.equal(local.download.hidden, false);
    local.download.click(); assert.equal(local.savedName, 'one.html');
    const blocked = run(encoded, { denied: true }); blocked.download.click();
    assert.ok(blocked.status.textContent.includes('다운로드하지 못했습니다'));
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});

test('missing or corrupt embedded source fails visibly without enabling an incomplete export', () => {
  for (const value of [null, 'invalid']) {
    const result = run(value);
    assert.equal(result.download.hidden, true); assert.equal(result.share.hidden, true);
    assert.equal(result.status.hidden, false);
  }
});
