/* scene.js: deterministic scene runtime (v2: prototype contract + kit hooks).
 *
 * Every scene HTML includes this file first (then the kit files it uses), then calls Scene.define({...}).
 * Contract exposed to the recorder (capture.js, stills.js) and to humans:
 *   window.DURATION      scene length in seconds (from the timeline entry, else the scene default)
 *   window.READY         true once fonts, data and setup() are done
 *   window.seek(t)       renders the frame at time t (seconds) and resolves when it is on screen;
 *                        window.__seek is an alias
 *   window.__ENTRY__     optional, injected by the recorder: {duration, cues, status, variant, data,
 *                        params, seed, register, badge, level, onscreen, question, id}
 *   window.__CAPTURE__   true when recorded: real clocks are frozen and replaced by virtual time
 *   window.__SCENE_ERROR__     set on any setup/data/font error (the recorder aborts loudly)
 *   window.__SCENE_WARNINGS__  list of non-fatal problems (unknown cue, two lower-thirds at once...)
 *   window.__QA__(t)     layout check at time t: small text, text outside the safe frame or in the
 *                        subtitle band, overlapping text boxes (see CONTRACT.md, checklist)
 *
 * Determinism rules enforced or helped here:
 *   - Date.now, performance.now and requestAnimationFrame follow the virtual clock in capture mode;
 *     queued rAF callbacks are flushed once per seek, with the virtual timestamp.
 *   - Math.random is replaced by a seeded generator (mulberry32) in all modes; components use their
 *     own streams (Scene.rng(key)) so adding one component never changes another one's randomness.
 *   - Web Animations (CSS animations/transitions included) are paused and set to currentTime = t.
 *   - Scene.stepper() integrates any state machine with a fixed dt and an integer step count, so a
 *     frame at time t is identical whatever the fps, the worker split or the seek order.
 */
(function () {
  'use strict';
  const qs = new URLSearchParams(location.search);
  const CAPTURE = !!window.__CAPTURE__ || qs.has('capture');
  // root of the video project (…/video/), from this script's own URL: data/, vendor/ and runtime/
  // paths are resolved against it whatever the depth of the scene file
  const SELF = (document.currentScript && document.currentScript.src) || location.href;
  const ROOT = new URL('../', SELF).href;

  // ---------- seeded randomness ----------
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  /** FNV-1a 32-bit hash of a string (stable seeds from names) */
  function hash(s) {
    let h = 0x811c9dc5;
    for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193); }
    return h >>> 0;
  }
  const entry = window.__ENTRY__ || (qs.get('entry') ? JSON.parse(qs.get('entry')) : {});
  const SEED = entry.seed ?? 12345;
  Math.random = mulberry32(SEED);

  // ---------- virtual clock ----------
  let vt = 0;                       // virtual time in seconds
  let rafQueue = [];
  const realRAF = window.requestAnimationFrame.bind(window);
  if (CAPTURE) {
    const epoch = Date.UTC(2027, 0, 1);
    Date.now = () => epoch + Math.round(vt * 1000);
    try { performance.now = () => vt * 1000; } catch (e) { /* read-only on some builds */ }
    let id = 0;
    window.requestAnimationFrame = (cb) => { rafQueue.push(cb); return ++id; };
    window.cancelAnimationFrame = () => {};
  }

  // ---------- helpers ----------
  const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const lerp = (a, b, p) => a + (b - a) * p;
  const ease = {
    linear: (p) => p,
    inOutCubic: (p) => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2),
    outCubic: (p) => 1 - Math.pow(1 - p, 3),
    inCubic: (p) => p * p * p,
    inOutSine: (p) => -(Math.cos(Math.PI * p) - 1) / 2,
    smooth: (p) => p * p * (3 - 2 * p),
  };
  /** progress of t inside [a, b], eased, clamped to [0, 1] */
  const seg = (t, a, b, e = ease.inOutCubic) => e(clamp((t - a) / Math.max(1e-9, b - a)));
  /** closed-form spring step response for p in [0, 1] (duration-normalised), overshoot <= `over`
   *  (default 3 %, the style guide's cap for physical objects: needles, knobs); exactly 1 for p >= 1 */
  function spring(p, over = 0.03) {
    if (p <= 0) return 0; if (p >= 1) return 1;
    if (over <= 0) { const w = 7; return 1 - Math.exp(-w * p) * (1 + w * p); }   // critically damped
    const L = Math.log(over), z = -L / Math.sqrt(Math.PI * Math.PI + L * L);      // damping ratio
    const wn = 6 / z, wd = wn * Math.sqrt(1 - z * z);
    return 1 - Math.exp(-z * wn * p) * (Math.cos(wd * p) + (z / Math.sqrt(1 - z * z)) * Math.sin(wd * p));
  }
  /** fixed-step integrator: at(t) returns the state after floor(t/dt) steps */
  function stepper(init, step, dt) {
    let state = init(), n = 0;
    return function at(t) {
      const target = Math.floor(t / dt + 1e-6);
      if (target < n) { state = init(); n = 0; }
      while (n < target) { state = step(state, dt, n * dt) || state; n++; }
      return state;
    };
  }
  /** resolve a data or asset path: "data/x.json", "vendor/…", "runtime/…" are relative to the
   *  video root; anything else (./, ../, absolute URL) relative to the page, as written */
  function url(p) {
    if (/^(data|vendor|runtime|assets)\//.test(p)) return new URL(p, ROOT).href;
    return new URL(p, location.href).href;
  }
  /** decode a packed array {dtype:"f32", shape:[…], b64:"…"} (written by tools/data_*.py) into a
   *  Float32Array with a .shape property; plain arrays are returned unchanged */
  function f32(obj) {
    if (!obj || Array.isArray(obj) || obj instanceof Float32Array) return obj;
    if (obj.dtype !== 'f32' || typeof obj.b64 !== 'string') throw new Error('Scene.f32: not a packed f32 array');
    const bin = atob(obj.b64), n = bin.length, buf = new Uint8Array(n);
    for (let i = 0; i < n; i++) buf[i] = bin.charCodeAt(i);
    const a = new Float32Array(buf.buffer);
    a.shape = obj.shape || [a.length];
    return a;
  }

  const warnings = [];
  window.__SCENE_WARNINGS__ = warnings;
  function warn(msg) { if (!warnings.includes(msg)) { warnings.push(msg); console.warn('[scene] ' + msg); } }

  async function loadData(spec, status) {
    const out = {}, missing = [], optional = [];
    const overrides = entry.data || {};
    for (const [name, v] of Object.entries(spec || {})) {
      const opt = typeof v === 'object' && v !== null ? !!v.optional : false;
      const url0 = typeof v === 'object' && v !== null ? v.url : v;
      const u = url(overrides[name] || url0);
      try {
        const r = await fetch(u, { cache: 'no-store' });
        if (!r.ok) throw new Error(r.status + ' ' + u);
        if (/\.(f32|bin)$/.test(u)) out[name] = new Float32Array(await r.arrayBuffer());
        else out[name] = await r.json();
      } catch (e) {
        out[name] = null;
        (opt || status === 'pending' ? optional : missing).push(name + ' (' + u + ')');
      }
    }
    return { data: out, missing, optional };
  }

  let readyResolve, readyReject;
  const readyP = new Promise((res, rej) => { readyResolve = res; readyReject = rej; });
  readyP.catch(() => {});
  let current = null;   // {spec, ctx}
  window.READY = false;

  const colCache = {};
  const Scene = {
    /** JS mirror of the NIGHT tokens (theme.css); use Scene.col(name) for register-aware values */
    C: { bg: '#0B0F14', panel: '#10151C', grid: '#1A222D', fg: '#F2F4F7', fg2: '#C7D0DA', muted: '#9AA6B2', chalk: '#E8E4D8',
         param: '#1BAF7A', u: '#3987E5', b: '#EB6834', model: '#B49CF0', metric: '#EDA100', infra: '#6B7A8C',
         matter: '#7C8794', matterDark: '#3A3F47', bNeg: '#9C3F18', silver: '#C9D3E0', uHi: '#6FB1FF', bHi: '#FF8A4C' },
    W: 1920, H: 1080, ROOT, CAPTURE, entry,
    clamp, lerp, ease, seg, spring, stepper, mulberry32, hash, url, f32, warn,
    /** independent seeded stream for a component or a use: Scene.rng('cloud') */
    rng: (key = '') => mulberry32((SEED ^ hash(String(key))) >>> 0),
    get time() { return vt; },
    /** current value of a colour token (--b, --param…) for the stage's register (Canvas code) */
    col(name) {
      const st = document.getElementById('stage');
      const reg = (st && st.dataset.register) || 'night', k = reg + ':' + name;
      if (!(k in colCache)) {
        const css = name.startsWith('--') ? name : '--' + name.replace(/[A-Z]/g, (m) => '-' + m.toLowerCase());
        const v = st ? getComputedStyle(st).getPropertyValue(css).trim() : '';
        colCache[k] = v || Scene.C[name] || '#ff00ff';
      }
      return colCache[k];
    },
    /** 2D context whose backing store follows devicePixelRatio (crisp at 4K = deviceScaleFactor 2), drawn in CSS px */
    hidpi(canvas, w = 1920, h = 1080) {
      const d = window.devicePixelRatio || 1;
      canvas.width = Math.round(w * d); canvas.height = Math.round(h * d);
      const g = canvas.getContext('2d'); g.setTransform(d, 0, 0, d, 0, 0); return g;
    },

    async define(spec) {
      try { await defineImpl(spec); }
      catch (e) { window.__SCENE_ERROR__ = String(e && e.message || e); console.error(e); readyReject(e); }
    },
  };

  const KATEX_FONTS = ['400 40px KaTeX_Main', 'italic 400 40px KaTeX_Math', '700 40px KaTeX_Main', 'italic 400 40px KaTeX_Main',
    '400 40px KaTeX_Size1', '400 40px KaTeX_Size2', '400 40px KaTeX_Size3', '400 40px KaTeX_Size4', '400 40px KaTeX_AMS'];
  const BASE_FONTS = ['400 30px Inter', '500 30px Inter', '600 30px Inter', '600 60px "Inter Display"', '800 60px "Inter Display"',
    '500 28px "JetBrains Mono"'];

  async function defineImpl(spec) {
    const stage = document.getElementById('stage');
    if (!stage) throw new Error('no #stage element');
    const duration = entry.duration ?? (qs.get('dur') ? +qs.get('dur') : spec.duration);
    if (!(duration > 0)) throw new Error('scene duration missing (spec.duration or entry.duration)');
    const specCues = spec.cues || {};
    const cues = Object.assign({}, specCues, entry.cues || {});
    const status = entry.status || spec.status || 'ready';
    const register = entry.register || (entry.params && entry.params.register) || spec.register || 'night';
    stage.dataset.register = String(register).toLowerCase();
    window.DURATION = duration;
    if (entry.cues) {
      for (const k of Object.keys(specCues)) if (!(k in entry.cues)) warn(`cue "${k}" is used by the scene but absent from the script entry (default time ${specCues[k]} s used)`);
    }
    const { data, missing, optional } = await loadData(spec.data, status);
    if (missing.length && spec.requireData !== false) {
      throw new Error('missing data: ' + missing.join(', '));
    }
    const fonts = (spec.fonts || BASE_FONTS).concat(window.katex ? KATEX_FONTS : []);
    await Promise.all(fonts.map((f) => document.fonts.load(f)));
    await document.fonts.ready;
    const used = new Set();
    const at = (s, fallback) => {
      if (s === undefined || s === null) {
        if (fallback === undefined) throw new Error('time spec missing'); return at(fallback);
      }
      if (typeof s === 'number') return s;
      if (typeof s === 'object') return at(s.cue) + (s.dt || 0);
      const m = String(s).match(/^\s*([A-Za-z_][\w.:-]*)\s*(?:([+-])\s*([\d.]+))?\s*$/);
      if (!m) { const n = Number(s); if (Number.isFinite(n)) return n; throw new Error('bad time spec: ' + s); }
      const name = m[1];
      let base;
      if (name in cues) { base = cues[name]; used.add(name); }
      else if (fallback !== undefined) return at(fallback);
      else throw new Error(`unknown cue "${name}" (declare it in Scene.define({cues}) with a preview time)`);
      return base + (m[2] ? (m[2] === '+' ? 1 : -1) * Number(m[3]) : 0);
    };
    // pending scenes: "pending" narration and empty seat; once the script marks them ready (data in),
    // the same template draws the "result" variant
    const variant = entry.variant || (status === 'pending' ? 'pending' : 'result');
    const ctx = {
      stage, data, missing: missing.concat(optional), cues, status, variant, duration, register: stage.dataset.register,
      params: Object.assign({}, spec.params || {}, entry.params || {}),
      /** what the script says about this scene (badge, level, onscreen, question…), when the build passes it */
      script: entry,
      /** time of a named cue, with a fallback when the timeline does not provide it */
      cue: (name, fallback) => (name in cues ? (used.add(name), cues[name]) : fallback),
      /** time spec → seconds: 2.5 | "eqs" | "eqs+0.4" | "eqs-0.2" | {cue:"eqs", dt:0.4} */
      at,
      layers: [],
      /** register a component: its render(t) is called on every seek, before the scene's render */
      add(comp) { ctx.layers.push(comp); return comp; },
      warn,
    };
    if (status === 'provisional') {
      const s = document.createElement('div'); s.id = '__stamp';
      s.textContent = 'PROVISIONAL DATA' + (entry.stamp ? ' · ' + entry.stamp : '');
      stage.appendChild(s);
    }
    if (spec.dither) addDither(stage);
    if (spec.setup) await spec.setup(ctx);
    // fonts requested by DOM built in setup (KaTeX glyphs, late weights) must be in before frame 0
    void stage.offsetHeight; await document.fonts.ready;
    if (window.Kit && window.Kit.afterSetup) window.Kit.afterSetup(ctx);
    current = { spec, ctx };
    window.__CUES_USED__ = () => Array.from(used);
    window.READY = true; readyResolve();
    if (!CAPTURE) startPreview(duration);
  }

  /** static 1.5 % noise against banding of dark gradients (opt-in: Scene.define({dither: true})) */
  function addDither(stage) {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256;
    const g = c.getContext('2d'), im = g.createImageData(256, 256), r = mulberry32(7);
    for (let i = 0; i < im.data.length; i += 4) { const v = r() * 255; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; }
    g.putImageData(im, 0, 0);
    const d = document.createElement('div'); d.id = '__dither';
    d.style.cssText = `position:absolute;inset:0;pointer-events:none;opacity:.015;z-index:90;background-image:url(${c.toDataURL()});`;
    stage.appendChild(d);
  }

  async function seek(t) {
    await readyP;
    vt = t;
    const { spec, ctx } = current;
    for (const a of document.getAnimations()) { a.pause(); a.currentTime = t * 1000; }
    for (const L of ctx.layers) if (L.render) L.render(t, ctx);
    if (spec.render) spec.render(t, ctx);
    if (rafQueue.length) { const q = rafQueue; rafQueue = []; q.forEach((cb) => cb(t * 1000)); }
    if (spec.afterRender) await spec.afterRender(t, ctx);
    return t;
  }
  window.seek = window.__seek = seek;

  // ---------- layout QA (reviewers, stills): window.__QA__(t) -> list of issues ----------
  window.__QA__ = async function (t, opts = {}) {
    if (t !== undefined) await seek(t);
    const stage = document.getElementById('stage'), sr = stage.getBoundingClientRect(), k = sr.width / 1920;
    const MIN = opts.minPx || 28, BAND = opts.band || 900;
    const issues = [], boxes = [];
    const visible = (el) => {
      for (let e = el; e && e !== stage; e = e.parentElement) {
        const cs = getComputedStyle(e);
        if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < 0.05) return false;
      }
      return true;
    };
    const all = stage.querySelectorAll('*');
    for (const el of all) {
      if (el.closest('#__hud,[data-qa="ignore"]')) continue;
      const own = Array.from(el.childNodes).some((n) => n.nodeType === 3 && n.textContent.trim());
      if (!own || !visible(el)) continue;
      const inKatex = el.closest('.katex');
      const r = el.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) continue;
      const kitEl = el.closest('[data-kit]');
      const box = { x: (r.left - sr.left) / k, y: (r.top - sr.top) / k, w: r.width / k, h: r.height / k,
        text: el.textContent.trim().slice(0, 40), owner: (kitEl && kitEl.dataset.kit) || el.id || el.tagName.toLowerCase(),
        node: inKatex ? inKatex : el, katex: !!inKatex };
      if (!inKatex) {
        const fs = parseFloat(getComputedStyle(el).fontSize) * (el instanceof SVGElement ? (el.ownerSVGElement?.getScreenCTM()?.a || k) / k : 1);
        if (fs < MIN - 0.01) issues.push({ kind: 'small-text', px: +fs.toFixed(1), ...box });
      } else {
        const root = inKatex.closest('.katex-display, .katex');
        const fs = parseFloat(getComputedStyle(root).fontSize);
        if (fs < MIN - 0.01) issues.push({ kind: 'small-formula', px: +fs.toFixed(1), ...box });
      }
      if (box.x < -0.5 || box.y < -0.5 || box.x + box.w > 1920.5 || box.y + box.h > 1080.5) issues.push({ kind: 'clipped', ...box });
      else if (box.y + box.h > BAND + 0.5 && !el.closest('[data-band="ok"]')) issues.push({ kind: 'subtitle-band', ...box });
      boxes.push(box);
    }
    // overlaps between text boxes (pieces of one formula are one box; an element and its own descendants
    // are not compared): catches a legend over a band label inside one plot as well as two components
    for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
      const a = boxes[i], b = boxes[j];
      if (a.node === b.node || a.node.contains(b.node) || b.node.contains(a.node)) continue;
      const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x), oy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
      if (ox > 2 && oy > 2) issues.push({ kind: 'overlap', a: a.owner + ': ' + a.text, b: b.owner + ': ' + b.text, x: Math.round(a.x), y: Math.round(a.y) });
    }
    return { t: vt, issues: issues.map(({ node, ...rest }) => rest), warnings: warnings.slice() };
  };

  // ---------- preview mode (a normal browser tab): real-time loop with a scrub bar ----------
  function startPreview(duration) {
    const hud = document.createElement('div'); hud.id = '__hud';
    hud.innerHTML = '<span id="__t">0.00</span><div class="bar"><i></i></div><span>space: pause · ←/→: frame · g: safe area</span>';
    document.body.appendChild(hud);
    const bar = hud.querySelector('.bar'), fill = bar.querySelector('i'), tl = hud.querySelector('#__t');
    let playing = !qs.has('t'), t = qs.has('t') ? +qs.get('t') : 0, last = null;
    // scale the 1920x1080 stage to the window
    const fit = () => { const s = Math.min(innerWidth / 1920, (innerHeight - 28) / 1080);
      const st = document.getElementById('stage'); st.style.transformOrigin = '0 0'; st.style.transform = `scale(${s})`; };
    addEventListener('resize', fit); fit();
    if (qs.has('safe')) document.getElementById('stage').classList.add('show-safe');
    bar.addEventListener('click', (e) => { const r = bar.getBoundingClientRect(); t = duration * (e.clientX - r.left) / r.width; });
    addEventListener('keydown', (e) => {
      if (e.code === 'Space') playing = !playing;
      if (e.code === 'ArrowRight') { playing = false; t = Math.min(duration, t + 1 / 30); }
      if (e.code === 'ArrowLeft') { playing = false; t = Math.max(0, t - 1 / 30); }
      if (e.key === 'g') document.getElementById('stage').classList.toggle('show-safe');
    });
    const loop = (now) => {
      if (last !== null && playing) t = (t + (now - last) / 1000) % duration;
      last = now; seek(t); tl.textContent = t.toFixed(2); fill.style.width = (100 * t / duration) + '%';
      realRAF(loop);
    };
    realRAF(loop);
  }

  window.addEventListener('error', (e) => { window.__SCENE_ERROR__ = String(e.message || e); });
  window.addEventListener('unhandledrejection', (e) => { window.__SCENE_ERROR__ = String(e.reason); });
  window.Scene = Scene;
})();
