#!/usr/bin/env node
/* capture.js: deterministic recorder. Opens a scene in headless Chromium, calls window.seek(t) for
 * every frame time t = (f0 + i) / fps, grabs the frame with CDP Page.captureScreenshot and pipes it
 * to ffmpeg (libx264). Nothing runs in real time, so the result does not depend on machine speed.
 *
 * Usage: NODE_PATH=/opt/node22/lib/node_modules node capture.js --scene scenes/a_fieldlines.html \
 *          --out out/a_30.mp4 [--fps 30] [--duration 6] [--workers 1] [--img png|jpeg] [--quality 92]
 *          [--scale 1] [--crf 18] [--preset medium] [--tune animation] [--gpu cpu|swgl|hw]
 *          [--ass subs/film.ass --ass-offset <scene start on the film clock, s>]
 *          [--entry '{"cues":{...},"status":"provisional"}'] [--metrics out/x.json] [--save-frames dir]
 *          [--frames N]  (limit for benchmarks)  [--isolate]  (one browser per worker)
 */
'use strict';
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path'), os = require('os');
const { spawn, execFileSync } = require('child_process');

const ROOT = __dirname;
const TMP = path.join(ROOT, '.tmp'); fs.mkdirSync(TMP, { recursive: true });
const argv = process.argv.slice(2), opt = {};
for (let i = 0; i < argv.length; i++) if (argv[i].startsWith('--')) { const k = argv[i].slice(2); const v = argv[i + 1]; if (v === undefined || v.startsWith('--')) opt[k] = true; else { opt[k] = v; i++; } }
const fps = +(opt.fps || 30), scale = +(opt.scale || 1), workers = +(opt.workers || 1);
const img = opt.img || 'png', quality = +(opt.quality || 92);
const crf = opt.crf || '18', preset = opt.preset || 'medium', tune = opt.tune === undefined ? 'animation' : opt.tune;
const entry = opt.entry ? JSON.parse(opt.entry.startsWith('{') ? opt.entry : fs.readFileSync(opt.entry, 'utf8')) : {};
const W = 1920, H = 1080;
// GPU modes (no GPU on this machine):
//  cpu   : 2D canvas, SVG and DOM rasterised by Skia on the CPU, compositing in software; WebGL still available through SwiftShader
//  swgl  : everything through SwiftShader (ANGLE). Needed only if a scene requires GPU-accelerated 2D canvas features (rare)
//  hw    : real GPU (a cloud GPU instance): ANGLE on the native driver
const gpu = opt.gpu || 'cpu';
const GPU_FLAGS = {
  cpu: ['--disable-gpu-compositing', '--disable-accelerated-2d-canvas', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
  swgl: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
  hw: ['--use-angle=default', '--ignore-gpu-blocklist', '--enable-gpu-rasterization'],
};

// ---------- tiny static server rooted at the prototype (fetch() of data files needs http, not file://) ----------
const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.otf': 'font/otf', '.png': 'image/png', '.svg': 'image/svg+xml', '.f32': 'application/octet-stream' };
function serve() {
  return new Promise((resolve) => {
    const srv = http.createServer((req, res) => {
      const p = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
      if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
      res.writeHead(200, { 'content-type': MIME[path.extname(p)] || 'application/octet-stream' });
      fs.createReadStream(p).pipe(res);
    });
    srv.listen(0, '127.0.0.1', () => resolve(srv));
  });
}

// ---------- CPU accounting ----------
const sysCpu = () => { const l = fs.readFileSync('/proc/stat', 'utf8').split('\n')[0].trim().split(/\s+/).slice(1).map(Number);
  const idle = l[3] + l[4]; return { idle, total: l.reduce((a, b) => a + b, 0) }; };
const HZ = 100;

function shiftAss(src, t0, t1, dst) {          // keep events overlapping [t0, t1) and shift them by -t0
  const toS = (s) => { const [h, m, x] = s.split(':'); return +h * 3600 + +m * 60 + +x; };
  const fmt = (x) => { x = Math.max(0, x); const h = Math.floor(x / 3600), m = Math.floor(x / 60) % 60, s = x - 3600 * h - 60 * m;
    return `${h}:${String(m).padStart(2, '0')}:${s.toFixed(2).padStart(5, '0')}`; };
  const out = fs.readFileSync(src, 'utf8').split('\n').map((l) => {
    const m = l.match(/^Dialogue: ([^,]*),([^,]*),([^,]*),(.*)$/); if (!m) return l;
    const a = toS(m[2]), b = toS(m[3]); if (b <= t0 || a >= t1) return null;
    return `Dialogue: ${m[1]},${fmt(a - t0)},${fmt(b - t0)},${m[4]}`;
  }).filter((l) => l !== null);
  fs.writeFileSync(dst, out.join('\n'));
}

function startFfmpeg(out, statFile, ass) {
  const vf = [`scale=out_color_matrix=bt709:out_range=tv:flags=bicubic`, 'format=yuv420p'];
  if (ass) vf.unshift(`ass=${ass}:fontsdir=${path.join(ROOT, 'vendor/fonts')}`);
  const args = ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', { png: 'png', jpeg: 'mjpeg', webp: 'webp' }[img], '-i', '-',
    '-vf', vf.join(','), '-c:v', 'libx264', '-preset', preset, '-crf', String(crf), ...(tune ? ['-tune', tune] : []),
    '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    '-g', String(fps * 2), '-movflags', '+faststart', out];
  // run ffmpeg under sh so that the shell's cutime/cstime (fields 16-17 of /proc/$$/stat) give ffmpeg's CPU time
  const p = spawn('sh', ['-c', 'ffmpeg "$@"; rc=$?; cat /proc/$$/stat > "' + statFile + '"; exit $rc', 'sh', ...args], { stdio: ['pipe', 'inherit', 'inherit'] });
  p.done = new Promise((res, rej) => p.on('exit', (c) => (c === 0 ? res() : rej(new Error('ffmpeg exit ' + c)))));
  return p;
}

async function runWorker(browser0, url, f0, f1, segOut, w, stats) {
  // --isolate: one browser per worker, hence one GPU/compositor process per worker (SwiftShader WebGL
  // and software compositing are serialised in the shared GPU process otherwise)
  const browser = opt.isolate ? await launch() : browser0;
  const context = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: scale });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.addInitScript(`window.__CAPTURE__ = true; window.__ENTRY__ = ${JSON.stringify(entry)};`);
  const tLoad = Date.now();
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForFunction(() => window.READY === true || !!window.__SCENE_ERROR__, null, { timeout: 120000, polling: 50 });
  const err = await page.evaluate(() => window.__SCENE_ERROR__);
  if (err) throw new Error('scene error: ' + err);
  stats.load_ms = Math.max(stats.load_ms || 0, Date.now() - tLoad);
  const cdp = await context.newCDPSession(page);
  const statFile = path.join(TMP, `ffstat_${process.pid}_${w}`);
  let ass = null;
  if (opt.ass) { const off = +(opt['ass-offset'] || 0); ass = path.join(TMP, `sub_${process.pid}_${w}.ass`); shiftAss(opt.ass, off + f0 / fps, off + f1 / fps, ass); }
  const ff = startFfmpeg(segOut, statFile, ass);
  // clip.scale is required: without it the headless shell returns CSS-pixel frames even when
  // deviceScaleFactor = 2 (checked: with it, frames are pixel-identical to Playwright's native 4K screenshot)
  const shotArgs = { format: img, captureBeyondViewport: false, fromSurface: true, optimizeForSpeed: !opt['no-fast'],
    clip: { x: 0, y: 0, width: W, height: H, scale } };
  if (img !== 'png') shotArgs.quality = quality;
  let tSeek = 0, tShot = 0, tWrite = 0, bytes = 0;
  for (let f = f0; f < f1; f++) {
    const a = process.hrtime.bigint();
    await page.evaluate((t) => window.seek(t), f / fps);
    const b = process.hrtime.bigint();
    const { data } = await cdp.send('Page.captureScreenshot', shotArgs);
    const buf = Buffer.from(data, 'base64');
    const c = process.hrtime.bigint();
    bytes += buf.length;
    if (f === f0 && img === 'png') stats.frame_px = [buf.readUInt32BE(16), buf.readUInt32BE(20)];   // measured, not assumed
    if (opt['save-frames']) fs.writeFileSync(path.join(opt['save-frames'], `f${String(f).padStart(6, '0')}.${{ png: 'png', jpeg: 'jpg', webp: 'webp' }[img]}`), buf);
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    const d = process.hrtime.bigint();
    tSeek += Number(b - a) / 1e6; tShot += Number(c - b) / 1e6; tWrite += Number(d - c) / 1e6;
  }
  ff.stdin.end();
  await ff.done;
  const st = fs.readFileSync(statFile, 'utf8').split(' ');
  stats.ffmpeg_cpu_s = (stats.ffmpeg_cpu_s || 0) + (+st[15] + +st[16]) / HZ;
  stats.seek_ms = (stats.seek_ms || 0) + tSeek; stats.shot_ms = (stats.shot_ms || 0) + tShot; stats.write_ms = (stats.write_ms || 0) + tWrite;
  stats.frame_bytes = (stats.frame_bytes || 0) + bytes;
  if (errors.length) stats.page_errors = (stats.page_errors || []).concat(errors.slice(0, 5));
  await context.close();
  if (opt.isolate) await browser.close();
}

const launch = () => chromium.launch({
  headless: true,
  args: [...GPU_FLAGS[gpu], '--force-color-profile=srgb', '--hide-scrollbars', '--disable-background-timer-throttling',
    '--disable-renderer-backgrounding', '--font-render-hinting=none'],
});

(async () => {
  const srv = await serve();
  const url = `http://127.0.0.1:${srv.address().port}/${opt.scene}`;
  const browser = await launch();
  // duration: entry > --duration > the scene's own default (read from a probe page)
  let duration = entry.duration ?? (opt.duration ? +opt.duration : null);
  if (duration == null) {
    const pg = await browser.newPage(); await pg.addInitScript('window.__CAPTURE__ = true;');
    await pg.goto(url); await pg.waitForFunction(() => window.READY === true || !!window.__SCENE_ERROR__, null, { timeout: 120000, polling: 50 });
    duration = await pg.evaluate(() => window.DURATION); await pg.close();
  }
  let nFrames = Math.round(duration * fps);
  if (opt.frames) nFrames = Math.min(nFrames, +opt.frames);
  if (opt['save-frames']) fs.mkdirSync(opt['save-frames'], { recursive: true });
  const out = path.resolve(opt.out);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  const per = Math.ceil(nFrames / workers), segs = [];
  const stats = {}, c0 = sysCpu(), n0 = process.cpuUsage(), t0 = Date.now();
  await Promise.all(Array.from({ length: workers }, (_, w) => {
    const f0 = w * per, f1 = Math.min(nFrames, f0 + per);
    const seg = workers === 1 ? out : out.replace(/\.mp4$/, `.part${w}.mp4`);
    if (f1 <= f0) return null;
    segs.push(seg);
    return runWorker(browser, url, f0, f1, seg, w, stats);
  }));
  if (workers > 1) {
    const list = out.replace(/\.mp4$/, '.concat.txt');
    fs.writeFileSync(list, segs.sort((a, b) => +a.match(/part(\d+)/)[1] - +b.match(/part(\d+)/)[1]).map((s) => `file '${s}'`).join('\n'));
    execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', '-movflags', '+faststart', out]);
    segs.forEach((s) => fs.unlinkSync(s)); fs.unlinkSync(list);
  }
  const wall = (Date.now() - t0) / 1000, c1 = sysCpu(), nu = process.cpuUsage(n0);
  await browser.close(); srv.close();
  const size = fs.statSync(out).size;
  const busy = 1 - (c1.idle - c0.idle) / (c1.total - c0.total);
  const m = {
    scene: opt.scene, out: path.relative(ROOT, out), width: (stats.frame_px || [W * scale])[0], height: (stats.frame_px || [0, H * scale])[1], fps, frames: nFrames, video_s: nFrames / fps,
    workers, isolate: !!opt.isolate, gpu, img, preset, crf: +crf, tune, wall_s: +wall.toFixed(2), capture_fps: +(nFrames / wall).toFixed(2),
    realtime_factor: +((nFrames / fps) / wall).toFixed(3),
    per_frame_ms: { seek_render: +(stats.seek_ms / nFrames).toFixed(1), screenshot: +(stats.shot_ms / nFrames).toFixed(1), pipe_write: +(stats.write_ms / nFrames).toFixed(1) },
    page_load_s: +(stats.load_ms / 1000).toFixed(2),
    cpu: { system_busy_pct: +(100 * busy).toFixed(1), cores_busy: +(busy * os.cpus().length).toFixed(2), ffmpeg_cpu_s: +stats.ffmpeg_cpu_s.toFixed(1),
      node_cpu_s: +((nu.user + nu.system) / 1e6).toFixed(1) },
    avg_frame_kb: +(stats.frame_bytes / nFrames / 1024).toFixed(0),
    size_mb: +(size / 1e6).toFixed(2), mb_per_min: +(size / 1e6 / (nFrames / fps) * 60).toFixed(1), kbps: Math.round(size * 8 / 1000 / (nFrames / fps)),
    page_errors: stats.page_errors || [],
  };
  if (opt.metrics) fs.writeFileSync(opt.metrics, JSON.stringify(m, null, 2));
  console.log(JSON.stringify(m));
})().catch((e) => { console.error(e); process.exit(1); });
