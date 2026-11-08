/* scene.js: deterministic scene runtime (prototype).
 *
 * Every scene HTML includes this file first, then calls Scene.define({...}).
 * Contract exposed to the recorder (capture.js) and to humans:
 *   window.DURATION      scene length in seconds (from the timeline entry, else the scene default)
 *   window.READY         true once fonts, data and setup() are done
 *   window.seek(t)       renders the frame at time t (seconds) and resolves when it is on screen;
 *                        window.__seek is an alias
 *   window.__ENTRY__     optional, injected by the recorder: {duration, cues, status, data, params, seed}
 *   window.__CAPTURE__   true when recorded: real clocks are frozen and replaced by virtual time
 *
 * Determinism rules enforced or helped here:
 *   - Date.now, performance.now and requestAnimationFrame follow the virtual clock in capture mode;
 *     queued rAF callbacks are flushed once per seek, with the virtual timestamp.
 *   - Math.random is replaced by a seeded generator (mulberry32) in all modes.
 *   - Web Animations (CSS animations/transitions included) are paused and set to currentTime = t.
 *   - Scene.stepper() integrates any state machine with a fixed dt and an integer step count, so a
 *     frame at time t is identical whatever the fps, the worker split or the seek order.
 */
(function () {
  'use strict';
  const CAPTURE = !!window.__CAPTURE__ || new URLSearchParams(location.search).has('capture');
  const qs = new URLSearchParams(location.search);

  // ---------- seeded randomness ----------
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  const entry = window.__ENTRY__ || (qs.get('entry') ? JSON.parse(qs.get('entry')) : {});
  Math.random = mulberry32(entry.seed ?? 12345);

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
    inOutSine: (p) => -(Math.cos(Math.PI * p) - 1) / 2,
    smooth: (p) => p * p * (3 - 2 * p),
  };
  /** progress of t inside [a, b], eased, clamped to [0, 1] */
  const seg = (t, a, b, e = ease.inOutCubic) => e(clamp((t - a) / Math.max(1e-9, b - a)));
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

  async function loadData(spec) {
    const out = {}, missing = [];
    const overrides = entry.data || {};
    for (const [name, url0] of Object.entries(spec || {})) {
      const url = overrides[name] || url0;
      try {
        const r = await fetch(url, { cache: 'no-store' });
        if (!r.ok) throw new Error(r.status + ' ' + url);
        if (/\.(f32|bin)$/.test(url)) out[name] = new Float32Array(await r.arrayBuffer());
        else out[name] = await r.json();
      } catch (e) { out[name] = null; missing.push(name + ' (' + url + ')'); }
    }
    return { data: out, missing };
  }

  let readyResolve, readyReject;
  const readyP = new Promise((res, rej) => { readyResolve = res; readyReject = rej; });
  readyP.catch(() => {});
  let current = null;   // {spec, ctx}
  window.READY = false;

  const Scene = {
    C: { bg: '#0B0F14', panel: '#10151C', grid: '#1A222D', fg: '#F2F4F7', fg2: '#C7D0DA', muted: '#9AA6B2', chalk: '#E8E4D8',
         param: '#1BAF7A', u: '#3987E5', b: '#EB6834', model: '#B49CF0', metric: '#EDA100', infra: '#6B7A8C' },
    W: 1920, H: 1080, CAPTURE, clamp, lerp, ease, seg, stepper, mulberry32,
    get time() { return vt; },
    /** 2D context whose backing store follows devicePixelRatio (crisp at 4K = deviceScaleFactor 2), drawn in CSS px */
    hidpi(canvas, w = 1920, h = 1080) {
      const d = window.devicePixelRatio || 1;
      canvas.width = Math.round(w * d); canvas.height = Math.round(h * d);
      const g = canvas.getContext('2d'); g.setTransform(d, 0, 0, d, 0, 0); return g;
    },

    async define(spec) {
      try { await defineImpl(spec); }
      catch (e) { window.__SCENE_ERROR__ = String(e && e.message || e); readyReject(e); }
    },
  };

  async function defineImpl(spec) {
      const stage = document.getElementById('stage');
      const duration = entry.duration ?? (qs.get('dur') ? +qs.get('dur') : spec.duration);
      const cues = Object.assign({}, spec.cues || {}, entry.cues || {});
      const status = entry.status || spec.status || 'ready';
      window.DURATION = duration;
      const { data, missing } = await loadData(spec.data);
      if (missing.length && spec.requireData !== false) {
        const msg = 'missing data: ' + missing.join(', ');
        window.__SCENE_ERROR__ = msg; throw new Error(msg);
      }
      // fonts: wait for every face declared in CSS that the scene asks for, then for the whole set
      await Promise.all((spec.fonts || ['500 30px Inter', '600 30px Inter', '500 20px "JetBrains Mono"'])
        .map((f) => document.fonts.load(f)));
      await document.fonts.ready;
      const ctx = {
        stage, data, missing, cues, status, duration, params: Object.assign({}, spec.params || {}, entry.params || {}),
        /** time of a named cue, with a fallback when the timeline does not provide it */
        cue: (name, fallback) => (name in cues ? cues[name] : fallback),
      };
      if (status === 'provisional') {
        const s = document.createElement('div'); s.id = '__stamp';
        s.textContent = 'PROVISIONAL DATA' + (entry.stamp ? ' · ' + entry.stamp : '');
        stage.appendChild(s);
      }
      if (spec.setup) await spec.setup(ctx);
      current = { spec, ctx };
      window.READY = true; readyResolve();
      if (!CAPTURE) startPreview(duration);
  }

  async function seek(t) {
    await readyP;
    vt = t;
    const { spec, ctx } = current;
    for (const a of document.getAnimations()) { a.pause(); a.currentTime = t * 1000; }
    spec.render(t, ctx);
    if (rafQueue.length) { const q = rafQueue; rafQueue = []; q.forEach((cb) => cb(t * 1000)); }
    if (spec.afterRender) await spec.afterRender(t, ctx);
    return t;
  }
  window.seek = window.__seek = seek;

  // ---------- preview mode (a normal browser tab): real-time loop with a scrub bar ----------
  function startPreview(duration) {
    const hud = document.createElement('div'); hud.id = '__hud';
    hud.innerHTML = '<span id="__t">0.00</span><div class="bar"><i></i></div><span>space: pause · ←/→: frame</span>';
    document.body.appendChild(hud);
    const bar = hud.querySelector('.bar'), fill = bar.querySelector('i'), tl = hud.querySelector('#__t');
    let playing = true, t = 0, last = null;
    // scale the 1920x1080 stage to the window
    const fit = () => { const s = Math.min(innerWidth / 1920, (innerHeight - 28) / 1080);
      const st = document.getElementById('stage'); st.style.transformOrigin = '0 0'; st.style.transform = `scale(${s})`; };
    addEventListener('resize', fit); fit();
    bar.addEventListener('click', (e) => { const r = bar.getBoundingClientRect(); t = duration * (e.clientX - r.left) / r.width; });
    addEventListener('keydown', (e) => {
      if (e.code === 'Space') playing = !playing;
      if (e.code === 'ArrowRight') { playing = false; t = Math.min(duration, t + 1 / 30); }
      if (e.code === 'ArrowLeft') { playing = false; t = Math.max(0, t - 1 / 30); }
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
