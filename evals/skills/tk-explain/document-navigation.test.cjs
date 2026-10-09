// Explicit local browser integration check; does not install a provider or browser.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const {chromium} = require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES + '/playwright');
const root = path.resolve(__dirname, '../../..');
const executablePath = process.env.TIGERKIT_BROWSER_PATH;
if (!executablePath) throw Error('Set TIGERKIT_BROWSER_PATH to an explicitly selected installed headless browser');
const evidence = path.join(root, '.tigerkit/evidence/issues-443-444');
const url = pathToFileURL(path.join(root, 'skills/tk-research/assets/report.html')).href;
const results = [];
async function geometry(page, width) {
  const measured = await page.evaluate(() => {
    const nav = document.querySelector('.ht-doc-nav').getBoundingClientRect();
    const panel = document.querySelector('.ht-doc-toc-panel').getBoundingClientRect();
    const content = document.querySelector('main').getBoundingClientRect();
    const bar = document.querySelector('.ht-topbar').getBoundingClientRect();
    const theme = document.querySelector('[data-ht-theme-control]').getBoundingClientRect();
    return {width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
      nav: {left: nav.left, right: nav.right, top: nav.top, bottom: nav.bottom},
      panel: {left: panel.left, right: panel.right, top: panel.top, bottom: panel.bottom},
      contentRight: content.right, height: innerHeight,
      themeInBar: theme.top >= bar.top && theme.bottom <= bar.bottom};
  });
  assert.equal(measured.width, width);
  assert.ok(measured.scrollWidth <= width, JSON.stringify(measured));
  assert.ok(measured.nav.right <= width && measured.nav.left >= measured.contentRight);
  assert.ok(measured.nav.top >= 0 && measured.nav.bottom <= measured.height);
  assert.ok(measured.panel.left >= 0 && measured.panel.right <= width && measured.panel.top >= 0 && measured.panel.bottom <= measured.height);
  if (width >= 1280) assert.ok(measured.themeInBar);
  return measured;
}
async function atHash(page, id) {
  await page.waitForFunction(id => location.hash === '#' + id, id);
  // Wait for the user-facing native smooth scroll to settle; no capture-only scroll override.
  await page.waitForFunction(id => {
    if (id === 'document-top') return scrollY < 2;
    const target = document.getElementById(id).getBoundingClientRect();
    const bar = document.querySelector('.ht-topbar');
    const top = getComputedStyle(bar).position === 'sticky' ? bar.getBoundingClientRect().bottom : 0;
    return target.top >= top - 1 && target.top < innerHeight;
  }, id);
}
(async () => {
  const browser = await chromium.launch({headless: true, executablePath});
  try {
    for (const width of [1280, 390, 500]) for (const colorScheme of ['light', 'dark']) {
      const context = await browser.newContext({viewport: {width, height: 900}, deviceScaleFactor: 1, locale: 'ko-KR', colorScheme});
      const page = await context.newPage(); const errors = [], requests = [];
      page.on('pageerror', error => errors.push(error.message));
      await page.route('**/*', route => { if (/^https?:/.test(route.request().url())) {requests.push(route.request().url()); return route.abort();} return route.continue(); });
      await page.goto(url);
      const summary = page.locator('.ht-doc-toc > summary');
      await summary.focus(); await page.keyboard.press('Enter');
      assert.equal(await page.locator('.ht-doc-toc').getAttribute('open'), '');
      const measured = await geometry(page, width);
      await page.screenshot({path: path.join(evidence, `after-${width}-${colorScheme}.png`)});
      await page.keyboard.press('Tab');
      assert.equal(await page.evaluate(() => document.activeElement.hash), '#overview');
      await page.keyboard.press('Escape');
      assert.ok(await summary.evaluate(el => document.activeElement === el));
      assert.equal(await page.locator('.ht-doc-toc').getAttribute('open'), null);
      await summary.press('Space');
      await page.locator('.ht-doc-toc-panel a').first().press('Enter'); await atHash(page, 'overview');
      assert.ok(await page.locator('#overview').evaluate(el => document.activeElement === el));
      assert.equal(await page.locator('.ht-doc-toc').getAttribute('open'), null);
      for (const id of ['context', 'status', 'directions', 'experiments', 'unknowns', 'frontier', 'sources']) {
        await summary.click(); await page.locator(`.ht-doc-toc-panel a[href="#${id}"]`).click(); await atHash(page, id);
      }
      await page.locator('.ht-doc-nav > a[href="#document-top"]').click(); await atHash(page, 'document-top');
      await page.waitForFunction(() => scrollY < 2);
      await page.locator('.ht-doc-nav > a[href="#document-bottom"]').click(); await atHash(page, 'document-bottom');
      await page.waitForFunction(() => innerHeight + scrollY >= document.documentElement.scrollHeight - 2);
      const firstCitation = page.locator('#cite-1-1 a');
      await firstCitation.hover();
      assert.equal(await page.locator('.ht-citation-preview').isVisible(), true);
      assert.match(await page.locator('.ht-citation-preview').innerText(), /실제로 읽은 근거/);
      assert.doesNotMatch(await page.locator('.ht-citation-preview').innerText(), /↩/);
      await page.mouse.move(0, 0);
      assert.equal(await page.locator('.ht-citation-preview').isHidden(), true);
      await firstCitation.focus();
      assert.equal(await firstCitation.getAttribute('aria-describedby'), 'ht-citation-preview');
      await page.keyboard.press('Escape');
      assert.equal(await page.locator('.ht-citation-preview').isHidden(), true);
      for (const cite of ['cite-1-1', 'cite-1-2']) {
        await page.goto(url + '#' + cite); await atHash(page, cite);
        await page.locator(`#${cite} a`).click(); await atHash(page, 'ref-1');
        await page.locator(`#ref-1 a[href="#${cite}"]`).click(); await atHash(page, cite);
        assert.equal(await page.locator(`#${cite}`).evaluate(el => getComputedStyle(el).outlineStyle), "none");
      }
      await page.reload(); await atHash(page, 'cite-1-2');
      await page.locator('#cite-1-2 a').click(); await atHash(page, 'ref-1');
      await page.goBack(); await atHash(page, 'cite-1-2');
      await summary.click(); await page.locator('h1').click();
      assert.equal(await page.locator('.ht-doc-toc').getAttribute('open'), null);
      for (const theme of ['dark', 'light', 'system']) {
        await page.locator(`label:has(input[name="ht-theme"][value="${theme}"])`).click();
        assert.equal(await page.locator('html').getAttribute('data-theme'), theme === 'system' ? null : theme);
      }
      await page.locator('input[name="ht-theme"][value="system"]').focus();
      await page.keyboard.press('ArrowRight');
      assert.equal(await page.locator('html').getAttribute('data-theme'), 'light');
      await page.emulateMedia({reducedMotion: 'reduce'});
      assert.equal(await page.evaluate(() => getComputedStyle(document.documentElement).scrollBehavior), 'auto');
      assert.deepEqual(errors, []); assert.deepEqual(requests, []);
      results.push({width, colorScheme, status: 'Pass', measured});
      await context.close();
    }
    const nested = path.join(root, '.tigerkit/tmp/issues-443-444/nested-after.html');
    let nestedHTML = fs.readFileSync(path.join(root, 'skills/tk-research/assets/report.html'), 'utf8');
    nestedHTML = nestedHTML.replace('<li><a href="#context">문제와 배경</a></li>', '<li><a href="#context">문제와 배경</a><ol><li><a href="#conditions">판단 조건</a></li></ol></li>');
    const parentStart = nestedHTML.indexOf('<section id="context">');
    const parentEnd = nestedHTML.indexOf('</section>', parentStart);
    nestedHTML = nestedHTML.slice(0, parentEnd) + '<section id="conditions" style="min-height:1000px"><h3>판단 조건</h3><p>상위 섹션 안에서 읽는 하위 섹션입니다.</p></section>' + nestedHTML.slice(parentEnd);
    fs.writeFileSync(nested, nestedHTML);
    for (const width of [1280, 390]) {
      const context = await browser.newContext({viewport:{width, height:900}, reducedMotion:'reduce'});
      const page = await context.newPage(); await page.goto(pathToFileURL(nested).href);
      await page.locator('.ht-doc-toc summary').click();
      await page.locator('.ht-doc-toc-panel a[href="#conditions"]').click(); await atHash(page, 'conditions');
      await page.waitForFunction(() => document.querySelector('.ht-doc-toc-panel [aria-current]').hash === '#conditions');
      await page.evaluate(() => scrollBy({top:100, behavior:'instant'}));
      await page.waitForFunction(() => document.querySelector('.ht-doc-toc-panel [aria-current]').hash === '#conditions');
      await page.locator('.ht-doc-toc summary').click();
      await geometry(page, width);
      await page.screenshot({path:path.join(evidence, `nested-after-${width}.png`)});
      results.push({width, nestedTOC:true, status:'Pass'}); await context.close();
    }
    for (const width of [1280, 390]) {
      const context = await browser.newContext({javaScriptEnabled: false, viewport: {width, height: 900}, reducedMotion: 'reduce'});
      const page = await context.newPage(); await page.goto(url);
      await page.locator('.ht-doc-toc > summary').focus(); await page.keyboard.press('Enter');
      await geometry(page, width);
      await page.keyboard.press('Tab'); await page.keyboard.press('Enter'); await atHash(page, 'overview');
      // Native no-JS disclosure can be closed with its summary; Escape is an enhancement.
      await page.locator('.ht-doc-toc > summary').click();
      await page.goto(url + '#cite-1-2'); await atHash(page, 'cite-1-2');
      await page.locator('#cite-1-2 a').click(); await atHash(page, 'ref-1');
      await page.locator('#ref-1 a[href="#cite-1-2"]').click(); await atHash(page, 'cite-1-2');
      await page.screenshot({path: path.join(evidence, `no-js-${width}.png`)});
      assert.ok(await page.locator('main').innerText());
      assert.ok(await page.locator('[data-ht-theme-control]').isHidden());
      results.push({width, javaScript: false, status: 'Pass'}); await context.close();
    }
    fs.writeFileSync(path.join(evidence, 'browser-results.json'), JSON.stringify({browser: browser.version(), provider:'playwright', headless:true, profile:'isolated run-owned contexts', auth:'none', target:url, capture_only_mutation:'none', checks:results, cleanup:'browser and contexts closed by finally'}, null, 2));
    console.log(JSON.stringify({status:'Pass', checks:results.length, browser:browser.version()}));
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
