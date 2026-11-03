/** Private Playwright renderer; launches only an isolated, installed Chrome. */
import {access, mkdtemp, rm} from 'node:fs/promises';
import {constants} from 'node:fs';
import {tmpdir} from 'node:os';
import {join, delimiter, isAbsolute} from 'node:path';
import {createRequire} from 'node:module';
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

function installedChromium() {
  const override = process.env.PLAYWRIGHT_MODULE_PATH;
  if (override !== undefined && !isAbsolute(override)) throw new Error('Blocked: PLAYWRIGHT_MODULE_PATH must be an absolute installed Playwright package path.');
  try {
    // Resolve from the caller project, not the skill installation or global packages.
    const {chromium} = createRequire(join(process.cwd(), 'package.json'))(override ?? 'playwright');
    if (!chromium || typeof chromium.launchPersistentContext !== 'function') throw new Error('Not a Playwright SDK');
    return chromium;
  } catch (error) {
    throw new Error(`Blocked: cannot load installed Playwright SDK${override === undefined ? ' from the caller project' : ' at PLAYWRIGHT_MODULE_PATH'}: ${error.message}. No installation attempted.`);
  }
}

export async function withPage(action, {viewport = {width: 1280, height: 720}, deviceScaleFactor = 1} = {}) {
  const chromium = installedChromium();
  const executablePath = await chromePath();
  let profile, context, denyProxy, interrupted;
  let rejectStop;
  const stopped = new Promise((_, reject) => { rejectStop = reject; });
  const stop = error => { interrupted = error; rejectStop(error); };
  // Install before acquiring resources, including cancellation during launch.
  const handlers = new Map(['SIGINT', 'SIGTERM', 'SIGHUP'].map(signal => [signal, () => {
    process.exitCode = {SIGINT: 130, SIGTERM: 143, SIGHUP: 129}[signal];
    stop(new Error(`Capture interrupted: ${signal}`));
  }]));
  for (const [signal, handler] of handlers) process.on(signal, handler);
  const timer = setTimeout(() => stop(new Error('Capture timeout (30000ms)')), 30000);
  const launch = (async () => {
    profile = await mkdtemp(join(tmpdir(), 'tk-writing-playwright-'));
    if (interrupted) throw interrupted;
    // Context routes cannot cover worker WebSockets. This run-owned proxy
    // never forwards connections, including loopback and TLS tunnels.
    denyProxy = createServer(socket => socket.destroy());
    await new Promise((resolve, reject) => {
      denyProxy.once('error', reject);
      denyProxy.listen(0, '127.0.0.1', resolve);
    });
    if (interrupted) throw interrupted;
    context = await chromium.launchPersistentContext(profile, {
      executablePath, headless: true, chromiumSandbox: true, viewport, deviceScaleFactor,
      timeout: 20000, handleSIGINT: false, handleSIGTERM: false, handleSIGHUP: false,
      serviceWorkers: 'block',
      proxy: {server: `http://127.0.0.1:${denyProxy.address().port}`, bypass: '<-loopback>'},
      // GPU surfaces can lose content in extreme-height captures.
      args: ['--disable-gpu', '--disable-background-networking', '--disable-quic',
        '--host-resolver-rules=MAP * ~NOTFOUND', '--force-webrtc-ip-handling-policy=disable_non_proxied_udp'],
    });
  })();
  const work = (async () => {
    await launch;
    if (interrupted) throw interrupted;
    if (typeof context.routeWebSocket !== 'function') throw new Error('Blocked: Playwright 1.48+ is required for WebSocket blocking.');
    context.setDefaultTimeout(15000);
    context.setDefaultNavigationTimeout(15000);
    await context.route('**/*', route => /^(?:file|data|about|blob):/.test(route.request().url()) ? route.continue() : route.abort('blockedbyclient'));
    await context.routeWebSocket('**/*', socket => socket.close());
    if (interrupted) throw interrupted;
    const page = context.pages()[0] || await context.newPage();
    if (interrupted) throw interrupted;
    return await action(page);
  })();
  try {
    return await Promise.race([work, stopped]);
  } finally {
    clearTimeout(timer);
    try {
      // Acquisition is bounded by Playwright's launch timeout; never await a hung action.
      await launch.catch(() => {});
      if (context) await context.close();
    } finally {
      try {
        if (denyProxy?.listening) await new Promise(resolve => denyProxy.close(resolve));
        if (profile) await rm(profile, {recursive: true, force: true, maxRetries: 5, retryDelay: 100});
      } finally {
        for (const [signal, handler] of handlers) process.removeListener(signal, handler);
      }
    }
  }
}

export async function evaluate(page, expression) {
  return await page.evaluate(expression);
}
