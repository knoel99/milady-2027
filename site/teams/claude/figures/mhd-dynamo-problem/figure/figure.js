// Hero: none, a parametric-problem schematic (box, parameter axis, equations); drawn flat with L.wireBox3 and library primitives.
export const figure = { width: 183, height: 100, name: 'mhd-dynamo-problem' };

export default function draw(F, L) {
  const C = L.STYLE.color;
  // colour key shared with the sibling figures: u blue, B vermillion, forcing grey, generated/measured green
  const U = '#0072B2', B = '#D55E00', FC = '#6E6E6E', G = '#009E73', INK = C.ink;
  const cu = (s) => `{#0072B2|${s}}`, cb = (s) => `{#D55E00|${s}}`, cf = (s) => `{#6E6E6E|${s}}`;

  // ================= a: periodic box =================
  const a = F.panel('a', { x: 0, y: 0, w: 64, h: 63 });
  L.text(a, 12, 8, '**Forced flow and field**', { size: 7, anchor: 'start' });
  const S = 92;
  const P = L.obliqueProj({ preset: 'cabinet', depth: 0.5, origin: [44, 152] });
  L.wireBox3(a, P, [S, S, S], { pos: [0, 0, 0], stroke: C.mid, width: 0.6 });
  const arrowEnd = (pts, col, w) => {
    const p1 = pts[pts.length - 2], p2 = pts[pts.length - 1];
    const dx = p2[0] - p1[0], dy = p2[1] - p1[1], l = Math.hypot(dx, dy);
    L.chevron(a, p2, [dx / l, dy / l], { len: 3.4, stroke: col, width: w });
  };
  // magnetic field: one large loop in the plane y = 0.72 S (k = 1: one period across the box)
  const yb = 0.74 * S, loop = [];
  for (let i = 0; i <= 60; i++) {
    const t = (i / 60) * 2 * Math.PI;
    loop.push(P(0.5 * S + 0.40 * S * Math.cos(t), yb, 0.5 * S + 0.33 * S * Math.sin(t)));
  }
  L.polyline(a, loop, { stroke: B, width: 1.2, fill: 'none' });
  arrowEnd([loop[44], loop[45]], B, 1.2);
  const loop2 = [];
  for (let i = 0; i <= 60; i++) {
    const t = (i / 60) * 2 * Math.PI;
    loop2.push(P(0.5 * S + 0.24 * S * Math.cos(t), yb, 0.5 * S + 0.18 * S * Math.sin(t)));
  }
  L.polyline(a, loop2, { stroke: B, width: 0.8, fill: 'none', opacity: 0.8 });
  arrowEnd([loop2[44], loop2[45]], B, 0.8);
  // helices along z with two turns: forcing (grey, left) and flow (blue, right), front plane y = 0.3 S
  const helix = (cx, cy, r, ph) => {
    const pts = [];
    for (let i = 0; i <= 80; i++) {
      const z = 0.06 * S + 0.88 * S * i / 80, th = ph + 2 * 2 * Math.PI * (i / 80);
      pts.push(P(cx + r * Math.cos(th), cy + r * Math.sin(th), z));
    }
    return pts;
  };
  const hf = helix(0.2 * S, 0.3 * S, 0.11 * S, 0);
  L.polyline(a, hf, { stroke: FC, width: 1.4, fill: 'none' });
  arrowEnd(hf.slice(-2), FC, 1.4);
  const hu = helix(0.8 * S, 0.3 * S, 0.12 * S, 1.0);
  L.polyline(a, hu, { stroke: U, width: 1.4, fill: 'none' });
  arrowEnd(hu.slice(-2), U, 1.4);
  // labels
  const lab = (pt, at, str, col, anchor) => L.callout(a, pt, at, str, { anchor, size: 6, halo: true });
  const top = (h) => P(0.2 * S, 0.3 * S, 0.06 * S + 0.88 * S * h);
  L.text(a, 2, 96, 'Forcing\n*f*, *k*_{f} = 2', { size: 6, anchor: 'start', color: FC, valign: 'top' });
  L.arrow(a, [30, 94], P(0.2 * S - 0.11 * S, 0.3 * S, 0.45 * S), { stroke: FC, width: 0.5, head: 2 });
  L.text(a, 179, 128, 'Flow *u*', { size: 6, anchor: 'end', color: U, valign: 'top' });
  L.arrow(a, [160, 128], P(0.8 * S + 0.12 * S, 0.3 * S, 0.3 * S), { stroke: U, width: 0.5, head: 2 });
  L.text(a, 179, 8, 'Large-scale *B*\n(*k* = 1)', { size: 6, anchor: 'end', color: B, valign: 'top' });
  L.arrow(a, [150, 26], P(0.5 * S + 0.40 * S * 0.86, yb, 0.5 * S + 0.33 * S * 0.5), { stroke: B, width: 0.5, head: 2 });
  L.text(a, 70, 164, '[0, 2π)³, periodic', { size: 6, anchor: 'middle', color: INK });

  // ================= b: parameter axis =================
  const b = F.panel('b', { x: 68, y: 0, w: 115, h: 63 });
  L.text(b, 12, 8, '**Control parameter η**', { size: 7, anchor: 'start' });
  L.text(b, 12, 17, 'stationary state at each η', { size: 5, anchor: 'start', italic: true, color: C.mid });
  const x0 = 62, x1 = 288, dx = (x1 - x0) / 10;
  const rows = [
    { y: 36, name: '{#0072B2|Kinetic energy *E*_{u}}', col: U, l: '0.48', r: '0.25', up: false, dash: null },
    { y: 70, name: '{#D55E00|Magnetic energy *E*_{B}}', col: B, l: '0.08', r: '0.17', up: true, dash: null },
    { y: 104, name: '{#D55E00|Magnetic helicity *H*_{M}}', col: B, l: '−0.044', r: '−0.10', up: false, dash: '2.4 1.4' },
  ];
  for (const r of rows) {
    L.rect(b, x0, r.y, x1 - x0, 20, { fill: C.tintGrey, stroke: 'none' });
    L.text(b, x0, r.y - 3, r.name, { size: 6, anchor: 'start' });
    const yl = r.up ? r.y + 16 : r.y + 4, yr = r.up ? r.y + 4 : r.y + 16;
    L.line(b, [x0, yl], [x1, yr], { stroke: r.col, width: 1.2, dash: r.dash ?? undefined });
    L.circle(b, x0, yl, 1.8, { fill: r.col, stroke: 'none' });
    L.circle(b, x1, yr, 1.8, { fill: r.col, stroke: 'none' });
    L.text(b, x0 - 4, yl, r.l, { size: 6, anchor: 'end', valign: 'middle', color: r.col });
    L.text(b, x1 + 4, yr, r.r, { size: 6, anchor: 'start', valign: 'middle', color: r.col });
  }
  // axis with the 11 values
  const ya = 140;
  const role = ['train', 'test', 'train', 'val', 'train', 'test', 'train', 'val', 'train', 'test', 'train'];
  L.arrow(b, [x0 - 52, ya], [x1 + 14, ya], { stroke: INK, width: 0.6, head: 2.6 });
  role.forEach((k, i) => {
    const x = x0 + i * dx;
    if (k === 'train') L.circle(b, x, ya, 2.5, { fill: INK, stroke: INK, width: 0.6 });
    else if (k === 'val') L.circle(b, x, ya, 2.5, { fill: C.light, stroke: INK, width: 0.8 });
    else L.circle(b, x, ya, 2.5, { fill: C.paper, stroke: INK, width: 1.1 });
  });
  const L0 = x1 - x0, xth = x0 - 0.227 * L0;
  L.line(b, [xth, ya - 8], [xth, ya + 8], { stroke: C.mid, width: 0.6, dash: '1.6 1.2' });
  L.text(b, xth - 2, ya + 13, 'Rm ≈ 5\n(exploratory)', { size: 5, anchor: 'start', valign: 'top', color: C.mid });
  L.text(b, x0, ya + 13, 'η = 0.08\nRm = 6.25', { size: 6, anchor: 'middle', valign: 'top' });
  L.text(b, x1, ya + 13, 'η = 0.03\nRm = 16.7', { size: 6, anchor: 'middle', valign: 'top' });
  L.text(b, (x0 + x1) / 2, ya - 6, '11 values, Rm = 1/(*k*_{f} η)', { size: 6, anchor: 'middle' });
  // legend
  const ly = 172;
  [['train', 'train (6)', 12], ['val', 'validation (2)', 82], ['test', 'held-out test (3)', 168]].forEach(([k, s, x]) => {
    if (k === 'train') L.circle(b, x, ly - 2, 2.5, { fill: INK, stroke: INK, width: 0.6 });
    else if (k === 'val') L.circle(b, x, ly - 2, 2.5, { fill: C.light, stroke: INK, width: 0.8 });
    else L.circle(b, x, ly - 2, 2.5, { fill: C.paper, stroke: INK, width: 1.1 });
    L.text(b, x + 5, ly, s, { size: 6, anchor: 'start' });
  });

  // ================= c: equations =================
  const c = F.panel('c', { x: 0, y: 67, w: 88, h: 33 });
  L.text(c, 12, 8, '**Governing equations**', { size: 7, anchor: 'start' });
  const eq = [
    `∂_{t}${cu('u')} = ${cu('u')} × ${cu('ω')} + ${cb('j')} × ${cb('B')} − ∇Π + ν∇²${cu('u')} + ${cf('f')}`,
    `∂_{t}${cb('B')} = ∇ × (${cu('u')} × ${cb('B')}) + η∇²${cb('B')}`,
    `∇·${cu('u')} = ∇·${cb('B')} = 0,   ${cu('ω')} = ∇×${cu('u')},   ${cb('j')} = ∇×${cb('B')}`,
  ];
  eq.forEach((s, i) => L.text(c, 12, 30 + i * 17, s, { size: 8.5, anchor: 'start' }));
  L.text(c, 12, 82, 'ν = 0.05 fixed (Re = 10)', { size: 6.5, anchor: 'start', color: C.mid });

  // ================= d: the task =================
  const d = F.panel('d', { x: 92, y: 67, w: 91, h: 33 });
  L.text(d, 12, 8, '**Generate (u, B) at unseen η**', { size: 7, anchor: 'start' });
  const tile = (x, y, col, ph, frame) => {
    const s = 30;
    L.rect(d, x, y, s, s, { fill: C.paper, stroke: frame, width: 1 });
    const g = d;
    for (let k = 0; k < 4; k++) {
      const pts = Array.from({ length: 41 }, (_, i) => { const t = i / 40; return [x + t * s, y + 5 + k * 6.7 + 2.2 * Math.sin(t * 9 + ph + k * 1.3)]; });
      L.polyline(g, pts, { stroke: col, width: 0.7, fill: 'none' });
    }
  };
  L.circle(d, 14, 37, 2.5, { fill: C.paper, stroke: INK, width: 1.1 });
  L.text(d, 14, 46, 'held-out\nη', { size: 6, anchor: 'middle', valign: 'top' });
  const gm = L.box(d, 28, 25, 38, 24, 'Generative\nmodel', { fill: C.tintGreen, stroke: G, r: 2 });
  L.arrow(d, [18, 37], [28, 37], { stroke: INK, width: 0.6, head: 2.4 });
  L.arrow(d, [66, 37], [75, 37], { stroke: G, width: 0.8, head: 2.4 });
  // generated pair (green frame) and reference pair (ink frame)
  tile(78, 22, U, 0.0, G); tile(112, 22, B, 1.6, G);
  L.text(d, 110, 60, 'Generated', { size: 6, anchor: 'middle', color: G });
  tile(168, 22, U, 0.5, INK); tile(202, 22, B, 2.0, INK);
  L.text(d, 200, 60, 'Reference (solver)', { size: 6, anchor: 'middle', color: INK });
  L.text(d, 155, 40, 'vs', { size: 6, anchor: 'middle', color: C.mid });
  void gm; void top; void lab;
}
