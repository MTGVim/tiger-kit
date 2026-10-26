// Run with TK_PLAYWRIGHT_MODULE and an installed TK_CHROMIUM_EXECUTABLE.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../../..');
const fixture = fs.readFileSync(path.join(__dirname, 'fixtures/card-flow.html'), 'utf8');
const titles = [
  '요건과 근거를 함께 보존하는 한국어 결과 문서의 긴 제목',
  'SourceEvidenceAndVerifiedRelationshipsForTheNextReviewWithoutAnArtificialLineLimit',
  '후속 검토에서 재사용할 조건과 예외에 대한 검증 기록',
  'Shared findings and independently verified acceptance evidence',
];

function buildHTML(count) {
  const cards = titles.slice(0, count).map((title, i) =>
    `<li class="ht-card"><h3>${title}</h3><p>결과 ${i + 1}은 서로 다른 목적을 담당하며, 다른 결과와 순차 관계가 없습니다.</p></li>`).join('\n');
  let html = fixture.replace('<!-- RESULTS -->', cards)
    .replace('/* SHARED_THEME_CSS */', fs.readFileSync(path.join(root, 'skills/tk-explain/assets/html-theme.css'), 'utf8'))
    .replace('/* SHARED_THEME_JS */', fs.readFileSync(path.join(root, 'skills/tk-explain/assets/html-theme.js'), 'utf8'));
  if (process.env.TK_FONT_FILE) {
    const font = fs.readFileSync(process.env.TK_FONT_FILE).toString('base64');
    html = html.replace('</style>', `@font-face { font-family: FixtureKorean; src: url(data:font/woff2;base64,${font}); } :root { --font-family: FixtureKorean, sans-serif; }</style>`);
  }
  return html;
}

const reportData = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures/diagnostic-report.json'), 'utf8'));
const escapeHTML = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
function buildReport(data) {
  assert.equal(data.nature, 'illustrative');
  const counts = [new Set(data.analyzedPrs).size, data.findings.length, data.findings.filter(x => x.solved).length];
  const labels = ['분석한 고유 PR 수', '중복 제거한 후보 수', '현재 해결된 후보 수'];
  const summary = data.analyzedPrs.length ? '<dl class="ht-kpis">' + counts.map((n, i) => `<div><dt>${labels[i]}</dt><dd>${n}</dd></div>`).join('') + '</dl>' : '';
  const findings = data.findings.length ? '<ul class="ht-info-list" role="list">' + data.findings.map((f, i) => `<li class="ht-info-row" data-solved="${f.solved}"><span class="ht-info-icon" aria-hidden="true">◇</span><div><h3>${escapeHTML(f.area)}</h3><p class="ht-status">${escapeHTML(f.status)}</p><p>${escapeHTML(f.judgment)}<sup id="cite-${i+1}-1"><a href="#ref-${i+1}" aria-label="참고문헌 ${i+1}">[${i+1}]</a></sup></p><p>${escapeHTML(f.basis)}</p><p>${escapeHTML(f.action)}</p></div></li>`).join('') + '</ul>' : '<p>No change: 확인된 개선 후보가 없습니다. 수집 범위 밖의 결론은 내리지 않습니다.</p>';
  let html = fs.readFileSync(path.join(__dirname, 'fixtures/diagnostic-report.html'), 'utf8')
    .replace('/* SHARED_THEME_CSS */', fs.readFileSync(path.join(root, 'skills/tk-explain/assets/html-theme.css'), 'utf8'))
    .replace('<!-- WINDOW -->', escapeHTML(data.window))
    .replace('<!-- COVERAGE -->', `고유 PR ${counts[0]}개 분석, ${new Set(data.inaccessiblePrs).size}개 접근 불가. 검토 필요는 개선 검토 대상이며, 해결됨은 현재 보호 장치로 확인한 상태입니다.`)
    .replace('<!-- SUMMARY -->', summary).replace('<!-- FINDINGS -->', findings)
    .replace('<!-- REFERENCES -->', data.findings.map((f,i) => `<li id="ref-${i+1}">예시 이력: PR ${f.prs.join(', ')}. <a href="#cite-${i+1}-1">인용 위치로 복귀</a></li>`).join(''));
  if (process.env.TK_FONT_FILE) html = html.replace('</style>', `@font-face { font-family: FixtureKorean; src: url(data:font/woff2;base64,${fs.readFileSync(process.env.TK_FONT_FILE).toString('base64')}); } :root { --font-family: FixtureKorean, sans-serif; }</style>`);
  return html;
}

test('diagnostic rows preserve evidence, counts, semantics and narrow-screen reading', {
  skip: !process.env.TK_PLAYWRIGHT_MODULE || !process.env.TK_CHROMIUM_EXECUTABLE,
}, async () => {
  const { chromium } = require(process.env.TK_PLAYWRIGHT_MODULE);
  const browser = await chromium.launch({ headless: true, executablePath: process.env.TK_CHROMIUM_EXECUTABLE,
    args: ['--no-sandbox', '--disable-webgl', '--disable-dev-shm-usage'] });
  const output = process.env.TK_EVIDENCE_DIR;
  const results = [];
  try {
    for (const width of [1280, 390]) for (const theme of ['light', 'dark', 'system']) {
      const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width, height: 1000 },
        isMobile: width < 600, colorScheme: theme === 'light' ? 'light' : 'dark', reducedMotion: 'reduce' });
      const page = await context.newPage();
      await page.route('**/*', route => { throw new Error('Offline report requested network: ' + route.request().url()); });
      await page.setContent(buildReport(reportData).replace('data-default-theme="system"', `data-default-theme="system"${theme === 'system' ? '' : ` data-theme="${theme}"`}`));
      await page.evaluate(async () => { await document.fonts.ready; });
      assert.deepEqual(await page.locator('.ht-kpis dd').allTextContents(), ['3', '2', '1']);
      assert.equal(await page.evaluate(() => getComputedStyle(document.body).backgroundColor), theme === 'light' ? 'rgb(233, 237, 243)' : 'rgb(16, 19, 25)');
      assert.equal(await page.locator('[data-solved="true"]').count(), 1);
      assert.equal(await page.locator('#criteria-title + ol > li').count(), 4);
      const snapshot = await page.locator('main').ariaSnapshot();
      for (const text of ['완료 기준', '분석한 고유 PR 수', '검토 필요', '해결됨', '참고문헌']) assert.ok(snapshot.includes(text));
      const geometry = await page.evaluate(() => {
        const errors = [];
        for (const row of document.querySelectorAll('.ht-info-row, .ht-kpis > div, .ht-callout')) {
          const b = row.getBoundingClientRect();
          for (const e of row.querySelectorAll('h3,p,dt,dd')) {
            const range = document.createRange(); range.selectNodeContents(e);
            for (const r of range.getClientRects()) if (r.x < b.x - 1 || r.right > b.right + 1 || r.y < b.y - 1 || r.bottom > b.bottom + 1) errors.push(e.textContent);
          }
        }
        return { width: innerWidth, scroll: document.documentElement.scrollWidth, errors };
      });
      assert.equal(geometry.width, width); assert.ok(geometry.scroll <= width); assert.deepEqual(geometry.errors, []);
      if (output && theme !== 'system') { fs.mkdirSync(output, { recursive: true }); await page.screenshot({ path: path.join(output, `diagnostic-${width}-${theme}.png`), fullPage: true }); fs.writeFileSync(path.join(output, 'diagnostic-report.html'), buildReport(reportData)); }
      await page.keyboard.press('Tab'); await page.keyboard.press('Enter');
      assert.equal(await page.evaluate(() => location.hash), '#ref-1');
      await page.evaluate(() => { for (const e of document.querySelectorAll('.ht-info-icon')) e.remove(); for (const s of document.styleSheets) s.disabled = true; });
      for (const text of ['1. 범위를 확인합니다.', '2. 독립 사건을 구별합니다.', '3. 근거를 연결합니다.', '4. 현재 해결 여부를 확인합니다.']) assert.ok((await page.locator('main').innerText()).includes(text));
      await page.setContent(buildReport({ ...reportData, analyzedPrs: [], findings: [] }));
      assert.equal(await page.locator('.ht-kpis').count(), 0); assert.equal(await page.locator('[data-solved]').count(), 0);
      assert.ok((await page.locator('main').innerText()).includes('No change'));
      results.push({ width, theme, ...geometry, noJS: true, iconAndCSSRemoval: 'Pass', emptyAndPartial: 'Pass' });
      await context.close();
    }
    if (output) fs.writeFileSync(path.join(output, 'diagnostic-results.json'), JSON.stringify(results, null, 2));
  } finally { await browser.close(); }
});

test('card flow preserves grouping, text geometry and offline controls across viewports', {
  skip: !process.env.TK_PLAYWRIGHT_MODULE || !process.env.TK_CHROMIUM_EXECUTABLE,
}, async () => {
  const { chromium } = require(process.env.TK_PLAYWRIGHT_MODULE);
  const browser = await chromium.launch({ headless: true, executablePath: process.env.TK_CHROMIUM_EXECUTABLE,
    args: ['--no-sandbox', '--disable-webgl', '--disable-dev-shm-usage'] });
  const records = [];
  const output = process.env.TK_EVIDENCE_DIR;
  if (output) fs.mkdirSync(output, { recursive: true });
  try {
    for (const width of [1280, 390, 500]) for (const theme of ['light', 'dark', 'system']) for (const count of [1, 2, 4]) {
      const context = await browser.newContext({ viewport: { width, height: 1000 }, deviceScaleFactor: 1,
        isMobile: width < 600, colorScheme: theme === 'light' ? 'light' : 'dark', reducedMotion: 'reduce' });
      const page = await context.newPage();
      await page.route('**/*', route => { throw new Error('Offline fixture requested network: ' + route.request().url()); });
      await page.setContent(buildHTML(count));
      await page.evaluate(async theme => { await document.fonts.ready;
        if (theme !== 'system') document.querySelector(`input[value="${theme}"]`).click();
      }, theme);
      const geometry = await page.evaluate(() => {
        const cards = [...document.querySelectorAll('.ht-flow-results > li')];
        const rects = cards.map(e => { const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height }; });
        const clipped = [];
        for (const card of document.querySelectorAll('.ht-flow .ht-card')) {
          const bounds = card.getBoundingClientRect();
          for (const text of card.querySelectorAll('h2,h3,p,a')) {
            const range = document.createRange(); range.selectNodeContents(text);
            for (const r of range.getClientRects()) if (r.x < bounds.x - 1 || r.right > bounds.right + 1 || r.y < bounds.y - 1 || r.bottom > bounds.bottom + 1) clipped.push(text.textContent);
          }
        }
        return { width: innerWidth, scroll: document.documentElement.scrollWidth, rects, clipped,
          stages: [...document.querySelectorAll('.ht-flow > li h2')].map(e => e.textContent),
          results: cards.map(e => e.querySelector('h3').textContent),
          background: getComputedStyle(document.body).backgroundColor,
          relation: document.querySelector('.ht-flow-link').textContent };
      });
      assert.equal(geometry.width, width); assert.ok(geometry.scroll <= width);
      assert.deepEqual(geometry.clipped, []); assert.equal(geometry.rects.length, count);
      assert.deepEqual(geometry.stages, ['입력 자료', '중심 처리', '동시 결과', '후속 재사용']);
      assert.deepEqual(geometry.results, titles.slice(0, count));
      assert.equal(geometry.background, theme === 'light' ? 'rgb(233, 237, 243)' : 'rgb(16, 19, 25)');
      const r = geometry.rects;
      if (count === 1) assert.ok(r[0].width > width * (width < 600 ? .7 : .5));
      else if (width < 600) for (let i = 1; i < count; i++) assert.ok(r[i].y >= r[i - 1].y + r[i - 1].height);
      else { assert.equal(r[0].y, r[1].y); assert.ok(r[1].x >= r[0].x + r[0].width); if (count === 4) assert.ok(r[2].y >= r[0].y + r[0].height); }
      if (output && count === 4 && width !== 500 && theme !== 'system') {
        await page.screenshot({ path: path.join(output, `card-flow-${width}-${theme}.png`), fullPage: true });
        fs.writeFileSync(path.join(output, 'card-flow.html'), buildHTML(4));
      }
      await page.locator(`input[value="${theme}"]`).focus();
      await page.keyboard.press('ArrowRight');
      const next = { system: 'light', light: 'dark', dark: 'system' }[theme];
      assert.equal(await page.locator(`input[value="${next}"]`).isChecked(), true);
      assert.equal(await page.evaluate(() => document.documentElement.getAttribute('data-theme')), next === 'system' ? null : next);
      await page.keyboard.press('Tab');
      assert.equal(await page.locator('a').evaluate(e => e === document.activeElement), true);
      await page.keyboard.press('Enter');
      assert.equal(await page.evaluate(() => location.hash), '#flow-title');
      records.push({ width, theme, count, ...geometry });
      await context.close();
    }
    const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 1000 }, colorScheme: 'dark' });
    const page = await context.newPage(); await page.setContent(buildHTML(4));
    assert.equal(await page.locator('.ht-flow-results > li').count(), 4);
    assert.equal(await page.locator('[data-ht-theme-control]').isVisible(), false);
    assert.ok(await page.locator('.ht-flow').innerText());
    await page.keyboard.press('Tab'); assert.equal(await page.locator('a').evaluate(e => e === document.activeElement), true);
    await page.keyboard.press('Enter'); assert.equal(await page.evaluate(() => location.hash), '#flow-title');
    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
    await context.close();
    if (output) fs.writeFileSync(path.join(output, 'render-results.json'), JSON.stringify({ browser: browser.version(), checks: records, noJS: 'Pass' }, null, 2));
  } finally { await browser.close(); }
});

test('two-row references keep backlinks and wrap long titles without clipping', {
  skip: !process.env.TK_PLAYWRIGHT_MODULE || !process.env.TK_CHROMIUM_EXECUTABLE,
}, async () => {
  const { chromium } = require(process.env.TK_PLAYWRIGHT_MODULE);
  const browser = await chromium.launch({ headless: true, executablePath: process.env.TK_CHROMIUM_EXECUTABLE,
    args: ['--no-sandbox', '--disable-webgl', '--disable-dev-shm-usage'] });
  try {
    for (const width of [1280, 390]) for (const theme of ['light', 'dark']) {
      const context = await browser.newContext({ javaScriptEnabled: false,
        viewport: { width, height: 1000 }, reducedMotion: 'reduce', colorScheme: theme });
      const page = await context.newPage();
      await page.route('**/*', route => { throw new Error('Offline reference requested network: ' + route.request().url()); });
      for (const long of [false, true]) {
        const title = long ? '한국어 설명의 조건과 실제 동작을 순서대로 확인하는 긴 참고 자료 제목 '.repeat(12) : '자료 제목';
        const entry = `<li id="ref-1"><a href="https://example.org/guide">${title}</a><span class="ht-ref-meta">기관, 2026. 근거: 동작 원리 <a href="#cite-1-1" aria-label="첫 인용으로 복귀">↩ 1</a> <a href="#cite-1-2" aria-label="둘째 인용으로 복귀">↩ 2</a></span></li>`;
        const html = fs.readFileSync(path.join(root, 'skills/tk-research/assets/report.html'), 'utf8')
          .replace(/<li id="ref-1">[\s\S]*?<\/li>/, entry)
          .replace('data-default-theme="system"', `data-default-theme="${theme}" data-theme="${theme}"`);
        await page.setContent(html);
        await page.evaluate(() => document.fonts.ready);
        assert.equal(await page.locator('#ref-1 > .ht-ref-meta').count(), 1);
        assert.equal(await page.locator('#ref-1 > .ht-ref-meta').evaluate(el => getComputedStyle(el).display), 'block');
        const layout = await page.locator('#ref-1').evaluate(li => {
          const box = li.getBoundingClientRect();
          const range = document.createRange(); range.selectNodeContents(li);
          const rects = [...range.getClientRects()];
          return { lines: new Set(rects.map(r => Math.round(r.top))).size,
            clipped: rects.some(r => r.left < box.left - 1 || r.right > box.right + 1),
            nowrap: getComputedStyle(li).whiteSpace === 'nowrap',
            overflow: document.documentElement.scrollWidth > innerWidth };
        });
        assert.equal(layout.clipped, false); assert.equal(layout.overflow, false); assert.equal(layout.nowrap, false);
        // Inline text and anchors may have different font baselines: compare total height instead.
        const height = await page.locator('#ref-1').evaluate(li => ({ actual: li.getBoundingClientRect().height,
          line: parseFloat(getComputedStyle(li).lineHeight) }));
        if (!long) assert.ok(height.actual >= height.line * 2 - 1);
        if (long && width === 390) assert.ok(height.actual > height.line * 2);
        for (const occurrence of ['cite-1-1', 'cite-1-2']) {
          await page.locator(`#${occurrence} > a`).click();
          assert.equal(await page.evaluate(() => location.hash), '#ref-1');
          await page.locator(`#ref-1 a[href="#${occurrence}"]`).click();
          assert.equal(await page.evaluate(() => location.hash), `#${occurrence}`);
        }
      }
      await context.close();
    }
  } finally { await browser.close(); }
});

test('visual-stack children contain a wide SVG scroller at 360px', {
  skip: !process.env.TK_PLAYWRIGHT_MODULE || !process.env.TK_CHROMIUM_EXECUTABLE,
}, async () => {
  const { chromium } = require(process.env.TK_PLAYWRIGHT_MODULE);
  const browser = await chromium.launch({headless:true, executablePath:process.env.TK_CHROMIUM_EXECUTABLE,
    args:['--no-sandbox','--disable-webgl','--disable-dev-shm-usage']});
  const current = fs.readFileSync(path.join(root,'skills/tk-explain/assets/html-theme.css'),'utf8');
  const variants = [['after',current]];
  if (process.env.TK_FORMATTING_BASELINE) {
    const {spawnSync} = require('node:child_process');
    const before=spawnSync('git',['show',`${process.env.TK_FORMATTING_BASELINE}:skills/tk-explain/assets/html-theme.css`],{cwd:root,encoding:'utf8'});
    assert.equal(before.status,0,before.stderr); variants.unshift(['before',before.stdout]);
  }
  try {
    for(const theme of ['light','dark']) for(const width of [360,1280]) for(const [phase,css] of variants) {
      const context=await browser.newContext({viewport:{width,height:800},javaScriptEnabled:false,colorScheme:theme});
      const page=await context.newPage();
      await page.route('**/*',route=>{throw Error('Unexpected network request');});
      await page.setContent(`<!doctype html><html lang="ko" data-theme="${theme}"><meta charset="utf-8"><style>${css}</style><style>main{margin:16px}figure{margin-inline:0}.wide{min-width:640px}</style><main><div class="ht-visual-stack"><figure><div class="ht-table-scroll" tabindex="0" aria-label="가로로 볼 수 있는 그림"><svg class="wide" viewBox="0 0 640 180" role="img" aria-label="두 줄 비교"><text x="10" y="40">이전 상태</text><text x="10" y="130">갱신 후 상태</text></svg></div><figcaption>서로 다른 두 시점의 상태</figcaption></figure></div></main></html>`);
      const measurement=await page.evaluate(()=>({pageOverflow:document.documentElement.scrollWidth>innerWidth,
        wrapperWidth:document.querySelector('.ht-table-scroll').clientWidth,
        scrollWidth:document.querySelector('.ht-table-scroll').scrollWidth}));
      if(phase==='before' && width===360) assert.equal(measurement.pageOverflow,true);
      else {
        assert.equal(measurement.pageOverflow,false,JSON.stringify({phase,theme,width,measurement}));
        if(width===360) assert.ok(measurement.scrollWidth>measurement.wrapperWidth);
      }
      await page.locator('figure').evaluate(el=>el.classList.add('ht-figure'));
      if(phase==='after') {
        const framed=await page.locator('figure').evaluate(el=>({border:getComputedStyle(el).borderTopWidth,
          overflow:document.documentElement.scrollWidth>innerWidth,
          containsCaption:el.contains(document.querySelector('figcaption'))}));
        assert.deepEqual(framed,{border:'1px',overflow:false,containsCaption:true});
        const scroller=page.locator('.ht-table-scroll');await scroller.focus();
        await page.keyboard.press('ArrowRight');
        // Reduced/smooth key scrolling can be asynchronous: programmatic containment is deterministic.
        assert.ok(await scroller.evaluate(el=>{el.scrollLeft=100;return el.scrollLeft>0 || el.scrollWidth===el.clientWidth;}));
      }
      await context.close();
    }
  } finally {await browser.close();}
});
