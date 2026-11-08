#!/usr/bin/env node
/* stills.js: render chosen times of a scene to PNG (QA contact sheets, quick checks).
   NODE_PATH=/opt/node22/lib/node_modules node stills.js --scene scenes/b_induction.html --times 0.5,2,5 --outdir out/stills [--entry '{...}'] */
'use strict';
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = __dirname, argv = process.argv.slice(2), opt = {};
for (let i = 0; i < argv.length; i += 2) opt[argv[i].slice(2)] = argv[i + 1];
const entry = opt.entry ? JSON.parse(opt.entry) : {};
const srv = http.createServer((req, res) => { const p = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  const t = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json' }[path.extname(p)];
  res.writeHead(200, t ? { 'content-type': t } : {}); fs.createReadStream(p).pipe(res); });
srv.listen(0, '127.0.0.1', async () => {
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--force-color-profile=srgb', '--hide-scrollbars'] });
  const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = []; pg.on('pageerror', (e) => errs.push(String(e))); pg.on('console', (m) => m.type() === 'error' && errs.push(m.text()));
  await pg.addInitScript(`window.__CAPTURE__=true; window.__ENTRY__=${JSON.stringify(entry)};`);
  await pg.goto(`http://127.0.0.1:${srv.address().port}/${opt.scene}`);
  await pg.waitForFunction(() => window.READY === true || !!window.__SCENE_ERROR__, null, { timeout: 60000, polling: 50 });
  const e = await pg.evaluate(() => window.__SCENE_ERROR__); if (e) { console.log(JSON.stringify({ scene: opt.scene, errors: [e] })); await b.close(); srv.close(); process.exit(1); }
  fs.mkdirSync(opt.outdir, { recursive: true });
  const base = path.basename(opt.scene, '.html');
  for (const t of opt.times.split(',').map(Number)) {
    await pg.evaluate((t) => window.seek(t), t);
    await pg.screenshot({ path: path.join(opt.outdir, `${base}_t${t.toFixed(2)}.png`) });
  }
  console.log(JSON.stringify({ scene: opt.scene, errors: errs }));
  await b.close(); srv.close();
});
