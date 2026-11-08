#!/usr/bin/env node
/* stills.js: render chosen times of scenes to PNG (QA stills, contact sheets, `make check`).
 *
 *   node stills.js --scene scenes/ch04/04_1_three_dials.html --times 0.5,2,5 --outdir out/stills [--entry file|json] [--scale 0.5]
 *   node stills.js --timeline script/_build/unit_ch04_timeline.json --outdir out/check/unit_ch04 [--only 04.1,04.2]
 *       check mode: for every scene of the timeline, one still per cue (taken 0.6 s after the cue, before the
 *       next one), plus the first and last frames; page errors, console errors, failed requests and scene
 *       errors are collected (exit code 1), with the runtime's warnings (window.__SCENE_WARNINGS__) and its
 *       layout check at each still (window.__QA__(t), when the runtime provides it); a contact sheet per
 *       scene; report.json.
 */
'use strict';
if (!process.env.NODE_PATH) { process.env.NODE_PATH = '/opt/node22/lib/node_modules'; require('module').Module._initPaths(); }
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const { execFileSync } = require('child_process');
const { serve } = require('./tools/server');
const ROOT = __dirname, argv = process.argv.slice(2), opt = {};
for (let i = 0; i < argv.length; i++) if (argv[i].startsWith('--')) { const k = argv[i].slice(2), v = argv[i + 1];
  if (v === undefined || v.startsWith('--')) opt[k] = true; else { opt[k] = v; i++; } }
const readEntry = (x) => (!x ? {} : JSON.parse(String(x).trim().startsWith('{') ? x : fs.readFileSync(x, 'utf8')));
const scale = +(opt.scale || 1);
const FLAGS = ['--disable-gpu-compositing', '--disable-accelerated-2d-canvas', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
  '--ignore-gpu-blocklist', '--force-color-profile=srgb', '--hide-scrollbars', '--font-render-hinting=none'];

async function shoot(browser, port, scene, entry, times, outdir, base) {
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: scale });
  const pg = await ctx.newPage();
  const errs = [];
  pg.on('pageerror', (e) => errs.push('pageerror: ' + String(e)));
  const dataLike = (u) => /\/data\/|\.(json|f32|bin)(\?|$)/.test(u);   // a 404 on data is expected while the scene is pending
  pg.on('console', (m) => m.type() === 'error' && !/^Failed to load resource/.test(m.text()) && errs.push('console: ' + m.text()));
  pg.on('requestfailed', (r) => { if (!(entry.status === 'pending' && dataLike(r.url()))) errs.push('request failed: ' + r.url().replace(/^http:\/\/127\.0\.0\.1:\d+/, '')); });
  pg.on('response', (r) => r.status() >= 400 && !(entry.status === 'pending' && dataLike(r.url())) && errs.push(`HTTP ${r.status()}: ` + r.url().replace(/^http:\/\/127\.0\.0\.1:\d+/, '')));
  await pg.addInitScript(`window.__CAPTURE__=true; window.__ENTRY__=${JSON.stringify(entry)};`);
  const files = [], qas = [];
  let warns = [];
  try {
    await pg.goto(`http://127.0.0.1:${port}/${scene}`);
    await pg.waitForFunction(() => window.READY === true || !!window.__SCENE_ERROR__, null, { timeout: 60000, polling: 50 });
    const e = await pg.evaluate(() => window.__SCENE_ERROR__);
    if (e) errs.push('scene error: ' + e);
    else {
      fs.mkdirSync(outdir, { recursive: true });
      for (const { t, label } of times) {
        await pg.evaluate((t) => window.seek(t), t);
        // runtime layout check (small text, clipped, subtitle band, overlaps): {t, issues, warnings}
        const qa = await pg.evaluate(async () => (typeof window.__QA__ === 'function' ? (await window.__QA__()).issues : []))
          .catch((x) => ['__QA__ failed: ' + x.message]);
        for (const q of Array.isArray(qa) ? qa : []) qas.push(`t=${t} ${typeof q === 'string' ? q : `${q.kind}${q.px ? ' ' + q.px + 'px' : ''}: ${q.text || (q.a + ' / ' + q.b)}`}`);
        const f = path.join(outdir, `${base}_${String(Math.round(t * 100)).padStart(5, '0')}_${label.replace(/[^\w.-]/g, '_')}.png`);
        await pg.screenshot({ path: f });
        files.push(f);
      }
      const late = await pg.evaluate(() => window.__SCENE_ERROR__);
      if (late) errs.push('scene error: ' + late);
      warns = await pg.evaluate(() => (window.__SCENE_WARNINGS__ || []).map(String));
    }
  } catch (x) { errs.push('load/seek failed: ' + String(x.message || x).split('\n')[0]); }
  await ctx.close();
  return { errors: [...new Set(errs)], files, warnings: [...new Set(warns)], qa: [...new Set(qas)] };
}

function contact(files, out) {
  if (!files.length) return null;
  const cols = Math.min(4, files.length), rows = Math.ceil(files.length / cols);
  const list = out + '.txt';
  fs.writeFileSync(list, files.map((f) => `file '${f}'`).join('\n'));
  execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', list, '-vf', `scale=480:-1,tile=${cols}x${rows}:padding=6:color=0x222222`, '-frames:v', '1', out]);
  fs.unlinkSync(list);
  return out;
}

(async () => {
  const srv = await serve();
  const port = srv.address().port;
  const browser = await chromium.launch({ args: FLAGS });
  let failed = false;
  if (opt.timeline) {
    const tl = JSON.parse(fs.readFileSync(opt.timeline, 'utf8'));
    const only = opt.only ? new Set(String(opt.only).split(',')) : null;
    const report = { timeline: path.relative(ROOT, opt.timeline), when: new Date().toISOString(), scenes: [] };
    for (const e of tl.scenes) {
      if (only && !only.has(e.id)) continue;
      const cues = Object.entries(e.entry.cues).filter(([k]) => !k.startsWith('s_') && !k.startsWith('_')).sort((a, b) => a[1] - b[1]);
      const all = Object.values(e.entry.cues).sort((a, b) => a - b);
      const times = [{ t: 0, label: 'start' }];
      for (const [name, c] of cues) {
        const next = all.find((x) => x > c + 1e-3);
        times.push({ t: +Math.min(c + 0.6, (next ?? e.duration) - 0.05, e.duration - 1 / tl.fps).toFixed(3), label: name });
      }
      times.push({ t: +(e.duration - 1 / tl.fps).toFixed(3), label: 'end' });
      const r = fs.existsSync(path.join(ROOT, e.file || '')) ? await shoot(browser, port, e.file, e.entry, times, opt.outdir, e.id)
        : { errors: [`scene file ${e.file} does not exist`], files: [], warnings: [], qa: [] };
      const sheet = contact(r.files, path.join(opt.outdir, `${e.id}_sheet.png`));
      if (r.errors.length) failed = true;
      report.scenes.push({ id: e.id, file: e.file, status: e.status, duration: e.duration, cues: Object.fromEntries(cues), stills: r.files.map((f) => path.relative(ROOT, f)),
        sheet: sheet && path.relative(ROOT, sheet), errors: r.errors, warnings: r.warnings, layout_qa: r.qa });
      console.log(`[check] ${e.id.padEnd(12)} ${r.files.length} stills ${r.errors.length ? 'ERRORS: ' + r.errors.slice(0, 4).join(' | ') : 'ok'}`
        + (r.warnings.length ? ` | ${r.warnings.length} scene warnings` : '') + (r.qa.length ? ` | ${r.qa.length} layout QA issues` : ''));
    }
    fs.mkdirSync(opt.outdir, { recursive: true });
    fs.writeFileSync(path.join(opt.outdir, 'report.json'), JSON.stringify(report, null, 1));
    console.log(`[check] ${report.scenes.length} scenes, ${report.scenes.filter((s) => s.errors.length).length} with errors; report ${path.relative(ROOT, path.join(opt.outdir, 'report.json'))}`);
  } else {
    const times = String(opt.times || '0').split(',').map((x) => ({ t: +x, label: 't' + (+x).toFixed(2) }));
    const r = await shoot(browser, port, opt.scene, readEntry(opt.entry), times, opt.outdir || 'out/stills', path.basename(opt.scene, '.html'));
    failed = r.errors.length > 0;
    console.log(JSON.stringify({ scene: opt.scene, stills: r.files.map((f) => path.relative(ROOT, f)), errors: r.errors, warnings: r.warnings, layout_qa: r.qa }));
  }
  await browser.close();
  srv.close();
  process.exit(failed ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(1); });
