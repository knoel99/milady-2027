/* ch11_kit.js: helpers shared by the scenes of unit ch11 (labels and fades, copied from ch09_kit.js) (labels with entrance/exit, faded groups,
   series lookup, on-screen text taken from the script). Pure functions of t; elements built in setup only.
   Nothing here duplicates a kit component; candidates for promotion are listed in script/_review/scenes_ch11.md. */
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
