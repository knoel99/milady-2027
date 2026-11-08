/* kit.js: core of the component kit (load after runtime/scene.js, before any other component file).
 *
 * Every component is a factory  Kit.<name>(ctx, opts)  called inside setup(ctx). It builds its DOM /
 * SVG / Canvas once, registers itself with ctx.add(), and is then redrawn by the runtime on every seek
 * as a pure function of t (no timers, no CSS transitions, no state carried between frames except
 * through Scene.stepper). Times are "time specs" resolved by ctx.at(): a number of seconds, a cue
 * name from the script ("eqs"), or a cue with an offset ("eqs+0.4", "eqs-0.2").
 *
 * Common options of every component:
 *   at     time spec of the entrance (default 0)
 *   out    time spec of the exit (default: stays until the end of the scene)
 *   parent element to mount into (default: a kit layer on #stage)
 * Every component returns an object {root, render(t), ...} whose root carries data-kit="<name>"
 * (the layout QA groups text boxes by it).
 */
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const S = window.Scene;
  if (!S) throw new Error('kit.js must be loaded after runtime/scene.js');
  const Kit = window.Kit || {};

  /** frame geometry at 1920x1080 (CSS px): content safe frame, subtitle band, fixed HUD zones */
  Kit.SAFE = { x0: 96, x1: 1824, y0: 56, y1: 880, band: 900, W: 1920, H: 1080 };
  Kit.ZONES = {
    badge: { x0: 1184, x1: 1824, y0: 40, y1: 100 },        // honesty badge, top-right
    needle: { x0: 1720, x1: 1824, y0: 124, y1: 228 },      // corner polarity needle (M1), under the badge
    rail: { x0: 0, x1: 92, y0: 180, y1: 780 },             // altitude rail (M8), left gutter
    lowerThird: { x0: 96, x1: 996, y0: 752, y1: 880 },     // lower-thirds, bottom-left
    formula: { x0: 1064, x1: 1824, y0: 752, y1: 880 },     // formula layer, bottom-right
  };

  // ---------- DOM helpers ----------
  Kit.NS = NS;
  /** HTML element: Kit.el('div', {class: 'x', style: 'left:4px'}, parent, 'text') */
  Kit.el = function (tag, attrs = {}, parent = null, text = null) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v === undefined || v === null) continue;
      if (k === 'html') e.innerHTML = v; else e.setAttribute(k, v);
    }
    if (text !== null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  };
  /** SVG element: Kit.s('path', {d: '…', fill: 'none'}, parent) */
  Kit.s = function (tag, attrs = {}, parent = null, text = null) {
    const e = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) if (v !== undefined && v !== null) e.setAttribute(k, v);
    if (text !== null) e.textContent = text;
    if (parent) parent.appendChild(e);
    return e;
  };
  /** full-stage HTML layer (z-index z), created on demand */
  Kit.layer = function (ctx, z = 10, name = '') {
    const d = Kit.el('div', { class: 'kit-layer', 'data-layer': name }, ctx.stage);
    d.style.zIndex = z;
    return d;
  };
  /** full-stage SVG layer in stage coordinates (viewBox 0 0 1920 1080) */
  Kit.svgLayer = function (ctx, z = 10, parent = null) {
    const svg = Kit.s('svg', { class: 'full', viewBox: '0 0 1920 1080', width: 1920, height: 1080 }, parent || ctx.stage);
    svg.style.zIndex = z; svg.style.overflow = 'visible';
    return svg;
  };
  /** Canvas layer with a hi-DPI backing store: {canvas, g} (drawn in CSS px) */
  Kit.canvasLayer = function (ctx, z = 5, box = null, parent = null) {
    const c = Kit.el('canvas', {}, parent || ctx.stage);
    const w = box ? box.w : 1920, h = box ? box.h : 1080;
    c.style.cssText = `position:absolute;left:${box ? box.x : 0}px;top:${box ? box.y : 0}px;width:${w}px;height:${h}px;z-index:${z}`;
    return { canvas: c, g: S.hidpi(c, w, h), w, h };
  };
  /** box of an element in stage coordinates (works in preview, where the stage is scaled) */
  Kit.box = function (el, ctx) {
    const st = (ctx ? ctx.stage : document.getElementById('stage')).getBoundingClientRect(), k = st.width / 1920;
    const r = el.getBoundingClientRect();
    return { x: (r.left - st.left) / k, y: (r.top - st.top) / k, w: r.width / k, h: r.height / k };
  };

  // ---------- time ----------
  /** entrance/exit envelope: {p: eased entrance progress, q: exit progress, o: opacity, on: visible} */
  Kit.env = function (t, t0, t1 = Infinity, din = 0.35, dout = 0.25, e = S.ease.outCubic) {
    const p = S.seg(t, t0, t0 + din, e), q = t1 === Infinity ? 0 : S.seg(t, t1, t1 + dout, S.ease.inOutSine);
    const o = S.seg(t, t0, t0 + din * 0.6, S.ease.linear) * (1 - q);
    return { p, q, o, on: t >= t0 && q < 1 };
  };
  /** resolve opts.at / opts.out once (in setup) */
  Kit.times = function (ctx, o, defAt = 0) {
    return { t0: ctx.at(o.at ?? defAt), t1: o.out === undefined || o.out === null ? Infinity : ctx.at(o.out) };
  };
  /** left-to-right reveal of an element by clip-path (p in [0, 1]); pad (px) keeps glyphs that overflow
   *  the box (KaTeX fractions, descenders, italics) unclipped above, below and on the left */
  Kit.wipe = function (el, p, pad = 200) {
    el.style.clipPath = p >= 1 ? 'none' : `inset(-${pad}px ${(100 - 100 * p).toFixed(3)}% -${pad}px -${pad}px)`;
    el.style.visibility = p <= 0 ? 'hidden' : 'visible';
  };
  Kit.show = (el, on) => { el.style.display = on ? '' : 'none'; };

  // ---------- text ----------
  const ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ESC[c]);
  Kit.esc = esc;
  /** script markup → HTML: {u}…{/} {b}…{/} {param}…{/} {model}…{/} {metric}…{/} key colours;
   *  *words* → <em> (target for the pen); $tex$ → KaTeX inline (if KaTeX is loaded) */
  Kit.markup = function (str) {
    let s = esc(str);
    s = s.replace(/\$([^$]+)\$/g, (m, tex) => (window.katex ? Kit.tex(tex.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&'), false) : m));
    s = s.replace(/\{(u|b|param|model|metric)\}(.*?)\{\/\}/g, '<span class="k-$1">$2</span>');
    s = s.replace(/\*(.+?)\*/g, '<em>$1</em>');
    return s;
  };
  /** capitals for mono labels WITHOUT touching math symbols: Greek letters and {sym}…{/} keep their case
   *  (CSS text-transform would turn ω into Ω, η into Η, j into J). Returns a plain string. */
  Kit.upper = function (str) {
    return String(str).split(/(\{sym\}.*?\{\/\}|[\u0370-\u03FF\u1F00-\u1FFF]+)/).map((p) => {
      if (!p) return '';
      const m = p.match(/^\{sym\}(.*?)\{\/\}$/);
      if (m) return m[1];
      return /^[\u0370-\u03FF\u1F00-\u1FFF]+$/.test(p) ? p : p.toUpperCase();
    }).join('');
  };
  /** shrink an element's font until it fits (w, h) in CSS px; never below minPx (warns instead) */
  Kit.fit = function (el, maxW, maxH, minPx = 28, ctx = null) {
    const cs = getComputedStyle(el); let fs = parseFloat(cs.fontSize);
    const fits = () => (!maxW || el.scrollWidth <= maxW + 0.5) && (!maxH || el.scrollHeight <= maxH + 0.5);
    while (!fits() && fs > minPx) { fs = Math.max(minPx, fs - 2); el.style.fontSize = fs + 'px'; }
    if (!fits()) S.warn(`text does not fit (${Math.round(el.scrollWidth)}x${Math.round(el.scrollHeight)} > ${maxW}x${maxH}) at ${minPx}px: "${el.textContent.slice(0, 60)}…" — shorten it`);
    return fs;
  };
  /** number for the screen: 3 significant digits, × 10ⁿ for very small/large, minus sign U+2212 */
  const SUP = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
  Kit.fmt = function (x, sig = 3, opts = {}) {
    if (x === null || x === undefined || !Number.isFinite(+x)) return '–';
    x = +x;
    if (x === 0) return '0';
    const a = Math.abs(x), e = Math.floor(Math.log10(a));
    let s;
    if (e < (opts.minExp ?? -3) || e > (opts.maxExp ?? 5)) {
      const m = x / Math.pow(10, e);
      s = (+m.toPrecision(sig)).toString() + ' × 10' + String(e).split('').map((c) => SUP[c]).join('');
    } else {
      s = (+x.toPrecision(sig)).toString();
      if (opts.fixed !== undefined) s = x.toFixed(opts.fixed);
    }
    return s.replace(/^-/, '−');
  };
  /** tick label of a log axis: 1, 10, 10², 10⁻³ … (mantissa kept when it is not 1) */
  Kit.pow10 = function (v) {
    const e = Math.round(Math.log10(v));
    if (Math.abs(v / Math.pow(10, e) - 1) > 1e-6) return Kit.fmt(v, 2);
    if (e === 0) return '1'; if (e === 1) return '10';
    return '10' + String(e).split('').map((c) => SUP[c]).join('');
  };
  /** KaTeX to an HTML string with the kit macros (colour by role) */
  Kit.MACROS = {
    '\\U': '\\htmlClass{k-u}{\\mathbf{u}}', '\\B': '\\htmlClass{k-b}{\\mathbf{B}}',
    '\\Rm': '\\htmlClass{k-param}{\\mathrm{Rm}}', '\\etaP': '\\htmlClass{k-param}{\\eta}', '\\Gam': '\\htmlClass{k-param}{\\Gamma}',
    '\\RE': '\\htmlClass{k-param}{\\mathrm{Re}}', '\\PM': '\\htmlClass{k-param}{\\mathrm{Pm}}', '\\Po': '\\htmlClass{k-param}{\\mathrm{Po}}',
    '\\vth': '\\htmlClass{k-model}{v_\\theta}', '\\Edist': '\\htmlClass{k-metric}{\\mathcal{E}}',
    '\\cu': '\\htmlClass{k-u}{#1}', '\\cb': '\\htmlClass{k-b}{#1}', '\\cp': '\\htmlClass{k-param}{#1}',
    '\\cm': '\\htmlClass{k-model}{#1}', '\\ck': '\\htmlClass{k-metric}{#1}', '\\cg': '\\htmlClass{k-muted}{#1}',
  };
  Kit.tex = function (tex, display = true, extraMacros = {}) {
    if (!window.katex) throw new Error('KaTeX not loaded (add vendor/katex/katex.min.js and katex.min.css)');
    return katex.renderToString(tex, { displayMode: display, output: 'html', strict: 'ignore', throwOnError: true,
      macros: Object.assign({}, Kit.MACROS, extraMacros), trust: (c) => ['\\htmlClass', '\\htmlId', '\\htmlData'].includes(c.command) });
  };

  // ---------- registry checks run by the runtime after setup ----------
  Kit._intervals = [];   // [{kind, t0, t1, label}] for one-at-a-time rules
  Kit.claim = function (kind, t0, t1, label) {
    for (const o of Kit._intervals) if (o.kind === kind && t0 < o.t1 && o.t0 < t1) {
      S.warn(`two ${kind}s on screen at once (${o.label} / ${label}): at most one at a time`);
    }
    Kit._intervals.push({ kind, t0, t1, label });
  };
  Kit.afterSetup = function () { /* hook for future global checks */ };

  // ---------- colour utilities (Canvas) ----------
  Kit.hex = function (h) { h = h.replace('#', ''); if (h.length === 3) h = h.split('').map((c) => c + c).join('');
    return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; };
  Kit.rgba = (h, a) => { const [r, g, b] = Kit.hex(h); return `rgba(${r},${g},${b},${a})`; };
  /** resolve a key name ('u', 'b', 'param', 'model', 'metric', 'fg', 'muted', 'chalk'…) or a #hex */
  Kit.c = (k) => (k && k[0] === '#' ? k : S.col(k || 'fg'));

  window.Kit = Kit;
})();
