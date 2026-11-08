/* ch10_kit.js: helpers shared by the scenes of unit ch10 (copied from ch09_kit.js / chSOA2_kit.js) (labels with entrance/exit, faded groups,
   series lookup, on-screen text taken from the script). Pure functions of t; elements built in setup only.
   Nothing here duplicates a kit component; candidates for promotion are listed in script/_review/scenes_ch10.md. */
window.UK = (function () {
  const K = Kit, S = Scene, U = {};
  /** a text label: {text | html, x, y, anchor 'l'|'c'|'r', size, color (token), cls ('mono' | 'display' | 'halo'), at, out, parent, z, maxW, alpha} */
  U.label = function (ctx, o) {
    const e = K.el('div', { class: 'uk-lab ' + (o.cls || ''), html: o.html ?? K.markup(o.text) }, o.parent || ctx.stage);
    e.style.left = o.x + 'px'; e.style.top = o.y + 'px';
    const a = o.anchor || 'l'; e.style.transform = `translate(${a === 'c' ? '-50%' : a === 'r' ? '-100%' : '0'}, ${o.vmid ? '-50%' : '0'})`;
    if (o.size) e.style.fontSize = o.size + 'px';
    if (o.color) e.style.color = K.c(o.color);
    if (o.z !== undefined) e.style.zIndex = o.z;
    if (o.maxW) { e.style.whiteSpace = 'normal'; e.style.width = o.maxW + 'px'; }
    const { t0, t1 } = K.times(ctx, o, 0), din = o.din ?? 0.25;
    return ctx.add({ root: e, el: e, alpha: 1, render(t) { const v = K.env(t, t0, t1, din, 0.25); K.show(e, v.on); e.style.opacity = (v.o * (o.alpha ?? 1) * this.alpha).toFixed(3); } });
  };
  /** fade an element (HTML or SVG) in at `at` and out at `out` (multiplied by el.__dim if set) */
  U.fade = function (ctx, el, o) {
    const { t0, t1 } = K.times(ctx, o, 0), din = o.din ?? 0.35;
    return ctx.add({ root: el, dim: () => 1, render(t) { const v = K.env(t, t0, t1, din, o.dout ?? 0.3); el.style.display = v.on ? '' : 'none'; el.style.opacity = (v.o * this.dim(t)).toFixed(3); } });
  };
  U.series = (D, name) => { const s = D.series.find((x) => x.name === name); if (!s) throw new Error('series not found: ' + name); return s; };
  /** an on-screen label of the script that starts with `prefix` (keeps the writer's text, numbers included) */
  U.onscreen = (ctx, prefix, fallback) => { const L = (ctx.script && ctx.script.onscreen && ctx.script.onscreen.labels) || []; return L.find((x) => x.startsWith(prefix)) || fallback; };
  /** time of a fraction of the sentence whose cue is `cue` (falls back to cue + dt in previews) */
  U.frac = function (ctx, cue, f, dt) {
    const s = ctx.script && ctx.script.sentences && ctx.script.sentences.find((x) => x.cue === cue);
    return s && Number.isFinite(s.end) ? s.start + f * (s.end - s.start) : ctx.at(cue) + (dt ?? 2);
  };
  U.end = (ctx, cue, dt) => U.frac(ctx, cue, 1, dt);
  /** percent label from a fraction (display rounding only) */
  U.pc = (v) => `${Math.round(v)} %`;
  return U;
})();
/** the script's formulas, each split at its top-level ';' into at most two items when it is long (same text, shown
   one after the other: the first on its cue, the second `dt` s later); for Kit.formulaLayer({items}) */
UK.formulaItems = function (ctx, maxLen = 110, dt = 4) {
  const F = (ctx.script && ctx.script.onscreen && ctx.script.onscreen.formulas) || [];
  const cutAt = (tex) => {   // [a, b] at the most central top-level ';', else '+', else '\ \ ', else '\quad'; null if none
    const find = (test) => { const r = []; let d = 0; for (let i = 0; i < tex.length; i++) { const c = tex[i]; if (c === '{') d++; else if (c === '}') d--; else if (d === 0 && test(i, c)) r.push(i); } return r; };
    const pick = (r) => r.reduce((b, c) => (Math.abs(c - tex.length / 2) < Math.abs(b - tex.length / 2) ? c : b), r[0]);
    let r = find((i, c) => c === ';'); if (r.length) { const m = pick(r); return [tex.slice(0, m), tex.slice(m + 1)]; }
    r = find((i, c) => c === '+' && i > 0); if (r.length) { const m = pick(r); return [tex.slice(0, m), '\\dots ' + tex.slice(m)]; }
    r = find((i) => tex.startsWith('\\ \\ ', i)); if (r.length) { const m = pick(r); return [tex.slice(0, m), tex.slice(m)]; }
    r = find((i) => tex.startsWith('\\quad', i) && tex[i - 1] !== 'q'); if (r.length) { const m = pick(r); return [tex.slice(0, m), tex.slice(m)]; }
    r = find((i) => tex.startsWith('\\Rightarrow', i)); if (r.length) { const m = pick(r); return [tex.slice(0, m), tex.slice(m)]; }
    return null; };
  const clean = (t) => t.replace(/^(\\[ ,;!]|\\quad|\\qquad|\s)+/, '').replace(/(\\[ ,;!]|\\quad|\\qquad|\s)+$/, '').trim();
  const split = (tex, depth) => { if (tex.length <= maxLen || depth > 2) return [tex]; const c = cutAt(tex); return c ? [...split(clean(c[0]), depth + 1), ...split(clean(c[1]), depth + 1)] : [tex]; };
  const out = [];
  F.forEach((f, gi) => { const parts = split(f.tex, 0).filter((x) => x.trim().length); parts.forEach((p, k) => out.push({ tex: p, at: k ? `${f.cue}+${dt * k}` : f.cue, out: k === parts.length - 1 ? f.out : undefined, grp: gi, k, n: parts.length, cue: f.cue, dt })); });
  return out;
};

/** WORKAROUND (kit issue: Kit.formulaLayer keeps its empty frame and label between an item's `out` and the next
   item): one layer per item, each with its own at/out (out = the item's out, else the next item's start) */
UK.formulaLayers = function (ctx, label, items, o = {}) {
  items = items || UK.formulaItems(ctx);
  const T = (x) => (typeof x === 'number' ? x : ctx.at(x));
  // the parts of one statement share the time until the next statement starts (never two layers at once)
  const starts = [...new Set(items.filter((it) => !it.k).map((it) => T(it.cue ?? it.at)))].sort((a, b) => a - b);
  const rows = items.map((it) => { if (it.n > 1) { const c = T(it.cue), nx = starts.find((x) => x > c + 1e-6), span = nx !== undefined ? nx - c : it.n * it.dt; return Object.assign({}, it, { a: c + it.k * Math.min(it.dt, span / it.n) }); } return Object.assign({}, it, { a: T(it.at) }); })
    .sort((p, q) => p.a - q.a);
  rows.forEach((it, i) => { const nxt = rows[i + 1]; let out = it.out !== undefined ? T(it.out) : undefined; if (nxt && (out === undefined || out > nxt.a)) out = nxt.a;
    const L = Kit.formulaLayer(ctx, { label, items: [{ tex: it.tex, at: it.a }], at: it.a, out: out === undefined ? undefined : out - 0.25 });
    if (L && o.left) { L.root.style.left = '96px'; L.root.style.right = 'auto'; } });   // bottom-left (the lower-third zone) when a seat column fills the right
};
/** Kit.seat with the script's seat params: cues that the current narration variant lacks (e.g. 'data', 'verdict' of
   the result variant) fall back to frame + 0.8; the 'why' line goes under CONFIDENCE; returns the seat */
UK.seat = function (ctx, sp, extra = {}) {
  const has = (c) => { try { ctx.at(c); return true; } catch (e) { return false; } };
  const cues = Object.assign({}, sp.cues || {});
  for (const k of Object.keys(cues)) if (!has(cues[k])) cues[k] = k === 'data' ? `${cues.frame}+0.8` : cues.frame;
  const o = Object.assign({ variant: ctx.variant || 'pending', data: ctx.data.seat || null }, sp, extra, { cues });
  if (o.variant === 'result' && !o.data) o.variant = 'pending';
  const S = Kit.seat(ctx, o);
  if (sp.why && S.col && S.col.children[1]) { const p = Kit.el('p', { html: Kit.markup(sp.why) }, S.col.children[1]); p.style.fontSize = '28px'; p.style.color = 'var(--fg-2)'; }
  return S;
};
