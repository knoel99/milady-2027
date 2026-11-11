// Figure « architecture » (concept A) : la chaîne d'une campagne et ses deux magasins (a), puis les
// services qui réalisent chaque rôle sur les trois cibles (b). Texte en français ou en anglais.
// Hero : aucun (architecture logicielle) ; icônes de machines en vector 3D (L.obliqueBox) ; vignette du
// champ calculée (écoulement de Taylor–Green initial, analytique, kf = 2, comme palier2_tg3d.yaml).

// Clé de couleurs du site (figures cadre, plan-these, taxonomie) : la couleur est réservée aux données.
export const K = {
  lam: '#009E73', lamT: '#006E4F', z: '#6C4BA0', zl: '#EEE9F6', u: '#0072B2', B: '#D55E00',
  E: '#C98A00', Efill: '#F6DFA6',
  ink: '#2b2b2b', sub: '#555555', mid: '#7a7a7a', light: '#bdbdbd', faint: '#ececec', paper: '#ffffff',
  badge: '#4d4d4d', frame: '#d3d6da', col: '#f6f7f8',
  cat: '#E3E8EE', catEdge: '#A9B4C0', catInk: '#34414e',      // catalogue : gris bleuté
  fil: '#EDE8E0', filEdge: '#BDB2A2', filInk: '#4a4136',      // fichiers : gris chaud
};
export const MONO = "'DejaVu Sans Mono', 'Liberation Mono', Consolas, monospace";

const T = {
  fr: {
    a: 'Chaîne d’une campagne', b: 'Trois cibles, même chaîne',
    stages: ['Campagne', 'Lancement', 'Simulation', 'Stockage', 'Jeu de données', 'Entraînement', 'Évaluation'],
    sims: '12 simulations', ref: 'référence', gen: 'généré', sameId: 'même UUID',
    catRail: 'Catalogue · PostgreSQL ou SQLite', filRail: 'Fichiers · S3, MinIO ou disque',
    cols: [['Portable', 'sans GPU'], ['VM cloud GPU', 'Docker Compose'], ['Cluster Slurm', 'Apptainer']],
    rows: ['Exécution', 'Fichiers', 'Catalogue', 'Suivi'],
    venv: 'venv, processus', ports: 'ports sur 127.0.0.1', tunnel: 'tunnel SSH',
    array: 'tableau de jobs', gpuSim: '1 GPU par simulation', torchrun: 'torchrun par nœud',
    sqliteWork: 'SQLite sur $WORK', noNet: 'nœuds sans Internet', copyS3: 'copie vers S3',
    container: 'conteneur worker-gpu', split: 'par point (Re, Pm)', evalSub: 'spectres, bilans',
  },
  en: {
    a: 'Campaign pipeline', b: 'Three targets, one pipeline',
    stages: ['Campaign', 'Launch', 'Simulation', 'Storage', 'Dataset', 'Training', 'Evaluation'],
    sims: '12 simulations', ref: 'reference', gen: 'generated', sameId: 'same UUID',
    catRail: 'Catalog · PostgreSQL or SQLite', filRail: 'Files · S3, MinIO or disk',
    cols: [['Laptop', 'no GPU'], ['Cloud GPU VM', 'Docker Compose'], ['Slurm cluster', 'Apptainer']],
    rows: ['Execution', 'Files', 'Catalog', 'Tracking'],
    venv: 'venv, processes', ports: 'ports on 127.0.0.1', tunnel: 'SSH tunnel',
    array: 'job array', gpuSim: '1 GPU per simulation', torchrun: 'torchrun per node',
    sqliteWork: 'SQLite on $WORK', noNet: 'nodes without Internet', copyS3: 'copy to S3',
    container: 'worker-gpu container', split: 'by (Re, Pm) point', evalSub: 'spectra, budgets',
  },
};

// ------------------------------------------------------------------------------------------ helpers
export function badge(L, p, cx, cy, r, k, size = 6) {
  L.circle(p, cx, cy, r, { fill: K.badge, stroke: 'none' });
  L.text(p, cx, cy, String(k), { size, weight: 'bold', color: '#ffffff', anchor: 'middle', valign: 'middle' });
}
// texte en chasse fixe : « _ », « * », « ^ », « { » sont des caractères, pas du balisage
export const esc = (s) => s.replace(/([_*^{])/g, '\\$1');
export function mono(L, p, x, y, s, o = {}) {
  return L.text(p, x, y, esc(s), { size: 5.5, family: MONO, color: K.ink, ...o });
}
// feuille à coin plié
export function sheet(L, p, x, y, w, h, { fold = 3, fill = '#ffffff', stroke = '#9aa3ab', width = 0.45 } = {}) {
  L.polygon(p, [[x, y], [x + w - fold, y], [x + w, y + fold], [x + w, y + h], [x, y + h]], { fill, stroke, width, join: 'round' });
  L.polyline(p, [[x + w - fold, y], [x + w - fold, y + fold], [x + w, y + fold]], { fill: 'none', stroke, width, join: 'round' });
}
// grille Re × Pm de palier2_tg3d : 4 colonnes (Re = 25, 50, 100, 200), 3 rangées (Pm = 0,5 ; 1 ; 2, vers le haut)
export function paramGrid(L, p, x0, y0, d, r, mark) {
  const pts = [];
  for (let i = 0; i < 4; i++) for (let j = 0; j < 3; j++) {
    const cx = x0 + i * d, cy = y0 - j * d;
    pts.push([cx, cy, i, j]);
    (mark ? mark(i, j, cx, cy) : L.circle(p, cx, cy, r, { fill: K.lam, stroke: 'none' }));
  }
  return pts;
}
// icônes de machines
export function laptop(L, p, x, y, s) {
  const P3 = L.obliqueProj({ preset: 'angles', angle: 28, depth: 0.5 });
  const base = L.obliqueBox(p, P3, [s, 0.62 * s, 0.06 * s], { at: [x, y + 0.18 * s], anchor: 'center', fill: '#d9dde1', stroke: '#6b737b', width: 0.35 });
  const BP = base.P;
  const scr = [[0, 0.62 * s, 0.06 * s], [s, 0.62 * s, 0.06 * s], [s, 0.68 * s, 0.68 * s], [0, 0.68 * s, 0.68 * s]].map((w) => BP(...w));
  L.polygon(p, scr, { fill: '#5b636b', stroke: '#3b4148', width: 0.35, join: 'round' });
  const inner = [[0.07 * s, 0.625 * s, 0.11 * s], [0.93 * s, 0.625 * s, 0.11 * s], [0.93 * s, 0.675 * s, 0.62 * s], [0.07 * s, 0.675 * s, 0.62 * s]].map((w) => BP(...w));
  L.polygon(p, inner, { fill: '#cfe3f1', stroke: 'none' });
}
export function server(L, p, x, y, s, { n = 3, gpu = false } = {}) {
  const P3 = L.obliqueProj({ preset: 'angles', angle: 28, depth: 0.5 });
  const b = L.obliqueBox(p, P3, [0.9 * s, 0.55 * s, 1.05 * s], { at: [x, y], anchor: 'center', fill: '#d9dde1', stroke: '#6b737b', width: 0.35 });
  const fr = b.faces.y0;
  for (let k = 0; k < n; k++) {
    const v0 = 0.12 + k * 0.28;
    L.polygon(p, fr.quad(0.1, v0, 0.9, v0 + 0.18), { fill: '#eef0f2', stroke: '#8a9299', width: 0.3 });
    L.circle(p, ...fr(0.18, v0 + 0.09), 0.35, { fill: gpu && k === n - 1 ? K.lam : '#7d868f', stroke: 'none' });
  }
  return b;
}
export function cloud(L, p, cx, cy, w, h) {
  L.cloud(p, cx, cy, w, h, { lobes: 9, fill: '#f1f4f7', stroke: '#9aa5b0', width: 0.4, seed: 7 });
}
// cylindre de base de données (catalogue) et dossier (fichiers), glyphes de rôle
export function dbGlyph(L, p, cx, cy, s, fill = K.cat, stroke = K.catEdge) {
  const rx = s / 2, ry = s * 0.17, h = s * 0.8;
  L.path(p, `M${cx - rx},${cy - h / 2} L${cx - rx},${cy + h / 2} A${rx},${ry} 0 0 0 ${cx + rx},${cy + h / 2} L${cx + rx},${cy - h / 2}`, { fill, stroke, width: 0.4 });
  L.ellipse(p, cx, cy - h / 2, rx, ry, { fill: L.shade(fill, 0.06), stroke, width: 0.4 });
  L.path(p, `M${cx - rx},${cy} A${rx},${ry} 0 0 0 ${cx + rx},${cy}`, { fill: 'none', stroke, width: 0.35 });
}
export function folderGlyph(L, p, cx, cy, s, fill = K.fil, stroke = K.filEdge) {
  const w = s, h = s * 0.72, x = cx - w / 2, y = cy - h / 2;
  L.path(p, `M${x},${y + h * 0.18} L${x},${y + h} L${x + w},${y + h} L${x + w},${y + h * 0.18} L${x + w * 0.5},${y + h * 0.18} L${x + w * 0.4},${y} L${x + w * 0.06},${y} Z`, { fill, stroke, width: 0.4, join: 'round' });
}
export function chipGlyph(L, p, cx, cy, s) {
  L.rect(p, cx - s / 2, cy - s / 2, s, s, { r: s * 0.12, fill: '#5f666d', stroke: 'none' });
  for (let k = -1; k <= 1; k++) for (const sgn of [-1, 1]) {
    L.line(p, [cx + k * s * 0.28, cy + sgn * s / 2], [cx + k * s * 0.28, cy + sgn * s * 0.68], { stroke: '#5f666d', width: 0.4 });
    L.line(p, [cx + sgn * s / 2, cy + k * s * 0.28], [cx + sgn * s * 0.68, cy + k * s * 0.28], { stroke: '#5f666d', width: 0.4 });
  }
  L.rect(p, cx - s * 0.22, cy - s * 0.22, s * 0.44, s * 0.44, { r: s * 0.05, fill: '#9aa2aa', stroke: 'none' });
}
export function trackGlyph(L, p, cx, cy, s) {
  L.polyline(p, [[cx - s / 2, cy - s * 0.3], [cx - s / 2, cy + s * 0.35], [cx + s / 2, cy + s * 0.35]], { fill: 'none', stroke: '#6b737b', width: 0.4 });
  L.polyline(p, L.sample((t) => cy - s * 0.25 + s * 0.45 * (1 - Math.exp(-3 * (t - (cx - s / 2)) / s)), cx - s * 0.45, cx + s * 0.45, 12).map(([x, y]) => [x, cy + s * 0.25 - (y - (cy - s * 0.25))]), { fill: 'none', stroke: '#6b737b', width: 0.5 });
}

// |u| de l'écoulement de Taylor–Green initial (kf = 2 sur [0, 2π)³), normalisé dans [0, 1]
export const tgSpeed = (X, Y, Z) => {
  const c = Math.cos(2 * Z);
  return Math.abs(c) * Math.sqrt(Math.sin(2 * X) ** 2 * Math.cos(2 * Y) ** 2 + Math.cos(2 * X) ** 2 * Math.sin(2 * Y) ** 2);
};

export function make(lang) {
  const S = T[lang];
  return async function draw(F, L) {
    const m = L.mm;
    // ------------------------------------------------------------------ panneau a
    const pa = F.panel('a', { x: 0, y: 0, w: 183, h: 62 });
    L.text(pa, 12, 7.6, S.a, { size: 7, weight: 'bold', color: K.ink, role: 'title' });
    const CW = 179 / 7, cx = (k) => m(2 + CW * (k + 0.5)), bx = (k) => m(2 + CW * k);
    const HY = m(9.2), GY = m(22.2), SUBY = m(34.4), MODY = m(37.2);
    const modules = ['infra/configs/', 'milady.sweep', 'milady.sim', 'milady.storage', 'milady.train.data', 'milady.train.fm3d', 'milady.eval'];
    for (let k = 0; k < 7; k++) {
      const x0 = bx(k) + m(1.4);
      badge(L, pa, x0 + m(1.9), HY, m(1.75), k + 1, 5.8);
      L.text(pa, x0 + m(4.4), HY, S.stages[k], { size: 6.5, weight: 'bold', color: K.ink, valign: 'middle' });
      mono(L, pa, cx(k), MODY, modules[k], { anchor: 'middle', size: 5.6, color: K.sub });
      F.anchor(`s${k}.in`, pa, bx(k) + m(1.1), GY);
      F.anchor(`s${k}.out`, pa, bx(k + 1) - m(1.1), GY);
    }
    for (let k = 0; k < 6; k++) {
      F.relate(`s${k}.out`, `s${k + 1}.in`, 'flow');
      L.connect(F, `s${k}.out`, `s${k + 1}.in`, { stroke: '#8a8a8a', width: 0.6, head: 2.2 });
    }
    const sub = (k, str, o = {}) => L.text(pa, cx(k), SUBY, str, { size: 5.7, color: K.sub, anchor: 'middle', ...o });

    // 1 : feuille YAML et grille Re × Pm (palier2_tg3d.yaml)
    {
      const c = cx(0), x = c - m(8.6), y = m(12.4), w = m(17.2), h = m(19.6), d = m(3.1);
      sheet(L, pa, x, y, w, h, { fold: m(3) });
      for (let k = 0; k < 2; k++) L.line(pa, [x + m(2), y + m(2.4 + k * 1.6)], [x + m(k ? 8.6 : 11.2), y + m(2.4 + k * 1.6)], { stroke: '#c4cad0', width: 0.8, cap: 'round' });
      const gx = x + m(6.0), gy = y + m(14.0);
      paramGrid(L, pa, gx, gy, d, m(0.82));
      L.text(pa, gx + 1.5 * d, gy + m(3.7), 'Re', { size: 6, italic: true, color: K.lamT, anchor: 'middle' });
      L.text(pa, x + m(2.9), gy - d, 'Pm', { size: 6, italic: true, color: K.lamT, anchor: 'middle', valign: 'middle' });
      sub(0, S.sims);
    }
    // 2 : douze tâches à identifiant déterministe
    {
      const c = cx(1), w = m(10.2), h = m(6.8);
      for (let k = 2; k >= 0; k--) {
        const x = c - m(9.0) + k * m(1.9), y = m(14.6) + k * m(2.3);
        L.rect(pa, x, y, w, h, { r: m(0.8), fill: '#ffffff', stroke: '#9aa3ab', width: 0.45 });
        if (k === 0) {
          L.circle(pa, x + m(2.0), y + h / 2, m(0.8), { fill: K.lam, stroke: 'none' });
          L.line(pa, [x + m(3.8), y + m(2.4)], [x + m(8.6), y + m(2.4)], { stroke: '#c4cad0', width: 0.8, cap: 'round' });
          L.line(pa, [x + m(3.8), y + m(4.4)], [x + m(7.2), y + m(4.4)], { stroke: '#c4cad0', width: 0.8, cap: 'round' });
        }
      }
      L.text(pa, c + m(7.8), GY, '×12', { size: 6.3, weight: 'bold', color: K.ink, anchor: 'middle', valign: 'middle' });
      mono(L, pa, c, SUBY, 'UUID v5', { anchor: 'middle', size: 5.6, color: K.sub });
    }
    // 3 : boîte périodique 64³, |u| du Taylor–Green initial (kf = 2) sur trois faces
    {
      const e = m(12.6);
      const P3 = L.obliqueProj({ preset: 'angles', angle: 32, depth: 0.55 });
      const box = L.obliqueBox(pa, P3, [e, e, e], { at: [cx(2) - m(0.6), GY - m(0.4)], anchor: 'center', fill: '#ffffff', stroke: 'none' });
      const lerp = (v) => L.ramp(['#fdfdfd', '#e1e3e6', '#a9b0b8', '#5d666f'], Math.min(1, Math.max(0, v)));
      const N = 40, TP = 2 * Math.PI;
      for (const key of ['y0', 'x1', 'z1']) {
        const M = box.faces[key];
        const dd = 'M' + M.corners.map((q) => q.map((v) => v.toFixed(3)).join(',')).join(' L') + ' Z';
        const g = L.group(pa, { clip: L.clipPath(pa.node, dd) }).node;
        const shade = key === 'z1' ? 0 : key === 'y0' ? -0.04 : -0.1;
        for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) {
          const du = 1 / N, ov = 0.4 / N, u0 = i * du, v0 = j * du;
          const wv = M.world(u0 + du / 2, v0 + du / 2);
          const val = tgSpeed(TP * wv[0] / e, TP * wv[1] / e, TP * wv[2] / e);
          L.polygon(g, M.quad(u0 - ov, v0 - ov, u0 + du + ov, v0 + du + ov), { fill: L.shade(lerp(val), shade), stroke: 'none' });
        }
      }
      for (const key of ['y0', 'x1', 'z1']) L.polygon(pa, box.faces[key].corners, { fill: 'none', stroke: K.ink, width: 0.5, join: 'round' });
      sub(2, '{' + K.u + '|**u**}, {' + K.B + '|**B**} · 64³');
    }
    // 4 : fichier MFF (HDF5 compatible The Well)
    {
      const c = cx(3), x = c - m(8.8), y = m(12.4), w = m(17.6), h = m(19.6);
      sheet(L, pa, x, y, w, h, { fold: m(3) });
      mono(L, pa, x + m(1.6), y + m(3.8), 'fields.h5', { size: 5.7, weight: 'bold' });
      const rows = [['dimensions/', K.sub], ['t1_fields/', K.u], ['milady_*', K.ink]];
      for (let k = 0; k < 3; k++) {
        const yy = y + m(8.0 + k * 3.7);
        L.polyline(pa, [[x + m(2.1), yy - m(3.0)], [x + m(2.1), yy - m(1.0)], [x + m(3.3), yy - m(1.0)]], { fill: 'none', stroke: '#9aa3ab', width: 0.35 });
        mono(L, pa, x + m(3.6), yy, rows[k][0], { size: 5.3, color: rows[k][1] });
      }
      sub(3, 'HDF5 · The Well');
    }
    // 5 : découpage par point de paramètres (train_fm3d.yaml : val Re = 100, Pm = 1 ; test Re = 50, Pm = 2)
    {
      const c = cx(4), d = m(2.9), r = m(0.78), x0 = c - m(8.9), y0 = m(27.8);
      const val = (x, y) => { L.circle(pa, x, y, r, { fill: K.lam, stroke: 'none' }); L.circle(pa, x, y, m(1.45), { fill: 'none', stroke: K.ink, width: 0.5 }); };
      const test = (x, y) => L.circle(pa, x, y, r, { fill: '#ffffff', stroke: K.lam, width: 0.75 });
      const tr = (x, y) => L.circle(pa, x, y, r, { fill: K.lam, stroke: 'none' });
      paramGrid(L, pa, x0, y0, d, r, (i, j, x, y) => (i === 2 && j === 1 ? val(x, y) : i === 1 && j === 2 ? test(x, y) : tr(x, y)));
      const lx = c + m(3.6);
      [[tr, 'train'], [val, 'val'], [test, 'test']].forEach(([gl, s], q) => {
        const y = y0 - (2 - q) * d;
        gl(lx, y);
        L.text(pa, lx + m(2.1), y, s, { size: 5.7, color: K.ink, valign: 'middle' });
      });
      sub(4, S.split);
    }
    // 6 : modèle génératif à potentiels vecteurs
    {
      const c = cx(5), x = c - m(9.4), y = m(14.0), w = m(11), h = m(14.4);
      L.rect(pa, x, y, w, h, { r: m(1.4), fill: K.zl, stroke: K.z, width: 0.55 });
      L.network(pa, x + m(1.2), y + m(1.6), { layers: [3, 4, 3], w: w - m(2.4), h: h - m(3.2), r: m(0.55), colors: [K.z, K.z, K.z], edges: true });
      const ax = x + w + m(1.0);
      L.text(pa, ax, y + m(3.2), '{' + K.u + '|A_{u}}, {' + K.B + '|A_{B}}', { size: 6, italic: true, anchor: 'start' });
      L.arrow(pa, [ax + m(2.6), y + m(5.0)], [ax + m(2.6), y + m(9.6)], { stroke: '#8a8a8a', width: 0.5, head: 1.8 });
      L.text(pa, ax + m(3.6), y + m(7.4), '∇×', { size: 6, color: K.ink, anchor: 'start', valign: 'middle' });
      L.text(pa, ax, y + m(12.6), '{' + K.u + '|**u**}, {' + K.B + '|**B**}', { size: 6, anchor: 'start' });
      sub(5, 'torchrun · DDP');
    }
    // 7 : comparaison de spectres (forme illustrative)
    {
      const c = cx(6), x = c - m(7.6), y = m(13.0), w = m(16.4), h = m(16.6);
      L.polyline(pa, [[x, y], [x, y + h], [x + w, y + h]], { fill: 'none', stroke: K.ink, width: 0.45 });
      L.text(pa, x - m(0.6), y + m(1.6), 'E(k)', { size: 5.7, italic: true, anchor: 'end' });
      L.text(pa, x + w, y + h + m(2.3), 'k', { size: 5.7, italic: true, anchor: 'end' });
      const ref = (t) => y + h * (0.10 + 0.80 * t), gen = (t) => y + h * (0.12 + 0.62 * t + 0.20 * t ** 4);
      L.polyline(pa, L.sample(ref, 0.05, 0.95, 30).map(([t, yy]) => [x + w * t, yy]), { fill: 'none', stroke: '#6f6f6f', width: 0.7 });
      L.polyline(pa, L.sample(gen, 0.05, 0.95, 30).map(([t, yy]) => [x + w * t, yy]), { fill: 'none', stroke: K.E, width: 0.85, dash: '1.6 0.9' });
      L.text(pa, x + w * 0.36, y + m(1.8), S.ref, { size: 5.5, color: '#555555', anchor: 'start' });
      L.text(pa, x + w * 0.36, y + m(4.5), S.gen, { size: 5.5, color: K.E, anchor: 'start' });
      sub(6, S.evalSub);
    }

    // rails : catalogue (haut) et fichiers (bas)
    const RX0 = m(2), RX1 = m(181), CY0 = m(40.2), CH = m(5.6), FY0 = m(50.8), FH = m(5.6);
    L.rect(pa, RX0, CY0, RX1 - RX0, CH, { r: CH / 2, fill: K.cat, stroke: K.catEdge, width: 0.4 });
    L.rect(pa, RX0, FY0, RX1 - RX0, FH, { r: FH / 2, fill: K.fil, stroke: K.filEdge, width: 0.4 });
    dbGlyph(L, pa, m(4.6), CY0 + CH + m(2.5), m(2.6));
    L.text(pa, m(6.9), CY0 + CH + m(2.6), S.catRail, { size: 5.9, weight: 'bold', color: K.catInk, valign: 'middle' });
    folderGlyph(L, pa, m(4.6), FY0 + FH + m(2.5), m(2.8));
    L.text(pa, m(6.9), FY0 + FH + m(2.6), S.filRail, { size: 5.9, weight: 'bold', color: K.filInk, valign: 'middle' });
    const tables = ['campaign', 'simulation · job', 'diagnostic', 'file', 'dataset', 'model', 'evaluation'];
    for (let k = 0; k < 7; k++) {
      L.line(pa, [cx(k), MODY + m(1.0)], [cx(k), CY0], { stroke: K.catEdge, width: 0.5 });
      L.circle(pa, cx(k), CY0, m(0.55), { fill: K.catInk, stroke: 'none' });
      mono(L, pa, cx(k), CY0 + CH / 2, tables[k], { anchor: 'middle', valign: 'middle', size: 5.6, color: K.catInk });
    }
    for (const [k, s] of [[3, 'fields.h5'], [5, 'last.pt']]) {
      L.line(pa, [cx(k), CY0 + CH], [cx(k), FY0], { stroke: K.filEdge, width: 0.5 });
      L.circle(pa, cx(k), FY0, m(0.55), { fill: K.filInk, stroke: 'none' });
      mono(L, pa, cx(k), FY0 + FH / 2, s, { anchor: 'middle', valign: 'middle', size: 5.6, color: K.filInk });
    }
    L.text(pa, cx(3) + m(1.0), (CY0 + CH + FY0) / 2, S.sameId, { size: 5.5, italic: true, color: K.sub, valign: 'middle' });
    const ix = m(176.5);
    L.arrow(pa, [ix, FY0], [ix, CY0 + CH], { stroke: K.sub, width: 0.5, head: 1.8, dash: '1.4 0.8' });
    mono(L, pa, ix - m(1.0), (CY0 + CH + FY0) / 2, 'ingest', { anchor: 'end', valign: 'middle', size: 5.6, color: K.sub });

    // ------------------------------------------------------------------ panneau b
    const pb = F.panel('b', { x: 0, y: 63, w: 183, h: 53.4 });
    L.text(pb, 12, 7.6, S.b, { size: 7, weight: 'bold', color: K.ink, role: 'title' });
    const C0 = [26, 78.4, 130.8], CWB = 50.4, top = m(5.4), bot = m(52.6);
    const RY = [m(21.4), m(30.6), m(39.4), m(48.0)], RH = m(8.4);
    for (const [r, f] of [[1, K.fil], [2, K.cat]]) L.rect(pb, m(2), RY[r] - RH / 2, m(179), RH, { r: m(1.2), fill: f, stroke: 'none', opacity: 0.6 });
    const glyphs = [chipGlyph, folderGlyph, dbGlyph, trackGlyph];
    for (let r = 0; r < 4; r++) {
      glyphs[r](L, pb, m(5.2), RY[r], m(3.0));
      L.text(pb, m(8.4), RY[r], S.rows[r], { size: 6.4, weight: 'bold', color: K.ink, valign: 'middle' });
    }
    for (let c = 0; c < 3; c++) L.rect(pb, m(C0[c]), top, m(CWB), bot - top, { r: m(1.8), fill: 'none', stroke: K.frame, width: 0.6 });
    const hx = (c) => m(C0[c] + 10.2), hy = m(11.0);
    laptop(L, pb, m(C0[0] + 5.0), hy - m(0.6), m(6.2));
    cloud(L, pb, m(C0[1] + 5.1), hy - m(0.2), m(9.2), m(6.4));
    server(L, pb, m(C0[1] + 5.1), hy + m(0.2), m(3.4), { n: 2, gpu: true });
    for (let k = 0; k < 3; k++) server(L, pb, m(C0[2] + 2.2 + k * 2.6), hy, m(2.6), { n: 3, gpu: true });
    for (let c = 0; c < 3; c++) {
      L.text(pb, hx(c), hy - m(1.6), S.cols[c][0], { size: 6.7, weight: 'bold', color: K.ink, valign: 'middle' });
      L.text(pb, hx(c), hy + m(1.8), S.cols[c][1], { size: 5.8, color: K.sub, valign: 'middle' });
    }
    L.text(pb, m(C0[2] + 10.2), m(15.9), S.noNet, { size: 5.5, color: K.sub, valign: 'middle' });
    const cell = (c, r, lines, dx = 2.4) => {
      const x = m(C0[c] + dx), n = lines.length, gap = m(2.7);
      lines.forEach((ln, i) => {
        const y = RY[r] + (i - (n - 1) / 2) * gap;
        const o = { size: 6.0, valign: 'middle', color: K.ink, ...(ln.o || {}) };
        if (ln.mono) mono(L, pb, x, y, ln.s, o); else L.text(pb, x, y, ln.s, o);
      });
    };
    const small = { size: 5.5, color: K.sub };
    cell(0, 0, [{ s: S.venv }]);
    cell(0, 1, [{ s: 'data/store/', mono: true }]);
    cell(0, 2, [{ s: 'SQLite' }, { s: 'data/catalog.sqlite', mono: true, o: small }]);
    cell(0, 3, [{ s: 'metrics.jsonl', mono: true }]);
    cell(1, 0, [{ s: S.container }, { s: 'milady:gpu', mono: true, o: small }]);
    cell(1, 1, [{ s: 'MinIO  :9000' }]);
    cell(1, 2, [{ s: 'PostgreSQL 16  :5432' }]);
    cell(1, 3, [{ s: 'MLflow  :5000' }]);
    cell(2, 0, [{ s: S.array }, { s: S.gpuSim, o: small }, { s: S.torchrun, o: small }]);
    cell(2, 1, [{ s: '$SCRATCH', mono: true }], 18.0);
    cell(2, 2, [{ s: S.sqliteWork }]);
    cell(2, 3, [{ s: 'MLflow SQLite' }]);
    // synchronisations : copie des fichiers du cluster vers le stockage S3 de la VM, puis ingestion de ces
    // fichiers dans PostgreSQL (milady.catalog ingest lit les fichiers MFF, pas le catalogue SQLite du cluster)
    F.anchor('cl.fil', pb, m(C0[2] + 16.6), RY[1]); F.anchor('vm.fil', pb, m(C0[1] + CWB - 6.0), RY[1]);
    F.relate('cl.fil', 'vm.fil', 'sync');
    L.connect(F, 'cl.fil', 'vm.fil', { stroke: K.sub, width: 0.55, head: 1.9, dash: '1.4 0.8' });
    L.text(pb, m(C0[2] + 4.0), RY[1] - m(2.1), S.copyS3, { size: 5.5, color: K.sub, anchor: 'middle', valign: 'middle', halo: true });
    const ixb = m(C0[1] + 30.0);
    F.anchor('vm.fil.i', pb, ixb, RY[1] + m(1.9)); F.anchor('vm.cat.i', pb, ixb, RY[2] - m(1.9));
    F.relate('vm.fil.i', 'vm.cat.i', 'ingest');
    L.connect(F, 'vm.fil.i', 'vm.cat.i', { stroke: K.sub, width: 0.55, head: 1.9, dash: '1.4 0.8' });
    mono(L, pb, ixb + m(1.2), (RY[1] + RY[2]) / 2, 'ingest', { size: 5.5, color: K.sub, valign: 'middle', halo: true });
  };
}
