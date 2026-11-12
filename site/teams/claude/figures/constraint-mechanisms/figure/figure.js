// Hero: none, a schematic of glyphs and labels; flat vector route (no 3D object to render)
// Figure 2: constraint mechanisms on one glyph set. Content: site/teams/claude/figures/FACTS.md
// ("Constraint mechanisms compared"). Colours: u blue, B orange/red, forcing grey.
export const figure = { width: 183, height: 129, name: 'constraint-mechanisms', format: 'journal' };

export default function draw(F, L) {
  const R = F.root;
  const U = '#0072B2', B = '#D55E00', INK = '#222222', GREY = '#8c8c8c', LG = '#c9c9c9', FR = '#b5b5b5';
  const W = L.mm(183);
  const cw = 164, gap = (W - 3 * cw) / 4, ph = 54, pitch = 88, top0 = 24;
  const colx = (c) => gap + c * (cw + gap);
  const N = [[-6, -15], [3, -9], [-5, -2], [5, 5], [-7, 11], [2, 16]];      // noise offsets
  const YD = [-17, -10, -3, 4, 11, 18], XD = [7, -9, 10, -6, 8, -10];       // end-point tangent / normal offsets

  // ---- shared glyphs -------------------------------------------------------------------------------
  const G = (x, y) => {                     // a cell: frame at (x, y), plot area cw x ph
    const g = { x, y, w: cw, h: ph, sx: x + 0.74 * cw, nx: x + 0.17 * cw, my: y + ph / 2 };
    L.rect(R, x, y, cw, ph, { fill: '#fafafa', stroke: FR, width: 0.5, r: 2 });
    return g;
  };
  const title = (x, y, v, name, note) => {
    L.text(R, x, y - 3, `**${v}**  ${name}`, { size: 6.5, valign: 'bottom' });
    note.forEach((t, j) => L.text(R, x, y + ph + 7 + j * 6.5, t, { size: 5.5, color: INK }));
  };
  const surface = (g, col = B) => {
    L.line(R, [g.sx, g.y + 4], [g.sx, g.y + ph - 4], { stroke: col, width: 1.4 });
    L.text(R, g.sx + 3, g.y + 2.5, '∇·B = 0', { size: 5, color: col, valign: 'top', weight: 'bold' });
  };
  const noise = (g, onLine = false) => {
    L.ellipse(R, g.nx, g.my, 11, 20, { fill: 'none', stroke: LG, width: 0.5, dash: '1.5 1.2' });
    return N.map((o) => [g.nx + o[0] * 0.7, g.my + o[1] * 0.9]);
  };
  const ends = (g, mode) => YD.map((yy, k) => [mode === 'on' ? g.sx : g.sx + XD[k], g.my + yy * 0.8]);
  const dot = (p, r, fill, stroke) => L.circle(R, p[0], p[1], r, { fill, stroke: stroke || fill, width: 0.4 });
  const flow = (g, nz, en, o = {}) => {
    nz.forEach((p, k) => L.line(R, p, en[k], { stroke: GREY, width: 0.4, opacity: 0.85 }));
    nz.forEach((p) => dot(p, 1.5, LG, GREY));
    if (!o.noEnds) en.forEach((p) => dot(p, o.r || 1.5, o.hollow ? '#fff' : INK, INK));
    L.arrow(R, [g.nx + 14, g.y + ph - 6], [g.nx + 38, g.y + ph - 6], { stroke: INK, width: 0.7, head: 2.4 });
  };
  const diamond = (p, col = INK) => L.polygon(R, [[p[0], p[1] - 3], [p[0] + 3, p[1]], [p[0], p[1] + 3], [p[0] - 3, p[1]]], { fill: '#fff', stroke: col, width: 0.9 });
  const ring = (c, r, dash = '2 1.2') => L.circle(R, c[0], c[1], r, { fill: 'none', stroke: B, width: 0.9, dash });
  const corr = (a, b) => L.arrow(R, a, b, { stroke: B, width: 0.9, head: 2.2 });

  // ---- column headers ------------------------------------------------------------------------------
  ['Model design', 'Training loss', 'Sampling procedure'].forEach((t, c) => {
    L.text(R, colx(c), 8, t, { size: 7.5, weight: 'bold', valign: 'middle' });
    L.line(R, [colx(c), 13.5], [colx(c) + cw, 13.5], { stroke: INK, width: 0.7 });
  });
  const cell = (c, r) => [colx(c), top0 + 8 + r * pitch];

  // ======== DESIGN ========
  { // W4 potentials
    const [x, y] = cell(0, 0); const g = G(x, y); surface(g);
    const nz = noise(g), en = ends(g, 'on'); flow(g, nz, en);
    L.text(R, g.nx + 44, g.y + ph - 6, 'B = ∇ × Â', { size: 5.5, valign: 'middle', italic: true });
    title(x, y, 'W4', 'Vector potentials', ['the output lies on the surface by construction']);
  }
  { // W4s equivariance
    const [x, y] = cell(0, 1); const g = G(x, y); surface(g);
    L.ellipse(R, g.nx, g.my, 8, 7, { fill: 'none', stroke: LG, width: 0.5, dash: '1.5 1.2' });
    const nz = [[-4, -3], [3, -1], [-1, -5]].map((o) => [g.nx + o[0], g.my + o[1]]);
    const up = [-18, -12, -6].map((yy) => [g.sx, g.my + yy]), dn = [6, 12, 18].map((yy) => [g.sx, g.my + yy]);
    nz.forEach((p, k) => { L.line(R, p, up[k], { stroke: GREY, width: 0.4 }); L.line(R, [p[0], 2 * g.my - p[1]], dn[k], { stroke: GREY, width: 0.4 }); dot(p, 1.5, LG, GREY); dot([p[0], 2 * g.my - p[1]], 1.5, LG, GREY); });
    up.concat(dn).forEach((p) => dot(p, 1.5, INK));
    L.line(R, [g.x + 6, g.my], [g.sx - 6, g.my], { stroke: INK, width: 0.5, dash: '3 1.5' });
    L.text(R, g.x + 6, g.y + 5, 'mirror: *B* → −*B*', { size: 5.5, anchor: 'start', valign: 'top', color: B, halo: true });
    title(x, y, 'W4s', 'B → −B equivariance', ['the velocity field is equivariant']);
  }
  { // W9-W11 affine term / Gaussian anchor
    const [x, y] = cell(0, 2); const g = G(x, y); const cx = g.x + 0.7 * cw;
    L.ellipse(R, cx, g.my, 22, 14, { fill: 'none', stroke: INK, width: 0.8, dash: '2 1.2' });
    const nz = noise(g);
    nz.forEach((p, k) => dot([cx + (N[k][0] * 2.4), g.my + N[k][1] * 0.6], 1.5, INK));
    L.arrow(R, [g.nx + 14, g.my], [cx - 25, g.my], { stroke: INK, width: 1.4, head: 3 });
    const pts = []; for (let i = 0; i <= 24; i++) { const t = i / 24; pts.push([g.nx + 16 + t * 40, g.my - 7 + 2.5 * Math.sin(t * 9)]); }
    L.polyline(R, pts, { stroke: GREY, width: 0.7, fill: 'none' });
    L.text(R, g.nx + 36, g.my + 6, '*G x* + *b*', { size: 5.5, anchor: 'middle', valign: 'top' });
    L.text(R, g.nx + 36, g.my - 12, '+ network', { size: 5.5, anchor: 'middle', valign: 'bottom', color: GREY });
    L.text(R, cx, g.y + ph - 4, 'Gaussian law, per mode', { size: 5.5, anchor: 'middle', valign: 'bottom' });
    title(x, y, 'W9, W10, W11', 'Affine term, Gaussian anchor', ['W9: affine term learned next to the network', 'W10: exact Gaussian field; W11: plus learned affine correction']);
  }
  { // G0
    const [x, y] = cell(0, 3); const g = G(x, y); const cx = g.x + 0.7 * cw;
    L.ellipse(R, cx, g.my, 22, 14, { fill: 'none', stroke: INK, width: 0.8, dash: '2 1.2' });
    YD.forEach((yy, k) => dot([cx + XD[k] * 2.2, g.my + yy * 0.6], 1.5, INK));
    L.rect(R, g.x + 12, g.my - 8, 44, 16, { fill: '#fff', stroke: INK, width: 0.6, r: 2 });
    L.text(R, g.x + 34, g.my, 'μ, Σ per mode', { size: 5.5, anchor: 'middle', valign: 'middle' });
    L.arrow(R, [g.x + 58, g.my], [cx - 25, g.my], { stroke: INK, width: 1.4, head: 3 });
    L.text(R, g.x + 82, g.my - 3, 'sample', { size: 5.5, anchor: 'middle', valign: 'bottom' });
    L.text(R, g.x + 34, g.y + ph - 4, 'no network', { size: 5.5, anchor: 'middle', valign: 'bottom', color: GREY });
    title(x, y, 'G0', 'Conditional Gaussian law', ['one mean and one 8 × 8 covariance per Fourier mode']);
  }

  // ======== LOSS ========
  { // W1
    const [x, y] = cell(1, 0); const g = G(x, y); surface(g);
    const nz = noise(g), en = ends(g, 'off'); flow(g, nz, en);
    const k = 2, a = nz[k], b = en[k], xt = [a[0] + 0.45 * (b[0] - a[0]), a[1] + 0.45 * (b[1] - a[1])];
    L.circle(R, xt[0], xt[1], 2, { fill: '#fff', stroke: INK, width: 0.8 });
    L.text(R, xt[0], xt[1] - 4, '*x*_{t}', { size: 5.5, anchor: 'middle', valign: 'bottom', halo: true });
    L.rect(R, b[0] - 2.3, b[1] - 2.3, 4.6, 4.6, { fill: '#fff', stroke: INK, width: 0.9 });
    L.text(R, b[0] + 4, b[1] + 3, 'x̂_{1}', { size: 5.5, valign: 'top', halo: true });
    corr([b[0] + 2.5, b[1] + 0.2], [g.sx - 1, b[1] + 0.2]);
    title(x, y, 'W1', 'Divergence penalty', ['on the end-of-path prediction x̂_{1} = *x*_{t} + (1 − *t*) *v*']);
  }
  { // W5
    const [x, y] = cell(1, 1); const g = G(x, y); const cx = g.x + 0.74 * cw;
    const nz = noise(g), en = ends(g, 'off').map((p, k) => [cx + XD[k] * 2.2, g.my + YD[k] * 0.85]); flow(g, nz, en);
    ring([cx, g.my], 5, '1.5 1');
    const mean = [cx - 10, g.my + 3]; diamond(mean);
    corr([mean[0] + 3, mean[1]], [cx - 6, g.my + 1]);
    L.text(R, g.x + cw - 4, g.y + 5, '⟨{#8c8c8c|*f*}·{#0072B2|*u*}⟩ − ν⟨|{#0072B2|ω}|²⟩ − η⟨|{#D55E00|*j*}|²⟩ = 0', { size: 5, anchor: 'end', valign: 'top' });
    title(x, y, 'W5', 'Law-level stationarity loss', ['constrains a mean over samples, not each sample']);
  }
  { // W0
    const [x, y] = cell(1, 2); const g = G(x, y); surface(g);
    const nz = noise(g), en = ends(g, 'off'); flow(g, nz, en);
    title(x, y, 'W0', 'No constraint', ['free Fourier components: baseline']);
  }
  { // legend
    const [x, y] = cell(1, 3); const g = G(x, y);
    const rows = [
      () => { dot([g.x + 10, g.y + 10], 1.5, LG, GREY); L.arrow(R, [g.x + 14, g.y + 10], [g.x + 26, g.y + 10], { stroke: INK, width: 0.7, head: 2.2 }); dot([g.x + 30, g.y + 10], 1.5, INK); return 'noise → sample, along the flow'; },
      () => { L.line(R, [g.x + 10, g.y + 18], [g.x + 30, g.y + 18], { stroke: B, width: 1.4 }); return 'constraint surface ∇·B = 0'; },
      () => { diamond([g.x + 14, g.y + 26]); ring([g.x + 26, g.y + 26], 3.5, '1.5 1'); return 'mean of the samples, law-level target'; },
      () => { corr([g.x + 10, g.y + 34], [g.x + 30, g.y + 34]); return 'correction by the mechanism'; },
      () => { L.text(R, g.x + 10, g.y + 42, '{#0072B2|*u*}   {#D55E00|*B*}   {#8c8c8c|*f*}', { size: 6, weight: 'bold', valign: 'middle' }); return 'velocity, magnetic field, forcing'; },
    ];
    rows.forEach((r, i) => { const t = r(); L.text(R, g.x + 40, g.y + 10 + i * 8, t, { size: 5.5, valign: 'middle' }); });
    L.text(R, x, y - 3, '**Shared glyphs**', { size: 6.5, valign: 'bottom' });
  }

  // ======== SAMPLING ========
  { // W2
    const [x, y] = cell(2, 0); const g = G(x, y); surface(g);
    const nz = noise(g), en = ends(g, 'off'); flow(g, nz, en, { hollow: true });
    en.forEach((p) => { corr([p[0] + 1.6 * Math.sign(g.sx - p[0]), p[1]], [g.sx - Math.sign(g.sx - p[0]) * 1.5, p[1]]); dot([g.sx, p[1]], 1.5, INK); });
    title(x, y, 'W2', 'Final Leray projection', ['projection of the final samples onto the surface']);
  }
  { // W3
    const [x, y] = cell(2, 1); const g = G(x, y); surface(g);
        [-22, 2].forEach((off) => {
      let yy = g.my + off; dot([g.sx, yy], 1.6, LG, GREY);
      for (let k = 0; k < 3; k++) { const a = [g.sx + 8, yy + 8]; L.line(R, [g.sx, yy], a, { stroke: GREY, width: 0.5 }); corr([a[0], a[1]], [g.sx + 1.5, a[1] + 0.01]); yy += 8; dot([g.sx, yy], 1.5, INK); }
    });
    L.text(R, g.x + 6, g.my - 4, 'projected noise', { size: 5.5, valign: 'bottom' });
    L.arrow(R, [g.x + 30, g.my], [g.sx - 14, g.my], { stroke: INK, width: 0.7, head: 2.4 });
    L.text(R, g.x + 6, g.my + 12, 'every step projected', { size: 5.5, valign: 'top' });
    title(x, y, 'W3', 'Projected flow', ['projected noise; projection of every integration stage']);
  }
  { // W7
    const [x, y] = cell(2, 2); const g = G(x, y); const cx = g.x + 0.74 * cw;
    const nz = noise(g), en = ends(g, 'off').map((p, k) => [cx + XD[k] * 2.2, g.my + YD[k] * 0.85]); flow(g, nz, en, { noEnds: true });
    const rr = [0.8, 1.2, 2.6, 2.4, 1.0, 0.7]; en.forEach((p, k) => dot(p, rr[k], INK));
    ring([cx, g.my], 5, '1.5 1'); diamond([cx + 3, g.my - 3]);
    title(x, y, 'W7', 'Exponential tilting', ['reweights the samples on the identities (dot size = weight)']);
  }
  { // W8
    const [x, y] = cell(2, 3); const g = G(x, y); const cx = g.x + 0.74 * cw, R0 = 17;
    const nz = noise(g); const ang = [0.3, 1.3, 2.4, 3.3, 4.4, 5.5], rad = [1.7, 0.55, 1.5, 0.6, 1.6, 0.5];
    const en = ang.map((a, k) => [cx + 0.6 * rad[k] * R0 * Math.cos(a) * 1.1, g.my + 0.55 * rad[k] * R0 * Math.sin(a) * 1.2]);
    flow(g, nz, en, { noEnds: true });
    ring([cx, g.my], R0, '2 1.2');
    en.forEach((p, k) => {
      const d = Math.hypot(p[0] - cx, p[1] - g.my), ux = (p[0] - cx) / d, uy = (p[1] - g.my) / d, tx = cx + ux * R0 * 0.66, ty = g.my + uy * R0 * 0.66;
      dot(p, 1.5, INK);
    });
    title(x, y, 'W8', 'Per-sample rescaling', ['each sample: small scales rescaled to the energy balance']);
  }
}
