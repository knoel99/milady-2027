#!/usr/bin/env node
/* build.js: make-like orchestrator for the film.
 *
 *   script/*.json ──tts.py──▶ audio/chunks/<scene>.wav ──align.py──▶ <scene>.align.json
 *         │                                                         │
 *         └──────────────── timeline.json (durations from audio, cues from sentences, status, deps)
 *                                   │
 *            subs/film.ass ◀────────┤ (script text, sentence timings)
 *                                   ▼
 *      out/scenes/<id>.mp4  ◀── capture.js (only when the scene's input hash changed)
 *                                   ▼
 *      concat of out/scenes/*.mp4 (stream copy) + out/narration.m4a (loudnorm, optional music) ─▶ out/film.mp4 (one pass)
 *
 * A scene's hash covers: its HTML, the runtime, vendored library versions, every data file it
 * depends on, its timeline entry (duration, cues, status, params), its subtitle events and the
 * render settings. New simulation results => new data/*.json hash => only those scenes re-render.
 * A "pending" scene whose data files now exist is promoted to "provisional" automatically.
 *
 * Usage: NODE_PATH=/opt/node22/lib/node_modules node build.js script/demo_script.json
 *          [--fps 30] [--workers 4] [--scale 1] [--only id,id] [--force] [--dry] [--music file|synth]
 *          [--plan]  (print what would be rebuilt and exit)
 */
'use strict';
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const { execFileSync, spawnSync } = require('child_process');
const ROOT = __dirname;
const argv = process.argv.slice(2), opt = { _: [] };
for (let i = 0; i < argv.length; i++) { if (argv[i].startsWith('--')) { const k = argv[i].slice(2), v = argv[i + 1];
  if (v === undefined || v.startsWith('--')) opt[k] = true; else { opt[k] = v; i++; } } else opt._.push(argv[i]); }
const scriptPath = opt._[0] || 'script/demo_script.json';
const script = JSON.parse(fs.readFileSync(path.join(ROOT, scriptPath), 'utf8'));
const fps = +(opt.fps || script.fps || 30), workers = +(opt.workers || 4), scale = +(opt.scale || 1);   // 4 isolated workers: best measured
const RENDER = { fps, scale, crf: 18, preset: 'medium', tune: 'animation', gpu: 'cpu', img: 'png' };
const sha = (x) => crypto.createHash('sha256').update(x).digest('hex');
const fileHash = (p) => (fs.existsSync(path.join(ROOT, p)) ? sha(fs.readFileSync(path.join(ROOT, p))) : 'MISSING');
const log = (...a) => console.log('[build]', ...a);
const T = {};
const timed = (k, f) => { const t = Date.now(); const r = f(); T[k] = +((Date.now() - t) / 1000).toFixed(2); return r; };

// 1. narration: TTS (or placeholder) + sentence alignment, both cached by content hash
timed('audio_tts_align_s', () => {
  execFileSync('python3', ['-I', path.join(ROOT, 'audio/tts.py'), path.join(ROOT, scriptPath)], { stdio: 'inherit' });
  execFileSync('python3', ['-I', path.join(ROOT, 'audio/align.py'), path.join(ROOT, scriptPath)], { stdio: 'inherit' });
});

// 2. timeline: durations derived from audio, quantised to whole frames
let t = 0;
const subs = { sentences: [] };
const scenes = script.scenes.map((sc) => {
  const al = JSON.parse(fs.readFileSync(path.join(ROOT, 'audio/chunks', sc.id + '.align.json'), 'utf8'));
  const frames = Math.round((sc.lead_in + al.duration + sc.tail) * fps), duration = frames / fps;
  const cues = {};
  for (const s of al.sentences) {
    cues['s_' + s.id] = +(sc.lead_in + s.start).toFixed(3);
    if (s.cue) cues[s.cue] = +(sc.lead_in + s.start).toFixed(3);
    subs.sentences.push({ id: s.id, text: s.text, start: +(t + sc.lead_in + s.start).toFixed(3), end: +(t + sc.lead_in + s.end).toFixed(3) });
  }
  const depsOk = (sc.deps || []).every((d) => fs.existsSync(path.join(ROOT, d)));
  let status = sc.status;
  if (status === 'pending' && sc.deps && sc.deps.length && depsOk) status = 'provisional';   // data arrived
  if (status !== 'pending' && !depsOk) status = 'pending';                                   // data vanished
  const entry = Object.assign({}, sc.entry || {}, { duration, cues, status, seed: 12345 });
  const e = { id: sc.id, file: sc.file, status, start: +t.toFixed(4), duration, frames, lead_in: sc.lead_in,
    audio: 'audio/chunks/' + sc.id + '.wav', audio_duration: al.duration, align_method: al.method, deps: sc.deps || [], entry, encode: sc.encode || null,
    render: `out/scenes/${sc.id}.mp4` };
  t += duration;
  return e;
});
fs.writeFileSync(path.join(ROOT, 'subs/cues.json'), JSON.stringify(subs, null, 1));
timed('subtitles_s', () => execFileSync('node', [path.join(ROOT, 'subs.js'), path.join(ROOT, 'subs/cues.json'), path.join(ROOT, 'subs/film')], { stdio: 'inherit' }));

// 3. per-scene input hash
const runtimeHash = sha(['runtime/scene.js', 'runtime/theme.css', 'package-lock.json', 'capture.js'].map(fileHash).join());
const assLines = fs.readFileSync(path.join(ROOT, 'subs/film.ass'), 'utf8').split('\n');
const toS = (s) => { const [h, m, x] = s.split(':'); return +h * 3600 + +m * 60 + +x; };
for (const e of scenes) {
  const ev = assLines.filter((l) => { const m = l.match(/^Dialogue: [^,]*,([^,]*),([^,]*),/); return m && toS(m[2]) > e.start && toS(m[1]) < e.start + e.duration; })
    .map((l) => l.replace(/^Dialogue: [^,]*,([^,]*),([^,]*),/, (_, a, b) => `${(toS(a) - e.start).toFixed(2)},${(toS(b) - e.start).toFixed(2)},`));
  e.hash = sha(JSON.stringify({ html: fileHash(e.file), runtimeHash, deps: e.deps.map((d) => [d, fileHash(d)]), entry: e.entry, ev, RENDER, encode: e.encode })).slice(0, 16);
  const hp = path.join(ROOT, 'out/scenes', e.id + '.hash');
  e.up_to_date = !opt.force && fs.existsSync(path.join(ROOT, e.render)) && fs.existsSync(hp) && fs.readFileSync(hp, 'utf8') === e.hash;
}
const timeline = { fps, width: 1920 * scale, height: 1080 * scale, total_s: +t.toFixed(3), total_frames: scenes.reduce((a, e) => a + e.frames, 0), scenes };
fs.writeFileSync(path.join(ROOT, 'timeline.json'), JSON.stringify(timeline, null, 1));
const only = opt.only ? new Set(String(opt.only).split(',')) : null;
const todo = scenes.filter((e) => !e.up_to_date && (!only || only.has(e.id)));
log(`timeline: ${scenes.length} scenes, ${timeline.total_s.toFixed(1)} s; to render: ${todo.map((e) => `${e.id}(${e.status})`).join(', ') || 'none'}`);
if (opt.plan) process.exit(0);

// 4. render changed scenes
fs.mkdirSync(path.join(ROOT, 'out/scenes'), { recursive: true });
const renders = [];
for (const e of todo) {
  const ef = path.join(ROOT, '.tmp', `entry_${e.id}.json`);
  fs.mkdirSync(path.dirname(ef), { recursive: true });
  fs.writeFileSync(ef, JSON.stringify(e.entry));
  const t0 = Date.now();
  const r = spawnSync('node', [path.join(ROOT, 'capture.js'), '--scene', e.file, '--out', path.join(ROOT, e.render), '--fps', String(fps),
    '--workers', String(workers), '--isolate', '--scale', String(scale), '--entry', ef, '--ass', path.join(ROOT, 'subs/film.ass'), '--ass-offset', String(e.start),
    '--metrics', path.join(ROOT, 'out/scenes', e.id + '.metrics.json'),
    ...(e.encode ? ['--crf', String(e.encode.crf ?? RENDER.crf), '--preset', e.encode.preset ?? RENDER.preset] : [])],
    { stdio: ['ignore', 'pipe', 'inherit'], env: process.env });
  if (r.status !== 0) { console.error(`[build] scene ${e.id} FAILED`); process.exit(1); }
  fs.writeFileSync(path.join(ROOT, 'out/scenes', e.id + '.hash'), e.hash);
  renders.push({ id: e.id, frames: e.frames, wall_s: (Date.now() - t0) / 1000 });
  log(`rendered ${e.id}: ${e.frames} frames in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
}
if (opt.dry) process.exit(0);

// 5. narration track: lead-in + chunk + pad to the frame-exact scene length, concatenated, then EBU R128
timed('audio_mix_s', () => {
  const ff = (args) => execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', ...args]);
  const ins = [], fl = [];
  scenes.forEach((e, i) => {
    ins.push('-i', path.join(ROOT, e.audio));
    const d = Math.round(e.lead_in * 1000);
    fl.push(`[${i}:a]aresample=48000,adelay=${d}:all=1,apad=whole_dur=${e.duration.toFixed(6)},atrim=0:${e.duration.toFixed(6)}[a${i}]`);
  });
  fl.push(scenes.map((_, i) => `[a${i}]`).join('') + `concat=n=${scenes.length}:v=0:a=1[out]`);
  const raw = path.join(ROOT, '.tmp/narration_raw.wav');
  ff([...ins, '-filter_complex', fl.join(';'), '-map', '[out]', '-ac', '1', raw]);
  // two-pass loudnorm: measure, then apply with measured values (linear mode keeps dynamics)
  const target = 'I=-16:TP=-1.5:LRA=11';
  const m = spawnSync('ffmpeg', ['-hide_banner', '-i', raw, '-af', `loudnorm=${target}:print_format=json`, '-f', 'null', '-'], { encoding: 'utf8' }).stderr;
  const meas = JSON.parse(m.slice(m.lastIndexOf('{'), m.lastIndexOf('}') + 1));
  const ln = `loudnorm=${target}:measured_I=${meas.input_i}:measured_TP=${meas.input_tp}:measured_LRA=${meas.input_lra}:measured_thresh=${meas.input_thresh}:offset=${meas.target_offset}:linear=true`;
  const voice = path.join(ROOT, '.tmp/narration_norm.wav');
  ff(['-i', raw, '-af', ln + ',aresample=48000', '-ac', '1', voice]);
  let mixIn = voice;
  if (opt.music) {
    // music bed ducked under the voice (sidechain), about 20 dB below the narration
    const mus = opt.music === 'synth' ? null : path.resolve(opt.music);
    const musArgs = mus ? ['-stream_loop', '-1', '-i', mus] : ['-f', 'lavfi', '-i', `aevalsrc=0.05*sin(2*PI*110*t)*(0.6+0.4*sin(2*PI*0.1*t))+0.04*sin(2*PI*164.8*t)+0.03*sin(2*PI*220*t):s=48000:d=${timeline.total_s}`];
    const mixed = path.join(ROOT, '.tmp/narration_music.wav');
    ff(['-i', voice, ...musArgs, '-filter_complex',
      `[1:a]aformat=channel_layouts=mono,volume=-20dB,atrim=0:${timeline.total_s}[m];[0:a]asplit=2[v][sc];[m][sc]sidechaincompress=threshold=0.02:ratio=6:attack=30:release=500[duck];[v][duck]amix=inputs=2:normalize=0:duration=first,loudnorm=${target}`,
      '-ar', '48000', '-ac', '1', mixed]);
    mixIn = mixed;
  }
  ff(['-i', mixIn, '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', path.join(ROOT, 'out/narration.m4a')]);
  const chk = spawnSync('ffmpeg', ['-hide_banner', '-i', path.join(ROOT, 'out/narration.m4a'), '-af', 'ebur128=peak=true', '-f', 'null', '-'], { encoding: 'utf8' }).stderr;
  const I = chk.match(/I:\s+(-?[\d.]+) LUFS/g), P = chk.match(/Peak:\s+(-?[\d.]+) dBFS/g);
  T.loudness = { integrated: I && I[I.length - 1], true_peak: P && P[P.length - 1], first_pass: { I: meas.input_i, TP: meas.input_tp } };
});

// 6. assembly: stream-copy concat of scene files (identical encoder settings), mux audio
timed('assemble_s', () => {
  const list = path.join(ROOT, '.tmp/film_concat.txt');
  fs.writeFileSync(list, scenes.map((e) => `file '${path.join(ROOT, e.render)}'`).join('\n'));
  // one pass, no intermediate file: concat demuxer for the video + the narration track, both stream-copied
  execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', list, '-i', path.join(ROOT, 'out/narration.m4a'),
    '-map', '0:v', '-map', '1:a', '-c', 'copy', '-movflags', '+faststart', path.join(ROOT, 'out/film.mp4')]);
});
const probe = JSON.parse(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration,size:stream=codec_type,duration,nb_frames', '-of', 'json', path.join(ROOT, 'out/film.mp4')]));
const report = { when: new Date().toISOString(), timeline_s: timeline.total_s, rendered: renders, skipped: scenes.filter((e) => !todo.includes(e)).map((e) => e.id), steps_s: T, film: probe };
fs.writeFileSync(path.join(ROOT, 'out/build_report.json'), JSON.stringify(report, null, 1));
log('done:', JSON.stringify({ rendered: renders.map((r) => r.id), skipped: report.skipped, steps_s: T, duration: probe.format.duration }));
