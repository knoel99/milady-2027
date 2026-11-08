#!/usr/bin/env node
/* subs.js: burned-in subtitles from the SCRIPT text (not from a transcription).
 * Input : a cue sheet JSON  {"sentences":[{"id":"s1","text":"...","start":1.23,"end":4.56}, ...]}
 *         (times on the film's global clock, produced by audio/align.py from the TTS audio)
 *         Key terms can be marked in the script as {u}velocity{/}, {b}magnetic field{/}, {param}…, {model}…, {metric}…
 * Output: an .ass file (burn with ffmpeg -vf ass=...) plus .srt and .vtt twins for platform captions.
 * Rules (styles.md 3.9): ≤ 2 lines of ≤ 42 characters, 1.2–6 s per cue, ≤ 17 characters/s when possible,
 *         cue = first word − 80 ms … last word + 250 ms, min gap 80 ms, 120 ms fade in, 100 ms fade out.
 * Usage : node subs.js cues.json out/base [--style box|outline] [--size 42]
 */
'use strict';
const fs = require('fs');
const [inp, base] = process.argv.slice(2, 4);
const style = process.argv.includes('--style') ? process.argv[process.argv.indexOf('--style') + 1] : 'box';
const size = process.argv.includes('--size') ? +process.argv[process.argv.indexOf('--size') + 1] : 42;
const MAXL = 42, LEAD = 0.08, TAIL = 0.25, GAP = 0.08, MAXDUR = 6, MINDUR = 1.2;
const KEY = { u: '3987E5', b: 'EB6834', param: '1BAF7A', model: 'B49CF0', metric: 'EDA100' };   // RRGGBB
const bgr = (hex) => '&H' + hex.slice(4, 6) + hex.slice(2, 4) + hex.slice(0, 2) + '&';

const plain = (s) => s.replace(/\{(u|b|param|model|metric)\}(.*?)\{\/\}/g, '$2');
/** split a sentence into n balanced cue texts of at most 2 lines x MAXL chars, preferring punctuation breaks */
function chunks(text) {
  const words = text.split(/\s+/).filter(Boolean), L = plain(text).length;
  if (wrap(text, true)) return [text];
  const ends = []; let c = 0;
  words.forEach((w, i) => { c += plain(w).length + (i ? 1 : 0); ends.push(c); });
  for (let n = Math.max(2, Math.ceil(L / (2 * MAXL - 6))); n <= words.length; n++) {
    const cuts = []; let start = 0;
    for (let k = 1; k < n; k++) {
      const ideal = L * k / n; let best = start, bs = Infinity;
      for (let i = start; i < words.length - 1; i++) {
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
/** balanced two-line break */
function wrap(text, strict = false) {
  const p = plain(text);
  if (p.length <= MAXL) return [text];
  const words = text.split(' ');
  let best = null;
  for (let i = 1; i < words.length; i++) {
    const a = plain(words.slice(0, i).join(' ')), b = plain(words.slice(i).join(' '));
    if (a.length > MAXL || b.length > MAXL) continue;
    const score = Math.abs(a.length - b.length) - (/[,;:.]$/.test(a) ? 8 : 0);
    if (!best || score < best.s) best = { s: score, i };
  }
  if (!best) { if (strict) return null; best = { i: Math.ceil(words.length / 2) }; }
  return [words.slice(0, best.i).join(' '), words.slice(best.i).join(' ')];
}
const toAss = (t) => { const h = Math.floor(t / 3600), m = Math.floor(t / 60) % 60, s = t - 3600 * h - 60 * m;
  return `${h}:${String(m).padStart(2, '0')}:${s.toFixed(2).padStart(5, '0')}`; };
const toSrt = (t, sep) => { const ms = Math.round(t * 1000), h = Math.floor(ms / 3600000), m = Math.floor(ms / 60000) % 60, s = Math.floor(ms / 1000) % 60;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}${sep}${String(ms % 1000).padStart(3, '0')}`; };

const sheet = JSON.parse(fs.readFileSync(inp, 'utf8'));
const cues = [];
for (const s of sheet.sentences) {
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
  c.cps = plain(c.text).length / (c.end - c.start);
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
const ass = [
  '[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1920', 'PlayResY: 1080', 'WrapStyle: 2', 'ScaledBorderAndShadow: yes', 'YCbCr Matrix: TV.709', '',
  '[V4+ Styles]',
  'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
  STYLES[style], '',
  '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
  ...cues.map((c) => `Dialogue: 0,${toAss(c.start)},${toAss(c.end)},Sub,,0,0,0,,{\\fad(120,100)\\move(960,1020,960,1016,0,120)}${assText(c.text)}`),
].join('\n');
fs.writeFileSync(base + '.ass', ass + '\n');
fs.writeFileSync(base + '.srt', cues.map((c, i) => `${i + 1}\n${toSrt(c.start, ',')} --> ${toSrt(c.end, ',')}\n${wrap(plain(c.text)).join('\n')}\n`).join('\n'));
fs.writeFileSync(base + '.vtt', 'WEBVTT\n\n' + cues.map((c) => `${toSrt(c.start, '.')} --> ${toSrt(c.end, '.')}\n${wrap(plain(c.text)).join('\n')}\n`).join('\n'));
const fast = cues.filter((c) => c.cps > 17);
console.log(JSON.stringify({ cues: cues.length, max_cps: +Math.max(...cues.map((c) => c.cps)).toFixed(1), over_17cps: fast.length }));
