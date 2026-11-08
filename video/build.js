#!/usr/bin/env node
/* build.js: make-like orchestrator for one cut of the film (or one unit, for checks).
 *
 *  script/<unit>.json ─tools/assemble_cut.py─▶ script/_build/film_<name>.json (running order, variants, lint)
 *        │ audio/tts.py   one Fish request per paragraph, cached by (text, voice, settings)
 *        ▼ audio/align.py sentence times by silence detection; scene track = paragraphs + [long pause] + holds
 *  audio/scenes/<id>.wav + .align.json   (or audio/external/<id>.* with --narration external)
 *        ▼ timeline     duration = lead_in + audio (holds included) + tail, whole frames; cues = sentence starts
 *  script/_build/<name>_cues.json, subs/<name>.{ass,srt,vtt}  (subtitles from the SCRIPT text)
 *        ▼ capture.js   only scenes whose input hash changed (html, runtime, data, entry, subtitles, settings)
 *  out/scenes/<id>.mp4 (+ .events.json: sound events exported by the page)
 *        ▼ audio/mix.py narration + synthesized music bed + effects, -16 LUFS, true peak <= -1 dBTP, stems
 *  out/film_<name>.mp4  (stream-copy concat; audio 1 = full mix, audio 2 = no narration; chapters; burned-in subtitles,
 *                        sidecar subs/<name>.srt/.vtt for the platforms)
 *
 * Usage (normally through the Makefile):
 *   node build.js --cut core|extended [--draft] [--plan] [--only id,id] [--force] [--tts live|auto|placeholder]
 *                 [--narration tts|external] [--voice ID] [--variant auto|pending|result] [--workers 4] [--lang en|fr]
 *   node build.js --unit ch04 --check          one still per cue for every scene of a unit, page errors reported
 * --lang fr (BRIEF section 9): French narration over the same English visuals. The cut merges script/fr/<unit>.json
 *   (tools/assemble_cut.py --lang fr), the French voice, lexicon and Fish "language": "fr" (audio/tts.py), its own
 *   timeline and renders: name <cut>_fr (film_<cut>_fr.mp4, stems/<cut>_fr_*, subs/<cut>_fr.*, <cut>_fr_cues.json),
 *   scene renders in out/scenes_fr/ (French subtitles burned in), tracks in audio/scenes_fr/, external narration
 *   in audio/external_fr/. --lang en (default) is exactly the English build.
 *   options for tests: --units script/_test --cuts script/_test/cuts.json --name _test_core
 */
'use strict';
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const { execFileSync, spawnSync } = require('child_process');
const ROOT = __dirname;
process.env.NODE_PATH = process.env.NODE_PATH || '/opt/node22/lib/node_modules';   // playwright for capture.js / stills.js
const SITE = path.resolve(ROOT, '..');

const argv = process.argv.slice(2), opt = {};
for (let i = 0; i < argv.length; i++) if (argv[i].startsWith('--')) {
  const k = argv[i].slice(2), v = argv[i + 1];
  if (v === undefined || v.startsWith('--')) opt[k] = true; else { opt[k] = v; i++; }
}
if (!opt.cut && !opt.unit) { console.error('usage: node build.js --cut core|extended | --unit <unit> [--check] [--lang en|fr]'); process.exit(2); }
const LANG = String(opt.lang || 'en');
if (!['en', 'fr'].includes(LANG)) { console.error(`[build] --lang ${LANG}: en or fr`); process.exit(2); }
const LSFX = LANG === 'en' ? '' : '_' + LANG;                    // every output of a French build is suffixed _fr
const NAME0 = opt.name || (opt.unit ? `unit_${opt.unit}` : opt.cut);
const NAME = LSFX && !NAME0.endsWith(LSFX) ? NAME0 + LSFX : NAME0;
const DRAFT = !!opt.draft, PLAN = !!opt.plan, CHECK = !!opt.check;
const TTS = opt.tts || (PLAN ? 'dry-run' : (DRAFT || CHECK) ? 'auto' : 'live');
const RENDER = DRAFT
  ? { fps: 15, scale: 0.5, crf: 23, preset: 'veryfast', maxrate: '2M', bufsize: '4M', profile: 'high', level: '4.1', x264: 'stitchable=1', gpu: 'cpu', img: 'png' }
  : { fps: 30, scale: 1, crf: 21, preset: 'medium', maxrate: '6M', bufsize: '12M', profile: 'high', level: '4.1', x264: 'stitchable=1', gpu: 'cpu', img: 'png' };
const fps = RENDER.fps;
const WORKERS = +(opt.workers || (DRAFT ? 3 : 4));
const SIZE_LIMIT = 1.9e9;
const OUT = path.join(ROOT, DRAFT ? 'out/draft' : 'out');
const SCN = path.join(OUT, 'scenes' + LSFX);                   // one render per scene and language (subtitles burned in)
const ASCN = path.join(ROOT, 'audio', 'scenes' + LSFX);        // narration tracks (audio/align.py)
const AEXT = path.join(ROOT, 'audio', 'external' + LSFX);      // external narration (tools/fit_narration.py)
const BUILD = path.join(ROOT, 'script/_build');
const META = DRAFT ? OUT : BUILD;                      // draft timings (15 fps) never overwrite the official cue sheet
const SUBS = DRAFT ? path.join(OUT, 'subs') : path.join(ROOT, 'subs');
const sha = (x) => crypto.createHash('sha256').update(x).digest('hex');
const rel = (p) => path.relative(ROOT, p);
const log = (...a) => console.log('[build]', ...a);
const warnings = [];
const warn = (m) => { warnings.push(m); console.log('[build] warning:', m); };
const T = {};
const timed = (k, f) => { const t = Date.now(); const r = f(); T[k] = +((Date.now() - t) / 1000).toFixed(2); return r; };
const run = (cmd, args, o = {}) => { const r = spawnSync(cmd, args, { stdio: 'inherit', cwd: ROOT, ...o }); if (r.status !== 0) { console.error(`[build] ${path.basename(args[1] || args[0] || cmd)} failed`); process.exit(r.status || 1); } };
[OUT, SCN, BUILD, SUBS, path.join(ROOT, '.tmp')].forEach((d) => fs.mkdirSync(d, { recursive: true }));

// ---------------------------------------------------------------- 1. script: assemble the cut
const filmPath = path.join(BUILD, `film_${NAME}.json`);
timed('assemble_s', () => run('python3', ['-I', 'tools/assemble_cut.py', ...(opt.unit ? ['--unit', opt.unit] : ['--cut', opt.cut]), '--name', NAME,
  '--units', opt.units || 'script', '--cuts', opt.cuts || 'plan/outline.json', ...(opt.voice ? ['--voice', opt.voice] : []),
  ...(opt.variant ? ['--variant', opt.variant] : []), ...(opt.strict ? ['--strict'] : []), ...(LSFX ? ['--lang', LANG] : [])]));
const film = JSON.parse(fs.readFileSync(filmPath, 'utf8'));
if (!film.scenes.length) { log('no scene in this cut yet (no unit script found)'); process.exit(PLAN ? 0 : 1); }

// ---------------------------------------------------------------- 2. narration: TTS + alignment (both cached)
timed('tts_align_s', () => {
  run('python3', ['-I', 'audio/tts.py', filmPath, '--mode', TTS, '--quiet']);
  run('python3', ['-I', 'audio/align.py', filmPath, ...(TTS === 'dry-run' ? ['--allow-missing'] : [])]);
});

// ---------------------------------------------------------------- 3. timeline
const scriptText = (sc) => JSON.stringify(sc.paragraphs.map((p) => [p.hold_after, p.sentences.map((s) => [s.id, s.text])]));
const cueSheet = { name: NAME, cut: film.cut, lang: LANG, fps, voice: film.voice && film.voice.reference_id, scenes: [], sentences: [] };
let t = 0;
const scenes = film.scenes.map((sc) => {
  let alp = path.join(ASCN, sc.id + '.align.json'), narration = 'tts';
  if (opt.narration === 'external') {
    const ex = path.join(AEXT, sc.id + '.align.json');
    if (fs.existsSync(ex)) {
      const ej = JSON.parse(fs.readFileSync(ex, 'utf8'));
      if (JSON.stringify(ej.script_text) === scriptText(sc)) { alp = ex; narration = 'external'; }
      else warn(`${sc.id}: external narration is stale (script text changed since the fit): TTS used`);
    }
  }
  const al = JSON.parse(fs.readFileSync(alp, 'utf8'));
  const silent = !al.sentences.length;
  const frames = silent ? Math.round(Math.max(sc.lead_in + sc.tail, sc.target_s || 3) * fps) : Math.round((sc.lead_in + al.duration + sc.tail) * fps);
  const duration = frames / fps;
  const cues = {};
  const sents = [];
  for (const s of al.sentences) {
    const c = +(sc.lead_in + s.start).toFixed(3);
    cues['s_' + s.id] = c;
    if (s.cue) cues[s.cue] = c;
    sents.push({ id: s.id, cue: s.cue || null, start: c, end: +(sc.lead_in + s.end).toFixed(3) });
    cueSheet.sentences.push({ id: s.id, scene: sc.id, cue: s.cue || null, text: s.text, start: +(t + sc.lead_in + s.start).toFixed(3), end: +(t + sc.lead_in + s.end).toFixed(3) });
  }
  cues._speech_end = +(sc.lead_in + (al.sentences.length ? al.sentences[al.sentences.length - 1].end : 0)).toFixed(3);
  cues._tail = +(duration - sc.tail).toFixed(3);
  const entry = {
    id: sc.id, unit: sc.unit, duration, fps, cues, sentences: sents, status: sc.status,
    variant: sc.variant === 'main' ? (sc.status === 'pending' ? 'pending' : 'result') : sc.variant,   // runtime: pending | result
    stamp: sc.stamp || null, level: sc.level || null, register: sc.register || null,
    badge: sc.badge || null, question: sc.question || null, title: sc.title || null, onscreen: sc.onscreen || null, sources: sc.sources || [],
    data: (sc.entry && sc.entry.data) || {}, params: (sc.entry && sc.entry.params) || {}, seed: (sc.entry && sc.entry.seed) || 12345,
    ...(LSFX ? { lang: LANG } : {}),                          // narration language (visuals stay English); absent = en
  };
  const e = { id: sc.id, unit: sc.unit, file: sc.file, title: sc.title, status: sc.status, variant: sc.variant, level: sc.level, register: sc.register,
    start: +t.toFixed(4), duration, frames, lead_in: sc.lead_in, tail: sc.tail, target_s: sc.target_s || null,
    audio: { wav: al.wav, key: al.key, duration: al.duration, method: al.method, estimated: !!al.estimated, sources: al.sources, narration },
    deps: sc.deps || [], assets: sc.assets || [], entry, encode: sc.encode || null, music: sc.music === undefined ? null : sc.music,
    sfx_spec: [...(sc.sfx || []), ...(((sc.entry || {}).params || {}).sfx || [])], render: rel(path.join(SCN, sc.id + '.mp4')) };
  cueSheet.scenes.push({ id: sc.id, unit: sc.unit, start: e.start, duration, cues });
  t += duration;
  return e;
});
const total_s = +t.toFixed(4);
cueSheet.total_s = total_s;
const cuesPath = path.join(META, `${NAME}_cues.json`);
fs.writeFileSync(cuesPath, JSON.stringify(cueSheet, null, 1));
timed('subtitles_s', () => run('node', ['subs.js', cuesPath, path.join(SUBS, NAME)]));

// ---------------------------------------------------------------- 4. per-scene input hash
const fileHash = (p) => (fs.existsSync(p) && fs.statSync(p).isFile() ? sha(fs.readFileSync(p)) : 'MISSING');
const walk = (d, f = () => true) => (!fs.existsSync(d) ? [] : fs.readdirSync(d, { withFileTypes: true }).flatMap((x) => {
  const p = path.join(d, x.name); return x.isDirectory() ? walk(p, f) : (f(p) ? [p] : []); })).sort();
const runtimeHash = sha([...walk(path.join(ROOT, 'runtime')), ...walk(path.join(ROOT, 'scenes/_shared')),
  path.join(ROOT, 'capture.js'), path.join(ROOT, 'tools/server.js'), path.join(ROOT, 'package-lock.json')].map((p) => rel(p) + ':' + fileHash(p)).join()
  + walk(path.join(ROOT, 'vendor')).map((p) => rel(p) + ':' + fs.statSync(p).size).join());
const sceneAss = (e) => path.join(SUBS, NAME + '_scenes', e.id + '.ass');   // scene-time subtitles (subs.js)
const assetPath = (a) => { const s = String(a).replace(/^site\//, ''); const v = path.join(ROOT, s); return fs.existsSync(v) ? v : path.join(SITE, s); };
for (const e of scenes) {
  const html = path.join(ROOT, e.file || '');
  const sceneDir = path.dirname(html);
  const parts = {
    html: fileHash(html),
    // other files of the scene's own folder (scenes/<unit>/...), shared by the unit's pages
    files: (e.file && fs.existsSync(html) && rel(sceneDir).split(path.sep).length >= 2
      ? sha(walk(sceneDir, (p) => !p.endsWith('.html')).map((p) => rel(p) + ':' + fileHash(p)).join()) : 'none').slice(0, 16),
    runtime: runtimeHash.slice(0, 16),
    deps: sha(JSON.stringify(e.deps.map((d) => [d, fileHash(path.join(ROOT, d))]))).slice(0, 16),
    assets: sha(JSON.stringify(e.assets.map((a) => [a, fileHash(assetPath(a))]))).slice(0, 16),
    entry: sha(JSON.stringify(e.entry)).slice(0, 16),
    subtitles: fileHash(sceneAss(e)).slice(0, 16),
    render: sha(JSON.stringify([RENDER, e.encode])).slice(0, 16),
  };
  e.hash = sha(JSON.stringify(parts)).slice(0, 16);
  e.hash_parts = parts;
  if (!fs.existsSync(html)) warn(`${e.id}: scene file ${e.file} does not exist yet`);
  const hp = path.join(SCN, e.id + '.hash.json');
  const old = fs.existsSync(hp) ? JSON.parse(fs.readFileSync(hp, 'utf8')) : null;
  e.up_to_date = !opt.force && !!old && old.hash === e.hash && fs.existsSync(path.join(ROOT, e.render));
  e.why = !old || !fs.existsSync(path.join(ROOT, e.render)) ? ['new'] : Object.keys(parts).filter((k) => !old.parts || old.parts[k] !== parts[k]);
}
const only = opt.only ? new Set(String(opt.only).split(',')) : null;
const todo = scenes.filter((e) => (only ? only.has(e.id) && (opt.force || !e.up_to_date) : !e.up_to_date));
const tlPath = path.join(META, `${NAME}_timeline.json`);
const timeline = { name: NAME, cut: film.cut, lang: LANG, draft: DRAFT, fps, width: Math.round(1920 * RENDER.scale), height: Math.round(1080 * RENDER.scale),
  total_s, total_frames: scenes.reduce((a, e) => a + e.frames, 0), voice: film.voice, scenes };
fs.writeFileSync(tlPath, JSON.stringify(timeline, null, 1));
const fmt = (s) => `${Math.floor(s / 60)}:${String(Math.round(s % 60)).padStart(2, '0')}`;
log(`${NAME}${LSFX ? ` (${LANG} narration)` : ''}${DRAFT ? ' (draft 960x540, 15 fps)' : ''}: ${scenes.length} scenes, ${fmt(total_s)}; to render: ${todo.length}`);
if (LSFX && film.totals && film.totals.untranslated) warn(`${film.totals.untranslated} sentences are not translated into ${LANG} yet (English text kept; live TTS refuses them)`);

if (PLAN) {
  const est = scenes.filter((e) => e.audio.estimated).length;
  for (const e of scenes) {
    const tgt = e.target_s ? ` target ${e.target_s}s` : '';
    console.log(`  ${e.id.padEnd(12)} ${e.status.padEnd(11)} ${String(e.variant).padEnd(7)} ${e.duration.toFixed(1).padStart(6)} s${tgt.padEnd(12)} audio:${e.audio.estimated ? 'estimated' : e.audio.sources.join('+')}`
      + `  ${e.up_to_date ? 'up to date' : 'RENDER (' + e.why.join(', ') + ')'}`);
  }
  if (est) log(`${est} scenes have no narration audio yet: durations estimated at 146 raw wpm (they will change after TTS)`);
  log(`plan only: nothing rendered. timeline ${rel(tlPath)}, cues ${rel(cuesPath)}`);
  process.exit(0);
}

if (CHECK) {
  const outdir = path.join(ROOT, 'out/check', NAME);
  const r = spawnSync('node', ['stills.js', '--timeline', tlPath, '--outdir', outdir, ...(opt.only ? ['--only', opt.only] : [])], { stdio: 'inherit', cwd: ROOT, env: process.env });
  process.exit(r.status);
}

// ---------------------------------------------------------------- 5. render the scenes that changed
const renders = [], pageErrors = {};
for (const e of todo) {
  if (!fs.existsSync(path.join(ROOT, e.file || ''))) { console.error(`[build] ${e.id}: missing scene file ${e.file}`); process.exit(1); }
  const ef = path.join(ROOT, '.tmp', `entry_${NAME}_${e.id}.json`);
  fs.writeFileSync(ef, JSON.stringify(e.entry));
  const out = path.join(ROOT, e.render);
  const w = Math.max(1, Math.min(WORKERS, Math.ceil(e.frames / 45)));
  const enc = Object.assign({}, RENDER, DRAFT ? {} : (e.encode || {}));
  const t0 = Date.now();
  const r = spawnSync('node', ['capture.js', '--scene', e.file, '--out', out, '--fps', String(fps), '--workers', String(w), '--isolate',
    '--scale', String(RENDER.scale), '--entry', ef, '--ass', sceneAss(e), '--ass-offset', '0', '--metrics', out.replace(/\.mp4$/, '.metrics.json'),
    '--events-out', out.replace(/\.mp4$/, '.events.json'), '--crf', String(enc.crf), '--preset', enc.preset, '--maxrate', String(enc.maxrate),
    '--bufsize', String(enc.bufsize), '--level', String(enc.level), '--x264-params', enc.x264],
  { stdio: ['ignore', 'pipe', 'inherit'], cwd: ROOT, env: process.env });
  if (r.status !== 0) { console.error(`[build] scene ${e.id} FAILED`); process.exit(1); }
  const m = JSON.parse(fs.readFileSync(out.replace(/\.mp4$/, '.metrics.json'), 'utf8'));
  if (m.page_errors && m.page_errors.length) { pageErrors[e.id] = m.page_errors; warn(`${e.id}: page errors: ${m.page_errors.slice(0, 3).join(' | ')}`); }
  fs.writeFileSync(path.join(SCN, e.id + '.hash.json'), JSON.stringify({ hash: e.hash, parts: e.hash_parts }));
  renders.push({ id: e.id, frames: e.frames, wall_s: (Date.now() - t0) / 1000, mb: m.size_mb, kbps: m.kbps });
  log(`rendered ${e.id}: ${e.frames} frames in ${((Date.now() - t0) / 1000).toFixed(1)} s (${m.capture_fps} fps, ${m.kbps} kb/s)`);
}
if (opt['no-mix']) process.exit(0);
const missing = scenes.filter((e) => !fs.existsSync(path.join(ROOT, e.render)));
const stale = scenes.filter((e) => !e.up_to_date && !todo.includes(e) && fs.existsSync(path.join(ROOT, e.render)));
if (stale.length) warn(`assembled with stale renders (not in --only): ${stale.map((e) => e.id).join(', ')}`);
if (missing.length) { console.error(`[build] not rendered yet: ${missing.map((e) => e.id).join(', ')} (rerun without --only)`); process.exit(1); }

// ---------------------------------------------------------------- 6. sound effects: script events + events exported by the pages
const parseSfx = (spec, e) => {
  const out = [];
  for (const it of spec) {
    let o = typeof it === 'string' ? (() => { const m = it.match(/^([\w-]+)@([^+\-]+|-?[\d.]+)([+-][\d.]+)?$/); return m ? { id: m[1], at: m[2], offset: +(m[3] || 0) } : null; })() : Object.assign({}, it);
    if (!o) { warn(`${e.id}: bad sfx spec ${JSON.stringify(it)}`); continue; }
    let base = o.t;
    const ref = o.at !== undefined ? o.at : o.cue;
    if (base === undefined && ref !== undefined) {
      if (/^-?[\d.]+$/.test(String(ref))) base = +ref;
      else if (ref === 'start') base = 0;
      else if (ref === 'end') base = e.duration;
      else if (ref in e.entry.cues) base = e.entry.cues[ref];
      else { warn(`${e.id}: sfx cue '${ref}' not found`); continue; }
    }
    const tt = +base + +(o.offset || 0);
    if (!(tt >= 0)) { warn(`${e.id}: sfx ${o.id} at negative time`); continue; }
    out.push({ t: +tt.toFixed(3), id: o.id, ...(o.gain_db !== undefined ? { gain_db: +o.gain_db } : {}), ...(o.pan !== undefined ? { pan: +o.pan } : {}), ...(o.dur !== undefined ? { dur: +o.dur } : {}) });
  }
  return out;
};
for (const e of scenes) {
  const evf = path.join(ROOT, e.render).replace(/\.mp4$/, '.events.json');
  const page = fs.existsSync(evf) ? JSON.parse(fs.readFileSync(evf, 'utf8')) : [];
  e.sfx = [...parseSfx(e.sfx_spec, e), ...parseSfx(Array.isArray(page) ? page : [], e)].sort((a, b) => a.t - b.t);
}
fs.writeFileSync(tlPath, JSON.stringify(timeline, null, 1));

// ---------------------------------------------------------------- 7. sound: narration + music + effects, loudness, stems
timed('mix_s', () => run('python3', ['-I', 'audio/mix.py', tlPath, '--outdir', rel(OUT)]));
const stems = (k) => path.join(OUT, 'stems', `${NAME}_${k}.m4a`);

// ---------------------------------------------------------------- 8. assembly: stream copy + two audio tracks + soft subtitles + chapters
const filmOut = path.join(OUT, `film_${NAME}.mp4`);
const ISO = { en: 'eng', fr: 'fra' };                         // ISO 639-2 audio language of track 1
const TRACK = { en: ['Narration, music and effects', 'Music and effects (no narration)'],
  fr: ['Narration française, musique et effets', 'Musique et effets (sans narration)'] };
timed('assemble_mp4_s', () => {
  const list = path.join(ROOT, '.tmp', `concat_${NAME}${DRAFT ? '_draft' : ''}.txt`);
  fs.writeFileSync(list, scenes.map((e) => `file '${path.join(ROOT, e.render)}'`).join('\n'));
  const chapters = [];
  for (const e of scenes) if (!chapters.length || chapters[chapters.length - 1].unit !== e.unit) chapters.push({ unit: e.unit, start: e.start, title: (film.units.find((u) => u.unit === e.unit) || {}).title || e.unit });
  chapters.forEach((c, i) => { c.end = i + 1 < chapters.length ? chapters[i + 1].start : total_s; });
  const meta = path.join(ROOT, '.tmp', `chapters_${NAME}.txt`);
  const esc = (s) => String(s).replace(/([=;#\\\n])/g, '\\$1');
  const ftitle = (film.title || 'MilaDy 2027 film') + (LANG === 'fr' ? ' (narration française)' : '');
  fs.writeFileSync(meta, ';FFMETADATA1\n' + `title=${esc(ftitle)}\n` + (LSFX ? `language=${ISO[LANG]}\n` : '') + chapters.map((c) =>
    `[CHAPTER]\nTIMEBASE=1/1000\nSTART=${Math.round(c.start * 1000)}\nEND=${Math.round(c.end * 1000)}\ntitle=${esc(c.title)}\n`).join(''));
  fs.writeFileSync(path.join(OUT, `film_${NAME}_chapters.txt`), chapters.map((c) => `${fmt(c.start)} ${c.title}`).join('\n') + '\n');
  const tmp = filmOut.replace(/\.mp4$/, '.part.mp4');
  execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', list, '-i', stems('full'), '-i', stems('nonarration'),
    '-i', meta, '-map', '0:v', '-map', '1:a', '-map', '2:a', '-map_metadata', '3', '-map_chapters', '3',
    '-c:v', 'copy', '-c:a', 'copy',
    '-metadata:s:a:0', `title=${TRACK[LANG][0]}`, '-metadata:s:a:0', `language=${ISO[LANG]}`, '-disposition:a:0', 'default',
    '-metadata:s:a:1', `title=${TRACK[LANG][1]}`, '-metadata:s:a:1', 'language=zxx', '-disposition:a:1', '0',
    '-movflags', '+faststart', tmp]);
  fs.renameSync(tmp, filmOut);
});

// ---------------------------------------------------------------- 9. checks and report
const probe = JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration,size:stream=index,codec_type,codec_name,width,height,duration,nb_frames,r_frame_rate', '-of', 'json', filmOut]));
const size = +probe.format.size;
const vdur = +(probe.streams.find((s) => s.codec_type === 'video').duration || probe.format.duration);
if (Math.abs(vdur - total_s) > 1.5 / fps) warn(`video lasts ${vdur} s, timeline ${total_s} s`);
if (size > SIZE_LIMIT) {
  const heavy = scenes.map((e) => ({ id: e.id, mb: fs.statSync(path.join(ROOT, e.render)).size / 1e6, s: e.duration })).sort((a, b) => b.mb - a.mb).slice(0, 8);
  warn(`film is ${(size / 1e9).toFixed(2)} GB > 1.9 GB: give the heaviest scenes "encode": {"maxrate": "4M"} (or crf 23): ${heavy.map((h) => `${h.id} ${h.mb.toFixed(0)} MB`).join(', ')}`);
}
const mixRep = JSON.parse(fs.readFileSync(path.join(OUT, 'stems', `${NAME}_mix.json`), 'utf8'));
const report = { when: new Date().toISOString(), name: NAME, draft: DRAFT, film: rel(filmOut), size_gb: +(size / 1e9).toFixed(3), duration_s: total_s,
  scenes: scenes.length, rendered: renders, skipped: scenes.filter((e) => !todo.includes(e)).map((e) => e.id), page_errors: pageErrors,
  loudness: mixRep.full_mix_aac, steps_s: T, warnings, probe };
fs.writeFileSync(path.join(OUT, `${NAME}_build_report.json`), JSON.stringify(report, null, 1));
log(`done: ${rel(filmOut)} ${(size / 1e6).toFixed(1)} MB, ${fmt(total_s)}, rendered ${renders.length}/${scenes.length}, loudness ${mixRep.full_mix_aac.I} LUFS / ${mixRep.full_mix_aac.TP} dBTP`
  + (Object.keys(pageErrors).length ? `, PAGE ERRORS in ${Object.keys(pageErrors).join(', ')}` : ''));
if (opt.strict && (Object.keys(pageErrors).length || warnings.length)) process.exit(3);
