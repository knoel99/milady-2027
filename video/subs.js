#!/usr/bin/env node
/* subs.js: subtitles from the SCRIPT text (never from a transcription), timed by the sentence alignment.
 *
 * Input : the cue sheet written by build.js (script/_build/<name>_cues.json):
 *           {"scenes":[{"id","start","duration"}], "sentences":[{"id","scene","text","start","end"}]}  (film clock)
 *         Key terms may be marked {u}velocity{/}, {b}magnetic field{/}, {param}…{/}, {model}…{/}, {metric}…{/}.
 * Output: <base>.ass, <base>.srt, <base>.vtt for the whole cut (upload .srt/.vtt as captions), and
 *         <base>_scenes/<scene>.ass in scene time, burned into each scene by capture.js.
 * Cues are computed scene by scene in scene time and never cross a scene boundary, so a scene's burned-in
 * subtitles do not depend on its neighbours or on the cut it is in (one render serves both cuts).
 * Rules (styles.md 3.9): ≤ 2 lines of ≤ 42 characters, 1.2–6 s per cue, ≤ 17 characters/s when possible,
 *         cue = first word − 80 ms … last word + 250 ms, min gap 80 ms, 120 ms fade in, 100 ms fade out.
 * French (cue sheet "lang": "fr", BRIEF section 9): the same rules on the French script text; a space before
 *         ? ! : ; » and after « becomes a no-break space, so a line never starts with that punctuation.
 *         Words are split on ordinary spaces only: a no-break space always glues its two words.
 * Usage : node subs.js cues.json subs/<name> [--style box|outline] [--size 42]
 */
'use strict';
const fs = require('fs'), path = require('path');
const [inp, base] = process.argv.slice(2, 4);
const style = process.argv.includes('--style') ? process.argv[process.argv.indexOf('--style') + 1] : 'box';
const size = process.argv.includes('--size') ? +process.argv[process.argv.indexOf('--size') + 1] : 42;
const MAXL = 42, LEAD = 0.08, TAIL = 0.25, GAP = 0.08, MAXDUR = 6, MINDUR = 1.2, EDGE = 0.04;
const KEY = { u: '3987E5', b: 'EB6834', param: '1BAF7A', model: 'B49CF0', metric: 'EDA100' };   // RRGGBB
const bgr = (hex) => '&H' + hex.slice(4, 6) + hex.slice(2, 4) + hex.slice(0, 2) + '&';

const plain = (s) => s.replace(/\{(u|b|param|model|metric)\}(.*?)\{\/\}/g, '$2');
/** split a sentence into n balanced cue texts of at most 2 lines x MAXL chars, preferring punctuation breaks */
function chunks(text) {
  const words = text.split(/[ \t\r\n]+/).filter(Boolean), L = plain(text).length;
  if (wrap(text, true)) return [text];
  const ends = [], depth = []; let c = 0, d = 0;
  words.forEach((w, i) => { c += plain(w).length + (i ? 1 : 0); ends.push(c);
    d += (w.match(/\{(u|b|param|model|metric)\}/g) || []).length - (w.match(/\{\/\}/g) || []).length; depth.push(d); });
  for (let n = Math.max(2, Math.ceil(L / (2 * MAXL - 6))); n <= words.length; n++) {
    const cuts = []; let start = 0;
    for (let k = 1; k < n; k++) {
      const ideal = L * k / n; let best = start, bs = Infinity;
      for (let i = start; i < words.length - 1; i++) {
        if (depth[i] > 0) continue;                 // never cut inside a marked term
        const sc = Math.abs(ends[i] - ideal) - (/[,;:]$/.test(plain(words[i])) ? 14 : 0);
        if (sc < bs) { bs = sc; best = i; }
      }
      cuts.push(best); start = best + 1;
    }
    const out = []; let s0 = 0;
    for (const ci of cuts) { out.push(words.slice(s0, ci + 1).join(' ')); s0 = ci + 1; }
    out.push(words.slice(s0).join(' '));
    if (out.every((x) => x && wrap(x, true))) return out;
  }
  return [text];
}
/** balanced two-line break (markup never split: a marked term is one token only if it has no space) */
function wrap(text, strict = false) {
  const p = plain(text);
  if (p.length <= MAXL) return [text];
  const words = text.split(' ');
  let best = null;
  for (let i = 1; i < words.length; i++) {
    const a = words.slice(0, i).join(' '), b = words.slice(i).join(' ');
    if ((a.match(/\{(u|b|param|model|metric)\}/g) || []).length !== (a.match(/\{\/\}/g) || []).length) continue;
    if (plain(a).length > MAXL || plain(b).length > MAXL) continue;
    const score = Math.abs(plain(a).length - plain(b).length) - (/[,;:.]$/.test(plain(a)) ? 8 : 0);
    if (!best || score < best.s) best = { s: score, i };
  }
  if (!best) { if (strict) return null; best = { i: Math.ceil(words.length / 2) }; }
  return [words.slice(0, best.i).join(' '), words.slice(best.i).join(' ')];
}
const toAss = (t) => { t = Math.max(0, t); const cs = Math.round(t * 100), h = Math.floor(cs / 360000), m = Math.floor(cs / 6000) % 60, s = (cs % 6000) / 100;
  return `${h}:${String(m).padStart(2, '0')}:${s.toFixed(2).padStart(5, '0')}`; };
const toSrt = (t, sep) => { const ms = Math.round(Math.max(0, t) * 1000), h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, s = Math.floor(ms / 1000) % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}${sep}${String(ms % 1000).padStart(3, '0')}`; };

/** cues of one scene, in scene time */
function sceneCues(sents, duration) {
  const cues = [];
  for (const s of sents) {
    const parts = chunks(s.text), total = parts.reduce((a, p) => a + plain(p).length, 0);
    let t = s.start;
    for (const p of parts) {   // inside a sentence, time is shared in proportion to characters
      const d = (s.end - s.start) * plain(p).length / total;
      cues.push({ text: p, start: t - LEAD, end: t + d + TAIL, sid: s.id });
      t += d;
    }
  }
  for (let i = 0; i < cues.length; i++) {
    const c = cues[i], n = cues[i + 1];
    c.start = Math.max(0, c.start);
    if (c.end - c.start < MINDUR) c.end = c.start + MINDUR;
    if (c.end - c.start > MAXDUR) c.end = c.start + MAXDUR;
    if (n && c.end > n.start - GAP) c.end = Math.max(c.start + 0.5, n.start - GAP);
    c.end = Math.min(c.end, duration - EDGE);
    c.cps = plain(c.text).length / Math.max(0.1, c.end - c.start);
  }
  return cues.filter((c) => c.end > c.start + 0.1);
}

// key-term colouring: at most one coloured term per cue (the first marked one)
const assText = (t) => {
  let used = false;
  return wrap(t).join('\\N').replace(/\{(u|b|param|model|metric)\}(.*?)\{\/\}/g, (_, k, w) => {
    if (used) return w; used = true; return `{\\c${bgr(KEY[k])}}${w}{\\c&HF7F4F2&}`; });
};
const STYLES = {
  // BorderStyle 3 = opaque box drawn with OutlineColour; Outline = box padding. rgba(11,15,20,.78) -> &H38140F0B
  box: `Style: Sub,Inter Medium,${size},&H00F7F4F2,&H00F7F4F2,&H38140F0B,&H00000000,0,0,0,0,100,100,0,0,3,12,0,2,240,240,64,1`,
  // BorderStyle 1 = outline + soft shadow, no box
  outline: `Style: Sub,Inter Medium,${size},&H00F7F4F2,&H00F7F4F2,&H00140F0B,&H80000000,0,0,0,0,100,100,0,0,1,3.2,1.5,2,240,240,64,1`,
};
const assDoc = (cues) => [
  '[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1920', 'PlayResY: 1080', 'WrapStyle: 2', 'ScaledBorderAndShadow: yes', 'YCbCr Matrix: TV.709', '',
  '[V4+ Styles]',
  'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
  STYLES[style], '',
  '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
  ...cues.map((c) => `Dialogue: 0,${toAss(c.start)},${toAss(c.end)},Sub,,0,0,0,,{\\fad(120,100)\\move(960,1020,960,1016,0,120)}${assText(c.text)}`),
].join('\n') + '\n';

const sheet = JSON.parse(fs.readFileSync(inp, 'utf8'));
const NBSP = '\u00a0';
if (sheet.lang === 'fr') for (const s of sheet.sentences) s.text = s.text.replace(/[ \t]+([?!:;»])/g, NBSP + '$1').replace(/«[ \t]+/g, '«' + NBSP);
const scenes = sheet.scenes || [{ id: '_all', start: 0, duration: Infinity }];
const dir = base + '_scenes';
fs.mkdirSync(dir, { recursive: true });
const all = [];
for (const sc of scenes) {
  const sents = sheet.sentences.filter((s) => (s.scene || '_all') === sc.id).map((s) => ({ ...s, start: s.start - sc.start, end: s.end - sc.start }));
  const local = sceneCues(sents, sc.duration);
  fs.writeFileSync(path.join(dir, sc.id + '.ass'), assDoc(local));
  for (const c of local) all.push({ ...c, start: c.start + sc.start, end: c.end + sc.start });
}
fs.writeFileSync(base + '.ass', assDoc(all));
fs.writeFileSync(base + '.srt', all.map((c, i) => `${i + 1}\n${toSrt(c.start, ',')} --> ${toSrt(c.end, ',')}\n${wrap(plain(c.text)).join('\n')}\n`).join('\n'));
fs.writeFileSync(base + '.vtt', 'WEBVTT\n\n' + all.map((c) => `${toSrt(c.start, '.')} --> ${toSrt(c.end, '.')}\n${wrap(plain(c.text)).join('\n')}\n`).join('\n'));
const fast = all.filter((c) => c.cps > 17);
console.log(JSON.stringify({ cues: all.length, max_cps: all.length ? +Math.max(...all.map((c) => c.cps)).toFixed(1) : 0, over_17cps: fast.length,
  over_17cps_ids: [...new Set(fast.map((c) => c.sid))].slice(0, 20) }));
