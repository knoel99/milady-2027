// Hero: none, a schematic of glyphs and labels; flat vector route (no 3D object to render)
// Figure 1: the generative pipeline. Content: site/teams/claude/figures/FACTS.md ("The generative pipeline").
export const figure = { width: 183, height: 55, name: 'generative-pipeline', format: 'journal' };

export default function draw(F, L) {
  const R = F.root;
  const U = '#0072B2', B = '#D55E00', INK = '#222222', GREY = '#8c8c8c', LG = '#c9c9c9', FR = '#b5b5b5';
  const W = L.mm(183);
  // deterministic gaussian-ish numbers
  let s = 7; const rnd = () => { s = (s * 16807) % 2147483647; return s / 2147483647; };
  const gauss = () => { let a = 0; for (let i = 0; i < 6; i++) a += rnd(); return (a - 3) * 1.4; };

  const bw = 74, gap = (W - 6 * bw - 10) / 5, x0 = 5;
  const top = 25, gh = 86;                       // glyph frame: y from top to top+gh
  const heads = ['Snapshots\n(u, B)', 'Fourier\nmodes', 'Vector\npotentials', 'Conditional\nflow matching', 'Sampling\nthe flow', 'Decoding\nby the curl'];
  const subs = [
    ['16³ grid'],
    ['|m_{i}| ≤ 5', '665 complex modes'],
    ['Craya–Herring basis', 'latent: 5320 reals'],
    ['noise → data, straight paths', 'conditioned on log η'],
    ['integrate the flow', 't = 0 → 1'],
    ['B = ∇ × A (u alike)', '∇·B = 0'],
  ];
  const bx = (i) => x0 + i * (bw + gap);
  const cy = top + gh / 2;

  for (let i = 0; i < 6; i++) {
    const x = bx(i), cx = x + bw / 2;
    L.rect(R, x, top, bw, gh, { fill: '#fafafa', stroke: FR, width: 0.5, r: 3 });
    L.text(R, cx, 13, heads[i], { size: 6.5, weight: 'bold', anchor: 'middle', valign: 'middle', lineGap: 1 });
    subs[i].forEach((t, j) => L.text(R, cx, top + gh + 8 + j * 7.5, t, { size: 5.5, anchor: 'middle', color: INK }));
    if (i < 5) L.arrow(R, [x + bw + 1.2, cy], [bx(i + 1) - 1.2, cy], { stroke: INK, width: 0.8, head: 3 });
  }

  // 1. two grids: B in front, u behind
  {
    const cx = bx(0) + bw / 2, g = (ox, oy, col, n = 5, sz = 34) => {
      L.rect(R, ox, oy, sz, sz, { fill: col, fillOpacity: 0.14, stroke: col, width: 0.8 });
      for (let k = 1; k < n; k++) {
        L.line(R, [ox + k * sz / n, oy], [ox + k * sz / n, oy + sz], { stroke: col, width: 0.3, opacity: 0.6 });
        L.line(R, [ox, oy + k * sz / n], [ox + sz, oy + k * sz / n], { stroke: col, width: 0.3, opacity: 0.6 });
      }
    };
    g(cx - 24, cy - 24, U); g(cx - 10, cy - 10, B);
    L.text(R, cx - 26, cy - 26, 'u', { size: 7, italic: true, color: U, weight: 'bold', anchor: 'end' });
    L.text(R, cx + 28, cy + 30, 'B', { size: 7, italic: true, color: B, weight: 'bold' });
  }
  // 2. Fourier lattice 11 x 11
  {
    const cx = bx(1) + bw / 2, sp = 4.6;
    for (let a = -5; a <= 5; a++) for (let b = -5; b <= 5; b++) {
      L.circle(R, cx + a * sp, cy + b * sp, a === 0 && b === 0 ? 1.4 : 1.0, { fill: a === 0 && b === 0 ? INK : GREY });
    }
    L.rect(R, cx - 5.8 * sp, cy - 5.8 * sp, 11.6 * sp, 11.6 * sp, { fill: 'none', stroke: INK, width: 0.5, dash: '2 1.4' });
    L.text(R, cx + 5.8 * sp + 1, cy + 5.8 * sp + 0.5, 'm', { size: 5.5, italic: true, anchor: 'end', valign: 'top', color: INK, halo: true });
  }
  // 3. Craya-Herring plane: k out of the plane, e1 e2 in the plane (B plane front, u plane behind)
  {
    const cx = bx(2) + bw / 2, plane = (ox, oy, col) => {
      L.polygon(R, [[ox - 26, oy + 6], [ox + 14, oy + 6], [ox + 26, oy - 12], [ox - 14, oy - 12]], { fill: col, fillOpacity: 0.14, stroke: col, width: 0.8 });
    };
    plane(cx - 4, cy + 8, U); plane(cx + 4, cy + 18, B);
    const o = [cx + 4, cy + 12];
    L.arrow(R, o, [o[0] + 20, o[1] + 0], { stroke: INK, width: 0.8, head: 2.6 });
    L.arrow(R, o, [o[0] + 8, o[1] - 12], { stroke: INK, width: 0.8, head: 2.6 });
    L.arrow(R, o, [o[0] - 2, o[1] - 36], { stroke: INK, width: 0.8, head: 2.6 });
    L.text(R, o[0] + 22, o[1] + 1, 'e_{1}', { size: 6, valign: 'middle', italic: true, halo: true });
    L.text(R, o[0] + 10, o[1] - 14, 'e_{2}', { size: 6, valign: 'bottom', italic: true, halo: true });
    L.text(R, o[0] + 3, o[1] - 36, '**k**', { size: 6.5, valign: 'middle' });
  }
  // 4. conditional flow matching
  {
    const x = bx(3), cxn = x + 17, cxd = x + bw - 16, my = cy - 8;
    const nz = [], dt = [];
    for (let k = 0; k < 6; k++) {
      nz.push([cxn + gauss() * 4.2, my + gauss() * 8]);
      const ang = -0.9 + k * 0.36;
      dt.push([cxd + 7 * Math.sin(ang * 1.6) , my + 17 * Math.sin(ang * 1.9 - 0.15) + (k % 2 ? 1.5 : -1.5)]);
    }
    L.ellipse(R, cxn, my, 11, 17, { fill: 'none', stroke: LG, width: 0.5, dash: '1.5 1.2' });
    nz.forEach((p, k) => L.line(R, p, dt[k], { stroke: GREY, width: 0.4, opacity: 0.8 }));
    nz.forEach((p) => L.circle(R, p[0], p[1], 1.5, { fill: LG, stroke: GREY, width: 0.4 }));
    dt.forEach((p) => L.circle(R, p[0], p[1], 1.5, { fill: INK }));
    L.text(R, cxn, my + 25, '*x*_{0}', { size: 6, anchor: 'middle' });
    L.text(R, cxd, my + 25, '*x*_{1}', { size: 6, anchor: 'middle' });
    // x_t on one path with its velocity
    const a = nz[2], b = dt[2], t = 0.5, xt = [a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])];
    L.circle(R, xt[0], xt[1], 2, { fill: '#fff', stroke: INK, width: 0.8 });
    L.arrow(R, xt, [xt[0] + 0.45 * (b[0] - a[0]), xt[1] + 0.45 * (b[1] - a[1])], { stroke: INK, width: 1, head: 2.6 });
    L.text(R, xt[0], xt[1] - 4, '*x*_{t}', { size: 5.5, anchor: 'middle', halo: true, valign: 'bottom' });
    L.rect(R, x + 10, top + gh - 21, bw - 20, 13, { fill: '#fff', stroke: INK, width: 0.6, r: 2 });
    L.text(R, x + bw / 2, top + gh - 14.5, '*v*_{θ}(*x*, *t*, *c*)', { size: 6, anchor: 'middle', valign: 'middle' });
  }
  // 5. sampling: one trajectory integrated in steps
  {
    const x = bx(4), cxn = x + 15, cxd = x + bw - 15, my = cy - 4;
    L.ellipse(R, cxn, my, 10, 17, { fill: 'none', stroke: LG, width: 0.5, dash: '1.5 1.2' });
    L.ellipse(R, cxd, my, 8, 17, { fill: 'none', stroke: LG, width: 0.5, dash: '1.5 1.2' });
    const p0 = [cxn + 1, my + 6], p1 = [cxd - 1, my - 7];
    const pts = []; const n = 7;
    for (let k = 0; k <= n; k++) { const t = k / n; pts.push([p0[0] + t * (p1[0] - p0[0]), p0[1] + t * (p1[1] - p0[1]) + 5 * Math.sin(Math.PI * t) ]); }
    L.polyline(R, pts, { stroke: INK, width: 0.7, fill: 'none' });
    pts.forEach((p, k) => L.circle(R, p[0], p[1], k === 0 ? 1.8 : 1.3, { fill: k === 0 ? LG : INK, stroke: k === 0 ? GREY : INK, width: 0.4 }));
    L.chevron(R, [pts[n][0] + 2, pts[n][1] - 1.3], [0.93, -0.36], { len: 3.2, stroke: INK, width: 0.8 });
    L.text(R, cxn, my + 25, '*x*_{0}', { size: 6, anchor: 'middle' });
    L.text(R, cxd, my + 25, '*x*_{1}', { size: 6, anchor: 'middle' });
    L.text(R, x + bw / 2, top + gh - 11, 'd*x*/d*t* = *v*_{θ}', { size: 6, anchor: 'middle', valign: 'middle' });
  }
  // 6. decoding: closed field lines of B
  {
    const cx = bx(5) + bw / 2, my = cy - 2;
    [[26, 18], [15, 10]].forEach(([rx, ry]) => {
      L.ellipse(R, cx, my, rx, ry, { fill: 'none', stroke: B, width: 1 });
      [[cx + rx * 0.0, my - ry], [cx, my + ry]].forEach((p, k) => L.chevron(R, [p[0] + (k ? -1 : 1) * 1.2, p[1]], [k ? -1 : 1, 0], { len: 3.2, stroke: B, width: 0.9 }));
    });
    L.circle(R, cx, my, 1.6, { fill: B });
    L.text(R, cx + 27, my - 18, '*B*', { size: 7, color: B, weight: 'bold', anchor: 'start' });
  }

  // bracket over the generated representation + banner with the one idea
  const bl = bx(2), br = bx(4) + bw, by = top + gh + 25;
  L.line(R, [bl, by], [br, by], { stroke: INK, width: 0.7 });
  L.line(R, [bl, by], [bl, by - 3], { stroke: INK, width: 0.7 });
  L.line(R, [br, by], [br, by - 3], { stroke: INK, width: 0.7 });
  L.text(R, (bl + br) / 2, by + 5, 'Generated: Fourier modes of the potentials', { size: 6, anchor: 'middle', valign: 'top', weight: 'bold' });
  L.rect(R, bx(5), by - 3, bw, 15, { fill: B, fillOpacity: 0.12, stroke: B, width: 0.6, r: 2 });
  L.text(R, bx(5) + bw / 2, by + 4.5, 'every sample: ∇·B = 0', { size: 6, anchor: 'middle', valign: 'middle', weight: 'bold', color: B });
}
