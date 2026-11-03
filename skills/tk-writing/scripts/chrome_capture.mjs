/** Private, dependency-free Chrome DevTools pipe; never attaches to a user session. */
import {spawn} from 'node:child_process';
import {access, mkdtemp, rm} from 'node:fs/promises';
import {constants} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, delimiter} from 'node:path';
import {createServer} from 'node:net';

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
  let profile, child, denyProxy, exited, stopError, signalCode;
  let next = 0, buffer = '', closed = false;
  const pending = new Map();
  const fail = error => { closed = true; for (const p of pending.values()) { clearTimeout(p.timer); p.reject(error); } pending.clear(); };
  let rejectStop;
  const stopped = new Promise((_, reject) => { rejectStop = reject; });
  const stop = error => { stopError = error; fail(error); rejectStop(error); };
  // Install before acquiring resources, including cancellation during launch.
  const handlers = new Map(['SIGINT', 'SIGTERM', 'SIGHUP'].map(signal => [signal, () => {
    signalCode = {SIGINT: 130, SIGTERM: 143, SIGHUP: 129}[signal];
    stop(new Error(`Capture interrupted: ${signal}`));
  }]));
  for (const [signal, handler] of handlers) process.on(signal, handler);
  const timer = setTimeout(() => stop(new Error('Capture timeout (30000ms)')), 30000);
  const launch = (async () => {
    profile = await mkdtemp(join(tmpdir(), 'tk-explain-chrome-'));
    if (stopError) throw stopError;
    // Page-level CDP blocking does not cover iframe/worker/WebSocket traffic.
    // This run-owned proxy never forwards, including requests to loopback.
    denyProxy = createServer(socket => socket.destroy());
    await new Promise((resolve, reject) => {
      denyProxy.once('error', reject);
      denyProxy.listen(0, '127.0.0.1', resolve);
    });
    if (stopError) throw stopError;
    child = spawn(executable, ['--headless=new', '--remote-debugging-pipe', '--no-first-run',
      '--no-default-browser-check', '--disable-background-networking',
      `--proxy-server=http://127.0.0.1:${denyProxy.address().port}`, '--proxy-bypass-list=<-loopback>',
      '--disable-quic', '--host-resolver-rules=MAP * ~NOTFOUND',
      '--force-webrtc-ip-handling-policy=disable_non_proxied_udp', `--user-data-dir=${profile}`, 'about:blank'],
      {stdio: ['ignore', 'ignore', 'pipe', 'pipe', 'pipe']});
    exited = new Promise(resolve => { child.once('exit', resolve); child.once('error', resolve); });
    child.on('error', fail); child.on('exit', () => fail(new Error('Chrome exited before capture completed')));
    child.stderr.resume();
    child.stdio[3].on('error', fail);
    child.stdio[4].on('error', fail);
    child.stdio[4].setEncoding('utf8');
    child.stdio[4].on('data', chunk => {
      buffer += chunk.toString();
      let end;
      while ((end = buffer.indexOf('\0')) >= 0) {
        let row;
        try { row = JSON.parse(buffer.slice(0, end)); } catch (error) { stop(error); return; }
        buffer = buffer.slice(end + 1);
        const p = pending.get(row.id); if (!p) continue;
        pending.delete(row.id); clearTimeout(p.timer);
        row.error ? p.reject(new Error(row.error.message)) : p.resolve(row.result);
      }
    });
  })();
  const send = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
    if (closed) { reject(stopError || new Error('Chrome is unavailable')); return; }
    const id = ++next;
    const timer = setTimeout(() => { pending.delete(id); reject(new Error(`Chrome timeout: ${method}`)); }, 20000);
    pending.set(id, {resolve, reject, timer});
    child.stdio[3].write(JSON.stringify({id, method, params, ...(sessionId ? {sessionId} : {})}) + '\0');
  });
  const work = (async () => {
    await launch;
    if (stopError) throw stopError;
    const {targetId} = await send('Target.createTarget', {url: 'about:blank'});
    const {sessionId} = await send('Target.attachToTarget', {targetId, flatten: true});
    const call = (method, params) => send(method, params, sessionId);
    await call('Page.enable'); await call('Network.enable');
    await call('Network.setBlockedURLs', {urls: ['http://*', 'https://*', 'ws://*', 'wss://*', 'ftp://*']});
    return await action(call);
  })();
  try {
    return await Promise.race([work, stopped]);
  } finally {
    clearTimeout(timer);
    try {
      // Finish resource acquisition before cleanup, but never await a hung action.
      await launch.catch(() => {});
      if (child?.pid && child.exitCode === null && child.signalCode === null) {
        child.kill();
        const killTimer = setTimeout(() => child.kill('SIGKILL'), 2000);
        try { await exited; } finally { clearTimeout(killTimer); }
      }
    } finally {
      fail(new Error('Capture ended'));
      // Extra pipe descriptors can remain readable after Chrome exits mid-command.
      for (const stream of child?.stdio || []) stream?.destroy();
      try {
        if (denyProxy?.listening) await new Promise(resolve => denyProxy.close(resolve));
        if (profile) await rm(profile, {recursive: true, force: true, maxRetries: 5, retryDelay: 100});
      } finally {
        for (const [signal, handler] of handlers) process.removeListener(signal, handler);
        // Public CLI catch blocks must not replace conventional signal exits with 1.
        if (signalCode) process.exit(signalCode);
      }
    }
  }
}

export async function evaluate(call, expression) {
  const value = await call('Runtime.evaluate', {expression, awaitPromise: true, returnByValue: true});
  if (value.exceptionDetails) throw new Error(value.exceptionDetails.text);
  return value.result.value;
}
