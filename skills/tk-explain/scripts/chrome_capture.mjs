/** Private, dependency-free Chrome DevTools pipe; never attaches to a user session. */
import {spawn} from 'node:child_process';
import {access, mkdtemp, rm} from 'node:fs/promises';
import {constants} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, delimiter} from 'node:path';

export async function chromePath() {
  const paths = process.env.CHROME_PATH ? [process.env.CHROME_PATH] : [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    ...['PROGRAMFILES', 'PROGRAMFILES(X86)', 'LOCALAPPDATA'].filter(k => process.env[k])
      .map(k => join(process.env[k], 'Google/Chrome/Application/chrome.exe')),
    ...(process.env.PATH || '').split(delimiter).flatMap(p => ['chromium', 'chromium-browser', 'google-chrome', 'chrome'].map(n => join(p, n)))
  ];
  for (const p of paths) { try { await access(p, constants.X_OK); return p; } catch {} }
  throw new Error('Blocked: installed Chrome/Chromium unavailable; set CHROME_PATH. No installation attempted.');
}

export async function withPage(action) {
  const executable = await chromePath();
  const profile = await mkdtemp(join(tmpdir(), 'tk-explain-chrome-'));
  const child = spawn(executable, ['--headless=new', '--remote-debugging-pipe', '--no-first-run',
    '--no-default-browser-check', '--disable-background-networking', `--user-data-dir=${profile}`, 'about:blank'],
    {stdio: ['ignore', 'ignore', 'pipe', 'pipe', 'pipe']});
  let next = 0, buffer = '', closed = false;
  const pending = new Map();
  const fail = error => { closed = true; for (const p of pending.values()) { clearTimeout(p.timer); p.reject(error); } pending.clear(); };
  child.on('error', fail); child.on('exit', () => fail(new Error('Chrome exited before capture completed')));
  child.stderr.resume();
  child.stdio[4].setEncoding('utf8');
  child.stdio[4].on('data', chunk => {
    buffer += chunk.toString();
    let end;
    while ((end = buffer.indexOf('\0')) >= 0) {
      const row = JSON.parse(buffer.slice(0, end)); buffer = buffer.slice(end + 1);
      const p = pending.get(row.id); if (!p) continue;
      pending.delete(row.id); clearTimeout(p.timer);
      row.error ? p.reject(new Error(row.error.message)) : p.resolve(row.result);
    }
  });
  const send = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
    if (closed) { reject(new Error('Chrome is unavailable')); return; }
    const id = ++next;
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`Chrome timeout: ${method}`)); }, 20000);
    pending.set(id, {resolve, reject, timer});
    child.stdio[3].write(JSON.stringify({id, method, params, ...(sessionId ? {sessionId} : {})}) + '\0');
  });
  try {
    const {targetId} = await send('Target.createTarget', {url: 'about:blank'});
    const {sessionId} = await send('Target.attachToTarget', {targetId, flatten: true});
    const call = (method, params) => send(method, params, sessionId);
    await call('Page.enable'); await call('Network.enable');
    await call('Network.setBlockedURLs', {urls: ['http://*', 'https://*', 'ws://*', 'wss://*', 'ftp://*']});
    return await action(call);
  } finally {
    if (!closed) {
      const exited = new Promise(resolve => child.once('exit', resolve));
      child.kill();
      const timer = setTimeout(() => child.kill('SIGKILL'), 2000);
      await exited; clearTimeout(timer);
    }
    fail(new Error('Capture ended'));
    await rm(profile, {recursive: true, force: true});
  }
}

export async function evaluate(call, expression) {
  const value = await call('Runtime.evaluate', {expression, awaitPromise: true, returnByValue: true});
  if (value.exceptionDetails) throw new Error(value.exceptionDetails.text);
  return value.result.value;
}
