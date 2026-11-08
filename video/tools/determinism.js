#!/usr/bin/env node
/* determinism.js: the frame at time t must not depend on how we got there.
   For each scene: (1) fresh page, seek(t) directly; (2) fresh page, seek through 0, 1/30, ... up to t;
   (3) a second fresh page, seek(t) directly. Compares SHA-256 of the PNG screenshots.
   Usage: NODE_PATH=/opt/node22/lib/node_modules node tools/determinism.js scenes/a_fieldlines.html 3.0 */
'use strict';
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path'), crypto = require('crypto');
const ROOT = path.resolve(__dirname, '..');
const [scene, tStr] = process.argv.slice(2), T = +tStr;
const srv = http.createServer((q, r) => { const p = path.join(ROOT, decodeURIComponent(new URL(q.url, 'http://x').pathname));
  if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); }
  const ty = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json' }[path.extname(p)];
  r.writeHead(200, ty ? { 'content-type': ty } : {}); fs.createReadStream(p).pipe(r); });
srv.listen(0, '127.0.0.1', async () => {
  const b = await chromium.launch({ args: ['--disable-gpu-compositing', '--disable-accelerated-2d-canvas', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--force-color-profile=srgb', '--hide-scrollbars'] });
  const shot = async (sequence) => {
    const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 } }); const pg = await ctx.newPage();
    await pg.addInitScript('window.__CAPTURE__=true;');
    await pg.goto(`http://127.0.0.1:${srv.address().port}/${scene}`);
    await pg.waitForFunction(() => window.READY === true, null, { polling: 50 });
    if (sequence) for (let f = 0; f < Math.round(T * 30); f++) await pg.evaluate((t) => window.seek(t), f / 30);
    await pg.evaluate((t) => window.seek(t), T);
    const png = await pg.screenshot();
    if (process.env.DET_SAVE) fs.writeFileSync(path.join(process.env.DET_SAVE, (sequence ? 'seq' : 'direct') + '.png'), png);
    const h = crypto.createHash('sha256').update(png).digest('hex').slice(0, 16);
    await ctx.close(); return h;
  };
  const direct = await shot(false), seq = await shot(true), again = await shot(false);
  console.log(JSON.stringify({ scene, t: T, direct, sequential: seq, direct_again: again, identical: direct === seq && seq === again }));
  await b.close(); srv.close();
});
