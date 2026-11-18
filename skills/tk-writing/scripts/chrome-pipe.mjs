/** Static offline capture fallback. Private Chrome pipe; no listening debug port. */
import {spawn} from 'node:child_process';

export async function launchChromePipe(executable, profile, proxy, viewport, deviceScaleFactor) {
  const child = spawn(executable, [
    '--headless=new', '--remote-debugging-pipe', `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--disable-gpu',
    '--disable-background-networking', '--disable-quic',
    '--host-resolver-rules=MAP * ~NOTFOUND', '--force-webrtc-ip-handling-policy=disable_non_proxied_udp',
    `--proxy-server=${proxy}`, '--proxy-bypass-list=<-loopback>', 'about:blank',
  ], {stdio: ['ignore', 'ignore', 'pipe', 'pipe', 'pipe']});
  let sequence = 0, pending = Buffer.alloc(0), stderr = '', closed = false;
  const calls = new Map();
  const exited = new Promise(resolve => child.once('close', resolve));
  const fail = error => { closed = true; for (const {reject} of calls.values()) reject(error); calls.clear(); };
  child.on('error', fail);
  child.on('exit', () => fail(new Error(`Chrome exited (${child.exitCode ?? child.signalCode}): ${stderr}`)));
  child.stderr.on('data', data => { stderr = (stderr + data.toString()).slice(-4000); });
  child.stdio[3].on('error', fail);
  child.stdio[4].on('error', fail);
  child.stdio[4].on('end', () => fail(new Error(`Chrome pipe ended: ${stderr}`)));
  child.stdio[4].on('data', chunk => {
    pending = Buffer.concat([pending, chunk]);
    let end;
    while ((end = pending.indexOf(0)) >= 0) {
      const data = pending.subarray(0, end); pending = pending.subarray(end + 1);
      let message;
      try { message = JSON.parse(data.toString()); } catch { fail(new Error('Invalid Chrome pipe response')); continue; }
      const call = calls.get(message.id);
      if (!call) continue;
      calls.delete(message.id);
      if (message.error) call.reject(new Error(message.error.message));
      else call.resolve(message.result);
    }
  });
  function send(method, params = {}, sessionId) {
    if (closed) return Promise.reject(new Error(`Chrome pipe closed: ${stderr}`));
    const id = ++sequence;
    return new Promise((resolve, reject) => {
      calls.set(id, {resolve, reject});
      child.stdio[3].write(JSON.stringify({id, method, params, ...(sessionId ? {sessionId} : {})}) + '\0');
    });
  }
  const close = async () => {
    if (child.exitCode === null && child.signalCode === null) child.kill('SIGTERM');
    const timer = setTimeout(() => child.kill('SIGKILL'), 1000);
    try { await exited; } finally { clearTimeout(timer); }
  };
  // Acquisition must end even when Chrome never answers; callers also bound the whole capture.
  const timer = setTimeout(() => { fail(new Error('Chrome pipe launch timeout (20000ms)')); child.kill('SIGKILL'); }, 20000);
  try {
    const {targetId} = await send('Target.createTarget', {url: 'about:blank'});
    const {sessionId} = await send('Target.attachToTarget', {targetId, flatten: true});
    const command = (method, params) => send(method, params, sessionId);
    await command('Page.enable');
    await command('Runtime.enable');
    await command('Network.enable');
    await command('Network.setBypassServiceWorker', {bypass: true});
    await command('Network.setBlockedURLs', {urls: ['http://*', 'https://*', 'ws://*', 'wss://*', 'ftp://*']});
    const page = {
      async evaluate(expression) {
        const {result, exceptionDetails} = await command('Runtime.evaluate', {expression, awaitPromise: true, returnByValue: true});
        if (exceptionDetails) throw new Error(exceptionDetails.exception?.description || exceptionDetails.text);
        return result.value;
      },
      async goto(url) {
        if (!url.startsWith('file:')) throw new Error('Chrome pipe capture accepts only local file URLs');
        const navigation = await command('Page.navigate', {url});
        if (navigation.errorText) throw new Error(navigation.errorText);
        // A navigation reply can arrive before the new document context exists.
        const deadline = Date.now() + 15000;
        while (Date.now() < deadline) {
          try { if (await page.evaluate(`location.href === ${JSON.stringify(url)} && document.readyState === 'complete'`)) return; }
          catch (error) { if (!/context|navigat/i.test(error.message)) throw error; }
          await new Promise(resolve => setTimeout(resolve, 25));
        }
        throw new Error('Chrome page load timeout (15000ms)');
      },
      async setViewportSize(size) {
        await command('Emulation.setDeviceMetricsOverride', {...size, deviceScaleFactor, mobile: false});
      },
      async setContent(html) {
        const {frameTree} = await command('Page.getFrameTree');
        await command('Page.setDocumentContent', {frameId: frameTree.frame.id, html});
      },
      async screenshot({clip, omitBackground = false}) {
        if (omitBackground) await command('Emulation.setDefaultBackgroundColorOverride', {color: {r: 0, g: 0, b: 0, a: 0}});
        const {data} = await command('Page.captureScreenshot', {format: 'png', fromSurface: true, captureBeyondViewport: true, clip: {...clip, scale: 1}});
        return Buffer.from(data, 'base64');
      },
    };
    await page.setViewportSize(viewport);
    return {page, close};
  } catch (error) {
    await close();
    throw error;
  } finally { clearTimeout(timer); }
}
