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
  /** PAPER ink change (T3): a NIGHT overlay clipped away behind a graphite pen line drawn left to right */
  XK.inkChange = function (ctx, t0, t1, y) {
    const ov = K.el('div', { class: 'xk-night', 'data-register': 'night', 'data-qa': 'ignore' }, ctx.stage);
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
  /** a deterministic Gaussian pair */
  XK.gauss = (rng) => { const u = Math.max(1e-9, rng()), v = rng(); return [Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v), Math.sqrt(-2 * Math.log(u)) * Math.sin(2 * Math.PI * v)]; };
  /** read a dotted path from an object */
  XK.get = (o, path) => path.split('.').reduce((a, k) => (a == null ? a : a[k]), o);
})();
/* X2 strip: five page cards (one per proposition), the active one at 100 % with a graphite underline, the others at
   45 % (script entry.params.strip). Glyphs are small ink drawings; the crowd glyph is amber. */
(function () {
  'use strict';
  const S = window.Scene, K = window.Kit, XK = window.XK;
  const glyph = (g, k) => {
    const ink = K.c('fg-2');
    const P = (d, col, w) => K.s('path', { d, fill: 'none', stroke: col || ink, 'stroke-width': w || 2, 'stroke-linecap': 'round' }, g);
    if (k === 0) { P('M4,22 C10,6 26,6 32,22'); P('M9,22 C13,12 23,12 27,22'); P('M14,22 C16,17 20,17 22,22'); }
    if (k === 1) P('M2,16 L7,6 L12,26 L17,6 L22,26 L27,6 L32,16');
    if (k === 2) { P('M3,26 C8,2 28,2 33,26'); K.s('circle', { cx: 18, cy: 20, r: 4, fill: 'none', stroke: ink, 'stroke-width': 2 }, g); }
    if (k === 3) { P('M18,2 L18,30', null, 2); K.s('circle', { cx: 8, cy: 12, r: 4, fill: ink }, g); K.s('circle', { cx: 28, cy: 20, r: 4, fill: 'none', stroke: ink, 'stroke-width': 2 }, g); }
    if (k === 4) [[8, 2], [5, 6], [2, 10]].forEach(([x, y]) => K.s('rect', { x, y, width: 18, height: 20, rx: 2, fill: K.c('panel'), stroke: K.c('metric'), 'stroke-width': 2 }, g));
  };
  /** XK.strip(ctx, P.strip, {at, activeAt}): cards slide in on `at`; the active card lights on `activeAt` */
  XK.strip = function (ctx, P, o = {}) {
    const t0 = ctx.at(o.at ?? -0.4), ta = ctx.at(o.activeAt ?? -0.4), cards = [];
    P.cards.forEach((c, k) => {
      const e = K.el('div', { class: 'x2-card' }, ctx.stage);
      Object.assign(e.style, { left: (P.x0 + k * (P.w + P.gap)) + 'px', top: P.y + 'px', width: P.w + 'px' });
      const sv = K.s('svg', { width: 36, height: 32, viewBox: '0 0 36 32' }, e); glyph(sv, k);
      K.el('span', {}, e, c.label);
      const ul = K.el('div', { class: 'ul' }, e);
      cards.push({ e, ul, k });
    });
    ctx.add({ render(t) {
      cards.forEach(({ e, ul, k }) => {
        const p = S.seg(t, t0 + 0.08 * k, t0 + 0.08 * k + 0.35, S.ease.outCubic), a = S.seg(t, ta, ta + 0.3, S.ease.linear);
        const act = k + 1 === P.active, op = act ? 1 : 1 - 0.55 * a;
        e.style.opacity = (p * op).toFixed(3); e.style.display = p > 0 ? '' : 'none';
        e.style.translate = `${(-30 * (1 - p)).toFixed(1)}px 0`;
        ul.style.opacity = act ? a.toFixed(3) : 0;
      });
    } });
    return cards;
  };
})();
