// Hero: none, a set of small metric panels (schematic curves and bars); drawn flat with library primitives.
export const figure = { width: 183, height: 86, name: 'metrics' };

export default function draw(F, L) {
  const C = L.STYLE.color;
  // colour key shared with the sibling figures: u blue, B vermillion, forcing grey, generated/measured green; reference = dark ink
  const U = '#0072B2', B = '#D55E00', FC = '#6E6E6E', G = '#009E73', INK = '#2b2b2b';
  const W = 43.5, H = 41, gx = 3, gy = 3;
  const cell = (i, letter, title, sub) => {
    const col = i % 4, row = Math.floor(i / 4);
    const p = F.panel(letter, { x: col * (W + gx), y: row * (H + gy), w: W, h: H });
    L.text(p, 12, 8, `**${title}**`, { size: 6.5, anchor: 'start' });
    if (sub) L.text(p, 12, 17, sub, { size: 5, anchor: 'start', color: C.mid });
    return p;
  };
  const axis = (p, x0, y0, x1, y1) => {
    L.arrow(p, [x0, y0], [x1, y0], { stroke: INK, width: 0.5, head: 2.2 });
    if (y1 !== undefined) L.arrow(p, [x0, y0], [x0, y1], { stroke: INK, width: 0.5, head: 2.2 });
  };
  const dot = (p, x, y, ens, r = 2.4) => L.circle(p, x, y, r, { fill: ens === 'gen' ? G : INK, stroke: 'none' });
  const bar = (p, x, y0, h, w, ens, fill) => L.rect(p, x, h >= 0 ? y0 - h : y0, w, Math.abs(h), { fill: fill ?? C.paper, stroke: ens === 'gen' ? G : INK, width: 1 });

  // a: what is compared (key)
  const a = cell(0, 'a', 'Compared ensembles', 'held-out η');
  dot(a, 20, 40, 'gen', 3); L.text(a, 28, 40, '**Generated** snapshots', { size: 7, anchor: 'start', valign: 'middle', color: G });
  dot(a, 20, 56, 'ref', 3); L.text(a, 28, 56, '**Reference** snapshots', { size: 7, anchor: 'start', valign: 'middle', color: INK });
  L.text(a, 28, 66, 'from the solver', { size: 5, anchor: 'start', valign: 'middle', color: C.mid });
  [[U, 'velocity *u*'], [B, 'field *B*'], [FC, 'forcing *f*']].forEach(([c, s], i) => {
    L.rect(a, 14, 78 + i * 12, 7, 6, { fill: c, stroke: 'none' });
    L.text(a, 25, 81 + i * 12, s, { size: 6, anchor: 'start', valign: 'middle', color: c });
  });

  // b: energy distance over noise floor
  const b = cell(1, 'b', 'Energy distance', 'distance to reference / noise floor');
  L.rect(b, 27, 42, 14, 34, { fill: '#e6e6e6', stroke: 'none' });
  axis(b, 14, 74, 112);
  L.line(b, [34, 70], [34, 78], { stroke: INK, width: 0.5 });
  L.text(b, 34, 80, '1', { size: 6, anchor: 'middle', valign: 'top' });
  dot(b, 34, 54, 'ref'); L.text(b, 34, 41, 'two reference\nsubsamples', { size: 5, anchor: 'middle', valign: 'bottom', color: INK });
  L.line(b, [34, 57], [34, 70], { stroke: INK, width: 0.5, dash: '1.4 1.2' });
  dot(b, 92, 54, 'gen'); L.text(b, 92, 41, 'generated\nvs reference', { size: 5, anchor: 'middle', valign: 'bottom', color: G });
  L.line(b, [92, 57], [92, 70], { stroke: G, width: 0.5, dash: '1.4 1.2' });
  L.arrow(b, [44, 54], [88, 54], { stroke: C.mid, width: 0.5, head: 2.2 });
  L.text(b, 66, 62, 'ratio', { size: 5, anchor: 'middle', color: C.mid });
  L.text(b, 12, 92, '**floor** (grey band): mean of 10 splits of the', { size: 5, anchor: 'start', color: C.mid });
  L.text(b, 12, 98, 'reference trajectories into two halves', { size: 5, anchor: 'start', color: C.mid });
  L.text(b, 12, 106, 'a perfect generator would score about 0.6, not 1', { size: 5, anchor: 'start', color: INK });

  // c: divergence of B
  const c = cell(2, 'c', 'Divergence of B', '‖∇·B‖ / ‖∇B‖');
  [[36, 46, 20, 14], [86, 46, 20, 14]].forEach(([cx, cy, rx, ry], i) => {
    const pts = Array.from({ length: 61 }, (_, k) => { const t = k / 60 * 2 * Math.PI; return [cx + rx * Math.cos(t), cy + ry * Math.sin(t)]; });
    L.polyline(c, pts, { stroke: B, width: 1, fill: 'none' });
    L.chevron(c, [cx + rx, cy], [0, -1], { len: 3, stroke: B, width: 1 });
  });
  L.text(c, 60, 72, 'closed field lines', { size: 5, anchor: 'middle', color: B });
  axis(c, 14, 98, 112);
  L.line(c, [24, 94], [24, 102], { stroke: INK, width: 0.5 });
  L.text(c, 24, 107, '0', { size: 6, anchor: 'middle', valign: 'top' });
  dot(c, 76, 98 - 0, 'gen', 0.01); L.circle(c, 76, 90, 2.4, { fill: G, stroke: 'none' });
  L.arrow(c, [72, 90], [28, 90], { stroke: G, width: 0.8, head: 2.4 });

  // d: mean energy balance
  const d = cell(3, 'd', 'Energy balance', '{#6E6E6E|injection} vs {#0072B2|ν} + {#D55E00|η} dissipation');
  const base = 92;
  [['ref', 16, 44, 44], ['gen', 68, 44, 36]].forEach(([e, x, hi, hd]) => {
    bar(d, x, base, hi, 12, e, FC);
    bar(d, x + 15, base, hd * 0.55, 12, e, U);
    bar(d, x + 15, base - hd * 0.55, hd * 0.45, 12, e, B);
    L.text(d, x + 13.5, base + 7, e === 'ref' ? 'ref.' : 'gen.', { size: 5, anchor: 'middle', valign: 'top', color: e === 'ref' ? INK : G });
  });
  L.line(d, [12, base], [114, base], { stroke: INK, width: 0.5 });

  // e: spectrum and helicity
  const e = cell(4, 'e', 'Spectrum, helicity', '*E*_{B}(*k*) and mean *H*_{M}');
  axis(e, 14, 92, 76, 26);
  for (let k = 0; k < 8; k++) {
    const x = 20 + k * 8, yr = 36 + 44 * Math.log(1 + k) / Math.log(8), yg = yr + [-2, 3, 2, -3, 3, 4, -2, 3][k];
    if (k) { L.line(e, [x - 8, 36 + 44 * Math.log(k) / Math.log(8)], [x, yr], { stroke: INK, width: 0.7 }); }
    dot(e, x, yr, 'ref', 1.6);
    dot(e, x + 0.01, yg, 'gen', 1.6);
  }
  L.text(e, 20, 100, '1', { size: 5, anchor: 'middle' }); L.text(e, 76, 100, '8', { size: 5, anchor: 'middle' });
  L.text(e, 48, 106, '*k*', { size: 5, anchor: 'middle' });
  L.line(e, [86, 54], [116, 54], { stroke: INK, width: 0.5 });
  bar(e, 91, 54, -18, 8, 'ref'); bar(e, 103, 54, -22, 8, 'gen');
  L.text(e, 101, 90, '*H*_{M}', { size: 6, anchor: 'middle', valign: 'top' });

  // f: magnetic null points
  const f = cell(5, 'f', 'Null points', 'mean count of *B* = 0');
  [[1, 0.5], [1, -0.5], [-1, 0.5], [-1, -0.5]].forEach(([sx, sy]) => {
    const pts = Array.from({ length: 21 }, (_, k) => { const t = 0.15 + k / 20 * 1.1; return [34 + sx * 22 * t, 52 + sy * 24 * t * t]; });
    L.polyline(f, pts, { stroke: B, width: 1, fill: 'none' });
  });
  L.line(f, [14, 52], [54, 52], { stroke: B, width: 0.5, dash: '1.2 1.2', opacity: 0.5 });
  L.circle(f, 34, 52, 2.2, { fill: C.paper, stroke: INK, width: 1 });
  L.text(f, 34, 78, '*B* = 0', { size: 5, anchor: 'middle', valign: 'top', color: B });
  L.line(f, [66, 92], [116, 92], { stroke: INK, width: 0.5 });
  bar(f, 72, 92, 38, 14, 'ref'); bar(f, 94, 92, 46, 14, 'gen');
  L.text(f, 79, 98, 'ref.', { size: 5, anchor: 'middle', valign: 'top', color: INK });
  L.text(f, 101, 98, 'gen.', { size: 5, anchor: 'middle', valign: 'top', color: G });

  // g: restart drift
  const g = cell(6, 'g', 'Restart drift', 'solver advances snapshots by τ = 4');
  axis(g, 14, 92, 112, 26);
  L.line(g, [22, 88], [22, 96], { stroke: INK, width: 0.5 });
  L.line(g, [96, 88], [96, 96], { stroke: INK, width: 0.5 });
  L.text(g, 22, 100, '0', { size: 5, anchor: 'middle', valign: 'top' }); L.text(g, 96, 100, 'τ', { size: 5, anchor: 'middle', valign: 'top' });
  L.text(g, 60, 108, 'time', { size: 5, anchor: 'middle', valign: 'top' });
  L.text(g, 12, 24, 'mean *E*_{B}', { size: 5, anchor: 'start', color: B });
  L.line(g, [22, 56], [96, 56], { stroke: INK, width: 1 });
  L.line(g, [22, 48], [96, 72], { stroke: G, width: 1 });
  dot(g, 22, 56, 'ref', 1.8); dot(g, 22.01, 48, 'gen', 1.8);
  dot(g, 96, 56, 'ref', 1.8); dot(g, 96.01, 72, 'gen', 1.8);
  L.bracket(g, [102, 48], [102, 72], { side: 'right', depth: 2.5 });
  L.text(g, 108, 60, 'drift', { size: 5, anchor: 'start', valign: 'middle', color: G });

  // h: polarity symmetry
  const h = cell(7, 'h', 'Polarity symmetry', '|P(⟨*u*·*B*⟩ > 0) − ½|');
  L.arrow(h, [14, 34], [40, 34], { stroke: B, width: 1.2, head: 3 });
  L.arrow(h, [112, 34], [86, 34], { stroke: B, width: 1.2, head: 3 });
  L.text(h, 27, 28, '*B*', { size: 6, anchor: 'middle', color: B }); L.text(h, 99, 28, '−*B*', { size: 6, anchor: 'middle', color: B });
  L.text(h, 63, 34, '↔', { size: 8, anchor: 'middle', valign: 'middle' });
  const yb = 96;
  L.line(h, [12, yb], [114, yb], { stroke: INK, width: 0.5 });
  bar(h, 16, yb, 30, 12, 'ref'); bar(h, 31, yb, 30, 12, 'ref');
  bar(h, 66, yb, 38, 12, 'gen'); bar(h, 81, yb, 22, 12, 'gen');
  L.line(h, [12, yb - 30], [114, yb - 30], { stroke: C.mid, width: 0.5, dash: '1.4 1.2' });
  L.text(h, 114, yb - 33, '½', { size: 5, anchor: 'end', valign: 'bottom', color: C.mid });
  L.text(h, 22, yb + 6, '>0', { size: 5, anchor: 'middle', valign: 'top' }); L.text(h, 37, yb + 6, '<0', { size: 5, anchor: 'middle', valign: 'top' });
  L.text(h, 72, yb + 6, '>0', { size: 5, anchor: 'middle', valign: 'top' }); L.text(h, 87, yb + 6, '<0', { size: 5, anchor: 'middle', valign: 'top' });
  L.text(h, 29, yb + 14, 'ref.', { size: 5, anchor: 'middle', valign: 'top', color: INK }); L.text(h, 79, yb + 14, 'gen.', { size: 5, anchor: 'middle', valign: 'top', color: G });
}
