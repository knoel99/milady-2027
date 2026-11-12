// Figure: experimental protocol (team claude, E4). Content only from site/teams/claude/figures/FACTS.md.
// Hero: none, a protocol diagram (boxes, axis, dumbbell and set schematics); flat route, no 3D part.
export const figure = { width: 183, height: 101, name: 'protocol', format: 'journal' };

export default function draw(F, L) {
  const C = L.STYLE.color;
  const U = C.blue, B = C.vermillion;                 // colour key: velocity u blue, magnetic field B orange/red
  const TR = '#009E73', VA = '#B39500', TE = '#8E3FA8'; // training, validation, held-out test
  const INK = C.ink, MID = C.mid;
  const tint = (h, a) => L.shade(h, a);

  // ---------------------------------------------------------------- a: hypothesis loop
  const a = F.panel('a', { x: 0, y: 0, w: 62, h: 52 });
  L.text(a, 11, 6, 'Hypothesis loop', { size: 6, weight: 'bold', valign: 'middle' });
  const bx = 14, bw = 136;
  L.box(a, bx, 16, bw, 34, '', { fill: C.tintGrey, stroke: MID });
  L.text(a, bx + bw / 2, 27, 'Hypothesis +\nrefutation criterion', { anchor: 'middle', valign: 'middle', size: 6, lineGap: 1 });
  L.text(a, bx + bw / 2, 43, '*written before the computation*', { anchor: 'middle', valign: 'middle', size: 5, color: INK });
  L.box(a, bx, 64, bw, 28, 'Computation: 5 seeds,\nheld-out η', { fill: C.tintGrey, stroke: MID, size: 6 });
  L.box(a, bx, 106, bw, 20, 'Supervisor’s verdict', { fill: C.tintGrey, stroke: MID, size: 6 });
  L.arrow(a, [bx + bw / 2, 50], [bx + bw / 2, 64], { stroke: INK, gap1: 0.6 });
  L.arrow(a, [bx + bw / 2, 92], [bx + bw / 2, 106], { stroke: INK, gap1: 0.6 });
  // return to the next hypothesis
  L.arrow(a, [bx + bw, 116], [bx + bw, 33], { via: [[bx + bw + 14, 116], [bx + bw + 14, 33]], stroke: MID, dash: '2 1.4', radius: 4, gap1: 0.6 });
  // three verdicts
  const chips = [['Confirmed', 44], ['Refuted', 40], ['Not discriminating', 68]];
  let cx = 8;
  for (const [t, w] of chips) {
    L.box(a, cx, 134, w, 14, t, { fill: '#fff', stroke: INK, size: 5.5, r: 3 });
    L.line(a, [cx + w / 2, 126], [cx + w / 2, 134], { stroke: MID, width: 0.4 });
    cx += w + 5;
  }

  // ---------------------------------------------------------------- b: eta axis and splits
  const b = F.panel('b', { x: 66, y: 0, w: 117, h: 52 });
  L.text(b, 11, 6, 'Eleven values of η, three roles', { size: 6, weight: 'bold', valign: 'middle' });
  const x0 = 110, dx = 20.2, X = (i) => x0 + i * dx, yAx = 34;
  const split = ['tr', 'te', 'tr', 'va', 'tr', 'te', 'tr', 'va', 'tr', 'te', 'tr'];
  const col = { tr: TR, va: VA, te: TE };
  const lanes = [['tr', 'Training (6)', 'fits the generator', 62], ['va', 'Validation (2)', 'chooses the model', 88], ['te', 'Held-out test (3)', 'judges the model', 114]];
  for (const [k, , , y] of lanes) L.rect(b, 0, y - 11, 331, 22, { fill: tint(col[k], 0.88), r: 2 });
  for (let i = 0; i < 11; i++) L.line(b, [X(i), yAx + 3], [X(i), 114], { stroke: C.light, width: 0.3, dash: '0.8 1.4' });
  L.line(b, [X(0) - 8, yAx], [X(10) + 8, yAx], { stroke: INK, width: 0.7 });
  const mark = (p, k, x, y, r = 4) => {
    if (k === 'tr') L.circle(p, x, y, r, { fill: col.tr, stroke: L.shade(col.tr, -0.4), width: 0.4 });
    else if (k === 'va') L.rect(p, x - r, y - r, 2 * r, 2 * r, { fill: col.va, stroke: L.shade(col.va, -0.4), width: 0.4 });
    else L.polygon(p, [[x, y - r * 1.3], [x + r * 1.3, y], [x, y + r * 1.3], [x - r * 1.3, y]], { fill: col.te, stroke: L.shade(col.te, -0.4), width: 0.4 });
  };
  for (let i = 0; i < 11; i++) {
    mark(b, split[i], X(i), yAx);
    L.text(b, X(i), yAx - 11, String(i), { anchor: 'middle', valign: 'middle', size: 6 });
  }
  L.text(b, x0 - 16, yAx - 11, 'index', { anchor: 'end', valign: 'middle', size: 5.5, color: MID });
  L.text(b, X(0), yAx + 12, 'η = 0.08', { anchor: 'middle', valign: 'middle', size: 5.5 });
  L.text(b, X(10), yAx + 12, 'η = 0.03', { anchor: 'middle', valign: 'middle', size: 5.5 });
  L.text(b, (X(0) + X(10)) / 2, yAx + 12, 'log-spaced', { anchor: 'middle', valign: 'middle', size: 5.5, color: MID, italic: true });
  for (const [k, name, role, y] of lanes) {
    L.text(b, 6, y - 3.5, name, { size: 6, weight: 'bold', valign: 'middle', color: L.shade(col[k], -0.3) });
    L.text(b, 6, y + 5.5, role, { size: 5.5, valign: 'middle' });
    split.forEach((s, i) => { if (s === k) mark(b, k, X(i), y); });
  }
  L.rect(b, 0, 128, 331, 18, { fill: '#fff', stroke: MID, width: 0.4, r: 2 });
  L.text(b, 165, 137, 'At every η: 24 trajectories × 100 snapshots of ({#0072B2|**u**}, {#D55E00|**B**})', { anchor: 'middle', valign: 'middle', size: 6 });

  // ---------------------------------------------------------------- c: five seeds, paired difference
  const c = F.panel('c', { x: 0, y: 56, w: 88, h: 48 });
  L.text(c, 11, 6, 'Five seeds, paired comparison', { size: 6, weight: 'bold', valign: 'middle' });
  const Av = [46, 62, 40, 70, 54], Bv = [88, 104, 76, 108, 92];   // schematic positions, not data
  const ya = (s) => 36 + s * 14;
  L.line(c, [30, 28], [30, 100], { stroke: C.light, width: 0.3, dash: '0.8 1.4' });
  for (let s = 0; s < 5; s++) {
    L.text(c, 24, ya(s), String(s + 1), { anchor: 'end', valign: 'middle', size: 5.5, color: MID });
    L.line(c, [30 + Av[s], ya(s)], [30 + Bv[s], ya(s)], { stroke: MID, width: 0.6 });
    L.circle(c, 30 + Av[s], ya(s), 3, { fill: '#fff', stroke: INK, width: 0.8 });
    L.circle(c, 30 + Bv[s], ya(s), 3, { fill: INK, stroke: INK, width: 0.5 });
  }
  L.text(c, 24, 24, 'seed', { anchor: 'end', valign: 'middle', size: 5.5, color: MID });
  L.circle(c, 52, 24, 2.6, { fill: '#fff', stroke: INK, width: 0.8 });
  L.text(c, 57, 24, 'variant A', { valign: 'middle', size: 5.5 });
  L.circle(c, 96, 24, 2.6, { fill: INK, stroke: INK, width: 0.5 });
  L.text(c, 101, 24, 'variant B', { valign: 'middle', size: 5.5 });
  // differences
  const zx = 160;
  L.line(c, [zx, 28], [zx, 100], { stroke: INK, width: 0.6 });
  L.text(c, zx, 24, 'paired difference B − A', { anchor: 'middle', valign: 'middle', size: 5.5 });
  for (let s = 0; s < 5; s++) {
    const d = (Bv[s] - Av[s]) * 1.35 / 1.0 - 20;
    L.line(c, [zx, ya(s)], [zx + d * 0.0 + (Bv[s] - Av[s]) * 0.9, ya(s)], { stroke: C.light, width: 0.4 });
    L.circle(c, zx + (Bv[s] - Av[s]) * 0.9, ya(s), 2.6, { fill: INK });
  }
  const mean = (Bv.reduce((u, v, i) => u + v - Av[i], 0) / 5) * 0.9;
  const my = ya(4) + 14;
  L.line(c, [zx + mean - 12, my], [zx + mean + 12, my], { stroke: INK, width: 0.9 });
  L.line(c, [zx + mean - 12, my - 2.5], [zx + mean - 12, my + 2.5], { stroke: INK, width: 0.9 });
  L.line(c, [zx + mean + 12, my - 2.5], [zx + mean + 12, my + 2.5], { stroke: INK, width: 0.9 });
  L.circle(c, zx + mean, my, 3, { fill: '#fff', stroke: INK, width: 1 });
  L.text(c, zx + mean + 18, my, 'mean ± standard\nerror', { valign: 'middle', size: 5.5, lineGap: 1 });

  // ---------------------------------------------------------------- d: noise floor
  const d = F.panel('d', { x: 92, y: 56, w: 91, h: 48 });
  L.text(d, 11, 6, 'Noise floor of the reference', { size: 6, weight: 'bold', valign: 'middle' });
  // 24 trajectories, two disjoint halves (one row each)
  const gx = 8, tw = 6.4, rows = [[22, 'half 1', MID], [48, 'half 2', C.light]];
  L.text(d, gx, 15, '24 reference trajectories, two disjoint halves', { valign: 'middle', size: 5.5 });
  const blob = (p, cx, cy, fill, seed) => {
    L.rect(p, cx - 22, cy - 9, 44, 18, { fill: '#fff', stroke: MID, width: 0.5, r: 2 });
    for (let k = 0; k < 26; k++) {
      const u = Math.sin(seed * 12.9898 + k * 78.233) * 43758.5453, v = Math.sin(seed * 4.1 + k * 19.7) * 12345.678;
      L.circle(p, cx - 19 + (u - Math.floor(u)) * 38, cy - 6 + (v - Math.floor(v)) * 12, 0.9, { fill });
    }
  };
  const sx = 104;
  rows.forEach(([y, nm, fill], r) => {
    for (let i = 0; i < 12; i++) L.rect(d, gx + i * tw, y, tw - 1, 16, { fill, stroke: fill === C.light ? MID : 'none', width: 0.3 });
    L.text(d, gx + 6 * tw, y + 22, nm, { anchor: 'middle', valign: 'middle', size: 5.5, color: MID });
    L.arrow(d, [gx + 12 * tw + 2, y + 8], [sx - 1, y + 8], { stroke: INK, gap1: 0.6, width: 0.5 });
    blob(d, sx + 22, y + 8, MID, r + 1);
    L.text(d, sx + 48, y + 8, '512 snapshots', { valign: 'middle', size: 5.5 });
  });
  L.arrow(d, [226, 32], [226, 54], { both: true, stroke: INK, width: 0.6, head: 2.2 });
  L.text(d, 231, 43, 'noise\nfloor', { valign: 'middle', size: 5.5, weight: 'bold', lineGap: 1 });
  L.text(d, 8, 80, 'noise floor = energy distance between the two subsamples', { valign: 'middle', size: 5.5 });
  // ratio axis
  const ay = 100, ax0 = 14, ax1 = 232;
  L.arrow(d, [ax0, ay], [ax1, ay], { stroke: INK, width: 0.7 });
  L.line(d, [ax0 + 10, ay - 3], [ax0 + 10, ay + 3], { stroke: INK, width: 0.7 });
  L.text(d, ax0 + 10, ay + 9, '1 (floor)', { anchor: 'middle', valign: 'middle', size: 5.5 });
  L.text(d, ax1, ay + 9, 'energy distance to the reference / floor', { anchor: 'end', valign: 'middle', size: 5.5 });
  L.circle(d, ax1 - 60, ay, 3, { fill: INK });
  L.text(d, ax1 - 60, ay - 9, 'generator', { anchor: 'middle', valign: 'middle', size: 5.5 });
}
