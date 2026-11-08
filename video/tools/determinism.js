#!/usr/bin/env node
/* determinism.js: the frame at time t must not depend on how we got there (CONTRACT §9).
   For each scene and time t: (1) fresh page, seek(t) directly; (2) a second fresh page, seek(t) directly: the two
   PNGs must be IDENTICAL (bit for bit); (3) fresh page, seek through 0, 1/fps, … up to t, then t: compared pixel by
   pixel with (1). Anti-aliasing of edges may differ after sequential seeking (a few hundred pixels, small deltas);
   a state leak between frames (a Canvas setting left behind, a stepper that does not rebuild) shows as thousands of
   pixels or large deltas.
   Usage:
     node tools/determinism.js scenes/<unit>/<page>.html 3.0                         (preview cues, as before)
     node tools/determinism.js scenes/<unit>/<page>.html --times 3,12.5 --entry entry.json|'{json}'
     node tools/determinism.js --timeline out/check/unit_ch04/build/unit_ch04_timeline.json [--only 04.2,04.3]
                               [--times 0.25,0.5,0.75 (fractions of the duration with --timeline, default)] [--fps 15]
   Output: one JSON line per (scene, t): {scene, t, direct_identical, seq_px (pixels that differ), seq_px32 (differ by
   more than 32 levels), seq_max (largest channel delta), verdict: identical | anti-aliasing | DIFFERENT}.
   Exit code 1 if any direct pair differs or any verdict is DIFFERENT (threshold: --tolerance 600 pixels > 32 levels).
   DET_SAVE=<dir> keeps the PNGs. NODE_PATH=/opt/node22/lib/node_modules. */
'use strict';
if (!process.env.NODE_PATH) { process.env.NODE_PATH = '/opt/node22/lib/node_modules'; require('module').Module._initPaths(); }
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const { serve } = require('./server');
const argv = process.argv.slice(2), opt = {}, pos = [];
for (let i = 0; i < argv.length; i++) {
  if (argv[i].startsWith('--')) { const k = argv[i].slice(2), v = argv[i + 1]; if (v === undefined || v.startsWith('--')) opt[k] = true; else { opt[k] = v; i++; } }
  else pos.push(argv[i]);
}
const FPS = +(opt.fps || 30), TOL = +(opt.tolerance || 600);
const FLAGS = ['--disable-gpu-compositing', '--disable-accelerated-2d-canvas', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
  '--ignore-gpu-blocklist', '--force-color-profile=srgb', '--hide-scrollbars', '--font-render-hinting=none'];
const readEntry = (x) => (!x ? null : JSON.parse(String(x).trim().startsWith('{') ? x : fs.readFileSync(x, 'utf8')));

const jobs = [];
if (opt.timeline) {
  const tl = JSON.parse(fs.readFileSync(opt.timeline, 'utf8')), only = opt.only ? new Set(String(opt.only).split(',')) : null;
  const fr = String(opt.times || '0.25,0.5,0.75').split(',').map(Number);
  for (const s of tl.scenes) if (!only || only.has(s.id)) jobs.push({ scene: s.file, id: s.id, entry: s.entry, times: fr.map((f) => +(f <= 1 ? f * s.duration : f).toFixed(3)) });
} else {
  if (!pos[0]) { console.error('usage: node tools/determinism.js <scene.html> <t> | --times a,b [--entry e] | --timeline tl.json [--only ids]'); process.exit(2); }
  jobs.push({ scene: pos[0], id: path.basename(pos[0], '.html'), entry: readEntry(opt.entry), times: String(opt.times || pos[1] || '3').split(',').map(Number) });
}

(async () => {
  const srv = await serve(), port = srv.address().port, b = await chromium.launch({ args: FLAGS });
  const cmp = await (await b.newContext()).newPage();   // pixel comparison in a blank page (no PNG library needed)
  let bad = false;
  const open = async (job) => {
    const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 } }), pg = await ctx.newPage(), errs = [];
    pg.on('pageerror', (e) => errs.push(String(e)));
    await pg.addInitScript(`window.__CAPTURE__=true;` + (job.entry ? `window.__ENTRY__=${JSON.stringify(job.entry)};` : ''));
    await pg.goto(`http://127.0.0.1:${port}/${job.scene}`);
    await pg.waitForFunction(() => window.READY === true || !!window.__SCENE_ERROR__, null, { polling: 50, timeout: 60000 });
    const e = await pg.evaluate(() => window.__SCENE_ERROR__); if (e) errs.push('scene error: ' + e);
    return { ctx, pg, errs };
  };
  const diff = (a, c) => cmp.evaluate(async ([x, y]) => {
    const load = async (b64) => { const im = new Image(); im.src = 'data:image/png;base64,' + b64; await im.decode(); const cv = document.createElement('canvas'); cv.width = im.width; cv.height = im.height; const g = cv.getContext('2d'); g.drawImage(im, 0, 0); return g.getImageData(0, 0, im.width, im.height).data; };
    const A = await load(x), B = await load(y); let px = 0, px32 = 0, mx = 0;
    for (let i = 0; i < A.length; i += 4) { const d = Math.max(Math.abs(A[i] - B[i]), Math.abs(A[i + 1] - B[i + 1]), Math.abs(A[i + 2] - B[i + 2])); if (d) { px++; if (d > 32) px32++; if (d > mx) mx = d; } }
    return { px, px32, mx };
  }, [a.toString('base64'), c.toString('base64')]);
  for (const job of jobs) {
    for (const T of job.times) {
      const shot = async (sequence) => {
        const o = await open(job);
        if (sequence) for (let f = 0; f < Math.round(T * FPS); f++) await o.pg.evaluate((t) => window.seek(t), f / FPS);
        await o.pg.evaluate((t) => window.seek(t), T);
        const png = await o.pg.screenshot();
        if (process.env.DET_SAVE) fs.writeFileSync(path.join(process.env.DET_SAVE, `${job.id}_${T}_${sequence ? 'seq' : 'direct'}.png`), png);
        await o.ctx.close();
        return { png, errs: o.errs };
      };
      const d1 = await shot(false), d2 = await shot(false), sq = await shot(true);
      const h = (x) => crypto.createHash('sha256').update(x.png).digest('hex').slice(0, 16);
      const same = h(d1) === h(d2), r = await diff(d1.png, sq.png);
      const verdict = r.px === 0 ? 'identical' : r.px32 <= TOL ? 'anti-aliasing' : 'DIFFERENT';
      const errs = [...new Set([...d1.errs, ...d2.errs, ...sq.errs])];
      if (!same || verdict === 'DIFFERENT' || errs.length) bad = true;
      console.log(JSON.stringify({ scene: job.id, t: T, direct_identical: same, seq_px: r.px, seq_px32: r.px32, seq_max: r.mx, verdict, ...(errs.length ? { errors: errs } : {}) }));
    }
  }
  await b.close(); srv.close();
  process.exit(bad ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
