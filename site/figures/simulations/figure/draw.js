// Figure « simulations » : les trois bancs du stage (E1 Gissinger, E2 MHD 2D, E3 dynamo ABC) sur un même gabarit.
// Hero : aucun (petits multiples) ; vignettes reprises de plan-these (mêmes données, calculées) ; réponses tracées à
// partir des résultats (E1, E3) ou recalculées avec le solveur et les réglages de E2 (make_data.py).

export const K = {
  lam: '#009E73', lamT: '#006E4F', lamL: '#e0f2ea', B: '#D55E00', BT: '#a8470a', u: '#0072B2',
  ink: '#2b2b2b', sub: '#555555', mid: '#7a7a7a', light: '#bdbdbd', faint: '#ececec', frame: '#d3d6da', badge: '#4d4d4d',
};
export const MONO = "'DejaVu Sans Mono', 'Liberation Mono', Consolas, monospace";
export const esc = (s) => s.replace(/([_*^{])/g, '\\$1');
const mono = (L, p, x, y, s, o = {}) => L.text(p, x, y, esc(s), { size: 5.6, family: MONO, color: K.ink, ...o });

const T = {
  fr: {
    cols: ['Système', 'Schéma numérique', 'Balayage du paramètre', 'Données gardées', 'Dans la chaîne'],
    names: [['E1', 'Gissinger, 3 modes'], ['E2', 'MHD 2D forcée'], ['E3', 'dynamo ABC']],
    scheme: [['RK4, Δt = 0,01', 'transitoire 300'], ['pseudo-spectral 32²', 'forçage blanc, Δt = 0,01'], ['pseudo-spectral 32³', 'RK4 à facteur intégrant']],
    data: [['16 trajectoires × 1 500', 'états par Γ'], ['16 membres × 150', 'instantanés par η'], ['λ(Rm) et', 'modes propres de B']],
    chain: ['script autonome', 'palier1_mhd2d', 'palier2_abc3d'],
    resp: ['passages de D par 0', 'E_{B}', 'λ'], train: 'entraînement (E1, E2)', test: 'test', thr: 'seuil',
    rows: ['Système', 'Balayage', 'Schéma', 'Données', 'Chaîne'], both: 'Données et chaîne',
  },
  en: {
    cols: ['System', 'Numerical scheme', 'Parameter sweep', 'Data kept', 'In the pipeline'],
    names: [['E1', 'Gissinger, 3 modes'], ['E2', 'forced 2D MHD'], ['E3', 'ABC dynamo']],
    scheme: [['RK4, Δt = 0.01', 'transient 300'], ['pseudo-spectral 32²', 'white forcing, Δt = 0.01'], ['pseudo-spectral 32³', 'integrating-factor RK4']],
    data: [['16 trajectories × 1,500', 'states per Γ'], ['16 members × 150', 'snapshots per η'], ['λ(Rm) and', 'B eigenmodes']],
    chain: ['standalone script', 'palier1_mhd2d', 'palier2_abc3d'],
    resp: ['zero crossings of D', 'E_{B}', 'λ'], train: 'training (E1, E2)', test: 'test', thr: 'threshold',
    rows: ['System', 'Sweep', 'Scheme', 'Data', 'Pipeline'], both: 'Data and pipeline',
  },
};

function bilinP(Mx, u, v) {
  const n = Mx.length, x = u * n - 0.5, y = v * n - 0.5;
  const i0 = Math.floor(x), j0 = Math.floor(y), fx = x - i0, fy = y - j0;
  const w = (i) => ((i % n) + n) % n;
  const a = Mx[w(i0)][w(j0)], b = Mx[w(i0 + 1)][w(j0)], c = Mx[w(i0)][w(j0 + 1)], d = Mx[w(i0 + 1)][w(j0 + 1)];
  return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy;
}
function badge(L, p, cx, cy, r, s) {
  L.circle(p, cx, cy, r, { fill: K.badge, stroke: 'none' });
  L.text(p, cx, cy, s, { size: 5.6, weight: 'bold', color: '#ffffff', anchor: 'middle', valign: 'middle' });
}

// ------------------------------------------------------------------- vignettes (mêmes dessins que plan-these)
function vGiss(L, p, D, bx, by, bw, bh) {
  const m = L.mm, g = L.group(p, {}).node;
  const y0 = m(by + bh / 2), X = (t) => m(bx + 1.6 + t * (bw - 3.4)), Y = (d) => y0 - d * m(bh / 2 - 0.3);
  L.line(g, [m(bx + 1.0), m(by - 0.6)], [m(bx + 1.0), m(by + bh + 0.4)], { stroke: '#7a7a7a', width: 0.4 });
  L.line(g, [m(bx + 1.0), y0], [m(bx + bw - 0.9), y0], { stroke: '#9a9a9a', width: 0.4, dash: '1.2 0.9' });
  L.polygon(g, [[m(bx + bw + 0.2), y0], [m(bx + bw - 1.2), y0 - m(0.55)], [m(bx + bw - 1.2), y0 + m(0.55)]], { fill: '#7a7a7a', stroke: 'none' });
  L.polyline(g, D.gissinger.t.map((t, i) => [X(t), Y(D.gissinger.D[i])]), { stroke: K.ink, width: 0.45, fill: 'none', join: 'round' });
  L.text(g, m(bx + 0.2), m(by - 0.4), '*D*', { size: 6, anchor: 'end', valign: 'top', color: K.B });
  L.text(g, m(bx + bw + 0.2), y0 + m(2.5), '*t*', { size: 6, anchor: 'end', valign: 'middle' });
}
function vMhd(L, p, D, bx, by, s) {
  const m = L.mm, rows0 = D.mhd2d.j.slice().reverse(), NU = 96;
  const rows = Array.from({ length: NU }, (_, r) => Array.from({ length: NU }, (_, c) => bilinP(rows0, (r + 0.5) / NU, (c + 0.5) / NU)));
  L.pixelImage(p, m(bx), m(by), m(s), rows, { palette: ['#fafafa', '#cdcdcd', '#6f6f6f'], overlap: 0.6, skipBelow: 0 });
  const clip = L.clipPath(p.node, `M${m(bx)},${m(by)} h${m(s)} v${m(s)} h${-m(s)} Z`);
  const g = L.group(p, { clip }).node;
  for (const ln of D.mhd2d.a_lines) L.polyline(g, ln.map(([u, v]) => [m(bx + u * s), m(by + (1 - v) * s)]), { stroke: '#2f2f2f', width: 0.3, fill: 'none', opacity: 0.8 });
  L.rect(p, m(bx), m(by), m(s), m(s), { fill: 'none', stroke: '#5f5f5f', width: 0.45 });
}
function vAbc(L, p, D, cx, cy, eMM) {
  const m = L.mm, e = m(eMM);
  const P3 = L.obliqueProj({ preset: 'angles', angle: 32, depth: 0.55 });
  const box = L.obliqueBox(p, P3, [e, e, e], { at: [m(cx), m(cy)], anchor: 'center', fill: '#ffffff', stroke: 'none' });
  const lerp = (v) => L.ramp(['#f9f9f9', '#c9c9c9', '#8a8a8a', '#3f3f3f'], Math.min(1, Math.max(0, v)));
  const N = 40, F_ = D.abc;
  const sample = (key, w) => {
    const f = w.map((c) => c / e);
    if (key === 'x1') return bilinP(F_.x1, f[1], f[2]);
    if (key === 'y0') return bilinP(F_.y0, f[0], f[2]);
    return bilinP(F_.z1, f[0], f[1]);
  };
  for (const key of ['y0', 'x1', 'z1']) {
    const M = box.faces[key];
    const d = 'M' + M.corners.map((q) => q.map((v) => v.toFixed(3)).join(',')).join(' L') + ' Z';
    const g = L.group(p, { clip: L.clipPath(p.node, d) }).node;
    const shade = key === 'z1' ? 0 : key === 'y0' ? -0.04 : -0.1;
    for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
      const du = 1 / N, ov = 0.4 / N, u0 = i * du, v0 = j * du;
      L.polygon(g, M.quad(u0 - ov, v0 - ov, u0 + du + ov, v0 + du + ov), { fill: L.shade(lerp(sample(key, M.world(u0 + du / 2, v0 + du / 2))), shade), stroke: 'none' });
    }
  }
  for (const key of ['y0', 'x1', 'z1']) L.polygon(p, box.faces[key].corners, { fill: 'none', stroke: K.ink, width: 0.5, join: 'round' });
}

// ------------------------------------------------------------------- balayages : réponse en fonction du paramètre
// cadre commun : axe horizontal = paramètre (vert), réponse en vermillon, points pleins = entraînement, vides = test
function frame(L, p, x, y, w, h, { xlab, ylab, ticks, X, ylabX }) {
  const m = L.mm;
  L.line(p, [m(x), m(y + h)], [m(x + w), m(y + h)], { stroke: K.ink, width: 0.45 });
  L.line(p, [m(x), m(y)], [m(x), m(y + h)], { stroke: K.ink, width: 0.45 });
  for (const [v, s] of ticks) {
    L.line(p, [X(v), m(y + h)], [X(v), m(y + h + 0.8)], { stroke: K.ink, width: 0.4 });
    L.text(p, X(v), m(y + h + 2.6), s, { size: 5.3, anchor: 'middle', valign: 'middle', color: K.sub });
  }
  L.text(p, m(x + w + 0.6), m(y + h), xlab, { size: 6.2, italic: true, color: K.lamT, anchor: 'start', valign: 'middle' });
  L.text(p, ylabX ?? m(x + 1.2), m(y - 1.6), ylab, { size: 5.6, color: K.BT, anchor: 'start', valign: 'middle' });
}
function dots(L, p, xs, yy, filled) {
  for (const x of xs) L.circle(p, x, yy, L.mm(0.62), filled ? { fill: K.lam, stroke: 'none' } : { fill: '#ffffff', stroke: K.lam, width: 0.55 });
}
function plotE1(L, p, S, E, x, y, w, h) {
  const f = (v, d) => v.toFixed(d).replace('.', S.dec);
  const m = L.mm, X = (g) => m(x + (g - 0.8) / 0.2 * w), ymax = 0.012, Y = (r) => m(y + h - r / ymax * h);
  // seuil des renversements : entre 0,86 et 0,865 (aucun passage jusqu'à 0,86)
  L.rect(p, X(0.86), m(y), X(0.865) - X(0.86), m(h), { fill: K.lamL, stroke: 'none' });
  L.text(p, X(0.8625), m(y - 1.6), S.thr, { size: 5.2, color: K.lamT, anchor: 'middle', valign: 'middle' });
  frame(L, p, x, y, w, h, { xlab: 'Γ', ylab: S.resp[0], ticks: [[0.8, f(0.8, 2)], [0.9, f(0.9, 2)], [1.0, f(1, 2)]], X, ylabX: X(0.885) });
  L.polyline(p, E.fine.map(([g, r]) => [X(g), Y(r)]), { fill: 'none', stroke: K.B, width: 0.8, join: 'round' });
  dots(L, p, E.G_train.map(X), m(y + h), true);
  dots(L, p, E.G_test.map(X), m(y + h - 1.6), false);
}
function plotE2(L, p, S, E, x, y, w, h) {
  const f = (v, d) => v.toFixed(d).replace('.', S.dec);
  const m = L.mm, l0 = Math.log10(0.0035), l1 = Math.log10(0.026), X = (eta) => m(x + (Math.log10(eta) - l0) / (l1 - l0) * w);
  const pts = E.points.slice().sort((a, b) => a.eta - b.eta);
  const ymax = Math.max(...pts.map((q) => q.Eb_mean + q.Eb_std)) * 1.08, Y = (v) => m(y + h - v / ymax * h);
  frame(L, p, x, y, w, h, { xlab: 'η', ylab: S.resp[1], ticks: [[0.004, f(0.004, 3)], [0.008, f(0.008, 3)], [0.016, f(0.016, 3)]], X });
  const band = pts.map((q) => [X(q.eta), Y(q.Eb_mean + q.Eb_std)]).concat(pts.slice().reverse().map((q) => [X(q.eta), Y(Math.max(0, q.Eb_mean - q.Eb_std))]));
  L.polygon(p, band, { fill: K.B, fillOpacity: 0.14, stroke: 'none' });
  L.polyline(p, pts.map((q) => [X(q.eta), Y(q.Eb_mean)]), { fill: 'none', stroke: K.B, width: 0.8, join: 'round' });
  dots(L, p, E.eta_train.map(X), m(y + h), true);
  dots(L, p, E.eta_test.map(X), m(y + h - 1.6), false);
}
function plotE3(L, p, S, E, x, y, w, h) {
  const m = L.mm, X = (r) => m(x + (r - 0) / 31 * w);
  // λ vaut ±0,01 entre Rm = 8 et 30 mais −0,50 à Rm = 2 : axe restreint, points hors échelle marqués d'une flèche
  const lo = -0.012, hi = 0.013, Y = (v) => m(y + h - (Math.max(lo, Math.min(hi, v)) - lo) / (hi - lo) * h);
  const th = E.thresholds;
  for (const [a, b] of [[th[0], th[1]], [th[2], 31]]) L.rect(p, X(a), m(y), X(b) - X(a), m(h), { fill: K.lamL, stroke: 'none' });
  frame(L, p, x, y, w, h, { xlab: 'Rm', ylab: S.resp[2], ticks: [[0, '0'], [10, '10'], [20, '20'], [30, '30']], X });
  L.line(p, [m(x), Y(0)], [m(x + w), Y(0)], { stroke: K.mid, width: 0.4, dash: '1.2 0.8' });
  L.text(p, m(x + w + 0.6), Y(0), '0', { size: 5.2, color: K.sub, anchor: 'start', valign: 'middle' });
  const inr = E.rates.filter(([, v]) => v >= lo), out = E.rates.filter(([, v]) => v < lo);
  const clip = L.clipPath(p.node, `M${m(x)},${m(y)} h${m(w)} v${m(h)} h${-m(w)} Z`);
  const g = L.group(p, { clip }).node;
  L.polyline(g, E.rates.map(([r, v]) => [X(r), Y(v)]), { fill: 'none', stroke: K.B, width: 0.8, join: 'round' });
  for (const [r, v] of inr) L.circle(p, X(r), Y(v), m(0.42), { fill: K.B, stroke: 'none' });
  for (const [r] of out) L.polygon(p, [[X(r) - m(0.75), m(y + h) - m(1.9)], [X(r) + m(0.75), m(y + h) - m(1.9)], [X(r), m(y + h) - m(0.5)]], { fill: K.B, stroke: 'none' });
  for (const t of th) L.text(p, X(t), m(y - 1.6), t.toFixed(t < 10 ? 2 : 1).replace('.', S.dec), { size: 5.1, color: K.lamT, anchor: 'middle', valign: 'middle' });
}

export function make(lang, concept = 'A') {
  const S = { ...T[lang], dec: lang === 'fr' ? ',' : '.' };
  return async function draw(F, L) {
    const m = L.mm;
    const D = await (await fetch('/figure/data/sim_data.json')).json();
    const V = D.vignettes;
    if (concept === 'A') {
      const P = F.panel('', { x: 0, y: 0, w: 183, h: 100 });
      const CX = [2, 46, 80, 141], RY = [9, 40, 71], RH = 29;
      S.cols.forEach((c, i) => { if (i < 4) L.text(P, m([2, 46, 80, 141][i]), m(4.2), i === 3 ? S.both : c, { size: 6.4, weight: 'bold', color: K.ink, valign: 'middle' }); });
      for (let r = 0; r < 3; r++) {
        const y0 = RY[r];
        L.line(P, [m(2), m(y0 - 1.6)], [m(181), m(y0 - 1.6)], { stroke: K.frame, width: 0.5 });
        badge(L, P, m(4.2), m(y0 + 2.6), m(1.9), S.names[r][0]);
        L.text(P, m(7.2), m(y0 + 2.6), S.names[r][1], { size: 6.4, weight: 'bold', valign: 'middle' });
        if (r === 0) vGiss(L, P, V, 8, y0 + 7.4, 30, 17);
        if (r === 1) vMhd(L, P, V, 12, y0 + 6.0, 20);
        if (r === 2) vAbc(L, P, V, 22, y0 + 16.4, 13);
        S.scheme[r].forEach((s, i) => L.text(P, m(CX[1]), m(y0 + 9 + i * 3.4), s, { size: 6, valign: 'middle', color: i ? K.sub : K.ink }));
        const px = CX[2] + 4, pw = 46, py = y0 + 6.0, ph = 16.4;
        if (r === 0) plotE1(L, P, S, D.e1, px, py, pw, ph);
        if (r === 1) plotE2(L, P, S, D.e2, px, py, pw, ph);
        if (r === 2) plotE3(L, P, S, D.e3, px, py, pw, ph);
        S.data[r].forEach((s, i) => L.text(P, m(CX[3]), m(y0 + 7 + i * 3.2), s, { size: 6, valign: 'middle' }));
        const ch = S.chain[r], isMono = r > 0;
        const cw = m(ch.length * (isMono ? 1.26 : 1.08) + 4.4);
        L.rect(P, m(CX[3]), m(y0 + 15.6), cw, m(4.4), { r: m(2.2), fill: r ? '#ffffff' : K.faint, stroke: r ? K.ink : K.light, width: 0.5 });
        if (isMono) mono(L, P, m(CX[3]) + cw / 2, m(y0 + 17.8), (r ? '→ ' : '') + ch, { size: 5.6, anchor: 'middle', valign: 'middle' });
        else L.text(P, m(CX[3]) + cw / 2, m(y0 + 17.8), ch, { size: 5.8, anchor: 'middle', valign: 'middle', color: K.sub });
      }
      // légende des points
      const ly = 98.2;
      dots(L, P, [m(80)], m(ly), true); L.text(P, m(81.4), m(ly), S.train, { size: 5.5, valign: 'middle', color: K.sub });
      dots(L, P, [m(112)], m(ly), false); L.text(P, m(113.4), m(ly), S.test, { size: 5.5, valign: 'middle', color: K.sub });
    } else {
      const P = F.panel('', { x: 0, y: 0, w: 183, h: 96 });
      const CX = [24, 77, 130], CW = 51;
      S.rows.forEach((s, i) => L.text(P, m(2), m([18, 46, 71, 80, 89][i]), s, { size: 6.2, weight: 'bold', valign: 'middle' }));
      for (let c = 0; c < 3; c++) {
        const x0 = CX[c];
        L.rect(P, m(x0), m(1), m(CW), m(94), { r: m(1.8), fill: 'none', stroke: K.frame, width: 0.5 });
        badge(L, P, m(x0 + 3.4), m(5.0), m(1.9), S.names[c][0]);
        L.text(P, m(x0 + 6.4), m(5.0), S.names[c][1], { size: 6.4, weight: 'bold', valign: 'middle' });
        if (c === 0) vGiss(L, P, V, x0 + 9, 11, 32, 15);
        if (c === 1) vMhd(L, P, V, x0 + 15.5, 9.4, 20);
        if (c === 2) vAbc(L, P, V, x0 + 24, 19.4, 13);
        const px = x0 + 6, pw = 38, py = 36, ph = 18;
        if (c === 0) plotE1(L, P, S, D.e1, px, py, pw, ph);
        if (c === 1) plotE2(L, P, S, D.e2, px, py, pw, ph);
        if (c === 2) plotE3(L, P, S, D.e3, px, py, pw, ph);
        L.text(P, m(x0 + 2.4), m(69.6), S.scheme[c].join(', '), { size: 5.6, valign: 'middle' });
        L.text(P, m(x0 + 2.4), m(80), S.data[c].join(' '), { size: 5.6, valign: 'middle' });
        mono(L, P, m(x0 + 2.4), m(89), (c ? '→ ' : '') + S.chain[c], { size: 5.6, valign: 'middle' });
      }
    }
  };
}
