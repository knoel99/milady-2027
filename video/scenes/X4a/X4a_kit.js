/* Unit helpers (batch 4: X1–X6). Generic timing/label helpers shared by the unit's scenes (a copy lives in each
   unit folder: CONTRACT 13.1 "unit helpers", never loaded across folders). Tokens only, pure functions of t. */
(function () {
  'use strict';
  const S = window.Scene, K = window.Kit;
  const XK = window.XK = {};
  /** fade (and optional slide) of any HTML/SVG element between two time specs; returns the element */
  XK.timed = function (ctx, el, at, out, o = {}) {
    const t0 = typeof at === 'number' && o.raw ? at : ctx.at(at ?? 0);
    const t1 = out === undefined || out === null ? Infinity : ctx.at(out);
    const din = o.din ?? 0.3, dout = o.dout ?? 0.3, dy = o.dy ?? 0, dx = o.dx ?? 0, svg = el instanceof SVGElement;
    const base = o.op ?? 1, dim = o.dim || null;   // dim: [at, to] lowers the opacity later
    const td = dim ? ctx.at(dim[0]) : 0;
    ctx.add({ render(t) {
      const p = S.seg(t, t0, t0 + din, S.ease.outCubic), q = t1 === Infinity ? 0 : S.seg(t, t1, t1 + dout, S.ease.linear);
      let a = p * (1 - q) * base; if (dim) a *= 1 - (1 - dim[1]) * S.seg(t, td, td + 0.6, S.ease.inOutSine);
      el.style.opacity = a.toFixed(3); el.style.display = a > 0.001 ? '' : 'none';
      if (dx || dy) { const tr = `translate(${(dx * (1 - p)).toFixed(1)}px, ${(dy * (1 - p)).toFixed(1)}px)`;
        if (svg) el.style.transform = tr; else el.style.translate = `${(dx * (1 - p)).toFixed(1)}px ${(dy * (1 - p)).toFixed(1)}px`; }
    } });
    return el;
  };
  /** an HTML label: anchor l | c | r, class xk-lab (+ cls); markup through Kit.markup */
  XK.lab = function (ctx, text, x, y, o = {}) {
    const e = K.el('div', { class: 'xk-lab ' + (o.cls || ''), html: o.html ? text : K.markup(text) }, o.parent || ctx.stage);
    e.style.left = x + 'px'; e.style.top = y + 'px'; e.style.zIndex = o.z ?? 31;
    if (o.anchor === 'c') e.style.transform = 'translateX(-50%)'; else if (o.anchor === 'r') e.style.transform = 'translateX(-100%)';
    if (o.color) e.style.color = K.c(o.color);
    if (o.size) e.style.fontSize = o.size + 'px';
    if (o.w) { e.style.width = o.w + 'px'; e.style.whiteSpace = 'normal'; }
    if (o.at !== undefined || o.out !== undefined) XK.timed(ctx, e, o.at ?? 0, o.out, o);
    return e;
  };
  /** the scene title (Inter Display 56, left at x 160) */
  XK.title = function (ctx, text, at, o = {}) {
    const e = XK.lab(ctx, text, o.x ?? 160, o.y ?? 196, { cls: 'xk-title', at, out: o.out, dy: 10 });
    return e;
  };
  /** an SVG path drawn on by stroke-dashoffset between at and at+dur (pathLength normalised) */
  XK.drawOn = function (ctx, path, at, dur = 0.8, out) {
    path.setAttribute('pathLength', 1); const t0 = ctx.at(at), t1 = out === undefined ? Infinity : ctx.at(out);
    ctx.add({ render(t) { const p = S.seg(t, t0, t0 + dur, S.ease.inOutSine), q = t1 === Infinity ? 0 : S.seg(t, t1, t1 + 0.3, S.ease.linear);
      path.style.strokeDasharray = '1 1'; path.style.strokeDashoffset = (1 - p).toFixed(4); path.style.opacity = (1 - q).toFixed(3); path.style.display = p > 0 && q < 1 ? '' : 'none'; } });
    return path;
  };
  /** a white/panel card (HTML) with optional heading; returns {root, body} */
  XK.card = function (ctx, x, y, w, h, o = {}) {
    const r = K.el('div', { class: 'xk-card ' + (o.cls || '') }, o.parent || ctx.stage);
    Object.assign(r.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px', zIndex: o.z ?? 14 });
    if (o.head) K.el('div', { class: 'xk-card-h', html: K.markup(o.head) }, r);
    const body = K.el('div', { class: 'xk-card-b', html: o.body ? K.markup(o.body) : '' }, r);
    if (o.at !== undefined) XK.timed(ctx, r, o.at, o.out, o);
    return { root: r, body };
  };
  /** inline KaTeX block placed at (x, y), anchor l | c */
  XK.tex = function (ctx, tex, x, y, o = {}) {
    const e = K.el('div', { class: 'xk-tex', html: K.tex(tex, false, o.macros || {}) }, o.parent || ctx.stage);
    e.style.left = x + 'px'; e.style.top = y + 'px'; e.style.fontSize = (o.size || 40) + 'px'; e.style.zIndex = o.z ?? 30;
    if (o.anchor === 'c') e.style.transform = 'translateX(-50%)';
    if (o.color) e.style.color = K.c(o.color);
    if (o.at !== undefined) XK.timed(ctx, e, o.at, o.out, o);
    return e;
  };
  /** lamp row: cards with a label and a lamp that lights at its time; state 'on' | 'off' | 'dim' */
  XK.lamp = function (ctx, x, y, text, at, o = {}) {
    const e = K.el('div', { class: 'xk-lamp', html: `<i></i><span>${K.markup(text)}</span>` }, o.parent || ctx.stage);
    e.style.left = x + 'px'; e.style.top = y + 'px'; e.style.zIndex = o.z ?? 31;
    const i = e.firstChild, col = K.c(o.color || 'metric'), t1 = ctx.at(at);
    XK.timed(ctx, e, o.show ?? at, o.out);
    ctx.add({ render(t) { const p = S.seg(t, t1, t1 + 0.25, S.ease.linear); i.style.background = p > 0.5 ? col : 'transparent'; i.style.borderColor = col; } });
    return e;
  };
  /** ink change (T3): an overlay in the previous register (default NIGHT) clipped away behind a graphite pen line drawn left to right */
  XK.inkChange = function (ctx, t0, t1, y, from = 'night') {
    const ov = K.el('div', { class: 'xk-night', 'data-register': from, 'data-qa': 'ignore' }, ctx.stage);
    const pen = K.el('div', { class: 'xk-pen', 'data-qa': 'ignore' }, ctx.stage); pen.style.top = (y - 2) + 'px';
    ctx.add({ render(t) { const p = S.seg(t, t0, t1, S.ease.inOutSine);
      ov.style.clipPath = `inset(0 0 0 ${(100 * p).toFixed(2)}%)`; ov.style.display = p < 1 ? '' : 'none';
      pen.style.width = (1920 * p).toFixed(1) + 'px'; pen.style.opacity = (1 - S.seg(t, t1, t1 + 0.4, S.ease.linear)).toFixed(3); pen.style.display = t > t1 + 0.4 ? 'none' : ''; } });
  };
  /** sentence fraction: time at fraction f of a sentence (cue-based fallback when the script has no sentences) */
  XK.frac = function (ctx, cue, f, fb) {
    const s = (ctx.script.sentences || []).find((x) => x.cue === cue);
    return s && s.end > s.start ? s.start + f * (s.end - s.start) : ctx.at(cue) + (fb ?? 2 * f);
  };
  XK.lerp = (a, b, p) => a + (b - a) * p;
  /** time spec + offset (ctx.at does not chain offsets) */
  XK.at = (ctx, spec, dt = 0) => ctx.at(spec) + dt;
  /** a deterministic Gaussian pair */
  XK.gauss = (rng) => { const u = Math.max(1e-9, rng()), v = rng(); return [Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v), Math.sqrt(-2 * Math.log(u)) * Math.sin(2 * Math.PI * v)]; };
  /** read a dotted path from an object */
  XK.get = (o, path) => path.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
})();
